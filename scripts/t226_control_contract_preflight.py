#!/usr/bin/env python3
"""Deterministic T2.26 control-contract renderer and preflight validator."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable, Mapping


WRITER_SOURCE = Path("docs/writer-style-guide.md")
WRITER_BOUNDARY = b"## \xe4\xb8\x89\xe3\x80\x81A/B \xe5\xae\x9e\xe9\xaa\x8c\xe6\x8c\x87\xe4\xbb\xa4"
WRITER_EXPECTED_BYTES = 6003
WRITER_EXPECTED_SHA256 = (
    "9a7a3bcaaf4d81cdc2936a2217ea9a147ea91b2edccf5ee0d83fd06a60462ffe"
)

CONTRACT_FILENAMES = (
    "writer-contract-v1.3.md",
    "target-reader-contract-v01.md",
    "reader-quality-rubric-v01.md",
    "human-local-review-form-v01.md",
    "issue-schema-v01.json",
)

READER_QUESTIONS = (
    "不知道该理论的目标读者能否理解其独特命题",
    "理论为什么需要在这里出现",
    "原文、理论和案例是否自然连接",
    "中文是否存在明显阅读摩擦",
    "读完能否带走新的、可复用判断",
    "是否存在阻断问题或发布问题",
)

RATER_ISSUE_FIELDS = (
    "issue_id",
    "artifact_sha",
    "issue_type",
    "location",
    "severity",
    "owner",
    "action",
    "first_detected_by",
    "status",
    "why",
    "meaning_to_preserve",
)

ISSUE_SCHEMA_REQUIRED_FIELDS = RATER_ISSUE_FIELDS[:9]
ISSUE_SCHEMA_OPTIONAL_FIELDS = ("confirmed_by", "resolved_by", "resolution")
RATER_TERMINALS = (
    "BLOCKED",
    "PATCH_ONCE",
    "ACCEPTED_WITH_NOTES",
    "ACCEPTED",
)
CHAPTER_TERMINALS = ("ACCEPTED", "REJECTED")
REGISTRY_SELF_REASON = "registry cannot hash its own final bytes"
SYNTHETIC_FIXTURE_ID = "T226_SYNTHETIC_PREFLIGHT_FIXTURE"
SYNTHETIC_FIXTURE_MARKERS = (
    SYNTHETIC_FIXTURE_ID.encode("ascii"),
    b'"event":"preflight-fixture"',
    b"# Synthetic deterministic closeout receipt",
    b"# Synthetic usage summary",
)


TARGET_READER_CONTRACT = """# 目标读者合同 v01

读者是正在阅读本书、具备正常常识和判断力的成年人。

陪读必须让读者先读作者的完整原文；一章或一节是完整阅读单元，不能以截出的几句话代替。评论可锚定具体句子、段落结尾或相邻段落之间，但不得隐藏紧接上下文或取代原文。

值得出现的内容必须提供真实认知增量：非显然、重要、具体、展开充分，并击中此处承重问题。它可以带来机制、模型、方法、预测、权衡、可迁移关系、高手指点或跨行业视角；不得只是复述、换词、术语命名、常识提醒或浅延伸。

读者应能看见核心命题、为何与原文有关、完整而可跟随的解释链，以及可带走的判断。新概念、外部案例或类比须讲清其含义、当前相关性与具体增量。

阅读负担必须由价值偿还：陌生术语、人物或细分理论首次承担论证作用时要可理解；冗长、术语堆砌、跨度失控或不能帮助理解的内容构成负价值。压缩可减少低收益支线和重复，不得删除承重推理。
"""


def _render_reader_questions() -> str:
    lines = []
    for index, question in enumerate(READER_QUESTIONS, 1):
        punctuation = "；" if index < len(READER_QUESTIONS) else "。"
        lines.append(f"{index}. {question}{punctuation}")
    return "\n".join(lines)


def _render_issue_fields() -> str:
    return "\n".join(RATER_ISSUE_FIELDS)


def _render_terminals(terminals: Iterable[str]) -> str:
    return "\n".join(f"- `{terminal}`" for terminal in terminals)


READER_QUALITY_RUBRIC = f"""# Reader Quality Rubric v01

