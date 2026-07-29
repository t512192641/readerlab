#!/usr/bin/env python3
"""Dispatch the current ReaderLab Expert Teaching implementation explicitly."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
try:
    version = (SKILL_ROOT / "CURRENT_VERSION").read_text(encoding="utf-8").strip()
except (OSError, UnicodeError) as error:
    raise SystemExit(f"CURRENT_VERSION is unavailable: {error}") from error
if re.fullmatch(r"0\.1\.[0-9]+", version) is None:
    raise SystemExit(f"invalid CURRENT_VERSION: {version!r}")
target = SKILL_ROOT / "versions" / version / "scripts" / "run.py"
version_dir = target.parents[1]
if version_dir.is_symlink() or target.parent.is_symlink() or target.is_symlink() or not target.is_file():
    raise SystemExit(f"current Skill implementation is unavailable: {target}")
version_file = target.parent.parent / "VERSION"
try:
    target_version = version_file.read_text(encoding="utf-8").strip()
except (OSError, UnicodeError) as error:
    raise SystemExit(f"current Skill implementation version is unavailable: {error}") from error
if version_file.is_symlink() or not version_file.is_file() or target_version != version:
    raise SystemExit(f"current Skill implementation version mismatch: {target}")
os.execv(sys.executable, [sys.executable, os.fspath(target), *sys.argv[1:]])
