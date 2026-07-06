#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_result(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def item_index(payload: Any, list_key: str, *id_keys: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    if not isinstance(payload, dict):
        return indexed
    raw = payload.get(list_key)
    if not isinstance(raw, list):
        return indexed
    for item in raw:
        if not isinstance(item, dict):
            continue
        for id_key in id_keys:
            item_id = item.get(id_key)
            if item_id:
                indexed[str(item_id)] = item
                break
    return indexed


def parse_tandem(note_text: str) -> tuple[str, dict[str, Any]]:
    match = re.search(r"```tandem-comments\n(.*?)\n```", note_text, re.DOTALL)
    if not match:
        raise ValueError("missing tandem-comments block")
    body = note_text[: match.start()].rstrip() + "\n"
    return body, json.loads(match.group(1))


def prefix_suffix(body: str, pos: int, exact: str) -> tuple[str, str]:
    return (
        body[max(0, pos - 24) : pos],
        body[pos + len(exact) : pos + len(exact) + 24],
    )


def load_demo_refs(demo_dir: Path) -> dict[str, Any]:
    location_map = load_json(demo_dir / "audit/location-map.json")
    claim_ledger = load_json(demo_dir / "audit/contracts/claim-ledger.json")
    candidate_tournament = load_json(demo_dir / "audit/contracts/candidate-tournament.json")
    annotation_trigger = load_json(demo_dir / "audit/contracts/annotation-trigger.json")
    skillization_gate = load_json(demo_dir / "audit/contracts/skillization-gate.json")
    trace_validation_path = demo_dir / "audit/contracts/trace-validation.json"
    trace_validation = load_json(trace_validation_path) if trace_validation_path.exists() else None
    return {
        "anchors": item_index(location_map, "anchors", "anchor_id", "id"),
        "claims": item_index(claim_ledger, "claims", "claim_id", "id"),
        "candidates": item_index(candidate_tournament, "candidates", "candidate_id", "id"),
        "annotation_trigger": annotation_trigger,
        "skillization_gate": skillization_gate,
        "trace_validation": trace_validation,
    }


