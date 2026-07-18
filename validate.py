#!/usr/bin/env python3
"""Validate the self-contained ReaderLab clean seed without reading legacy paths."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "audit/manifest.json"
TOP_DOCS = {
    "AGENTS.md",
    "README.md",
    "PRODUCT-DECISIONS.md",
    "ENGINEERING-LESSONS.md",
    "GOLD-STANDARDS.md",
}
SUPPORT_DOCS = {
    "blueprints/PIPELINE-MAP.md",
    "references/BOOK-AND-SKILLS-METHODS.md",
}
FORBIDDEN_TEXT = (
    "/Users/",
    "/private/",
    "readerlab-v3",
    "readerlab-rebuild",
    "CORE.md",
    "CURRENT.md",
    ".scratch/",
    "v3/runs/",
    "source_sha256",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owned_files() -> list[Path]:
    return sorted(
        [ROOT / name for name in TOP_DOCS]
        + [ROOT / name for name in SUPPORT_DOCS]
        + list((ROOT / "examples").rglob("*.md")),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def build_manifest() -> dict[str, object]:
    files = owned_files()
    return {
        "schema": "readerlab-clean-seed-manifest/v1",
        "purpose": "只验证当前候选包内部文件；不读取、不引用、不依赖任何旧项目目录。",
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": digest(path),
            }
            for path in files
        ],
    }


def main() -> int:
    if "--write-manifest" in sys.argv:
        MANIFEST.write_text(
            json.dumps(build_manifest(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    errors: list[str] = []
    top_docs = {path.name for path in ROOT.glob("*.md")}
    if top_docs != TOP_DOCS:
        errors.append(f"top-level Markdown mismatch: {sorted(top_docs)}")

    files = owned_files()
    example_files = [path for path in files if "examples" in path.parts]
    expected_counts = {"positive": 4, "negative": 8, "reference": 4}
    observed_counts = {
        kind: sum(1 for path in example_files if kind in path.parts)
        for kind in expected_counts
    }
    if observed_counts != expected_counts:
        errors.append(f"example counts mismatch: {observed_counts}")

    for path in files + [MANIFEST]:
        if not path.is_file():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        if path.is_symlink():
            errors.append(f"symlink forbidden: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                errors.append(f"legacy reference {forbidden!r} in {path.relative_to(ROOT)}")

    for path in [ROOT / name for name in TOP_DOCS | SUPPORT_DOCS]:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if "://" in target or target.startswith(("/", "~")):
                errors.append(f"non-local link in {path.name}: {target}")
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"link escapes clean seed in {path.name}: {target}")
                continue
            if not resolved.is_file():
                errors.append(f"broken link in {path.name}: {target}")

    if not MANIFEST.is_file():
        errors.append("audit/manifest.json missing")
    else:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if manifest != build_manifest():
            errors.append("internal manifest does not match current clean-seed files")
        manifest_text = MANIFEST.read_text(encoding="utf-8")
        if re.search(r"(?:/Users/|/private/|readerlab-v3|readerlab-rebuild)", manifest_text):
            errors.append("manifest contains a legacy or absolute path")

    all_paths = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
    ]
    if any(path.endswith(".asset") for path in all_paths):
        errors.append("opaque .asset file found")
    if any("saturn" in path.lower() for path in all_paths):
        errors.append("product-owner rejected Saturn example was copied")

    if errors:
        print("clean seed validation FAILED")
        print("\n".join(errors))
        return 1

    print(
        "clean seed validation PASSED: "
        f"3 authority documents, 2 project entry documents, "
        f"{len(SUPPORT_DOCS)} derived support documents, "
        f"{len(example_files)} readable example files, "
        "0 legacy paths, 0 opaque assets, internal-only manifest."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
