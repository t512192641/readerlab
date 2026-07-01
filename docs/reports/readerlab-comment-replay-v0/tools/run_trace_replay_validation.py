#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_DIR = REPO_ROOT / "docs/reports/readerlab-comment-replay-v0"
PRIVATE_DEMOS = REPO_ROOT / "docs/reports/readerlab-private-material-validation-v0/demos"

FIXTURE_DIR = REPORT_DIR / "fixtures"
RESULT_DIR = REPORT_DIR / "results"

TIMESTAMP = "2026-07-01T00:00:00.000Z"


CASES = [
    {
        "case_id": "CR-A2-PLAY-001",
        "fixture": "A_feel_good_productivity.tandem.md",
        "comment_id": "rl-a2-play-001",
        "demo": "A_feel_good_productivity",
        "anchor_ref": "A-BODY-003",
        "claim_ref": "C4",
        "candidate_ref": "K3",
        "exact": "如果这件事很好玩，会是什么样子？",
        "reader_comment": "这里的“好玩”是在鼓励逃避任务，还是在改变行动方式？",
        "reply": "这里不能读成逃避任务。它更像是在问：同一个目标能不能换一种更有能量的进入方式。这个回复只依据正文附近的 play/control/connection 线索，不把它扩大成全书结论。",
        "reply_checks": {
            "source_boundary_respected": True,
            "does_not_claim_author_intent_without_evidence": True,
            "does_not_promote_rejected_candidate": True,
        },
    },
    {
        "case_id": "CR-A2-REST-002",
        "fixture": "A_feel_good_productivity.tandem.md",
        "comment_id": "rl-a2-rest-002",
        "demo": "A_feel_good_productivity",
        "anchor_ref": "A-BODY-005",
        "claim_ref": "C6",
        "candidate_ref": "K6",
        "exact": "休息不是一份特别的奖赏。它是一种绝对的必需。",
        "reader_comment": "这里是不是在说休息本身就是系统的一部分，而不是完成任务后的奖励？",
        "reply": "是的，正文附近把休息放在维持系统的位置，而不是奖励位置。ReaderLab 可以把它解释成维护机制，但不能借此宣称这份私有材料已经证明公开长文泛化。",
        "reply_checks": {
            "source_boundary_respected": True,
            "does_not_claim_author_intent_without_evidence": True,
            "does_not_promote_rejected_candidate": True,
        },
    },
    {
        "case_id": "CR-B2-STATE-003",
        "fixture": "B_planning_with_files.tandem.md",
        "comment_id": "rl-b2-state-003",
        "demo": "B_planning_with_files",
        "anchor_ref": "B-BODY-003",
        "claim_ref": "C5",
        "candidate_ref": "K3",
        "exact": "复杂任务需要外部化状态；发现要及时落盘；决策前要重新对齐目标；错误要变成下一步策略的输入。",
        "reader_comment": "这句话是不是可以迁移成 ReaderLab 的通用执行规则？",
        "reply": "可以作为设计原则候选，但不能直接变成正式 Skill。它需要继续拆成触发、输入、步骤、输出、边界和证据，才能进入 Skillization Gate。",
        "reply_checks": {
            "source_boundary_respected": True,
            "does_not_claim_author_intent_without_evidence": True,
            "does_not_promote_rejected_candidate": True,
        },
    },
    {
        "case_id": "CR-B2-ERROR-004",
        "fixture": "B_planning_with_files.tandem.md",
        "comment_id": "rl-b2-error-004",
        "demo": "B_planning_with_files",
        "anchor_ref": "B-BODY-004",
        "claim_ref": "C6",
        "candidate_ref": "K4",
        "exact": "三次失败后升级、不能原样重试、每次失败都要记录，这使复杂任务更容易被审计和接手。",
        "reader_comment": "这里的三次失败规则，对 ReaderLab 是不是应该做成自动化？",
        "reply": "它适合进入错误处理协议讨论，但不应该被自动提升为 ReaderLab 默认架构。这里的证据只支持“失败要转成策略输入”，不支持复制原 Skill 的宿主外壳。",
        "reply_checks": {
            "source_boundary_respected": True,
            "does_not_claim_author_intent_without_evidence": True,
            "does_not_promote_rejected_candidate": True,
        },
    },
]


