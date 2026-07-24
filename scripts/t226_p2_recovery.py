#!/usr/bin/env python3
"""Deterministic, append-only recovery for the T2.26 v07 P2 review package."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Mapping


RUN_REL = Path("runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-07")
TASKCARD_REL = Path("taskcards/T2.26-v07-p2-recovery.md")
PARENT_TASKCARD_REL = Path("taskcards/T2.26-v07.md")
SCRIPT_REL = Path("scripts/t226_p2_recovery.py")
TEST_REL = Path("tests/test_t226_p2_recovery.py")

PACKAGE_V01_REL = RUN_REL / "review/p2-product-review-v01.md"
PACKAGE_V02_REL = RUN_REL / "review/p2-product-review-v02.md"
PROVENANCE_REL = RUN_REL / "control/p2-recovery-provenance-v02.json"
CONTRACT_REL = RUN_REL / "control/p2-recovery-contract-v02.json"
PRODUCT_READY_REL = RUN_REL / "control/p2-recovery-product-ready-v02.json"
REGISTRY_V02_REL = RUN_REL / "control/artifact-registry-p2-v02.jsonl"
ROOT_REGISTRY_REL = RUN_REL / "control/artifact-registry.jsonl"

CANDIDATE_ARTIFACTS_DIR = Path("candidate-artifacts")
CANDIDATE_MANIFEST = CANDIDATE_ARTIFACTS_DIR / "candidate-manifest.json"
PROMOTION_RECEIPT = Path("promotion-receipt.json")

PARENT_TASKCARD_SHA256 = (
    "a655eb1c8e98f26b6d6353a8aa626f24315b6f04b7304a498d6f95dc3fb079dc"
)
EXPECTED_BRANCH = "codex/readerlab-book-lens-original-goal-v1"
EXPECTED_HEAD = "d63118fd057e0b9a8aadc05b2fae244035c02891"

FROZEN_FILES = {
    RUN_REL / "review/C-01-lesson-v01.md": (
        9705,
        "d29cb70326af589216bfbcfb329aaf8cbeeefd7f33c243a8a12a25d09175ea78",
    ),
    RUN_REL / "review/C-03-lesson-v01.md": (
        5415,
        "d2912187d518be5ae3dec1f3d290771f7d644d4da90ae41e0257e2b1de28efbc",
    ),
    PACKAGE_V01_REL: (
        7802,
        "576e44bc0be1c728c171143a5fb451a2db4ecd770b10f716ee878fffd935b4be",
    ),
    RUN_REL / "control/artifact-registry-p1-v01.jsonl": (
        2495,
        "2250f94fed0fdd931d36877e31f51207f82494aee9fbadebaffe909961495189",
    ),
    RUN_REL / "control/artifact-registry-p2-v01.jsonl": (
        3563,
        "968ed7d7ab82546b3445635a3f9c3f178424ddf712adff46c1c6c8ce27b48add",
    ),
    RUN_REL / "control/production-group-ledger.jsonl": (
        4482,
        "6be028150eb37d72841d271f767f5d411ccda32ef5f69c1f98af1552b21ab28d",
    ),
    RUN_REL / "control/usage-ledger.jsonl": (
        8470,
        "94b1cf13de253a4f8c81f62f99e863350e0d670ec4112c1fc0f7189726f6d791",
    ),
    RUN_REL / "control/C-01-p1-gate.txt": (
        46,
        "3dc51d9dcfb0879d04adc887558ff7bc50e9000c1f63080c08f9d084fb63ea88",
    ),
    RUN_REL / "control/C-03-p1-gate.txt": (
        46,
        "e7993540c8251216d74a6a01dca85c8c8b6eda2b6c2977d4d87a70313e69cc3d",
    ),
}

LESSON_REL_BY_ID = {
    "C-01": RUN_REL / "review/C-01-lesson-v01.md",
    "C-03": RUN_REL / "review/C-03-lesson-v01.md",
}
GATE_REL_BY_ID = {
    "C-01": RUN_REL / "control/C-01-p1-gate.txt",
    "C-03": RUN_REL / "control/C-03-p1-gate.txt",
}

EXISTING_RUN_FILES = {
    Path("acceptance/p1-product-verdicts.md"),
    Path("control/C-01-p1-gate.txt"),
    Path("control/C-03-p1-gate.txt"),
    Path("control/artifact-registry-p1-v01.jsonl"),
    Path("control/artifact-registry-p2-v01.jsonl"),
    Path("control/contract-manifest.md"),
    Path("control/human-local-review-form-v01.md"),
    Path("control/issue-schema-v01.json"),
    Path("control/material-selection-manifest.md"),
    Path("control/production-group-ledger.jsonl"),
    Path("control/reader-quality-rubric-v01.md"),
    Path("control/target-reader-contract-v01.md"),
    Path("control/usage-ledger.jsonl"),
    Path("control/writer-contract-v1.3.md"),
    Path("diagnostics/candidate-breadth-v01.md"),
    Path("inputs/chapter-scope.xhtml"),
    Path("review/C-01-lesson-v01.md"),
    Path("review/C-03-lesson-v01.md"),
    Path("review/comparison-v01.md"),
    Path("review/p1-product-review-v01.md"),
    Path("review/p2-product-review-v01.md"),
    Path("review/usage-summary.md"),
    Path("working/candidate-pool-v01.md"),
}

RECOVERY_RUN_FILES = {
    PACKAGE_V02_REL.relative_to(RUN_REL),
    PROVENANCE_REL.relative_to(RUN_REL),
    CONTRACT_REL.relative_to(RUN_REL),
    PRODUCT_READY_REL.relative_to(RUN_REL),
    REGISTRY_V02_REL.relative_to(RUN_REL),
}

FORBIDDEN_AFTER_P2_PATTERNS = (
    "acceptance/p2-product-verdicts.md",
    "control/*-p2-gate.txt",
    "control/*-local-context-v01.md",
    "review/*-source-audit-*.md",
    "review/*-lesson-v02-source-fixed.md",
    "handoff/*-writer-input-*.md",
    "review/*-reader-*.md",
    "review/*-edit-ledger-*.md",
    "review/*-fidelity-*.md",
    "sealed/*",
    "review/end-to-end-review-*.md",
    "review/product-blind-review-pack-*.md",
    "receipts/*",
    "acceptance/product-blind-verdicts.md",
    "review/issue-lineage-*.jsonl",
    "review/rater-human-comparison-*.md",
    "acceptance/rater-match-verdicts.md",
    "diagnostics/content-dimensions-*.md",
)

OFFICIAL_CONTROL_RELS = (TASKCARD_REL, SCRIPT_REL, TEST_REL)
OFFICIAL_ARTIFACT_RELS = (
    PACKAGE_V02_REL,
    PROVENANCE_REL,
    CONTRACT_REL,
    PRODUCT_READY_REL,
    REGISTRY_V02_REL,
)

REGISTRY_REQUIRED_RELS = (
    *OFFICIAL_CONTROL_RELS,
    PARENT_TASKCARD_REL,
    *LESSON_REL_BY_ID.values(),
    *GATE_REL_BY_ID.values(),
    RUN_REL / "control/artifact-registry-p1-v01.jsonl",
    RUN_REL / "control/artifact-registry-p2-v01.jsonl",
    PACKAGE_V01_REL,
    RUN_REL / "control/production-group-ledger.jsonl",
    RUN_REL / "control/usage-ledger.jsonl",
    PACKAGE_V02_REL,
    PROVENANCE_REL,
    CONTRACT_REL,
    PRODUCT_READY_REL,
)

REGISTRY_SELF_REASON = "registry cannot hash its own final bytes"

PACKAGE_HEADER = """# P2 产品审阅包 v02（技术恢复）

