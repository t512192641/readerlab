#!/usr/bin/env python3
"""Create, freeze, and deterministically check a lightweight ReaderLab run.

Single-writer contract: during each command, the explicit root, material path,
and run directory are writable only by the current caller. External concurrent
writes are outside this deliberately lightweight three-command skeleton.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath


RUN_SCHEMA = "readerlab-run/v2"
PRODUCTION_FREEZE_SCHEMA = "readerlab-production-freeze/v1"
ACCEPTANCE_FREEZE_SCHEMA = "readerlab-acceptance-freeze/v1"
METADATA_NAME = "run.json"
PRODUCTION_FREEZE_NAME = "production-freeze.json"
ACCEPTANCE_DIRECTORY = "acceptance"
ACCEPTANCE_FREEZE_NAME = "acceptance-freeze.json"
ACCEPTANCE_FREEZE_PATH = f"{ACCEPTANCE_DIRECTORY}/{ACCEPTANCE_FREEZE_NAME}"
ROOT_RECEIPT_NAME = "freeze-receipt.md"
FINAL_RECEIPT_PATH = "final/freeze-receipt.md"
PRODUCTION_DIRECTORIES = ("raw", "locked", "final")
PREDICTIONS_NAME = "judge-predictions.md"
ACCEPTANCE_REPORT_NAME = "acceptance-report.md"
PRODUCT_VERDICTS_NAME = "product-verdicts.md"
FROZEN_ACCEPTANCE_NAMES = (PREDICTIONS_NAME, ACCEPTANCE_REPORT_NAME)
SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
T31_RECEIPT_BINDING = re.compile(
    r"^t3\.1-freeze-receipt-sha256: (?P<sha256>[0-9a-f]{64})$",
    flags=re.MULTILINE,
)
STATE_HEADER = re.compile(
    r"\A(?:---\n)?"
    r"status: (?P<status>draft|frozen)\n"
    r"scope: (?P<scope>long-term|run-only)\n"
    r"(?:---\n)?"
)


class RunError(Exception):
    """A deterministic run-contract failure."""


def _lexists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


def _require_text(value: str, label: str) -> str:
    value = value.strip()
    if not value:
        raise RunError(f"{label} must be explicitly provided")
    return value


def _require_regular_file(path: Path, label: str) -> None:
    if path.is_symlink():
        raise RunError(f"{label} must not be a symlink: {path}")
    if not path.is_file():
        raise RunError(f"{label} must be an existing regular file: {path}")


def _resolve_real_directory(path: Path, label: str) -> Path:
    if path.is_symlink():
        raise RunError(f"{label} must not be a symlink: {path}")
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise RunError(f"{label} does not exist: {path}") from error
    if not resolved.is_dir():
        raise RunError(f"{label} must be a directory: {path}")
    return resolved


def _require_within(root: Path, path: Path, label: str) -> Path:
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise RunError(f"{label} escapes explicit root: {path}") from error
    if not relative.parts:
        raise RunError(f"{label} must be below explicit root: {path}")
    return relative


def _resolve_new_target(root: Path, path: Path) -> Path:
    if _lexists(path):
        raise RunError(f"refusing to overwrite existing run path: {path}")
    if path.name in {"", ".", ".."}:
        raise RunError(f"run path must name a new directory: {path}")
    if path.parent.is_symlink():
        raise RunError(f"run parent must not be a symlink: {path.parent}")
    parent = _resolve_real_directory(path.parent, "run parent")
    target = parent / path.name
    _require_within(root, target, "run path")
    return target


def _resolve_new_material(root: Path, path: Path) -> tuple[Path, str]:
    _require_regular_file(path, "material")
    try:
        material = path.resolve(strict=True)
    except OSError as error:
        raise RunError(f"material missing / 材料丢失: {path}") from error
    relative = _require_within(root, material, "material")
    return material, relative.as_posix()


def _sha256_and_size(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        before = os.fstat(handle.fileno())
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
        after = os.fstat(handle.fileno())

    identity_before = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    identity_after = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if identity_before != identity_after:
        raise RunError(f"file changed while hashing: {path}")
    return digest.hexdigest(), before.st_size


def _write_json_exclusive(path: Path, value: dict[str, object]) -> None:
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as error:
        raise RunError(f"refusing to overwrite existing file: {path}") from error


def _read_json_object(path: Path, label: str) -> dict[str, object]:
    _require_regular_file(path, label)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RunError(f"{label} is not valid UTF-8 JSON: {path}") from error
    if not isinstance(value, dict):
        raise RunError(f"{label} must contain a JSON object: {path}")
    return value


def _resolve_run_directory(path: Path) -> Path:
    run_dir = _resolve_real_directory(path, "run directory")
    _require_regular_file(run_dir / METADATA_NAME, "run metadata")

    required_directories = (*PRODUCTION_DIRECTORIES, ACCEPTANCE_DIRECTORY)
    for name in required_directories:
        directory = run_dir / name
        if directory.is_symlink() or not directory.is_dir():
            raise RunError(f"missing real isolated directory: {directory}")

    allowed_names = {
        METADATA_NAME,
        PRODUCTION_FREEZE_NAME,
        ROOT_RECEIPT_NAME,
        *required_directories,
    }
    for child in run_dir.iterdir():
        if child.name not in allowed_names:
            raise RunError(f"unexpected path at run root: {child.name}")
        if child.is_symlink():
            raise RunError(f"symlink forbidden at run root: {child.name}")
        if child.name == PRODUCTION_FREEZE_NAME and not child.is_file():
            raise RunError(f"production freeze must be a regular file: {child}")
        if child.name == ROOT_RECEIPT_NAME and not child.is_file():
            raise RunError(f"root freeze receipt must be a regular file: {child}")
    return run_dir


def _relative_material_reference(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise RunError("material relative path is missing")
    reference = PurePosixPath(value)
    if (
        reference.is_absolute()
        or reference.as_posix() != value
        or any(part in {"", ".", ".."} for part in reference.parts)
    ):
        raise RunError(f"material path is not root-bound relative: {value!r}")
    return value


def _validate_metadata(run_dir: Path) -> tuple[dict[str, object], Path, str]:
    metadata = _read_json_object(run_dir / METADATA_NAME, "run metadata")
    expected_keys = {
        "schema",
        "route",
        "source",
        "scope",
        "root_from_run",
        "material",
        "directories",
    }
    if set(metadata) != expected_keys:
        raise RunError("run metadata keys do not match the run contract")
    if metadata["schema"] != RUN_SCHEMA:
        raise RunError(f"unsupported run schema: {metadata['schema']!r}")
    if metadata["route"] not in {"book", "skills"}:
        raise RunError(f"invalid material route: {metadata['route']!r}")
    if not isinstance(metadata["source"], str) or not metadata["source"].strip():
        raise RunError("run source is not explicitly confirmed")
    if not isinstance(metadata["scope"], str) or not metadata["scope"].strip():
        raise RunError("run scope is not explicitly confirmed")
    if metadata["directories"] != {
        "production": list(PRODUCTION_DIRECTORIES),
        "acceptance": ACCEPTANCE_DIRECTORY,
    }:
        raise RunError("run directory isolation contract does not match")

    root_from_run = metadata["root_from_run"]
    if not isinstance(root_from_run, str) or not root_from_run:
        raise RunError("run root binding is missing")
    root_reference = PurePosixPath(root_from_run)
    if (
        root_reference.is_absolute()
        or root_reference.as_posix() != root_from_run
        or not root_reference.parts
        or any(part != ".." for part in root_reference.parts)
    ):
        raise RunError(f"run root binding is invalid: {root_from_run!r}")
    try:
        root = run_dir.joinpath(*root_reference.parts).resolve(strict=True)
    except OSError as error:
        raise RunError("run root binding cannot be resolved") from error
    if not root.is_dir():
        raise RunError("run root binding is not a directory")
    run_relative = _require_within(root, run_dir, "run directory")
    canonical_root_reference = "/".join(".." for _ in run_relative.parts)
    if root_from_run != canonical_root_reference:
        raise RunError("run root binding is not canonical")

    material = metadata["material"]
    if not isinstance(material, dict) or set(material) != {"path", "sha256", "bytes"}:
        raise RunError("material identity does not match the run contract")
    material_relative = _relative_material_reference(material["path"])
    if not isinstance(material["sha256"], str) or not SHA256.fullmatch(
        material["sha256"]
    ):
        raise RunError("material sha256 is invalid")
    if (
        isinstance(material["bytes"], bool)
        or not isinstance(material["bytes"], int)
        or material["bytes"] < 0
    ):
        raise RunError("material byte count is invalid")
    return metadata, root, material_relative


def _material_error(kind: str, relative: str, detail: str = "") -> RunError:
    labels = {
        "missing": "material missing / 材料丢失",
        "changed": "material changed / 材料被改",
    }
    suffix = f": {detail}" if detail else ""
    return RunError(f"{labels[kind]}: {relative}{suffix}")


def _verify_material(
    metadata: dict[str, object], root: Path, material_relative: str
) -> None:
    material = metadata["material"]
    if not isinstance(material, dict):
        raise RunError("material identity does not match the run contract")
    reference = PurePosixPath(material_relative)
    candidate = root.joinpath(*reference.parts)
    if not _lexists(candidate):
        raise _material_error("missing", material_relative)

    cursor = root
    for part in reference.parts:
        cursor /= part
        if cursor.is_symlink():
            raise _material_error(
                "changed", material_relative, "material path became a symlink"
            )
    if not candidate.is_file():
        raise _material_error(
            "changed", material_relative, "material is no longer a regular file"
        )
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
        observed_sha256, observed_bytes = _sha256_and_size(candidate)
    except FileNotFoundError as error:
        raise _material_error("missing", material_relative) from error
    except (OSError, RunError, ValueError) as error:
        raise _material_error(
            "changed", material_relative, "material cannot be verified inside root"
        ) from error

    expected_sha256 = material["sha256"]
    expected_bytes = material["bytes"]
    if observed_sha256 != expected_sha256 or observed_bytes != expected_bytes:
        raise _material_error(
            "changed",
            material_relative,
            (
                f"expected bytes={expected_bytes} sha256={expected_sha256}; "
                f"observed bytes={observed_bytes} sha256={observed_sha256}"
            ),
        )


def _load_context(
    run_path: Path,
) -> tuple[Path, dict[str, object], Path, str]:
    run_dir = _resolve_run_directory(run_path)
    metadata, root, material_relative = _validate_metadata(run_dir)
    return run_dir, metadata, root, material_relative


def _file_record(path: Path, run_dir: Path) -> dict[str, object]:
    file_sha256, byte_count = _sha256_and_size(path)
    return {
        "path": path.relative_to(run_dir).as_posix(),
        "sha256": file_sha256,
        "bytes": byte_count,
    }


def _production_snapshot(
    run_dir: Path,
) -> tuple[list[str], list[dict[str, object]]]:
    directories: list[str] = []
    files = [_file_record(run_dir / METADATA_NAME, run_dir)]
    for name in PRODUCTION_DIRECTORIES:
        root = run_dir / name
        directories.append(name)
        for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
            relative = path.relative_to(run_dir).as_posix()
            if path.is_symlink():
                raise RunError(f"symlink forbidden in production: {relative}")
            if path.is_dir():
                directories.append(relative)
            elif path.is_file():
                files.append(_file_record(path, run_dir))
            else:
                raise RunError(f"non-regular path forbidden in production: {relative}")
    return sorted(directories), sorted(files, key=lambda item: str(item["path"]))


def _verify_final_receipt_binding(
    run_dir: Path, *, require_when_root_exists: bool
) -> None:
    root_receipt = run_dir / ROOT_RECEIPT_NAME
    final_receipt = run_dir / FINAL_RECEIPT_PATH
    root_exists = _lexists(root_receipt)
    final_exists = _lexists(final_receipt)

    if not root_exists:
        if final_exists:
            raise RunError(
                f"final freeze receipt requires root receipt: {ROOT_RECEIPT_NAME}"
            )
        return
    _require_regular_file(root_receipt, "T3.1 root freeze receipt")

    if not final_exists:
        if require_when_root_exists:
            raise RunError(
                "final freeze receipt missing for T3.1 root receipt: "
                f"{FINAL_RECEIPT_PATH}"
            )
        return
    _require_regular_file(final_receipt, "T3.6 final freeze receipt")
    try:
        text = final_receipt.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise RunError(
            f"T3.6 final freeze receipt is not readable UTF-8: {final_receipt}"
        ) from error
    matches = list(T31_RECEIPT_BINDING.finditer(text))
    if len(matches) != 1:
        raise RunError(
            "final freeze receipt requires exactly one binding field: "
            "t3.1-freeze-receipt-sha256: <64 lowercase hex>"
        )

    expected_sha256, _ = _sha256_and_size(root_receipt)
    observed_sha256 = matches[0].group("sha256")
    if observed_sha256 != expected_sha256:
        raise RunError(
            "final freeze receipt binding mismatch: "
            f"expected {expected_sha256}, observed {observed_sha256}"
        )


def _expected_production_freeze(
    context: tuple[Path, dict[str, object], Path, str]
) -> dict[str, object]:
    run_dir, metadata, root, material_relative = context
    _verify_material(metadata, root, material_relative)
    _verify_final_receipt_binding(run_dir, require_when_root_exists=True)
    directories, files = _production_snapshot(run_dir)
    return {
        "schema": PRODUCTION_FREEZE_SCHEMA,
        "run_schema": RUN_SCHEMA,
        "scope": "production",
        "directories": directories,
        "files": files,
    }


def _records_by_path(records: list[object]) -> dict[str, object]:
    result: dict[str, object] = {}
    for record in records:
        if isinstance(record, dict) and isinstance(record.get("path"), str):
            result[record["path"]] = record
    return result


def _records_difference(actual: object, expected: object) -> list[str]:
    if not isinstance(actual, list) or not isinstance(expected, list):
        return ["file records changed"]
    actual_by_path = _records_by_path(actual)
    expected_by_path = _records_by_path(expected)
    missing = sorted(actual_by_path.keys() - expected_by_path.keys())
    added = sorted(expected_by_path.keys() - actual_by_path.keys())
    changed = sorted(
        path
        for path in actual_by_path.keys() & expected_by_path.keys()
        if actual_by_path[path] != expected_by_path[path]
    )
    details: list[str] = []
    if missing:
        details.append(f"missing={missing}")
    if added:
        details.append(f"added={added}")
    if changed:
        details.append(f"changed={changed}")
    return details


def _manifest_difference(
    actual: dict[str, object], expected: dict[str, object]
) -> str:
    details = _records_difference(actual.get("files"), expected.get("files"))
    actual_directories = actual.get("directories")
    expected_directories = expected.get("directories")
    if isinstance(expected_directories, list):
        if not isinstance(actual_directories, list):
            details.append("directory records changed")
        else:
            missing_directories = sorted(
                set(actual_directories) - set(expected_directories)
            )
            added_directories = sorted(
                set(expected_directories) - set(actual_directories)
            )
            if missing_directories:
                details.append(f"missing directories={missing_directories}")
            if added_directories:
                details.append(f"added directories={added_directories}")

    actual_metadata = {
        key: value for key, value in actual.items() if key not in {"files", "directories"}
    }
    expected_metadata = {
        key: value
        for key, value in expected.items()
        if key not in {"files", "directories"}
    }
    if actual_metadata != expected_metadata:
        details.append("freeze manifest metadata changed")
    return ", ".join(details) or "freeze manifest structure changed"


def _acceptance_entries(run_dir: Path) -> dict[str, Path]:
    acceptance_dir = run_dir / ACCEPTANCE_DIRECTORY
    entries: dict[str, Path] = {}
    for path in sorted(acceptance_dir.iterdir(), key=lambda item: item.name):
        relative = path.relative_to(run_dir).as_posix()
        if path.is_symlink():
            raise RunError(f"symlink forbidden in acceptance: {relative}")
        if not path.is_file():
            raise RunError(f"non-regular path forbidden in acceptance: {relative}")
        entries[path.name] = path
    return entries


def _require_acceptance_empty(run_dir: Path) -> None:
    entries = _acceptance_entries(run_dir)
    if entries:
        raise RunError(
            "acceptance sequence violation: production freeze required before "
            f"acceptance files: {sorted(entries)}"
        )


def _validate_open_acceptance(run_dir: Path) -> dict[str, Path]:
    entries = _acceptance_entries(run_dir)
    if PRODUCT_VERDICTS_NAME in entries:
        raise RunError(
            "acceptance sequence violation: product verdict requires acceptance freeze"
        )
    unexpected = sorted(set(entries) - set(FROZEN_ACCEPTANCE_NAMES))
    if unexpected:
        raise RunError(
            f"unexpected acceptance path before acceptance freeze: {unexpected}"
        )
    return entries


def _validate_frozen_acceptance(run_dir: Path) -> dict[str, Path]:
    entries = _acceptance_entries(run_dir)
    allowed = {
        *FROZEN_ACCEPTANCE_NAMES,
        ACCEPTANCE_FREEZE_NAME,
        PRODUCT_VERDICTS_NAME,
    }
    unexpected = sorted(set(entries) - allowed)
    if unexpected:
        raise RunError(f"unexpected path after acceptance freeze: {unexpected}")
    return entries


def _acceptance_file_records(
    run_dir: Path, entries: dict[str, Path]
) -> list[dict[str, object]]:
    missing = sorted(set(FROZEN_ACCEPTANCE_NAMES) - set(entries))
    if missing:
        raise RunError(f"acceptance freeze requires files: {missing}")
    return [
        _file_record(entries[name], run_dir) for name in FROZEN_ACCEPTANCE_NAMES
    ]


def _verify_production_freeze(
    context: tuple[Path, dict[str, object], Path, str]
) -> tuple[int, str, int]:
    run_dir = context[0]
    freeze_path = run_dir / PRODUCTION_FREEZE_NAME
    actual = _read_json_object(freeze_path, "production freeze manifest")
    expected = _expected_production_freeze(context)
    if actual != expected:
        raise RunError(
            "production frozen check failed: "
            f"{_manifest_difference(actual, expected)}"
        )
    freeze_sha256, freeze_bytes = _sha256_and_size(freeze_path)
    files = expected["files"]
    if not isinstance(files, list):
        raise RunError("internal production freeze record error")
    return len(files), freeze_sha256, freeze_bytes


def _expected_acceptance_freeze(
    run_dir: Path,
    entries: dict[str, Path],
    production_sha256: str,
    production_bytes: int,
) -> dict[str, object]:
    return {
        "schema": ACCEPTANCE_FREEZE_SCHEMA,
        "run_schema": RUN_SCHEMA,
        "scope": "acceptance",
        "production_freeze": {
            "path": PRODUCTION_FREEZE_NAME,
            "sha256": production_sha256,
            "bytes": production_bytes,
        },
        "files": _acceptance_file_records(run_dir, entries),
    }


def _verify_acceptance_freeze(
    context: tuple[Path, dict[str, object], Path, str],
    production_identity: tuple[str, int] | None = None,
) -> int:
    run_dir = context[0]
    if production_identity is None:
        _, production_sha256, production_bytes = _verify_production_freeze(context)
    else:
        production_sha256, production_bytes = production_identity
    entries = _validate_frozen_acceptance(run_dir)
    freeze_path = run_dir / ACCEPTANCE_FREEZE_PATH
    actual = _read_json_object(freeze_path, "acceptance freeze manifest")
    expected = _expected_acceptance_freeze(
        run_dir, entries, production_sha256, production_bytes
    )
    if actual != expected:
        raise RunError(
            "acceptance frozen check failed: "
            f"{_manifest_difference(actual, expected)}"
        )
    files = expected["files"]
    if not isinstance(files, list):
        raise RunError("internal acceptance freeze record error")
    return len(files)


def _check_state_header(path: Path) -> tuple[str, str]:
    _require_regular_file(path, "state file")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise RunError(f"state file is not readable UTF-8: {path}") from error
    match = STATE_HEADER.match(text)
    if match is None:
        raise RunError(f"missing valid status/scope header: {path}")
    return match.group("status"), match.group("scope")


def _new_run(args: argparse.Namespace) -> None:
    root = _resolve_real_directory(args.root, "explicit root")
    run_dir = _resolve_new_target(root, args.run_dir)
    material, material_relative = _resolve_new_material(root, args.material)
    source = _require_text(args.source, "source")
    scope = _require_text(args.scope, "scope")
    material_sha256, material_bytes = _sha256_and_size(material)
    run_relative = _require_within(root, run_dir, "run path")
    root_from_run = "/".join(".." for _ in run_relative.parts)
    metadata: dict[str, object] = {
        "schema": RUN_SCHEMA,
        "route": args.route,
        "source": source,
        "scope": scope,
        "root_from_run": root_from_run,
        "material": {
            "path": material_relative,
            "sha256": material_sha256,
            "bytes": material_bytes,
        },
        "directories": {
            "production": list(PRODUCTION_DIRECTORIES),
            "acceptance": ACCEPTANCE_DIRECTORY,
        },
    }

    try:
        run_dir.mkdir()
    except FileExistsError as error:
        raise RunError(f"refusing to overwrite existing run path: {run_dir}") from error
    for name in (*PRODUCTION_DIRECTORIES, ACCEPTANCE_DIRECTORY):
        (run_dir / name).mkdir()
    _write_json_exclusive(run_dir / METADATA_NAME, metadata)

    context = _load_context(run_dir)
    _verify_material(context[1], context[2], context[3])
    if context[1] != metadata:
        raise RunError("new run postflight metadata mismatch")
    print(
        f"new: created {run_dir} "
        f"(material={material_relative}, sha256={material_sha256})"
    )


def _freeze_production(
    context: tuple[Path, dict[str, object], Path, str]
) -> None:
    run_dir = context[0]
    freeze_path = run_dir / PRODUCTION_FREEZE_NAME
    if _lexists(freeze_path):
        raise RunError(f"refusing to overwrite existing file: {freeze_path}")
    _require_acceptance_empty(run_dir)
    manifest = _expected_production_freeze(context)
    _write_json_exclusive(freeze_path, manifest)
    file_count, _, _ = _verify_production_freeze(context)
    print(f"freeze: wrote {freeze_path} ({file_count} production files)")


def _freeze_acceptance(
    context: tuple[Path, dict[str, object], Path, str]
) -> None:
    run_dir = context[0]
    freeze_path = run_dir / ACCEPTANCE_FREEZE_PATH
    if _lexists(freeze_path):
        raise RunError(f"refusing to overwrite existing file: {freeze_path}")
    _, production_sha256, production_bytes = _verify_production_freeze(context)
    entries = _validate_open_acceptance(run_dir)
    missing = sorted(set(FROZEN_ACCEPTANCE_NAMES) - set(entries))
    if missing:
        raise RunError(f"acceptance freeze requires files: {missing}")
    manifest = _expected_acceptance_freeze(
        run_dir, entries, production_sha256, production_bytes
    )
    _write_json_exclusive(freeze_path, manifest)
    file_count = _verify_acceptance_freeze(
        context, (production_sha256, production_bytes)
    )
    print(f"freeze: wrote {freeze_path} ({file_count} acceptance files)")


def _freeze_run(args: argparse.Namespace) -> None:
    context = _load_context(args.run_dir)
    if args.acceptance:
        _freeze_acceptance(context)
    else:
        _freeze_production(context)


def _check_run(args: argparse.Namespace) -> None:
    context = _load_context(args.run_dir)
    run_dir, metadata, root, material_relative = context
    state_headers = [
        (path, *_check_state_header(path)) for path in args.state_file
    ]
    production_freeze = run_dir / PRODUCTION_FREEZE_NAME
    if not _lexists(production_freeze):
        _verify_material(metadata, root, material_relative)
        _verify_final_receipt_binding(run_dir, require_when_root_exists=False)
        _, production_files = _production_snapshot(run_dir)
        _require_acceptance_empty(run_dir)
        print(
            f"check: PASSED {run_dir} "
            f"({len(production_files)} production files, "
            "production=open, acceptance=open:0, "
            f"{len(state_headers)} state headers); "
            "semantic and product acceptance not evaluated"
        )
        return

    production_count, production_sha256, production_bytes = (
        _verify_production_freeze(context)
    )
    acceptance_freeze = run_dir / ACCEPTANCE_FREEZE_PATH
    if _lexists(acceptance_freeze):
        acceptance_count = _verify_acceptance_freeze(
            context, (production_sha256, production_bytes)
        )
        acceptance_state = "frozen"
    else:
        acceptance_count = len(_validate_open_acceptance(run_dir))
        acceptance_state = "open"

    print(
        f"check: PASSED {run_dir} "
        f"({production_count} production files, "
        "production=frozen, "
        f"acceptance={acceptance_state}:{acceptance_count}, "
        f"{len(state_headers)} state headers); "
        "semantic and product acceptance not evaluated"
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create, freeze, and check a deterministic ReaderLab run.",
        epilog=(
            "Single-writer contract: while a command runs, only its caller may "
            "write the explicit root, material path, or run directory."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="create a non-overwriting run")
    new_parser.add_argument("run_dir", type=Path)
    new_parser.add_argument("--root", type=Path, default=Path.cwd())
    new_parser.add_argument("--material", required=True, type=Path)
    new_parser.add_argument("--source", required=True)
    new_parser.add_argument("--scope", required=True)
    new_parser.add_argument("--route", required=True, choices=("book", "skills"))
    new_parser.set_defaults(handler=_new_run)

    freeze_parser = subparsers.add_parser(
        "freeze", help="write an exclusive production or acceptance manifest"
    )
    freeze_parser.add_argument("run_dir", type=Path)
    freeze_parser.add_argument(
        "--acceptance",
        action="store_true",
        help=f"freeze {ACCEPTANCE_FREEZE_PATH} after production",
    )
    freeze_parser.set_defaults(handler=_freeze_run)

    check_parser = subparsers.add_parser(
        "check",
        help="check material, open or frozen production, and acceptance ordering",
    )
    check_parser.add_argument("run_dir", type=Path)
    check_parser.add_argument(
        "--state-file",
        action="append",
        default=[],
        type=Path,
        help="Markdown file requiring a valid status/scope header; repeatable",
    )
    check_parser.set_defaults(handler=_check_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        args.handler(args)
    except (RunError, OSError) as error:
        print(f"run error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
