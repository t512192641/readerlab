#!/usr/bin/env python3
"""Build a sanitized, shareable ReaderLab Skill package."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
DEFAULT_MANIFEST = ROOT / "packaging" / "readerlab-package-manifest.json"
TEXT_EXTS = {".md", ".json", ".py", ".txt", ".yaml", ".yml", ".toml"}
FORBIDDEN_TEXT_MARKERS = (
    "/Users/",
    "/private/",
    "/tmp/",
    "/workspace/",
    "技能项目/skills-canonical/packages/gstack",
    "python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation",
    "active only inside this repository",
    "repo-local only",
)
FORBIDDEN_PATH_PARTS = {
    "reports",
    "private-material-validation",
    "comment-replay",
    "experiments",
}
SANITIZE_REPLACEMENTS = {
    "/Users/tianqiang/.codex/skills/": "~/.codex/skills/",
    "/Users/tianqiang/技能项目/skills-canonical/packages/gstack": "<external-gstack-source-not-in-package>",
    "This Skill is active only inside this repository at `.agents/skills/readerlab/`.": (
        "This Skill is packaged as a shareable ReaderLab Skill candidate. Install it only into a user-approved Codex Skill location."
    ),
    "Do not install it globally or copy it to `~/.codex/skills/` without explicit user approval.": (
        "Do not install it without explicit user approval."
    ),
    "- installing this Skill globally": "- installing this Skill without explicit user approval",
    "Use this checklist before treating `.agents/skills/readerlab/SKILL.md` as repo-local trial ready.": (
        "Use this checklist before treating a built ReaderLab package as shareable-package prepared."
    ),
    "- [ ] Active package remains under `.agents/skills/readerlab/`.": (
        "- [ ] Active package remains inside the approved package or install target."
    ),
    "- [ ] Skill states that it is repo-local only.": "- [ ] Skill states its package and installation boundary.",
    "- [ ] Skill is not installed globally under `~/.codex/skills/`.": (
        "- [ ] Skill is installed only into a user-approved Codex Skill location."
    ),
    "Historical draft source was removed during MEM cleanup; current repo-local source is `.agents/skills/readerlab/`.": (
        "Historical draft source was removed during MEM cleanup; built packages use the package root as their source."
    ),
    "Allowed activation target only after explicit user approval:\n\n```text\n.agents/skills/readerlab/\n```\n\nDo not install to:\n\n```text\n~/.codex/skills/\n```": (
        "Install only into a user-approved Codex Skill location."
    ),
    "- [x] User approved repo-local activation.": "- [x] User approved bounded activation for the relevant stage.",
    "- [x] User confirmed activation is repo-local only.": "- [x] User confirmed activation is bounded to the approved target.",
    "- [x] `reports/review-studio.md` has no blocker for repo-local trial use.": (
        "- [x] No package audit blocker is present for shareable package preparation."
    ),
    "Run these prompts after repo-local activation:": "Run these prompts after bounded activation:",
    "remove .agents/skills/readerlab/": "remove the approved ReaderLab Skill install target",
    "Allowed after repo-local activation:": "Allowed after bounded activation:",
    ".agents/skills/readerlab/examples/run-config-example.json": "examples/run-config-example.json",
    "python3 tests/test_readerlab_trace_validator.py\npython3 tests/test_readerlab.py": (
        "python3 tests/package_smoke_test.py"
    ),
    "python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation/demos/A_feel_good_productivity --demo tests/fixtures/readerlab/private-material-validation/demos/B_planning_with_files --cases-json tests/fixtures/readerlab/comment-replay/fixtures/comment-replay-cases.json --fixture-dir tests/fixtures/readerlab/comment-replay/fixtures": (
        "python3 scripts/readerlab.py validate-run-config examples/run-config-example.json --no-source-exists-check"
    ),
    "refusing to write eval report under LifeAtlas; use /private/tmp or repo-local path": (
        "refusing to write eval report under LifeAtlas; use an explicit temporary or repo-local path"
    ),
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"{path}: manifest must be a JSON object")
    return payload


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS


def sanitize_text(text: str) -> str:
    for old, new in SANITIZE_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def require_within(path: Path, boundary: Path, *, label: str) -> Path:
    resolved = path.resolve()
    boundary_resolved = boundary.resolve()
    if resolved != boundary_resolved and boundary_resolved not in resolved.parents:
        raise SystemExit(f"{label} escapes allowed boundary: {path}")
    return resolved


def source_path(value: str) -> Path:
    return require_within(ROOT / value, ROOT_RESOLVED, label="include source")


def package_path(package_root: Path, value: str) -> Path:
    return require_within(package_root / value, package_root, label="package target")


def copy_file(source: Path, target: Path, *, sanitize: bool, package_root: Path) -> dict[str, Any]:
    source = require_within(source, ROOT_RESOLVED, label="include source")
    target = require_within(target, package_root, label="package target")
    if not source.is_file():
        raise SystemExit(f"include source file not found: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if sanitize and is_text_file(source):
        target.write_text(sanitize_text(source.read_text(encoding="utf-8")), encoding="utf-8")
    else:
        shutil.copy2(source, target)
    return {
        "kind": "file",
        "source": source.relative_to(ROOT_RESOLVED).as_posix(),
        "target": package_rel(target, package_root),
        "sha256": file_sha256(target),
        "bytes": target.stat().st_size,
        "sanitized": sanitize,
    }


def copy_dir(source: Path, target: Path, *, sanitize: bool, package_root: Path) -> list[dict[str, Any]]:
    source = require_within(source, ROOT_RESOLVED, label="include source")
    target = require_within(target, package_root, label="package target")
    if not source.is_dir():
        raise SystemExit(f"include source directory not found: {source}")
    copied: list[dict[str, Any]] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        copied.append(copy_file(path, target / relative, sanitize=sanitize, package_root=package_root))
    return copied


def package_rel(path: Path, package_root: Path) -> str:
    return path.relative_to(package_root.resolve()).as_posix()


def audit_package(package_root: Path) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    files: list[dict[str, Any]] = []
    for path in sorted(package_root.rglob("*")):
        if not path.is_file():
            continue
        rel = package_rel(path, package_root)
        if rel == "PACKAGE_AUDIT.json":
            continue
        files.append({"path": rel, "sha256": file_sha256(path), "bytes": path.stat().st_size})
        parts = set(Path(rel).parts)
        if parts & FORBIDDEN_PATH_PARTS:
            failures.append(f"{rel}: forbidden package path marker")
        if is_text_file(path):
            text = path.read_text(encoding="utf-8")
            for marker in FORBIDDEN_TEXT_MARKERS:
                if marker in text:
                    failures.append(f"{rel}: forbidden text marker {marker!r}")
    audit = {
        "schema": "readerlab.package-audit.v1",
        "status": "fail" if failures else "pass",
        "check_class": "package_boundary_structure",
        "not_reader_acceptance": True,
        "not_production_ready": True,
        "audit_file": "PACKAGE_AUDIT.json",
        "files": files,
        "failures": failures,
    }
    return failures, audit


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copied_for_manifest(copied: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for item in copied:
        entries.append(
            {
                "kind": item["kind"],
                "source": item["source"],
                "target": item["target"],
                "sha256": item["sha256"],
                "bytes": item["bytes"],
                "sanitized": item["sanitized"],
            }
        )
    return entries


def package_manifest_ref(manifest_path: Path) -> str:
    try:
        return manifest_path.relative_to(ROOT_RESOLVED).as_posix()
    except ValueError:
        return manifest_path.name


def ensure_safe_package_root(output_dir: Path, package_root: Path) -> Path:
    output_dir_resolved = output_dir.resolve()
    resolved = package_root.resolve()
    if resolved != output_dir_resolved and output_dir_resolved not in resolved.parents:
        raise SystemExit(f"refusing package output outside --output-dir: {package_root}")
    if resolved == ROOT_RESOLVED or ROOT_RESOLVED in resolved.parents or resolved in ROOT_RESOLVED.parents:
        raise SystemExit(f"refusing to use source checkout as package output: {package_root}")
    return resolved


def build_package(manifest_path: Path, output_dir: Path, *, force: bool = False) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    manifest = read_json(manifest_path)
    output_dir = output_dir.resolve()
    package_root = ensure_safe_package_root(output_dir, output_dir / str(manifest.get("package_root_name") or "readerlab"))
    if package_root.exists():
        if not force:
            raise SystemExit(f"package output exists; pass --force to replace: {package_root}")
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True)

    copied: list[dict[str, Any]] = []
    for entry in manifest.get("include_files") or []:
        copied.append(
            copy_file(
                source_path(entry["source"]),
                package_path(package_root, entry["target"]),
                sanitize=bool(entry.get("sanitize")),
                package_root=package_root,
            )
        )
    for entry in manifest.get("include_dirs") or []:
        copied.extend(
            copy_dir(
                source_path(entry["source"]),
                package_path(package_root, entry["target"]),
                sanitize=bool(entry.get("sanitize")),
                package_root=package_root,
            )
        )

    shutil.copy2(ROOT / "docs" / "readerlab-v2-package-boundary.md", package_root / "PACKAGE_BOUNDARY.md")
    copied.append(
        {
            "kind": "file",
            "source": "docs/readerlab-v2-package-boundary.md",
            "target": "PACKAGE_BOUNDARY.md",
            "sha256": file_sha256(package_root / "PACKAGE_BOUNDARY.md"),
            "bytes": (package_root / "PACKAGE_BOUNDARY.md").stat().st_size,
            "sanitized": False,
        }
    )

    result = {
        "schema": "readerlab.package-build-result.v1",
        "status": "shareable_package_prepared",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "package_root": "readerlab",
        "manifest": package_manifest_ref(manifest_path),
        "copied": copied_for_manifest(copied),
        "audit_file": "PACKAGE_AUDIT.json",
    }
    write_json(package_root / "PACKAGE_MANIFEST.json", result)
    failures, audit = audit_package(package_root)
    if failures:
        result["status"] = "package_audit_failed"
        write_json(package_root / "PACKAGE_MANIFEST.json", result)
        failures, audit = audit_package(package_root)
    write_json(package_root / "PACKAGE_AUDIT.json", audit)
    if failures:
        raise SystemExit("package audit failed:\n- " + "\n- ".join(failures))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(prog="build-readerlab-package")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    result = build_package(Path(args.manifest), Path(args.output_dir), force=args.force)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
