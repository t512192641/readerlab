#!/usr/bin/env python3
"""Install and discovery smoke for a built ReaderLab shareable package."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


SKILL_NAME = "readerlab"
GLOBAL_CODEX_SKILLS = (Path.home() / ".codex" / "skills").resolve()


class SmokeFailure(Exception):
    def __init__(self, phase: str, message: str) -> None:
        super().__init__(message)
        self.phase = phase
        self.message = message


def require_clean_install_root(path: Path, *, allow_global_codex_skills: bool) -> Path:
    resolved = path.resolve()
    if not allow_global_codex_skills and (resolved == GLOBAL_CODEX_SKILLS or GLOBAL_CODEX_SKILLS in resolved.parents):
        raise SmokeFailure(
            "install",
            "refusing to write to the global Codex Skill directory; use a clean temporary install root",
        )
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def read_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise SmokeFailure("discovery", "SKILL.md is missing YAML front matter")
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    raise SmokeFailure("discovery", "SKILL.md front matter is not closed")


def run_command(command: list[str], *, cwd: Path, phase: str) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SmokeFailure(
            phase,
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stderr or result.stdout}",
        )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_first_line": result.stdout.splitlines()[0] if result.stdout.splitlines() else "",
    }


def install_package(
    package_root: Path,
    install_root: Path,
    *,
    force: bool,
    allow_global_codex_skills: bool,
) -> Path:
    package_root = package_root.resolve()
    if not (package_root / "SKILL.md").is_file():
        raise SmokeFailure("install", f"package root does not contain SKILL.md: {package_root}")
    install_root = require_clean_install_root(install_root, allow_global_codex_skills=allow_global_codex_skills)
    target = install_root / SKILL_NAME
    if target.exists():
        if not force:
            raise SmokeFailure("install", f"install target exists; pass --force to replace: {target}")
        if install_root.resolve() not in target.resolve().parents:
            raise SmokeFailure("install", f"refusing to replace target outside install root: {target}")
        shutil.rmtree(target)
    shutil.copytree(package_root, target)
    return target


def discover_skill(install_root: Path) -> dict[str, Any]:
    skill_file = install_root / SKILL_NAME / "SKILL.md"
    if not skill_file.is_file():
        raise SmokeFailure("discovery", f"installed skill entry not found: {skill_file}")
    frontmatter = read_frontmatter(skill_file)
    if frontmatter.get("name") != SKILL_NAME:
        raise SmokeFailure("discovery", f"expected skill name {SKILL_NAME!r}, got {frontmatter.get('name')!r}")
    description = frontmatter.get("description", "")
    if len(description) < 40:
        raise SmokeFailure("discovery", "SKILL.md description is missing or too short to be readable")
    return {
        "name": frontmatter["name"],
        "description_present": True,
        "entry": f"{SKILL_NAME}/SKILL.md",
    }


def run_smoke(
    package_root: Path,
    install_root: Path,
    *,
    force: bool,
    allow_global_codex_skills: bool = False,
) -> dict[str, Any]:
    installed_root = install_package(
        package_root,
        install_root,
        force=force,
        allow_global_codex_skills=allow_global_codex_skills,
    )
    discovery = discover_skill(install_root.resolve())
    package_smoke = run_command(["python3", "tests/package_smoke_test.py"], cwd=installed_root, phase="command")
    config_smoke = run_command(
        [
            "python3",
            "scripts/readerlab.py",
            "validate-run-config",
            "examples/run-config-example.json",
            "--no-source-exists-check",
        ],
        cwd=installed_root,
        phase="config",
    )
    return {
        "schema": "readerlab.install-smoke.v1",
        "status": "pass",
        "check_class": "install_discovery_smoke",
        "not_reader_acceptance": True,
        "not_production_ready": True,
        "installed_skill_root": installed_root.relative_to(install_root.resolve()).as_posix(),
        "discovery": discovery,
        "commands": {
            "package_smoke": package_smoke,
            "runtime_config": config_smoke,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="readerlab-install-smoke")
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--install-root", required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--allow-global-codex-skills",
        action="store_true",
        help="Allow writing under ~/.codex/skills after explicit user approval.",
    )
    args = parser.parse_args()

    try:
        result = run_smoke(
            Path(args.package_root),
            Path(args.install_root),
            force=args.force,
            allow_global_codex_skills=args.allow_global_codex_skills,
        )
    except SmokeFailure as exc:
        print(
            json.dumps(
                {
                    "schema": "readerlab.install-smoke.v1",
                    "status": "fail",
                    "failed_phase": exc.phase,
                    "message": exc.message,
                    "not_reader_acceptance": True,
                    "not_production_ready": True,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