仅评估读者侧体验，不评估理论或事实真实性、来源强度、Writer 对 Expert 的忠实性、整章 Reader 数量／重复／节奏，也不直接重写正文。

## 六项 Reader 问题

{_render_reader_questions()}

## Issue 输出字段

每个问题必须输出：

```text
{_render_issue_fields()}
```

## 允许终局

{_render_terminals(RATER_TERMINALS)}
"""


HUMAN_LOCAL_REVIEW_FORM = f"""# 人类局部盲审表 v01

每篇 Reader 必须独立填写，不得读取影子 Rater 结果。单篇问题与完整章节组合问题必须分区记录。

## 单篇 Reader 身份

- candidate_id：
- artifact_sha：
- Writer 版本：

## 六项 Reader 问题

{_render_reader_questions()}

## Issue 记录

每个问题使用与 Reader Quality Rater 相同的字段：

```text
{_render_issue_fields()}
```

## 单篇终局

{_render_terminals(RATER_TERMINALS)}

## 完整章节组合区

- Reader 是否重复：
- 数量和密度是否过载：
- 锚点是否破坏阅读节奏：
- 是否出现统一模板感：
- 完整章节终局：`ACCEPTED` / `REJECTED`

完整章节组合问题不得写入单篇 Issue 记录，也不得计作 Reader Quality Rater 漏报。
"""


ISSUE_SCHEMA = {
    "required_fields": list(ISSUE_SCHEMA_REQUIRED_FIELDS),
    "optional_resolution_fields": list(ISSUE_SCHEMA_OPTIONAL_FIELDS),
    "matching_conditions": [
        "artifact_sha exactly equal",
        "location identical or materially overlapping",
        "issue_type equal",
        "owner equal",
        "severity differs by at most one level",
        "core cause materially equal",
    ],
}


class PreflightError(RuntimeError):
    """A deterministic control-contract preflight failure."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exclusive_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def require_synthetic_output_outside_workspace(
    workspace: Path, output_dir: Path
) -> None:
    if _is_within(output_dir, workspace):
        raise PreflightError(
            "synthetic preflight output must be outside the workspace; "
            "use bootstrap-contracts for an official run"
        )


def writer_contract_bytes(workspace: Path) -> bytes:
    source = (workspace / WRITER_SOURCE).read_bytes()
    if source.count(WRITER_BOUNDARY) != 1:
        raise PreflightError("writer boundary must occur exactly once")
    boundary = source.index(WRITER_BOUNDARY)
    contract = source[:boundary]
    if len(contract) != WRITER_EXPECTED_BYTES:
        raise PreflightError(
            f"writer contract bytes mismatch: {len(contract)} != {WRITER_EXPECTED_BYTES}"
        )
    actual_sha = sha256_bytes(contract)
    if actual_sha != WRITER_EXPECTED_SHA256:
        raise PreflightError(
            f"writer contract sha mismatch: {actual_sha} != {WRITER_EXPECTED_SHA256}"
        )
    if not contract.endswith(b"---\n\n"):
        raise PreflightError("writer contract has an unexpected byte suffix")
    return contract


