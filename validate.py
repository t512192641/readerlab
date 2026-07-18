#!/usr/bin/env python3
"""Validate the self-contained ReaderLab clean seed without reading legacy paths."""

from __future__ import annotations

import ast
import hashlib
import json
import os
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
T0_3_FILES = {
    "contracts/GLOSSARY.md",
    "taskcards/TEMPLATE.md",
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
TASK_SECTION_HEADINGS = tuple(
    f"## {index}. {heading}"
    for index, heading in enumerate(TASK_SECTION_NAMES, start=1)
)
TEMPLATE_REQUIRED_TEXT = (
    "taskcards/<任务编号>-BLOCKER.md",
    "首次写入后",
    "权限仅覆盖本节逐路径列出的交付文件",
    "具体 owner 章节或路线任务条目",
    "纯技术缺口",
    "主控技术门",
    "必须在汇报中对产品负责人可见",
    "涉及产品判断、材料授权、产品事实或决议冲突",
    "只能由产品负责人决定",
    "主控不得代答",
    "### 可机械检查",
    "### 主控核验",
    "`implemented`",
    "`integrated`",
    "`verified`",
    "`accepted`",
    "不得先做后报",
)
GLOSSARY_STATUS_HEADER = "---\nstatus: draft\nscope: long-term\n---\n"
GLOSSARY_CORE_HEADINGS = ("知识卡", "承重主张", "锚点")
GLOSSARY_REVIEW_STATES = ("锁定", "淘汰", "退回", "待补证据")
GLOSSARY_INCREMENT_HEADINGS = (
    "机制",
    "模型",
    "方法",
    "预测",
    "权衡",
    "可迁移关系",
    "高手指点",
    "跨行业视角",
)
GLOSSARY_EVIDENCE_HEADINGS = ("execution", "semantic", "product")
GLOSSARY_TANDEM_BOUNDARY = "- `tandem-comments` 的精确锚点格式：`unknown`。"
GLOSSARY_REQUIRED_TEXT = (
    "不拥有产品决议",
    "不固定未来 schema、字段、阈值、聚合、失败处理或锚点格式",
    "必须整体保留",
    "Writer 不选题、不添事实",
    "生产端不得读取 `GOLD-STANDARDS.md` 与 `examples/`",
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


def read_regular_bytes(
    path: Path, errors: list[str], project_root: Path
) -> bytes | None:
    label = path.relative_to(project_root).as_posix()
    if path.parent.is_symlink():
        errors.append(f"symlinked parent directory forbidden: {label}")
        return None
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        errors.append(f"missing or unreadable file: {label}: {error}")
        return None
    if stat.S_ISLNK(mode):
        errors.append(f"symlink forbidden: {label}")
        return None
    if not stat.S_ISREG(mode):
        errors.append(f"regular file required: {label}")
        return None

    descriptor = -1
    try:
        descriptor = os.open(
            path,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        )
        opened_mode = os.fstat(descriptor).st_mode
        if not stat.S_ISREG(opened_mode):
            errors.append(f"regular file required: {label}")
            return None
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = -1
            return handle.read()
    except OSError as error:
        errors.append(f"cannot read regular file: {label}: {error}")
        return None
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def read_regular_utf8(
    path: Path, errors: list[str], project_root: Path
) -> str | None:
    content = read_regular_bytes(path, errors, project_root)
    if content is None:
        return None
    try:
        return content.decode("utf-8")
    except UnicodeError as error:
        label = path.relative_to(project_root).as_posix()
        errors.append(f"file is not valid UTF-8: {label}: {error}")
        return None


def has_exact_taskcard_sections(text: str) -> bool:
    return (
        re.findall(r"^## .+$", text, flags=re.MULTILINE)
        == list(TASK_SECTION_HEADINGS)
    )


def owned_files() -> list[Path]:
    return sorted(
        [ROOT / name for name in TOP_DOCS]
        + [ROOT / name for name in SUPPORT_DOCS]
        + [ROOT / name for name in T0_3_FILES]
        + [ROOT / name for name in RUNTIME_FILES]
        + [ROOT / name for name in MATERIAL_GUARD_FILES]
        + list((ROOT / "examples").rglob("*.md")),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def build_manifest(errors: list[str]) -> dict[str, object] | None:
    files = owned_files()
    entries: list[dict[str, str]] = []
    for path in files:
        content = read_regular_bytes(path, errors, ROOT)
        if content is None:
            continue
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    if errors:
        return None
    return {
        "schema": "readerlab-clean-seed-manifest/v1",
        "purpose": "只验证当前候选包内部文件；不读取、不引用、不依赖任何旧项目目录。",
        "files": entries,
    }


def validate_manifest_parent(errors: list[str]) -> None:
    parent = MANIFEST.parent
    label = parent.relative_to(ROOT).as_posix()
    try:
        mode = parent.lstat().st_mode
    except OSError as error:
        errors.append(
            f"missing or unreadable manifest parent directory: {label}: {error}"
        )
        return
    if stat.S_ISLNK(mode):
        errors.append(f"symlinked manifest parent directory forbidden: {label}")
    elif not stat.S_ISDIR(mode):
        errors.append(f"manifest parent must be a directory: {label}")


def write_manifest_atomically(text: str) -> None:
    temporary_name = f".{MANIFEST.name}.tmp"
    parent_descriptor = -1
    descriptor = -1
    created = False
    try:
        parent_descriptor = os.open(
            MANIFEST.parent,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0),
        )
        descriptor = os.open(
            temporary_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o644,
            dir_fd=parent_descriptor,
        )
        created = True
        with os.fdopen(
            descriptor, "w", encoding="utf-8", newline="\n"
        ) as handle:
            descriptor = -1
            handle.write(text)
        os.replace(
            temporary_name,
            MANIFEST.name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        created = False
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if created and parent_descriptor >= 0:
            try:
                os.unlink(temporary_name, dir_fd=parent_descriptor)
            except FileNotFoundError:
                pass
        if parent_descriptor >= 0:
            os.close(parent_descriptor)


def validate_forbidden_text(
    path: Path, text: str, errors: list[str]
) -> None:
    label = path.relative_to(ROOT)
    for forbidden in FORBIDDEN_TEXT:
        if forbidden in text:
            errors.append(f"legacy reference {forbidden!r} in {label}")


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


def validate_t0_3_contracts(
    errors: list[str], project_root: Path = ROOT
) -> None:
    template = project_root / "taskcards/TEMPLATE.md"
    template_text = read_regular_utf8(template, errors, project_root)
    if template_text is not None:
        if not has_exact_taskcard_sections(template_text):
            errors.append(
                "taskcard template sections must be exact, unique, and ordered"
            )
        missing_template_text = sorted(
            text for text in TEMPLATE_REQUIRED_TEXT if text not in template_text
        )
        if missing_template_text:
            errors.append(
                "taskcard template contract text missing: "
                f"{missing_template_text}"
            )

    glossary = project_root / "contracts/GLOSSARY.md"
    glossary_text = read_regular_utf8(glossary, errors, project_root)
    if glossary_text is None:
        return
    if not glossary_text.startswith(GLOSSARY_STATUS_HEADER):
        errors.append("contracts/GLOSSARY.md must have draft/long-term status header")

    for heading in GLOSSARY_CORE_HEADINGS:
        if glossary_text.count(f"## {heading}\n") != 1:
            errors.append(
                f"contracts/GLOSSARY.md must define {heading!r} exactly once"
            )
    for state_name in GLOSSARY_REVIEW_STATES:
        state_pattern = rf"^- \*\*{re.escape(state_name)}\*\*：.+$"
        if len(re.findall(state_pattern, glossary_text, flags=re.MULTILINE)) != 1:
            errors.append(
                "contracts/GLOSSARY.md must define review state "
                f"{state_name!r} exactly once"
            )
    for heading in GLOSSARY_INCREMENT_HEADINGS:
        if glossary_text.count(f"### {heading}\n") != 1:
            errors.append(
                "contracts/GLOSSARY.md must define increment type "
                f"{heading!r} exactly once"
            )
    for heading in GLOSSARY_EVIDENCE_HEADINGS:
        if glossary_text.count(f"### {heading}\n") != 1:
            errors.append(
                "contracts/GLOSSARY.md must distinguish evidence layer "
                f"{heading!r} exactly once"
            )

    tandem_lines = [
        line for line in glossary_text.splitlines() if "tandem-comments" in line
    ]
    if tandem_lines != [GLOSSARY_TANDEM_BOUNDARY]:
        errors.append(
            "contracts/GLOSSARY.md must keep the exact tandem-comments "
            "anchor format unknown"
        )
    missing_glossary_text = sorted(
        text for text in GLOSSARY_REQUIRED_TEXT if text not in glossary_text
    )
    if missing_glossary_text:
        errors.append(
            "contracts/GLOSSARY.md boundary text missing: "
            f"{missing_glossary_text}"
        )


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


def _run_t0_3_only(project_root: Path) -> int:
    errors: list[str] = []
    validate_t0_3_contracts(errors, project_root)
    if errors:
        print("T0.3 validation FAILED")
        print("\n".join(errors))
        return 1
    print("T0.3 validation PASSED")
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

    if "--check-t0-3-root" in sys.argv:
        if len(sys.argv) != 3 or sys.argv[1] != "--check-t0-3-root":
            print(
                "usage: validate.py --check-t0-3-root <project-root>",
                file=sys.stderr,
            )
            return 2
        return _run_t0_3_only(Path(sys.argv[2]).resolve())

    write_manifest = "--write-manifest" in sys.argv
    errors: list[str] = []
    validate_t0_3_contracts(errors)
    validate_manifest_parent(errors)
    if errors:
        print("clean seed validation FAILED")
        print("\n".join(errors))
        return 1

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
        if not has_exact_taskcard_sections(text):
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

    constrained_files = set(files)
    if taskcard_root.is_dir() and not taskcard_root.is_symlink():
        constrained_files.update(taskcard_root.glob("*.md"))
    constrained_files.update(stateful_files())
    for path in sorted(
        constrained_files,
        key=lambda item: item.relative_to(ROOT).as_posix(),
    ):
        if not path.is_file():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        if path.is_symlink():
            errors.append(f"symlink forbidden: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        validate_forbidden_text(path, text, errors)

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

    if not write_manifest:
        manifest_text = read_regular_utf8(MANIFEST, errors, ROOT)
        manifest: object | None = None
        if manifest_text is not None:
            try:
                manifest = json.loads(manifest_text)
            except json.JSONDecodeError as error:
                errors.append(f"audit/manifest.json is not valid JSON: {error}")
            manifest_errors: list[str] = []
            expected_manifest = build_manifest(manifest_errors)
            errors.extend(manifest_errors)
            if expected_manifest is not None and manifest != expected_manifest:
                errors.append("internal manifest does not match current clean-seed files")
            validate_forbidden_text(MANIFEST, manifest_text, errors)

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

    manifest_text_to_write: str | None = None
    if write_manifest and not errors:
        manifest_errors: list[str] = []
        manifest = build_manifest(manifest_errors)
        errors.extend(manifest_errors)
        if manifest is not None:
            manifest_text_to_write = (
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
            )
            validate_forbidden_text(MANIFEST, manifest_text_to_write, errors)

    if errors:
        print("clean seed validation FAILED")
        print("\n".join(errors))
        return 1

    if manifest_text_to_write is not None:
        try:
            write_manifest_atomically(manifest_text_to_write)
        except OSError as error:
            print("clean seed validation FAILED")
            print(f"cannot write audit/manifest.json atomically: {error}")
            return 1

    print(
        "clean seed validation PASSED: "
        f"3 authority documents, 2 project entry documents, "
        f"{len(SUPPORT_DOCS)} derived support documents, {len(TASK_IDS)} taskcards, "
        f"{len(T0_3_FILES)} T0.3 contract documents, "
        f"{len(example_files)} readable example files, {len(RUNTIME_FILES)} runtime script, "
        f"{len(MATERIAL_GUARD_FILES)} material guard, "
        "0 legacy paths, 0 opaque assets, internal-only manifest."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