def validate_trace_validation_contract(refs: dict[str, Any], errors: list[str]) -> dict[str, int]:
    trace_validation = refs.get("trace_validation")
    anchors: dict[str, dict[str, Any]] = refs["anchors"]
    claims: dict[str, dict[str, Any]] = refs["claims"]
    candidates: dict[str, dict[str, Any]] = refs["candidates"]

    if trace_validation is None:
        errors.append("missing audit/contracts/trace-validation.json")
        return {"reader_paragraphs_checked": 0, "candidate_uses_checked": 0, "skill_candidate_traces_checked": 0}
    if not isinstance(trace_validation, dict):
        errors.append("trace-validation.json must be an object")
        return {"reader_paragraphs_checked": 0, "candidate_uses_checked": 0, "skill_candidate_traces_checked": 0}
    if trace_validation.get("contract") != "trace-validation.v1":
        errors.append("trace-validation contract must be trace-validation.v1")

    reader_paragraphs = trace_validation.get("reader_paragraphs", [])
    if not isinstance(reader_paragraphs, list) or not reader_paragraphs:
        errors.append("trace-validation reader_paragraphs is empty")
        reader_paragraphs = []

    for paragraph in reader_paragraphs:
        if not isinstance(paragraph, dict):
            errors.append("trace-validation reader paragraph must be an object")
            continue
        reader_ref = paragraph.get("reader_ref")
        if not reader_ref:
            errors.append("trace-validation reader paragraph missing reader_ref")
        anchor_refs = paragraph.get("anchor_refs", [])
        claim_refs = paragraph.get("claim_refs", [])
        candidate_refs = paragraph.get("candidate_refs", [])
        gate_refs = paragraph.get("gate_refs", [])
        if not isinstance(anchor_refs, list) or not anchor_refs:
            errors.append(f"{reader_ref} has no anchor_refs")
            anchor_refs = []
        if not isinstance(claim_refs, list) or not claim_refs:
            errors.append(f"{reader_ref} has no claim_refs")
            claim_refs = []
        if not isinstance(candidate_refs, list):
            errors.append(f"{reader_ref} candidate_refs must be a list")
            candidate_refs = []
        if not isinstance(gate_refs, list):
            errors.append(f"{reader_ref} gate_refs must be a list")
            gate_refs = []
        if not candidate_refs and not gate_refs:
            errors.append(f"{reader_ref} has no candidate_refs or gate_refs")
        if paragraph.get("trace_status") != "complete":
            errors.append(f"{reader_ref} trace_status must be complete")

        for anchor_ref in anchor_refs:
            if anchor_ref not in anchors:
                errors.append(f"{reader_ref} references missing anchor {anchor_ref}")
        for claim_ref in claim_refs:
            if claim_ref not in claims:
                errors.append(f"{reader_ref} references missing claim {claim_ref}")
        for candidate_ref in candidate_refs:
            if candidate_ref not in candidates:
                errors.append(f"{reader_ref} references missing candidate {candidate_ref}")

    candidate_uses = trace_validation.get("candidate_uses", [])
    if not isinstance(candidate_uses, list):
        errors.append("trace-validation candidate_uses must be a list")
        candidate_uses = []
    for candidate_use in candidate_uses:
        if not isinstance(candidate_use, dict):
            errors.append("trace-validation candidate_use must be an object")
            continue
        candidate_ref = candidate_use.get("candidate_ref")
        if candidate_ref not in candidates:
            errors.append(f"candidate_use references missing candidate {candidate_ref}")
            continue
        if candidate_use.get("decision") != candidates[candidate_ref].get("decision"):
            errors.append(f"candidate_use {candidate_ref} decision does not match candidate-tournament")
        final_use = candidate_use.get("final_use", [])
        if not isinstance(final_use, list) or not final_use:
            errors.append(f"candidate_use {candidate_ref} has no final_use")

    skill_candidate_traces = trace_validation.get("skill_candidate_traces", [])
    if not isinstance(skill_candidate_traces, list):
        errors.append("trace-validation skill_candidate_traces must be a list")
        skill_candidate_traces = []
    for skill_trace in skill_candidate_traces:
        if not isinstance(skill_trace, dict):
            errors.append("trace-validation skill_candidate_trace must be an object")
            continue
        candidate_ref = skill_trace.get("candidate_ref")
        if candidate_ref not in candidates:
            errors.append(f"skill_candidate_trace references missing candidate {candidate_ref}")
        for key in ["has_trigger", "has_input", "has_steps", "has_output", "has_boundary", "has_evidence"]:
            if skill_trace.get(key) is not True:
                errors.append(f"skill_candidate_trace {candidate_ref} {key} must be true")
        evidence_refs = skill_trace.get("evidence_refs", [])
        if not isinstance(evidence_refs, list) or not evidence_refs:
            errors.append(f"skill_candidate_trace {candidate_ref} has no evidence_refs")
            evidence_refs = []
        for evidence_ref in evidence_refs:
            if evidence_ref not in claims and evidence_ref not in anchors:
                errors.append(f"skill_candidate_trace {candidate_ref} references missing evidence {evidence_ref}")
        if skill_trace.get("trace_status") != "complete":
            errors.append(f"skill_candidate_trace {candidate_ref} trace_status must be complete")

    if trace_validation.get("result") != "pass":
        errors.append("trace-validation result must be pass")
    blocking_reasons = trace_validation.get("blocking_reasons", [])
    if not isinstance(blocking_reasons, list):
        errors.append("trace-validation blocking_reasons must be a list")
    elif blocking_reasons:
        errors.append("trace-validation blocking_reasons must be empty for pass")

    return {
        "reader_paragraphs_checked": len(reader_paragraphs),
        "candidate_uses_checked": len(candidate_uses),
        "skill_candidate_traces_checked": len(skill_candidate_traces),
    }