def canonical_contract_bytes(workspace: Path) -> dict[str, bytes]:
    return {
        "writer-contract-v1.3.md": writer_contract_bytes(workspace),
        "target-reader-contract-v01.md": TARGET_READER_CONTRACT.encode("utf-8"),
        "reader-quality-rubric-v01.md": READER_QUALITY_RUBRIC.encode("utf-8"),
        "human-local-review-form-v01.md": HUMAN_LOCAL_REVIEW_FORM.encode("utf-8"),
        "issue-schema-v01.json": (
            json.dumps(ISSUE_SCHEMA, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8"),
    }


def _section(text: str, start: str, end: str | None = None) -> str:
    if text.count(start) != 1:
        raise PreflightError(f"section marker must occur exactly once: {start}")
    value = text.split(start, 1)[1]
    if end is not None:
        if value.count(end) != 1:
            raise PreflightError(f"section end marker must occur exactly once: {end}")
        value = value.split(end, 1)[0]
    return value


def _numbered_questions(text: str, start: str, end: str) -> tuple[str, ...]:
    value = _section(text, start, end)
    matches = re.findall(r"^\d+\.\s+(.+?)[；。]?$", value, flags=re.MULTILINE)
    return tuple(match.strip() for match in matches)


def _fenced_fields(text: str, start: str, end: str | None = None) -> tuple[str, ...]:
    value = _section(text, start, end)
    match = re.search(r"```text\n(.*?)\n```", value, flags=re.DOTALL)
    if match is None:
        raise PreflightError(f"missing text field block after: {start}")
    return tuple(line.strip() for line in match.group(1).splitlines() if line.strip())


def _backtick_values(text: str, start: str, end: str | None = None) -> tuple[str, ...]:
    value = _section(text, start, end)
    return tuple(re.findall(r"`([A-Z_]+)`", value))


def validate_contract_structure(
    contracts: Mapping[str, bytes], workspace: Path
) -> dict[str, object]:
    if set(contracts) != set(CONTRACT_FILENAMES):
        missing = sorted(set(CONTRACT_FILENAMES) - set(contracts))
        extra = sorted(set(contracts) - set(CONTRACT_FILENAMES))
        raise PreflightError(f"contract file set mismatch; missing={missing}; extra={extra}")

    decoded = {
        name: data.decode("utf-8") for name, data in contracts.items() if name.endswith(".md")
    }
    rubric = decoded["reader-quality-rubric-v01.md"]
    human = decoded["human-local-review-form-v01.md"]
    target = decoded["target-reader-contract-v01.md"]

    rubric_questions = _numbered_questions(
        rubric, "## 六项 Reader 问题", "## Issue 输出字段"
    )
    human_questions = _numbered_questions(
        human, "## 六项 Reader 问题", "## Issue 记录"
    )
    if rubric_questions != READER_QUESTIONS:
        raise PreflightError("reader rubric questions do not match the six frozen questions")
    if human_questions != rubric_questions:
        raise PreflightError("human review questions do not match the Reader rubric")

    rubric_fields = _fenced_fields(rubric, "## Issue 输出字段", "## 允许终局")
    human_fields = _fenced_fields(human, "## Issue 记录", "## 单篇终局")
    if rubric_fields != RATER_ISSUE_FIELDS:
        raise PreflightError("reader rubric issue fields do not match the frozen field list")
    if human_fields != rubric_fields:
        raise PreflightError("human review issue fields do not match the Reader rubric")

    rubric_terminals = _backtick_values(rubric, "## 允许终局")
    human_terminals = _backtick_values(
        human, "## 单篇终局", "## 完整章节组合区"
    )
    if rubric_terminals != RATER_TERMINALS:
        raise PreflightError("reader rubric terminals do not match the frozen terminals")
    if human_terminals != rubric_terminals:
        raise PreflightError("human review terminals do not match the Reader rubric")

    chapter_section = _section(human, "## 完整章节组合区")
    for required in (
        "Reader 是否重复",
        "数量和密度是否过载",
        "锚点是否破坏阅读节奏",
        "是否出现统一模板感",
    ):
        if required not in chapter_section:
            raise PreflightError(f"human chapter section is missing: {required}")
    if _backtick_values(human, "## 完整章节组合区") != CHAPTER_TERMINALS:
        raise PreflightError("human chapter terminals must be ACCEPTED / REJECTED")

    issue_schema = json.loads(contracts["issue-schema-v01.json"])
    if tuple(issue_schema.get("required_fields", ())) != ISSUE_SCHEMA_REQUIRED_FIELDS:
        raise PreflightError("issue schema required fields do not match the frozen schema")
    if tuple(issue_schema.get("optional_resolution_fields", ())) != (
        ISSUE_SCHEMA_OPTIONAL_FIELDS
    ):
        raise PreflightError("issue schema optional fields do not match the frozen schema")
    if tuple(rubric_fields[: len(ISSUE_SCHEMA_REQUIRED_FIELDS)]) != (
        ISSUE_SCHEMA_REQUIRED_FIELDS
    ):
        raise PreflightError("Reader issue fields do not begin with issue schema fields")

    for required in (
        "具备正常常识和判断力的成年人",
        "完整原文",
        "真实认知增量",
        "可带走的判断",
        "阅读负担必须由价值偿还",
    ):
        if required not in target:
            raise PreflightError(f"target reader contract is missing: {required}")
    for forbidden in ("T2.25", "A/B", "P1", "产品判词", "历史答案"):
        if forbidden in target:
            raise PreflightError(
                f"target reader contract contains forbidden process/history text: {forbidden}"
            )

    expected = canonical_contract_bytes(workspace)
    for name in CONTRACT_FILENAMES:
        if contracts[name] != expected[name]:
            raise PreflightError(f"{name} differs from canonical frozen bytes")

    return {
        "contract_files": list(CONTRACT_FILENAMES),
        "reader_question_count": len(rubric_questions),
        "reader_issue_field_count": len(rubric_fields),
        "reader_terminal_count": len(rubric_terminals),
        "issue_schema_required_field_count": len(ISSUE_SCHEMA_REQUIRED_FIELDS),
        "chapter_composition_separate": True,
        "target_reader_structure": "PASS",
    }


def contract_hashes(contracts: Mapping[str, bytes]) -> dict[str, str]:
    return {name: sha256_bytes(contracts[name]) for name in CONTRACT_FILENAMES}


def manifest_bytes(hashes: Mapping[str, str]) -> bytes:
    lines = ["# T2.26 frozen contract manifest", ""]
    for name in CONTRACT_FILENAMES:
        lines.append(f"- `{name}`: `{hashes[name]}`")
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def parse_manifest(data: bytes) -> dict[str, str]:
    text = data.decode("utf-8")
    matches = re.findall(
        r"^- `([^`]+)`: `([0-9a-f]{64})`$", text, flags=re.MULTILINE
    )
    result = dict(matches)
    if set(result) != set(CONTRACT_FILENAMES):
        raise PreflightError("contract manifest does not list exactly five contracts")
    return result


def render_contract_bundle(workspace: Path, control_dir: Path) -> dict[str, object]:
    contracts = canonical_contract_bytes(workspace)
    structure = validate_contract_structure(contracts, workspace)
    hashes = contract_hashes(contracts)
    control_dir.mkdir(parents=True, exist_ok=False)
    for name in CONTRACT_FILENAMES:
        target = control_dir / name
        exclusive_write(target, contracts[name])
        readback = target.read_bytes()
        if readback != contracts[name] or sha256_bytes(readback) != hashes[name]:
            raise PreflightError(f"first-write readback mismatch: {name}")
    manifest_path = control_dir / "contract-manifest.md"
    exclusive_write(manifest_path, manifest_bytes(hashes))
    validate_contract_bundle(workspace, control_dir)
    return {"hashes": hashes, "structure": structure}


def validate_contract_bundle(workspace: Path, control_dir: Path) -> dict[str, object]:
    contracts = {
        name: (control_dir / name).read_bytes() for name in CONTRACT_FILENAMES
    }
    structure = validate_contract_structure(contracts, workspace)
    actual_hashes = contract_hashes(contracts)
    manifest_hashes = parse_manifest((control_dir / "contract-manifest.md").read_bytes())
    if manifest_hashes != actual_hashes:
        raise PreflightError("contract manifest hashes do not match actual readback hashes")
    return {"hashes": actual_hashes, "structure": structure}


def freeze_snapshot(control_dir: Path) -> dict[str, str]:
    names = (*CONTRACT_FILENAMES, "contract-manifest.md")
    return {name: sha256_bytes((control_dir / name).read_bytes()) for name in names}


def validate_frozen(snapshot: Mapping[str, str], control_dir: Path) -> None:
    current = freeze_snapshot(control_dir)
    if dict(snapshot) != current:
        changed = sorted(
            name for name in set(snapshot) | set(current) if snapshot.get(name) != current.get(name)
        )
        raise PreflightError(f"frozen contract mutation detected: {changed}")


def _run_files(run_root: Path, registry_path: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in run_root.rglob("*")
            if path.is_file() and path.resolve() != registry_path.resolve()
        ),
        key=lambda path: path.relative_to(run_root).as_posix(),
    )


def validate_no_synthetic_fixtures(paths: Iterable[Path]) -> None:
    for path in paths:
        data = path.read_bytes()
        for marker in SYNTHETIC_FIXTURE_MARKERS:
            if marker in data:
                raise PreflightError(
                    f"official artifact registry contains synthetic fixture: {path}"
                )


def build_artifact_registry(
    run_root: Path, registry_path: Path, *, allow_synthetic: bool = False
) -> None:
    if registry_path.exists():
        raise PreflightError("artifact registry target already exists")
    run_files = _run_files(run_root, registry_path)
    if not allow_synthetic:
        validate_no_synthetic_fixtures(run_files)
    records = []
    for path in run_files:
        records.append(
            {
                "kind": "artifact",
                "path": path.relative_to(run_root).as_posix(),
                "sha256": sha256_bytes(path.read_bytes()),
                "status": "frozen",
            }
        )
    records.append(
        {
            "kind": "artifact_registry",
            "path": registry_path.relative_to(run_root).as_posix(),
            "reason": REGISTRY_SELF_REASON,
            "sha256": None,
            "status": "self_exempt",
        }
    )
    data = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
        for record in records
    ).encode("utf-8")
    exclusive_write(registry_path, data)


