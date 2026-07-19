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
import tempfile
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
RECOVERY_TASK_IDS = (
    "T2.2-R01",
    "T2.2-R02",
    "T2.2-R03",
    "T2.2-R04",
    "T2.2-R05",
    "T2.2-R06",
    "T2.2-R07",
    "T2.2-R08",
    "T2.2-R09",
    "T2.2-R10",
    "T2.2-R11",
    "T2.2-R12",
    "T2.2-R13",
    "T2.2-R14",
    "T2.2-R15",
    "T2.2-R16",
    "T2.2-R17",
    "T2.2-R18",
    "T2.2-R19",
    "T2.2-R20",
    "T2.2-R21",
)
RECOVERY_COMPOSITE_TASK_IDS = {
    "T2.2-R09",
    "T2.2-R14",
    "T2.2-R19",
}
RECOVERY_ARCHITECTURE_IDENTITIES = {
    "active-architecture": (
        "diagnostics/T2.2-recovery-architecture-v3.md",
        "a67f011d112e1e06022867cb3577110816064bd9",
        "38025c0b2ebb26171e7f6ad8bef69b97bfeb2d88597a78e67b3dcdc48110d1e1",
    ),
    "active-architecture-review": (
        "diagnostics/T2.2-recovery-architecture-v3-preflight-review.md",
        "626562fa3fa6487200e953ca0b804a275ec3ef33",
        "e5d450f019685fba6eed679e06ccedee10255591e9a4a65359ac6cfb918e06ec",
    ),
    "quality-audit": (
        "diagnostics/T2.2-recovery-architecture-v3-preflight-review-quality-audit.md",
        "e74221b85a8c750827c534e14d6df4079cb85c06",
        "a81ded57546981d40b7c95d0d206ca0b627008fe509c32dfff1fb09abb415342",
    ),
}
RECOVERY_MATERIAL_SLOTS = (
    "materials/T2.2-v2/source-01-full.md",
    "materials/T2.2-v2/source-02-full.md",
    "materials/T2.2-v2/source-03-full.md",
    "materials/T2.2-v2/source-04-full.md",
    "materials/T2.2-v2/source-05-full.md",
    "materials/T2.2-v2/source-06-full.md",
    "materials/T2.2-v2/source-07-full.md",
    "materials/T2.2-v2/source-08-full.md",
    "materials/T2.2-v2/source-09-full.md",
    "materials/T2.2-v2/source-10-full.md",
    "materials/T2.2-v2/source-11-full.md",
    "materials/T2.2-v2/source-12-full.md",
    "materials/T2.2-v2/source-13-full.md",
    "materials/T2.2-v2/source-14-full.md",
)
RECOVERY_RAW_BLOBS = (
    "diagnostics/T2.2-fixture-bytes-v2/candidate-01.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-01.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-02.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-02.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-03.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-03.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-04.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-04.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-05.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-05.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-06.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-06.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-07.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-07.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-08.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-08.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-09.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-09.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-10.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-10.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-11.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-11.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-12.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-12.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-13.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-13.bin",
    "diagnostics/T2.2-fixture-bytes-v2/candidate-14.bin",
    "diagnostics/T2.2-fixture-bytes-v2/context-14.bin",
)


def _artifact_policy(
    owner: str,
    status: str,
    scope: str,
    direct_review_path: str = "none",
    m2_active: str = "no",
    attempt_local: str = "yes",
    header_required: str = "yes",
) -> dict[str, str]:
    return {
        "owner": owner,
        "header-required": header_required,
        "status": status,
        "scope": scope,
        "direct-review-path": direct_review_path,
        "review-scope-inherits": (
            "yes" if direct_review_path != "none" else "not-applicable"
        ),
        "m2-active": m2_active,
        "attempt-local": attempt_local,
    }


