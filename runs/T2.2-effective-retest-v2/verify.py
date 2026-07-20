#!/usr/bin/env python3
"""Deterministically verify the T2.2 object-level effective retest v2."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parent
REPO = RUN_DIR.parents[1]

PACKET_SHA256 = "e09ce22554cfc693b358348ab85eca794023a9b6df9e6f6e5b339c31668869d0"
BRIEF_SHA256 = "9002771d3c98094fea8c65b30ec87fdb4a9e1909ae69433fcff568c8aed7620d"
T18_SHA256 = "7d8b60170669637ca7aa004e27df6fb301739d1a7009bc6f59e22dd2a48f5093"
ANSWERS_SHA256 = "66933ee7a2640383420e5fa7f052ab12b450b2c02ec483b826699579cfa6979b"
BASE = "c9988591b97ed472d2341f0747316d4ea650c9b7"
BRANCH = "codex/readerlab-book-t2-2-effective-retest-v2"

REQUIRED_RUN_FILES = {
    "run-manifest.json",
    "packet.md",
    "judge-brief.md",
    "judge-input-manifest.json",
    "judge-answers.md",
    "scoring-key.json",
    "verify.py",
    "receipt.json",
    "report.md",
}

FIXED_FILE_HASHES = {
    "GOLD-STANDARDS.md": "ca87c53ff671f7f9243dc61b519eea89ab69d70c9f5ee25a9de58f3b49b6ee68",
    "contracts/T1.8-independent-acceptance.md": T18_SHA256,
    "contracts/M1-freeze-receipt.md": "6dd5ce00a3a0c14e0c2dc8036e7543c113d885a986b6c393025d60e1e5432aa1",
    "examples/book/positive/automatic-driving-safe-state.md": "61c4962cddbedaf201cefc69b3925a292b9f38b147c3cb88d6cd673f8ba965da",
    "examples/book/positive/demand-pooling.md": "925cdd81638fdd398802083efe739e1b6b024b7abbdde7e58d3e753c0b59f1be",
    "examples/book/negative/innovation-failure-rejected.md": "d7e6507ef8eedf4ad0b80d0a50a1aae77d18f3bbf0975c2f115bcabe446de977",
    "examples/book/negative/lens-core-e1-rejected.md": "49fb54d32afc9a42fd11146668609c3809b33429afd0a23264ed9c2c907e3662",
    "examples/book/negative/lens-core-e2-rejected.md": "af022f6b3a5b57c8d6e4ebc91d8ae473fe27f1ba96a4ff6c69bf3b342d7aeaf1",
    "examples/book/negative/lens-core-e3-rejected.md": "7ae512ada094005cf24a0943faab00f39b8000ac54dbe83d2517b13f6d9f89a5",
    "examples/book/negative/fresh-demo-five-rejected.md": "6e52141085602851e644be4f8841abd4fbb1305e8e56ead32efa1083c234303b",
    "examples/book/negative/harari-chapter01-rejected.md": "f6e050611f578aa62ceb2c0beaf18fbb53bc476bb6df6259f7ffbdc6cb04866c",
    "examples/book/negative/phase4-centralized-rejected.md": "cda357e619321d8649669c3f404e0ff13e784a9f91792872d2629bc2060cbcf7",
    "examples/book/negative/phase4-nearby-rejected.md": "c41f24aa9efefce0814cdc29bb4b7fd2f63f6d29adb6030e4b193dd37a9b13a1",
    "examples/book/reference/r01-r08-borderline.md": "cf5f7e01e02d2c68bd5f14fde1773d4b9cd0b100a38417b243fc5fed92520238",
    "examples/book/reference/book-kernel-h3-borderline.md": "07078e3627ac2ea24b98f2d62c8fff58fc1b578499f3427b0235ad1effe4d0d7",
}

CASES = [
    {
        "index": 1,
        "id": "CASE-K7M2Q",
        "category": "positive",
        "expected": "放行",
        "source": ("examples/book/negative/phase4-centralized-rejected.md", 125, 125, "cfdccb6683867e9567a9460180002f9cec9d1a9bbda7b6cf4f8cfa333ee7d719"),
        "candidate": ("examples/book/positive/automatic-driving-safe-state.md", 7, 7, "4cd03ef04484d778fb4733780ac20ab1bf9a266e7e0c3e22d3a52cc413b5a6d8"),
    },
    {
        "index": 2,
        "id": "CASE-C2F6P",
        "category": "negative",
        "expected": "拦截",
        "source": ("examples/book/negative/innovation-failure-rejected.md", 11, 25, "b323d01419b9641145ebe604ddef1428f88359dccdc6cce98136ca00633b54a7"),
        "candidate": ("examples/book/negative/innovation-failure-rejected.md", 27, 30, "f3319e78ea65497b09b53d6e4f28207dda59019471964967994d3948df9c3591"),
    },
    {
        "index": 3,
        "id": "CASE-J9W4D",
        "category": "negative",
        "expected": "拦截",
        "source": ("examples/book/negative/lens-core-e1-rejected.md", 23, 23, "1444bd2a67463028d24010c613526010300a58245d8d191d3e782f3db1f0f382"),
        "candidate": ("examples/book/negative/lens-core-e1-rejected.md", 25, 27, "3e4bff82810f49894ce7e55c0568fcbc0ae201b17a88748ccba2fc577ddac168"),
    },
    {
        "index": 4,
        "id": "CASE-B9Q5J",
        "category": "reference",
        "expected": None,
        "source": ("examples/book/reference/r01-r08-borderline.md", 6, 6, "eba92155c4c4120ca3bdad9d2d2241dc822e017fe8c55e5621ea5089d08e3a26"),
        "candidate": ("examples/book/reference/r01-r08-borderline.md", 9, 15, "84be856b8319ca742d5aa320394eb7637a5ee823080c25352e4536689b2011a8"),
    },
    {
        "index": 5,
        "id": "CASE-M5A8S",
        "category": "negative",
        "expected": "拦截",
        "source": ("examples/book/negative/lens-core-e2-rejected.md", 7, 11, "7d946c73f067b064a13446ce86e381af28626542c104fda68d23a08726961545"),
        "candidate": ("examples/book/negative/lens-core-e2-rejected.md", 13, 15, "670c2bc1e58531bb7881bfc8a07235da4b6b9dd84185ce62cf53b376ddee17cf"),
    },
    {
        "index": 6,
        "id": "CASE-V8H3L",
        "category": "positive",
        "expected": "放行",
        "source": ("examples/book/negative/phase4-centralized-rejected.md", 129, 133, "955f626344a0c5bbc501c1d994852c5321d4f10a2f44642878148893ec3daf28"),
        "candidate": ("examples/book/positive/demand-pooling.md", 7, 15, "278e2554462069e283631e6d0f2acd38bd42388f8868af40925cb1b92c9bac91"),
    },
    {
        "index": 7,
        "id": "CASE-Q3L7X",
        "category": "negative",
        "expected": "拦截",
        "source": ("examples/book/negative/lens-core-e3-rejected.md", 23, 27, "26f95ee9f1c264bf1f3441fe8960eaf298c27d34840a3441bf07fbee7dc9b5d2"),
        "candidate": ("examples/book/negative/lens-core-e3-rejected.md", 29, 31, "085a18423f49088ec54e4d49dab1ced0f4a686dbe0db8fefe034b70d340a965d"),
    },
    {
        "index": 8,
        "id": "CASE-H6N2B",
        "category": "negative",
        "expected": "拦截",
        "source": ("examples/book/negative/fresh-demo-five-rejected.md", 11, 17, "163ea61be8d1d32012c62cb1ba48ea2b76f5130270b3e5f9b9a9a9264853458b"),
        "candidate": ("examples/book/negative/fresh-demo-five-rejected.md", 21, 27, "8aa8d0721b297741a499e44684340e4d11ffdabd8bec80e03e3613d747482539"),
    },
    {
        "index": 9,
        "id": "CASE-L3E7W",
        "category": "reference",
        "expected": None,
        "source": ("examples/book/reference/book-kernel-h3-borderline.md", 23, 27, "7e9d635734cc6cf2cc69c30628bdd01dedf1bfae9f7a0cb02a14f42c0614e7b0"),
        "candidate": ("examples/book/reference/book-kernel-h3-borderline.md", 29, 31, "41a31120daad3dfb8298fd7f96b97cce3dae138dd479647f34a69a01fd0b6f0a"),
    },
    {
        "index": 10,
        "id": "CASE-T8C5R",
        "category": "negative",
        "expected": "拦截",
        "source": ("examples/book/negative/harari-chapter01-rejected.md", 6, 6, "eba92155c4c4120ca3bdad9d2d2241dc822e017fe8c55e5621ea5089d08e3a26"),
        "candidate": ("examples/book/negative/harari-chapter01-rejected.md", 8, 10, "30e54d7c4b05c13a7c86804c28e3c7dffffb98a4f239f74fd6c506aff533d4dc"),
    },
    {
        "index": 11,
        "id": "CASE-D4V9K",
        "category": "negative",
        "expected": "拦截",
        "source": ("examples/book/negative/phase4-centralized-rejected.md", 11, 29, "f7b5e4e28ad089c003bdda2313f97852b023c5f2f9779761a1f186a0e9e2c65f"),
        "candidate": ("examples/book/negative/phase4-centralized-rejected.md", 295, 297, "8afdab4a6d24664d3ae5e119892eb7f9f6bb2501326f94f3ad940c3f68280d83"),
    },
    {
        "index": 12,
        "id": "CASE-P7G3M",
        "category": "negative",
        "expected": "拦截",
        "source": ("examples/book/negative/phase4-nearby-rejected.md", 11, 29, "f7b5e4e28ad089c003bdda2313f97852b023c5f2f9779761a1f186a0e9e2c65f"),
        "candidate": ("examples/book/negative/phase4-nearby-rejected.md", 31, 33, "3cb3ef142e492970c36582a08557ddef1613498ff2eb2bd65d87e9e9aae7cee0"),
    },
]

DIMENSIONS = {
    "内容增量": {"有实质增量", "无实质增量", "unknown"},
    "解释深度": {"解释充分", "解释不足", "unknown"},
    "原文关联": {"关联成立", "关联不成立", "unknown"},
    "认知杠杆": {"形成认知杠杆", "未形成认知杠杆", "unknown"},
    "呈现质量": {"呈现清楚", "呈现妨碍理解", "unknown"},
}


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid JSON {path.relative_to(REPO)}: {exc}")


def extract_bytes(relative_path: str, start: int, end: int) -> bytes:
    lines = (REPO / relative_path).read_bytes().splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        fail(f"invalid line range {relative_path}:{start}-{end}")
    return b"".join(lines[start - 1 : end])


def display_text(data: bytes, strip_quote_prefix: bool) -> str:
    text = data.decode("utf-8").rstrip("\n")
    if not strip_quote_prefix:
        return text
    normalized = []
    for line in text.splitlines():
        if line == ">":
            normalized.append("")
        elif line.startswith("> "):
            normalized.append(line[2:])
        else:
            normalized.append(line)
    return "\n".join(normalized)


def parse_packet(text: str) -> dict[str, tuple[str, str]]:
    pieces = re.split(r"(?m)^## (CASE-[A-Z0-9]+)\n\n", text)[1:]
    if len(pieces) != 24:
        fail("packet must contain exactly 12 CASE sections")
    sections = {}
    for offset in range(0, len(pieces), 2):
        case_id = pieces[offset]
        body = pieces[offset + 1].rstrip("\n")
        prefix = "### 原文片段\n\n"
        separator = "\n\n### 候选陪读\n\n"
        if not body.startswith(prefix) or body.count(separator) != 1:
            fail(f"packet section shape invalid: {case_id}")
        source, candidate = body[len(prefix) :].split(separator, 1)
        sections[case_id] = (source, candidate)
    return sections


def parse_answers(text: str) -> tuple[dict[str, str], str]:
    pieces = re.split(r"(?m)^## (CASE-[A-Z0-9]+)\n", text)[1:]
    if len(pieces) != 24:
        fail("judge answers must contain exactly 12 CASE sections")
    dispositions = {}
    for offset in range(0, len(pieces), 2):
        case_id = pieces[offset]
        body = pieces[offset + 1].rstrip("\n")
        lines = body.splitlines()
        if len(lines) != 6:
            fail(f"{case_id} must contain exactly six non-heading lines")
        for index, (dimension, allowed) in enumerate(DIMENSIONS.items()):
            prefix = f"{dimension}："
            if not lines[index].startswith(prefix) or "｜" not in lines[index]:
                fail(f"{case_id} invalid {dimension} line")
            judgment, reason = lines[index][len(prefix) :].split("｜", 1)
            if judgment not in allowed or not reason.strip():
                fail(f"{case_id} invalid {dimension} judgment or reason")
        final_prefix = "最终处置："
        if not lines[5].startswith(final_prefix):
            fail(f"{case_id} missing final disposition")
        disposition = lines[5][len(final_prefix) :].strip()
        if disposition not in {"放行", "拦截", "边缘"}:
            fail(f"{case_id} invalid final disposition: {disposition}")
        dispositions[case_id] = disposition
    completed = re.search(r"(?m)^completed-at-utc:\s*(\S+)\s*$", text)
    if not completed:
        fail("answers missing completion timestamp")
    return dispositions, completed.group(1)


def parse_utc(value: str) -> dt.datetime:
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"invalid UTC timestamp {value}: {exc}")


def verify() -> dict:
    actual_run_entries = {path.name for path in RUN_DIR.iterdir()}
    if actual_run_entries != REQUIRED_RUN_FILES:
        fail(
            "run entry set mismatch; "
            f"missing={sorted(REQUIRED_RUN_FILES - actual_run_entries)}, "
            f"extra={sorted(actual_run_entries - REQUIRED_RUN_FILES)}"
        )
    for required_name in REQUIRED_RUN_FILES:
        if not (RUN_DIR / required_name).is_file():
            fail(f"required run entry is not a regular file: {required_name}")

    for path in [RUN_DIR, *RUN_DIR.rglob("*")]:
        if path.is_symlink():
            fail(f"symlink forbidden: {path.relative_to(REPO)}")

    for relative_path, expected_hash in FIXED_FILE_HASHES.items():
        path = REPO / relative_path
        if path.is_symlink() or not path.is_file():
            fail(f"fixed source missing or symlink: {relative_path}")
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            fail(f"fixed source hash mismatch: {relative_path}")

    packet_path = RUN_DIR / "packet.md"
    brief_path = RUN_DIR / "judge-brief.md"
    answers_path = RUN_DIR / "judge-answers.md"
    if sha256_file(packet_path) != PACKET_SHA256:
        fail("packet hash mismatch")
    if sha256_file(brief_path) != BRIEF_SHA256:
        fail("judge brief hash mismatch")
    if sha256_file(REPO / "contracts/T1.8-independent-acceptance.md") != T18_SHA256:
        fail("T1.8 hash mismatch")
    if sha256_file(answers_path) != ANSWERS_SHA256:
        fail("judge answers hash mismatch")

    packet_text = packet_path.read_text(encoding="utf-8")
    forbidden = re.compile(
        r"GOLD-STANDARDS|negative|positive|reference|rejected|"
        r"examples/book|hidden expected|产品判词|源路径|源文件|第\d+行",
        re.IGNORECASE,
    )
    leak = forbidden.search(packet_text)
    if leak:
        fail(f"packet leakage token: {leak.group(0)}")

    packet_sections = parse_packet(packet_text)
    expected_order = [case["id"] for case in CASES]
    if list(packet_sections) != expected_order:
        fail("packet case order mismatch")

    for case in CASES:
        source_path, source_start, source_end, source_hash = case["source"]
        candidate_path, candidate_start, candidate_end, candidate_hash = case["candidate"]
        source_bytes = extract_bytes(source_path, source_start, source_end)
        candidate_bytes = extract_bytes(candidate_path, candidate_start, candidate_end)
        if sha256_bytes(source_bytes) != source_hash:
            fail(f"{case['id']} source extraction hash mismatch")
        if sha256_bytes(candidate_bytes) != candidate_hash:
            fail(f"{case['id']} candidate extraction hash mismatch")
        packet_source, packet_candidate = packet_sections[case["id"]]
        if packet_source != display_text(source_bytes, False):
            fail(f"{case['id']} packet source differs from fixed lines")
        if packet_candidate != display_text(candidate_bytes, True):
            fail(f"{case['id']} packet candidate differs beyond quote normalization")

    input_manifest = read_json(RUN_DIR / "judge-input-manifest.json")
    expected_reads = [
        "AGENTS.md",
        "contracts/T1.8-independent-acceptance.md",
        "runs/T2.2-effective-retest-v2/packet.md",
        "runs/T2.2-effective-retest-v2/judge-brief.md",
    ]
    expected_writes = ["runs/T2.2-effective-retest-v2/judge-answers.md"]
    if input_manifest.get("read_only") != expected_reads:
        fail("judge read-only input closure mismatch")
    if input_manifest.get("write_only") != expected_writes:
        fail("judge write-only output closure mismatch")
    if set(input_manifest) != {"status", "scope", "read_only", "write_only"}:
        fail("judge input manifest contains unexpected fields")

    answers_text = answers_path.read_text(encoding="utf-8")
    required_answer_metadata = [
        "status: frozen",
        "scope: run-only",
        "model: gpt-5.6-terra",
        "reasoning: high",
        "fork_turns: none",
        f"t1.8-actual: {T18_SHA256}",
        f"packet-actual: {PACKET_SHA256}",
        f"judge-brief-actual: {BRIEF_SHA256}",
    ]
    for marker in required_answer_metadata:
        if marker not in answers_text:
            fail(f"answers metadata mismatch: {marker}")
    dispositions, answers_completed_at = parse_answers(answers_text)
    if list(dispositions) != expected_order:
        fail("answers case order mismatch")

    scoring_key = read_json(RUN_DIR / "scoring-key.json")
    if scoring_key.get("created_after_answers_sha256") != ANSWERS_SHA256:
        fail("scoring key not bound to frozen answers")
    key_cases = scoring_key.get("cases")
    if not isinstance(key_cases, list) or len(key_cases) != 12:
        fail("scoring key must contain 12 cases")
    for case, key_case in zip(CASES, key_cases):
        if (
            key_case.get("index") != case["index"]
            or key_case.get("id") != case["id"]
            or key_case.get("expected_category") != case["category"]
            or key_case.get("expected_disposition") != case["expected"]
        ):
            fail(f"scoring key identity mismatch: {case['id']}")
        for role in ("source", "candidate"):
            path, start, end, extraction_hash = case[role]
            key_role = key_case.get(role, {})
            if (
                key_role.get("path") != path
                or key_role.get("file_sha256") != FIXED_FILE_HASHES[path]
                or key_role.get("lines") != [start, end]
                or key_role.get("extraction_sha256") != extraction_hash
            ):
                fail(f"scoring key {role} mismatch: {case['id']}")

    key_created_at = scoring_key.get("created_at_utc", "")
    if parse_utc(key_created_at) <= parse_utc(answers_completed_at):
        fail("scoring key timestamp is not later than answers completion")
    if hasattr(answers_path.stat(), "st_birthtime") and hasattr(
        (RUN_DIR / "scoring-key.json").stat(), "st_birthtime"
    ):
        if (RUN_DIR / "scoring-key.json").stat().st_birthtime <= answers_path.stat().st_birthtime:
            fail("scoring key filesystem creation is not later than answers creation")

    scored = []
    positive_hits = 0
    negative_hits = 0
    references = []
    for case in CASES:
        disposition = dispositions[case["id"]]
        hit = None if case["category"] == "reference" else disposition == case["expected"]
        if case["category"] == "positive" and hit:
            positive_hits += 1
        elif case["category"] == "negative" and hit:
            negative_hits += 1
        elif case["category"] == "reference":
            references.append({"id": case["id"], "disposition": disposition})
        scored.append(
            {
                "index": case["index"],
                "id": case["id"],
                "category": case["category"],
                "expected": case["expected"],
                "actual": disposition,
                "hit": hit,
            }
        )
    exam_result = (
        "PASS" if positive_hits == 2 and negative_hits == 8 else "FAIL"
    )
    result = {
        "exam_result": exam_result,
        "positive": {"hits": positive_hits, "total": 2},
        "negative": {"hits": negative_hits, "total": 8},
        "references": references,
        "scored_cases": scored,
        "answers_completed_at_utc": answers_completed_at,
        "key_created_at_utc": key_created_at,
    }

    manifest = read_json(RUN_DIR / "run-manifest.json")
    if manifest.get("base") != BASE or manifest.get("branch") != BRANCH:
        fail("run manifest branch/base mismatch")
    if manifest.get("case_order") != expected_order:
        fail("run manifest case order mismatch")
    if manifest.get("frozen_hashes") != {
        "t1_8": T18_SHA256,
        "packet": PACKET_SHA256,
        "judge_brief": BRIEF_SHA256,
        "judge_answers": ANSWERS_SHA256,
    }:
        fail("run manifest frozen hashes mismatch")
    if manifest.get("exam_result") != exam_result:
        fail("run manifest exam result mismatch")

    receipt = read_json(RUN_DIR / "receipt.json")
    if receipt.get("execution_status") != "COMPLETE":
        fail("receipt execution status mismatch")
    if receipt.get("exam_result") != exam_result:
        fail("receipt exam result mismatch")
    if receipt.get("scoring") != {
        "positive": result["positive"],
        "negative": result["negative"],
        "references": result["references"],
    }:
        fail("receipt scoring mismatch")
    if receipt.get("key_timing") != {
        "answers_completed_at_utc": answers_completed_at,
        "key_created_at_utc": key_created_at,
        "key_created_after_answers": True,
    }:
        fail("receipt key timing mismatch")
    receipt_hashes = receipt.get("hashes", {})
    artifact_hashes = {
        "t1_8": T18_SHA256,
        "packet": PACKET_SHA256,
        "judge_brief": BRIEF_SHA256,
        "judge_answers": ANSWERS_SHA256,
        "judge_input_manifest": sha256_file(RUN_DIR / "judge-input-manifest.json"),
        "scoring_key": sha256_file(RUN_DIR / "scoring-key.json"),
        "run_manifest": sha256_file(RUN_DIR / "run-manifest.json"),
        "verify_py": sha256_file(RUN_DIR / "verify.py"),
    }
    if receipt_hashes != artifact_hashes:
        fail("receipt artifact hashes mismatch")
    if receipt.get("verify") != {
        "command": "python3 -B runs/T2.2-effective-retest-v2/verify.py",
        "result": "PASS",
    }:
        fail("receipt verification claim mismatch")

    report = (RUN_DIR / "report.md").read_text(encoding="utf-8")
    required_report_markers = [
        "# T2.2 对象级有效性复考 v2 报告",
        "执行状态：`COMPLETE`",
        f"考试成绩：`{exam_result}`",
        f"positive：`{positive_hits}/2`",
        f"negative：`{negative_hits}/8`",
        "root validator 未运行",
        "已暂停的 21 卡恢复控制面",
        "accepted：`unknown`",
    ]
    for marker in required_report_markers:
        if marker not in report:
            fail(f"report missing marker: {marker}")

    return result


if __name__ == "__main__":
    try:
        computed = verify()
    except AssertionError as exc:
        print(f"VERIFY FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "VERIFY PASS: "
        f"exam={computed['exam_result']}; "
        f"positive={computed['positive']['hits']}/{computed['positive']['total']}; "
        f"negative={computed['negative']['hits']}/{computed['negative']['total']}; "
        "references="
        + ",".join(
            f"{item['id']}:{item['disposition']}"
            for item in computed["references"]
        )
    )
