#!/usr/bin/env python3
"""Unified deterministic entry point for ReaderLab Book Expert Teaching v0.1.2."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tarfile
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if os.fspath(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, os.fspath(SCRIPT_DIR))

from lib.control import (  # noqa: E402
    ALLOWLIST_SCHEMA,
    DEPTH_SELF_LABEL_RE,
    FIDELITY_STATES,
    FORBIDDEN_PRODUCT_RE,
    REPO_ROOT,
    SCHEMA,
    SKILL_DIR,
    SOURCE_ACCESS_AUDIT_SCOPE,
    SOURCE_ACCESS_SCHEMA,
    SOURCE_BOUNDARY_SCHEMA,
    SKILL_VERSION,
    SkillError,
    TEACHING_STATES,
    allowlist_summary,
    allowlist_urls,
    assert_output_urls_allowed,
    assert_no_forbidden_product_content,
    assert_output_file,
    copy_exclusive,
    file_record,
    load_state,
    now,
    path_from_run,
    publish_exclusive,
    read_json,
    read_source_allowlist,
    read_source_access,
    read_text,
    readable_markdown,
    relative_path,
    render,
    replace_json,
    require_dir,
    require_file,
    resolve_input,
    resolve_run,
    sha256_size,
    skill_fingerprint,
    stage_freeze,
    stable_bytes,
    source_boundary_summary,
    template,
    transition_with_fields,
    update_documents,
    verify_prompt_freeze,
    verify_stage_freeze,
    write_json_exclusive,
    write_text_exclusive,
)


INPUT_NAMES = {
    "source": "source.md",
    "framework": "framework.md",
    "source_map": "source-map.md",
    "source_allowlist": "source-allowlist.json",
}
EXPERT_LOCAL_READ_SET = [
    "inputs/source.md",
    "inputs/framework.md",
    "inputs/source-map.md",
    "control/expert-task.md",
]
REVIEW_LOCAL_READ_SET = [
    "inputs/source.md",
    "inputs/framework.md",
    "inputs/source-map.md",
    "raw/expert-teaching-draft.md",
    "raw/expert-teaching-source-map.md",
    "control/review-task.md",
]
EXPERT_ACCESS_PATH = "raw/expert-source-access.json"
REVIEW_ACCESS_PATH = "acceptance/reviewer-source-access.json"
TRANSITIONS = {
    ("NONE", "EXPERT_OPEN"),
    ("EXPERT_OPEN", "REVIEW_OPEN"),
    ("REVIEW_OPEN", "REVIEW_TERMINAL"),
    ("REVIEW_TERMINAL", "PRODUCT_READY"),
}


def _nonempty(value: str, label: str) -> str:
    value = value.strip()
    if not value:
        raise SkillError(f"{label} must not be empty")
    return value


def _stage_dir(run: Path) -> Path:
    path = run / "control" / "stage-freezes"
    path.mkdir(parents=True, exist_ok=True)
    return require_dir(path, "stage freeze directory")


def _safe_new_run(run_value: str) -> Path:
    path = Path(run_value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve(strict=False)
    if path.exists() or path.is_symlink():
        raise SkillError(f"refusing to overwrite existing run: {path}")
    if path.name in {"", ".", ".."}:
        raise SkillError("run must name a new directory")
    if path.parent.is_symlink():
        raise SkillError("run parent must not be a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _allowed_sources_text(entries: list[dict[str, Any]]) -> str:
    urls = allowlist_urls(entries, {"allowed"})
    if not urls:
        return "- （没有 allowed URL；保持关闭搜索）"
    return "\n".join(f"- `{url}`（仅限已登记的 allowed URL）" for url in urls)


def _read_set(run: Path, role: str, local_files: list[str], entries: list[dict[str, Any]]) -> dict[str, Any]:
    summary = allowlist_summary(entries)
    return {
        "schema": "readerlab-book-expert-teaching/read-set/v1.1",
        "role": role,
        "exact_local_files": local_files,
        "allowed_source_urls": summary["allowed_urls"],
        "source_status_counts": summary["status_counts"],
        "registered_redirect_count": sum(len(entry["redirects"]) for entry in entries),
        "network": "allowed URLs and explicitly registered redirects only; no open-ended search",
        "forbidden": [
            "old runs",
            "other agents or hidden reasoning",
            "Writer/Reader/ABC/Discovery outputs",
            "product verdicts and route history",
        ],
    }


def _write_read_set(run: Path, relative: str, value: dict[str, Any]) -> None:
    write_json_exclusive(run / relative, value)


def _write_task_files(run: Path, entries: list[dict[str, Any]]) -> None:
    display = run.name
    values = {
        "RUN_NAME": display,
        "RUN_DIR": os.fspath(run),
        "ALLOWED_SOURCES": _allowed_sources_text(entries),
        "EXPERT_READ_SET": "\n".join(f"- `{item}`" for item in EXPERT_LOCAL_READ_SET),
        "REVIEW_READ_SET": "\n".join(f"- `{item}`" for item in REVIEW_LOCAL_READ_SET),
    }
    write_text_exclusive(run / "control/expert-task.md", render(template("expert-task.md"), values))
    write_text_exclusive(run / "control/review-task.md", render(template("expert-review-task.md"), values))
    product_task = (
        f"# 产品审阅包任务 · {display}\n\n"
        "只有在 `SOURCE_FIDELITY_PASS + TEACHING_PASS` 同时成立后才能生成。控制层必须把固定原文转成可读 Markdown，"
        "加入完整专家教学课和固定产品问题，并拒绝原始 XHTML、来源表、内部控制元数据、旧稿和路线元数据。\n"
    )
    write_text_exclusive(run / "control/product-review-task.md", product_task)


def _write_input_freeze(run: Path, original: dict[str, Path], copied: dict[str, dict[str, Any]]) -> None:
    value = {
        "schema": "readerlab-book-expert-teaching/input-freeze/v1",
        "skill_version": SKILL_VERSION,
        "inputs": {
            name: {
                "original_path": os.fspath(original[name]),
                "copied_path": f"inputs/{INPUT_NAMES[name]}",
                **copied[name],
            }
            for name in INPUT_NAMES
        },
    }
    write_json_exclusive(run / "control/input-freeze.json", value)


def _write_prompt_freeze(run: Path) -> None:
    lines = []
    for relative in (
        "control/expert-task.md",
        "control/review-task.md",
        "control/product-review-task.md",
    ):
        digest, size = sha256_size(path_from_run(run, relative))
        lines.append(f"{digest}  {relative}  # {size} bytes")
    write_text_exclusive(run / "control/prompt-freeze.sha256", "\n".join(lines) + "\n")


def _initial_state(
    run: Path,
    original: dict[str, Path],
    copied: dict[str, dict[str, Any]],
    source_boundary: dict[str, Any],
) -> dict[str, Any]:
    created = now()
    return {
        "schema": SCHEMA,
        "skill_version": SKILL_VERSION,
        "run": os.fspath(run),
        "status": "EXPERT_OPEN",
        "created_at": created,
        "updated_at": created,
        "inputs": {
            name: {
                "original_path": os.fspath(original[name]),
                "copied_path": f"inputs/{INPUT_NAMES[name]}",
                **copied[name],
            }
            for name in INPUT_NAMES
        },
        "skill_fingerprint": skill_fingerprint(),
        "source_allowlist": {
            "schema": ALLOWLIST_SCHEMA,
            "path": f"inputs/{INPUT_NAMES['source_allowlist']}",
            "sha256": copied["source_allowlist"]["sha256"],
            "bytes": copied["source_allowlist"]["bytes"],
        },
        "source_boundary": {
            "schema": SOURCE_BOUNDARY_SCHEMA,
            "path": "control/source-boundary.json",
            "sha256": file_record(run / "control/source-boundary.json")["sha256"],
            "bytes": file_record(run / "control/source-boundary.json")["bytes"],
            "summary": source_boundary,
        },
        "expert": {"status": "OPEN"},
        "review": {"status": "NOT_OPEN"},
        "product": {"status": "NOT_CREATED"},
        "transitions": [{"from": "NONE", "to": "EXPERT_OPEN", "at": created}],
    }


def cmd_init(args: argparse.Namespace) -> None:
    if args.skill_version != SKILL_VERSION:
        raise SkillError(f"--skill-version must be {SKILL_VERSION}")
    original = {
        "source": resolve_input(args.source, "source"),
        "framework": resolve_input(args.framework, "framework identity"),
        "source_map": resolve_input(args.source_map, "source map"),
        "source_allowlist": resolve_input(args.source_allowlist, "source allowlist"),
    }
    run = _safe_new_run(args.run)
    try:
        run.mkdir()
        for directory in ("inputs", "control", "raw", "acceptance"):
            (run / directory).mkdir()
        _stage_dir(run)
        copied = {}
        for name, filename in INPUT_NAMES.items():
            copied[name] = copy_exclusive(original[name], run / "inputs" / filename, name)
        entries = read_source_allowlist(run / "inputs/source-allowlist.json")
        source_boundary = source_boundary_summary(
            read_text(run / "inputs/source-map.md", "source map"), entries
        )
        write_json_exclusive(run / "control/source-allowlist.json", allowlist_summary(entries))
        write_json_exclusive(run / "control/source-boundary.json", source_boundary)
        _write_task_files(run, entries)
        _write_read_set(run, "control/expert-read-set.json", _read_set(run, "Expert teaching", EXPERT_LOCAL_READ_SET, entries))
        _write_read_set(run, "control/review-read-set.json", _read_set(run, "Independent review", REVIEW_LOCAL_READ_SET, entries))
        _write_input_freeze(run, original, copied)
        _write_prompt_freeze(run)
        stage_freeze(
            run,
            "stage-0.sha256",
            [
                "inputs/source.md",
                "inputs/framework.md",
                "inputs/source-map.md",
                "inputs/source-allowlist.json",
                "control/source-allowlist.json",
                "control/source-boundary.json",
                "control/expert-task.md",
                "control/review-task.md",
                "control/product-review-task.md",
                "control/expert-read-set.json",
                "control/review-read-set.json",
            ],
        )
        state = _initial_state(run, original, copied, source_boundary)
        write_json_exclusive(run / "run.json", state)
        write_text_exclusive(run / "run-manifest.md", "# pending manifest\n")
        write_text_exclusive(run / "run-ledger.md", "# pending ledger\n")
        update_documents(run, state)
    except Exception:
        # The run is a newly-created target owned by this command; remove only
        # that target on an init failure so a partial run cannot be mistaken for
        # a usable fixture.
        if run.exists() or run.is_symlink():
            shutil.rmtree(run)
        raise
    print(json.dumps({"status": "INITIALIZED", "run": os.fspath(run), "skill_version": SKILL_VERSION}, ensure_ascii=False, sort_keys=True))


def _check_common_frozen(run: Path) -> dict[str, Any]:
    state = load_state(run)
    verify_stage_freeze(run, "stage-0.sha256")
    verify_prompt_freeze(run)
    current_fingerprint = skill_fingerprint()
    if state.get("skill_fingerprint") != current_fingerprint:
        raise SkillError("Skill files changed after init; fixture/run fingerprint drifted")
    for name, record in state["inputs"].items():
        copied = path_from_run(run, record["copied_path"])
        observed = file_record(copied)
        if observed["sha256"] != record["sha256"] or observed["bytes"] != record["bytes"]:
            raise SkillError(f"input hash drift: {name}")
    allowlist_path = path_from_run(run, "inputs/source-allowlist.json")
    entries = read_source_allowlist(allowlist_path)
    summary = read_json(run / "control/source-allowlist.json", "normalized source allowlist")
    if summary != allowlist_summary(entries):
        raise SkillError("source allowlist normalization drifted")
    expected = state.get("source_allowlist", {})
    if expected.get("schema") != ALLOWLIST_SCHEMA or file_record(allowlist_path, run)["sha256"] != expected.get("sha256"):
        raise SkillError("source allowlist record drifted")
    boundary = source_boundary_summary(
        read_text(run / "inputs/source-map.md", "source map"), entries
    )
    boundary_path = run / "control/source-boundary.json"
    boundary_record = state.get("source_boundary", {})
    if boundary_record.get("schema") != SOURCE_BOUNDARY_SCHEMA:
        raise SkillError("source boundary record is missing or has the wrong schema")
    if boundary != read_json(boundary_path, "source boundary summary"):
        raise SkillError("source boundary closure drifted")
    if file_record(boundary_path, run)["sha256"] != boundary_record.get("sha256"):
        raise SkillError("source boundary record drifted")
    return state


def _set_control_fields(run: Path, **fields: Any) -> dict[str, Any]:
    state = load_state(run)
    state.update(fields)
    state["updated_at"] = now()
    replace_json(run / "run.json", state)
    update_documents(run, state)
    return state


def cmd_seal_expert(args: argparse.Namespace) -> None:
    run = resolve_run(args.run)
    state = _check_common_frozen(run)
    if state["status"] != "EXPERT_OPEN":
        raise SkillError("seal-expert requires status EXPERT_OPEN")
    agent_id = _nonempty(args.agent_id, "Expert Agent ID")
    draft = assert_output_file(run, "raw/expert-teaching-draft.md", "Expert teaching draft")
    source_map = assert_output_file(run, "raw/expert-teaching-source-map.md", "Expert source map")
    source_access = assert_output_file(run, EXPERT_ACCESS_PATH, "Expert source access receipt")
    draft_text = read_text(draft, "Expert teaching draft")
    if DEPTH_SELF_LABEL_RE.search(draft_text):
        raise SkillError("Expert teaching draft contains an internal depth self-label")
    entries = read_source_allowlist(run / "inputs/source-allowlist.json")
    assert_output_urls_allowed(draft_text, entries, "Expert teaching draft")
    assert_output_urls_allowed(read_text(source_map, "Expert source map"), entries, "Expert source map")
    access_value = read_source_access(source_access, entries, "Expert source access receipt")
    stage_freeze(
        run,
        "stage-1.sha256",
        ["raw/expert-teaching-draft.md", "raw/expert-teaching-source-map.md", EXPERT_ACCESS_PATH],
    )
    state = transition_with_fields(
        run,
        "EXPERT_OPEN",
        "REVIEW_OPEN",
        {
            "expert": {
                "status": "SEALED",
                "agent_id": agent_id,
                "model": args.model,
                "reasoning": args.reasoning,
                "network": args.network,
                "retries": args.retries,
                "prompt_modified": args.prompt_modified,
                "metadata_provenance": "controller_declared",
                "draft": file_record(draft, run),
                "source_map": file_record(source_map, run),
                "source_access": file_record(source_access, run),
                "source_access_provenance": access_value["provenance"],
                "source_access_audit_scope": access_value["audit_scope"],
            },
            "review": {"status": "OPEN"},
        },
        stage="expert",
        agent_id=agent_id,
    )
    update_documents(run, state)
    print(json.dumps({"status": "EXPERT_SEALED", "run": os.fspath(run), "draft_sha256": state["expert"]["draft"]["sha256"]}, ensure_ascii=False, sort_keys=True))


def _review_terminals(review_path: Path) -> tuple[str, str]:
    lines = read_text(review_path, "review result").splitlines()
    if len(lines) < 2:
        raise SkillError("review result must begin with two terminal lines")
    fidelity = re.fullmatch(r"SOURCE_FIDELITY_FINAL:\s*(\S+)", lines[0])
    teaching = re.fullmatch(r"TEACHING_FINAL:\s*(\S+)", lines[1])
    if not fidelity or fidelity.group(1) not in FIDELITY_STATES:
        raise SkillError("invalid SOURCE_FIDELITY_FINAL terminal")
    if not teaching or teaching.group(1) not in TEACHING_STATES:
        raise SkillError("invalid TEACHING_FINAL terminal")
    return fidelity.group(1), teaching.group(1)


def cmd_seal_review(args: argparse.Namespace) -> None:
    run = resolve_run(args.run)
    state = _check_common_frozen(run)
    if state["status"] != "REVIEW_OPEN":
        raise SkillError("seal-review requires status REVIEW_OPEN")
    reviewer_id = _nonempty(args.reviewer_id, "reviewer Agent ID")
    expert_id = state.get("expert", {}).get("agent_id")
    if reviewer_id == expert_id:
        raise SkillError("Expert and reviewer Agent IDs must be different")
    review_path = assert_output_file(run, "acceptance/expert-teaching-review.md", "review result")
    source_access = assert_output_file(run, REVIEW_ACCESS_PATH, "reviewer source access receipt")
    entries = read_source_allowlist(run / "inputs/source-allowlist.json")
    assert_output_urls_allowed(read_text(review_path, "review result"), entries, "review result")
    access_value = read_source_access(source_access, entries, "reviewer source access receipt")
    fidelity, teaching = _review_terminals(review_path)
    if (run / "acceptance/expert-product-review.md").exists() or (run / "acceptance/expert-product-review.md").is_symlink():
        raise SkillError("review cannot be sealed after a product package exists")
    stage_freeze(run, "stage-2.sha256", ["acceptance/expert-teaching-review.md", REVIEW_ACCESS_PATH])
    state = transition_with_fields(
        run,
        "REVIEW_OPEN",
        "REVIEW_TERMINAL",
        {
            "review": {
                "status": "SEALED",
                "agent_id": reviewer_id,
                "model": args.model,
                "reasoning": args.reasoning,
                "network": args.network,
                "retries": args.retries,
                "prompt_modified": args.prompt_modified,
                "metadata_provenance": "controller_declared",
                "fidelity": fidelity,
                "teaching": teaching,
                "report": file_record(review_path, run),
                "source_access": file_record(source_access, run),
                "source_access_provenance": access_value["provenance"],
                "source_access_audit_scope": access_value["audit_scope"],
            },
            "product": {
                "status": "NOT_CREATED"
                if not (fidelity == "SOURCE_FIDELITY_PASS" and teaching == "TEACHING_PASS")
                else "ELIGIBLE"
            },
        },
        stage="review",
        reviewer_id=reviewer_id,
        fidelity=fidelity,
        teaching=teaching,
    )
    update_documents(run, state)
    print(json.dumps({"status": "REVIEW_SEALED", "run": os.fspath(run), "fidelity": fidelity, "teaching": teaching}, ensure_ascii=False, sort_keys=True))


def cmd_build_product(args: argparse.Namespace) -> None:
    run = resolve_run(args.run)
    state = _check_common_frozen(run)
    if state["status"] != "REVIEW_TERMINAL":
        raise SkillError("build-product-pack requires status REVIEW_TERMINAL")
    if state.get("review", {}).get("fidelity") != "SOURCE_FIDELITY_PASS" or state.get("review", {}).get("teaching") != "TEACHING_PASS":
        raise SkillError("product package requires SOURCE_FIDELITY_PASS + TEACHING_PASS")
    product_path = run / "acceptance/expert-product-review.md"
    if product_path.exists() or product_path.is_symlink():
        raise SkillError("refusing to overwrite existing product package")
    draft = assert_output_file(run, "raw/expert-teaching-draft.md", "Expert teaching draft")
    source_context = readable_markdown(run / "inputs/source.md")
    course = read_text(draft, "Expert teaching draft")
    package_text = render(
        template("product-review.md"),
        {"SOURCE_CONTEXT": source_context, "COURSE": course},
    )
    assert_no_forbidden_product_content(package_text)
    write_text_exclusive(product_path, package_text)
    stage_freeze(run, "stage-3.sha256", ["acceptance/expert-product-review.md"])
    state = transition_with_fields(
        run,
        "REVIEW_TERMINAL",
        "PRODUCT_READY",
        {"product": {"status": "SEALED", "package": file_record(product_path, run)}},
        stage="product",
    )
    update_documents(run, state)
    print(json.dumps({"status": "PRODUCT_PACK_BUILT", "run": os.fspath(run), "sha256": state["product"]["package"]["sha256"]}, ensure_ascii=False, sort_keys=True))


def _verify_read_sets(run: Path) -> None:
    expert = read_json(run / "control/expert-read-set.json", "Expert read set")
    review = read_json(run / "control/review-read-set.json", "review read set")
    entries = read_source_allowlist(run / "inputs/source-allowlist.json")
    summary = allowlist_summary(entries)
    if expert.get("exact_local_files") != EXPERT_LOCAL_READ_SET:
        raise SkillError("Expert read set drifted")
    if review.get("exact_local_files") != REVIEW_LOCAL_READ_SET:
        raise SkillError("review read set drifted")
    for value in (expert, review):
        if value.get("network") != "allowed URLs and explicitly registered redirects only; no open-ended search":
            raise SkillError("read-set network policy drifted")
        if value.get("allowed_source_urls") != summary["allowed_urls"]:
            raise SkillError("read-set allowed URLs drifted")
        if value.get("source_status_counts") != summary["status_counts"]:
            raise SkillError("read-set source status counts drifted")


def _verify_metadata_provenance(state: dict[str, Any]) -> None:
    for role in ("expert", "review"):
        record = state.get(role, {})
        if record.get("status") in {"SEALED", "OPEN"} and record.get("metadata_provenance") not in {
            None,
            "controller_declared",
        }:
            raise SkillError(f"{role} metadata provenance is not controller_declared")


def cmd_verify(args: argparse.Namespace) -> None:
    run = resolve_run(args.run)
    state = _check_common_frozen(run)
    _verify_read_sets(run)
    _verify_metadata_provenance(state)
    transitions = {(event.get("from"), event.get("to")) for event in state.get("transitions", [])}
    if not transitions.issubset(TRANSITIONS):
        raise SkillError("illegal state transition recorded")
    if state["status"] in {"REVIEW_OPEN", "REVIEW_TERMINAL", "PRODUCT_READY"}:
        verify_stage_freeze(run, "stage-1.sha256")
        draft = assert_output_file(run, "raw/expert-teaching-draft.md", "Expert teaching draft")
        source_map = assert_output_file(run, "raw/expert-teaching-source-map.md", "Expert source map")
        source_access = assert_output_file(run, EXPERT_ACCESS_PATH, "Expert source access receipt")
        entries = read_source_allowlist(run / "inputs/source-allowlist.json")
        assert_output_urls_allowed(read_text(draft, "Expert teaching draft"), entries, "Expert teaching draft")
        assert_output_urls_allowed(read_text(source_map, "Expert source map"), entries, "Expert source map")
        read_source_access(source_access, entries, "Expert source access receipt")
        if state.get("expert", {}).get("agent_id") is None:
            raise SkillError("Expert Agent ID missing")
        for key, path in (("draft", draft), ("source_map", source_map), ("source_access", source_access)):
            record = state.get("expert", {}).get(key, {})
            observed = file_record(path, run)
            if observed != record:
                raise SkillError(f"Expert {key} record drifted")
    if state["status"] in {"REVIEW_TERMINAL", "PRODUCT_READY"}:
        verify_stage_freeze(run, "stage-2.sha256")
        report = assert_output_file(run, "acceptance/expert-teaching-review.md", "review result")
        source_access = assert_output_file(run, REVIEW_ACCESS_PATH, "reviewer source access receipt")
        entries = read_source_allowlist(run / "inputs/source-allowlist.json")
        assert_output_urls_allowed(read_text(report, "review result"), entries, "review result")
        read_source_access(source_access, entries, "reviewer source access receipt")
        fidelity, teaching = _review_terminals(report)
        review_state = state.get("review", {})
        if review_state.get("agent_id") in {None, state.get("expert", {}).get("agent_id")}:
            raise SkillError("reviewer Agent ID is missing or equals Expert Agent ID")
        if (fidelity, teaching) != (review_state.get("fidelity"), review_state.get("teaching")):
            raise SkillError("review terminal drifted")
        if file_record(report, run) != review_state.get("report"):
            raise SkillError("review report record drifted")
        if file_record(source_access, run) != review_state.get("source_access"):
            raise SkillError("reviewer source access record drifted")
        product_exists = (run / "acceptance/expert-product-review.md").exists()
        dual_pass = fidelity == "SOURCE_FIDELITY_PASS" and teaching == "TEACHING_PASS"
        if not dual_pass and product_exists:
            raise SkillError("non-dual-pass review has a product package")
    if state["status"] == "PRODUCT_READY":
        verify_stage_freeze(run, "stage-3.sha256")
        package = assert_output_file(run, "acceptance/expert-product-review.md", "product package")
        package_text = read_text(package, "product package")
        assert_no_forbidden_product_content(package_text)
        if file_record(package, run) != state.get("product", {}).get("package"):
            raise SkillError("product package record drifted")
    print(json.dumps({"status": "VERIFY_PASS", "run": os.fspath(run), "state": state["status"]}, ensure_ascii=False, sort_keys=True))


def _archive_entries(run: Path) -> list[Path]:
    entries = []
    for path in sorted(run.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise SkillError(f"archive refuses symlink: {path}")
        if path.is_file():
            entries.append(path)
    return entries


def cmd_archive(args: argparse.Namespace) -> None:
    run = resolve_run(args.run)
    cmd_verify(argparse.Namespace(run=os.fspath(run)))
    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = Path.cwd() / output
    output = output.resolve(strict=False)
    if output.exists() or output.is_symlink():
        raise SkillError(f"refusing to overwrite archive: {output}")
    try:
        output.relative_to(run)
    except ValueError:
        pass
    else:
        raise SkillError("archive output must be outside the run directory")
    require_dir(output.parent, "archive parent")
    entries = _archive_entries(run)
    with tarfile.open(output, mode="w:gz") as archive:
        for path in entries:
            relative = path.relative_to(run).as_posix()
            info = archive.gettarinfo(os.fspath(path), arcname=f"{run.name}/{relative}")
            info.mtime = 0
            with path.open("rb") as handle:
                archive.addfile(info, handle)
    digest, size = sha256_size(output)
    print(json.dumps({"status": "ARCHIVE_CREATED", "archive": os.fspath(output), "sha256": digest, "bytes": size, "entries": len(entries)}, ensure_ascii=False, sort_keys=True))


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ReaderLab Book Expert Teaching Skill v0.1.2")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create and freeze a new Skill run")
    init.add_argument("--source", required=True)
    init.add_argument("--framework", required=True)
    init.add_argument("--source-map", required=True)
    init.add_argument("--source-allowlist", required=True)
    init.add_argument("--run", required=True)
    init.add_argument("--skill-version", required=True)
    init.set_defaults(handler=cmd_init)

    seal_expert = sub.add_parser("seal-expert", help="freeze Expert outputs and open review")
    seal_expert.add_argument("--run", required=True)
    seal_expert.add_argument("--agent-id", required=True)
    seal_expert.add_argument("--model", default="unavailable")
    seal_expert.add_argument("--reasoning", default="unavailable")
    seal_expert.add_argument("--network", default="unavailable")
    seal_expert.add_argument("--retries", default="no")
    seal_expert.add_argument("--prompt-modified", default="no")
    seal_expert.set_defaults(handler=cmd_seal_expert)

    seal_review = sub.add_parser("seal-review", help="freeze independent review terminals")
    seal_review.add_argument("--run", required=True)
    seal_review.add_argument("--reviewer-id", required=True)
    seal_review.add_argument("--model", default="unavailable")
    seal_review.add_argument("--reasoning", default="unavailable")
    seal_review.add_argument("--network", default="unavailable")
    seal_review.add_argument("--retries", default="no")
    seal_review.add_argument("--prompt-modified", default="no")
    seal_review.set_defaults(handler=cmd_seal_review)

    product = sub.add_parser("build-product-pack", help="build the dual-pass product review package")
    product.add_argument("--run", required=True)
    product.set_defaults(handler=cmd_build_product)

    verify = sub.add_parser("verify", help="verify identity, state, outputs, and gates")
    verify.add_argument("--run", required=True)
    verify.set_defaults(handler=cmd_verify)

    archive = sub.add_parser("archive", help="verify and archive a run")
    archive.add_argument("--run", required=True)
    archive.add_argument("--output", required=True)
    archive.set_defaults(handler=cmd_archive)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _argument_parser().parse_args(argv)
    try:
        args.handler(args)
    except (SkillError, OSError, ValueError) as error:
        print(f"skill error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
