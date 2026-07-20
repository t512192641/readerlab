#!/usr/bin/env python3
"""Deterministic artifact boundary for a functional producer/judge run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import time
from pathlib import Path
from typing import Any


RUN_SCHEMA = "readerlab-functional-run/v1"
CANDIDATE_SCHEMA = "readerlab-functional-candidate/v1"
JUDGMENT_SCHEMA = "readerlab-functional-judgment/v1"
CANDIDATE_SEAL_SCHEMA = "readerlab-functional-candidate-seal/v1"
CANDIDATE_HANDOFF_SCHEMA = "readerlab-functional-candidate-handoff/v1"
JUDGMENT_SEAL_SCHEMA = "readerlab-functional-judgment-seal/v1"
HIDDEN_KEY_SCHEMA = "readerlab-functional-hidden-key/v1"
RECEIPT_SCHEMA = "readerlab-functional-receipt/v1"
VERDICTS = {"PASS", "FAIL"}

RUN_JSON = Path("run.json")
PRODUCER_SOURCE = Path("producer/input/source.md")
PRODUCER_BRIEF = Path("producer/input/brief.md")
PRODUCER_CANDIDATE = Path("producer/output/candidate.json")
CANDIDATE_SEAL = Path("producer/candidate-seal.json")
JUDGE_SOURCE = Path("judge/input/source.md")
JUDGE_CANDIDATE = Path("judge/input/candidate.json")
JUDGE_RUBRIC = Path("judge/input/rubric.md")
CANDIDATE_HANDOFF = Path("judge/candidate-handoff.json")
JUDGE_JUDGMENT = Path("judge/output/judgment.json")
JUDGMENT_SEAL = Path("judge/judgment-seal.json")
HIDDEN_KEY = Path("scorer/hidden-key.json")
RECEIPT = Path("receipt.json")

INIT_FILES = {RUN_JSON, PRODUCER_SOURCE, PRODUCER_BRIEF, JUDGE_RUBRIC}
CANDIDATE_FILES = INIT_FILES | {
    PRODUCER_CANDIDATE,
    CANDIDATE_SEAL,
    JUDGE_SOURCE,
    JUDGE_CANDIDATE,
    CANDIDATE_HANDOFF,
}
JUDGMENT_FILES = CANDIDATE_FILES | {JUDGE_JUDGMENT, JUDGMENT_SEAL}
SCORED_FILES = JUDGMENT_FILES | {HIDDEN_KEY, RECEIPT}


class RunError(Exception):
    """A contract violation that must stop the run."""


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    ensure_regular_file(path)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            raise RunError(f"symlink is forbidden: {current}")


def ensure_regular_file(path: Path) -> None:
    ensure_no_symlink_components(path)
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError as exc:
        raise RunError(f"required file is missing: {path}") from exc
    if not stat.S_ISREG(mode):
        raise RunError(f"expected a regular file: {path}")


def ensure_run_tree_safe(root: Path) -> None:
    ensure_no_symlink_components(root)
    if not root.is_dir():
        raise RunError(f"run directory is missing: {root}")
    for directory, names, files in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in names + files:
            item = base / name
            if item.is_symlink():
                raise RunError(f"symlink is forbidden: {item}")


def list_run_files(root: Path) -> set[Path]:
    result: set[Path] = set()
    for directory, _, files in os.walk(root, followlinks=False):
        base = Path(directory)
        for filename in files:
            result.add((base / filename).relative_to(root))
    return result


def require_exact_files(
    root: Path, allowed: set[Path], optional_outputs: set[Path] | None = None
) -> None:
    actual = list_run_files(root)
    accepted = allowed | (optional_outputs or set())
    extras = actual - accepted
    missing = allowed - actual
    if extras:
        raise RunError(
            "unexpected run files: " + ", ".join(sorted(str(path) for path in extras))
        )
    if missing:
        raise RunError(
            "required run files are missing: "
            + ", ".join(sorted(str(path) for path in missing))
        )


def load_json(path: Path) -> dict[str, Any]:
    ensure_regular_file(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RunError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise RunError(f"JSON root must be an object: {path}")
    return value


def require_keys(value: dict[str, Any], keys: set[str], label: str) -> None:
    actual = set(value)
    if actual != keys:
        raise RunError(
            f"{label} fields must be exactly {sorted(keys)}; got {sorted(actual)}"
        )


def require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RunError(f"{label} must be a non-empty string")
    return value


def require_string_list(value: Any, label: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise RunError(f"{label} must be a non-empty list of non-empty strings")
    return value


def validate_run(value: dict[str, Any]) -> dict[str, Any]:
    require_keys(
        value,
        {"schema", "candidate_id", "created_at_ns", "source_sha256",
         "brief_sha256", "rubric_sha256"},
        "run",
    )
    if value["schema"] != RUN_SCHEMA:
        raise RunError("run schema mismatch")
    require_nonempty_string(value["candidate_id"], "run candidate_id")
    if not isinstance(value["created_at_ns"], int) or value["created_at_ns"] <= 0:
        raise RunError("run created_at_ns must be a positive integer")
    for field in ("source_sha256", "brief_sha256", "rubric_sha256"):
        require_sha256(value[field], f"run {field}")
    return value


def validate_candidate(
    value: dict[str, Any], expected_candidate_id: str
) -> dict[str, Any]:
    require_keys(value, {"schema", "candidate_id", "claim", "evidence"}, "candidate")
    if value["schema"] != CANDIDATE_SCHEMA:
        raise RunError("candidate schema mismatch")
    if value["candidate_id"] != expected_candidate_id:
        raise RunError("candidate ID mismatch")
    require_nonempty_string(value["claim"], "candidate claim")
    require_string_list(value["evidence"], "candidate evidence")
    return value


def validate_judgment(
    value: dict[str, Any], expected_candidate_id: str
) -> dict[str, Any]:
    require_keys(
        value, {"schema", "candidate_id", "verdict", "reasons"}, "judgment"
    )
    if value["schema"] != JUDGMENT_SCHEMA:
        raise RunError("judgment schema mismatch")
    if value["candidate_id"] != expected_candidate_id:
        raise RunError("judgment candidate ID mismatch")
    if value["verdict"] not in VERDICTS:
        raise RunError("judgment verdict must be PASS or FAIL")
    require_string_list(value["reasons"], "judgment reasons")
    return value


def require_sha256(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise RunError(f"{label} must be a lowercase SHA-256")
    return value


def exclusive_write(path: Path, content: bytes) -> None:
    ensure_no_symlink_components(path.parent)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise RunError(f"refusing to overwrite: {path}") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        raise


def exclusive_copy(source: Path, target: Path) -> None:
    ensure_regular_file(source)
    exclusive_write(target, source.read_bytes())


def next_timestamp(after: int = 0) -> int:
    return max(time.time_ns(), after + 1)


def root_from(value: str) -> Path:
    root = Path(value).absolute()
    ensure_no_symlink_components(root)
    return root


def validate_fictional_source(path: Path) -> None:
    ensure_regular_file(path)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise RunError("source must be UTF-8 text") from exc
    first = next((line.strip() for line in lines if line.strip()), "")
    if first != "FICTIONAL TEST MATERIAL":
        raise RunError(
            "source must begin with the exact fictional marker: "
            "FICTIONAL TEST MATERIAL"
        )


def verify_initial_hashes(root: Path, run: dict[str, Any]) -> None:
    expected = {
        "source_sha256": sha256_file(root / PRODUCER_SOURCE),
        "brief_sha256": sha256_file(root / PRODUCER_BRIEF),
        "rubric_sha256": sha256_file(root / JUDGE_RUBRIC),
    }
    for field, value in expected.items():
        if run[field] != value:
            raise RunError(f"{field} mismatch")


def load_candidate_seal(root: Path, run: dict[str, Any]) -> dict[str, Any]:
    value = load_json(root / CANDIDATE_SEAL)
    keys = {
        "schema", "candidate_id", "sealed_at_ns", "source_sha256",
        "brief_sha256", "candidate_sha256",
    }
    require_keys(value, keys, "candidate seal")
    if value["schema"] != CANDIDATE_SEAL_SCHEMA:
        raise RunError("candidate seal schema mismatch")
    if value["candidate_id"] != run["candidate_id"]:
        raise RunError("candidate seal ID mismatch")
    if (
        not isinstance(value["sealed_at_ns"], int)
        or value["sealed_at_ns"] <= run["created_at_ns"]
    ):
        raise RunError("candidate seal timestamp is invalid")
    expected = {
        "source_sha256": sha256_file(root / PRODUCER_SOURCE),
        "brief_sha256": sha256_file(root / PRODUCER_BRIEF),
        "candidate_sha256": sha256_file(root / PRODUCER_CANDIDATE),
    }
    for field, actual in expected.items():
        require_sha256(value[field], f"candidate seal {field}")
        if value[field] != actual:
            raise RunError(f"candidate seal {field} mismatch")
    if value["source_sha256"] != run["source_sha256"]:
        raise RunError("candidate seal source does not match run")
    if value["brief_sha256"] != run["brief_sha256"]:
        raise RunError("candidate seal brief does not match run")
    return value


def load_candidate_handoff(
    root: Path, run: dict[str, Any], candidate_seal: dict[str, Any]
) -> dict[str, Any]:
    value = load_json(root / CANDIDATE_HANDOFF)
    keys = {
        "schema", "candidate_id", "created_at_ns", "source_sha256",
        "candidate_sha256",
    }
    require_keys(value, keys, "candidate handoff")
    if value["schema"] != CANDIDATE_HANDOFF_SCHEMA:
        raise RunError("candidate handoff schema mismatch")
    if value["candidate_id"] != run["candidate_id"]:
        raise RunError("candidate handoff ID mismatch")
    if (
        not isinstance(value["created_at_ns"], int)
        or value["created_at_ns"] <= candidate_seal["sealed_at_ns"]
    ):
        raise RunError("candidate handoff timestamp is invalid")
    source_sha = sha256_file(root / JUDGE_SOURCE)
    candidate_sha = sha256_file(root / JUDGE_CANDIDATE)
    if value["source_sha256"] != source_sha:
        raise RunError("candidate handoff source hash mismatch")
    if value["candidate_sha256"] != candidate_sha:
        raise RunError("candidate handoff candidate hash mismatch")
    if source_sha != candidate_seal["source_sha256"]:
        raise RunError("judge source is not an exact copy")
    if candidate_sha != candidate_seal["candidate_sha256"]:
        raise RunError("judge candidate is not an exact copy")
    return value


def load_judgment_seal(
    root: Path,
    run: dict[str, Any],
    candidate_seal: dict[str, Any],
    candidate_handoff: dict[str, Any],
) -> dict[str, Any]:
    value = load_json(root / JUDGMENT_SEAL)
    keys = {
        "schema", "candidate_id", "sealed_at_ns", "source_sha256",
        "candidate_sha256", "rubric_sha256", "judgment_sha256",
    }
    require_keys(value, keys, "judgment seal")
    if value["schema"] != JUDGMENT_SEAL_SCHEMA:
        raise RunError("judgment seal schema mismatch")
    if value["candidate_id"] != run["candidate_id"]:
        raise RunError("judgment seal ID mismatch")
    if (
        not isinstance(value["sealed_at_ns"], int)
        or value["sealed_at_ns"] <= candidate_handoff["created_at_ns"]
    ):
        raise RunError("judgment seal timestamp is invalid")
    expected = {
        "source_sha256": sha256_file(root / JUDGE_SOURCE),
        "candidate_sha256": sha256_file(root / JUDGE_CANDIDATE),
        "rubric_sha256": sha256_file(root / JUDGE_RUBRIC),
        "judgment_sha256": sha256_file(root / JUDGE_JUDGMENT),
    }
    for field, actual in expected.items():
        require_sha256(value[field], f"judgment seal {field}")
        if value[field] != actual:
            raise RunError(f"judgment seal {field} mismatch")
    if value["source_sha256"] != run["source_sha256"]:
        raise RunError("judgment source does not match run")
    if value["candidate_sha256"] != candidate_seal["candidate_sha256"]:
        raise RunError("judgment candidate does not match frozen candidate")
    if value["rubric_sha256"] != run["rubric_sha256"]:
        raise RunError("judgment rubric does not match run")
    return value


def init_run(args: argparse.Namespace) -> dict[str, Any]:
    root = root_from(args.run)
    if root.exists():
        raise RunError(f"refusing to overwrite existing run: {root}")
    source = Path(args.source).absolute()
    brief = Path(args.brief).absolute()
    rubric = Path(args.rubric).absolute()
    validate_fictional_source(source)
    ensure_regular_file(brief)
    ensure_regular_file(rubric)
    candidate_id = require_nonempty_string(args.candidate_id, "candidate_id")

    root.mkdir(parents=False)
    try:
        for directory in (
            PRODUCER_SOURCE.parent,
            PRODUCER_CANDIDATE.parent,
            JUDGE_RUBRIC.parent,
            JUDGE_JUDGMENT.parent,
            HIDDEN_KEY.parent,
        ):
            (root / directory).mkdir(parents=True, exist_ok=False)
        exclusive_copy(source, root / PRODUCER_SOURCE)
        exclusive_copy(brief, root / PRODUCER_BRIEF)
        exclusive_copy(rubric, root / JUDGE_RUBRIC)
        created_at = next_timestamp()
        value = {
            "schema": RUN_SCHEMA,
            "candidate_id": candidate_id,
            "created_at_ns": created_at,
            "source_sha256": sha256_file(root / PRODUCER_SOURCE),
            "brief_sha256": sha256_file(root / PRODUCER_BRIEF),
            "rubric_sha256": sha256_file(root / JUDGE_RUBRIC),
        }
        exclusive_write(root / RUN_JSON, canonical_json(value))
    except Exception:
        shutil.rmtree(root)
        raise
    return {"status": "initialized", "run": str(root), **value}


def seal_candidate(args: argparse.Namespace) -> dict[str, Any]:
    root = root_from(args.run)
    ensure_run_tree_safe(root)
    require_exact_files(root, INIT_FILES, {PRODUCER_CANDIDATE})
    if not (root / PRODUCER_CANDIDATE).exists():
        raise RunError("producer candidate must exist before sealing")
    if (root / HIDDEN_KEY).exists():
        raise RunError("hidden key appeared before judgment was frozen")
    run = validate_run(load_json(root / RUN_JSON))
    verify_initial_hashes(root, run)
    validate_candidate(load_json(root / PRODUCER_CANDIDATE), run["candidate_id"])
    sealed_at = next_timestamp(run["created_at_ns"])
    seal = {
        "schema": CANDIDATE_SEAL_SCHEMA,
        "candidate_id": run["candidate_id"],
        "sealed_at_ns": sealed_at,
        "source_sha256": run["source_sha256"],
        "brief_sha256": run["brief_sha256"],
        "candidate_sha256": sha256_file(root / PRODUCER_CANDIDATE),
    }
    exclusive_write(root / CANDIDATE_SEAL, canonical_json(seal))
    exclusive_copy(root / PRODUCER_SOURCE, root / JUDGE_SOURCE)
    exclusive_copy(root / PRODUCER_CANDIDATE, root / JUDGE_CANDIDATE)
    handoff = {
        "schema": CANDIDATE_HANDOFF_SCHEMA,
        "candidate_id": run["candidate_id"],
        "created_at_ns": next_timestamp(sealed_at),
        "source_sha256": sha256_file(root / JUDGE_SOURCE),
        "candidate_sha256": sha256_file(root / JUDGE_CANDIDATE),
    }
    exclusive_write(root / CANDIDATE_HANDOFF, canonical_json(handoff))
    return {"status": "candidate-sealed-and-handed-off", "seal": seal,
            "handoff": handoff}


def seal_judgment(args: argparse.Namespace) -> dict[str, Any]:
    root = root_from(args.run)
    ensure_run_tree_safe(root)
    require_exact_files(root, CANDIDATE_FILES, {JUDGE_JUDGMENT})
    if not (root / JUDGE_JUDGMENT).exists():
        raise RunError("judge judgment must exist before sealing")
    if (root / HIDDEN_KEY).exists():
        raise RunError("hidden key appeared before judgment was frozen")
    run = validate_run(load_json(root / RUN_JSON))
    verify_initial_hashes(root, run)
    candidate = validate_candidate(
        load_json(root / PRODUCER_CANDIDATE), run["candidate_id"]
    )
    validate_candidate(load_json(root / JUDGE_CANDIDATE), run["candidate_id"])
    candidate_seal = load_candidate_seal(root, run)
    candidate_handoff = load_candidate_handoff(root, run, candidate_seal)
    judgment = validate_judgment(
        load_json(root / JUDGE_JUDGMENT), run["candidate_id"]
    )
    sealed_at = next_timestamp(candidate_handoff["created_at_ns"])
    seal = {
        "schema": JUDGMENT_SEAL_SCHEMA,
        "candidate_id": run["candidate_id"],
        "sealed_at_ns": sealed_at,
        "source_sha256": sha256_file(root / JUDGE_SOURCE),
        "candidate_sha256": candidate_seal["candidate_sha256"],
        "rubric_sha256": sha256_file(root / JUDGE_RUBRIC),
        "judgment_sha256": sha256_file(root / JUDGE_JUDGMENT),
    }
    exclusive_write(root / JUDGMENT_SEAL, canonical_json(seal))
    return {
        "status": "judgment-sealed",
        "candidate_claim": candidate["claim"],
        "verdict": judgment["verdict"],
        **seal,
    }


def build_receipt(
    root: Path,
    run: dict[str, Any],
    candidate_seal: dict[str, Any],
    candidate_handoff: dict[str, Any],
    judgment_seal: dict[str, Any],
    hidden_key: dict[str, Any],
) -> dict[str, Any]:
    judgment = validate_judgment(
        load_json(root / JUDGE_JUDGMENT), run["candidate_id"]
    )
    comparison = (
        "PASS" if judgment["verdict"] == hidden_key["expected_verdict"] else "FAIL"
    )
    return {
        "schema": RECEIPT_SCHEMA,
        "candidate_id": run["candidate_id"],
        "inputs": {
            "producer_source": {
                "path": str(PRODUCER_SOURCE),
                "sha256": run["source_sha256"],
            },
            "producer_brief": {
                "path": str(PRODUCER_BRIEF),
                "sha256": run["brief_sha256"],
            },
            "judge_source": {
                "path": str(JUDGE_SOURCE),
                "sha256": judgment_seal["source_sha256"],
            },
            "judge_candidate": {
                "path": str(JUDGE_CANDIDATE),
                "sha256": judgment_seal["candidate_sha256"],
            },
            "judge_rubric": {
                "path": str(JUDGE_RUBRIC),
                "sha256": judgment_seal["rubric_sha256"],
            },
        },
        "artifacts": {
            "candidate": {
                "path": str(PRODUCER_CANDIDATE),
                "sha256": candidate_seal["candidate_sha256"],
            },
            "judgment": {
                "path": str(JUDGE_JUDGMENT),
                "sha256": judgment_seal["judgment_sha256"],
            },
        },
        "copy_relations": {
            "source_identical": (
                run["source_sha256"] == judgment_seal["source_sha256"]
            ),
            "candidate_identical": (
                candidate_seal["candidate_sha256"]
                == judgment_seal["candidate_sha256"]
            ),
        },
        "sequence": {
            "run_created_at_ns": run["created_at_ns"],
            "candidate_sealed_at_ns": candidate_seal["sealed_at_ns"],
            "candidate_handoff_at_ns": candidate_handoff["created_at_ns"],
            "judgment_sealed_at_ns": judgment_seal["sealed_at_ns"],
            "hidden_key_published_at_ns": hidden_key["published_at_ns"],
        },
        "mechanical_comparison": {
            "judge_verdict": judgment["verdict"],
            "expected_verdict": hidden_key["expected_verdict"],
            "result": comparison,
        },
    }


def validate_hidden_key(
    value: dict[str, Any], run: dict[str, Any], judgment_seal: dict[str, Any]
) -> dict[str, Any]:
    require_keys(
        value,
        {"schema", "candidate_id", "expected_verdict", "published_at_ns"},
        "hidden key",
    )
    if value["schema"] != HIDDEN_KEY_SCHEMA:
        raise RunError("hidden key schema mismatch")
    if value["candidate_id"] != run["candidate_id"]:
        raise RunError("hidden key candidate ID mismatch")
    if value["expected_verdict"] not in VERDICTS:
        raise RunError("hidden key expected_verdict must be PASS or FAIL")
    if (
        not isinstance(value["published_at_ns"], int)
        or value["published_at_ns"] <= judgment_seal["sealed_at_ns"]
    ):
        raise RunError("hidden key was not published after judgment seal")
    return value


def score(args: argparse.Namespace) -> dict[str, Any]:
    root = root_from(args.run)
    ensure_run_tree_safe(root)
    require_exact_files(root, JUDGMENT_FILES)
    if args.expected_verdict not in VERDICTS:
        raise RunError("expected verdict must be PASS or FAIL")
    run = validate_run(load_json(root / RUN_JSON))
    verify_initial_hashes(root, run)
    validate_candidate(load_json(root / PRODUCER_CANDIDATE), run["candidate_id"])
    validate_candidate(load_json(root / JUDGE_CANDIDATE), run["candidate_id"])
    candidate_seal = load_candidate_seal(root, run)
    candidate_handoff = load_candidate_handoff(root, run, candidate_seal)
    validate_judgment(load_json(root / JUDGE_JUDGMENT), run["candidate_id"])
    judgment_seal = load_judgment_seal(
        root, run, candidate_seal, candidate_handoff
    )
    hidden_key = {
        "schema": HIDDEN_KEY_SCHEMA,
        "candidate_id": run["candidate_id"],
        "expected_verdict": args.expected_verdict,
        "published_at_ns": next_timestamp(judgment_seal["sealed_at_ns"]),
    }
    exclusive_write(root / HIDDEN_KEY, canonical_json(hidden_key))
    receipt = build_receipt(
        root, run, candidate_seal, candidate_handoff, judgment_seal, hidden_key
    )
    exclusive_write(root / RECEIPT, canonical_json(receipt))
    return {
        "status": "scored",
        "result": receipt["mechanical_comparison"]["result"],
        "candidate_sha256": candidate_seal["candidate_sha256"],
        "judgment_sha256": judgment_seal["judgment_sha256"],
    }


def verify(args: argparse.Namespace) -> dict[str, Any]:
    root = root_from(args.run)
    ensure_run_tree_safe(root)
    require_exact_files(root, SCORED_FILES)
    run = validate_run(load_json(root / RUN_JSON))
    verify_initial_hashes(root, run)
    validate_fictional_source(root / PRODUCER_SOURCE)
    validate_candidate(load_json(root / PRODUCER_CANDIDATE), run["candidate_id"])
    validate_candidate(load_json(root / JUDGE_CANDIDATE), run["candidate_id"])
    candidate_seal = load_candidate_seal(root, run)
    candidate_handoff = load_candidate_handoff(root, run, candidate_seal)
    validate_judgment(load_json(root / JUDGE_JUDGMENT), run["candidate_id"])
    judgment_seal = load_judgment_seal(
        root, run, candidate_seal, candidate_handoff
    )
    hidden_key = validate_hidden_key(
        load_json(root / HIDDEN_KEY), run, judgment_seal
    )
    expected_receipt = build_receipt(
        root, run, candidate_seal, candidate_handoff, judgment_seal, hidden_key
    )
    actual_receipt = load_json(root / RECEIPT)
    if canonical_json(actual_receipt) != canonical_json(expected_receipt):
        raise RunError("receipt does not match recomputed evidence")
    sequence = expected_receipt["sequence"]
    if not (
        sequence["run_created_at_ns"]
        < sequence["candidate_sealed_at_ns"]
        < sequence["candidate_handoff_at_ns"]
        < sequence["judgment_sealed_at_ns"]
        < sequence["hidden_key_published_at_ns"]
    ):
        raise RunError("artifact sequence is invalid")
    if not all(expected_receipt["copy_relations"].values()):
        raise RunError("copy relation verification failed")
    return {
        "status": "verified",
        "result": expected_receipt["mechanical_comparison"]["result"],
        "candidate_sha256": candidate_seal["candidate_sha256"],
        "judgment_sha256": judgment_seal["judgment_sha256"],
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init")
    init_parser.add_argument("--run", required=True)
    init_parser.add_argument("--source", required=True)
    init_parser.add_argument("--brief", required=True)
    init_parser.add_argument("--rubric", required=True)
    init_parser.add_argument("--candidate-id", required=True)
    init_parser.set_defaults(handler=init_run)

    for name, handler in (
        ("seal-candidate", seal_candidate),
        ("seal-judgment", seal_judgment),
        ("verify", verify),
    ):
        command = commands.add_parser(name)
        command.add_argument("--run", required=True)
        command.set_defaults(handler=handler)

    score_parser = commands.add_parser("score")
    score_parser.add_argument("--run", required=True)
    score_parser.add_argument("--expected-verdict", required=True)
    score_parser.set_defaults(handler=score)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        output = args.handler(args)
    except (OSError, RunError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
