#!/usr/bin/env python3
"""Prepare and, only with a separate authorization receipt, run 18 formal Scouts."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path("/private/tmp/readerlab-new-route-20260726/discovery-isolation")
A_ROOT = ROOT / "checkpoint-a"
B_ROOT = ROOT / "checkpoint-b"
PLAN_PATH = B_ROOT / "protocol/run-plan.json"
RUNS_ROOT = B_ROOT / "formal-scout-runs"
AUTH_PATH = B_ROOT / "EXECUTION-AUTHORIZATION.json"
MANIFEST_PATH = B_ROOT / "audit/file-manifest.json"

EXPECTED_A_HASHES = {
    A_ROOT / "protocol/treatment-isolation-v0.1.md": "52ef7835ce7b9ccebab19da61449c54ede70d91ebbad4681262401fddae1e94a",
    A_ROOT / "protocol/prompts/scout-v0.md": "78fcc2f4a420bf460ec97c16f7d2e3c0614d641e1727fd9db7aef2039250b70f",
    A_ROOT / "protocol/prompts/scout-v1-prime.md": "585ec24f4060d524fc99889623f6fdfcb418c62c67e26e56ec29e488011aeca0",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if mode is not None:
        path.chmod(mode)


def assert_hash(path: Path, expected: str) -> None:
    actual = sha256(path.read_bytes())
    if actual != expected:
        raise RuntimeError(f"hash mismatch: {path}: {actual} != {expected}")


def load_and_validate_plan() -> dict[str, Any]:
    plan = read_json(PLAN_PATH)
    if plan.get("schema_version") != "formal-scout-run-plan.v0.1":
        raise RuntimeError("unexpected run plan schema version")
    if plan.get("model") != "gpt-5.4" or plan.get("reasoning_effort") != "medium":
        raise RuntimeError("model or effort drift")
    expected_flags = [
        "features.plugins=false",
        "features.apps=false",
        "skills.include_instructions=false",
    ]
    if plan.get("session_flags") != expected_flags:
        raise RuntimeError("session isolation flags drift")
    runs = plan.get("runs")
    if not isinstance(runs, list) or len(runs) != 18:
        raise RuntimeError("run plan must contain exactly 18 runs")
    if [run["sequence"] for run in runs] != list(range(1, 19)):
        raise RuntimeError("run sequence must be exactly 1..18")
    run_ids = [run["run_id"] for run in runs]
    if len(run_ids) != len(set(run_ids)):
        raise RuntimeError("duplicate run_id")
    for block in range(1, 10):
        members = [run for run in runs if run["block"] == block]
        if len(members) != 2:
            raise RuntimeError(f"block {block} does not have exactly two runs")
        if len({member["pair_id"] for member in members}) != 1:
            raise RuntimeError(f"block {block} pair mismatch")
        if {member["variant"] for member in members} != {"V0", "V1P"}:
            raise RuntimeError(f"block {block} variant mismatch")
        if len({member["material_id"] for member in members}) != 1:
            raise RuntimeError(f"block {block} material mismatch")
        if len({member["repeat"] for member in members}) != 1:
            raise RuntimeError(f"block {block} repeat mismatch")
    return plan


def validate_frozen_inputs(plan: dict[str, Any]) -> dict[str, str]:
    for path, expected in EXPECTED_A_HASHES.items():
        assert_hash(path, expected)
    for material in plan["frozen_inputs"].values():
        assert_hash(Path(material["source_path"]), material["source_sha256"])
    for variant in plan["variants"].values():
        assert_hash(Path(variant["prompt_path"]), variant["prompt_sha256"])
        schema = read_json(Path(variant["response_schema_path"]))
        jsonschema.Draft202012Validator.check_schema(schema)

    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("codex executable not found")
    version = subprocess.run(
        [codex, "--version"], check=False, capture_output=True, text=True
    )
    if version.returncode != 0:
        raise RuntimeError("codex --version failed")
    if version.stdout.strip() != plan["cli_version"]:
        raise RuntimeError(
            f"CLI drift: {version.stdout.strip()!r} != {plan['cli_version']!r}"
        )
    return {
        "codex_path": codex,
        "cli_version_stdout": version.stdout.strip(),
        "cli_version_stderr": version.stderr.strip(),
    }


def render_prompt(run: dict[str, Any], plan: dict[str, Any]) -> bytes:
    variant = plan["variants"][run["variant"]]
    template = Path(variant["prompt_path"]).read_bytes().decode("utf-8")
    source = (
        Path(plan["frozen_inputs"][run["material_id"]]["source_path"])
        .read_bytes()
        .decode("utf-8")
    )
    if template.count("{{RUN_ID}}") != 1:
        raise RuntimeError("prompt template RUN_ID placeholder drift")
    if template.count("{{EXACT_SOURCE_BYTES_UTF8}}") != 1:
        raise RuntimeError("prompt template source placeholder drift")
    rendered = template.replace("{{RUN_ID}}", run["run_id"]).replace(
        "{{EXACT_SOURCE_BYTES_UTF8}}", source
    )
    return rendered.encode("utf-8")


def command_for(
    codex: str,
    plan: dict[str, Any],
    run_dir: Path,
    attempt: int,
) -> list[str]:
    return [
        codex,
        "exec",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--model",
        plan["model"],
        "-c",
        f'model_reasoning_effort="{plan["reasoning_effort"]}"',
        "-c",
        "features.plugins=false",
        "-c",
        "features.apps=false",
        "-c",
        "skills.include_instructions=false",
        "--sandbox",
        "read-only",
        "--cd",
        str(run_dir / f"workdir-attempt-{attempt}"),
        "--skip-git-repo-check",
        "--output-schema",
        str(run_dir / "output-schema.json"),
        "-",
    ]


def prepare() -> dict[str, Any]:
    plan = load_and_validate_plan()
    client = validate_frozen_inputs(plan)
    RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    prepared = []
    for run in plan["runs"]:
        run_dir = RUNS_ROOT / f"{run['sequence']:02d}-{run['run_id']}"
        run_dir.mkdir(parents=True, exist_ok=True)
        workdir = run_dir / "workdir-attempt-1"
        workdir.mkdir(parents=True, exist_ok=True)
        if any(workdir.iterdir()):
            raise RuntimeError(f"Scout workdir is not empty: {workdir}")

        prompt = render_prompt(run, plan)
        prompt_path = run_dir / "prompt.txt"
        prompt_path.write_bytes(prompt)
        schema_source = Path(
            plan["variants"][run["variant"]]["response_schema_path"]
        )
        schema_path = run_dir / "output-schema.json"
        shutil.copyfile(schema_source, schema_path)

        semantic_request = {
            "prompt_sha256": sha256(prompt),
            "output_schema_sha256": sha256(schema_path.read_bytes()),
            "model": plan["model"],
            "reasoning_effort": plan["reasoning_effort"],
            "session_flags": plan["session_flags"],
            "source_sha256": plan["frozen_inputs"][run["material_id"]][
                "source_sha256"
            ],
        }
        read_set = {
            "schema_version": "scout-read-set.v0.1",
            "run_id": run["run_id"],
            "filesystem_workdir": str(workdir),
            "filesystem_workdir_files": [],
            "request_components": [
                {
                    "kind": "exact_user_prompt",
                    "path": str(prompt_path),
                    "sha256": semantic_request["prompt_sha256"],
                },
                {
                    "kind": "output_schema",
                    "path": str(schema_path),
                    "sha256": semantic_request["output_schema_sha256"],
                },
            ],
            "explicitly_excluded": [
                "checkpoint-a/inputs/audit",
                "checkpoint-a/inputs/prior-sidecar",
                "checkpoint-a/materials/MATERIALS.md",
                "all sibling materials",
                "all earlier or sibling run outputs",
            ],
        }
        write_json(run_dir / "read-set-manifest.json", read_set)
        preflight = {
            "schema_version": "scout-preflight.v0.1",
            **run,
            **client,
            "semantic_request_sha256": canonical_sha256(semantic_request),
            "semantic_request": semantic_request,
            "prepared_at_utc": utc_now(),
            "execution_authorized": False,
            "command_preview": command_for(
                client["codex_path"], plan, run_dir, attempt=1
            ),
        }
        write_json(run_dir / "preflight.json", preflight)
        prepared.append(
            {
                "sequence": run["sequence"],
                "run_id": run["run_id"],
                "semantic_request_sha256": preflight[
                    "semantic_request_sha256"
                ],
                "workdir_empty": True,
            }
        )
    receipt = {
        "schema_version": "formal-scout-prepare-receipt.v0.1",
        "prepared_at_utc": utc_now(),
        "run_plan_sha256": sha256(PLAN_PATH.read_bytes()),
        "run_count": len(prepared),
        "semantic_model_calls": 0,
        "runs": prepared,
    }
    write_json(RUNS_ROOT / "prepare-receipt.json", receipt)
    return receipt


def parse_events(stdout: bytes) -> tuple[list[Any], list[int]]:
    events = []
    malformed = []
    for index, line in enumerate(stdout.splitlines(), start=1):
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            malformed.append(index)
    return events, malformed


def extract_agent_message(events: list[Any]) -> str | None:
    messages = [
        event["item"]["text"]
        for event in events
        if isinstance(event, dict)
        and event.get("type") == "item.completed"
        and isinstance(event.get("item"), dict)
        and event["item"].get("type") == "agent_message"
        and isinstance(event["item"].get("text"), str)
    ]
    return messages[-1] if messages else None


def extract_usage(events: list[Any]) -> dict[str, int] | None:
    usages = [
        event["usage"]
        for event in events
        if isinstance(event, dict)
        and event.get("type") == "turn.completed"
        and isinstance(event.get("usage"), dict)
    ]
    return usages[-1] if usages else None


def classify_empty_failure(
    events: list[Any], stderr: bytes, plan: dict[str, Any]
) -> tuple[str, str | None]:
    event_text = json.dumps(events, ensure_ascii=False).lower()
    combined = event_text + "\n" + stderr.decode("utf-8", errors="replace").lower()
    retry_policy = plan["retry_policy"]
    for marker in retry_policy["nonretryable_precedence"]:
        if marker in combined:
            return "NONRETRYABLE_CONFIG_OR_REQUEST", marker
    for marker in retry_policy["retryable_transport_allowlist"]:
        if marker in combined:
            return "RETRYABLE_TRANSPORT", marker
    return "NONRETRYABLE_UNKNOWN", None


def validate_response(
    run: dict[str, Any], plan: dict[str, Any], response: Any
) -> dict[str, Any]:
    schema = read_json(Path(plan["variants"][run["variant"]]["response_schema_path"]))
    jsonschema.validate(response, schema)
    seed_batch = response if run["variant"] == "V0" else response["seed_batch"]
    if seed_batch["run_id"] != run["run_id"]:
        raise RuntimeError("response run_id mismatch")
    seed_ids = [seed["seed_id"] for seed in seed_batch["seeds"]]
    if len(seed_ids) != len(set(seed_ids)):
        raise RuntimeError("duplicate seed_id")
    source_text = Path(
        plan["frozen_inputs"][run["material_id"]]["source_path"]
    ).read_text(encoding="utf-8")
    for seed in seed_batch["seeds"]:
        if seed["source_anchor_quote_en"] not in source_text:
            raise RuntimeError(
                f"seed anchor not an exact source substring: {seed['seed_id']}"
            )
    if run["variant"] == "V1P":
        for trigger in response["trigger_map"]["triggers"]:
            if trigger["source_anchor_quote_en"] not in source_text:
                raise RuntimeError(
                    "trigger anchor not an exact source substring: "
                    + trigger["trigger_id"]
                )
    return seed_batch


def run_attempt(
    run: dict[str, Any],
    plan: dict[str, Any],
    client: dict[str, str],
    attempt: int,
) -> dict[str, Any]:
    run_dir = RUNS_ROOT / f"{run['sequence']:02d}-{run['run_id']}"
    attempt_dir = run_dir / f"attempt-{attempt}"
    if attempt_dir.exists():
        raise RuntimeError(f"refusing to overwrite existing attempt: {attempt_dir}")
    attempt_dir.mkdir(parents=True)
    workdir = run_dir / f"workdir-attempt-{attempt}"
    workdir.mkdir(parents=True, exist_ok=True)
    if any(workdir.iterdir()):
        raise RuntimeError(f"attempt workdir not empty: {workdir}")
    prompt = (run_dir / "prompt.txt").read_bytes()
    command = command_for(client["codex_path"], plan, run_dir, attempt)
    semantic_request_sha = read_json(run_dir / "preflight.json")[
        "semantic_request_sha256"
    ]
    request = {
        "schema_version": "formal-scout-request.v0.1",
        "run_id": run["run_id"],
        "attempt": attempt,
        "command_argv": command,
        "cli_version": client["cli_version_stdout"],
        "exact_prompt_sha256": sha256(prompt),
        "semantic_request_sha256": semantic_request_sha,
        "full_invocation_request_sha256": None,
    }
    request["full_invocation_request_sha256"] = canonical_sha256(
        {key: value for key, value in request.items() if key != "full_invocation_request_sha256"}
    )
    write_json(attempt_dir / "request.json", request)
    started = utc_now()
    result = subprocess.run(
        command, input=prompt, check=False, capture_output=True
    )
    ended = utc_now()
    (attempt_dir / "transcript.jsonl").write_bytes(result.stdout)
    (attempt_dir / "stderr.txt").write_bytes(result.stderr)
    events, malformed = parse_events(result.stdout)
    message = extract_agent_message(events)
    usage = extract_usage(events)

    status = "INFRASTRUCTURE_FAILURE"
    error = None
    seed_batch = None
    if result.returncode == 0 and message is not None:
        try:
            response = json.loads(message)
            seed_batch = validate_response(run, plan, response)
            write_json(attempt_dir / "response.json", response)
            status = "VALID"
        except (json.JSONDecodeError, jsonschema.ValidationError, RuntimeError) as exc:
            error = f"{type(exc).__name__}: {exc}"
            status = "MODEL_CONTRACT_FAILURE"
    elif message is not None or usage is not None:
        status = "PARTIAL_FAILURE"
        error = "nonzero exit or missing final response after observable model activity"
    else:
        error = "no agent message and no usage"

    failure_class = None
    failure_marker = None
    if status == "INFRASTRUCTURE_FAILURE" and message is None and usage is None:
        failure_class, failure_marker = classify_empty_failure(
            events, result.stderr, plan
        )
    retry_allowed = (
        status == "INFRASTRUCTURE_FAILURE"
        and failure_class == "RETRYABLE_TRANSPORT"
        and attempt == 1
    )
    receipt = {
        "schema_version": "formal-scout-attempt-receipt.v0.1",
        "run_id": run["run_id"],
        "attempt": attempt,
        "started_at_utc": started,
        "ended_at_utc": ended,
        "exit_code": result.returncode,
        "status": status,
        "error": error,
        "failure_class": failure_class,
        "failure_marker": failure_marker,
        "retry_allowed": retry_allowed,
        "semantic_request_sha256": semantic_request_sha,
        "prompt_sha256": sha256(prompt),
        "transcript_sha256": sha256(result.stdout),
        "stderr_sha256": sha256(result.stderr),
        "malformed_jsonl_lines": malformed,
        "agent_message_observed": message is not None,
        "provider_usage": usage,
        "resolved_backend_snapshot": "unknown",
        "exact_system_prompt": "unknown",
        "provider_billed_cost": "unknown",
    }
    write_json(attempt_dir / "receipt.json", receipt)

    if status == "VALID":
        downstream_dir = run_dir / "downstream"
        downstream_dir.mkdir(exist_ok=False)
        write_json(downstream_dir / "seed-batch.json", seed_batch)
        if run["variant"] == "V1P":
            response = read_json(attempt_dir / "response.json")
            sealed_dir = run_dir / "sealed"
            sealed_dir.mkdir(exist_ok=False)
            trigger_bytes = (
                json.dumps(
                    response["trigger_map"], ensure_ascii=False, indent=2
                )
                + "\n"
            ).encode("utf-8")
            trigger_path = sealed_dir / "trigger-map.json"
            trigger_path.write_bytes(trigger_bytes)
            trigger_path.chmod(0o600)
            write_json(
                sealed_dir / "seal-receipt.json",
                {
                    "run_id": run["run_id"],
                    "trigger_map_sha256": sha256(trigger_bytes),
                    "downstream_allowlist": ["../downstream/seed-batch.json"],
                    "downstream_must_not_read": ["trigger-map.json"],
                },
                mode=0o600,
            )
    return receipt


def validate_freeze_manifest() -> str:
    if not MANIFEST_PATH.exists():
        raise RuntimeError(f"missing Checkpoint B freeze manifest: {MANIFEST_PATH}")
    manifest = read_json(MANIFEST_PATH)
    if manifest.get("root") != str(B_ROOT):
        raise RuntimeError("Checkpoint B manifest root mismatch")
    if manifest.get("excludes_self") != "audit/file-manifest.json":
        raise RuntimeError("manifest must exclude itself")
    if "EXECUTION-AUTHORIZATION.json" not in manifest.get(
        "explicitly_excluded", []
    ):
        raise RuntimeError("manifest must explicitly exclude authorization receipt")
    for record in manifest["files"]:
        path = B_ROOT / record["path"]
        if not path.is_file():
            raise RuntimeError(f"frozen file missing: {path}")
        if sha256(path.read_bytes()) != record["sha256"]:
            raise RuntimeError(f"frozen file hash drift: {path}")
    return sha256(MANIFEST_PATH.read_bytes())


def require_authorization() -> None:
    if not AUTH_PATH.exists():
        raise RuntimeError(
            f"semantic execution is not authorized; missing {AUTH_PATH}"
        )
    auth = read_json(AUTH_PATH)
    expected_plan = sha256(PLAN_PATH.read_bytes())
    expected_manifest = validate_freeze_manifest()
    if auth != {
        "authorized": True,
        "scope": "18-scout-semantic-run",
        "run_plan_sha256": expected_plan,
        "checkpoint_b_manifest_sha256": expected_manifest,
    }:
        raise RuntimeError("execution authorization receipt is invalid or stale")


def execute() -> dict[str, Any]:
    require_authorization()
    plan = load_and_validate_plan()
    client = validate_frozen_inputs(plan)
    if not (RUNS_ROOT / "prepare-receipt.json").exists():
        raise RuntimeError("run prepare before execute")
    run_results = []
    incomplete_pairs: set[str] = set()
    for run in plan["runs"]:
        first = run_attempt(run, plan, client, attempt=1)
        final = first
        if first["retry_allowed"]:
            final = run_attempt(run, plan, client, attempt=2)
        if final["status"] != "VALID":
            incomplete_pairs.add(run["pair_id"])
        run_results.append(
            {
                "sequence": run["sequence"],
                "run_id": run["run_id"],
                "pair_id": run["pair_id"],
                "final_status": final["status"],
            }
        )
    receipt = {
        "schema_version": "formal-scout-execution-receipt.v0.1",
        "completed_at_utc": utc_now(),
        "run_plan_sha256": sha256(PLAN_PATH.read_bytes()),
        "runs": run_results,
        "incomplete_pairs": sorted(incomplete_pairs),
        "counting_rule": "exclude both sides of every incomplete pair",
    }
    write_json(RUNS_ROOT / "execution-receipt.json", receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare", "execute"])
    args = parser.parse_args()
    result = prepare() if args.action == "prepare" else execute()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