## 使用说明

本包只供产品负责人进行 P2 审阅。控制层按固定顺序逐字嵌入两份冻结
Expert lesson；未做摘要、删减、合并、改写或语义补充。技术验证与 registry
只证明装配合同、来源和 bytes，不构成产品判词。

失效的 `p2-product-review-v01.md` 完整保留为技术证据，不得作为产品判词
输入。当前尚无 P2 判词或 P2 gate；产品负责人仍只对每个对象判断
`WORTH_PUBLISHING` / `REJECT`。

"""


class RecoveryError(RuntimeError):
    """A deterministic P2 recovery failure."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def canonical_jsonl_bytes(records: Iterable[Mapping[str, object]]) -> bytes:
    return "".join(
        json.dumps(
            dict(record),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
        for record in records
    ).encode("utf-8")


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def exclusive_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def checked_read(path: Path, expected_bytes: int, expected_sha: str) -> bytes:
    data = path.read_bytes()
    actual_sha = sha256_bytes(data)
    if len(data) != expected_bytes or actual_sha != expected_sha:
        raise RecoveryError(
            f"frozen identity mismatch: {path}; "
            f"bytes={len(data)} sha256={actual_sha}"
        )
    return data


def parse_neutral_gate(data: bytes, candidate_id: str) -> dict[str, str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RecoveryError(f"{candidate_id} gate is not UTF-8") from error
    expected = (
        f"candidate_id: {candidate_id}\n"
        "p1_status: WORTH_EXPANDING\n"
    )
    if text != expected:
        raise RecoveryError(
            f"{candidate_id} P1 gate must contain only neutral identity and status"
        )
    return {"candidate_id": candidate_id, "p1_status": "WORTH_EXPANDING"}


def _current_run_files(workspace: Path) -> set[Path]:
    run_root = workspace / RUN_REL
    return {
        path.relative_to(run_root)
        for path in run_root.rglob("*")
        if path.is_file()
    }


def _matches_any(path: Path, patterns: Iterable[str]) -> bool:
    return any(path.match(pattern) for pattern in patterns)


def validate_git_identity(workspace: Path) -> dict[str, str]:
    try:
        branch = subprocess.run(
            ["git", "-C", str(workspace), "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        head = subprocess.run(
            ["git", "-C", str(workspace), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise RecoveryError("unable to verify frozen git branch/HEAD") from error
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise RecoveryError(
            "frozen git identity mismatch: "
            f"branch={branch!r} head={head!r}"
        )
    return {"status": "PASS", "branch": branch, "head": head}


def validate_stage(workspace: Path, *, allow_recovery_files: bool) -> dict[str, object]:
    workspace = workspace.resolve()
    git_identity = validate_git_identity(workspace)
    if sha256_bytes((workspace / PARENT_TASKCARD_REL).read_bytes()) != (
        PARENT_TASKCARD_SHA256
    ):
        raise RecoveryError("frozen parent taskcard identity changed")
    if (workspace / ROOT_REGISTRY_REL).exists():
        raise RecoveryError("final root registry must not exist during P2 recovery")

    current = _current_run_files(workspace)
    allowed = set(EXISTING_RUN_FILES)
    if allow_recovery_files:
        allowed.update(RECOVERY_RUN_FILES)
    unknown = sorted(path.as_posix() for path in current - allowed)
    missing = sorted(path.as_posix() for path in EXISTING_RUN_FILES - current)
    if unknown or missing:
        raise RecoveryError(
            f"run path allowlist mismatch; missing={missing}; unknown={unknown}"
        )
    forbidden = sorted(
        path.as_posix()
        for path in current
        if _matches_any(path, FORBIDDEN_AFTER_P2_PATTERNS)
    )
    if forbidden:
        raise RecoveryError(f"P2 downstream artifacts must not exist: {forbidden}")

    gates = {}
    for relative, (expected_bytes, expected_sha) in FROZEN_FILES.items():
        data = checked_read(
            workspace / relative,
            expected_bytes,
            expected_sha,
        )
        for candidate_id, gate_relative in GATE_REL_BY_ID.items():
            if relative == gate_relative:
                gates[candidate_id] = parse_neutral_gate(data, candidate_id)

    if set(gates) != set(LESSON_REL_BY_ID):
        raise RecoveryError("neutral P1 gate set mismatch")
    return {
        "status": "PASS",
        "stage": "LESSONS_FROZEN_AWAITING_VALID_P2_PACKAGE",
        "allowed_run_path_count": len(allowed),
        "current_run_file_count": len(current),
        "neutral_p1_gates": gates,
        "p2_downstream_artifacts": 0,
        "root_registry_exists": False,
        "git_identity": git_identity,
    }


def lesson_separator(
    candidate_id: str, source_relative: Path, lesson_data: bytes
) -> bytes:
    return (
        f"## 审阅对象 {candidate_id}\n\n"
        f"- source_path: `{source_relative.as_posix()}`\n"
        f"- source_bytes: `{len(lesson_data)}`\n"
        f"- source_sha256: `{sha256_bytes(lesson_data)}`\n\n"
        f"<!-- BEGIN FROZEN LESSON {candidate_id} -->\n"
    ).encode("utf-8")


def lesson_suffix(candidate_id: str) -> bytes:
    return (
        f"<!-- END FROZEN LESSON {candidate_id} -->\n\n"
    ).encode("utf-8")


def render_package(workspace: Path) -> tuple[bytes, dict[str, object]]:
    parts = [PACKAGE_HEADER.encode("utf-8")]
    sources = []
    for candidate_id in ("C-01", "C-03"):
        relative = LESSON_REL_BY_ID[candidate_id]
        expected_bytes, expected_sha = FROZEN_FILES[relative]
        data = checked_read(
            workspace / relative,
            expected_bytes,
            expected_sha,
        )
        parts.extend(
            (
                lesson_separator(candidate_id, relative, data),
                data,
                lesson_suffix(candidate_id),
            )
        )
        sources.append(
            {
                "candidate_id": candidate_id,
                "path": relative.as_posix(),
                "bytes": len(data),
                "sha256": sha256_bytes(data),
            }
        )
    package = b"".join(parts)
    validate_package_bytes(workspace, package)
    return package, {"sources": sources}


def validate_package_bytes(workspace: Path, package: bytes) -> dict[str, object]:
    expected_parts = [PACKAGE_HEADER.encode("utf-8")]
    source_results = []
    cursor = len(expected_parts[0])
    for candidate_id in ("C-01", "C-03"):
        relative = LESSON_REL_BY_ID[candidate_id]
        expected_bytes, expected_sha = FROZEN_FILES[relative]
        lesson = checked_read(
            workspace / relative,
            expected_bytes,
            expected_sha,
        )
        separator = lesson_separator(candidate_id, relative, lesson)
        suffix = lesson_suffix(candidate_id)
        expected_parts.extend((separator, lesson, suffix))
        lesson_count = package.count(lesson)
        if lesson_count != 1:
            raise RecoveryError(
                f"{candidate_id} frozen lesson occurrence count is {lesson_count}, not 1"
            )
        expected_start = cursor + len(separator)
        actual_start = package.find(lesson)
        if actual_start != expected_start:
            raise RecoveryError(f"{candidate_id} lesson byte position mismatch")
        cursor = expected_start + len(lesson) + len(suffix)
        source_results.append(
            {
                "candidate_id": candidate_id,
                "bytes": len(lesson),
                "sha256": sha256_bytes(lesson),
                "complete_original_byte_occurrences": lesson_count,
            }
        )
    expected = b"".join(expected_parts)
    if package != expected:
        raise RecoveryError(
            "package differs from the fixed wrapper plus frozen lesson bytes"
        )
    return {
        "status": "PASS",
        "package_bytes": len(package),
        "package_sha256": sha256_bytes(package),
        "deterministic_render_equal": True,
        "lesson_results": source_results,
    }


def candidate_path(candidate_root: Path, relative: Path) -> Path:
    return candidate_root / CANDIDATE_ARTIFACTS_DIR / relative


def _candidate_control_hashes(candidate_root: Path) -> dict[str, str]:
    result = {}
    for relative in OFFICIAL_CONTROL_RELS:
        path = candidate_root / relative
        if not path.is_file():
            raise RecoveryError(f"candidate control file missing: {relative}")
        result[relative.as_posix()] = sha256_bytes(path.read_bytes())
    return result


def _expected_registry_records(
    workspace: Path,
    candidate_root: Path,
    artifact_bytes: Mapping[Path, bytes],
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    candidate_control = {
        relative: (candidate_root / relative).read_bytes()
        for relative in OFFICIAL_CONTROL_RELS
    }
    for relative in REGISTRY_REQUIRED_RELS:
        if relative in candidate_control:
            data = candidate_control[relative]
        elif relative in artifact_bytes:
            data = artifact_bytes[relative]
        else:
            data = (workspace / relative).read_bytes()
        records.append(
            {
                "kind": "artifact",
                "path": relative.as_posix(),
                "sha256": sha256_bytes(data),
                "status": "frozen",
            }
        )
    records.append(
        {
            "kind": "artifact_registry",
            "path": REGISTRY_V02_REL.as_posix(),
            "reason": REGISTRY_SELF_REASON,
            "sha256": None,
            "status": "self_exempt",
        }
    )
    return records


def _build_reports(
    workspace: Path,
    candidate_root: Path,
    package: bytes,
) -> dict[Path, bytes]:
    package_result = validate_package_bytes(workspace, package)
    stage = validate_stage(workspace, allow_recovery_files=False)
    control_hashes = _candidate_control_hashes(candidate_root)
    source_records = []
    for candidate_id in ("C-01", "C-03"):
        lesson_relative = LESSON_REL_BY_ID[candidate_id]
        gate_relative = GATE_REL_BY_ID[candidate_id]
        lesson = (workspace / lesson_relative).read_bytes()
        gate = (workspace / gate_relative).read_bytes()
        source_records.append(
            {
                "candidate_id": candidate_id,
                "lesson": {
                    "path": lesson_relative.as_posix(),
                    "bytes": len(lesson),
                    "sha256": sha256_bytes(lesson),
                    "complete_original_byte_occurrences": package.count(lesson),
                },
                "neutral_p1_gate": {
                    "path": gate_relative.as_posix(),
                    "sha256": sha256_bytes(gate),
                    **parse_neutral_gate(gate, candidate_id),
                },
            }
        )

    provenance = {
        "axis": "provenance",
        "status": "PASS",
        "assembly_method": "deterministic_fixed_wrapper_plus_frozen_bytes",
        "semantic_model_calls": 0,
        "package": {
            "path": PACKAGE_V02_REL.as_posix(),
            "bytes": len(package),
            "sha256": sha256_bytes(package),
        },
        "sources_in_fixed_order": source_records,
        "product_judgment": "NOT_EVALUATED",
    }
    contract = {
        "axis": "contract",
        "status": "PASS",
        "stage": stage["stage"],
        "candidate_outside_workspace": True,
        "candidate_validation": "PASS",
        "promotion": "BYTE_IDENTICAL_O_EXCL_FIRST_WRITE_REQUIRED",
        "package_exact_deterministic_bytes": package_result["deterministic_render_equal"],
        "allowed_added_text": [
            "fixed_title",
            "fixed_usage_instructions",
            "object_separators",
            "sha_and_provenance_metadata",
        ],
        "parent_taskcard": {
            "path": PARENT_TASKCARD_REL.as_posix(),
            "sha256": PARENT_TASKCARD_SHA256,
            "modified": False,
        },
        "preserved_v01": {
            "package_sha256": FROZEN_FILES[PACKAGE_V01_REL][1],
            "p1_registry_sha256": FROZEN_FILES[
                RUN_REL / "control/artifact-registry-p1-v01.jsonl"
            ][1],
            "p2_registry_sha256": FROZEN_FILES[
                RUN_REL / "control/artifact-registry-p2-v01.jsonl"
            ][1],
        },
        "control_candidate_hashes": control_hashes,
        "usage_ledger_unchanged_sha256": FROZEN_FILES[
            RUN_REL / "control/usage-ledger.jsonl"
        ][1],
        "production_group_ledger_unchanged_sha256": FROZEN_FILES[
            RUN_REL / "control/production-group-ledger.jsonl"
        ][1],
        "semantic_model_calls_during_recovery": 0,
        "p2_downstream_artifacts": 0,
        "root_registry_created": False,
        "git_identity": stage["git_identity"],
        "product_judgment": "NOT_EVALUATED",
    }
    product_ready = {
        "axis": "product_ready",
        "status": "READY_FOR_PRODUCT_REVIEW",
        "package_path": PACKAGE_V02_REL.as_posix(),
        "package_sha256": sha256_bytes(package),
        "provenance_status": "PASS",
        "contract_status": "PASS",
        "registry_claim_scope": "INTEGRITY_ONLY",
        "product_verdict": "NOT_MADE",
        "p2_gates": "NOT_CREATED",
        "downstream": "BLOCKED_PENDING_PRODUCT_REVIEW",
        "allowed_product_verdicts": ["WORTH_PUBLISHING", "REJECT"],
    }
    return {
        PACKAGE_V02_REL: package,
        PROVENANCE_REL: canonical_json_bytes(provenance),
        CONTRACT_REL: canonical_json_bytes(contract),
        PRODUCT_READY_REL: canonical_json_bytes(product_ready),
    }


def build_candidate(workspace: Path, candidate_root: Path) -> dict[str, object]:
    workspace = workspace.resolve()
    candidate_root = candidate_root.resolve()
    if is_within(candidate_root, workspace):
        raise RecoveryError("candidate root must be outside the workspace")
    artifacts_root = candidate_root / CANDIDATE_ARTIFACTS_DIR
    if artifacts_root.exists():
        raise RecoveryError("candidate artifacts directory already exists")
    validate_stage(workspace, allow_recovery_files=False)
    package, _ = render_package(workspace)
    artifact_bytes = _build_reports(workspace, candidate_root, package)
    registry_records = _expected_registry_records(
        workspace,
        candidate_root,
        artifact_bytes,
    )
    artifact_bytes[REGISTRY_V02_REL] = canonical_jsonl_bytes(registry_records)

    for relative in OFFICIAL_ARTIFACT_RELS:
        exclusive_write(candidate_path(candidate_root, relative), artifact_bytes[relative])
    manifest = {
        "status": "CANDIDATE_VALIDATED",
        "candidate_root_outside_workspace": True,
        "control_hashes": _candidate_control_hashes(candidate_root),
        "artifacts": {
            relative.as_posix(): {
                "bytes": len(artifact_bytes[relative]),
                "sha256": sha256_bytes(artifact_bytes[relative]),
            }
            for relative in OFFICIAL_ARTIFACT_RELS
        },
    }
    exclusive_write(
        candidate_root / CANDIDATE_MANIFEST,
        canonical_json_bytes(manifest),
    )
    validation = validate_candidate(workspace, candidate_root)
    return {
        "status": "PASS",
        "candidate_root": str(candidate_root),
        "candidate_outside_workspace": True,
        **validation,
    }


def _read_candidate_artifacts(candidate_root: Path) -> dict[Path, bytes]:
    return {
        relative: candidate_path(candidate_root, relative).read_bytes()
        for relative in OFFICIAL_ARTIFACT_RELS
    }


def validate_candidate(workspace: Path, candidate_root: Path) -> dict[str, object]:
    workspace = workspace.resolve()
    candidate_root = candidate_root.resolve()
    if is_within(candidate_root, workspace):
        raise RecoveryError("candidate root must be outside the workspace")
    stage = validate_stage(workspace, allow_recovery_files=False)
    artifact_bytes = _read_candidate_artifacts(candidate_root)
    expected_package, _ = render_package(workspace)
    expected = _build_reports(workspace, candidate_root, expected_package)
    expected[REGISTRY_V02_REL] = canonical_jsonl_bytes(
        _expected_registry_records(workspace, candidate_root, expected)
    )
    for relative in OFFICIAL_ARTIFACT_RELS:
        if artifact_bytes[relative] != expected[relative]:
            raise RecoveryError(f"candidate artifact bytes mismatch: {relative}")
    package_result = validate_package_bytes(
        workspace,
        artifact_bytes[PACKAGE_V02_REL],
    )
    manifest = json.loads(
        (candidate_root / CANDIDATE_MANIFEST).read_text(encoding="utf-8")
    )
    expected_manifest = {
        "status": "CANDIDATE_VALIDATED",
        "candidate_root_outside_workspace": True,
        "control_hashes": _candidate_control_hashes(candidate_root),
        "artifacts": {
            relative.as_posix(): {
                "bytes": len(expected[relative]),
                "sha256": sha256_bytes(expected[relative]),
            }
            for relative in OFFICIAL_ARTIFACT_RELS
        },
    }
    if manifest != expected_manifest:
        raise RecoveryError("candidate manifest mismatch")
    return {
        "candidate_validation": "PASS",
        "stage_validation": stage["status"],
        "package_validation": package_result,
        "candidate_manifest_sha256": sha256_bytes(
            (candidate_root / CANDIDATE_MANIFEST).read_bytes()
        ),
    }


def validate_promotion_receipt(candidate_root: Path) -> dict[str, object]:
    path = candidate_root / PROMOTION_RECEIPT
    if not path.is_file():
        raise RecoveryError(
            "test and two-axis review receipt is required before promotion"
        )
    receipt = json.loads(path.read_text(encoding="utf-8"))
    expected_hashes = _candidate_control_hashes(candidate_root)
    expected_manifest_sha = sha256_bytes(
        (candidate_root / CANDIDATE_MANIFEST).read_bytes()
    )
    if (
        receipt.get("tests") != "PASS"
        or receipt.get("test_exit_code") != 0
        or receipt.get("red_regression") != "OBSERVED"
        or receipt.get("red_exit_code") != 1
    ):
        raise RecoveryError("red regression and green tests must be recorded as passing")
    if receipt.get("standards") != "PASS" or receipt.get("spec") != "PASS":
        raise RecoveryError("Standards and Spec reviews must both be PASS")
    if receipt.get("reviewed_control_hashes") != expected_hashes:
        raise RecoveryError("promotion receipt does not bind current control candidates")
    if receipt.get("reviewed_candidate_manifest_sha256") != expected_manifest_sha:
        raise RecoveryError("promotion receipt does not bind current candidate manifest")
    return receipt


def run_candidate_tests(workspace: Path, candidate_root: Path) -> dict[str, object]:
    environment = dict(os.environ)
    environment.update(
        {
            "T226_WORKSPACE": str(workspace),
            "T226_RECOVERY_MODULE": str(candidate_root / SCRIPT_REL),
            "T226_PROMOTION_TEST_MODE": "1",
        }
    )
    command = [
        sys.executable,
        str(candidate_root / TEST_REL),
        "-v",
    ]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=environment,
    )
    if completed.returncode != 0:
        raise RecoveryError(
            "bound candidate tests failed before promotion: "
            f"{completed.stderr[-2000:]}"
        )
    return {
        "status": "PASS",
        "exit_code": completed.returncode,
        "command": command,
        "stdout_sha256": sha256_bytes(completed.stdout.encode("utf-8")),
        "stderr_sha256": sha256_bytes(completed.stderr.encode("utf-8")),
    }


def _promote_one(workspace: Path, candidate: Path, relative: Path) -> str:
    data = candidate.read_bytes()
    target = workspace / relative
    if target.exists():
        raise RecoveryError(f"formal target already exists: {relative}")
    exclusive_write(target, data)
    readback = target.read_bytes()
    if readback != data:
        raise RecoveryError(f"formal readback differs from candidate: {relative}")
    return sha256_bytes(readback)


def promote_control(workspace: Path, candidate_root: Path) -> dict[str, object]:
    workspace = workspace.resolve()
    candidate_root = candidate_root.resolve()
    validate_candidate(workspace, candidate_root)
    receipt = validate_promotion_receipt(candidate_root)
    bound_tests = run_candidate_tests(workspace, candidate_root)
    for relative in OFFICIAL_CONTROL_RELS:
        if (workspace / relative).exists():
            raise RecoveryError(f"formal control target already exists: {relative}")
    hashes = {}
    for relative in OFFICIAL_CONTROL_RELS:
        hashes[relative.as_posix()] = _promote_one(
            workspace,
            candidate_root / relative,
            relative,
        )
    return {
        "status": "PASS",
        "promotion": "BYTE_IDENTICAL_O_EXCL_FIRST_WRITE",
        "review_receipt_sha256": sha256_bytes(
            (candidate_root / PROMOTION_RECEIPT).read_bytes()
        ),
        "promoted_control_hashes": hashes,
        "standards": receipt["standards"],
        "spec": receipt["spec"],
        "bound_tests": bound_tests,
    }


def _validate_official_control(workspace: Path, candidate_root: Path) -> None:
    for relative in OFFICIAL_CONTROL_RELS:
        official = (workspace / relative).read_bytes()
        candidate = (candidate_root / relative).read_bytes()
        if official != candidate:
            raise RecoveryError(f"official control differs from candidate: {relative}")


def promote_artifacts(workspace: Path, candidate_root: Path) -> dict[str, object]:
    workspace = workspace.resolve()
    candidate_root = candidate_root.resolve()
    validate_candidate(workspace, candidate_root)
    validate_promotion_receipt(candidate_root)
    _validate_official_control(workspace, candidate_root)
    for relative in OFFICIAL_ARTIFACT_RELS:
        if (workspace / relative).exists():
            raise RecoveryError(f"formal artifact target already exists: {relative}")

    promoted = {}
    for relative in (
        PACKAGE_V02_REL,
        PROVENANCE_REL,
        CONTRACT_REL,
        PRODUCT_READY_REL,
        REGISTRY_V02_REL,
    ):
        promoted[relative.as_posix()] = _promote_one(
            workspace,
            candidate_path(candidate_root, relative),
            relative,
        )
        if relative == PACKAGE_V02_REL:
            validate_package_bytes(workspace, (workspace / relative).read_bytes())
    official = verify_official(workspace)
    return {
        "status": "PASS",
        "promotion": "BYTE_IDENTICAL_O_EXCL_FIRST_WRITE",
        "promoted_artifact_hashes": promoted,
        "official_verification": official,
    }


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(workspace: Path) -> dict[str, object]:
    records = [
        json.loads(line)
        for line in (workspace / REGISTRY_V02_REL)
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    paths = [record.get("path") for record in records]
    if len(paths) != len(set(paths)):
        raise RecoveryError("recovery registry contains duplicate paths")
    expected_paths = {relative.as_posix() for relative in REGISTRY_REQUIRED_RELS}
    regular = {
        record["path"]: record
        for record in records
        if record.get("path") != REGISTRY_V02_REL.as_posix()
    }
    if set(regular) != expected_paths:
        missing = sorted(expected_paths - set(regular))
        extra = sorted(set(regular) - expected_paths)
        raise RecoveryError(
            f"recovery registry closure mismatch; missing={missing}; extra={extra}"
        )
    for relative_text, record in regular.items():
        relative = Path(relative_text)
        actual = sha256_bytes((workspace / relative).read_bytes())
        if record != {
            "kind": "artifact",
            "path": relative_text,
            "sha256": actual,
            "status": "frozen",
        }:
            raise RecoveryError(f"recovery registry integrity mismatch: {relative}")
    self_records = [
        record
        for record in records
        if record.get("path") == REGISTRY_V02_REL.as_posix()
    ]
    expected_self = {
        "kind": "artifact_registry",
        "path": REGISTRY_V02_REL.as_posix(),
        "reason": REGISTRY_SELF_REASON,
        "sha256": None,
        "status": "self_exempt",
    }
    if self_records != [expected_self]:
        raise RecoveryError("recovery registry self-exemption mismatch")
    return {
        "status": "PASS",
        "claim_scope": "INTEGRITY_ONLY",
        "registered_artifact_count": len(regular),
        "self_exemption_count": 1,
    }


def verify_official(workspace: Path) -> dict[str, object]:
    workspace = workspace.resolve()
    stage = validate_stage(workspace, allow_recovery_files=True)
    for relative in OFFICIAL_CONTROL_RELS + OFFICIAL_ARTIFACT_RELS:
        if not (workspace / relative).is_file():
            raise RecoveryError(f"official recovery file missing: {relative}")
    package_result = validate_package_bytes(
        workspace,
        (workspace / PACKAGE_V02_REL).read_bytes(),
    )
    provenance = _load_json(workspace / PROVENANCE_REL)
    contract = _load_json(workspace / CONTRACT_REL)
    product_ready = _load_json(workspace / PRODUCT_READY_REL)
    if not isinstance(provenance, dict) or provenance.get("status") != "PASS":
        raise RecoveryError("official provenance axis is not PASS")
    if not isinstance(contract, dict) or contract.get("status") != "PASS":
        raise RecoveryError("official contract axis is not PASS")
    if (
        not isinstance(product_ready, dict)
        or product_ready.get("status") != "READY_FOR_PRODUCT_REVIEW"
        or product_ready.get("product_verdict") != "NOT_MADE"
        or product_ready.get("p2_gates") != "NOT_CREATED"
    ):
        raise RecoveryError("official product-ready axis is invalid")
    registry = validate_registry(workspace)
    return {
        "status": "PASS",
        "technical_state": "READY_FOR_PRODUCT_REVIEW",
        "package": package_result,
        "provenance": "PASS",
        "contract": "PASS",
        "product_ready": "READY_FOR_PRODUCT_REVIEW",
        "product_verdict": "NOT_MADE",
        "registry": registry,
        "stage": stage,
        "semantic_model_calls_during_recovery": 0,
        "v01_preserved": True,
        "p2_downstream_artifacts": 0,
        "root_registry_created": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in (
        "build-candidate",
        "validate-candidate",
        "promote-control",
        "promote-artifacts",
    ):
        command = subparsers.add_parser(name)
        command.add_argument("--workspace", type=Path, required=True)
        command.add_argument("--candidate-root", type=Path, required=True)
    verify = subparsers.add_parser("verify-official")
    verify.add_argument("--workspace", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "build-candidate":
            result = build_candidate(args.workspace, args.candidate_root)
        elif args.command == "validate-candidate":
            result = validate_candidate(args.workspace, args.candidate_root)
        elif args.command == "promote-control":
            result = promote_control(args.workspace, args.candidate_root)
        elif args.command == "promote-artifacts":
            result = promote_artifacts(args.workspace, args.candidate_root)
        else:
            result = verify_official(args.workspace)
    except (OSError, UnicodeError, ValueError, RecoveryError) as error:
        print(
            json.dumps(
                {"status": "FAIL", "error": str(error)},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
