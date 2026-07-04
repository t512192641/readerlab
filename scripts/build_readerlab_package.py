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
DEFAULT_MANIFEST = ROOT / "packaging" / "readerlab-package-manifest.json"
TEXT_EXTS = {".md", ".json", ".py", ".txt", ".yaml", ".yml", ".toml"}
FORBIDDEN_TEXT_MARKERS = (
    "/Users/",
    "技能项目/skills-canonical/packages/gstack",
    "python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation",
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
    "python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation/demos/A_feel_good_productivity --demo tests/fixtures/readerlab/private-material-validation/demos/B_planning_with_files --cases-json tests/fixtures/readerlab/comment-replay/fixtures/comment-replay-cases.json --fixture-dir tests/fixtures/readerlab/comment-replay/fixtures": (
        "python3 scripts/readerlab.py validate-run-config examples/run-config-example.json --no-source-exists-check"
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


def copy_file(source: Path, target: Path, *, sanitize: bool) -> dict[str, Any]:
    if not source.is_file():
        raise SystemExit(f"include source file not found: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if sanitize and is_text_file(source):
        target.write_text(sanitize_text(source.read_text(encoding="utf-8")), encoding="utf-8")
    else:
        shutil.copy2(source, target)
    return {
        "kind": "file",
        "source": str(source.relative_to(ROOT)),
        "target": str(target),
        "sha256": file_sha256(target),
        "bytes": target.stat().st_size,
        "sanitized": sanitize,
    }


def copy_dir(source: Path, target: Path, *, sanitize: bool) -> list[dict[str, Any]]:
    if not source.is_dir():
        raise SystemExit(f"include source directory not found: {source}")
    copied: list[dict[str, Any]] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        copied.append(copy_file(path, target / relative, sanitize=sanitize))
    return copied


def package_rel(path: Path, package_root: Path) -> str:
    return path.relative_to(package_root).as_posix()


def audit_package(package_root: Path) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    files: list[dict[str, Any]] = []
    for path in sorted(package_root.rglob("*")):
        if not path.is_file():
            continue
        rel = package_rel(path, package_root)
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
        "files": files,
        "failures": failures,
    }
    return failures, audit


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_package(manifest_path: Path, output_dir: Path, *, force: bool = False) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    package_root = output_dir / str(manifest.get("package_root_name") or "readerlab")
    if package_root.exists():
        if not force:
            raise SystemExit(f"package output exists; pass --force to replace: {package_root}")
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True)

    copied: list[dict[str, Any]] = []
    for entry in manifest.get("include_files") or []:
        copied.append(
            copy_file(
                ROOT / entry["source"],
                package_root / entry["target"],
                sanitize=bool(entry.get("sanitize")),
            )
        )
    for entry in manifest.get("include_dirs") or []:
        copied.extend(
            copy_dir(
                ROOT / entry["source"],
                package_root / entry["target"],
                sanitize=bool(entry.get("sanitize")),
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

    failures, audit = audit_package(package_root)
    result = {
        "schema": "readerlab.package-build-result.v1",
        "status": "shareable_package_prepared" if not failures else "package_audit_failed",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "package_root": str(package_root),
        "manifest": str(manifest_path),
        "copied": copied,
        "audit": audit,
    }
    write_json(package_root / "PACKAGE_AUDIT.json", audit)
    write_json(package_root / "PACKAGE_MANIFEST.json", result)
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