def validate_artifact_registry(
    run_root: Path, registry_path: Path, *, allow_synthetic: bool = False
) -> dict[str, object]:
    records = [
        json.loads(line)
        for line in registry_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    paths = [record.get("path") for record in records]
    if len(paths) != len(set(paths)):
        raise PreflightError("artifact registry contains duplicate paths")

    registry_relative = registry_path.relative_to(run_root).as_posix()
    self_records = [record for record in records if record.get("path") == registry_relative]
    if len(self_records) != 1:
        raise PreflightError("artifact registry must contain one self-exemption record")
    expected_self = {
        "kind": "artifact_registry",
        "path": registry_relative,
        "reason": REGISTRY_SELF_REASON,
        "sha256": None,
        "status": "self_exempt",
    }
    if self_records[0] != expected_self:
        raise PreflightError("artifact registry self-exemption record is invalid")

    regular_records = {
        record["path"]: record
        for record in records
        if record.get("path") != registry_relative
    }
    expected_files = {
        path.relative_to(run_root).as_posix(): path
        for path in _run_files(run_root, registry_path)
    }
    if not allow_synthetic:
        validate_no_synthetic_fixtures(expected_files.values())
    if set(regular_records) != set(expected_files):
        missing = sorted(set(expected_files) - set(regular_records))
        extra = sorted(set(regular_records) - set(expected_files))
        raise PreflightError(
            f"artifact registry closure mismatch; missing={missing}; extra={extra}"
        )
    for relative, path in expected_files.items():
        record = regular_records[relative]
        if record.get("sha256") != sha256_bytes(path.read_bytes()):
            raise PreflightError(f"artifact registry sha mismatch: {relative}")
        if record.get("status") != "frozen":
            raise PreflightError(f"artifact registry status mismatch: {relative}")
        if record.get("sha256") == "PENDING_SELF_READBACK":
            raise PreflightError(f"artifact registry contains pending SHA: {relative}")

    return {
        "registered_artifact_count": len(expected_files),
        "self_exemption_count": 1,
        "closure": "PASS",
    }


def run_preflight(workspace: Path, output_dir: Path) -> dict[str, object]:
    require_synthetic_output_outside_workspace(workspace, output_dir)
    if output_dir.exists():
        raise PreflightError(f"preflight output already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    control_dir = output_dir / "control"
    rendered = render_contract_bundle(workspace, control_dir)
    snapshot = freeze_snapshot(control_dir)
    validate_contract_bundle(workspace, control_dir)
    validate_frozen(snapshot, control_dir)

    exclusive_write(
        control_dir / "production-group-ledger.jsonl",
        (
            json.dumps(
                {"event": SYNTHETIC_FIXTURE_ID, "status": "complete"},
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8"),
    )
    exclusive_write(
        control_dir / "usage-ledger.jsonl",
        (
            json.dumps(
                {
                    "event": SYNTHETIC_FIXTURE_ID,
                    "semantic_model_calls": 0,
                    "status": "complete",
                },
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8"),
    )
    exclusive_write(
        output_dir / "receipts" / "deterministic-receipt-v01.md",
        (
            "# Synthetic deterministic closeout receipt\n\n"
            f"{SYNTHETIC_FIXTURE_ID}\n"
        ).encode("ascii"),
    )
    exclusive_write(
        output_dir / "review" / "usage-summary.md",
        (
            "# Synthetic usage summary\n\n"
            f"- fixture identity: `{SYNTHETIC_FIXTURE_ID}`\n"
            "- semantic model calls: 0\n"
        ).encode("ascii"),
    )
    registry_path = control_dir / "artifact-registry.jsonl"
    build_artifact_registry(output_dir, registry_path, allow_synthetic=True)
    registry = validate_artifact_registry(
        output_dir, registry_path, allow_synthetic=True
    )
    validate_frozen(snapshot, control_dir)

    return {
        "status": "PASS",
        "semantic_model_calls": 0,
        "chapter_body_reads": 0,
        "mode": "synthetic_preflight",
        "read_set": [WRITER_SOURCE.as_posix()],
        "contract_hashes": rendered["hashes"],
        "contract_structure": rendered["structure"],
        "freeze_immutability": "PASS",
        "artifact_registry": registry,
        "output_dir": str(output_dir),
    }


def bootstrap_contract_bundle(workspace: Path, control_dir: Path) -> dict[str, object]:
    rendered = render_contract_bundle(workspace, control_dir)
    snapshot = freeze_snapshot(control_dir)
    validated = validate_contract_bundle(workspace, control_dir)
    validate_frozen(snapshot, control_dir)
    return {
        "status": "PASS",
        "mode": "official_contract_bootstrap",
        "semantic_model_calls": 0,
        "chapter_body_reads": 0,
        "read_set": [WRITER_SOURCE.as_posix()],
        "contract_hashes": validated["hashes"],
        "contract_structure": validated["structure"],
        "freeze_immutability": "PASS",
        "created_files": [
            *(f"control/{name}" for name in CONTRACT_FILENAMES),
            "control/contract-manifest.md",
        ],
        "synthetic_artifacts_created": 0,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--workspace", type=Path, required=True)
    preflight.add_argument("--output-dir", type=Path, required=True)

    bootstrap = subparsers.add_parser("bootstrap-contracts")
    bootstrap.add_argument("--workspace", type=Path, required=True)
    bootstrap.add_argument("--control-dir", type=Path, required=True)

    validate_contracts = subparsers.add_parser("validate-contracts")
    validate_contracts.add_argument("--workspace", type=Path, required=True)
    validate_contracts.add_argument("--control-dir", type=Path, required=True)

    validate_registry = subparsers.add_parser("validate-registry")
    validate_registry.add_argument("--run-root", type=Path, required=True)
    validate_registry.add_argument("--registry", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "preflight":
            result = run_preflight(args.workspace.resolve(), args.output_dir.resolve())
        elif args.command == "bootstrap-contracts":
            result = bootstrap_contract_bundle(
                args.workspace.resolve(), args.control_dir.resolve()
            )
        elif args.command == "validate-contracts":
            result = validate_contract_bundle(
                args.workspace.resolve(), args.control_dir.resolve()
            )
            result["status"] = "PASS"
        else:
            result = validate_artifact_registry(
                args.run_root.resolve(), args.registry.resolve()
            )
            result["status"] = "PASS"
    except (OSError, UnicodeError, ValueError, PreflightError) as error:
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