def validate_demo(demo_dir: Path) -> dict[str, Any]:
    refs = load_demo_refs(demo_dir)
    anchors: dict[str, dict[str, Any]] = refs["anchors"]
    claims: dict[str, dict[str, Any]] = refs["claims"]
    candidates: dict[str, dict[str, Any]] = refs["candidates"]
    annotation_trigger: dict[str, Any] = refs["annotation_trigger"]
    skillization_gate: dict[str, Any] = refs["skillization_gate"]

    errors: list[str] = []

    if not anchors:
        errors.append("location-map anchors is empty")
    if not claims:
        errors.append("claim-ledger claims is empty")
    if not candidates:
        errors.append("candidate-tournament candidates is empty")

    trace_counts = validate_trace_validation_contract(refs, errors)

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
        if not isinstance(trigger, dict):
            continue
        trigger_id = trigger.get("trigger_id") or trigger.get("id")
        anchor_ref = trigger.get("anchor_ref")
        if anchor_ref not in anchors:
            errors.append(f"{trigger_id} references missing anchor {anchor_ref}")

    entries = skillization_gate.get("items", []) if isinstance(skillization_gate, dict) else []
    skill_candidates = []
    for item in entries:
        if not isinstance(item, dict) or item.get("decision") != "skill_candidate":
            continue
        candidate_ref = item.get("candidate_ref") or item.get("id")
        skill_candidates.append(candidate_ref)
        missing = [
            key
            for key in ["trigger", "input", "steps", "output", "boundary", "evidence"]
            if not item.get(key)
        ]
        if missing:
            errors.append(f"{candidate_ref} missing skillization fields: {', '.join(missing)}")
        for evidence_ref in item.get("evidence", []):
            if evidence_ref not in claims and evidence_ref not in anchors:
                errors.append(f"{candidate_ref} references missing evidence {evidence_ref}")

    rejected_or_downgraded = [
        candidate_id
        for candidate_id, candidate in candidates.items()
        if candidate.get("decision") in {"reject", "downgrade"}
    ]

    return {
        "demo": demo_dir.name,
        "pass": not errors,
        "anchors_checked": len(anchors),
        "claims_checked": len(claims),
        "candidates_checked": len(candidates),
        **trace_counts,
        "annotation_triggers_checked": len(triggers),
        "skill_candidates_checked": skill_candidates,
        "rejected_or_downgraded_candidates": rejected_or_downgraded,
        "errors": errors,
    }


