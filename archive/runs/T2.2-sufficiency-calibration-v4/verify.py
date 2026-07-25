#!/usr/bin/env python3
"""Deterministic verifier for the T2.2 v4 negative-first calibration run."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "runs/T2.2-sufficiency-calibration-v4"
START = "8df2c7966c2006acab956fb5b9a9aa52d0a68985"
V3_STANDARD = "e8bd46c166531aa291dd83e89450a1b300f3cb4b"
V2_EVIDENCE = "0891ecf3366573c2142fb3ce36120dcd0614ebf6"
MAIN = "c9988591b97ed472d2341f0747316d4ea650c9b7"
V3_BRANCH = "refs/heads/codex/readerlab-book-t2-2-sufficiency-calibration-v3-complete"
V4_BRANCH = "codex/readerlab-book-t2-2-negative-first-calibration-v4"
ARCHITECTURE_REPORT = Path("/private/tmp/readerlab-t2-2-judge-failure-rule-diagnosis-20260720.md")
ARCHITECTURE_HASH = "f5d2be8285285860057d9c9b69bf4f723749dd98ef68ba2e4a7e90a1d197ec16"
T1_8_HASH = "7d8b60170669637ca7aa004e27df6fb301739d1a7009bc6f59e22dd2a48f5093"
PACKET_HASH = "e09ce22554cfc693b358348ab85eca794023a9b6df9e6f6e5b339c31668869d0"
EXCERPT_HASH = "0e199ad969a4e2e6ae2916d638a38ade45c891c94f0d1c5c47f90427b1b3fb27"

CASE_IDS = [
    "CASE-K7M2Q",
    "CASE-C2F6P",
    "CASE-J9W4D",
    "CASE-B9Q5J",
    "CASE-M5A8S",
    "CASE-V8H3L",
    "CASE-Q3L7X",
    "CASE-H6N2B",
    "CASE-L3E7W",
    "CASE-T8C5R",
    "CASE-D4V9K",
    "CASE-P7G3M",
]
VETO_NAMES = [
    "common_sense_small_step",
    "relabel_or_reorganize",
    "external_not_self_contained",
    "load_bearing_direction_miss",
    "unsupported_causal_link",
    "critical_explanation_gap",
    "substantive_unknown",
]
POSITIVE_EVIDENCE = {
    "new_claim",
    "non_obvious_and_important",
    "explanation_chain",
    "load_bearing_hit",
    "cognitive_change",
    "logical_closure",
}
RUN_FILES = {
    "run-manifest.json",
    "packet.md",
    "product-standard-excerpt.md",
    "v4-calibration-contract.md",
    "skeptical-reader-brief.md",
    "skeptical-reader-input-manifest.json",
    "objection-sheet.json",
    "final-judge-brief.md",
    "final-judge-input-manifest.json",
    "final-judgment.json",
    "scoring-key.json",
    "verify.py",
    "receipt.json",
    "report.md",
}
CHANGED_PATHS = {"taskcards/T2.2.md"} | {
    f"runs/T2.2-sufficiency-calibration-v4/{name}" for name in RUN_FILES
}


def fail(message: str) -> None:
    raise AssertionError(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((RUN / name).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    check(result.returncode == 0, f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def current_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", START).splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    return tracked | untracked


def birth_epoch(path: Path) -> int:
    stat = path.stat()
    check(hasattr(stat, "st_birthtime"), f"creation time unavailable for {path}")
    return int(stat.st_birthtime)


def validate_git_and_files() -> None:
    check(git("rev-parse", START) == START, "starting commit missing")
    check(git("rev-parse", f"{START}^") == V3_STANDARD, "starting parent mismatch")
    check(git("rev-parse", f"{V3_STANDARD}^") == V2_EVIDENCE, "v3 parent mismatch")
    check(git("merge-base", START, MAIN) == MAIN, "main merge-base mismatch")
    check(git("rev-parse", "--verify", V3_BRANCH) == START, "durable v3 branch moved")
    check(git("branch", "--show-current") == V4_BRANCH, "wrong v4 branch")
    check(git("merge-base", "--is-ancestor", START, "HEAD") == "", "HEAD is not based on start")
    check(current_paths() == CHANGED_PATHS, f"changed-path closure mismatch: {sorted(current_paths())}")

    actual_files = {
        path.name for path in RUN.iterdir() if path.is_file() or path.is_symlink()
    }
    check(actual_files == RUN_FILES, f"run file closure mismatch: {sorted(actual_files)}")
    for path in RUN.iterdir():
        check(not path.is_symlink(), f"symlink forbidden: {path}")
        check(path.is_file(), f"non-file entry forbidden: {path}")

    check(ARCHITECTURE_REPORT.is_file(), "architecture report missing")
    check(sha(ARCHITECTURE_REPORT) == ARCHITECTURE_HASH, "architecture report hash mismatch")
    check(sha(ROOT / "contracts/T1.8-independent-acceptance.md") == T1_8_HASH, "T1.8 changed")
    check(sha(RUN / "packet.md") == PACKET_HASH, "v4 packet hash mismatch")
    check(sha(RUN / "product-standard-excerpt.md") == EXCERPT_HASH, "v4 excerpt hash mismatch")
    check(
        (RUN / "packet.md").read_bytes()
        == (ROOT / "runs/T2.2-sufficiency-calibration-v3/packet.md").read_bytes(),
        "v3/v4 packet bytes differ",
    )
    check(
        (RUN / "product-standard-excerpt.md").read_bytes()
        == (
            ROOT / "runs/T2.2-sufficiency-calibration-v3/product-standard-excerpt.md"
        ).read_bytes(),
        "v3/v4 excerpt bytes differ",
    )


def validate_manifest(
    manifest: dict,
    *,
    role: str,
    reads: list[str],
    write: str,
    expected_hashes: dict[str, str],
) -> None:
    check(manifest["schema"] == "readerlab-t2.2-v4-role-input-manifest/v1", "manifest schema")
    check(manifest["run_id"] == "T2.2-sufficiency-calibration-v4", "manifest run")
    check(manifest["role"] == role and manifest["status"] == "frozen", "manifest role/status")
    check(
        manifest["invocation"]
        == {
            "model": "gpt-5.6-terra",
            "reasoning": "high",
            "fork_turns": "none",
            "calls": 1,
            "objects_in_call": 12,
        },
        f"{role} invocation mismatch",
    )
    check([item["path"] for item in manifest["allowed_reads"]] == reads, f"{role} reads")
    check(manifest["allowed_writes"] == [write], f"{role} writes")
    for item in manifest["allowed_reads"]:
        path = ROOT / item["path"]
        check(path.is_file() and not path.is_symlink(), f"invalid role input {path}")
        check(item["sha256"] == sha(path), f"role input changed: {path}")
        check(item["sha256"] == expected_hashes[item["path"]], f"unexpected hash: {path}")


def validate_role_inputs_and_timing(run_manifest: dict) -> None:
    skeptical_reads = [
        "AGENTS.md",
        "contracts/T1.8-independent-acceptance.md",
        "runs/T2.2-sufficiency-calibration-v4/packet.md",
        "runs/T2.2-sufficiency-calibration-v4/product-standard-excerpt.md",
        "runs/T2.2-sufficiency-calibration-v4/v4-calibration-contract.md",
        "runs/T2.2-sufficiency-calibration-v4/skeptical-reader-brief.md",
    ]
    final_reads = [
        "AGENTS.md",
        "contracts/T1.8-independent-acceptance.md",
        "runs/T2.2-sufficiency-calibration-v4/packet.md",
        "runs/T2.2-sufficiency-calibration-v4/product-standard-excerpt.md",
        "runs/T2.2-sufficiency-calibration-v4/v4-calibration-contract.md",
        "runs/T2.2-sufficiency-calibration-v4/final-judge-brief.md",
        "runs/T2.2-sufficiency-calibration-v4/objection-sheet.json",
    ]
    hashes = {
        "AGENTS.md": sha(ROOT / "AGENTS.md"),
        "contracts/T1.8-independent-acceptance.md": T1_8_HASH,
        "runs/T2.2-sufficiency-calibration-v4/packet.md": PACKET_HASH,
        "runs/T2.2-sufficiency-calibration-v4/product-standard-excerpt.md": EXCERPT_HASH,
        "runs/T2.2-sufficiency-calibration-v4/v4-calibration-contract.md": sha(
            RUN / "v4-calibration-contract.md"
        ),
        "runs/T2.2-sufficiency-calibration-v4/skeptical-reader-brief.md": sha(
            RUN / "skeptical-reader-brief.md"
        ),
        "runs/T2.2-sufficiency-calibration-v4/final-judge-brief.md": sha(
            RUN / "final-judge-brief.md"
        ),
        "runs/T2.2-sufficiency-calibration-v4/objection-sheet.json": sha(
            RUN / "objection-sheet.json"
        ),
    }
    validate_manifest(
        load("skeptical-reader-input-manifest.json"),
        role="skeptical_reader",
        reads=skeptical_reads,
        write="runs/T2.2-sufficiency-calibration-v4/objection-sheet.json",
        expected_hashes=hashes,
    )
    validate_manifest(
        load("final-judge-input-manifest.json"),
        role="final_judge",
        reads=final_reads,
        write="runs/T2.2-sufficiency-calibration-v4/final-judgment.json",
        expected_hashes=hashes,
    )

    forbidden = (
        "hard_negative",
        "non_pass_borderline",
        "allowed_dispositions",
        "positive_required",
        "hard_negative_required",
        "non_pass_borderline_required",
        "scoring-key.json",
        "judge-answers.md",
    )
    for relative in set(skeptical_reads + final_reads):
        text = (ROOT / relative).read_text(encoding="utf-8")
        check(not any(token in text for token in forbidden), f"answer leakage in {relative}")
    objection_text = (RUN / "objection-sheet.json").read_text(encoding="utf-8")
    check(
        not any(token in objection_text for token in ("放行", "拦截", "边缘", "final_disposition")),
        "skeptical output predicts a disposition",
    )

    timeline = run_manifest["timeline"]
    paths = {
        "skeptical_manifest_birth_epoch": RUN / "skeptical-reader-input-manifest.json",
        "objection_birth_epoch": RUN / "objection-sheet.json",
        "final_manifest_birth_epoch": RUN / "final-judge-input-manifest.json",
        "final_judgment_birth_epoch": RUN / "final-judgment.json",
        "scoring_key_birth_epoch": RUN / "scoring-key.json",
    }
    for field, path in paths.items():
        check(timeline[field] == birth_epoch(path), f"timeline evidence mismatch: {field}")
    values = [timeline[field] for field in paths]
    check(values == sorted(values) and len(set(values)) == len(values), "role/key order invalid")

    check(
        run_manifest["skeptical_reader"]
        == {
            "agent_id": "/root/t2_2_v4_skeptical_reader",
            "model": "gpt-5.6-terra",
            "reasoning": "high",
            "fork_turns": "none",
            "calls": 1,
            "objects_in_call": 12,
            "completed_at_utc": "2026-07-20T16:01:05Z",
        },
        "skeptical agent evidence mismatch",
    )
    check(
        run_manifest["final_judge"]
        == {
            "agent_id": "/root/t2_2_v4_final_judge",
            "model": "gpt-5.6-terra",
            "reasoning": "high",
            "fork_turns": "none",
            "calls": 1,
            "objects_in_call": 12,
            "completed_at_utc": "2026-07-20T16:10:37Z",
        },
        "final agent evidence mismatch",
    )
    check(
        run_manifest["skeptical_reader"]["calls"] + run_manifest["final_judge"]["calls"] == 2,
        "role call total is not two",
    )


def validate_objection_sheet(objection: dict) -> None:
    check(objection["schema"] == "readerlab-t2.2-v4-objection-sheet/v1", "objection schema")
    check(objection["run_id"] == "T2.2-sufficiency-calibration-v4", "objection run")
    check(objection["status"] == "frozen", "objection status")
    check(
        objection["agent"]
        == {
            "id": "/root/t2_2_v4_skeptical_reader",
            "model": "gpt-5.6-terra",
            "reasoning": "high",
            "fork_turns": "none",
            "calls": 1,
        },
        "objection agent mismatch",
    )
    check([case["id"] for case in objection["cases"]] == CASE_IDS, "objection order")
    check(len(set(CASE_IDS)) == 12, "case IDs not unique")
    for case in objection["cases"]:
        check(set(case["veto_checks"]) == set(VETO_NAMES), f"veto keys: {case['id']}")
        strongest = case["strongest_objection"]
        check(strongest["weight"] in {"load_bearing", "non_load_bearing"}, "strongest weight")
        check(bool(strongest["claim"]), "strongest claim missing")
        check(isinstance(strongest["source_quotes"], list), "strongest source quotes")
        check(isinstance(strongest["candidate_quotes"], list), "strongest candidate quotes")
        for veto in case["veto_checks"].values():
            check(veto["status"] in {"present", "absent", "unknown"}, "veto status")
            check(veto["weight"] in {"load_bearing", "non_load_bearing"}, "veto weight")
            check(isinstance(veto["source_quotes"], list), "veto source quotes")
            check(isinstance(veto["candidate_quotes"], list), "veto candidate quotes")
            check(bool(veto["reason"]), "veto reason")
        for key in ("unsupported_links", "judge_must_not_supply"):
            seen: set[str] = set()
            for item in case[key]:
                check(item["id"] not in seen, f"duplicate {key} id")
                seen.add(item["id"])
                check(item["weight"] in {"load_bearing", "non_load_bearing"}, f"{key} weight")
        check("final_disposition" not in case, "skeptical reader supplied disposition")


def mechanical_disposition(objection: dict, judgment: dict) -> tuple[str, list[str], list[str]]:
    hard: list[str] = []
    resolutions = judgment["objection_resolutions"]

    for name in VETO_NAMES:
        veto = objection["veto_checks"][name]
        resolution = resolutions["veto_checks"][name]
        valid_reject = (
            resolution["resolution"] == "rejected" and bool(resolution["candidate_quotes"])
        )
        if veto["status"] == "present" and not valid_reject:
            hard.append(f"veto:{name}")
        if veto["status"] == "unknown" and veto["weight"] == "load_bearing":
            hard.append(f"unknown-veto:{name}")

    if judgment["content_increment"]["value"] == "none":
        hard.append("content_increment=none")
    if judgment["source_relevance"]["value"] == "does_not_hold":
        hard.append("source_relevance=does_not_hold")
    if judgment["cognitive_leverage"]["value"] == "not_formed":
        hard.append("cognitive_leverage=not_formed")
    if judgment["explanation_gap_class"]["value"] == "critical":
        hard.append("explanation_gap_class=critical")
    if judgment["presentation_issue_class"]["value"] == "critical":
        hard.append("presentation_issue_class=critical")
    for name in (
        "content_increment",
        "explanation_depth",
        "source_relevance",
        "cognitive_leverage",
    ):
        if judgment[name]["value"] == "unknown":
            hard.append(f"{name}=unknown")
    for name, evidence in judgment["positive_evidence"].items():
        if evidence["status"] != "supported":
            hard.append(f"positive_evidence:{name}={evidence['status']}")

    if (
        objection["strongest_objection"]["weight"] == "load_bearing"
        and resolutions["strongest_objection"]["resolution"] != "rejected"
    ):
        hard.append("strongest_objection")
    for kind in ("unsupported_links", "judge_must_not_supply"):
        for objection_item, resolution in zip(objection[kind], resolutions[kind]):
            if (
                objection_item["weight"] == "load_bearing"
                and resolution["resolution"] != "rejected"
            ):
                hard.append(f"{kind}:{objection_item['id']}")
    for name in VETO_NAMES:
        veto = objection["veto_checks"][name]
        resolution = resolutions["veto_checks"][name]
        if (
            veto["weight"] == "load_bearing"
            and veto["status"] in {"present", "unknown"}
            and resolution["resolution"] != "rejected"
        ):
            hard.append(f"load-bearing-veto:{name}")

    minor: list[str] = []
    if judgment["explanation_gap_class"]["value"] == "non_critical":
        minor.append("explanation_gap")
    if (
        judgment["presentation_issue_class"]["value"] == "local"
        or judgment["presentation_quality"]["value"] == "unknown"
    ):
        minor.append("presentation_issue")

    all_resolutions = (
        [resolutions["strongest_objection"]]
        + list(resolutions["veto_checks"].values())
        + resolutions["unsupported_links"]
        + resolutions["judge_must_not_supply"]
    )
    all_closed = all(
        item["resolution"] == "rejected" and item["candidate_quotes"]
        for item in all_resolutions
    )
    axes_positive = (
        judgment["content_increment"]["value"] == "substantial"
        and judgment["explanation_depth"]["value"] == "sufficient"
        and judgment["source_relevance"]["value"] == "holds"
        and judgment["cognitive_leverage"]["value"] == "formed"
    )
    all_supported = all(
        item["status"] == "supported" for item in judgment["positive_evidence"].values()
    )
    if hard:
        disposition = "block"
    elif (
        axes_positive
        and judgment["presentation_quality"]["value"] in {"clear", "unknown"}
        and all_supported
        and len(minor) == 1
    ):
        disposition = "borderline"
    elif (
        axes_positive
        and judgment["presentation_quality"]["value"] == "clear"
        and judgment["explanation_gap_class"]["value"] == "none"
        and judgment["presentation_issue_class"]["value"] == "none"
        and all_supported
        and all_closed
        and not minor
    ):
        disposition = "allow"
    else:
        disposition = "block"
    return disposition, hard, minor


def validate_final_and_score(objection: dict, final: dict, key: dict) -> dict:
    check(final["schema"] == "readerlab-t2.2-v4-final-judgment/v1", "final schema")
    check(final["run_id"] == "T2.2-sufficiency-calibration-v4", "final run")
    check(final["status"] == "frozen", "final status")
    check(
        final["agent"]
        == {
            "id": "/root/t2_2_v4_final_judge",
            "model": "gpt-5.6-terra",
            "reasoning": "high",
            "fork_turns": "none",
            "calls": 1,
        },
        "final agent mismatch",
    )
    check([case["id"] for case in final["cases"]] == CASE_IDS, "final order")
    check([case["id"] for case in key["cases"]] == CASE_IDS, "key order")
    check(
        key["created_after_final_judgment_sha256"] == sha(RUN / "final-judgment.json"),
        "key does not bind final judgment",
    )

    axis_values = {
        "content_increment": {"substantial", "none", "unknown"},
        "explanation_depth": {"sufficient", "insufficient", "unknown"},
        "source_relevance": {"holds", "does_not_hold", "unknown"},
        "cognitive_leverage": {"formed", "not_formed", "unknown"},
        "presentation_quality": {"clear", "impairs_understanding", "unknown"},
    }
    subclass_values = {
        "explanation_gap_class": {"none", "critical", "non_critical", "unknown"},
        "presentation_issue_class": {"none", "critical", "local", "unknown"},
    }
    dispositions: dict[str, str] = {}
    for objection_case, case in zip(objection["cases"], final["cases"]):
        for name, allowed in axis_values.items():
            item = case[name]
            check(item["value"] in allowed, f"{case['id']} {name}")
            check(isinstance(item["candidate_quotes"], list), f"{case['id']} candidate quotes")
            check(isinstance(item["source_quotes"], list), f"{case['id']} source quotes")
            check(bool(item["reason"]) and "boundary" in item, f"{case['id']} axis evidence")
        for name, allowed in subclass_values.items():
            item = case[name]
            check(item["value"] in allowed, f"{case['id']} {name}")
            check(isinstance(item["candidate_quotes"], list), f"{case['id']} subclass quotes")
            check(bool(item["reason"]), f"{case['id']} subclass reason")
        check(set(case["positive_evidence"]) == POSITIVE_EVIDENCE, "positive evidence keys")
        for evidence in case["positive_evidence"].values():
            check(evidence["status"] in {"supported", "unsupported", "unknown"}, "evidence status")
            check(isinstance(evidence["candidate_quotes"], list), "evidence quotes")
            check(bool(evidence["reason"]) and "boundary" in evidence, "evidence reason")
            if evidence["status"] == "supported":
                check(bool(evidence["candidate_quotes"]), "supported evidence lacks quote")

        resolutions = case["objection_resolutions"]
        check(
            set(resolutions)
            == {"strongest_objection", "veto_checks", "unsupported_links", "judge_must_not_supply"},
            "resolution groups",
        )
        check(set(resolutions["veto_checks"]) == set(VETO_NAMES), "resolution veto keys")
        check(
            [item["id"] for item in objection_case["unsupported_links"]]
            == [item["id"] for item in resolutions["unsupported_links"]],
            "unsupported link binding",
        )
        check(
            [item["id"] for item in objection_case["judge_must_not_supply"]]
            == [item["id"] for item in resolutions["judge_must_not_supply"]],
            "must-not-supply binding",
        )
        all_resolutions = (
            [resolutions["strongest_objection"]]
            + list(resolutions["veto_checks"].values())
            + resolutions["unsupported_links"]
            + resolutions["judge_must_not_supply"]
        )
        for resolution in all_resolutions:
            check(resolution["resolution"] in {"accepted", "rejected", "unresolved"}, "resolution")
            check(isinstance(resolution["candidate_quotes"], list), "resolution quotes")
            check(bool(resolution["reason"]), "resolution reason")
            if resolution["resolution"] == "rejected":
                check(bool(resolution["candidate_quotes"]), "rejected objection lacks quote")

        derived, hard, minor = mechanical_disposition(objection_case, case)
        check(case["final_disposition"] == derived, f"{case['id']} disposition mismatch")
        check(
            case["aggregation_trace"]["derived_disposition"] == derived,
            f"{case['id']} trace mismatch",
        )
        check(
            case["aggregation_trace"]["minor_count"] == len(case["minor_limitations"]),
            f"{case['id']} minor count",
        )
        check(bool(case["hard_vetoes"]) == bool(hard), f"{case['id']} hard-veto trace")
        check(
            [item["type"] for item in case["minor_limitations"]] == minor,
            f"{case['id']} minor trace",
        )
        dispositions[case["id"]] = derived

    score_cases = []
    groups = {
        "positive": {"hits": 0, "total": 0},
        "hard_negative": {"hits": 0, "total": 0},
        "non_pass_borderline": {"hits": 0, "total": 0},
    }
    references = []
    for expected in key["cases"]:
        actual = dispositions[expected["id"]]
        hit = actual in expected["allowed_dispositions"] if expected["hard_gate"] else None
        score_cases.append(
            {
                "index": expected["index"],
                "id": expected["id"],
                "category": expected["category"],
                "allowed": expected["allowed_dispositions"],
                "actual": actual,
                "hit": hit,
            }
        )
        if expected["hard_gate"]:
            group = groups[expected["category"]]
            group["total"] += 1
            group["hits"] += int(bool(hit))
        else:
            references.append({"id": expected["id"], "disposition": actual})
    result = "PASS" if all(group["hits"] == group["total"] for group in groups.values()) else "FAIL"
    return {
        **groups,
        "references": references,
        "cases": score_cases,
        "calibration_result": result,
    }


def validate_hashes_and_reports(run_manifest: dict, receipt: dict, report: str) -> None:
    frozen = run_manifest["frozen_hashes"]
    for name, expected in frozen.items():
        check(sha(RUN / name) == expected, f"frozen hash mismatch: {name}")
    for name, expected in receipt["hashes"].items():
        path = ROOT / name
        check(path.is_file() and sha(path) == expected, f"receipt hash mismatch: {name}")
    check(receipt["hashes"]["runs/T2.2-sufficiency-calibration-v4/run-manifest.json"] == sha(RUN / "run-manifest.json"), "manifest receipt hash")
    receipt_hash = sha(RUN / "receipt.json")
    check(receipt_hash in report, "report does not bind receipt hash")
    check("执行状态：`COMPLETE`" in report, "report status")
    check("校准成绩：`FAIL`" in report, "report calibration result")
    check("同题校准不证明未知材料泛化" in report, "report missing remaining risk")
    check("未 push" in report, "report missing no-push boundary")

    taskcard = (ROOT / "taskcards/T2.2.md").read_text(encoding="utf-8")
    check("v4 负向先行双角色校准（当前唯一 active gate）" in taskcard, "taskcard active gate")
    check("v4 calibration：`FAIL`" in taskcard, "taskcard v4 result")
    check("不直接生成 v5 Prompt" in taskcard, "taskcard fail next-boundary")
    check("未知材料资格" in taskcard, "taskcard qualification boundary")


def validate_project_checks() -> None:
    root_validation = subprocess.run(
        [sys.executable, "-B", "validate.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    check(root_validation.returncode == 0, f"root validator failed: {root_validation.stderr}")
    diff_check = subprocess.run(
        ["git", "diff", "--check", START],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    check(diff_check.returncode == 0, f"git diff --check failed: {diff_check.stdout}{diff_check.stderr}")


def main() -> None:
    validate_git_and_files()
    run_manifest = load("run-manifest.json")
    check(run_manifest["starting_commit"] == START, "manifest start")
    check(run_manifest["branch"] == V4_BRANCH, "manifest branch")
    check(run_manifest["execution_status"] == "COMPLETE", "manifest execution status")
    check(run_manifest["calibration_result"] == "FAIL", "manifest calibration result")
    validate_role_inputs_and_timing(run_manifest)
    objection = load("objection-sheet.json")
    final = load("final-judgment.json")
    key = load("scoring-key.json")
    validate_objection_sheet(objection)
    scoring = validate_final_and_score(objection, final, key)
    check(scoring == run_manifest["scoring"], "manifest scoring mismatch")
    receipt = load("receipt.json")
    check(receipt["scoring"] == scoring, "receipt scoring mismatch")
    check(receipt["execution_status"] == "COMPLETE", "receipt execution status")
    check(receipt["calibration_result"] == "FAIL", "receipt calibration result")
    validate_hashes_and_reports(
        run_manifest,
        receipt,
        (RUN / "report.md").read_text(encoding="utf-8"),
    )
    validate_project_checks()
    print(
        "T2.2 v4 verification PASSED: execution=COMPLETE; calibration=FAIL; "
        "positive=0/2; hard_negative=5/5; non_pass_borderline=3/3; "
        "two isolated one-shot roles; mechanical aggregation consistent."
    )


if __name__ == "__main__":
    main()
