#!/usr/bin/env python3
"""Deterministically verify the T2.2 sufficient-value calibration v3."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parent
REPO = RUN_DIR.parents[1]
RUN_REL = "runs/T2.2-sufficiency-calibration-v3"

START = "e8bd46c166531aa291dd83e89450a1b300f3cb4b"
V2_COMMIT = "0891ecf3366573c2142fb3ce36120dcd0614ebf6"
MAIN_MERGE_BASE = "c9988591b97ed472d2341f0747316d4ea650c9b7"
V2_WORKTREE = Path("/Users/tianqiang/.codex/worktrees/d0fb/readerlab")
V2_VERIFY = V2_WORKTREE / "runs/T2.2-effective-retest-v2/verify.py"

HASHES = {
    "AGENTS.md": "2db26cb8800acfe1220958d5cace4f937a17e0541797c8d89d5105de0090dd6a",
    "PRODUCT-DECISIONS.md": "66f772dd629b1bd1428dfc94ee2c64524f72067a7302d1342c9ef1a2ffa46cce",
    "GOLD-STANDARDS.md": "88bf346022a6b7776042082b3a42798d15ae499d22b0dc5ebb98202f3db13a4b",
    "taskcards/T2.2.md": "126348788576e0a31acafdf6739b8b95479cff8e38e289e4cba7df2b5ff8a38a",
    "audit/manifest.json": "8d4352f8f8cbe62cbee8e75b332428fad844007314bda33f420850c571e6a73d",
    "contracts/T1.8-independent-acceptance.md": "7d8b60170669637ca7aa004e27df6fb301739d1a7009bc6f59e22dd2a48f5093",
    f"{RUN_REL}/packet.md": "e09ce22554cfc693b358348ab85eca794023a9b6df9e6f6e5b339c31668869d0",
    f"{RUN_REL}/product-standard-excerpt.md": "0e199ad969a4e2e6ae2916d638a38ade45c891c94f0d1c5c47f90427b1b3fb27",
    f"{RUN_REL}/judge-brief.md": "cb873e315d5e0ec9d7569667a812837ba8b000dc398c626ae643da3fd6738c88",
    f"{RUN_REL}/judge-input-manifest.json": "d47f3fd4bc4be0246c25d13d26ab06e86a20675778094a530f2cd9e0e0db4fc2",
    f"{RUN_REL}/judge-answers.md": "232364e0bb664e1308d5c2ffd12d07b4d35ca618370407e0aa62aa9bc1dba80f",
    f"{RUN_REL}/scoring-key.json": "71391d6d9f9551fa8ceb844b8aa3dbbd2551cbf5964fceb0924d3273ed7b16bc",
}

OWNER_HASHES = {
    key: HASHES[key]
    for key in (
        "PRODUCT-DECISIONS.md",
        "GOLD-STANDARDS.md",
        "taskcards/T2.2.md",
        "audit/manifest.json",
    )
}

REQUIRED_RUN_FILES = {
    "run-manifest.json",
    "packet.md",
    "product-standard-excerpt.md",
    "judge-brief.md",
    "judge-input-manifest.json",
    "judge-answers.md",
    "scoring-key.json",
    "verify.py",
    "receipt.json",
    "report.md",
}

CASES = [
    (1, "CASE-K7M2Q", "positive", ("放行",)),
    (2, "CASE-C2F6P", "hard_negative", ("拦截",)),
    (3, "CASE-J9W4D", "hard_negative", ("拦截",)),
    (4, "CASE-B9Q5J", "reference", ("放行", "拦截", "边缘")),
    (5, "CASE-M5A8S", "non_pass_borderline", ("边缘", "拦截")),
    (6, "CASE-V8H3L", "positive", ("放行",)),
    (7, "CASE-Q3L7X", "hard_negative", ("拦截",)),
    (8, "CASE-H6N2B", "hard_negative", ("拦截",)),
    (9, "CASE-L3E7W", "reference", ("放行", "拦截", "边缘")),
    (10, "CASE-T8C5R", "hard_negative", ("拦截",)),
    (11, "CASE-D4V9K", "non_pass_borderline", ("边缘", "拦截")),
    (12, "CASE-P7G3M", "non_pass_borderline", ("边缘", "拦截")),
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


def run(command: list[str], cwd: Path = REPO) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"command failed ({' '.join(command)}): {completed.stdout.strip()}")
    return completed.stdout


def git(*args: str) -> str:
    return run(["git", *args]).strip()


def parse_utc(value: str) -> dt.datetime:
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"invalid UTC timestamp {value}: {exc}")


def parse_answers(text: str) -> tuple[dict[str, str], str]:
    metadata = {
        "agent-id": "/root/t2_2_v3_fresh_judge",
        "model": "gpt-5.6-terra",
        "reasoning": "high",
        "fork_turns": "none",
        "calls": "1",
    }
    for key, expected in metadata.items():
        match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
        if not match or match.group(1) != expected:
            fail(f"answers metadata mismatch: {key}")
    completed = re.search(r"(?m)^completed-at-utc:\s*(\S+)\s*$", text)
    if not completed:
        fail("answers missing completion timestamp")

    pieces = re.split(r"(?m)^## (CASE-[A-Z0-9]+)\n", text)[1:]
    if len(pieces) != 24:
        fail("judge answers must contain exactly 12 CASE sections")
    dispositions: dict[str, str] = {}
    for offset in range(0, len(pieces), 2):
        case_id = pieces[offset]
        lines = pieces[offset + 1].rstrip("\n").splitlines()
        if len(lines) != 6:
            fail(f"{case_id} must contain exactly six lines")
        for index, (dimension, allowed) in enumerate(DIMENSIONS.items()):
            prefix = f"{dimension}："
            if not lines[index].startswith(prefix) or "｜" not in lines[index]:
                fail(f"{case_id} invalid {dimension} line")
            judgment, reason = lines[index][len(prefix) :].split("｜", 1)
            if judgment not in allowed or not reason.strip():
                fail(f"{case_id} invalid {dimension} judgment or reason")
        prefix = "最终处置："
        if not lines[5].startswith(prefix):
            fail(f"{case_id} missing final disposition")
        disposition = lines[5][len(prefix) :].strip()
        if disposition not in {"放行", "拦截", "边缘"}:
            fail(f"{case_id} invalid disposition")
        dispositions[case_id] = disposition
    return dispositions, completed.group(1)


def verify_git_and_sources() -> None:
    if git("rev-parse", f"{START}^") != V2_COMMIT:
        fail("first commit parent mismatch")
    if git("merge-base", START, "main") != MAIN_MERGE_BASE:
        fail("main merge-base mismatch")
    if git("show", "-s", "--format=%s", START) != (
        "T2.2-v3: record sufficient-value product standard"
    ):
        fail("first commit message mismatch")
    changed = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", START).splitlines())
    if changed != set(OWNER_HASHES):
        fail(f"first commit changed paths mismatch: {sorted(changed)}")
    run(["git", "cat-file", "-e", f"{V2_COMMIT}^{{commit}}"])

    head = git("rev-parse", "HEAD")
    if head != START:
        if git("rev-parse", "HEAD^") != START:
            fail("current commit is not the single second commit after starting commit")
        if git("show", "-s", "--format=%s", "HEAD") != (
            "T2.2-v3: run sufficient-value judge calibration"
        ):
            fail("second commit message mismatch")
        second_paths = git(
            "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"
        ).splitlines()
        if not second_paths or any(
            not path.startswith(f"{RUN_REL}/") for path in second_paths
        ):
            fail("second commit path scope mismatch")

    tracked_or_staged = git("diff", "--name-only", START).splitlines()
    if any(not path.startswith(f"{RUN_REL}/") for path in tracked_or_staged):
        fail("diff contains a path outside the v3 run")
    status = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    for line in status:
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not path.startswith(f"{RUN_REL}/"):
            fail(f"worktree change outside allowed write closure: {path}")

    for relative_path, expected in HASHES.items():
        path = REPO / relative_path
        if path.is_symlink() or not path.is_file():
            fail(f"fixed file missing or symlink: {relative_path}")
        if sha256_file(path) != expected:
            fail(f"fixed hash mismatch: {relative_path}")


def verify_v2_original_worktree() -> None:
    if V2_WORKTREE.resolve() != Path(
        "/Users/tianqiang/.codex/worktrees/d0fb/readerlab"
    ):
        fail("v2 verifier is not bound to the original evidence worktree")
    status = run(
        ["git", "-C", str(V2_WORKTREE), "status", "--short", "--branch"]
    ).splitlines()
    if len(status) != 1 or not status[0].startswith("## "):
        fail(f"original v2 evidence worktree is not clean: {status}")
    head = run(
        ["git", "-C", str(V2_WORKTREE), "rev-parse", "HEAD"]
    ).strip()
    if head != V2_COMMIT:
        fail("original v2 evidence worktree HEAD mismatch")
    if V2_VERIFY.resolve() != (
        V2_WORKTREE / "runs/T2.2-effective-retest-v2/verify.py"
    ):
        fail("v2 verifier path escaped original evidence worktree")
    output = run([sys.executable, "-B", str(V2_VERIFY)])
    if "VERIFY PASS:" not in output:
        fail("original v2 verifier did not PASS")


def verify_frozen_inputs() -> None:
    packet = (RUN_DIR / "packet.md").read_bytes()
    v2_packet = subprocess.run(
        [
            "git",
            "show",
            f"{V2_COMMIT}:runs/T2.2-effective-retest-v2/packet.md",
        ],
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if v2_packet.returncode != 0 or packet != v2_packet.stdout:
        fail("v3 packet is not byte-identical to packet at the v2 commit")

    product = (REPO / "PRODUCT-DECISIONS.md").read_text(encoding="utf-8")
    start_marker = "### B2 足够增量门槛\n"
    end_marker = "\n图书线长期保留的五项产品语义"
    expected_excerpt = product[
        product.index(start_marker) : product.index(end_marker)
    ].rstrip() + "\n"
    excerpt = (RUN_DIR / "product-standard-excerpt.md").read_text(encoding="utf-8")
    if excerpt != expected_excerpt:
        fail("product standard excerpt is not the exact owner section")
    excerpt_forbidden = re.compile(
        r"CASE-|GOLD-STANDARDS|examples/|(?:^|\D)12(?:\D|$)|"
        r"逐题|分类名单|样张路径|hard[_ -]?negative|borderline|reference",
        re.IGNORECASE,
    )
    if excerpt_forbidden.search(excerpt):
        fail("product standard excerpt contains forbidden answer material")

    packet_text = packet.decode("utf-8")
    brief = (RUN_DIR / "judge-brief.md").read_text(encoding="utf-8")
    answer_leak = re.compile(
        r"CASE-[A-Z0-9]+.*(?:放行|拦截|边缘)|"
        r"(?:放行|拦截|边缘).*CASE-[A-Z0-9]+|"
        r"GOLD-STANDARDS|examples/book|hard[_ -]?negative|borderline|"
        r"v2 judge|judge 错题|逐题答案|产品逐题判词|分类数量",
        re.IGNORECASE,
    )
    for label, text in (("packet", packet_text), ("excerpt", excerpt), ("brief", brief)):
        if answer_leak.search(text):
            fail(f"{label} contains answer leakage")
    if re.search(r"CASE-[A-Z0-9]+", brief):
        fail("judge brief contains case-specific material")

    manifest = read_json(RUN_DIR / "judge-input-manifest.json")
    expected_reads = [
        "AGENTS.md",
        f"{RUN_REL}/product-standard-excerpt.md",
        "contracts/T1.8-independent-acceptance.md",
        f"{RUN_REL}/packet.md",
        f"{RUN_REL}/judge-brief.md",
    ]
    if manifest.get("read_only") != expected_reads:
        fail("judge read-only closure mismatch")
    if manifest.get("write_only") != [f"{RUN_REL}/judge-answers.md"]:
        fail("judge write-only closure mismatch")
    expected_input_hashes = {path: HASHES[path] for path in expected_reads}
    if manifest.get("input_hashes") != expected_input_hashes:
        fail("judge input hashes mismatch")
    if manifest.get("judge_config") != {
        "fork_turns": "none",
        "model": "gpt-5.6-terra",
        "reasoning": "high",
        "calls_allowed": 1,
        "objects_in_call": 12,
    }:
        fail("fresh judge config mismatch")


def verify_scoring() -> dict:
    answers_path = RUN_DIR / "judge-answers.md"
    answers_text = answers_path.read_text(encoding="utf-8")
    dispositions, answers_completed = parse_answers(answers_text)
    expected_order = [case_id for _, case_id, _, _ in CASES]
    if list(dispositions) != expected_order:
        fail("answers case order mismatch")

    key_path = RUN_DIR / "scoring-key.json"
    key = read_json(key_path)
    if key.get("created_after_answers_sha256") != HASHES[f"{RUN_REL}/judge-answers.md"]:
        fail("scoring key is not bound to frozen answers")
    key_cases = key.get("cases")
    if not isinstance(key_cases, list) or len(key_cases) != len(CASES):
        fail("scoring key case count mismatch")
    for expected, actual in zip(CASES, key_cases):
        index, case_id, category, allowed = expected
        if actual != {
            "index": index,
            "id": case_id,
            "category": category,
            "allowed_dispositions": list(allowed),
            "hard_gate": category != "reference",
        }:
            fail(f"scoring key mismatch: {case_id}")

    key_created = key.get("created_at_utc", "")
    if parse_utc(key_created) <= parse_utc(answers_completed):
        fail("scoring key timestamp is not later than answers")
    answers_stat = answers_path.stat()
    key_stat = key_path.stat()
    if hasattr(answers_stat, "st_birthtime") and (
        key_stat.st_birthtime <= answers_stat.st_birthtime
    ):
        fail("scoring key filesystem creation is not later than answers")

    scored_cases = []
    buckets = {
        "positive": {"hits": 0, "total": 0},
        "hard_negative": {"hits": 0, "total": 0},
        "non_pass_borderline": {"hits": 0, "total": 0},
    }
    references = []
    for index, case_id, category, allowed in CASES:
        actual = dispositions[case_id]
        hit = None if category == "reference" else actual in allowed
        if category == "reference":
            references.append({"id": case_id, "disposition": actual})
        else:
            buckets[category]["total"] += 1
            if hit:
                buckets[category]["hits"] += 1
        scored_cases.append(
            {
                "index": index,
                "id": case_id,
                "category": category,
                "allowed": list(allowed),
                "actual": actual,
                "hit": hit,
            }
        )
    result = (
        "PASS"
        if all(bucket["hits"] == bucket["total"] for bucket in buckets.values())
        else "FAIL"
    )
    return {
        "calibration_result": result,
        "positive": buckets["positive"],
        "hard_negative": buckets["hard_negative"],
        "non_pass_borderline": buckets["non_pass_borderline"],
        "references": references,
        "scored_cases": scored_cases,
        "answers_completed_at_utc": answers_completed,
        "key_created_at_utc": key_created,
    }


def verify_receipt_and_report(scoring: dict) -> None:
    manifest = read_json(RUN_DIR / "run-manifest.json")
    if manifest.get("starting_commit") != START:
        fail("run manifest starting commit mismatch")
    if manifest.get("first_commit_parent") != V2_COMMIT:
        fail("run manifest first commit parent mismatch")
    if manifest.get("main_merge_base") != MAIN_MERGE_BASE:
        fail("run manifest merge-base mismatch")
    if manifest.get("owner_hashes") != OWNER_HASHES:
        fail("run manifest owner hashes mismatch")
    if manifest.get("calibration_result") != scoring["calibration_result"]:
        fail("run manifest calibration result mismatch")
    if manifest.get("scoring") != {
        "positive": scoring["positive"],
        "hard_negative": scoring["hard_negative"],
        "non_pass_borderline": scoring["non_pass_borderline"],
        "references": scoring["references"],
    }:
        fail("run manifest scoring mismatch")
    if manifest.get("judge") != {
        "agent_id": "/root/t2_2_v3_fresh_judge",
        "fork_turns": "none",
        "model": "gpt-5.6-terra",
        "reasoning": "high",
        "calls": 1,
        "objects_in_call": 12,
        "completed_at_utc": scoring["answers_completed_at_utc"],
        "input_manifest": f"{RUN_REL}/judge-input-manifest.json",
    }:
        fail("run manifest judge evidence mismatch")
    if manifest.get("key_timing") != {
        "answers_completed_at_utc": scoring["answers_completed_at_utc"],
        "key_created_at_utc": scoring["key_created_at_utc"],
        "key_created_after_answers": True,
    }:
        fail("run manifest key timing mismatch")
    expected_frozen_hashes = {
        "t1_8": HASHES["contracts/T1.8-independent-acceptance.md"],
        "packet": HASHES[f"{RUN_REL}/packet.md"],
        "product_standard_excerpt": HASHES[f"{RUN_REL}/product-standard-excerpt.md"],
        "judge_brief": HASHES[f"{RUN_REL}/judge-brief.md"],
        "judge_input_manifest": HASHES[f"{RUN_REL}/judge-input-manifest.json"],
        "judge_answers": HASHES[f"{RUN_REL}/judge-answers.md"],
        "scoring_key": HASHES[f"{RUN_REL}/scoring-key.json"],
    }
    if manifest.get("frozen_hashes") != expected_frozen_hashes:
        fail("run manifest frozen hashes mismatch")

    receipt = read_json(RUN_DIR / "receipt.json")
    if receipt.get("execution_status") != "COMPLETE":
        fail("receipt execution status mismatch")
    if receipt.get("calibration_result") != scoring["calibration_result"]:
        fail("receipt calibration result mismatch")
    if receipt.get("scoring") != {
        "positive": scoring["positive"],
        "hard_negative": scoring["hard_negative"],
        "non_pass_borderline": scoring["non_pass_borderline"],
        "references": scoring["references"],
        "cases": scoring["scored_cases"],
    }:
        fail("receipt scoring mismatch")
    if receipt.get("key_timing") != {
        "answers_completed_at_utc": scoring["answers_completed_at_utc"],
        "key_created_at_utc": scoring["key_created_at_utc"],
        "key_created_after_answers": True,
    }:
        fail("receipt key timing mismatch")
    expected_hashes = {
        "t1_8": HASHES["contracts/T1.8-independent-acceptance.md"],
        "packet": HASHES[f"{RUN_REL}/packet.md"],
        "product_standard_excerpt": HASHES[f"{RUN_REL}/product-standard-excerpt.md"],
        "judge_brief": HASHES[f"{RUN_REL}/judge-brief.md"],
        "judge_input_manifest": HASHES[f"{RUN_REL}/judge-input-manifest.json"],
        "judge_answers": HASHES[f"{RUN_REL}/judge-answers.md"],
        "scoring_key": HASHES[f"{RUN_REL}/scoring-key.json"],
        "run_manifest": sha256_file(RUN_DIR / "run-manifest.json"),
        "verify_py": sha256_file(RUN_DIR / "verify.py"),
    }
    if receipt.get("hashes") != expected_hashes:
        fail("receipt hashes mismatch")
    if receipt.get("verify") != {
        "v2_original_worktree": "PASS",
        "v3": "PASS",
        "root_validator": "PASS",
        "diff_check": "PASS",
    }:
        fail("receipt verification claims mismatch")

    report = (RUN_DIR / "report.md").read_text(encoding="utf-8")
    required_markers = [
        "# T2.2 足够增量校准 v3 报告",
        "执行状态：`COMPLETE`",
        f"校准成绩：`{scoring['calibration_result']}`",
        "同题校准不证明未知材料泛化",
        "accepted：产品负责人的既有标准已落库；本次校准不是新的产品判词",
        "未 push",
    ]
    for marker in required_markers:
        if marker not in report:
            fail(f"report missing marker: {marker}")


def verify() -> dict:
    entries = {path.name for path in RUN_DIR.iterdir()}
    if entries != REQUIRED_RUN_FILES:
        fail(
            f"run file set mismatch: missing={sorted(REQUIRED_RUN_FILES - entries)}, "
            f"extra={sorted(entries - REQUIRED_RUN_FILES)}"
        )
    for path in [RUN_DIR, *RUN_DIR.rglob("*")]:
        if path.is_symlink():
            fail(f"symlink forbidden: {path.relative_to(REPO)}")
    verify_git_and_sources()
    verify_v2_original_worktree()
    verify_frozen_inputs()
    scoring = verify_scoring()
    verify_receipt_and_report(scoring)
    return scoring


if __name__ == "__main__":
    try:
        computed = verify()
    except AssertionError as exc:
        print(f"VERIFY FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "VERIFY PASS: "
        f"calibration={computed['calibration_result']}; "
        f"positive={computed['positive']['hits']}/{computed['positive']['total']}; "
        f"hard_negative={computed['hard_negative']['hits']}/{computed['hard_negative']['total']}; "
        "non_pass_borderline="
        f"{computed['non_pass_borderline']['hits']}/"
        f"{computed['non_pass_borderline']['total']}; "
        "references="
        + ",".join(
            f"{item['id']}:{item['disposition']}"
            for item in computed["references"]
        )
    )