RECOVERY_ARTIFACT_POLICY = {
    "contracts/T2.2-historical-qualification-adapter-v1.md": _artifact_policy(
        "T2.2-R01",
        "frozen",
        "long-term",
        "diagnostics/T2.2-historical-qualification-adapter-v1-review.md",
        "indirect",
        "no",
    ),
    "diagnostics/T2.2-fixture-census-v2.md": _artifact_policy(
        "T2.2-R01",
        "frozen",
        "run-only",
        "diagnostics/T2.2-fixture-census-review-v2.md",
    ),
    "diagnostics/T2.2-fixture-gap-list-v2.md": _artifact_policy(
        "T2.2-R01",
        "frozen",
        "run-only",
        "diagnostics/T2.2-fixture-census-review-v2.md",
    ),
    "diagnostics/T2.2-historical-qualification-adapter-v1-review.md": _artifact_policy(
        "T2.2-R02", "frozen", "long-term", m2_active="indirect", attempt_local="no"
    ),
    "diagnostics/T2.2-fixture-census-review-v2.md": _artifact_policy(
        "T2.2-R02", "frozen", "run-only"
    ),
    "materials/T2.2-v2/authorization.md": _artifact_policy(
        "T2.2-R03/product",
        "frozen",
        "run-only",
        "diagnostics/T2.2-fixture-byte-review-v2.md",
    ),
    "diagnostics/T2.2-material-gap-manifest-v2.md": _artifact_policy(
        "T2.2-R03",
        "frozen",
        "run-only",
        "diagnostics/T2.2-fixture-byte-review-v2.md",
    ),
    "diagnostics/T2.2-fixture-resolution-v2.md": _artifact_policy(
        "T2.2-R03",
        "frozen",
        "run-only",
        "diagnostics/T2.2-fixture-byte-review-v2.md",
    ),
    "diagnostics/T2.2-fixture-admission-v2.md": _artifact_policy(
        "T2.2-R03",
        "frozen",
        "run-only",
        "diagnostics/T2.2-fixture-byte-review-v2.md",
    ),
    "diagnostics/T2.2-fixture-byte-manifest-v2.md": _artifact_policy(
        "T2.2-R03",
        "frozen",
        "run-only",
        "diagnostics/T2.2-fixture-byte-review-v2.md",
    ),
    "diagnostics/T2.2-fixture-byte-review-v2.md": _artifact_policy(
        "T2.2-R04", "frozen", "run-only"
    ),
    "diagnostics/T2.2-qualification-attempt-manifest-v2.md": _artifact_policy(
        "T2.2-R05",
        "frozen",
        "run-only",
        "diagnostics/T2.2-package-preflight-review-v2.md",
        "yes",
    ),
    "diagnostics/T2.2-blind-packet-v2.md": _artifact_policy(
        "T2.2-R05",
        "frozen",
        "run-only",
        "diagnostics/T2.2-package-preflight-review-v2.md",
        "indirect",
    ),
    "diagnostics/T2.2-scoring-key-v2.md": _artifact_policy(
        "T2.2-R05",
        "frozen",
        "run-only",
        "diagnostics/T2.2-package-preflight-review-v2.md",
        "indirect",
    ),
    "diagnostics/T2.2-judge-brief-v2.md": _artifact_policy(
        "T2.2-R05",
        "frozen",
        "run-only",
        "diagnostics/T2.2-package-preflight-review-v2.md",
        "indirect",
    ),
    "diagnostics/T2.2-judge-brief-variant-v1-02.md": _artifact_policy(
        "T2.2-R05",
        "frozen",
        "run-only",
        "diagnostics/T2.2-package-preflight-review-v2.md",
        "indirect",
    ),
    "diagnostics/T2.2-contrast-key-v1.md": _artifact_policy(
        "T2.2-R05",
        "frozen",
        "run-only",
        "diagnostics/T2.2-package-preflight-review-v2.md",
        "indirect",
    ),
    "diagnostics/T2.2-contrast-packet-v1-01.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-contrast-packet-v1-02.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-contrast-packet-v1-03.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-contrast-packet-v1-04.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-contrast-packet-v1-05.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-contrast-packet-v1-06.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-01.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-02.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-03.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-04.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-05.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-06.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-07.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-08.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-09.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-10.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-11.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-12.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-13.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-retest-packet-v2-14.md": _artifact_policy(
        "T2.2-R05", "frozen", "run-only", "diagnostics/T2.2-package-preflight-review-v2.md", "indirect"
    ),
    "diagnostics/T2.2-package-manifest-v2.md": _artifact_policy(
        "T2.2-R05",
        "frozen",
        "run-only",
        "diagnostics/T2.2-package-preflight-review-v2.md",
        "indirect",
    ),
    "diagnostics/T2.2-package-preflight-review-v2.md": _artifact_policy(
        "T2.2-R06", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-contrast-control-call-manifest-v1.md": _artifact_policy(
        "T2.2-R07",
        "frozen",
        "run-only",
        "diagnostics/T2.2-contrast-control-input-review-v1.md",
    ),
    "diagnostics/T2.2-contrast-control-input-review-v1.md": _artifact_policy(
        "T2.2-R08", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-01.md": _artifact_policy(
        "T2.2-R09 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-02.md": _artifact_policy(
        "T2.2-R09 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-03.md": _artifact_policy(
        "T2.2-R09 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-04.md": _artifact_policy(
        "T2.2-R09 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-control-answers-index-v1.md": _artifact_policy(
        "T2.2-R09 controller", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-control-results-v1.md": _artifact_policy(
        "T2.2-R10",
        "frozen",
        "run-only",
        "diagnostics/T2.2-contrast-control-postflight-review-v1.md",
    ),
    "diagnostics/T2.2-contrast-control-postflight-review-v1.md": _artifact_policy(
        "T2.2-R11", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-diagnostic-call-manifest-v1.md": _artifact_policy(
        "T2.2-R12",
        "frozen",
        "run-only",
        "diagnostics/T2.2-contrast-diagnostic-input-review-v1.md",
    ),
    "diagnostics/T2.2-contrast-diagnostic-input-review-v1.md": _artifact_policy(
        "T2.2-R13", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-05.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-06.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-07.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-08.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-09.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-10.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-11.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-12.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-13.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-answer-v1-14.md": _artifact_policy(
        "T2.2-R14 fresh judge", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-diagnostic-answers-index-v1.md": _artifact_policy(
        "T2.2-R14 controller", "frozen", "run-only"
    ),
    "diagnostics/T2.2-contrast-results-v1.md": _artifact_policy(
        "T2.2-R15",
        "frozen",
        "run-only",
        "diagnostics/T2.2-contrast-postflight-review-v1.md",
    ),
    "diagnostics/T2.2-contrast-postflight-review-v1.md": _artifact_policy(
        "T2.2-R16", "frozen", "run-only"
    ),
    "diagnostics/T2.2-retest-call-manifest-v2.md": _artifact_policy(
        "T2.2-R17",
        "frozen",
        "run-only",
        "diagnostics/T2.2-retest-input-review-v2.md",
    ),
    "diagnostics/T2.2-retest-input-review-v2.md": _artifact_policy(
        "T2.2-R18", "frozen", "run-only"
    ),
    "diagnostics/T2.2-judge-answer-v2-01.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-02.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-03.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-04.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-05.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-06.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-07.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-08.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-09.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-10.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-11.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-12.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-13.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answer-v2-14.md": _artifact_policy(
        "T2.2-R19 fresh judge", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-answers-index-v2.md": _artifact_policy(
        "T2.2-R19 controller", "frozen", "run-only", m2_active="indirect"
    ),
    "diagnostics/T2.2-judge-baseline-v2.md": _artifact_policy(
        "T2.2-R20",
        "frozen",
        "long-term",
        "diagnostics/T2.2-postflight-review-v2.md",
        "yes",
        "no",
    ),
    "diagnostics/T2.2-postflight-review-v2.md": _artifact_policy(
        "T2.2-R21", "frozen", "long-term", m2_active="yes", attempt_local="no"
    ),
}
RECOVERY_BLOCKER_ARTIFACT_POLICY = {
    "taskcards/T2.2-R01-BLOCKER.md": _artifact_policy(
        "T2.2-R01", "blocked", "run-only"
    ),
    "taskcards/T2.2-R02-BLOCKER.md": _artifact_policy(
        "T2.2-R02", "blocked", "run-only"
    ),
    "taskcards/T2.2-R03-BLOCKER.md": _artifact_policy(
        "T2.2-R03", "blocked", "run-only"
    ),
    "taskcards/T2.2-R04-BLOCKER.md": _artifact_policy(
        "T2.2-R04", "blocked", "run-only"
    ),
    "taskcards/T2.2-R05-BLOCKER.md": _artifact_policy(
        "T2.2-R05", "blocked", "run-only"
    ),
    "taskcards/T2.2-R06-BLOCKER.md": _artifact_policy(
        "T2.2-R06", "blocked", "run-only"
    ),
    "taskcards/T2.2-R07-BLOCKER.md": _artifact_policy(
        "T2.2-R07", "blocked", "run-only"
    ),
    "taskcards/T2.2-R08-BLOCKER.md": _artifact_policy(
        "T2.2-R08", "blocked", "run-only"
    ),
    "taskcards/T2.2-R09-BLOCKER.md": _artifact_policy(
        "T2.2-R09", "blocked", "run-only"
    ),
    "taskcards/T2.2-R10-BLOCKER.md": _artifact_policy(
        "T2.2-R10", "blocked", "run-only"
    ),
    "taskcards/T2.2-R11-BLOCKER.md": _artifact_policy(
        "T2.2-R11", "blocked", "run-only"
    ),
    "taskcards/T2.2-R12-BLOCKER.md": _artifact_policy(
        "T2.2-R12", "blocked", "run-only"
    ),
    "taskcards/T2.2-R13-BLOCKER.md": _artifact_policy(
        "T2.2-R13", "blocked", "run-only"
    ),
    "taskcards/T2.2-R14-BLOCKER.md": _artifact_policy(
        "T2.2-R14", "blocked", "run-only"
    ),
    "taskcards/T2.2-R15-BLOCKER.md": _artifact_policy(
        "T2.2-R15", "blocked", "run-only"
    ),
    "taskcards/T2.2-R16-BLOCKER.md": _artifact_policy(
        "T2.2-R16", "blocked", "run-only"
    ),
    "taskcards/T2.2-R17-BLOCKER.md": _artifact_policy(
        "T2.2-R17", "blocked", "run-only"
    ),
    "taskcards/T2.2-R18-BLOCKER.md": _artifact_policy(
        "T2.2-R18", "blocked", "run-only"
    ),
    "taskcards/T2.2-R19-BLOCKER.md": _artifact_policy(
        "T2.2-R19", "blocked", "run-only"
    ),
    "taskcards/T2.2-R20-BLOCKER.md": _artifact_policy(
        "T2.2-R20", "blocked", "run-only"
    ),
    "taskcards/T2.2-R21-BLOCKER.md": _artifact_policy(
        "T2.2-R21", "blocked", "run-only"
    ),
}
RECOVERY_CONTROL_ARTIFACT_POLICY = {
    "diagnostics/T2.2-recovery-architecture-v3-preflight-review.md": (
        _artifact_policy(
            "independent-architecture-review",
            "frozen",
            "run-only",
            m2_active="indirect",
            attempt_local="no",
        )
    ),
    "diagnostics/M2-gate-receipt.md": _artifact_policy(
        "M2-controller",
        "frozen",
        "long-term",
        m2_active="yes",
        attempt_local="no",
    ),
}

RECOVERY_REVIEW_SUBJECTS = {
    "diagnostics/T2.2-recovery-architecture-v3-preflight-review.md": (
        "diagnostics/T2.2-recovery-architecture-v3.md",
    ),
    "diagnostics/T2.2-historical-qualification-adapter-v1-review.md": (
        "contracts/T2.2-historical-qualification-adapter-v1.md",
    ),
    "diagnostics/T2.2-fixture-census-review-v2.md": (
        "diagnostics/T2.2-fixture-census-v2.md",
        "diagnostics/T2.2-fixture-gap-list-v2.md",
    ),
    "diagnostics/T2.2-fixture-byte-review-v2.md": (
        "materials/T2.2-v2/authorization.md",
        "diagnostics/T2.2-material-gap-manifest-v2.md",
        "diagnostics/T2.2-fixture-resolution-v2.md",
        "diagnostics/T2.2-fixture-admission-v2.md",
        "diagnostics/T2.2-fixture-byte-manifest-v2.md",
        *RECOVERY_RAW_BLOBS,
    ),
    "diagnostics/T2.2-package-preflight-review-v2.md": tuple(
        path
        for path, policy in RECOVERY_ARTIFACT_POLICY.items()
        if policy["owner"] == "T2.2-R05"
    ),
    "diagnostics/T2.2-contrast-control-input-review-v1.md": (
        "diagnostics/T2.2-contrast-control-call-manifest-v1.md",
    ),
    "diagnostics/T2.2-contrast-control-postflight-review-v1.md": (
        "diagnostics/T2.2-contrast-control-results-v1.md",
    ),
    "diagnostics/T2.2-contrast-diagnostic-input-review-v1.md": (
        "diagnostics/T2.2-contrast-diagnostic-call-manifest-v1.md",
    ),
    "diagnostics/T2.2-contrast-postflight-review-v1.md": (
        "diagnostics/T2.2-contrast-results-v1.md",
    ),
    "diagnostics/T2.2-retest-input-review-v2.md": (
        "diagnostics/T2.2-retest-call-manifest-v2.md",
    ),
    "diagnostics/T2.2-postflight-review-v2.md": (
        "diagnostics/T2.2-judge-baseline-v2.md",
    ),
}
RECOVERY_HISTORICAL_MARKDOWN = {
    "diagnostics/T2.2-blind-packet.md",
    "diagnostics/T2.2-scoring-key.md",
    "diagnostics/T2.2-judge-brief.md",
    "diagnostics/T2.2-judge-answers.md",
    "diagnostics/T2.2-judge-baseline.md",
    "diagnostics/T2.2-recovery-architecture-v1.md",
    "diagnostics/T2.2-recovery-architecture-v1-preflight-review.md",
    "diagnostics/T2.2-recovery-architecture-v2.md",
    "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md",
    "diagnostics/T2.2-recovery-architecture-v3.md",
    "diagnostics/T2.2-recovery-architecture-v3-preflight-review.md",
    "diagnostics/T2.2-recovery-architecture-v3-preflight-review-quality-audit.md",
}
RECOVERY_SELECTOR_PATH = "diagnostics/T2.2-material-gap-manifest-v2.md"
M2_RECEIPT_PATH = "diagnostics/M2-gate-receipt.md"
RECOVERY_R01_BLOCKER_PATH = "taskcards/T2.2-R01-BLOCKER.md"
M2_RECEIPT_REQUIRED_KEYS = (
    "m1-freeze-receipt-sha256",
    "t1.8-independent-acceptance-sha256",
    "t2.1-r01-r08-sha256",
    "t2.3-seed-lenses-v2-sha256",
    "t2.2-active-architecture-path",
    "t2.2-active-architecture-sha256",
    "t2.2-active-architecture-review-path",
    "t2.2-active-architecture-review-sha256",
    "t2.2-active-attempt-id",
    "t2.2-active-attempt-manifest-path",
    "t2.2-active-attempt-manifest-sha256",
    "t2.2-active-baseline-path",
    "t2.2-active-baseline-sha256",
    "t2.2-active-postflight-review-path",
    "t2.2-active-postflight-review-sha256",
    "t2.2-active-result",
    "t2.2-history-v1-baseline-path",
    "t2.2-history-v1-baseline-sha256",
    "t2.2-history-v1-baseline-result",
    "t2.2-history-v1-blocker-path",
    "t2.2-history-v1-blocker-sha256",
    "t2.2-history-v2-architecture-path",
    "t2.2-history-v2-architecture-sha256",
    "t2.2-history-v2-review-path",
    "t2.2-history-v2-review-sha256",
    "t2.2-history-v2-review-result",
)
RECOVERY_SOURCE_PATHS = (
    "examples/book/positive/automatic-driving-safe-state.md",
    "examples/book/positive/civilization-lifecycle.md",
    "examples/book/positive/demand-pooling.md",
    "examples/book/negative/fresh-demo-five-rejected.md",
    "examples/book/negative/harari-chapter01-rejected.md",
    "examples/book/negative/innovation-failure-rejected.md",
    "examples/book/negative/lens-core-e1-rejected.md",
    "examples/book/negative/lens-core-e2-rejected.md",
    "examples/book/negative/lens-core-e3-rejected.md",
    "examples/book/negative/phase4-centralized-rejected.md",
    "examples/book/negative/phase4-nearby-rejected.md",
    "examples/book/reference/book-kernel-h3-borderline.md",
    "examples/book/reference/premortem-non-gold.md",
    "examples/book/reference/r01-r08-borderline.md",
)
RECOVERY_PACKAGE_MANIFEST_PATH = "diagnostics/T2.2-package-manifest-v2.md"
RECOVERY_ATTEMPT_MANIFEST_PATH = (
    "diagnostics/T2.2-qualification-attempt-manifest-v2.md"
)
RECOVERY_PACKAGE_MEMBER_PATHS = tuple(
    path
    for path, policy in RECOVERY_ARTIFACT_POLICY.items()
    if policy["owner"] == "T2.2-R05"
    and path
    not in {
        RECOVERY_ATTEMPT_MANIFEST_PATH,
        RECOVERY_PACKAGE_MANIFEST_PATH,
    }
)
RECOVERY_PACKET_PATHS = (
    "diagnostics/T2.2-blind-packet-v2.md",
    *tuple(
        f"diagnostics/T2.2-contrast-packet-v1-{index:02d}.md"
        for index in range(1, 7)
    ),
    *tuple(
        f"diagnostics/T2.2-retest-packet-v2-{index:02d}.md"
        for index in range(1, 15)
    ),
)
RECOVERY_ATTEMPT_FUTURE_PATHS = (
    *RECOVERY_PACKAGE_MEMBER_PATHS,
    RECOVERY_PACKAGE_MANIFEST_PATH,
    *tuple(
        path
        for path, policy in RECOVERY_ARTIFACT_POLICY.items()
        if policy["owner"].split()[0].split("/")[0]
        in {f"T2.2-R{index:02d}" for index in range(6, 22)}
    ),
    M2_RECEIPT_PATH,
)
RECOVERY_M14_CALLS = (
    ("01", "C", "01", "full", "P-r1"),
    ("02", "C", "01", "full", "P-r2"),
    ("03", "C", "02", "full", "N1-r1"),
    ("04", "C", "02", "full", "N1-r2"),
    ("05", "B", "01", "variant", "P-r1"),
    ("06", "B", "01", "variant", "P-r2"),
    ("07", "B", "02", "variant", "N1-r1"),
    ("08", "B", "02", "variant", "N1-r2"),
    ("09", "E", "03", "full", "P-r1"),
    ("10", "E", "03", "full", "P-r2"),
    ("11", "E", "04", "full", "N1-r1"),
    ("12", "E", "04", "full", "N1-r2"),
    ("13", "G", "05", "full", "P,N1"),
    ("14", "G", "06", "full", "N1,P"),
)
RECOVERY_FIXED_START_PATHS = (
    "contracts/M1-freeze-receipt.md",
    "contracts/T1.8-independent-acceptance.md",
    "diagnostics/T2.2-blind-packet.md",
    "diagnostics/T2.2-scoring-key.md",
    "diagnostics/T2.2-judge-brief.md",
    "diagnostics/T2.2-judge-answers.md",
    "diagnostics/T2.2-judge-baseline.md",
    "taskcards/T2.2-BLOCKER.md",
)
RECOVERY_CARD_COMMON_READ_PATHS = (
    "AGENTS.md",
    "PRODUCT-DECISIONS.md",
    "ENGINEERING-LESSONS.md",
    "blueprints/EXECUTION-ROADMAP.md",
    *RECOVERY_FIXED_START_PATHS,
)
RECOVERY_ACTIVE_CONTROL_PATHS = (
    "diagnostics/T2.2-recovery-architecture-v1.md",
    "diagnostics/T2.2-recovery-architecture-v1-preflight-review.md",
    "diagnostics/T2.2-recovery-architecture-v2.md",
    "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md",
    "diagnostics/T2.2-recovery-architecture-v3.md",
    "diagnostics/T2.2-recovery-architecture-v3-preflight-review.md",
    "diagnostics/T2.2-recovery-architecture-v3-preflight-review-quality-audit.md",
)
RECOVERY_PREPARATION_READ_TASKS = {
    "T2.2-R01",
    "T2.2-R02",
    "T2.2-R03",
    "T2.2-R04",
    "T2.2-R06",
}
RECOVERY_FULL_BRIEF_PATH = "diagnostics/T2.2-judge-brief-v2.md"
RECOVERY_VARIANT_BRIEF_PATH = (
    "diagnostics/T2.2-judge-brief-variant-v1-02.md"
)
RECOVERY_SCORING_KEY_PATH = "diagnostics/T2.2-scoring-key-v2.md"
RECOVERY_CONTRAST_KEY_PATH = "diagnostics/T2.2-contrast-key-v1.md"
RECOVERY_PACKAGE_REVIEW_PATH = (
    "diagnostics/T2.2-package-preflight-review-v2.md"
)
RECOVERY_EXACT_HEADER = "---\nstatus: {status}\nscope: {scope}\n---\n"
RECOVERY_BLOCKER_HEADER = "---\nstatus: blocked\nscope: run-only\n---\n"
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
GLOSSARY_STATUS_HEADERS = (
    "---\nstatus: draft\nscope: long-term\n---\n",
    "---\nstatus: frozen\nscope: long-term\n---\n",
)
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
    root = Path(os.path.abspath(project_root))
    normalized = Path(os.path.abspath(path))
    try:
        label = normalized.relative_to(root).as_posix()
    except ValueError:
        errors.append(f"path escapes project root: {path}")
        return None
    parent = normalized.parent
    while parent != root:
        try:
            parent_mode = parent.lstat().st_mode
        except OSError:
            break
        if stat.S_ISLNK(parent_mode):
            errors.append(f"symlinked parent directory forbidden: {label}")
            return None
        parent = parent.parent
    try:
        mode = normalized.lstat().st_mode
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
            normalized,
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


def _taskcard_section_bodies(text: str) -> dict[str, str]:
    if not has_exact_taskcard_sections(text):
        return {}
    matches = list(
        re.finditer(
            r"^(" + "|".join(re.escape(item) for item in TASK_SECTION_HEADINGS) + r")$",
            text,
            flags=re.MULTILINE,
        )
    )
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[match.end() : end]
    return sections


def _material_slot_references(text: str) -> list[str]:
    references = re.findall(
        r"materials/T2\.2-v2/[^\s`|)>\],;，。]*",
        text,
        flags=re.IGNORECASE,
    )
    return [
        reference
        for reference in references
        if reference != "materials/T2.2-v2/authorization.md"
    ]


def _taskcard_relative_path_references(text: str) -> list[str]:
    references: list[str] = []
    for token in re.findall(r"`([^`\n]+)`", text):
        if (
            token.endswith(
                (".md", ".py", ".json", ".toml", ".yaml", ".yml", ".txt", ".bin")
            )
            or any(character in token for character in "*?[]<>{}")
            or "/" in token
        ):
            references.append(token)
    return references


def _r05_has_expanded_material_authorization(
    read_section: str, expected_policy_lines: set[str]
) -> bool:
    authorization_control_line = (
        "- read-path: `materials/T2.2-v2/authorization.md`"
    )
    remaining = "\n".join(
        line
        for line in read_section.splitlines()
        if line not in expected_policy_lines
        and line != authorization_control_line
    )
    forbidden_patterns = (
        r"runtime-open:",
        r"(?:打开|读取|扫描|探测)(?:任一|全部|整个|所有).{0,12}(?:材料|slot|目录)?",
        r"(?:允许|可以|可)(?:打开|读取|扫描|探测).{0,24}(?:任一|全部|整个|所有|目录|glob|材料|slot)",
        r"\b(?:allow|open|read|scan|probe).{0,24}\b(?:all|any|directory|glob|material|slot)s?\b",
    )
    return any(
        re.search(pattern, remaining, flags=re.IGNORECASE)
        for pattern in forbidden_patterns
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


def _walk_files_pruned(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, directory_names, file_names in os.walk(
        root, topdown=True, followlinks=False
    ):
        current_path = Path(current)
        if current_path == root:
            directory_names[:] = [
                name for name in directory_names if name != ".git"
            ]
        if current_path == root / "materials":
            directory_names[:] = [
                name for name in directory_names if name != "T2.2-v2"
            ]
        directory_names.sort()
        file_names.sort()
        files.extend(current_path / name for name in file_names)
    return files


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
            for current, directory_names, file_names in os.walk(
                root, topdown=True, followlinks=False
            ):
                current_path = Path(current)
                retained_directories: list[str] = []
                for name in sorted(directory_names):
                    path = current_path / name
                    relative = path.relative_to(ROOT).as_posix()
                    if path.is_symlink():
                        links.append(path)
                        continue
                    if relative == "materials/T2.2-v2":
                        continue
                    retained_directories.append(name)
                directory_names[:] = retained_directories
                links.extend(
                    current_path / name
                    for name in sorted(file_names)
                    if (current_path / name).is_symlink()
                )
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

    nested_guards: list[Path] = []
    for current, directory_names, file_names in os.walk(
        materials, topdown=True, followlinks=False
    ):
        current_path = Path(current)
        if current_path == materials:
            directory_names[:] = [
                name for name in directory_names if name != "T2.2-v2"
            ]
        if ".gitignore" in file_names and current_path / ".gitignore" != guard:
            nested_guards.append(current_path / ".gitignore")
    nested_guards.sort()
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


def _regular_file_content_if_present(
    relative_path: str, errors: list[str], project_root: Path
) -> bytes | None:
    path = project_root / relative_path
    try:
        path.lstat()
    except FileNotFoundError:
        return None
    except OSError as error:
        errors.append(f"cannot inspect recovery artifact {relative_path}: {error}")
        return None
    return read_regular_bytes(path, errors, project_root)


def _validate_fixed_file_hash(
    relative_path: str,
    expected_hash: str,
    errors: list[str],
    project_root: Path,
) -> bytes | None:
    content = read_regular_bytes(project_root / relative_path, errors, project_root)
    if content is not None:
        actual_hash = hashlib.sha256(content).hexdigest()
        if actual_hash != expected_hash:
            errors.append(
                f"fixed recovery identity hash mismatch: {relative_path}: "
                f"{actual_hash} != {expected_hash}"
            )
    return content


def _validate_commit_identity(
    relative_path: str,
    commit: str,
    expected_hash: str,
    errors: list[str],
    project_root: Path,
) -> None:
    try:
        ancestor = subprocess.run(
            ["git", "-C", str(project_root), "merge-base", "--is-ancestor", commit, "HEAD"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        blob = subprocess.run(
            ["git", "-C", str(project_root), "show", f"{commit}:{relative_path}"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        errors.append(f"cannot verify recovery commit identity {commit}: {error}")
        return
    if ancestor.returncode != 0:
        errors.append(f"recovery identity commit is not a HEAD ancestor: {commit}")
    if blob.returncode != 0:
        detail = blob.stderr.decode("utf-8", errors="replace").strip()
        errors.append(
            f"cannot read fixed recovery commit blob {commit}:{relative_path}: {detail}"
        )
    elif hashlib.sha256(blob.stdout).hexdigest() != expected_hash:
        errors.append(
            f"fixed recovery commit blob hash mismatch: {commit}:{relative_path}"
        )


def _format_artifact_policy_line(
    relative_path: str, policy: dict[str, str]
) -> str:
    direct_review = policy["direct-review-path"]
    direct_value = f"`{direct_review}`" if direct_review != "none" else "none"
    return (
        f"- artifact-policy: `{relative_path}`"
        f" | owner: {policy['owner']}"
        f" | header-required: {policy['header-required']}"
        f" | status: {policy['status']}"
        f" | scope: {policy['scope']}"
        f" | direct-review-path: {direct_value}"
        f" | review-scope-inherits: {policy['review-scope-inherits']}"
        f" | m2-active: {policy['m2-active']}"
        f" | attempt-local: {policy['attempt-local']}"
    )


def _recovery_blocker_policy(task_id: str) -> tuple[str, dict[str, str]]:
    matches = [
        (path, policy)
        for path, policy in RECOVERY_BLOCKER_ARTIFACT_POLICY.items()
        if policy["owner"] == task_id
    ]
    if len(matches) != 1:
        raise RuntimeError(f"invalid blocker policy for {task_id}")
    return matches[0]


def _recovery_raw_policy() -> dict[str, str]:
    return _artifact_policy(
        "T2.2-R03",
        "non-markdown",
        "run-only",
        "diagnostics/T2.2-fixture-byte-review-v2.md",
        header_required="no",
    )


def _recovery_material_policy() -> dict[str, str]:
    return _artifact_policy(
        "T2.2-R03/product",
        "raw-input",
        "run-only",
        header_required="no",
    )


def _expected_card_policy_lines(task_id: str) -> set[str]:
    lines = {
        _format_artifact_policy_line(path, policy)
        for path, policy in RECOVERY_ARTIFACT_POLICY.items()
        if policy["owner"].startswith(task_id)
    }
    if task_id == "T2.2-R03":
        raw_policy = _recovery_raw_policy()
        material_policy = _recovery_material_policy()
        lines.update(
            _format_artifact_policy_line(path, raw_policy)
            for path in RECOVERY_RAW_BLOBS
        )
        lines.update(
            _format_artifact_policy_line(path, material_policy)
            for path in RECOVERY_MATERIAL_SLOTS
        )
    blocker_path, blocker_policy = _recovery_blocker_policy(task_id)
    lines.add(_format_artifact_policy_line(blocker_path, blocker_policy))
    return lines


def _expected_card_material_slot_lines(task_id: str) -> set[str]:
    if task_id not in {"T2.2-R03", "T2.2-R04", "T2.2-R05", "T2.2-R06"}:
        return set()
    runtime_open = "forbidden" if task_id == "T2.2-R05" else "selected-only"
    return {
        f"- material-slot-policy: `{path}` | runtime-open: {runtime_open}"
        for path in RECOVERY_MATERIAL_SLOTS
    }


def _recovery_output_paths(*task_ids: str) -> set[str]:
    expected = set(task_ids)
    return {
        path
        for path, policy in RECOVERY_ARTIFACT_POLICY.items()
        if policy["owner"].split()[0].split("/")[0] in expected
    }


def _prior_recovery_blocker_paths(task_id: str) -> set[str]:
    task_number = int(task_id.removeprefix("T2.2-R"))
    prior_ids = {
        f"T2.2-R{index:02d}" for index in range(1, task_number)
    }
    return {
        path
        for path, policy in RECOVERY_BLOCKER_ARTIFACT_POLICY.items()
        if policy["owner"] in prior_ids
    }


def _expected_card_read_paths(task_id: str) -> set[str]:
    chain_dependencies = _recovery_chain_dependencies(
        "SLOTS_REQUIRED", r01_product_blocker_present=True
    )
    paths = {
        *RECOVERY_CARD_COMMON_READ_PATHS,
        f"taskcards/{task_id}.md",
        *_prior_recovery_blocker_paths(task_id),
    }
    if task_id in RECOVERY_PREPARATION_READ_TASKS:
        paths.update({"GOLD-STANDARDS.md", *RECOVERY_SOURCE_PATHS})

    if task_id == "T2.2-R02":
        paths.update(_recovery_output_paths("T2.2-R01"))
    elif task_id == "T2.2-R03":
        paths.update(_recovery_output_paths("T2.2-R01", "T2.2-R02"))
        paths.add("materials/T2.2-v2/authorization.md")
    elif task_id == "T2.2-R04":
        paths.update(
            _recovery_output_paths("T2.2-R01", "T2.2-R02", "T2.2-R03")
        )
        paths.update(RECOVERY_RAW_BLOBS)
    elif task_id == "T2.2-R05":
        paths.update(
            chain_dependencies[RECOVERY_ATTEMPT_MANIFEST_PATH]
        )
    elif task_id == "T2.2-R06":
        paths.update(
            _recovery_output_paths(
                "T2.2-R01",
                "T2.2-R02",
                "T2.2-R03",
                "T2.2-R04",
                "T2.2-R05",
            )
        )
        paths.update(RECOVERY_RAW_BLOBS)

    adapter_path = "contracts/T2.2-historical-qualification-adapter-v1.md"
    control_call = "diagnostics/T2.2-contrast-control-call-manifest-v1.md"
    control_review = "diagnostics/T2.2-contrast-control-input-review-v1.md"
    control_index = "diagnostics/T2.2-contrast-control-answers-index-v1.md"
    control_result = "diagnostics/T2.2-contrast-control-results-v1.md"
    diagnostic_call = "diagnostics/T2.2-contrast-diagnostic-call-manifest-v1.md"
    diagnostic_review = "diagnostics/T2.2-contrast-diagnostic-input-review-v1.md"
    diagnostic_index = "diagnostics/T2.2-contrast-diagnostic-answers-index-v1.md"
    contrast_result = "diagnostics/T2.2-contrast-results-v1.md"
    retest_call = "diagnostics/T2.2-retest-call-manifest-v2.md"
    retest_review = "diagnostics/T2.2-retest-input-review-v2.md"
    formal_index = "diagnostics/T2.2-judge-answers-index-v2.md"
    baseline = "diagnostics/T2.2-judge-baseline-v2.md"
    control_answers = tuple(
        f"diagnostics/T2.2-contrast-answer-v1-{index:02d}.md"
        for index in range(1, 5)
    )
    diagnostic_answers = tuple(
        f"diagnostics/T2.2-contrast-answer-v1-{index:02d}.md"
        for index in range(5, 15)
    )
    formal_answers = tuple(
        f"diagnostics/T2.2-judge-answer-v2-{index:02d}.md"
        for index in range(1, 15)
    )
    if task_id == "T2.2-R07":
        paths.update(chain_dependencies[control_call])
        paths.add(adapter_path)
    elif task_id == "T2.2-R08":
        paths.update({control_call, *chain_dependencies[control_call]})
        paths.add(adapter_path)
    elif task_id == "T2.2-R09":
        paths.update(chain_dependencies[control_index])
        for answer_path in control_answers:
            paths.update(chain_dependencies[answer_path])
        paths.add(adapter_path)
    elif task_id == "T2.2-R10":
        paths.update(chain_dependencies[control_result])
    elif task_id == "T2.2-R11":
        paths.update({control_result, *chain_dependencies[control_result]})
    elif task_id == "T2.2-R12":
        paths.update(chain_dependencies[diagnostic_call])
        paths.add(adapter_path)
    elif task_id == "T2.2-R13":
        paths.update({diagnostic_call, *chain_dependencies[diagnostic_call]})
        paths.add(adapter_path)
    elif task_id == "T2.2-R14":
        paths.update(chain_dependencies[diagnostic_index])
        for answer_path in diagnostic_answers:
            paths.update(chain_dependencies[answer_path])
        paths.add(adapter_path)
    elif task_id == "T2.2-R15":
        paths.update(chain_dependencies[contrast_result])
    elif task_id == "T2.2-R16":
        paths.update({contrast_result, *chain_dependencies[contrast_result]})
    elif task_id == "T2.2-R17":
        paths.update(chain_dependencies[retest_call])
        paths.add(adapter_path)
    elif task_id == "T2.2-R18":
        paths.update({retest_call, *chain_dependencies[retest_call]})
        paths.add(adapter_path)
    elif task_id == "T2.2-R19":
        paths.update(chain_dependencies[formal_index])
        for answer_path in formal_answers:
            paths.update(chain_dependencies[answer_path])
        paths.add(adapter_path)
    elif task_id == "T2.2-R20":
        paths.update(chain_dependencies[baseline])
    elif task_id == "T2.2-R21":
        paths.update(RECOVERY_ACTIVE_CONTROL_PATHS)
        paths.update(
            {
                "diagnostics/T2.1-r01-r08.md",
                "lenses/T2.3-seed-lenses-v2.md",
            }
        )
        paths.update(
            _recovery_output_paths(
                *[f"T2.2-R{index:02d}" for index in range(1, 21)]
            )
        )
        paths.discard("materials/T2.2-v2/authorization.md")
        paths.update(RECOVERY_RAW_BLOBS)
    return paths


def _expected_card_read_path_lines(task_id: str) -> set[str]:
    return {
        f"- read-path: `{path}`"
        for path in _expected_card_read_paths(task_id)
    }


def _validate_recovery_policy_invariants(errors: list[str]) -> None:
    if len(RECOVERY_ARTIFACT_POLICY) != 82:
        errors.append(
            "recovery artifact policy must contain exactly 82 normal Markdown outputs"
        )
    if len(RECOVERY_REVIEW_SUBJECTS) != 11:
        errors.append("recovery direct-review map must contain exactly 11 relations")
    stateful_policy_count = (
        len(RECOVERY_ARTIFACT_POLICY)
        + len(RECOVERY_BLOCKER_ARTIFACT_POLICY)
        + len(RECOVERY_CONTROL_ARTIFACT_POLICY)
    )
    if stateful_policy_count != 105:
        errors.append(
            "recovery stateful artifact policy must contain exactly 105 paths"
        )
    if {
        policy["owner"] for policy in RECOVERY_BLOCKER_ARTIFACT_POLICY.values()
    } != set(RECOVERY_TASK_IDS):
        errors.append("recovery blocker policy owner set must equal the 21 task IDs")
    for task_id in RECOVERY_TASK_IDS:
        read_paths = _expected_card_read_paths(task_id)
        if f"taskcards/{task_id}.md" not in read_paths:
            errors.append(f"recovery taskcard read projection omits itself: {task_id}")
        preparation_paths = {"GOLD-STANDARDS.md", *RECOVERY_SOURCE_PATHS}
        actual_preparation_paths = read_paths & preparation_paths
        expected_preparation_paths = (
            preparation_paths
            if task_id in RECOVERY_PREPARATION_READ_TASKS
            else set()
        )
        if actual_preparation_paths != expected_preparation_paths:
            errors.append(
                f"recovery preparation read isolation mismatch: {task_id}"
            )
        material_read_paths = {
            path for path in read_paths if path.startswith("materials/")
        }
        if task_id == "T2.2-R05" and material_read_paths != {
            "materials/T2.2-v2/authorization.md"
        }:
            errors.append(
                "R05 read projection may contain only the authorization control file"
            )
        if (
            int(task_id.removeprefix("T2.2-R")) >= 7
            and material_read_paths
        ):
            errors.append(
                f"post-preparation read projection must not open materials: {task_id}"
            )
    for consumer, inputs in _recovery_chain_dependencies(
        "SLOTS_REQUIRED", r01_product_blocker_present=True
    ).items():
        owner = RECOVERY_ARTIFACT_POLICY[consumer]["owner"].split()[0]
        owner = owner.split("/")[0]
        missing_inputs = set(inputs) - _expected_card_read_paths(owner)
        if missing_inputs:
            errors.append(
                f"recovery read projection misses hash dependencies: "
                f"{owner}: {sorted(missing_inputs)}"
            )
    for review_path, subjects in RECOVERY_REVIEW_SUBJECTS.items():
        review_policy = RECOVERY_ARTIFACT_POLICY.get(review_path)
        if review_policy is None:
            continue
        reviewer = review_policy["owner"].split()[0].split("/")[0]
        missing_subjects = set(subjects) - _expected_card_read_paths(reviewer)
        if missing_subjects:
            errors.append(
                f"recovery reviewer read projection misses subjects: "
                f"{reviewer}: {sorted(missing_subjects)}"
            )

    review_subject_map: dict[str, str] = {}
    for review_path, subjects in RECOVERY_REVIEW_SUBJECTS.items():
        for subject_path in subjects:
            if subject_path in review_subject_map:
                errors.append(
                    f"recovery subject has multiple direct reviews: {subject_path}"
                )
            review_subject_map[subject_path] = review_path

    for path, policy in RECOVERY_ARTIFACT_POLICY.items():
        expected_review = review_subject_map.get(path, "none")
        if policy["direct-review-path"] != expected_review:
            errors.append(
                f"artifact/direct-review map mismatch: {path}: "
                f"{policy['direct-review-path']} != {expected_review}"
            )

    for path in RECOVERY_RAW_BLOBS:
        if review_subject_map.get(path) != (
            "diagnostics/T2.2-fixture-byte-review-v2.md"
        ):
            errors.append(f"raw blob direct-review mapping missing: {path}")

    scopes = {
        path: policy["scope"]
        for path, policy in RECOVERY_ARTIFACT_POLICY.items()
    }
    scopes.update(
        {
            "diagnostics/T2.2-recovery-architecture-v3.md": "run-only",
            "diagnostics/T2.2-recovery-architecture-v3-preflight-review.md": "run-only",
        }
    )
    scopes.update({path: "run-only" for path in RECOVERY_RAW_BLOBS})
    for review_path, subjects in RECOVERY_REVIEW_SUBJECTS.items():
        review_scope = scopes.get(review_path)
        if review_scope is None:
            errors.append(f"review missing lifecycle policy: {review_path}")
            continue
        for subject_path in subjects:
            if subject_path == "materials/T2.2-v2/authorization.md":
                subject_scope = "run-only"
            else:
                subject_scope = scopes.get(subject_path)
            if subject_scope != review_scope:
                errors.append(
                    f"review scope does not inherit subject scope: "
                    f"{review_path} <- {subject_path}"
                )


def _validate_recovery_roadmap(
    errors: list[str], project_root: Path
) -> None:
    roadmap_path = project_root / "blueprints/EXECUTION-ROADMAP.md"
    roadmap = read_regular_utf8(roadmap_path, errors, project_root)
    if roadmap is None:
        return
    roadmap_ids = set(re.findall(r"\bT2\.2-R\d{2}\b", roadmap))
    expected_ids = set(RECOVERY_TASK_IDS)
    if roadmap_ids != expected_ids:
        errors.append(
            "roadmap recovery ID set mismatch: "
            f"missing {sorted(expected_ids - roadmap_ids)}, "
            f"unexpected {sorted(roadmap_ids - expected_ids)}"
        )
    required_literals = {
        "A2_CONTROL_PLANE_INTEGRATED",
        "controller-only bootstrap seam",
        "recovery-registration-cardinality: 0|21",
        "recovery-composite-task-ids: T2.2-R09,T2.2-R14,T2.2-R19",
        "recovery-normal-markdown-output-count: 82",
        "recovery-stateful-path-universe-count: 105",
        "recovery-direct-review-count: 11",
        "recovery-material-slot-count: 14",
        "recovery-raw-blob-count: 28",
        "t2.2-active-baseline-path: diagnostics/T2.2-judge-baseline-v2.md",
        "t2.2-active-postflight-review-path: diagnostics/T2.2-postflight-review-v2.md",
        "t2.2-history-v1-baseline-result: FAIL",
        "diagnostics/M2-gate-receipt.md",
    }
    missing = sorted(literal for literal in required_literals if literal not in roadmap)
    if missing:
        errors.append(f"recovery roadmap control literals missing: {missing}")
    receipt_block = re.search(
        r"未来 M2 receipt 的 T2\.2 机器字段必须恰好一次"
        r".*?```text\n(?P<schema>.*?)```",
        roadmap,
        flags=re.DOTALL,
    )
    if receipt_block is None:
        errors.append("recovery roadmap v3 receipt schema block missing")
    else:
        roadmap_keys = tuple(
            line.split(":", 1)[0]
            for line in receipt_block.group("schema").splitlines()
            if line.strip()
        )
        if roadmap_keys != M2_RECEIPT_REQUIRED_KEYS:
            errors.append(
                "recovery roadmap receipt schema must exactly match "
                "v3 section 13.2"
            )
    if re.search(r"\blatest\b", roadmap, flags=re.IGNORECASE):
        errors.append("recovery roadmap must not use latest-path resolution")


def _validate_recovery_document_wiring(
    errors: list[str], project_root: Path
) -> None:
    requirements = {
        "README.md": {
            "A2_CONTROL_PLANE_INTEGRATED",
            "恢复卡数量：`0`",
            "T2.2 资格仍为 `FAIL`",
            "M2 receipt 仍不存在",
            "C0 不授权恢复卡、材料、模型调用、M2 receipt 或恢复执行",
        },
        "taskcards/T3.6.md": {
            "diagnostics/T2.2-judge-baseline-v2.md",
            "diagnostics/T2.2-postflight-review-v2.md",
            "diagnostics/T2.2-judge-baseline.md",
            "taskcards/T2.2-BLOCKER.md",
            "无有效 `diagnostics/M2-gate-receipt.md` 即硬阻塞",
            "禁止版本扫描、别名、回退或 latest 解析",
        },
        "taskcards/T4.1.md": {
            "diagnostics/T2.2-judge-baseline-v2.md",
            "diagnostics/T2.2-postflight-review-v2.md",
            "diagnostics/T2.2-judge-baseline.md",
            "taskcards/T2.2-BLOCKER.md",
            "无有效 `diagnostics/M2-gate-receipt.md` 即硬阻塞",
            "禁止版本扫描、别名、回退或 latest 解析",
        },
    }
    for relative_path, literals in requirements.items():
        text = read_regular_utf8(project_root / relative_path, errors, project_root)
        if text is None:
            continue
        missing = sorted(literal for literal in literals if literal not in text)
        if missing:
            errors.append(
                f"recovery downstream wiring missing in {relative_path}: {missing}"
            )


def _recovery_taskcard_names(
    errors: list[str], project_root: Path
) -> set[str]:
    taskcard_root = project_root / "taskcards"
    try:
        entries = list(os.scandir(taskcard_root))
    except OSError as error:
        errors.append(f"cannot inspect recovery taskcards: {error}")
        return set()

    expected_cards = {f"{task_id}.md" for task_id in RECOVERY_TASK_IDS}
    expected_blockers = {
        PurePosixPath(path).name
        for path in RECOVERY_BLOCKER_ARTIFACT_POLICY
    }
    recovery_like = {
        entry.name
        for entry in entries
        if entry.name.casefold().startswith("t2.2-r")
    }
    formal_cards = recovery_like & expected_cards
    blockers = recovery_like & expected_blockers
    unexpected = recovery_like - expected_cards - expected_blockers
    if unexpected:
        errors.append(f"unexpected recovery taskcard/blocker names: {sorted(unexpected)}")

    if len(formal_cards) not in {0, 21}:
        errors.append(
            "recovery taskcards must register atomically as 0 or 21: "
            f"observed {len(formal_cards)}"
        )
    if formal_cards and formal_cards != expected_cards:
        errors.append(
            "recovery taskcard closed set mismatch: "
            f"missing {sorted(expected_cards - formal_cards)}, "
            f"unexpected {sorted(formal_cards - expected_cards)}"
        )
    if blockers and formal_cards != expected_cards:
        errors.append("recovery blocker exists before the 21-card set is registered")

    registered_ids = {name.removesuffix(".md") for name in formal_cards}
    for blocker_name in blockers:
        blocker_id = blocker_name.removesuffix("-BLOCKER.md")
        if blocker_id not in registered_ids:
            errors.append(
                f"recovery blocker does not belong to a registered ID: {blocker_name}"
            )
        blocker = taskcard_root / blocker_name
        content = read_regular_bytes(blocker, errors, project_root)
        if content is not None and not content.startswith(
            RECOVERY_BLOCKER_HEADER.encode("utf-8")
        ):
            errors.append(
                f"recovery blocker header must be blocked/run-only at byte 0: "
                f"taskcards/{blocker_name}"
            )

    if formal_cards == expected_cards:
        for task_id in RECOVERY_TASK_IDS:
            relative_path = f"taskcards/{task_id}.md"
            path = project_root / relative_path
            text = read_regular_utf8(path, errors, project_root)
            if text is None:
                continue
            if not has_exact_taskcard_sections(text):
                errors.append(
                    f"recovery taskcard sections must match TEMPLATE.md: {relative_path}"
                )
            sections = _taskcard_section_bodies(text)
            read_section = sections.get(TASK_SECTION_HEADINGS[2], "")
            write_section = sections.get(TASK_SECTION_HEADINGS[3], "")
            expected_mode = (
                "composite"
                if task_id in RECOVERY_COMPOSITE_TASK_IDS
                else "single-session"
            )
            mode_lines = re.findall(
                r"^- recovery-execution-mode: (.+)$",
                text,
                flags=re.MULTILINE,
            )
            if mode_lines != [expected_mode]:
                errors.append(
                    f"recovery composite/single-session mode mismatch: {relative_path}"
                )
            if text.count(f"`{task_id}`：") != 1:
                errors.append(f"recovery task ID/title mismatch: {relative_path}")
            actual_policy_lines = [
                line
                for line in text.splitlines()
                if line.startswith("- artifact-policy:")
            ]
            write_policy_lines = [
                line
                for line in write_section.splitlines()
                if line.startswith("- artifact-policy:")
            ]
            expected_policy_lines = _expected_card_policy_lines(task_id)
            if (
                len(actual_policy_lines) != len(set(actual_policy_lines))
                or actual_policy_lines != write_policy_lines
                or set(actual_policy_lines) != expected_policy_lines
            ):
                errors.append(
                    f"recovery taskcard write/artifact-policy projection mismatch: "
                    f"{relative_path}"
                )
            actual_write_path_references = sorted(
                _taskcard_relative_path_references(write_section)
            )
            expected_write_path_references = sorted(
                _taskcard_relative_path_references(
                    "\n".join(expected_policy_lines)
                )
            )
            if actual_write_path_references != expected_write_path_references:
                errors.append(
                    f"recovery taskcard write whitelist path mismatch: "
                    f"{relative_path}"
                )
            actual_read_lines = [
                line
                for line in text.splitlines()
                if line.startswith("- read-path:")
            ]
            section_read_lines = [
                line
                for line in read_section.splitlines()
                if line.startswith("- read-path:")
            ]
            expected_read_lines = _expected_card_read_path_lines(task_id)
            if (
                len(actual_read_lines) != len(set(actual_read_lines))
                or actual_read_lines != section_read_lines
                or set(actual_read_lines) != expected_read_lines
            ):
                errors.append(
                    f"recovery taskcard read-path projection mismatch: "
                    f"{relative_path}"
                )
            actual_material_lines = [
                line
                for line in text.splitlines()
                if line.startswith("- material-slot-policy:")
            ]
            read_material_lines = [
                line
                for line in read_section.splitlines()
                if line.startswith("- material-slot-policy:")
            ]
            expected_material_lines = _expected_card_material_slot_lines(task_id)
            if (
                len(actual_material_lines) != len(set(actual_material_lines))
                or actual_material_lines != read_material_lines
                or set(actual_material_lines) != expected_material_lines
            ):
                errors.append(
                    f"recovery taskcard read/material-slot-policy projection mismatch: "
                    f"{relative_path}"
                )
            material_references = _material_slot_references(read_section)
            expected_material_references = (
                list(RECOVERY_MATERIAL_SLOTS)
                if task_id
                in {"T2.2-R03", "T2.2-R04", "T2.2-R05", "T2.2-R06"}
                else []
            )
            if (
                len(material_references) != len(set(material_references))
                or set(material_references) != set(expected_material_references)
            ):
                errors.append(
                    f"recovery taskcard material read whitelist mismatch: "
                    f"{relative_path}"
                )
            actual_read_path_references = sorted(
                _taskcard_relative_path_references(read_section)
            )
            expected_read_path_references = sorted(
                {
                    *_expected_card_read_paths(task_id),
                    *expected_material_references,
                }
            )
            if actual_read_path_references != expected_read_path_references:
                errors.append(
                    f"recovery taskcard complete read whitelist path mismatch: "
                    f"{relative_path}"
                )
            runtime_values = re.findall(
                r"runtime-open: ([a-z-]+)", read_section
            )
            expected_runtime = (
                ["forbidden"] * 14
                if task_id == "T2.2-R05"
                else (
                    ["selected-only"] * 14
                    if task_id
                    in {"T2.2-R03", "T2.2-R04", "T2.2-R06"}
                    else []
                )
            )
            if sorted(runtime_values) != sorted(expected_runtime):
                errors.append(
                    f"recovery taskcard material runtime-open contract mismatch: "
                    f"{relative_path}"
                )
            if task_id == "T2.2-R05" and _r05_has_expanded_material_authorization(
                read_section, expected_material_lines
            ):
                errors.append(
                    "R05 read whitelist must forbid every material open, "
                    f"directory, glob, or all-material authorization: {relative_path}"
                )
    return formal_cards


def _validate_recovery_selector(
    errors: list[str], project_root: Path
) -> tuple[set[str], str | None]:
    selector_content = _regular_file_content_if_present(
        RECOVERY_SELECTOR_PATH, errors, project_root
    )
    if selector_content is None:
        return set(), None
    try:
        selector = selector_content.decode("utf-8")
    except UnicodeError as error:
        errors.append(f"recovery selector is not UTF-8: {error}")
        return set(), None

    exact_header = RECOVERY_EXACT_HEADER.format(
        status="frozen", scope="run-only"
    )
    if not selector.startswith(exact_header):
        errors.append("recovery selector must start with exact frozen/run-only header")
    if selector.count("slot-set-id: T2.2-V2-SOURCE-SLOTS-01-14") != 1:
        errors.append("recovery selector slot-set-id missing or duplicated")

    slot_members = re.findall(r"^slot-member: (.+)$", selector, flags=re.MULTILINE)
    selected_lines = re.findall(
        r"^selected-slot: ([^|]+) \| source-group: ([^|]+) \| request-id: (.+)$",
        selector,
        flags=re.MULTILINE,
    )
    selected = {path.strip() for path, _, _ in selected_lines}
    selected_groups = [group.strip() for _, group, _ in selected_lines]
    request_ids = [request_id.strip() for _, _, request_id in selected_lines]
    unselected = set(
        re.findall(r"^unselected-slot: (.+)$", selector, flags=re.MULTILINE)
    )
    allowed = set(RECOVERY_MATERIAL_SLOTS)
    if len(slot_members) != 14 or set(slot_members) != allowed:
        errors.append("recovery selector static slot-member set must equal the 14 literals")
    if len(selected) != len(selected_lines):
        errors.append("recovery selector selected-slot entries must be unique")
    allowed_groups = {f"{index:02d}" for index in range(1, 15)}
    if (
        len(selected_groups) != len(set(selected_groups))
        or any(group not in allowed_groups for group in selected_groups)
    ):
        errors.append(
            "recovery selector selected source-groups must be unique members of 01-14"
        )
    if (
        len(request_ids) != len(set(request_ids))
        or any(not request_id for request_id in request_ids)
    ):
        errors.append("recovery selector selected request IDs must be unique/nonempty")
    if selected - allowed or unselected - allowed:
        errors.append(
            "recovery selector contains slot outside the static 14-member whitelist"
        )
    for path, group, _ in selected_lines:
        normalized_group = group.strip()
        if normalized_group in allowed_groups and path.strip() != (
            RECOVERY_MATERIAL_SLOTS[int(normalized_group) - 1]
        ):
            errors.append(
                "recovery selector selected slot/source-group mapping mismatch: "
                f"{path.strip()} != group {normalized_group}"
            )
    if selected & unselected or selected | unselected != allowed:
        errors.append(
            "recovery selector selected/unselected sets must be disjoint complements"
        )

    count_matches = re.findall(
        r"^selected-slot-count: ([0-9]+)$", selector, flags=re.MULTILINE
    )
    if count_matches != [str(len(selected))]:
        errors.append("recovery selector selected-slot-count mismatch")
    result_matches = re.findall(
        r"^selector-result: (NO_SLOTS|SLOTS_REQUIRED|BLOCKED)$",
        selector,
        flags=re.MULTILINE,
    )
    selector_result = result_matches[0] if len(result_matches) == 1 else None
    if selector_result is None:
        errors.append("recovery selector-result missing, duplicated, or invalid")
    elif selector_result == "NO_SLOTS" and selected:
        errors.append("NO_SLOTS selector must have zero selected slots")
    elif selector_result == "SLOTS_REQUIRED" and not selected:
        errors.append("SLOTS_REQUIRED selector must select at least one slot")
    if not re.search(r"^selection-reason: .+$", selector, flags=re.MULTILINE):
        errors.append("recovery selector selection-reason missing")

    for relative_path in sorted(selected & allowed):
        content = read_regular_bytes(
            project_root / relative_path, errors, project_root
        )
        if content is not None and content.startswith(b"---\nstatus:"):
            errors.append(
                f"selected raw material slot must not have Markdown header: "
                f"{relative_path}"
            )
    return selected, selector_result


def _validate_recovery_raw_blobs(
    errors: list[str], project_root: Path
) -> set[str]:
    raw_root = project_root / "diagnostics/T2.2-fixture-bytes-v2"
    try:
        mode = raw_root.lstat().st_mode
    except FileNotFoundError:
        return set()
    except OSError as error:
        errors.append(f"cannot inspect recovery raw blob directory: {error}")
        return set()
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        errors.append("recovery raw blob root must be a regular directory, not symlink")
        return set()
    try:
        entries = list(os.scandir(raw_root))
    except OSError as error:
        errors.append(f"cannot scan recovery raw blob directory: {error}")
        return set()
    if not entries:
        return set()

    expected = set(RECOVERY_RAW_BLOBS)
    observed = {
        f"diagnostics/T2.2-fixture-bytes-v2/{entry.name}" for entry in entries
    }
    if observed != expected:
        errors.append(
            "recovery raw blobs must publish atomically as the exact 28-file set: "
            f"missing {sorted(expected - observed)}, "
            f"unexpected {sorted(observed - expected)}"
        )
    for relative_path in sorted(observed & expected):
        content = read_regular_bytes(
            project_root / relative_path, errors, project_root
        )
        if content is not None and content.startswith(b"---\nstatus:"):
            errors.append(
                f"recovery raw blob must not have Markdown header: {relative_path}"
            )
    return observed


def _validate_recovery_artifacts(
    errors: list[str], project_root: Path
) -> None:
    allowed_markdown = (
        RECOVERY_HISTORICAL_MARKDOWN
        | set(RECOVERY_ARTIFACT_POLICY)
        | {M2_RECEIPT_PATH}
    )
    for root_name in ("contracts", "diagnostics", "lenses", "runs"):
        root = project_root / root_name
        if not root.is_dir() or root.is_symlink():
            continue
        for current, directory_names, file_names in os.walk(
            root, topdown=True, followlinks=False
        ):
            current_path = Path(current)
            if current_path == project_root / "diagnostics":
                for name in directory_names:
                    if (
                        name.startswith("T2.2-")
                        and name != "T2.2-fixture-bytes-v2"
                    ):
                        errors.append(
                            "unexpected recovery artifact directory: "
                            f"diagnostics/{name}"
                        )
                directory_names[:] = [
                    name
                    for name in directory_names
                    if name != "T2.2-fixture-bytes-v2"
                ]
            for name in file_names:
                relative_path = (current_path / name).relative_to(
                    project_root
                ).as_posix()
                if (
                    name.startswith("T2.2-")
                    and relative_path not in allowed_markdown
                ):
                    errors.append(
                        f"unexpected recovery artifact path: {relative_path}"
                    )

    for relative_path, policy in RECOVERY_ARTIFACT_POLICY.items():
        content = _regular_file_content_if_present(
            relative_path, errors, project_root
        )
        if content is None:
            continue
        expected_header = RECOVERY_EXACT_HEADER.format(
            status=policy["status"], scope=policy["scope"]
        ).encode("utf-8")
        if not content.startswith(expected_header):
            errors.append(
                f"recovery artifact status/scope header mismatch: {relative_path}"
            )

    for review_path, subjects in RECOVERY_REVIEW_SUBJECTS.items():
        review_content = _regular_file_content_if_present(
            review_path, errors, project_root
        )
        if review_content is None:
            continue
        for subject_path in subjects:
            if (
                subject_path == "materials/T2.2-v2/authorization.md"
                and not (project_root / subject_path).exists()
            ):
                continue
            if _regular_file_content_if_present(
                subject_path, errors, project_root
            ) is None:
                errors.append(
                    f"direct review exists without its subject: "
                    f"{review_path} <- {subject_path}"
                )


def _path_entry_exists(path: Path, errors: list[str]) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    except OSError as error:
        errors.append(f"cannot inspect recovery blocker {path.name}: {error}")
        return True
    return True


def _validate_recovery_blockers_for_m2(
    errors: list[str], project_root: Path
) -> bool:
    for blocker_path in RECOVERY_BLOCKER_ARTIFACT_POLICY:
        if blocker_path == RECOVERY_R01_BLOCKER_PATH:
            continue
        if _path_entry_exists(project_root / blocker_path, errors):
            errors.append(
                "M2 receipt forbidden while non-closable recovery blocker exists: "
                f"{blocker_path}"
            )

    r01_path = project_root / RECOVERY_R01_BLOCKER_PATH
    if not _path_entry_exists(r01_path, errors):
        return False
    blocker_content = read_regular_bytes(r01_path, errors, project_root)
    if blocker_content is None:
        return True
    try:
        blocker = blocker_content.decode("utf-8")
    except UnicodeError as error:
        errors.append(f"R01 blocker is not UTF-8: {error}")
        return True
    if not blocker.startswith(RECOVERY_BLOCKER_HEADER):
        errors.append("R01 blocker must start with exact blocked/run-only header")
    blocker_types = re.findall(
        r"^blocker-type: ([a-z-]+)$", blocker, flags=re.MULTILINE
    )
    raw_blocker_type_lines = [
        line for line in blocker.splitlines() if line.startswith("blocker-type:")
    ]
    if (
        len(raw_blocker_type_lines) != len(blocker_types)
        or blocker_types != ["product-request"]
    ):
        errors.append(
            "R01 blocker can remain at M2 only as exact product-request type"
        )
    request_pattern = re.compile(
        r"^- product-request-id: ([A-Za-z0-9][A-Za-z0-9._-]*)$",
        flags=re.MULTILINE,
    )
    request_ids = request_pattern.findall(blocker)
    raw_request_lines = [
        line
        for line in blocker.splitlines()
        if line.startswith("- product-request-id:")
    ]
    if len(raw_request_lines) != len(request_ids):
        errors.append("R01 blocker has malformed product request ID")
    if not request_ids:
        errors.append("R01 product-request blocker must contain at least one request ID")
    if len(request_ids) != len(set(request_ids)):
        errors.append("R01 product-request blocker request IDs must be unique")

    resolution_path = "diagnostics/T2.2-fixture-resolution-v2.md"
    resolution_content = _regular_file_content_if_present(
        resolution_path, errors, project_root
    )
    if resolution_content is None:
        errors.append("R01 product-request blocker requires R03 resolution")
        return True
    try:
        resolution = resolution_content.decode("utf-8")
    except UnicodeError as error:
        errors.append(f"R03 resolution is not UTF-8: {error}")
        return True
    resolution_pattern = re.compile(
        r"^- product-request-resolution: "
        r"([A-Za-z0-9][A-Za-z0-9._-]*)"
        r" \| status: (resolved|rejected|unresolved)$",
        flags=re.MULTILINE,
    )
    resolution_records = resolution_pattern.findall(resolution)
    raw_resolution_lines = [
        line
        for line in resolution.splitlines()
        if line.startswith("- product-request-resolution:")
    ]
    if len(raw_resolution_lines) != len(resolution_records):
        errors.append("R03 resolution has malformed product request resolution")
    resolution_ids = [request_id for request_id, _ in resolution_records]
    if len(resolution_ids) != len(set(resolution_ids)):
        errors.append("R03 resolution product request IDs must be unique")
    if set(resolution_ids) != set(request_ids):
        errors.append(
            "R01 blocker and R03 resolution request ID sets must be exactly equal"
        )
    nonresolved = [
        (request_id, status)
        for request_id, status in resolution_records
        if status != "resolved"
    ]
    if nonresolved:
        errors.append(
            "R01 product-request blocker remains open unless every request is resolved"
        )
    return True


def _recovery_chain_dependencies(
    selector_result: str | None,
    r01_product_blocker_present: bool = False,
) -> dict[str, tuple[str, ...]]:
    control_answers = tuple(
        f"diagnostics/T2.2-contrast-answer-v1-{index:02d}.md"
        for index in range(1, 5)
    )
    diagnostic_answers = tuple(
        f"diagnostics/T2.2-contrast-answer-v1-{index:02d}.md"
        for index in range(5, 15)
    )
    formal_answers = tuple(
        f"diagnostics/T2.2-judge-answer-v2-{index:02d}.md"
        for index in range(1, 15)
    )
    control_call = "diagnostics/T2.2-contrast-control-call-manifest-v1.md"
    control_review = "diagnostics/T2.2-contrast-control-input-review-v1.md"
    diagnostic_call = "diagnostics/T2.2-contrast-diagnostic-call-manifest-v1.md"
    diagnostic_review = "diagnostics/T2.2-contrast-diagnostic-input-review-v1.md"
    retest_call = "diagnostics/T2.2-retest-call-manifest-v2.md"
    retest_review = "diagnostics/T2.2-retest-input-review-v2.md"
    control_index = "diagnostics/T2.2-contrast-control-answers-index-v1.md"
    diagnostic_index = "diagnostics/T2.2-contrast-diagnostic-answers-index-v1.md"
    formal_index = "diagnostics/T2.2-judge-answers-index-v2.md"
    control_result = "diagnostics/T2.2-contrast-control-results-v1.md"
    control_postflight = (
        "diagnostics/T2.2-contrast-control-postflight-review-v1.md"
    )
    contrast_result = "diagnostics/T2.2-contrast-results-v1.md"
    contrast_postflight = "diagnostics/T2.2-contrast-postflight-review-v1.md"
    brief = "diagnostics/T2.2-judge-brief-v2.md"
    variant = "diagnostics/T2.2-judge-brief-variant-v1-02.md"
    package_review = "diagnostics/T2.2-package-preflight-review-v2.md"
    contrast_key = "diagnostics/T2.2-contrast-key-v1.md"

    attempt_inputs = [
        RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture"][0],
        RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture-review"][0],
        "diagnostics/T2.2-recovery-architecture-v2.md",
        "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md",
        "diagnostics/T2.2-judge-baseline.md",
        "taskcards/T2.2-BLOCKER.md",
        "contracts/T2.2-historical-qualification-adapter-v1.md",
        "diagnostics/T2.2-fixture-census-v2.md",
        "diagnostics/T2.2-fixture-gap-list-v2.md",
        "diagnostics/T2.2-historical-qualification-adapter-v1-review.md",
        "diagnostics/T2.2-fixture-census-review-v2.md",
        RECOVERY_SELECTOR_PATH,
        "diagnostics/T2.2-fixture-resolution-v2.md",
        "diagnostics/T2.2-fixture-admission-v2.md",
        "diagnostics/T2.2-fixture-byte-manifest-v2.md",
        "diagnostics/T2.2-fixture-byte-review-v2.md",
        *RECOVERY_RAW_BLOBS,
    ]
    if r01_product_blocker_present:
        attempt_inputs.append(RECOVERY_R01_BLOCKER_PATH)
    if selector_result == "SLOTS_REQUIRED":
        attempt_inputs.append("materials/T2.2-v2/authorization.md")

    dependencies: dict[str, tuple[str, ...]] = {
        RECOVERY_ATTEMPT_MANIFEST_PATH: tuple(attempt_inputs),
        control_call: (
            RECOVERY_PACKAGE_MANIFEST_PATH,
            package_review,
            brief,
            "diagnostics/T2.2-contrast-packet-v1-01.md",
            "diagnostics/T2.2-contrast-packet-v1-02.md",
        ),
        control_index: (*control_answers, control_call, control_review),
        control_result: (
            *control_answers,
            control_index,
            contrast_key,
            control_call,
            control_review,
        ),
        diagnostic_call: (
            RECOVERY_PACKAGE_MANIFEST_PATH,
            package_review,
            control_result,
            control_postflight,
            brief,
            variant,
            *tuple(
                f"diagnostics/T2.2-contrast-packet-v1-{index:02d}.md"
                for index in range(1, 7)
            ),
        ),
        diagnostic_index: (
            *diagnostic_answers,
            diagnostic_call,
            diagnostic_review,
        ),
        contrast_result: (
            *control_answers,
            *diagnostic_answers,
            control_result,
            control_postflight,
            diagnostic_index,
            diagnostic_call,
            diagnostic_review,
            contrast_key,
        ),
        retest_call: (
            RECOVERY_PACKAGE_MANIFEST_PATH,
            package_review,
            contrast_result,
            contrast_postflight,
            brief,
            *tuple(
                f"diagnostics/T2.2-retest-packet-v2-{index:02d}.md"
                for index in range(1, 15)
            ),
        ),
        formal_index: (*formal_answers, retest_call, retest_review),
        "diagnostics/T2.2-judge-baseline-v2.md": (
            RECOVERY_ATTEMPT_MANIFEST_PATH,
            "diagnostics/T2.2-fixture-byte-manifest-v2.md",
            "diagnostics/T2.2-fixture-byte-review-v2.md",
            RECOVERY_PACKAGE_MANIFEST_PATH,
            package_review,
            control_call,
            control_review,
            *control_answers,
            control_index,
            control_result,
            control_postflight,
            diagnostic_call,
            diagnostic_review,
            *diagnostic_answers,
            diagnostic_index,
            contrast_result,
            contrast_postflight,
            retest_call,
            retest_review,
            *formal_answers,
            formal_index,
            "diagnostics/T2.2-scoring-key-v2.md",
        ),
    }
    for index, answer_path in enumerate(control_answers, start=1):
        packet_index = 1 if index <= 2 else 2
        dependencies[answer_path] = (
            control_call,
            control_review,
            brief,
            f"diagnostics/T2.2-contrast-packet-v1-{packet_index:02d}.md",
        )
    for index, answer_path in enumerate(diagnostic_answers, start=5):
        packet_index = {
            5: 1,
            6: 1,
            7: 2,
            8: 2,
            9: 3,
            10: 3,
            11: 4,
            12: 4,
            13: 5,
            14: 6,
        }[index]
        answer_brief = variant if index <= 8 else brief
        dependencies[answer_path] = (
            diagnostic_call,
            diagnostic_review,
            answer_brief,
            f"diagnostics/T2.2-contrast-packet-v1-{packet_index:02d}.md",
        )
    for index, answer_path in enumerate(formal_answers, start=1):
        dependencies[answer_path] = (
            retest_call,
            retest_review,
            brief,
            f"diagnostics/T2.2-retest-packet-v2-{index:02d}.md",
        )
    return dependencies


def _binding_line(prefix: str, relative_path: str, content: bytes) -> str:
    return (
        f"- {prefix}: `{relative_path}`"
        f" | byte-length: {len(content)}"
        f" | sha256: {hashlib.sha256(content).hexdigest()}"
    )


def _validate_hash_binding_set(
    relative_path: str,
    prefix: str,
    expected_inputs: tuple[str, ...],
    errors: list[str],
    project_root: Path,
) -> None:
    content = _regular_file_content_if_present(relative_path, errors, project_root)
    if content is None:
        return
    try:
        text = content.decode("utf-8")
    except UnicodeError as error:
        errors.append(f"chain artifact is not UTF-8: {relative_path}: {error}")
        return
    pattern = re.compile(
        rf"^- {re.escape(prefix)}: `([^`]+)`"
        rf" \| byte-length: ([0-9]+)"
        rf" \| sha256: ([0-9a-f]{{64}})$",
        flags=re.MULTILINE,
    )
    records = pattern.findall(text)
    raw_lines = [
        line for line in text.splitlines() if line.startswith(f"- {prefix}:")
    ]
    if len(raw_lines) != len(records):
        errors.append(f"malformed {prefix} line in {relative_path}")
    observed_paths = [path for path, _, _ in records]
    if len(observed_paths) != len(set(observed_paths)):
        errors.append(f"duplicate {prefix} path in {relative_path}")
    if set(observed_paths) != set(expected_inputs):
        errors.append(
            f"{prefix} closed set mismatch in {relative_path}: "
            f"missing {sorted(set(expected_inputs) - set(observed_paths))}, "
            f"unexpected {sorted(set(observed_paths) - set(expected_inputs))}"
        )
    for input_path, declared_length, declared_hash in records:
        if input_path not in set(expected_inputs):
            continue
        input_content = read_regular_bytes(
            project_root / input_path, errors, project_root
        )
        if input_content is None:
            continue
        if int(declared_length) != len(input_content):
            errors.append(
                f"{prefix} byte length mismatch: {relative_path} <- {input_path}"
            )
        if declared_hash != hashlib.sha256(input_content).hexdigest():
            errors.append(
                f"{prefix} hash mismatch: {relative_path} <- {input_path}"
            )


def _review_owner_task(subject_path: str) -> str:
    if subject_path in RECOVERY_RAW_BLOBS:
        return "T2.2-R03"
    policy = RECOVERY_ARTIFACT_POLICY.get(subject_path)
    if policy is None:
        raise RuntimeError(f"missing review subject owner: {subject_path}")
    return policy["owner"].split()[0].split("/")[0]


def _validate_direct_review_bindings(
    errors: list[str],
    project_root: Path,
    selector_result: str | None,
) -> None:
    pattern = re.compile(
        r"^- subject-binding: `([^`]+)`"
        r" \| owner-task: ([^|]+)"
        r" \| commit: ([0-9a-f]{40})"
        r" \| sha256: ([0-9a-f]{64})$",
        flags=re.MULTILINE,
    )
    for review_path, configured_subjects in RECOVERY_REVIEW_SUBJECTS.items():
        if review_path == RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture-review"
        ][0]:
            continue
        subjects = tuple(
            subject
            for subject in configured_subjects
            if not (
                subject == "materials/T2.2-v2/authorization.md"
                and selector_result == "NO_SLOTS"
            )
        )
        content = _regular_file_content_if_present(
            review_path, errors, project_root
        )
        if content is None:
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeError as error:
            errors.append(f"direct review is not UTF-8: {review_path}: {error}")
            continue
        if re.findall(
            r"^review-result: (PASS|FAIL)$", text, flags=re.MULTILINE
        ) != ["PASS"]:
            errors.append(f"direct review result must be one PASS: {review_path}")
        if re.findall(
            r"^subjects-unchanged-since-commit: (yes|no)$",
            text,
            flags=re.MULTILINE,
        ) != ["yes"]:
            errors.append(
                f"direct review unchanged gate must be one yes: {review_path}"
            )
        records = pattern.findall(text)
        raw_lines = [
            line
            for line in text.splitlines()
            if line.startswith("- subject-binding:")
        ]
        if len(raw_lines) != len(records):
            errors.append(f"malformed subject-binding line in {review_path}")
        observed_paths = [path for path, _, _, _ in records]
        if (
            len(observed_paths) != len(set(observed_paths))
            or set(observed_paths) != set(subjects)
        ):
            errors.append(f"direct review subject set mismatch: {review_path}")
        for subject_path, owner, commit, declared_hash in records:
            if subject_path not in set(subjects):
                continue
            expected_owner = _review_owner_task(subject_path)
            if owner.strip() != expected_owner:
                errors.append(
                    f"direct review owner mismatch: {review_path} <- {subject_path}"
                )
            subject = read_regular_bytes(
                project_root / subject_path, errors, project_root
            )
            if subject is None:
                continue
            actual_hash = hashlib.sha256(subject).hexdigest()
            if declared_hash != actual_hash:
                errors.append(
                    f"direct review current hash mismatch: "
                    f"{review_path} <- {subject_path}"
                )
            _validate_commit_identity(
                subject_path,
                commit,
                declared_hash,
                errors,
                project_root,
            )


def _selector_group_slots(
    project_root: Path, errors: list[str]
) -> dict[str, str]:
    content = _regular_file_content_if_present(
        RECOVERY_SELECTOR_PATH, errors, project_root
    )
    if content is None:
        return {}
    try:
        text = content.decode("utf-8")
    except UnicodeError:
        return {}
    records = re.findall(
        r"^selected-slot: ([^|]+) \| source-group: ([^|]+) \| request-id: .+$",
        text,
        flags=re.MULTILINE,
    )
    mapping: dict[str, str] = {}
    for path, group in records:
        normalized_path = path.strip()
        normalized_group = group.strip()
        if normalized_group not in {f"{index:02d}" for index in range(1, 15)}:
            errors.append(
                f"recovery selector selected-slot source-group invalid: "
                f"{normalized_group}"
            )
        elif normalized_group in mapping:
            errors.append(
                f"recovery selector selected-slot source-group duplicated: "
                f"{normalized_group}"
            )
        else:
            mapping[normalized_group] = normalized_path
    return mapping


def _validate_recovery_byte_manifest(
    errors: list[str], project_root: Path
) -> dict[str, tuple[str, str, str]]:
    manifest_path = "diagnostics/T2.2-fixture-byte-manifest-v2.md"
    content = _regular_file_content_if_present(
        manifest_path, errors, project_root
    )
    if content is None:
        return {}
    try:
        text = content.decode("utf-8")
    except UnicodeError as error:
        errors.append(f"recovery byte manifest is not UTF-8: {error}")
        return {}
    candidate_pattern = re.compile(
        r"^- candidate-byte-proof: ([0-9]{2})"
        r" \| selected-candidate-id: ([^|]+)"
        r" \| verdict-scope: ([^|]+)"
        r" \| source-path: `([^`]+)`"
        r" \| source-sha256: ([0-9a-f]{64})"
        r" \| range: ([0-9]+):([0-9]+)"
        r" \| fragment-sha256: ([0-9a-f]{64})"
        r" \| blob-path: `([^`]+)`"
        r" \| byte-length: ([0-9]+)"
        r" \| blob-sha256: ([0-9a-f]{64})"
        r" \| ends-with-lf: (yes|no)"
        r" \| raw-slot-foreign-key: (`[^`]+`|none)"
        r" \| copy-ready: (yes|no)$",
        flags=re.MULTILINE,
    )
    context_pattern = re.compile(
        r"^- context-byte-proof: ([0-9]{2})"
        r" \| source-path: `([^`]+)`"
        r" \| source-sha256: ([0-9a-f]{64})"
        r" \| spans: ([0-9:,a-f]+)"
        r" \| span-count: ([0-9]+)"
        r" \| blob-path: `([^`]+)`"
        r" \| byte-length: ([0-9]+)"
        r" \| blob-sha256: ([0-9a-f]{64})"
        r" \| ends-with-lf: (yes|no)"
        r" \| extraction-evidence: "
        r"(anchor=yes,dependencies=yes,nearest-only=yes,scope-stop=yes)"
        r" \| copy-ready: (yes|no)$",
        flags=re.MULTILINE,
    )
    candidate_records = candidate_pattern.findall(text)
    context_records = context_pattern.findall(text)
    candidate_lines = [
        line
        for line in text.splitlines()
        if line.startswith("- candidate-byte-proof:")
    ]
    context_lines = [
        line
        for line in text.splitlines()
        if line.startswith("- context-byte-proof:")
    ]
    if len(candidate_lines) != len(candidate_records):
        errors.append("malformed candidate-byte-proof line")
    if len(context_lines) != len(context_records):
        errors.append("malformed context-byte-proof line")
    expected_groups = {f"{index:02d}" for index in range(1, 15)}
    candidate_groups = [record[0] for record in candidate_records]
    context_groups = [record[0] for record in context_records]
    if (
        len(candidate_groups) != len(set(candidate_groups))
        or set(candidate_groups) != expected_groups
    ):
        errors.append("candidate byte proof group set must equal 01-14")
    if (
        len(context_groups) != len(set(context_groups))
        or set(context_groups) != expected_groups
    ):
        errors.append("context byte proof group set must equal 01-14")

    selected_by_group = _selector_group_slots(project_root, errors)
    item_metadata: dict[str, tuple[str, str, str]] = {}

    def source_bytes_for(
        group: str, source_path: str, declared_hash: str
    ) -> bytes | None:
        selected_path = selected_by_group.get(group)
        allowed = {
            (
                selected_path
                if selected_path is not None
                else RECOVERY_SOURCE_PATHS[int(group) - 1]
            )
        }
        if source_path not in allowed:
            errors.append(
                f"byte proof source path is not allowed for group {group}: "
                f"{source_path}"
            )
            return None
        source = read_regular_bytes(
            project_root / source_path, errors, project_root
        )
        if source is None:
            return None
        try:
            source.decode("utf-8")
        except UnicodeError as error:
            errors.append(
                f"byte proof source is not strict UTF-8: {source_path}: {error}"
            )
        if declared_hash != hashlib.sha256(source).hexdigest():
            errors.append(f"byte proof source hash mismatch: {source_path}")
        return source

    for record in candidate_records:
        (
            group,
            candidate_id,
            verdict_scope,
            source_path,
            source_hash,
            start_text,
            end_text,
            fragment_hash,
            blob_path,
            length_text,
            blob_hash,
            ends_lf,
            raw_slot_foreign_key,
            ready,
        ) = record
        candidate_id = candidate_id.strip()
        verdict_scope = verdict_scope.strip()
        normalized_foreign_key = (
            raw_slot_foreign_key[1:-1]
            if raw_slot_foreign_key.startswith("`")
            else raw_slot_foreign_key
        )
        item_metadata[group] = (
            candidate_id,
            verdict_scope,
            normalized_foreign_key,
        )
        if not candidate_id or not verdict_scope:
            errors.append(
                f"candidate ID/verdict scope missing for group {group}"
            )
        expected_foreign_key = selected_by_group.get(group, "none")
        if normalized_foreign_key != expected_foreign_key:
            errors.append(
                f"candidate raw-slot foreign key mismatch for group {group}"
            )
        expected_blob = (
            f"diagnostics/T2.2-fixture-bytes-v2/candidate-{group}.bin"
        )
        if blob_path != expected_blob:
            errors.append(f"candidate blob path mismatch for group {group}")
            continue
        source = source_bytes_for(group, source_path, source_hash)
        blob = read_regular_bytes(project_root / blob_path, errors, project_root)
        if source is None or blob is None:
            continue
        start, end = int(start_text), int(end_text)
        if not (0 <= start < end <= len(source)):
            errors.append(f"candidate range invalid for group {group}")
            continue
        rebuilt = source[start:end]
        rebuilt_hash = hashlib.sha256(rebuilt).hexdigest()
        if fragment_hash != rebuilt_hash or fragment_hash != blob_hash:
            errors.append(f"candidate fragment/blob hash mismatch for group {group}")
        if rebuilt != blob:
            errors.append(f"candidate source/blob bytes mismatch for group {group}")
        if int(length_text) != len(blob):
            errors.append(f"candidate blob length mismatch for group {group}")
        if blob_hash != hashlib.sha256(blob).hexdigest():
            errors.append(f"candidate actual blob hash mismatch for group {group}")
        if ends_lf != ("yes" if blob.endswith(b"\n") else "no"):
            errors.append(f"candidate ends-with-lf mismatch for group {group}")
        if ready != "yes" or not blob:
            errors.append(f"candidate blob not copy-ready/nonempty for group {group}")
        try:
            blob.decode("utf-8")
        except UnicodeError as error:
            errors.append(f"candidate blob is not strict UTF-8: {group}: {error}")

    span_pattern = re.compile(r"([0-9]+):([0-9]+):([0-9a-f]{64})")
    for record in context_records:
        (
            group,
            source_path,
            source_hash,
            spans_text,
            span_count_text,
            blob_path,
            length_text,
            blob_hash,
            ends_lf,
            extraction_evidence,
            ready,
        ) = record
        expected_blob = f"diagnostics/T2.2-fixture-bytes-v2/context-{group}.bin"
        if blob_path != expected_blob:
            errors.append(f"context blob path mismatch for group {group}")
            continue
        source = source_bytes_for(group, source_path, source_hash)
        blob = read_regular_bytes(project_root / blob_path, errors, project_root)
        spans = span_pattern.findall(spans_text)
        if ",".join(":".join(span) for span in spans) != spans_text:
            errors.append(f"context spans grammar mismatch for group {group}")
            continue
        if len(spans) != int(span_count_text) or not spans:
            errors.append(f"context span count mismatch for group {group}")
            continue
        if source is None or blob is None:
            continue
        rebuilt_parts: list[bytes] = []
        previous_end = -1
        valid_spans = True
        for start_text, end_text, span_hash in spans:
            start, end = int(start_text), int(end_text)
            if not (0 <= start < end <= len(source)) or start < previous_end:
                valid_spans = False
                break
            span = source[start:end]
            if span_hash != hashlib.sha256(span).hexdigest():
                errors.append(f"context span hash mismatch for group {group}")
            rebuilt_parts.append(span)
            previous_end = end
        if not valid_spans:
            errors.append(f"context spans invalid/overlapping for group {group}")
            continue
        rebuilt = b"".join(rebuilt_parts)
        if rebuilt != blob:
            errors.append(f"context source/blob bytes mismatch for group {group}")
        if int(length_text) != len(blob):
            errors.append(f"context blob length mismatch for group {group}")
        if blob_hash != hashlib.sha256(blob).hexdigest():
            errors.append(f"context actual blob hash mismatch for group {group}")
        if ends_lf != ("yes" if blob.endswith(b"\n") else "no"):
            errors.append(f"context ends-with-lf mismatch for group {group}")
        if ready != "yes" or not blob:
            errors.append(f"context blob not copy-ready/nonempty for group {group}")
        if extraction_evidence != (
            "anchor=yes,dependencies=yes,nearest-only=yes,scope-stop=yes"
        ):
            errors.append(
                f"context extraction evidence incomplete for group {group}"
            )
        try:
            blob.decode("utf-8")
        except UnicodeError as error:
            errors.append(f"context blob is not strict UTF-8: {group}: {error}")
    candidate_ids = [metadata[0] for metadata in item_metadata.values()]
    if len(candidate_ids) != len(set(candidate_ids)):
        errors.append("byte manifest selected candidate IDs must be unique")
    return item_metadata


def _parse_packet_byte_blocks(
    packet_path: str,
    content: bytes,
    errors: list[str],
) -> list[tuple[str, bytes, int, str]]:
    blocks: list[tuple[str, bytes, int, str]] = []
    cursor = 0
    header_pattern = re.compile(
        rb"BYTE-BLOCK: (CANDIDATE|SOURCE-CONTEXT)\n"
        rb"PAYLOAD-LENGTH: ([0-9]+)\n"
        rb"PAYLOAD-SHA256: ([0-9a-f]{64})\n"
        rb"PAYLOAD-BEGIN\n"
    )
    while True:
        marker = content.find(b"BYTE-BLOCK:", cursor)
        if marker < 0:
            break
        if marker > 0 and content[marker - 1 : marker] != b"\n":
            errors.append(f"packet byte block is not line-aligned: {packet_path}")
            return blocks
        match = header_pattern.match(content, marker)
        if match is None:
            errors.append(f"packet byte block header malformed: {packet_path}")
            return blocks
        kind = match.group(1).decode("ascii")
        length = int(match.group(2))
        declared_hash = match.group(3).decode("ascii")
        payload_start = match.end()
        payload_end = payload_start + length
        if content[payload_end : payload_end + len(b"\nPAYLOAD-END\n")] != (
            b"\nPAYLOAD-END\n"
        ):
            errors.append(f"packet byte block length boundary mismatch: {packet_path}")
            return blocks
        payload = content[payload_start:payload_end]
        if hashlib.sha256(payload).hexdigest() != declared_hash:
            errors.append(f"packet payload header hash mismatch: {packet_path}")
        blocks.append((kind, payload, length, declared_hash))
        cursor = payload_end + len(b"\nPAYLOAD-END\n")
    return blocks


def _validate_attempt_mapping(
    errors: list[str],
    project_root: Path,
    byte_items: dict[str, tuple[str, str, str]],
) -> tuple[dict[str, tuple[str, str, str, str]], dict[str, str]]:
    content = _regular_file_content_if_present(
        RECOVERY_ATTEMPT_MANIFEST_PATH, errors, project_root
    )
    if content is None:
        return {}, {}
    try:
        text = content.decode("utf-8")
    except UnicodeError:
        return {}, {}
    if re.findall(
        r"^attempt-salt-hex: ([0-9a-f]{64})$", text, flags=re.MULTILINE
    ) == []:
        errors.append("attempt manifest requires one 32-byte lowercase hex salt")
    elif len(
        re.findall(
            r"^attempt-salt-hex: ([0-9a-f]{64})$",
            text,
            flags=re.MULTILINE,
        )
    ) != 1:
        errors.append("attempt manifest salt must occur exactly once")
    item_pattern = re.compile(
        r"^- qualification-item: ([0-9]{2})"
        r" \| candidate-id: ([^|]+)"
        r" \| q-id: ([^|]+)"
        r" \| candidate-blob-path: `([^`]+)`"
        r" \| context-blob-path: `([^`]+)`"
        r" \| formal-packet-path: `([^`]+)`$",
        flags=re.MULTILINE,
    )
    records = item_pattern.findall(text)
    raw_item_lines = [
        line
        for line in text.splitlines()
        if line.startswith("- qualification-item:")
    ]
    if len(raw_item_lines) != len(records):
        errors.append("malformed attempt qualification-item line")
    expected_groups = {f"{index:02d}" for index in range(1, 15)}
    groups = [record[0] for record in records]
    if len(groups) != len(set(groups)) or set(groups) != expected_groups:
        errors.append("attempt qualification item group set must equal 01-14")
    candidate_ids = [record[1].strip() for record in records]
    q_ids = [record[2].strip() for record in records]
    if (
        len(candidate_ids) != len(set(candidate_ids))
        or any(not value for value in candidate_ids)
    ):
        errors.append("attempt selected candidate IDs must be 14 unique values")
    if len(q_ids) != len(set(q_ids)) or any(not value for value in q_ids):
        errors.append("attempt Q IDs must be 14 unique values")
    mapping: dict[str, tuple[str, str, str, str]] = {}
    formal_paths: list[str] = []
    for group, candidate_id, q_id, candidate_path, context_path, packet_path in records:
        byte_item = byte_items.get(group)
        if byte_item is None or candidate_id.strip() != byte_item[0]:
            errors.append(
                f"attempt candidate ID does not match byte manifest for group {group}"
            )
        if candidate_path != (
            f"diagnostics/T2.2-fixture-bytes-v2/candidate-{group}.bin"
        ):
            errors.append(f"attempt candidate blob path mismatch for group {group}")
        if context_path != (
            f"diagnostics/T2.2-fixture-bytes-v2/context-{group}.bin"
        ):
            errors.append(f"attempt context blob path mismatch for group {group}")
        formal_paths.append(packet_path)
        mapping[group] = (
            candidate_path,
            context_path,
            packet_path,
            q_id.strip(),
        )
    expected_formal_paths = {
        f"diagnostics/T2.2-retest-packet-v2-{index:02d}.md"
        for index in range(1, 15)
    }
    if set(formal_paths) != expected_formal_paths or len(formal_paths) != len(
        set(formal_paths)
    ):
        errors.append("attempt formal packet path set must equal the 14 literals")

    sentinel_records = re.findall(
        r"^- sentinel: (P|N1) \| source-group: ([0-9]{2})$",
        text,
        flags=re.MULTILINE,
    )
    sentinels = {name: group for name, group in sentinel_records}
    if (
        len(sentinel_records) != 2
        or set(sentinels) != {"P", "N1"}
        or len(set(sentinels.values())) != 2
        or any(group not in mapping for group in sentinels.values())
    ):
        errors.append("attempt sentinels must bind distinct P and N1 source groups")

    m14_pattern = re.compile(
        r"^- m14-call: ([0-9]{2})"
        r" \| arm: (C|B|E|G)"
        r" \| packet-path: `diagnostics/T2\.2-contrast-packet-v1-([0-9]{2})\.md`"
        r" \| brief-path: `([^`]+)`"
        r" \| object-order: ([A-Za-z0-9,-]+)$",
        flags=re.MULTILINE,
    )
    m14_records = m14_pattern.findall(text)
    m14_lines = [
        line for line in text.splitlines() if line.startswith("- m14-call:")
    ]
    if len(m14_lines) != len(m14_records):
        errors.append("malformed attempt M14 call line")
    normalized_m14: list[tuple[str, str, str, str, str]] = []
    full_brief = "diagnostics/T2.2-judge-brief-v2.md"
    variant_brief = "diagnostics/T2.2-judge-brief-variant-v1-02.md"
    for answer, arm, packet, brief_path, object_order in m14_records:
        if brief_path == full_brief:
            brief_kind = "full"
        elif brief_path == variant_brief:
            brief_kind = "variant"
        else:
            brief_kind = "invalid"
        normalized_m14.append(
            (answer, arm, packet, brief_kind, object_order)
        )
    if normalized_m14 != list(RECOVERY_M14_CALLS):
        errors.append("attempt M14 call mapping/order mismatch")

    future_paths = re.findall(
        r"^- future-path: `([^`]+)`$", text, flags=re.MULTILINE
    )
    if (
        len(future_paths) != len(set(future_paths))
        or set(future_paths) != set(RECOVERY_ATTEMPT_FUTURE_PATHS)
    ):
        errors.append("attempt future path closed set mismatch")
    return mapping, sentinels


def _validate_recovery_package(
    errors: list[str],
    project_root: Path,
    attempt_mapping: dict[str, tuple[str, str, str, str]],
    sentinels: dict[str, str],
) -> None:
    _validate_hash_binding_set(
        RECOVERY_PACKAGE_MANIFEST_PATH,
        "package-binding",
        RECOVERY_PACKAGE_MEMBER_PATHS,
        errors,
        project_root,
    )
    manifest_content = _regular_file_content_if_present(
        RECOVERY_PACKAGE_MANIFEST_PATH, errors, project_root
    )
    if manifest_content is None:
        return
    try:
        manifest = manifest_content.decode("utf-8")
    except UnicodeError as error:
        errors.append(f"package manifest is not UTF-8: {error}")
        return
    copy_pattern = re.compile(
        r"^- payload-copy-proof: `([^`]+)`"
        r" \| block-index: ([0-9]+)"
        r" \| input-blob-path: `([^`]+)`"
        r" \| input-blob-length: ([0-9]+)"
        r" \| input-blob-sha256: ([0-9a-f]{64})"
        r" \| embedded-payload-length: ([0-9]+)"
        r" \| embedded-payload-sha256: ([0-9a-f]{64})"
        r" \| copy-equality: (PASS|FAIL)$",
        flags=re.MULTILINE,
    )
    omission_pattern = re.compile(
        r"^- payload-omission-proof: `([^`]+)`"
        r" \| block-index: ([0-9]+)"
        r" \| canonical-blob-path: `([^`]+)`"
        r" \| canonical-blob-sha256: ([0-9a-f]{64})"
        r" \| context-omitted-by-experiment: (yes|no)$",
        flags=re.MULTILINE,
    )
    copy_records = copy_pattern.findall(manifest)
    omission_records = omission_pattern.findall(manifest)
    copy_lines = [
        line
        for line in manifest.splitlines()
        if line.startswith("- payload-copy-proof:")
    ]
    omission_lines = [
        line
        for line in manifest.splitlines()
        if line.startswith("- payload-omission-proof:")
    ]
    if len(copy_lines) != len(copy_records):
        errors.append("malformed package payload-copy-proof line")
    if len(omission_lines) != len(omission_records):
        errors.append("malformed package payload-omission-proof line")
    copy_by_key = {
        (path, int(index)): (
            blob_path,
            int(blob_length),
            blob_hash,
            int(payload_length),
            payload_hash,
            equality,
        )
        for (
            path,
            index,
            blob_path,
            blob_length,
            blob_hash,
            payload_length,
            payload_hash,
            equality,
        ) in copy_records
    }
    omission_by_key = {
        (path, int(index)): (blob_path, blob_hash, omitted)
        for path, index, blob_path, blob_hash, omitted in omission_records
    }
    if len(copy_by_key) != len(copy_records):
        errors.append("duplicate package payload-copy-proof key")
    if len(omission_by_key) != len(omission_records):
        errors.append("duplicate package payload-omission-proof key")
    if set(copy_by_key) & set(omission_by_key):
        errors.append("package block cannot have both copy and omission proof")

    parsed: dict[str, list[tuple[str, bytes, int, str]]] = {}
    expected_keys: set[tuple[str, int]] = set()
    for packet_path in RECOVERY_PACKET_PATHS:
        packet = read_regular_bytes(
            project_root / packet_path, errors, project_root
        )
        if packet is None:
            continue
        try:
            packet.decode("utf-8")
        except UnicodeError as error:
            errors.append(f"package packet is not strict UTF-8: {packet_path}: {error}")
        blocks = _parse_packet_byte_blocks(packet_path, packet, errors)
        parsed[packet_path] = blocks
        expected_keys.update(
            (packet_path, index) for index in range(1, len(blocks) + 1)
        )
        for index, (kind, payload, embedded_length, embedded_hash) in enumerate(
            blocks, start=1
        ):
            key = (packet_path, index)
            if key in copy_by_key:
                (
                    blob_path,
                    blob_length,
                    blob_hash,
                    declared_payload_length,
                    declared_payload_hash,
                    equality,
                ) = copy_by_key[key]
                if blob_path not in set(RECOVERY_RAW_BLOBS):
                    errors.append(f"package copy proof blob path invalid: {key}")
                    continue
                if kind == "CANDIDATE" and "/candidate-" not in blob_path:
                    errors.append(f"candidate block bound to non-candidate blob: {key}")
                if kind == "SOURCE-CONTEXT" and "/context-" not in blob_path:
                    errors.append(f"context block bound to non-context blob: {key}")
                blob = read_regular_bytes(
                    project_root / blob_path, errors, project_root
                )
                if blob is None:
                    continue
                actual_hash = hashlib.sha256(blob).hexdigest()
                if (
                    blob_length != len(blob)
                    or blob_hash != actual_hash
                    or declared_payload_length != embedded_length
                    or declared_payload_hash != embedded_hash
                    or embedded_length != len(payload)
                    or embedded_hash != hashlib.sha256(payload).hexdigest()
                    or payload != blob
                    or equality != "PASS"
                ):
                    errors.append(f"package payload copy proof mismatch: {key}")
            elif key in omission_by_key:
                blob_path, blob_hash, omitted = omission_by_key[key]
                allowed_packet = packet_path in {
                    "diagnostics/T2.2-contrast-packet-v1-03.md",
                    "diagnostics/T2.2-contrast-packet-v1-04.md",
                }
                blob = (
                    read_regular_bytes(
                        project_root / blob_path, errors, project_root
                    )
                    if blob_path in set(RECOVERY_RAW_BLOBS)
                    and "/context-" in blob_path
                    else None
                )
                if (
                    kind != "SOURCE-CONTEXT"
                    or not allowed_packet
                    or payload
                    or embedded_length != 0
                    or embedded_hash != hashlib.sha256(b"").hexdigest()
                    or blob is None
                    or blob_hash != hashlib.sha256(blob).hexdigest()
                    or omitted != "yes"
                ):
                    errors.append(f"package experimental omission proof mismatch: {key}")
            else:
                errors.append(f"package byte block has no copy proof: {key}")
    observed_keys = set(copy_by_key) | set(omission_by_key)
    if observed_keys != expected_keys:
        errors.append(
            "package payload proof key set mismatch: "
            f"missing {sorted(expected_keys - observed_keys)}, "
            f"unexpected {sorted(observed_keys - expected_keys)}"
        )

    blind = parsed.get("diagnostics/T2.2-blind-packet-v2.md", [])
    if len(blind) != 28:
        errors.append("canonical blind packet must contain exactly 28 byte blocks")
    else:
        blind_blob_paths = [
            copy_by_key[(RECOVERY_PACKET_PATHS[0], index)][0]
            for index in range(1, 29)
            if (RECOVERY_PACKET_PATHS[0], index) in copy_by_key
        ]
        if set(blind_blob_paths) != set(RECOVERY_RAW_BLOBS):
            errors.append("canonical blind packet must copy the exact 28 raw blobs")
    for index in range(1, 15):
        packet_path = f"diagnostics/T2.2-retest-packet-v2-{index:02d}.md"
        blocks = parsed.get(packet_path, [])
        if len(blocks) != 2 or [block[0] for block in blocks] != [
            "CANDIDATE",
            "SOURCE-CONTEXT",
        ]:
            errors.append(f"formal retest packet block shape mismatch: {packet_path}")
    for group, (candidate_path, context_path, packet_path, _) in attempt_mapping.items():
        proof_paths = [
            copy_by_key.get((packet_path, 1), (None,))[0],
            copy_by_key.get((packet_path, 2), (None,))[0],
        ]
        if proof_paths != [candidate_path, context_path]:
            errors.append(
                f"formal packet does not match attempt mapping for group {group}"
            )
    contrast_counts = {1: 2, 2: 2, 3: 2, 4: 2, 5: 4, 6: 4}
    for index, count in contrast_counts.items():
        packet_path = f"diagnostics/T2.2-contrast-packet-v1-{index:02d}.md"
        if len(parsed.get(packet_path, [])) != count:
            errors.append(f"contrast packet block count mismatch: {packet_path}")
    if set(sentinels) == {"P", "N1"} and all(
        group in attempt_mapping for group in sentinels.values()
    ):
        p_candidate, p_context, _, _ = attempt_mapping[sentinels["P"]]
        n_candidate, n_context, _, _ = attempt_mapping[sentinels["N1"]]
        expected_contrast_paths = {
            1: (p_candidate, p_context),
            2: (n_candidate, n_context),
            3: (p_candidate, None),
            4: (n_candidate, None),
            5: (p_candidate, p_context, n_candidate, n_context),
            6: (n_candidate, n_context, p_candidate, p_context),
        }
        for index, expected_paths in expected_contrast_paths.items():
            packet_path = (
                f"diagnostics/T2.2-contrast-packet-v1-{index:02d}.md"
            )
            observed_paths: list[str | None] = []
            for block_index in range(1, len(expected_paths) + 1):
                key = (packet_path, block_index)
                if key in copy_by_key:
                    observed_paths.append(copy_by_key[key][0])
                elif key in omission_by_key:
                    observed_paths.append(None)
                else:
                    observed_paths.append("missing")
            if tuple(observed_paths) != expected_paths:
                errors.append(
                    f"contrast packet does not match attempt sentinel mapping: "
                    f"{packet_path}"
                )


RECOVERY_ATTEMPT_FIXED_IDENTITIES = {
    RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture"][0]: (
        RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture"][1],
        RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture"][2],
        "ACTIVE",
    ),
    RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture-review"][0]: (
        RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture-review"][1],
        RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture-review"][2],
        "PASS",
    ),
    "diagnostics/T2.2-recovery-architecture-v2.md": (
        "037f33b0893208a232efa4aaeb23866885ec5fd0",
        "1154110c3a3bff65e4dc2ceb8244e724f0da60924c4e32ba4afa413600a2043a",
        "SUPERSEDED",
    ),
    "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md": (
        "4bc9feca20f41e9c41158885cad41683f4d227b2",
        "9d2c80e23e30018c4dc4283c56315ab2df2198344b98dda91cebae6755f92e13",
        "FAIL",
    ),
    "diagnostics/T2.2-judge-baseline.md": (
        "909531c42336a0fd6f22a39f7aaba7b3c9c1e3dd",
        "830f0758439ee72d549efe27296a444ccb9769c92c1298399dd9b5bebce0d4af",
        "FAIL",
    ),
    "taskcards/T2.2-BLOCKER.md": (
        "909531c42336a0fd6f22a39f7aaba7b3c9c1e3dd",
        "84c7a0dede0797c5667228398cc4be1b8a945d8a871dab7058737778bba1684b",
        "BLOCKED",
    ),
}


def _validate_attempt_fixed_identities(
    errors: list[str],
    project_root: Path,
    identities: dict[str, tuple[str, str, str]],
) -> None:
    content = _regular_file_content_if_present(
        RECOVERY_ATTEMPT_MANIFEST_PATH, errors, project_root
    )
    if content is None:
        return
    try:
        text = content.decode("utf-8")
    except UnicodeError:
        return
    pattern = re.compile(
        r"^- fixed-identity: `([^`]+)`"
        r" \| commit: ([0-9a-f]{40})"
        r" \| sha256: ([0-9a-f]{64})"
        r" \| result: ([A-Z-]+)$",
        flags=re.MULTILINE,
    )
    records = pattern.findall(text)
    raw_lines = [
        line for line in text.splitlines() if line.startswith("- fixed-identity:")
    ]
    if len(raw_lines) != len(records):
        errors.append("malformed attempt fixed-identity line")
    observed = [path for path, _, _, _ in records]
    if len(observed) != len(set(observed)) or set(observed) != set(identities):
        errors.append("attempt fixed-identity closed set mismatch")
    for path, commit, declared_hash, result in records:
        expected = identities.get(path)
        if expected is None:
            continue
        if (commit, declared_hash, result) != expected:
            errors.append(f"attempt fixed identity mismatch: {path}")
        content_bytes = read_regular_bytes(
            project_root / path, errors, project_root
        )
        if content_bytes is not None and hashlib.sha256(
            content_bytes
        ).hexdigest() != declared_hash:
            errors.append(f"attempt fixed identity current hash mismatch: {path}")
        _validate_commit_identity(
            path, commit, declared_hash, errors, project_root
        )


def _validate_m2_chain(
    errors: list[str],
    project_root: Path,
    selector_result: str | None,
    attempt_identities: dict[str, tuple[str, str, str]] | None = None,
    r01_product_blocker_present: bool | None = None,
) -> None:
    if r01_product_blocker_present is None:
        r01_product_blocker_present = _path_entry_exists(
            project_root / RECOVERY_R01_BLOCKER_PATH, errors
        )
    result_requirements = (
        (
            RECOVERY_ATTEMPT_MANIFEST_PATH,
            "attempt-id",
            "T2.2-QV2-A01",
        ),
        (
            "diagnostics/T2.2-contrast-control-results-v1.md",
            "control-result",
            "PASS",
        ),
        (
            "diagnostics/T2.2-judge-baseline-v2.md",
            "qualification-result",
            "PASS",
        ),
    )
    for relative_path, key, expected in result_requirements:
        content = _regular_file_content_if_present(
            relative_path, errors, project_root
        )
        if content is None:
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeError:
            continue
        if re.findall(
            rf"^{re.escape(key)}: (.+)$", text, flags=re.MULTILINE
        ) != [expected]:
            errors.append(
                f"M2 chain result field mismatch: {relative_path}: {key}"
            )
    byte_items = _validate_recovery_byte_manifest(errors, project_root)
    _validate_direct_review_bindings(errors, project_root, selector_result)
    attempt_mapping, sentinels = _validate_attempt_mapping(
        errors, project_root, byte_items
    )
    for consumer, inputs in _recovery_chain_dependencies(
        selector_result,
        r01_product_blocker_present=r01_product_blocker_present,
    ).items():
        _validate_hash_binding_set(
            consumer, "input-binding", inputs, errors, project_root
        )
    _validate_recovery_package(
        errors, project_root, attempt_mapping, sentinels
    )
    _validate_attempt_fixed_identities(
        errors,
        project_root,
        (
            RECOVERY_ATTEMPT_FIXED_IDENTITIES
            if attempt_identities is None
            else attempt_identities
        ),
    )


def _receipt_field_values(
    text: str, required_keys: tuple[str, ...], errors: list[str]
) -> dict[str, str]:
    header = RECOVERY_EXACT_HEADER.format(status="frozen", scope="long-term")
    body = text[len(header) :] if text.startswith(header) else text
    field_lines = [line for line in body.splitlines() if line]
    observed_keys: list[str] = []
    malformed_lines: list[str] = []
    for line in field_lines:
        match = re.fullmatch(r"([^:\s][^:]*): (.+)", line)
        if match is None:
            malformed_lines.append(line)
        else:
            observed_keys.append(match.group(1))
    if (
        malformed_lines
        or len(observed_keys) != len(set(observed_keys))
        or set(observed_keys) != set(required_keys)
    ):
        errors.append(
            "M2 receipt key set must exactly equal v3 section 13.2: "
            f"missing {sorted(set(required_keys) - set(observed_keys))}, "
            f"unexpected {sorted(set(observed_keys) - set(required_keys))}, "
            f"duplicates {sorted(key for key in set(observed_keys) if observed_keys.count(key) > 1)}, "
            f"malformed {malformed_lines}"
        )
    values: dict[str, str] = {}
    for key in required_keys:
        matches = re.findall(
            rf"^{re.escape(key)}: (.+)$", body, flags=re.MULTILINE
        )
        if len(matches) != 1:
            errors.append(f"M2 receipt field must occur exactly once: {key}")
        else:
            values[key] = matches[0]
    return values


def _v3_receipt_schema_keys() -> tuple[str, ...]:
    architecture = (
        ROOT / RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture"][0]
    ).read_text(encoding="utf-8")
    section_match = re.search(
        r"^### 13\.2 M2 receipt 必填字段\n(?P<section>.*?)"
        r"^### 13\.3 M2 必须不存在的条件$",
        architecture,
        flags=re.MULTILINE | re.DOTALL,
    )
    if section_match is None:
        raise AssertionError("cannot locate v3 section 13.2 receipt schema")
    block_match = re.search(
        r"```text\n(?P<schema>.*?)```",
        section_match.group("section"),
        flags=re.DOTALL,
    )
    if block_match is None:
        raise AssertionError("cannot locate v3 section 13.2 receipt code block")
    keys = tuple(
        line.split(":", 1)[0]
        for line in block_match.group("schema").splitlines()
        if line.strip()
    )
    if any(
        not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", key)
        for key in keys
    ):
        raise AssertionError("invalid key in v3 section 13.2 receipt schema")
    return keys


def _validate_m2_receipt(
    errors: list[str],
    project_root: Path,
    formal_cards: set[str],
    raw_blobs: set[str],
    selector_result: str | None,
    attempt_identities: dict[str, tuple[str, str, str]] | None = None,
    fixed_values_override: dict[str, str] | None = None,
) -> None:
    receipt_content = _regular_file_content_if_present(
        M2_RECEIPT_PATH, errors, project_root
    )
    if receipt_content is None:
        return
    expected_header = RECOVERY_EXACT_HEADER.format(
        status="frozen", scope="long-term"
    ).encode("utf-8")
    if not receipt_content.startswith(expected_header):
        errors.append("M2 receipt must start with exact frozen/long-term header")
    try:
        receipt = receipt_content.decode("utf-8")
    except UnicodeError as error:
        errors.append(f"M2 receipt is not UTF-8: {error}")
        return
    if selector_result == "BLOCKED":
        errors.append("M2 receipt forbidden while recovery selector is BLOCKED")
    elif selector_result not in {"NO_SLOTS", "SLOTS_REQUIRED"}:
        errors.append("M2 receipt requires one valid non-blocked recovery selector")

    fields = _receipt_field_values(receipt, M2_RECEIPT_REQUIRED_KEYS, errors)

    fixed_values = {
        "t2.2-active-architecture-path": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture"
        ][0],
        "t2.2-active-architecture-sha256": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture"
        ][2],
        "t2.2-active-architecture-review-path": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture-review"
        ][0],
        "t2.2-active-architecture-review-sha256": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture-review"
        ][2],
        "t2.2-active-attempt-id": "T2.2-QV2-A01",
        "t2.2-active-attempt-manifest-path": (
            "diagnostics/T2.2-qualification-attempt-manifest-v2.md"
        ),
        "t2.2-active-baseline-path": "diagnostics/T2.2-judge-baseline-v2.md",
        "t2.2-active-postflight-review-path": (
            "diagnostics/T2.2-postflight-review-v2.md"
        ),
        "t2.2-active-result": "PASS",
        "t2.2-history-v1-baseline-path": "diagnostics/T2.2-judge-baseline.md",
        "t2.2-history-v1-baseline-sha256": (
            "830f0758439ee72d549efe27296a444ccb9769c92c1298399dd9b5bebce0d4af"
        ),
        "t2.2-history-v1-baseline-result": "FAIL",
        "t2.2-history-v1-blocker-path": "taskcards/T2.2-BLOCKER.md",
        "t2.2-history-v1-blocker-sha256": (
            "84c7a0dede0797c5667228398cc4be1b8a945d8a871dab7058737778bba1684b"
        ),
        "t2.2-history-v2-architecture-path": (
            "diagnostics/T2.2-recovery-architecture-v2.md"
        ),
        "t2.2-history-v2-architecture-sha256": (
            "1154110c3a3bff65e4dc2ceb8244e724f0da60924c4e32ba4afa413600a2043a"
        ),
        "t2.2-history-v2-review-path": (
            "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md"
        ),
        "t2.2-history-v2-review-sha256": (
            "9d2c80e23e30018c4dc4283c56315ab2df2198344b98dda91cebae6755f92e13"
        ),
        "t2.2-history-v2-review-result": "FAIL",
    }
    if fixed_values_override is not None:
        if set(fixed_values_override) != set(fixed_values):
            errors.append("M2 receipt test fixed-value override key set mismatch")
        else:
            fixed_values = fixed_values_override
    for key, expected in fixed_values.items():
        if fields.get(key) != expected:
            errors.append(f"M2 receipt fixed field mismatch: {key}")

    hash_bindings = {
        "m1-freeze-receipt-sha256": "contracts/M1-freeze-receipt.md",
        "t1.8-independent-acceptance-sha256": (
            "contracts/T1.8-independent-acceptance.md"
        ),
        "t2.1-r01-r08-sha256": "diagnostics/T2.1-r01-r08.md",
        "t2.3-seed-lenses-v2-sha256": "lenses/T2.3-seed-lenses-v2.md",
        "t2.2-active-attempt-manifest-sha256": (
            "diagnostics/T2.2-qualification-attempt-manifest-v2.md"
        ),
        "t2.2-active-baseline-sha256": "diagnostics/T2.2-judge-baseline-v2.md",
        "t2.2-active-postflight-review-sha256": (
            "diagnostics/T2.2-postflight-review-v2.md"
        ),
    }
    for key, relative_path in hash_bindings.items():
        content = read_regular_bytes(
            project_root / relative_path, errors, project_root
        )
        if content is not None and fields.get(key) != hashlib.sha256(
            content
        ).hexdigest():
            errors.append(f"M2 receipt actual hash mismatch: {key}")

    expected_cards = {f"{task_id}.md" for task_id in RECOVERY_TASK_IDS}
    if formal_cards != expected_cards:
        errors.append("M2 receipt forbidden before all 21 recovery cards are registered")
    r01_product_blocker_present = _validate_recovery_blockers_for_m2(
        errors, project_root
    )
    if raw_blobs != set(RECOVERY_RAW_BLOBS):
        errors.append("M2 receipt requires the exact 28 raw blobs")

    for relative_path in RECOVERY_ARTIFACT_POLICY:
        if (
            relative_path == "materials/T2.2-v2/authorization.md"
            and selector_result == "NO_SLOTS"
        ):
            continue
        if _regular_file_content_if_present(
            relative_path, errors, project_root
        ) is None:
            errors.append(
                f"M2 receipt exists without required recovery artifact: {relative_path}"
            )

    _validate_m2_chain(
        errors,
        project_root,
        selector_result,
        attempt_identities=attempt_identities,
        r01_product_blocker_present=r01_product_blocker_present,
    )

    attempt = _regular_file_content_if_present(
        "diagnostics/T2.2-qualification-attempt-manifest-v2.md",
        errors,
        project_root,
    )
    if attempt is not None and b"attempt-id: T2.2-QV2-A01" not in attempt:
        errors.append("active attempt manifest ID mismatch")
    baseline = _regular_file_content_if_present(
        "diagnostics/T2.2-judge-baseline-v2.md", errors, project_root
    )
    if baseline is not None and not re.search(
        rb"^qualification-result: PASS$", baseline, flags=re.MULTILINE
    ):
        errors.append("active v2 baseline must record qualification-result: PASS")


def validate_recovery_control(
    errors: list[str], project_root: Path = ROOT
) -> None:
    _validate_recovery_policy_invariants(errors)
    _validate_recovery_roadmap(errors, project_root)
    _validate_recovery_document_wiring(errors, project_root)

    for relative_path, commit, expected_hash in (
        RECOVERY_ARCHITECTURE_IDENTITIES.values()
    ):
        content = _validate_fixed_file_hash(
            relative_path, expected_hash, errors, project_root
        )
        _validate_commit_identity(
            relative_path, commit, expected_hash, errors, project_root
        )
        if content is not None:
            if relative_path.endswith("-preflight-review.md") and (
                "最终结论：`PASS`" not in content.decode("utf-8", errors="replace")
            ):
                errors.append("active recovery architecture review result is not PASS")
            if relative_path.endswith("-quality-audit.md") and (
                "质量结论：`CONFIRMED_PASS`"
                not in content.decode("utf-8", errors="replace")
            ):
                errors.append("recovery quality audit result is not CONFIRMED_PASS")

    _validate_fixed_file_hash(
        "diagnostics/T2.2-judge-baseline.md",
        "830f0758439ee72d549efe27296a444ccb9769c92c1298399dd9b5bebce0d4af",
        errors,
        project_root,
    )
    _validate_fixed_file_hash(
        "taskcards/T2.2-BLOCKER.md",
        "84c7a0dede0797c5667228398cc4be1b8a945d8a871dab7058737778bba1684b",
        errors,
        project_root,
    )
    _validate_fixed_file_hash(
        "diagnostics/T2.2-recovery-architecture-v2.md",
        "1154110c3a3bff65e4dc2ceb8244e724f0da60924c4e32ba4afa413600a2043a",
        errors,
        project_root,
    )
    _validate_commit_identity(
        "diagnostics/T2.2-recovery-architecture-v2.md",
        "037f33b0893208a232efa4aaeb23866885ec5fd0",
        "1154110c3a3bff65e4dc2ceb8244e724f0da60924c4e32ba4afa413600a2043a",
        errors,
        project_root,
    )
    _validate_fixed_file_hash(
        "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md",
        "9d2c80e23e30018c4dc4283c56315ab2df2198344b98dda91cebae6755f92e13",
        errors,
        project_root,
    )
    _validate_commit_identity(
        "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md",
        "4bc9feca20f41e9c41158885cad41683f4d227b2",
        "9d2c80e23e30018c4dc4283c56315ab2df2198344b98dda91cebae6755f92e13",
        errors,
        project_root,
    )

    formal_cards = _recovery_taskcard_names(errors, project_root)
    _, selector_result = _validate_recovery_selector(errors, project_root)
    raw_blobs = _validate_recovery_raw_blobs(errors, project_root)
    _validate_recovery_artifacts(errors, project_root)
    _validate_m2_receipt(
        errors, project_root, formal_cards, raw_blobs, selector_result
    )


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
    if not glossary_text.startswith(GLOSSARY_STATUS_HEADERS):
        errors.append(
            "contracts/GLOSSARY.md must have draft-or-frozen/long-term status header"
        )

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


def _run_recovery_only(project_root: Path) -> int:
    errors: list[str] = []
    validate_recovery_control(errors, project_root)
    if errors:
        print("T2.2 recovery control validation FAILED")
        print("\n".join(errors))
        return 1
    print("T2.2 recovery control validation PASSED")
    return 0


def _synthetic_recovery_card_text(task_id: str) -> str:
    mode = (
        "composite"
        if task_id in RECOVERY_COMPOSITE_TASK_IDS
        else "single-session"
    )
    lines = [
        f"## {index}. {heading}"
        for index, heading in enumerate(TASK_SECTION_NAMES, start=1)
    ]
    lines[0] += f"\n\n`{task_id}`：synthetic"
    lines[1] += "\n\nsynthetic"
    lines[2] += (
        "\n\nsynthetic\n"
        + "\n".join(sorted(_expected_card_read_path_lines(task_id)))
    )
    if task_id in {"T2.2-R03", "T2.2-R04", "T2.2-R05", "T2.2-R06"}:
        runtime_open = (
            "forbidden" if task_id == "T2.2-R05" else "selected-only"
        )
        lines[2] += "\n" + "\n".join(
            f"- material-slot-policy: `{path}` | runtime-open: {runtime_open}"
            for path in RECOVERY_MATERIAL_SLOTS
        )
    lines[3] += (
        f"\n\n- recovery-execution-mode: {mode}\n"
        + "\n".join(sorted(_expected_card_policy_lines(task_id)))
    )
    lines[4] += "\n\nsynthetic"
    lines[5] += "\n\nsynthetic"
    return "\n\n".join(lines) + "\n"


def _self_test_recovery_card_projection() -> None:
    with tempfile.TemporaryDirectory(prefix="readerlab-recovery-cards-") as directory:
        project_root = Path(directory)
        taskcard_root = project_root / "taskcards"
        taskcard_root.mkdir()
        empty_errors: list[str] = []
        _recovery_taskcard_names(empty_errors, project_root)
        if empty_errors:
            raise AssertionError(f"zero-card registration failed: {empty_errors}")
        for task_id in RECOVERY_TASK_IDS:
            (taskcard_root / f"{task_id}.md").write_text(
                _synthetic_recovery_card_text(task_id),
                encoding="utf-8",
            )

        errors: list[str] = []
        _recovery_taskcard_names(errors, project_root)
        if errors:
            raise AssertionError(f"legal 21-card registration failed: {errors}")

        write_card = taskcard_root / "T2.2-R10.md"
        write_original = write_card.read_text(encoding="utf-8")
        write_card.write_text(
            write_original.replace(
                "## 5. 硬约束\n",
                "- write-path: `diagnostics/T2.2-extra.md`\n\n"
                "## 5. 硬约束\n",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("write whitelist path mismatch" in error for error in errors):
            raise AssertionError("extra recovery write path was accepted")
        write_card.write_text(write_original, encoding="utf-8")
        write_card.write_text(
            write_original.replace(
                "## 5. 硬约束\n",
                "- additional-authorized-output: `tools/run.py`\n\n"
                "## 5. 硬约束\n",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("write whitelist path mismatch" in error for error in errors):
            raise AssertionError("non-policy recovery write path was accepted")
        write_card.write_text(write_original, encoding="utf-8")
        write_card.write_text(
            write_original.replace(
                "## 5. 硬约束\n",
                "- additional-authorized-output-prefix: `tools/`\n\n"
                "## 5. 硬约束\n",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("write whitelist path mismatch" in error for error in errors):
            raise AssertionError("recovery write directory prefix was accepted")
        write_card.write_text(write_original, encoding="utf-8")

        read_card = taskcard_root / "T2.2-R10.md"
        read_original = read_card.read_text(encoding="utf-8")
        read_line = next(
            line
            for line in read_original.splitlines()
            if line.startswith("- read-path:")
        )
        read_card.write_text(
            read_original.replace(read_line + "\n", "", 1),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("read-path projection mismatch" in error for error in errors):
            raise AssertionError("missing recovery read path was accepted")
        read_card.write_text(
            read_original.replace(
                read_line + "\n",
                read_line + "\n" + read_line + "\n",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("read-path projection mismatch" in error for error in errors):
            raise AssertionError("duplicate recovery read path was accepted")
        read_card.write_text(
            read_original.replace(read_line + "\n", "", 1).replace(
                "## 4. 交付文件清单\n",
                "## 4. 交付文件清单\n\n" + read_line + "\n",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("read-path projection mismatch" in error for error in errors):
            raise AssertionError("recovery read path in wrong section was accepted")
        read_card.write_text(
            read_original.replace(
                "## 4. 交付文件清单\n",
                "- read-path: `GOLD-STANDARDS.md`\n\n"
                "## 4. 交付文件清单\n",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any(
            "complete read whitelist path mismatch" in error for error in errors
        ):
            raise AssertionError("R10 unauthorized GOLD read path was accepted")
        read_card.write_text(
            read_original.replace(
                "## 4. 交付文件清单\n",
                "- additional-authorized-input: `tools/run.py`\n\n"
                "## 4. 交付文件清单\n",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any(
            "complete read whitelist path mismatch" in error for error in errors
        ):
            raise AssertionError("non-policy recovery read path was accepted")
        read_card.write_text(
            read_original.replace(
                "## 4. 交付文件清单\n",
                "- additional-authorized-input-prefix: `tools/`\n\n"
                "## 4. 交付文件清单\n",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any(
            "complete read whitelist path mismatch" in error for error in errors
        ):
            raise AssertionError("recovery read directory prefix was accepted")
        read_card.write_text(read_original, encoding="utf-8")

        for task_id in ("T2.2-R03", "T2.2-R04", "T2.2-R05", "T2.2-R06"):
            card = taskcard_root / f"{task_id}.md"
            original = card.read_text(encoding="utf-8")
            slot_line = next(
                line
                for line in original.splitlines()
                if line.startswith("- material-slot-policy:")
            )
            card.write_text(
                original.replace(slot_line + "\n", "", 1),
                encoding="utf-8",
            )
            errors = []
            _recovery_taskcard_names(errors, project_root)
            if not any(
                "material-slot-policy projection mismatch" in error
                for error in errors
            ):
                raise AssertionError(
                    f"{task_id} missing material slot was not rejected"
                )
            card.write_text(original, encoding="utf-8")
            card.write_text(
                original.replace(slot_line + "\n", slot_line + "\n" + slot_line + "\n", 1),
                encoding="utf-8",
            )
            errors = []
            _recovery_taskcard_names(errors, project_root)
            if not any(
                "material-slot-policy projection mismatch" in error
                for error in errors
            ):
                raise AssertionError(
                    f"{task_id} duplicate material slot was not rejected"
                )
            card.write_text(original, encoding="utf-8")
            tampered = original.replace(
                slot_line,
                slot_line.replace(
                    RECOVERY_MATERIAL_SLOTS[0],
                    "materials/T2.2-v2/source-01-*.md",
                ),
                1,
            )
            card.write_text(tampered, encoding="utf-8")
            errors = []
            _recovery_taskcard_names(errors, project_root)
            if not any(
                "material-slot-policy projection mismatch" in error
                for error in errors
            ):
                raise AssertionError(
                    f"{task_id} tampered material slot was not rejected"
                )
            card.write_text(original, encoding="utf-8")
            misplaced = original.replace(slot_line + "\n", "", 1).replace(
                "## 4. 交付文件清单\n",
                "## 4. 交付文件清单\n\n" + slot_line + "\n",
                1,
            )
            card.write_text(misplaced, encoding="utf-8")
            errors = []
            _recovery_taskcard_names(errors, project_root)
            if not any(
                "read/material-slot-policy projection mismatch" in error
                for error in errors
            ):
                raise AssertionError(
                    f"{task_id} material policy in wrong section was accepted"
                )
            card.write_text(original, encoding="utf-8")

        r05 = taskcard_root / "T2.2-R05.md"
        r05_original = r05.read_text(encoding="utf-8")
        r05_injections = (
            (
                "- read-path: `GOLD-STANDARDS.md`\n"
                "- read-path: `examples/book/positive/"
                "automatic-driving-safe-state.md`\n",
                "R05 GOLD/examples read paths were accepted",
            ),
            (
                "- read-path: `materials/T2.2-v2/*.md`\n",
                "R05 material glob was accepted",
            ),
            (
                "- read-path: `materials/T2.2-v2/source-15-full.md`\n",
                "R05 extra material path was accepted",
            ),
            (
                "- 打开全部材料\n",
                "R05 all-material authorization was accepted",
            ),
        )
        for injection, message in r05_injections:
            r05.write_text(
                r05_original.replace(
                    "## 4. 交付文件清单\n",
                    injection + "\n## 4. 交付文件清单\n",
                    1,
                ),
                encoding="utf-8",
            )
            errors = []
            _recovery_taskcard_names(errors, project_root)
            if not errors:
                raise AssertionError(message)
        r05.write_text(
            r05_original.replace(
                "runtime-open: forbidden",
                "runtime-open: selected-only",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("runtime-open contract mismatch" in error for error in errors):
            raise AssertionError("R05 non-forbidden runtime permission was accepted")
        r05.write_text(r05_original, encoding="utf-8")

        originals = {
            task_id: (taskcard_root / f"{task_id}.md").read_text(
                encoding="utf-8"
            )
            for task_id in RECOVERY_TASK_IDS
        }
        for count in range(1, 21):
            for task_id in RECOVERY_TASK_IDS:
                path = taskcard_root / f"{task_id}.md"
                if path.exists():
                    path.unlink()
            for task_id in RECOVERY_TASK_IDS[:count]:
                (taskcard_root / f"{task_id}.md").write_text(
                    originals[task_id], encoding="utf-8"
                )
            errors = []
            _recovery_taskcard_names(errors, project_root)
            if not any("atomically as 0 or 21" in error for error in errors):
                raise AssertionError(f"{count}-card partial registration was accepted")
        for task_id, text in originals.items():
            (taskcard_root / f"{task_id}.md").write_text(text, encoding="utf-8")

        r22 = taskcard_root / "T2.2-R22.md"
        r22.write_text("synthetic", encoding="utf-8")
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("unexpected recovery taskcard" in error for error in errors):
            raise AssertionError("R22 card was accepted")
        r22.unlink()

        illegal_blocker = taskcard_root / "T2.2-R22-BLOCKER.md"
        illegal_blocker.write_text(RECOVERY_BLOCKER_HEADER, encoding="utf-8")
        errors = []
        _recovery_taskcard_names(errors, project_root)
        if not any("unexpected recovery taskcard" in error for error in errors):
            raise AssertionError("illegal R22 blocker was accepted")
        illegal_blocker.unlink()

        composite = taskcard_root / "T2.2-R09.md"
        composite_original = composite.read_text(encoding="utf-8")
        composite.write_text(
            composite_original.replace(
                "recovery-execution-mode: composite",
                "recovery-execution-mode: single-session",
            ),
            encoding="utf-8",
        )
        errors = []
        _recovery_taskcard_names(errors, project_root)
        composite.write_text(composite_original, encoding="utf-8")
        if not any("mode mismatch" in error for error in errors):
            raise AssertionError("wrong recovery composite set was accepted")


def _self_test_selector_and_filesystem_guards() -> None:
    with tempfile.TemporaryDirectory(prefix="readerlab-recovery-guards-") as directory:
        project_root = Path(directory)
        selector = project_root / RECOVERY_SELECTOR_PATH
        selector.parent.mkdir(parents=True)
        selected_path = RECOVERY_MATERIAL_SLOTS[0]
        selected_file = project_root / selected_path
        selected_file.parent.mkdir(parents=True)
        selected_file.write_text("synthetic selected source\n", encoding="utf-8")
        selector_lines = [
            "slot-set-id: T2.2-V2-SOURCE-SLOTS-01-14",
            *tuple(f"slot-member: {path}" for path in RECOVERY_MATERIAL_SLOTS),
            (
                f"selected-slot: {selected_path}"
                " | source-group: 01 | request-id: REQUEST-01"
            ),
            *tuple(
                f"unselected-slot: {path}"
                for path in RECOVERY_MATERIAL_SLOTS[1:]
            ),
            "selected-slot-count: 1",
            "selector-result: SLOTS_REQUIRED",
            "selection-reason: synthetic one-selected test",
        ]
        selector.write_text(
            RECOVERY_EXACT_HEADER.format(status="frozen", scope="run-only")
            + "\n".join(selector_lines)
            + "\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        selected, result = _validate_recovery_selector(errors, project_root)
        if errors or selected != {selected_path} or result != "SLOTS_REQUIRED":
            raise AssertionError(
                f"unselected absent slots caused false positive: {errors}"
            )
        valid_selector = selector.read_text(encoding="utf-8")
        selector.write_text(
            valid_selector.replace(
                "source-group: 01 | request-id: REQUEST-01",
                "source-group: 02 | request-id: REQUEST-01",
                1,
            ),
            encoding="utf-8",
        )
        errors = []
        _validate_recovery_selector(errors, project_root)
        if not any("slot/source-group mapping mismatch" in error for error in errors):
            raise AssertionError("mismatched selected slot/source-group was accepted")
        selector.write_text(valid_selector, encoding="utf-8")
        selected_file.unlink()
        selector.write_text(
            RECOVERY_EXACT_HEADER.format(status="frozen", scope="run-only")
            + "\n".join(
                (
                    "slot-set-id: T2.2-V2-SOURCE-SLOTS-01-14",
                    *tuple(
                        f"slot-member: {path}"
                        for path in RECOVERY_MATERIAL_SLOTS
                    ),
                    *tuple(
                        f"unselected-slot: {path}"
                        for path in RECOVERY_MATERIAL_SLOTS
                    ),
                    "selected-slot-count: 0",
                    "selector-result: NO_SLOTS",
                    "selection-reason: synthetic no-slots test",
                )
            )
            + "\n",
            encoding="utf-8",
        )
        errors = []
        selected, result = _validate_recovery_selector(errors, project_root)
        if errors or selected or result != "NO_SLOTS":
            raise AssertionError(f"legal NO_SLOTS selector failed: {errors}")

        raw_root = project_root / "diagnostics/T2.2-fixture-bytes-v2"
        raw_root.mkdir()
        (project_root / RECOVERY_RAW_BLOBS[0]).write_bytes(b"one")
        errors = []
        _validate_recovery_raw_blobs(errors, project_root)
        if not any("exact 28-file set" in error for error in errors):
            raise AssertionError("partial raw blob publication was accepted")
        for relative_path in RECOVERY_RAW_BLOBS[1:]:
            (project_root / relative_path).write_bytes(b"synthetic")
        (raw_root / "candidate-15.bin").write_bytes(b"unexpected")
        errors = []
        _validate_recovery_raw_blobs(errors, project_root)
        if not any("unexpected" in error for error in errors):
            raise AssertionError("29th raw blob was accepted")
        (raw_root / "candidate-15.bin").unlink()

        regular = project_root / "regular.bin"
        regular.write_bytes(b"regular")
        link = project_root / "link.bin"
        link.symlink_to(regular)
        errors = []
        read_regular_bytes(link, errors, project_root)
        if not any("symlink forbidden" in error for error in errors):
            raise AssertionError("symlink file was accepted")
        nonregular = project_root / "not-a-file"
        nonregular.mkdir()
        errors = []
        read_regular_bytes(nonregular, errors, project_root)
        if not any("regular file required" in error for error in errors):
            raise AssertionError("non-regular file was accepted")
        outside = project_root.parent / f"{project_root.name}-outside"
        outside.write_bytes(b"outside")
        errors = []
        read_regular_bytes(outside, errors, project_root)
        outside.unlink()
        if not any("escapes project root" in error for error in errors):
            raise AssertionError("path escape was accepted")

        unexpected = project_root / "diagnostics/T2.2-unexpected.md"
        unexpected.write_text(
            RECOVERY_EXACT_HEADER.format(status="frozen", scope="run-only"),
            encoding="utf-8",
        )
        errors = []
        _validate_recovery_artifacts(errors, project_root)
        if not any("unexpected recovery artifact path" in error for error in errors):
            raise AssertionError("unexpected recovery artifact was accepted")
        unexpected.unlink()
        wrong_header_path = (
            project_root / "diagnostics/T2.2-fixture-resolution-v2.md"
        )
        wrong_header_path.write_text(
            RECOVERY_EXACT_HEADER.format(status="draft", scope="run-only"),
            encoding="utf-8",
        )
        errors = []
        _validate_recovery_artifacts(errors, project_root)
        if not any("status/scope header mismatch" in error for error in errors):
            raise AssertionError("wrong recovery status/scope was accepted")


def _self_test_blocked_selector_rejects_m2() -> None:
    with tempfile.TemporaryDirectory(prefix="readerlab-recovery-blocked-") as directory:
        project_root = Path(directory)
        receipt = project_root / M2_RECEIPT_PATH
        receipt.parent.mkdir(parents=True)
        receipt.write_text(
            RECOVERY_EXACT_HEADER.format(status="frozen", scope="long-term"),
            encoding="utf-8",
        )
        errors: list[str] = []
        _validate_m2_receipt(
            errors,
            project_root,
            {f"{task_id}.md" for task_id in RECOVERY_TASK_IDS},
            set(RECOVERY_RAW_BLOBS),
            "BLOCKED",
        )
        if not any("selector is BLOCKED" in error for error in errors):
            raise AssertionError("BLOCKED selector did not forbid M2 receipt")
        if not any(
            "M2 receipt field must occur exactly once" in error
            or "M2 receipt T2.2 key set mismatch" in error
            for error in errors
        ):
            raise AssertionError("fake/incomplete M2 receipt fields were accepted")


def _synthetic_git(project_root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(project_root), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def _synthetic_commit(project_root: Path, message: str) -> str:
    _synthetic_git(project_root, "add", "-A")
    _synthetic_git(project_root, "commit", "-m", message)
    return _synthetic_git(project_root, "rev-parse", "HEAD")


def _synthetic_artifact_header(relative_path: str) -> str:
    policy = RECOVERY_ARTIFACT_POLICY.get(relative_path)
    if policy is not None:
        return RECOVERY_EXACT_HEADER.format(
            status=policy["status"], scope=policy["scope"]
        )
    if relative_path == "taskcards/T2.2-BLOCKER.md":
        return RECOVERY_BLOCKER_HEADER
    return RECOVERY_EXACT_HEADER.format(status="frozen", scope="run-only")


def _synthetic_write(
    project_root: Path,
    relative_path: str,
    body_lines: tuple[str, ...] = (),
    input_paths: tuple[str, ...] = (),
) -> None:
    path = project_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = list(body_lines)
    for input_path in input_paths:
        input_content = (project_root / input_path).read_bytes()
        lines.append(_binding_line("input-binding", input_path, input_content))
    path.write_text(
        _synthetic_artifact_header(relative_path)
        + ("\n".join(lines) + "\n" if lines else ""),
        encoding="utf-8",
    )


def _synthetic_write_review(
    project_root: Path,
    review_path: str,
    subjects: tuple[str, ...],
    subject_commit: str,
) -> None:
    lines = ["review-result: PASS", "subjects-unchanged-since-commit: yes"]
    for subject_path in subjects:
        subject = (project_root / subject_path).read_bytes()
        lines.append(
            f"- subject-binding: `{subject_path}`"
            f" | owner-task: {_review_owner_task(subject_path)}"
            f" | commit: {subject_commit}"
            f" | sha256: {hashlib.sha256(subject).hexdigest()}"
        )
    _synthetic_write(project_root, review_path, tuple(lines))


def _synthetic_packet_block(kind: str, payload: bytes) -> bytes:
    return (
        f"BYTE-BLOCK: {kind}\n"
        f"PAYLOAD-LENGTH: {len(payload)}\n"
        f"PAYLOAD-SHA256: {hashlib.sha256(payload).hexdigest()}\n"
        "PAYLOAD-BEGIN\n"
    ).encode("ascii") + payload + b"\nPAYLOAD-END\n"


def _synthetic_write_packet(
    project_root: Path,
    relative_path: str,
    blocks: tuple[tuple[str, str | None], ...],
) -> list[tuple[str, str | None, bytes]]:
    content = _synthetic_artifact_header(relative_path).encode("utf-8")
    observed: list[tuple[str, str | None, bytes]] = []
    for kind, blob_path in blocks:
        payload = (
            b"" if blob_path is None else (project_root / blob_path).read_bytes()
        )
        content += _synthetic_packet_block(kind, payload)
        observed.append((kind, blob_path, payload))
    path = project_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return observed


def _build_synthetic_recovery_chain(
    project_root: Path,
    r01_requests: tuple[str, ...] = (),
) -> dict[str, tuple[str, str, str]]:
    _synthetic_git(project_root, "init")
    _synthetic_git(project_root, "config", "user.email", "readerlab@example.invalid")
    _synthetic_git(project_root, "config", "user.name", "ReaderLab Self Test")
    taskcard_root = project_root / "taskcards"
    taskcard_root.mkdir(parents=True)
    for task_id in RECOVERY_TASK_IDS:
        (taskcard_root / f"{task_id}.md").write_text(
            _synthetic_recovery_card_text(task_id), encoding="utf-8"
        )
    fixed_paths = tuple(RECOVERY_ATTEMPT_FIXED_IDENTITIES)
    for relative_path in fixed_paths:
        _synthetic_write(
            project_root,
            relative_path,
            (f"synthetic-fixed-path: {relative_path}",),
        )
    for relative_path in (
        RECOVERY_ARCHITECTURE_IDENTITIES["quality-audit"][0],
        "contracts/M1-freeze-receipt.md",
        "contracts/T1.8-independent-acceptance.md",
        "diagnostics/T2.1-r01-r08.md",
        "lenses/T2.3-seed-lenses-v2.md",
    ):
        _synthetic_write(
            project_root,
            relative_path,
            (f"synthetic-gate-path: {relative_path}",),
        )
    fixed_commit = _synthetic_commit(project_root, "synthetic fixed identities")
    fixed_results = {
        path: RECOVERY_ATTEMPT_FIXED_IDENTITIES[path][2] for path in fixed_paths
    }
    identities = {
        path: (
            fixed_commit,
            hashlib.sha256((project_root / path).read_bytes()).hexdigest(),
            fixed_results[path],
        )
        for path in fixed_paths
    }

    r01_subjects = (
        "contracts/T2.2-historical-qualification-adapter-v1.md",
        "diagnostics/T2.2-fixture-census-v2.md",
        "diagnostics/T2.2-fixture-gap-list-v2.md",
    )
    for relative_path in r01_subjects:
        _synthetic_write(project_root, relative_path, ("synthetic-r01: yes",))
    if r01_requests:
        r01_blocker = project_root / RECOVERY_R01_BLOCKER_PATH
        r01_blocker.write_text(
            RECOVERY_BLOCKER_HEADER
            + "blocker-type: product-request\n"
            + "\n".join(
                f"- product-request-id: {request_id}"
                for request_id in r01_requests
            )
            + "\n",
            encoding="utf-8",
        )
    r01_commit = _synthetic_commit(project_root, "synthetic R01")
    _synthetic_write_review(
        project_root,
        "diagnostics/T2.2-historical-qualification-adapter-v1-review.md",
        (r01_subjects[0],),
        r01_commit,
    )
    _synthetic_write_review(
        project_root,
        "diagnostics/T2.2-fixture-census-review-v2.md",
        r01_subjects[1:],
        r01_commit,
    )
    _synthetic_commit(project_root, "synthetic R02")

    source_bytes: dict[str, bytes] = {}
    candidate_bytes: dict[str, bytes] = {}
    context_bytes: dict[str, bytes] = {}
    selector_lines = ["slot-set-id: T2.2-V2-SOURCE-SLOTS-01-14"]
    for index, slot_path in enumerate(RECOVERY_MATERIAL_SLOTS, start=1):
        group = f"{index:02d}"
        candidate = f"CANDIDATE-{group}\n".encode("utf-8")
        context = f"CONTEXT-{group}\n".encode("utf-8")
        source = candidate + context
        source_bytes[group] = source
        candidate_bytes[group] = candidate
        context_bytes[group] = context
        slot = project_root / slot_path
        slot.parent.mkdir(parents=True, exist_ok=True)
        slot.write_bytes(source)
        selector_lines.append(f"slot-member: {slot_path}")
    for index, slot_path in enumerate(RECOVERY_MATERIAL_SLOTS, start=1):
        selector_lines.append(
            f"selected-slot: {slot_path}"
            f" | source-group: {index:02d}"
            f" | request-id: REQUEST-{index:02d}"
        )
    selector_lines.extend(
        (
            "selected-slot-count: 14",
            "selector-result: SLOTS_REQUIRED",
            "selection-reason: synthetic full-chain fixture",
        )
    )
    _synthetic_write(
        project_root,
        "materials/T2.2-v2/authorization.md",
        ("synthetic-authorization: yes",),
    )
    _synthetic_write(
        project_root, RECOVERY_SELECTOR_PATH, tuple(selector_lines)
    )
    _synthetic_write(
        project_root,
        "diagnostics/T2.2-fixture-resolution-v2.md",
        (
            "synthetic-r03: yes",
            *tuple(
                f"- product-request-resolution: {request_id} | status: resolved"
                for request_id in r01_requests
            ),
        ),
    )
    _synthetic_write(
        project_root,
        "diagnostics/T2.2-fixture-admission-v2.md",
        ("synthetic-r03: yes",),
    )
    byte_manifest_lines: list[str] = []
    raw_root = project_root / "diagnostics/T2.2-fixture-bytes-v2"
    raw_root.mkdir(parents=True)
    for index, slot_path in enumerate(RECOVERY_MATERIAL_SLOTS, start=1):
        group = f"{index:02d}"
        source = source_bytes[group]
        candidate = candidate_bytes[group]
        context = context_bytes[group]
        candidate_path = (
            f"diagnostics/T2.2-fixture-bytes-v2/candidate-{group}.bin"
        )
        context_path = (
            f"diagnostics/T2.2-fixture-bytes-v2/context-{group}.bin"
        )
        (project_root / candidate_path).write_bytes(candidate)
        (project_root / context_path).write_bytes(context)
        source_hash = hashlib.sha256(source).hexdigest()
        candidate_hash = hashlib.sha256(candidate).hexdigest()
        context_hash = hashlib.sha256(context).hexdigest()
        candidate_end = len(candidate)
        context_end = len(source)
        byte_manifest_lines.append(
            f"- candidate-byte-proof: {group}"
            f" | selected-candidate-id: SYNTHETIC-CANDIDATE-{group}"
            f" | verdict-scope: synthetic-scope-{group}"
            f" | source-path: `{slot_path}`"
            f" | source-sha256: {source_hash}"
            f" | range: 0:{candidate_end}"
            f" | fragment-sha256: {candidate_hash}"
            f" | blob-path: `{candidate_path}`"
            f" | byte-length: {len(candidate)}"
            f" | blob-sha256: {candidate_hash}"
            f" | ends-with-lf: yes | raw-slot-foreign-key: `{slot_path}`"
            " | copy-ready: yes"
        )
        byte_manifest_lines.append(
            f"- context-byte-proof: {group}"
            f" | source-path: `{slot_path}`"
            f" | source-sha256: {source_hash}"
            f" | spans: {candidate_end}:{context_end}:{context_hash}"
            " | span-count: 1"
            f" | blob-path: `{context_path}`"
            f" | byte-length: {len(context)}"
            f" | blob-sha256: {context_hash}"
            " | ends-with-lf: yes"
            " | extraction-evidence: "
            "anchor=yes,dependencies=yes,nearest-only=yes,scope-stop=yes"
            " | copy-ready: yes"
        )
    _synthetic_write(
        project_root,
        "diagnostics/T2.2-fixture-byte-manifest-v2.md",
        tuple(byte_manifest_lines),
    )
    r03_commit = _synthetic_commit(project_root, "synthetic R03")
    _synthetic_write_review(
        project_root,
        "diagnostics/T2.2-fixture-byte-review-v2.md",
        RECOVERY_REVIEW_SUBJECTS[
            "diagnostics/T2.2-fixture-byte-review-v2.md"
        ],
        r03_commit,
    )
    _synthetic_commit(project_root, "synthetic R04")

    dependencies = _recovery_chain_dependencies(
        "SLOTS_REQUIRED",
        r01_product_blocker_present=bool(r01_requests),
    )
    fixed_identity_lines = tuple(
        f"- fixed-identity: `{path}`"
        f" | commit: {commit}"
        f" | sha256: {sha256}"
        f" | result: {result}"
        for path, (commit, sha256, result) in identities.items()
    )
    attempt_mapping_lines = tuple(
        f"- qualification-item: {index:02d}"
        f" | candidate-id: SYNTHETIC-CANDIDATE-{index:02d}"
        f" | q-id: SYNTHETIC-Q-{index:02d}"
        f" | candidate-blob-path: "
        f"`diagnostics/T2.2-fixture-bytes-v2/candidate-{index:02d}.bin`"
        f" | context-blob-path: "
        f"`diagnostics/T2.2-fixture-bytes-v2/context-{index:02d}.bin`"
        f" | formal-packet-path: "
        f"`diagnostics/T2.2-retest-packet-v2-{index:02d}.md`"
        for index in range(1, 15)
    )
    m14_lines = tuple(
        f"- m14-call: {answer}"
        f" | arm: {arm}"
        f" | packet-path: "
        f"`diagnostics/T2.2-contrast-packet-v1-{packet}.md`"
        f" | brief-path: `"
        + (
            "diagnostics/T2.2-judge-brief-v2.md"
            if brief_kind == "full"
            else "diagnostics/T2.2-judge-brief-variant-v1-02.md"
        )
        + f"` | object-order: {object_order}"
        for answer, arm, packet, brief_kind, object_order in RECOVERY_M14_CALLS
    )
    _synthetic_write(
        project_root,
        RECOVERY_ATTEMPT_MANIFEST_PATH,
        (
            "attempt-id: T2.2-QV2-A01",
            "attempt-salt-hex: "
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            *attempt_mapping_lines,
            "- sentinel: P | source-group: 01",
            "- sentinel: N1 | source-group: 04",
            *m14_lines,
            *tuple(
                f"- future-path: `{path}`"
                for path in RECOVERY_ATTEMPT_FUTURE_PATHS
            ),
            *fixed_identity_lines,
        ),
        dependencies[RECOVERY_ATTEMPT_MANIFEST_PATH],
    )
    for relative_path in RECOVERY_PACKAGE_MEMBER_PATHS:
        if relative_path not in RECOVERY_PACKET_PATHS:
            _synthetic_write(
                project_root, relative_path, ("synthetic-package-member: yes",)
            )
    packet_records: dict[str, list[tuple[str, str | None, bytes]]] = {}
    blind_blocks: list[tuple[str, str | None]] = []
    for index in range(1, 15):
        group = f"{index:02d}"
        blind_blocks.extend(
            (
                (
                    "CANDIDATE",
                    f"diagnostics/T2.2-fixture-bytes-v2/candidate-{group}.bin",
                ),
                (
                    "SOURCE-CONTEXT",
                    f"diagnostics/T2.2-fixture-bytes-v2/context-{group}.bin",
                ),
            )
        )
    blind_path = "diagnostics/T2.2-blind-packet-v2.md"
    packet_records[blind_path] = _synthetic_write_packet(
        project_root, blind_path, tuple(blind_blocks)
    )
    for index in range(1, 15):
        group = f"{index:02d}"
        packet_path = f"diagnostics/T2.2-retest-packet-v2-{group}.md"
        packet_records[packet_path] = _synthetic_write_packet(
            project_root,
            packet_path,
            (
                (
                    "CANDIDATE",
                    f"diagnostics/T2.2-fixture-bytes-v2/candidate-{group}.bin",
                ),
                (
                    "SOURCE-CONTEXT",
                    f"diagnostics/T2.2-fixture-bytes-v2/context-{group}.bin",
                ),
            ),
        )
    sentinel_groups = ("01", "04")
    contrast_specs = {
        1: (sentinel_groups[0],),
        2: (sentinel_groups[1],),
        3: (sentinel_groups[0],),
        4: (sentinel_groups[1],),
        5: sentinel_groups,
        6: tuple(reversed(sentinel_groups)),
    }
    for index, groups in contrast_specs.items():
        blocks: list[tuple[str, str | None]] = []
        for group in groups:
            blocks.append(
                (
                    "CANDIDATE",
                    f"diagnostics/T2.2-fixture-bytes-v2/candidate-{group}.bin",
                )
            )
            blocks.append(
                (
                    "SOURCE-CONTEXT",
                    (
                        None
                        if index in {3, 4}
                        else (
                            "diagnostics/T2.2-fixture-bytes-v2/"
                            f"context-{group}.bin"
                        )
                    ),
                )
            )
        packet_path = f"diagnostics/T2.2-contrast-packet-v1-{index:02d}.md"
        packet_records[packet_path] = _synthetic_write_packet(
            project_root, packet_path, tuple(blocks)
        )
    package_lines = [
        _binding_line(
            "package-binding",
            path,
            (project_root / path).read_bytes(),
        )
        for path in RECOVERY_PACKAGE_MEMBER_PATHS
    ]
    for packet_path in RECOVERY_PACKET_PATHS:
        records = packet_records[packet_path]
        for block_index, (kind, blob_path, payload) in enumerate(records, start=1):
            if blob_path is None:
                contrast_index = int(PurePosixPath(packet_path).stem.rsplit("-", 1)[1])
                canonical_group = contrast_specs[contrast_index][0]
                canonical_path = (
                    "diagnostics/T2.2-fixture-bytes-v2/"
                    f"context-{canonical_group}.bin"
                )
                canonical = (project_root / canonical_path).read_bytes()
                package_lines.append(
                    f"- payload-omission-proof: `{packet_path}`"
                    f" | block-index: {block_index}"
                    f" | canonical-blob-path: `{canonical_path}`"
                    f" | canonical-blob-sha256: "
                    f"{hashlib.sha256(canonical).hexdigest()}"
                    " | context-omitted-by-experiment: yes"
                )
            else:
                blob = (project_root / blob_path).read_bytes()
                blob_hash = hashlib.sha256(blob).hexdigest()
                package_lines.append(
                    f"- payload-copy-proof: `{packet_path}`"
                    f" | block-index: {block_index}"
                    f" | input-blob-path: `{blob_path}`"
                    f" | input-blob-length: {len(blob)}"
                    f" | input-blob-sha256: {blob_hash}"
                    f" | embedded-payload-length: {len(payload)}"
                    f" | embedded-payload-sha256: "
                    f"{hashlib.sha256(payload).hexdigest()}"
                    " | copy-equality: PASS"
                )
    _synthetic_write(
        project_root, RECOVERY_PACKAGE_MANIFEST_PATH, tuple(package_lines)
    )
    r05_commit = _synthetic_commit(project_root, "synthetic R05")
    _synthetic_write_review(
        project_root,
        "diagnostics/T2.2-package-preflight-review-v2.md",
        RECOVERY_REVIEW_SUBJECTS[
            "diagnostics/T2.2-package-preflight-review-v2.md"
        ],
        r05_commit,
    )
    _synthetic_commit(project_root, "synthetic R06")

    stage_specs = (
        (
            "R07",
            ("diagnostics/T2.2-contrast-control-call-manifest-v1.md",),
        ),
        (
            "R08-review",
            ("diagnostics/T2.2-contrast-control-input-review-v1.md",),
        ),
        (
            "R09",
            (
                *tuple(
                    f"diagnostics/T2.2-contrast-answer-v1-{index:02d}.md"
                    for index in range(1, 5)
                ),
                "diagnostics/T2.2-contrast-control-answers-index-v1.md",
            ),
        ),
        (
            "R10",
            ("diagnostics/T2.2-contrast-control-results-v1.md",),
        ),
        (
            "R11-review",
            ("diagnostics/T2.2-contrast-control-postflight-review-v1.md",),
        ),
        (
            "R12",
            ("diagnostics/T2.2-contrast-diagnostic-call-manifest-v1.md",),
        ),
        (
            "R13-review",
            ("diagnostics/T2.2-contrast-diagnostic-input-review-v1.md",),
        ),
        (
            "R14",
            (
                *tuple(
                    f"diagnostics/T2.2-contrast-answer-v1-{index:02d}.md"
                    for index in range(5, 15)
                ),
                "diagnostics/T2.2-contrast-diagnostic-answers-index-v1.md",
            ),
        ),
        ("R15", ("diagnostics/T2.2-contrast-results-v1.md",)),
        (
            "R16-review",
            ("diagnostics/T2.2-contrast-postflight-review-v1.md",),
        ),
        ("R17", ("diagnostics/T2.2-retest-call-manifest-v2.md",)),
        (
            "R18-review",
            ("diagnostics/T2.2-retest-input-review-v2.md",),
        ),
        (
            "R19",
            (
                *tuple(
                    f"diagnostics/T2.2-judge-answer-v2-{index:02d}.md"
                    for index in range(1, 15)
                ),
                "diagnostics/T2.2-judge-answers-index-v2.md",
            ),
        ),
        ("R20", ("diagnostics/T2.2-judge-baseline-v2.md",)),
        ("R21-review", ("diagnostics/T2.2-postflight-review-v2.md",)),
    )
    for stage, paths in stage_specs:
        if stage.endswith("-review"):
            review_path = paths[0]
            subjects = RECOVERY_REVIEW_SUBJECTS[review_path]
            subject_commit = _synthetic_git(project_root, "rev-parse", "HEAD")
            _synthetic_write_review(
                project_root, review_path, subjects, subject_commit
            )
        else:
            for relative_path in paths:
                body: tuple[str, ...] = ("synthetic-chain-artifact: yes",)
                if relative_path.endswith("contrast-control-results-v1.md"):
                    body += ("control-result: PASS",)
                if relative_path.endswith("judge-baseline-v2.md"):
                    body += ("qualification-result: PASS",)
                _synthetic_write(
                    project_root,
                    relative_path,
                    body,
                    dependencies[relative_path],
                )
        _synthetic_commit(project_root, f"synthetic {stage}")
    return identities


def _synthetic_receipt_fixed_values(
    project_root: Path,
    identities: dict[str, tuple[str, str, str]],
) -> dict[str, str]:
    active_path = RECOVERY_ARCHITECTURE_IDENTITIES["active-architecture"][0]
    review_path = RECOVERY_ARCHITECTURE_IDENTITIES[
        "active-architecture-review"
    ][0]
    return {
        "t2.2-active-architecture-path": active_path,
        "t2.2-active-architecture-sha256": identities[active_path][1],
        "t2.2-active-architecture-review-path": review_path,
        "t2.2-active-architecture-review-sha256": identities[review_path][1],
        "t2.2-active-attempt-id": "T2.2-QV2-A01",
        "t2.2-active-attempt-manifest-path": RECOVERY_ATTEMPT_MANIFEST_PATH,
        "t2.2-active-baseline-path": "diagnostics/T2.2-judge-baseline-v2.md",
        "t2.2-active-postflight-review-path": (
            "diagnostics/T2.2-postflight-review-v2.md"
        ),
        "t2.2-active-result": "PASS",
        "t2.2-history-v1-baseline-path": "diagnostics/T2.2-judge-baseline.md",
        "t2.2-history-v1-baseline-sha256": identities[
            "diagnostics/T2.2-judge-baseline.md"
        ][1],
        "t2.2-history-v1-baseline-result": "FAIL",
        "t2.2-history-v1-blocker-path": "taskcards/T2.2-BLOCKER.md",
        "t2.2-history-v1-blocker-sha256": identities[
            "taskcards/T2.2-BLOCKER.md"
        ][1],
        "t2.2-history-v2-architecture-path": (
            "diagnostics/T2.2-recovery-architecture-v2.md"
        ),
        "t2.2-history-v2-architecture-sha256": identities[
            "diagnostics/T2.2-recovery-architecture-v2.md"
        ][1],
        "t2.2-history-v2-review-path": (
            "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md"
        ),
        "t2.2-history-v2-review-sha256": identities[
            "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md"
        ][1],
        "t2.2-history-v2-review-result": "FAIL",
    }


def _synthetic_write_m2_receipt(
    project_root: Path, fixed_values: dict[str, str]
) -> None:
    hash_bindings = {
        "m1-freeze-receipt-sha256": "contracts/M1-freeze-receipt.md",
        "t1.8-independent-acceptance-sha256": (
            "contracts/T1.8-independent-acceptance.md"
        ),
        "t2.1-r01-r08-sha256": "diagnostics/T2.1-r01-r08.md",
        "t2.3-seed-lenses-v2-sha256": "lenses/T2.3-seed-lenses-v2.md",
        "t2.2-active-attempt-manifest-sha256": (
            RECOVERY_ATTEMPT_MANIFEST_PATH
        ),
        "t2.2-active-baseline-sha256": (
            "diagnostics/T2.2-judge-baseline-v2.md"
        ),
        "t2.2-active-postflight-review-sha256": (
            "diagnostics/T2.2-postflight-review-v2.md"
        ),
    }
    values = dict(fixed_values)
    values.update(
        {
            key: hashlib.sha256(
                (project_root / relative_path).read_bytes()
            ).hexdigest()
            for key, relative_path in hash_bindings.items()
        }
    )
    schema_keys = _v3_receipt_schema_keys()
    if (
        schema_keys != M2_RECEIPT_REQUIRED_KEYS
        or set(values) != set(schema_keys)
    ):
        raise AssertionError(
            "synthetic M2 receipt values do not match v3 section 13.2"
        )
    receipt = project_root / M2_RECEIPT_PATH
    receipt.write_text(
        RECOVERY_EXACT_HEADER.format(status="frozen", scope="long-term")
        + "\n".join(f"{key}: {values[key]}" for key in schema_keys)
        + "\n",
        encoding="utf-8",
    )


def _replace_first_hash(text: str, line_prefix: str) -> str:
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith(line_prefix):
            match = re.search(r"([0-9a-f]{64})", line)
            if match is None:
                break
            replacement = ("0" if match.group(1)[0] != "0" else "1") + match.group(
                1
            )[1:]
            lines[index] = (
                line[: match.start()] + replacement + line[match.end() :]
            )
            return "".join(lines)
    raise AssertionError(f"no hash line found for prefix {line_prefix}")


def _replace_first_match(text: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise AssertionError(f"no match found for tamper pattern {pattern}")
    return updated


def _assert_chain_tamper_rejected(
    project_root: Path,
    identities: dict[str, tuple[str, str, str]],
    relative_path: str,
    mutate,
) -> None:
    path = project_root / relative_path
    original = path.read_bytes()
    mutated = mutate(original)
    if mutated == original:
        raise AssertionError(f"tamper did not change {relative_path}")
    path.write_bytes(mutated)
    errors: list[str] = []
    _validate_m2_chain(
        errors,
        project_root,
        "SLOTS_REQUIRED",
        attempt_identities=identities,
    )
    path.write_bytes(original)
    if not errors:
        raise AssertionError(f"chain tamper was not rejected: {relative_path}")


def _self_test_complete_m2_chain() -> None:
    with tempfile.TemporaryDirectory(prefix="readerlab-recovery-chain-") as directory:
        project_root = Path(directory)
        schema_keys = _v3_receipt_schema_keys()
        if schema_keys != M2_RECEIPT_REQUIRED_KEYS or len(schema_keys) != 26:
            raise AssertionError(
                "validator receipt schema does not exactly match the 26 v3 fields"
            )
        forbidden_private_keys = {
            "t2.2-active-architecture-commit",
            "t2.2-active-architecture-review-commit",
            "t2.2-active-architecture-review-result",
            "t2.2-quality-audit-path",
            "t2.2-quality-audit-commit",
            "t2.2-quality-audit-sha256",
            "t2.2-quality-audit-result",
            "t2.2-history-v2-architecture-commit",
            "t2.2-history-v2-review-commit",
        }
        if forbidden_private_keys & set(schema_keys):
            raise AssertionError("private C0 fields leaked into the v3 receipt schema")
        identities = _build_synthetic_recovery_chain(project_root)
        errors: list[str] = []
        _validate_m2_chain(
            errors,
            project_root,
            "SLOTS_REQUIRED",
            attempt_identities=identities,
        )
        if errors:
            raise AssertionError(f"legal complete M2 chain failed: {errors}")
        receipt_fixed_values = _synthetic_receipt_fixed_values(
            project_root, identities
        )
        _synthetic_write_m2_receipt(project_root, receipt_fixed_values)
        errors = []
        _validate_m2_receipt(
            errors,
            project_root,
            {f"{task_id}.md" for task_id in RECOVERY_TASK_IDS},
            set(RECOVERY_RAW_BLOBS),
            "SLOTS_REQUIRED",
            attempt_identities=identities,
            fixed_values_override=receipt_fixed_values,
        )
        if errors:
            raise AssertionError(f"legal complete M2 receipt failed: {errors}")
        receipt_path = project_root / M2_RECEIPT_PATH
        receipt_text = receipt_path.read_text(encoding="utf-8")
        receipt_schema_tampers = (
            receipt_text.replace(
                f"{schema_keys[0]}: ",
                "removed-field: ",
                1,
            ).replace("removed-field: ", "", 1),
            receipt_text
            + f"{schema_keys[0]}: duplicate\n",
            receipt_text + "private-extra-field: forbidden\n",
            receipt_text + "任意额外字段: forbidden\n",
        )
        for tampered_receipt in receipt_schema_tampers:
            schema_errors: list[str] = []
            _receipt_field_values(
                tampered_receipt,
                M2_RECEIPT_REQUIRED_KEYS,
                schema_errors,
            )
            if not schema_errors:
                raise AssertionError(
                    "missing, duplicate, or extra M2 receipt field was accepted"
                )

        hash_tampers = (
            (
                "diagnostics/T2.2-fixture-byte-manifest-v2.md",
                "- candidate-byte-proof:",
            ),
            (
                "diagnostics/T2.2-fixture-byte-review-v2.md",
                "- subject-binding:",
            ),
            (RECOVERY_ATTEMPT_MANIFEST_PATH, "- input-binding:"),
            (RECOVERY_PACKAGE_MANIFEST_PATH, "- package-binding:"),
            (
                "diagnostics/T2.2-contrast-control-call-manifest-v1.md",
                "- input-binding:",
            ),
            (
                "diagnostics/T2.2-contrast-control-input-review-v1.md",
                "- subject-binding:",
            ),
            (
                "diagnostics/T2.2-contrast-answer-v1-01.md",
                "- input-binding:",
            ),
            (
                "diagnostics/T2.2-contrast-control-answers-index-v1.md",
                "- input-binding:",
            ),
            (
                "diagnostics/T2.2-contrast-control-results-v1.md",
                "- input-binding:",
            ),
            (
                "diagnostics/T2.2-judge-baseline-v2.md",
                "- input-binding:",
            ),
            (
                "diagnostics/T2.2-postflight-review-v2.md",
                "- subject-binding:",
            ),
        )
        for relative_path, prefix in hash_tampers:
            _assert_chain_tamper_rejected(
                project_root,
                identities,
                relative_path,
                lambda content, line_prefix=prefix: _replace_first_hash(
                    content.decode("utf-8"), line_prefix
                ).encode("utf-8"),
            )
        _assert_chain_tamper_rejected(
            project_root,
            identities,
            "diagnostics/T2.2-fixture-bytes-v2/candidate-01.bin",
            lambda content: content + b"tamper",
        )
        _assert_chain_tamper_rejected(
            project_root,
            identities,
            "diagnostics/T2.2-contrast-packet-v1-01.md",
            lambda content: content.replace(b"CANDIDATE-01", b"XANDIDATE-01", 1),
        )
        _assert_chain_tamper_rejected(
            project_root,
            identities,
            "diagnostics/T2.2-contrast-control-postflight-review-v1.md",
            lambda content: content.replace(
                b"review-result: PASS", b"review-result: FAIL", 1
            ),
        )
        structured_tampers = (
            (
                "diagnostics/T2.2-fixture-byte-manifest-v2.md",
                r"byte-length: ([0-9]+)",
                "byte-length: 999",
            ),
            (
                "diagnostics/T2.2-fixture-byte-review-v2.md",
                r"owner-task: T2\.2-R03",
                "owner-task: T2.2-R04",
            ),
            (
                "diagnostics/T2.2-fixture-byte-review-v2.md",
                r"commit: [0-9a-f]{40}",
                "commit: 0000000000000000000000000000000000000000",
            ),
            (
                RECOVERY_ATTEMPT_MANIFEST_PATH,
                r"- future-path: `diagnostics/T2\.2-blind-packet-v2\.md`",
                "- future-path: `diagnostics/T2.2-unexpected-packet-v2.md`",
            ),
            (
                RECOVERY_ATTEMPT_MANIFEST_PATH,
                r"candidate-id: SYNTHETIC-CANDIDATE-01",
                "candidate-id: SYNTHETIC-CANDIDATE-WRONG",
            ),
            (
                RECOVERY_ATTEMPT_MANIFEST_PATH,
                r"- m14-call: 01 \| arm: C",
                "- m14-call: 01 | arm: B",
            ),
            (
                RECOVERY_PACKAGE_MANIFEST_PATH,
                r"input-blob-length: ([0-9]+)",
                "input-blob-length: 999",
            ),
            (
                "diagnostics/T2.2-contrast-control-call-manifest-v1.md",
                (
                    r"`diagnostics/T2\.2-package-manifest-v2\.md`"
                    r" \| byte-length:"
                ),
                (
                    "`diagnostics/T2.2-package-preflight-review-v2.md`"
                    " | byte-length:"
                ),
            ),
        )
        for relative_path, pattern, replacement in structured_tampers:
            _assert_chain_tamper_rejected(
                project_root,
                identities,
                relative_path,
                lambda content, regex=pattern, value=replacement: _replace_first_match(
                    content.decode("utf-8"), regex, value
                ).encode("utf-8"),
            )

        answer_path = project_root / "diagnostics/T2.2-judge-answer-v2-01.md"
        baseline_path = project_root / "diagnostics/T2.2-judge-baseline-v2.md"
        answer_original = answer_path.read_bytes()
        baseline_original = baseline_path.read_bytes()
        answer_path.write_bytes(answer_original + b"intermediate-tamper\n")
        _synthetic_write(
            project_root,
            "diagnostics/T2.2-judge-baseline-v2.md",
            ("synthetic-chain-artifact: yes", "qualification-result: PASS"),
            _recovery_chain_dependencies("SLOTS_REQUIRED")[
                "diagnostics/T2.2-judge-baseline-v2.md"
            ],
        )
        errors = []
        _validate_m2_chain(
            errors,
            project_root,
            "SLOTS_REQUIRED",
            attempt_identities=identities,
        )
        answer_path.write_bytes(answer_original)
        baseline_path.write_bytes(baseline_original)
        if not errors:
            raise AssertionError(
                "patched final baseline masked an intermediate answer tamper"
            )

        receipt_original = receipt_path.read_bytes()
        answer_path.write_bytes(answer_original + b"receipt-only-tamper\n")
        _synthetic_write_m2_receipt(project_root, receipt_fixed_values)
        errors = []
        _validate_m2_receipt(
            errors,
            project_root,
            {f"{task_id}.md" for task_id in RECOVERY_TASK_IDS},
            set(RECOVERY_RAW_BLOBS),
            "SLOTS_REQUIRED",
            attempt_identities=identities,
            fixed_values_override=receipt_fixed_values,
        )
        answer_path.write_bytes(answer_original)
        receipt_path.write_bytes(receipt_original)
        if not errors:
            raise AssertionError(
                "patched final receipt masked an intermediate answer tamper"
            )


def _self_test_r01_product_request_blocker() -> None:
    with tempfile.TemporaryDirectory(prefix="readerlab-recovery-r01-") as directory:
        project_root = Path(directory)
        requests = ("REQUEST-01", "REQUEST-02")
        identities = _build_synthetic_recovery_chain(
            project_root, r01_requests=requests
        )
        fixed_values = _synthetic_receipt_fixed_values(project_root, identities)
        _synthetic_write_m2_receipt(project_root, fixed_values)
        blocker_path = project_root / RECOVERY_R01_BLOCKER_PATH
        blocker_original = blocker_path.read_bytes()
        errors: list[str] = []
        _validate_m2_receipt(
            errors,
            project_root,
            {f"{task_id}.md" for task_id in RECOVERY_TASK_IDS},
            set(RECOVERY_RAW_BLOBS),
            "SLOTS_REQUIRED",
            attempt_identities=identities,
            fixed_values_override=fixed_values,
        )
        if errors:
            raise AssertionError(
                f"legally closed R01 product blocker failed full M2: {errors}"
            )
        if not blocker_path.exists() or blocker_path.read_bytes() != blocker_original:
            raise AssertionError("legal R01 closure modified or deleted the blocker")

        resolution_path = (
            project_root / "diagnostics/T2.2-fixture-resolution-v2.md"
        )
        resolution_original = resolution_path.read_bytes()

        blocker_tampers = (
            blocker_original.replace(
                b"blocker-type: product-request",
                b"blocker-type: technical",
                1,
            ),
            blocker_original.replace(
                b"- product-request-id: REQUEST-02\n",
                b"",
                1,
            ),
            blocker_original.replace(
                b"- product-request-id: REQUEST-02\n",
                b"- product-request-id: REQUEST-01\n",
                1,
            ),
        )
        for tampered in blocker_tampers:
            blocker_path.write_bytes(tampered)
            blocker_errors: list[str] = []
            _validate_recovery_blockers_for_m2(blocker_errors, project_root)
            if not blocker_errors:
                raise AssertionError("invalid R01 blocker request contract was accepted")
        blocker_path.write_bytes(blocker_original)

        resolution_tampers = (
            resolution_original.replace(
                b"- product-request-resolution: REQUEST-02 | status: resolved\n",
                b"",
                1,
            ),
            resolution_original.replace(
                b"REQUEST-02 | status: resolved",
                b"REQUEST-99 | status: resolved",
                1,
            ),
            resolution_original.replace(
                b"REQUEST-02 | status: resolved",
                b"REQUEST-01 | status: resolved",
                1,
            ),
            resolution_original.replace(
                b"REQUEST-01 | status: resolved",
                b"REQUEST-01 | status: unresolved",
                1,
            ),
            resolution_original.replace(
                b"REQUEST-01 | status: resolved",
                b"REQUEST-01 | status: rejected",
                1,
            ),
        )
        for tampered in resolution_tampers:
            resolution_path.write_bytes(tampered)
            resolution_errors: list[str] = []
            _validate_recovery_blockers_for_m2(
                resolution_errors, project_root
            )
            if not resolution_errors:
                raise AssertionError(
                    "missing, duplicate, unequal, unresolved, or rejected "
                    "R03 resolution was accepted"
                )
        resolution_path.write_bytes(resolution_original)

        for blocker_relative_path in RECOVERY_BLOCKER_ARTIFACT_POLICY:
            if blocker_relative_path == RECOVERY_R01_BLOCKER_PATH:
                continue
            other_path = project_root / blocker_relative_path
            other_path.write_text(
                RECOVERY_BLOCKER_HEADER + "blocker-type: technical\n",
                encoding="utf-8",
            )
            other_errors: list[str] = []
            _validate_recovery_blockers_for_m2(other_errors, project_root)
            other_path.unlink()
            if not any(
                "non-closable recovery blocker" in error
                for error in other_errors
            ):
                raise AssertionError(
                    f"non-R01 blocker did not reject M2: {blocker_relative_path}"
                )

        resolution_path.write_bytes(
            resolution_original.replace(
                b"REQUEST-01 | status: resolved",
                b"REQUEST-01 | status: unresolved",
                1,
            )
        )
        chain_errors: list[str] = []
        _validate_m2_chain(
            chain_errors,
            project_root,
            "SLOTS_REQUIRED",
            attempt_identities=identities,
            r01_product_blocker_present=True,
        )
        resolution_path.write_bytes(resolution_original)
        if not chain_errors:
            raise AssertionError("tampered closed R01 resolution escaped attempt binding")

        attempt_path = project_root / RECOVERY_ATTEMPT_MANIFEST_PATH
        attempt_original = attempt_path.read_bytes()
        attempt_path.write_bytes(
            _replace_first_hash(
                attempt_original.decode("utf-8"),
                (
                    "- input-binding: "
                    "`diagnostics/T2.2-fixture-resolution-v2.md`"
                ),
            ).encode("utf-8")
        )
        chain_errors = []
        _validate_m2_chain(
            chain_errors,
            project_root,
            "SLOTS_REQUIRED",
            attempt_identities=identities,
            r01_product_blocker_present=True,
        )
        attempt_path.write_bytes(attempt_original)
        if not chain_errors:
            raise AssertionError("tampered R01 resolution attempt binding was accepted")


def _run_recovery_self_test() -> int:
    try:
        _self_test_recovery_card_projection()
        _self_test_selector_and_filesystem_guards()
        _self_test_blocked_selector_rejects_m2()
        _self_test_complete_m2_chain()
        _self_test_r01_product_request_blocker()
    except AssertionError as error:
        print("T2.2 recovery deterministic self-test FAILED")
        print(error)
        return 1
    print("T2.2 recovery deterministic self-test PASSED")
    return 0


def main() -> int:
    if "--self-test-recovery" in sys.argv:
        if len(sys.argv) != 2:
            print("usage: validate.py --self-test-recovery", file=sys.stderr)
            return 2
        return _run_recovery_self_test()

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

    if "--check-recovery-root" in sys.argv:
        if len(sys.argv) != 3 or sys.argv[1] != "--check-recovery-root":
            print(
                "usage: validate.py --check-recovery-root <project-root>",
                file=sys.stderr,
            )
            return 2
        return _run_recovery_only(Path(sys.argv[2]).resolve())

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
    validate_recovery_control(errors)

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
    allowed_nonformal_taskcards.update(
        PurePosixPath(path).name
        for path in RECOVERY_BLOCKER_ARTIFACT_POLICY
    )
    missing_taskcards = expected_taskcards - observed_taskcards
    allowed_recovery_taskcards = {
        f"{task_id}.md" for task_id in RECOVERY_TASK_IDS
    }
    unexpected_taskcards = (
        observed_taskcards
        - expected_taskcards
        - allowed_recovery_taskcards
        - allowed_nonformal_taskcards
    )
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
        for path in _walk_files_pruned(ROOT)
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
        "T2.2 recovery control 0/21 atomic registration, "
        f"{len(T0_3_FILES)} T0.3 contract documents, "
        f"{len(example_files)} readable example files, {len(RUNTIME_FILES)} runtime script, "
        f"{len(MATERIAL_GUARD_FILES)} material guard, "
        "0 legacy paths, 0 opaque assets, internal-only manifest."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
