#!/usr/bin/env python3
"""Validate the self-contained ReaderLab clean seed without reading legacy paths."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath


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
    "blueprints/EXECUTION-ROADMAP.md",
    "references/BOOK-AND-SKILLS-METHODS.md",
}
RUNTIME_FILES = {"tools/run.py"}
MATERIAL_GUARD_FILES = {"materials/.gitignore"}
EXPECTED_MATERIALS_GITIGNORE = (
    "# Copyrighted and source materials are ignored by default.\n"
    "*\n"
    "!*/\n"
    "!/.gitignore\n"
    "!.gitkeep\n"
    "!authorization.md\n"
    "!**/.gitkeep\n"
    "!**/authorization.md\n"
)
REQUIRED_DIRECTORIES = {
    "contracts",
    "runs",
    "materials",
    "tools",
    "diagnostics",
    "lenses",
    "taskcards",
}
TASK_IDS = (
    "T0.1",
    "T0.2",
    "T0.3",
    "T1.1",
    "T1.2",
    "T1.3",
    "T1.4",
    "T1.5",
    "T1.6",
    "T1.7",
    "T1.8",
    "T1.9",
    "T2.1",
    "T2.2",
    "T2.3",
    "T3.1",
    "T3.2",
    "T3.3",
    "T3.4",
    "T3.5",
    "T3.6",
    "T4.1",
    "T4.2",
    "T4.3",
)
TASK_SECTION_NAMES = (
    "任务编号与标题",
    "目标",
    "允许读取清单",
    "交付文件清单",
    "硬约束",
    "完成判据",
)
STATEFUL_ROOTS = ("contracts", "lenses", "diagnostics")
STATE_HEADER = re.compile(
    r"\A(?:---\n)?status: (?:draft|frozen)\nscope: (?:long-term|run-only)\n(?:---\n)?"
)
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
        + [ROOT / name for name in RUNTIME_FILES]
        + [ROOT / name for name in MATERIAL_GUARD_FILES]
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


def stateful_files() -> list[Path]:
    files: list[Path] = []
    for directory in STATEFUL_ROOTS:
        root = ROOT / directory
        if root.is_dir() and not root.is_symlink():
            files.extend(path for path in root.rglob("*.md") if path.name != "GLOSSARY.md")
    return files


def required_tree_symlinks() -> list[Path]:
    links: list[Path] = []
    for directory in REQUIRED_DIRECTORIES:
        root = ROOT / directory
        if root.is_symlink():
            links.append(root)
            continue
        if root.is_dir():
            links.extend(path for path in root.rglob("*") if path.is_symlink())
    return links


def validate_run_script(errors: list[str]) -> None:
    run_script = ROOT / "tools/run.py"
    if not run_script.is_file():
        errors.append("tools/run.py missing")
        return
    if run_script.is_symlink():
        errors.append("symlink forbidden: tools/run.py")
        return
    if stat.S_IMODE(run_script.stat().st_mode) & 0o111 != 0o111:
        errors.append("tools/run.py must be executable by owner, group, and others")

    try:
        tree = ast.parse(run_script.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, SyntaxError) as error:
        errors.append(f"tools/run.py is not valid Python: {error}")
        return

    imports: set[str] = set()
    strings: set[str] = set()
    subcommands: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            strings.add(node.value)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_parser"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            subcommands.add(node.args[0].value)

    allowed_imports = set(sys.stdlib_module_names) | {"__future__"}
    nonstandard_imports = sorted(imports - allowed_imports)
    if nonstandard_imports:
        errors.append(f"tools/run.py has non-stdlib imports: {nonstandard_imports}")
    if subcommands != {"new", "freeze", "check"}:
        errors.append(
            "tools/run.py subcommands must be exactly new/freeze/check: "
            f"{sorted(subcommands)}"
        )

    required_literals = {
        "new",
        "freeze",
        "check",
        "raw",
        "locked",
        "final",
        "acceptance",
        "production-freeze.json",
        "acceptance-freeze.json",
        "judge-predictions.md",
        "acceptance-report.md",
        "product-verdicts.md",
        "freeze-receipt.md",
        "final/freeze-receipt.md",
        "production=open",
        "Single-writer contract",
        "material missing / 材料丢失",
        "material changed / 材料被改",
    }
    missing_literals = sorted(
        literal
        for literal in required_literals
        if not any(literal in value for value in strings)
    )
    if missing_literals:
        errors.append(f"tools/run.py contract literals missing: {missing_literals}")


def validate_material_guard(
    errors: list[str], project_root: Path = ROOT
) -> None:
    materials = project_root / "materials"
    guard = materials / ".gitignore"
    if materials.is_symlink():
        errors.append("symlink forbidden: materials")
        return
    if guard.is_symlink():
        errors.append("symlink forbidden: materials/.gitignore")
        return
    if not guard.is_file():
        errors.append("materials/.gitignore missing")
        return
    try:
        text = guard.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        errors.append(f"materials/.gitignore is not readable UTF-8: {error}")
        return
    if text != EXPECTED_MATERIALS_GITIGNORE:
        errors.append("materials/.gitignore does not match the source-material guard")

    nested_guards = sorted(
        path
        for path in materials.rglob(".gitignore")
        if path != guard
    )
    for path in nested_guards:
        errors.append(
            "nested materials .gitignore forbidden: "
            f"{path.relative_to(project_root).as_posix()}"
        )


def _allowed_material_index_path(path: str) -> bool:
    reference = PurePosixPath(path)
    if not reference.parts or reference.parts[0] != "materials":
        return False
    if path == "materials/.gitignore":
        return True
    return reference.name in {".gitkeep", "authorization.md"}


def validate_material_index(
    errors: list[str], project_root: Path = ROOT
) -> None:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(project_root),
                "ls-files",
                "--cached",
                "-z",
                "--",
                "materials",
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        errors.append(f"cannot inspect Git index for materials: {error}")
        return
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        errors.append(f"cannot inspect Git index for materials: {detail}")
        return

    tracked = [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]
    forbidden = sorted(
        path for path in tracked if not _allowed_material_index_path(path)
    )
    for path in forbidden:
        errors.append(f"tracked/staged material forbidden: {path}")


def validate_t36_freeze_contract(errors: list[str]) -> None:
    taskcard = ROOT / "taskcards/T3.6.md"
    if not taskcard.is_file() or taskcard.is_symlink():
        return
    text = taskcard.read_text(encoding="utf-8")
    required_text = {
        "runs/T3.1/production-freeze.json",
        "runs/T3.1/acceptance/acceptance-freeze.json",
        "tools/run.py freeze runs/T3.1 --acceptance",
        "product-verdicts.md",
        "t3.1-freeze-receipt-sha256: <64 lowercase hex>",
        "单写者",
    }
    missing = sorted(item for item in required_text if item not in text)
    if missing:
        errors.append(f"T3.6 two-freeze contract text missing: {missing}")


def _run_materials_only(project_root: Path) -> int:
    errors: list[str] = []
    validate_material_guard(errors, project_root)
    validate_material_index(errors, project_root)
    if errors:
        print("materials validation FAILED")
        print("\n".join(errors))
        return 1
    print("materials validation PASSED")
    return 0


def main() -> int:
    if "--check-materials-root" in sys.argv:
        if len(sys.argv) != 3 or sys.argv[1] != "--check-materials-root":
            print(
                "usage: validate.py --check-materials-root <project-root>",
                file=sys.stderr,
            )
            return 2
        return _run_materials_only(Path(sys.argv[2]).resolve())

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

    for directory in REQUIRED_DIRECTORIES:
        path = ROOT / directory
        if path.is_symlink():
            errors.append(f"symlinked required directory: {directory}")
        elif not path.is_dir():
            errors.append(f"missing required directory: {directory}")

    for path in required_tree_symlinks():
        errors.append(f"symlink forbidden in required tree: {path.relative_to(ROOT)}")

    validate_run_script(errors)
    validate_material_guard(errors)
    validate_material_index(errors)
    validate_t36_freeze_contract(errors)

    expected_taskcards = {f"{task_id}.md" for task_id in TASK_IDS}
    taskcard_root = ROOT / "taskcards"
    observed_taskcards = (
        {
            path.name for path in taskcard_root.glob("T*.md")
        }
        if taskcard_root.is_dir() and not taskcard_root.is_symlink()
        else set()
    )
    allowed_nonformal_taskcards = {"TEMPLATE.md"}
    allowed_nonformal_taskcards.update(f"{task_id}-BLOCKER.md" for task_id in TASK_IDS)
    missing_taskcards = expected_taskcards - observed_taskcards
    unexpected_taskcards = observed_taskcards - expected_taskcards - allowed_nonformal_taskcards
    if missing_taskcards or unexpected_taskcards:
        errors.append(
            "taskcard set mismatch: "
            f"missing {sorted(missing_taskcards)}, unexpected {sorted(unexpected_taskcards)}"
        )
    taskcard_names = sorted(expected_taskcards) if not taskcard_root.is_symlink() else []
    for taskcard_name in taskcard_names:
        taskcard = taskcard_root / taskcard_name
        if not taskcard.is_file():
            continue
        if taskcard.is_symlink():
            errors.append(f"symlink forbidden: {taskcard.relative_to(ROOT)}")
            continue
        text = taskcard.read_text(encoding="utf-8")
        expected_sections = [
            f"## {index}. {heading}"
            for index, heading in enumerate(TASK_SECTION_NAMES, start=1)
        ]
        observed_sections = re.findall(r"^## .+$", text, flags=re.MULTILINE)
        if observed_sections != expected_sections:
            errors.append(
                f"taskcard sections must be exact, unique, and ordered: "
                f"{taskcard.relative_to(ROOT)}"
            )

    roadmap = ROOT / "blueprints/EXECUTION-ROADMAP.md"
    if not roadmap.is_file():
        errors.append("formal execution roadmap missing")
    elif roadmap.is_symlink():
        errors.append("symlink forbidden: blueprints/EXECUTION-ROADMAP.md")
    elif not roadmap.read_text(encoding="utf-8").startswith(
        "# ReaderLab 图书线重建执行路线图\n\n"
        "> 派生执行路线，不拥有产品决议，与 owner 文档冲突时停止并报告\n"
    ):
        errors.append("formal execution roadmap header mismatch")

    for path in stateful_files():
        if path.is_symlink():
            errors.append(f"symlink forbidden: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not STATE_HEADER.search(text):
            errors.append(f"missing status/scope header: {path.relative_to(ROOT)}")

    constrained_files = files + [MANIFEST]
    if taskcard_root.is_dir() and not taskcard_root.is_symlink():
        constrained_files.extend(taskcard_root.glob("*.md"))
    constrained_files.extend(stateful_files())
    for path in constrained_files:
        if not path.is_file():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        if path.is_symlink():
            errors.append(f"symlink forbidden: {path.relative_to(ROOT)}")
            continue
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
    cache_paths = sorted(
        path
        for path in all_paths
        if "__pycache__" in Path(path).parts or path.endswith((".pyc", ".pyo"))
    )
    if cache_paths:
        errors.append(f"Python cache artifacts found: {cache_paths}")

    if errors:
        print("clean seed validation FAILED")
        print("\n".join(errors))
        return 1

    print(
        "clean seed validation PASSED: "
        f"3 authority documents, 2 project entry documents, "
        f"{len(SUPPORT_DOCS)} derived support documents, {len(TASK_IDS)} taskcards, "
        f"{len(example_files)} readable example files, {len(RUNTIME_FILES)} runtime script, "
        f"{len(MATERIAL_GUARD_FILES)} material guard, "
        "0 legacy paths, 0 opaque assets, internal-only manifest."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