def validate_replay(cases_path: Path, fixture_dir: Path) -> dict[str, Any]:
    payload = load_json(cases_path)
    cases = payload.get("replays", []) if isinstance(payload, dict) else []
    errors: list[str] = []
    results: list[dict[str, Any]] = []
    demo_cache: dict[str, dict[str, Any]] = {}

    for case in cases:
        if not isinstance(case, dict):
            continue
        case_errors: list[str] = []
        case_id = str(case.get("replay_id") or case.get("case_id"))
        demo_dir = Path(str(case["demo_dir"]))
        if not demo_dir.is_absolute():
            demo_dir = cases_path.parent / demo_dir
        fixture_path = fixture_dir / str(case["fixture"])

        if str(demo_dir) not in demo_cache:
            demo_cache[str(demo_dir)] = load_demo_refs(demo_dir)
        refs = demo_cache[str(demo_dir)]
        anchors: dict[str, dict[str, Any]] = refs["anchors"]
        claims: dict[str, dict[str, Any]] = refs["claims"]
        candidates: dict[str, dict[str, Any]] = refs["candidates"]

        try:
            body, comments = parse_tandem(fixture_path.read_text(encoding="utf-8"))
        except Exception as exc:
            body, comments = "", {}
            case_errors.append(str(exc))

        comment = comments.get(case.get("comment_id")) if isinstance(comments, dict) else None
        if not isinstance(comment, dict):
            case_errors.append("missing comment id in tandem-comments block")
        else:
            anchor = comment.get("anchor", {})
            exact = anchor.get("exact") if isinstance(anchor, dict) else None
            pos = anchor.get("pos") if isinstance(anchor, dict) else None
            if not isinstance(exact, str) or not exact:
                case_errors.append("anchor.exact missing")
            if not isinstance(pos, int):
                case_errors.append("anchor.pos is not an integer")
            elif isinstance(exact, str) and body[pos : pos + len(exact)] != exact:
                case_errors.append("anchor.pos does not point to anchor.exact")
            if isinstance(anchor, dict) and isinstance(pos, int) and isinstance(exact, str):
                expected_prefix, expected_suffix = prefix_suffix(body, pos, exact)
                if anchor.get("prefix") != expected_prefix:
                    case_errors.append("anchor.prefix mismatch")
                if anchor.get("suffix") != expected_suffix:
                    case_errors.append("anchor.suffix mismatch")
            thread = comment.get("thread")
            if not isinstance(thread, list) or len(thread) < 2:
                case_errors.append("comment thread must include reader comment and Codex reply")

        anchor_ref = str(case.get("anchor_ref"))
        claim_ref = str(case.get("claim_ref"))
        candidate_ref = str(case.get("candidate_ref"))
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

        reply = case.get("reply", {})
        if not isinstance(reply, dict):
            case_errors.append("reply missing")
        else:
            for key in [
                "source_boundary_respected",
                "does_not_claim_author_intent_without_evidence",
                "does_not_promote_rejected_candidate",
            ]:
                if reply.get(key) is not True:
                    case_errors.append(f"reply.{key} must be true")

        candidate_decision = candidates.get(candidate_ref, {}).get("decision")
        results.append(
            {
                "replay_id": case_id,
                "pass": not case_errors,
                "comment_source": case.get("comment_source"),
                "plugin_format": "tandem-comments",
                "anchor_ref": anchor_ref,
                "claim_ref": claim_ref,
                "candidate_ref": candidate_ref,
                "candidate_decision": candidate_decision,
                "errors": case_errors,
            }
        )
        errors.extend([f"{case_id}: {err}" for err in case_errors])

    return {
        "pass": not errors,
        "plugin_format": "tandem-comments",
        "cases_checked": len(results),
        "results": results,
        "errors": errors,
    }


def validate_suite(demo_dirs: list[Path], cases_path: Path | None, fixture_dir: Path | None) -> dict[str, Any]:
    demo_results = [validate_demo(path) for path in demo_dirs]
    replay_result = validate_replay(cases_path, fixture_dir) if cases_path and fixture_dir else None
    passed = all(result["pass"] for result in demo_results) and (replay_result is None or replay_result["pass"])
    return {
        "pass": passed,
        "trace_validation": demo_results,
        "comment_replay": replay_result,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ReaderLab trace and comment replay references.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo_parser = subparsers.add_parser("validate-demo")
    demo_parser.add_argument("demo_dir", type=Path)

    replay_parser = subparsers.add_parser("validate-replay")
    replay_parser.add_argument("cases_json", type=Path)
    replay_parser.add_argument("--fixture-dir", type=Path, required=True)

    suite_parser = subparsers.add_parser("validate-suite")
    suite_parser.add_argument("--demo", dest="demo_dirs", type=Path, action="append", required=True)
    suite_parser.add_argument("--cases-json", type=Path)
    suite_parser.add_argument("--fixture-dir", type=Path)

    args = parser.parse_args(argv)
    if args.command == "validate-demo":
        result = validate_demo(args.demo_dir)
    elif args.command == "validate-replay":
        result = validate_replay(args.cases_json, args.fixture_dir)
    else:
        result = validate_suite(args.demo_dirs, args.cases_json, args.fixture_dir)

    dump_result(result)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