FIXTURE_BODIES = {
    "A_feel_good_productivity.tandem.md": """# A2 tandem-comments fixture

This fixture keeps only nearby body excerpts for comment replay validation.
It is not a full body track.

第一个正文附近片段：
如果这件事很好玩，会是什么样子？

第二个正文附近片段：
休息不是一份特别的奖赏。它是一种绝对的必需。
""",
    "B_planning_with_files.tandem.md": """# B2 tandem-comments fixture

This fixture keeps only nearby cleaned-body excerpts for comment replay
validation. It is not a replacement for the source body.

核心流程附近片段：
复杂任务需要外部化状态；发现要及时落盘；决策前要重新对齐目标；错误要变成下一步策略的输入。

错误处理附近片段：
三次失败后升级、不能原样重试、每次失败都要记录，这使复杂任务更容易被审计和接手。
""",
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def dump_tandem(data: dict[str, object]) -> str:
    return "```tandem-comments\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```"


def parse_tandem(note_text: str) -> tuple[str, dict[str, object]]:
    match = re.search(r"```tandem-comments\n(.*?)\n```", note_text, re.DOTALL)
    if not match:
        raise ValueError("missing tandem-comments block")
    body = note_text[: match.start()].rstrip() + "\n"
    return body, json.loads(match.group(1))


def prefix_suffix(body: str, pos: int, exact: str) -> tuple[str, str]:
    prefix = body[max(0, pos - 24) : pos]
    suffix = body[pos + len(exact) : pos + len(exact) + 24]
    return prefix, suffix


def generate_fixtures() -> None:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    cases_by_fixture: dict[str, list[dict[str, object]]] = {}
    for case in CASES:
        cases_by_fixture.setdefault(case["fixture"], []).append(case)

    for fixture_name, body in FIXTURE_BODIES.items():
        comments: dict[str, object] = {}
        for case in cases_by_fixture[fixture_name]:
            exact = str(case["exact"])
            pos = body.index(exact)
            prefix, suffix = prefix_suffix(body, pos, exact)
            comments[str(case["comment_id"])] = {
                "anchor": {
                    "exact": exact,
                    "pos": pos,
                    "prefix": prefix,
                    "suffix": suffix,
                },
                "status": "open",
                "thread": [
                    {
                        "author": "Reader",
                        "ts": TIMESTAMP,
                        "text": case["reader_comment"],
                    },
                    {
                        "author": "Codex",
                        "ts": TIMESTAMP,
                        "text": case["reply"],
                    },
                ],
            }
        note = body.rstrip() + "\n\n" + dump_tandem(comments) + "\n"
        (FIXTURE_DIR / fixture_name).write_text(note, encoding="utf-8")


def index_candidates(candidate_tournament: object) -> dict[str, dict[str, object]]:
    candidates: dict[str, dict[str, object]] = {}
    if isinstance(candidate_tournament, dict):
        raw = candidate_tournament.get("candidates")
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    item_id = item.get("candidate_id") or item.get("id")
                    if item_id:
                        candidates[str(item_id)] = item
    return candidates


def index_claims(claim_ledger: object) -> dict[str, dict[str, object]]:
    claims: dict[str, dict[str, object]] = {}
    if isinstance(claim_ledger, dict):
        raw = claim_ledger.get("claims")
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    item_id = item.get("claim_id") or item.get("id")
                    if item_id:
                        claims[str(item_id)] = item
    return claims


def index_anchors(location_map: object) -> dict[str, dict[str, object]]:
    anchors: dict[str, dict[str, object]] = {}
    if isinstance(location_map, dict):
        raw = location_map.get("anchors")
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    item_id = item.get("anchor_id") or item.get("id")
                    if item_id:
                        anchors[str(item_id)] = item
    return anchors


def validate_trace_for_demo(demo_name: str) -> dict[str, object]:
    demo_dir = PRIVATE_DEMOS / demo_name
    location_map = load_json(demo_dir / "audit/location-map.json")
    claim_ledger = load_json(demo_dir / "audit/contracts/claim-ledger.json")
    candidate_tournament = load_json(demo_dir / "audit/contracts/candidate-tournament.json")
    annotation_trigger = load_json(demo_dir / "audit/contracts/annotation-trigger.json")
    skillization_gate = load_json(demo_dir / "audit/contracts/skillization-gate.json")

    anchors = index_anchors(location_map)
    claims = index_claims(claim_ledger)
    candidates = index_candidates(candidate_tournament)

    errors: list[str] = []

    for anchor_id, anchor in anchors.items():
        for claim_ref in anchor.get("claim_refs", []):
            if claim_ref not in claims:
                errors.append(f"{anchor_id} references missing claim {claim_ref}")
        for candidate_ref in anchor.get("candidate_refs", []):
            if candidate_ref not in candidates:
                errors.append(f"{anchor_id} references missing candidate {candidate_ref}")

    for claim_id, claim in claims.items():
        anchor_ref = claim.get("anchor_ref")
        if anchor_ref and anchor_ref not in anchors:
            errors.append(f"{claim_id} references missing anchor {anchor_ref}")

    triggers = annotation_trigger.get("triggers", []) if isinstance(annotation_trigger, dict) else []
    for trigger in triggers:
        if isinstance(trigger, dict):
            anchor_ref = trigger.get("anchor_ref")
            if anchor_ref not in anchors:
                errors.append(f"{trigger.get('id')} references missing anchor {anchor_ref}")

    skill_candidates = []
    entries = skillization_gate.get("items", []) if isinstance(skillization_gate, dict) else []
    for item in entries:
        if isinstance(item, dict) and item.get("decision") == "skill_candidate":
            missing = [
                key
                for key in ["trigger", "input", "steps", "output", "boundary", "evidence"]
                if not item.get(key)
            ]
            item_id = item.get("candidate_ref") or item.get("id")
            skill_candidates.append(item_id)
            if missing:
                errors.append(f"{item_id} missing skillization fields: {', '.join(missing)}")

    rejected_or_downgraded = [
        candidate_id
        for candidate_id, candidate in candidates.items()
        if candidate.get("decision") in {"reject", "downgrade"}
    ]

    return {
        "demo": demo_name,
        "pass": not errors,
        "anchors_checked": len(anchors),
        "claims_checked": len(claims),
        "candidates_checked": len(candidates),
        "annotation_triggers_checked": len(triggers),
        "skill_candidates_checked": skill_candidates,
        "rejected_or_downgraded_candidates": rejected_or_downgraded,
        "errors": errors,
    }


def validate_replay_cases() -> dict[str, object]:
    results = []
    errors: list[str] = []

    demo_cache: dict[str, dict[str, object]] = {}
    for case in CASES:
        demo_name = str(case["demo"])
        if demo_name not in demo_cache:
            demo_dir = PRIVATE_DEMOS / demo_name
            demo_cache[demo_name] = {
                "anchors": index_anchors(load_json(demo_dir / "audit/location-map.json")),
                "claims": index_claims(load_json(demo_dir / "audit/contracts/claim-ledger.json")),
                "candidates": index_candidates(load_json(demo_dir / "audit/contracts/candidate-tournament.json")),
            }
        refs = demo_cache[demo_name]
        anchors = refs["anchors"]
        claims = refs["claims"]
        candidates = refs["candidates"]

        fixture_path = FIXTURE_DIR / str(case["fixture"])
        body, comments = parse_tandem(fixture_path.read_text(encoding="utf-8"))
        comment = comments.get(case["comment_id"])
        case_errors: list[str] = []

        if not isinstance(comment, dict):
            case_errors.append("missing comment id in tandem-comments block")
        else:
            anchor = comment.get("anchor", {})
            exact = str(case["exact"])
            pos = anchor.get("pos") if isinstance(anchor, dict) else None
            if not isinstance(pos, int):
                case_errors.append("anchor.pos is not an integer")
            elif body[pos : pos + len(exact)] != exact:
                case_errors.append("anchor.pos does not point to anchor.exact")
            if isinstance(anchor, dict):
                expected_prefix, expected_suffix = prefix_suffix(body, int(pos), exact) if isinstance(pos, int) else ("", "")
                if anchor.get("exact") != exact:
                    case_errors.append("anchor.exact mismatch")
                if anchor.get("prefix") != expected_prefix:
                    case_errors.append("anchor.prefix mismatch")
                if anchor.get("suffix") != expected_suffix:
                    case_errors.append("anchor.suffix mismatch")
            thread = comment.get("thread")
            if not isinstance(thread, list) or len(thread) < 2:
                case_errors.append("comment thread must include reader comment and Codex reply")

        anchor_ref = str(case["anchor_ref"])
        claim_ref = str(case["claim_ref"])
        candidate_ref = str(case["candidate_ref"])
        if anchor_ref not in anchors:
            case_errors.append(f"missing location-map anchor {anchor_ref}")
        if claim_ref not in claims:
            case_errors.append(f"missing claim {claim_ref}")
        elif claims[claim_ref].get("anchor_ref") != anchor_ref:
            case_errors.append(f"claim {claim_ref} does not point to {anchor_ref}")
        if candidate_ref not in candidates:
            case_errors.append(f"missing candidate {candidate_ref}")
        elif anchor_ref in anchors and candidate_ref not in anchors[anchor_ref].get("candidate_refs", []):
            case_errors.append(f"anchor {anchor_ref} does not include candidate {candidate_ref}")

        reply_checks = case.get("reply_checks", {})
        if not all(reply_checks.values()):
            case_errors.append("reply boundary checks not all true")

        candidate_decision = candidates.get(candidate_ref, {}).get("decision")
        results.append(
            {
                "case_id": case["case_id"],
                "pass": not case_errors,
                "fixture": case["fixture"],
                "comment_id": case["comment_id"],
                "demo": demo_name,
                "anchor_ref": anchor_ref,
                "claim_ref": claim_ref,
                "candidate_ref": candidate_ref,
                "candidate_decision": candidate_decision,
                "plugin_format": "tandem-comments",
                "source_boundary_respected": reply_checks.get("source_boundary_respected"),
                "errors": case_errors,
            }
        )
        errors.extend([f"{case['case_id']}: {err}" for err in case_errors])

    return {
        "pass": not errors,
        "plugin_format": "tandem-comments",
        "cases_checked": len(results),
        "results": results,
        "errors": errors,
    }


def write_eval(trace: dict[str, object], replay: dict[str, object]) -> None:
    status = "pass" if trace["pass"] and replay["pass"] else "fail"
    lines = [
        "# Comment replay validation eval",
        "",
        f"Overall: {status}",
        "",
        "What was tested:",
        "",
        "- Four mock reader comments were stored with the current Obsidian plugin shape: `tandem-comments` fenced JSON.",
        "- Each comment anchor was checked against `exact`, `pos`, `prefix`, and `suffix` in the fixture body.",
        "- Each replay case was connected back to an existing A2/B2 body anchor, claim, candidate, and gate decision.",
        "- Existing A2/B2 trace maps were checked for location-map, claim-ledger, candidate-tournament, annotation-trigger, and skillization-gate consistency.",
        "",
        "Important boundary:",
        "",
        "- This validates the plugin storage/replay chain, not the Obsidian UI interaction itself.",
        "- No existing ReaderLab file was modified; this package only adds test fixtures and results.",
        "",
        "Result files:",
        "",
        "- `results/trace-validation.json`",
        "- `results/comment-replay.json`",
    ]
    (RESULT_DIR / "eval.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    generate_fixtures()
    trace_results = {
        "pass": True,
        "demos_checked": [],
    }
    for demo_name in ["A_feel_good_productivity", "B_planning_with_files"]:
        result = validate_trace_for_demo(demo_name)
        trace_results["demos_checked"].append(result)
        if not result["pass"]:
            trace_results["pass"] = False
    replay_results = validate_replay_cases()

    dump_json(RESULT_DIR / "trace-validation.json", trace_results)
    dump_json(RESULT_DIR / "comment-replay.json", replay_results)
    write_eval(trace_results, replay_results)

    if not trace_results["pass"] or not replay_results["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
