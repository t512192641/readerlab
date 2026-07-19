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
            expected_policy_lines = _expected_card_policy_lines(task_id)
            if (
                len(actual_policy_lines) != len(set(actual_policy_lines))
                or set(actual_policy_lines) != expected_policy_lines
            ):
                errors.append(
                    f"recovery taskcard artifact-policy projection mismatch: "
                    f"{relative_path}"
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
    unselected = set(
        re.findall(r"^unselected-slot: (.+)$", selector, flags=re.MULTILINE)
    )
    allowed = set(RECOVERY_MATERIAL_SLOTS)
    if len(slot_members) != 14 or set(slot_members) != allowed:
        errors.append("recovery selector static slot-member set must equal the 14 literals")
    if len(selected) != len(selected_lines):
        errors.append("recovery selector selected-slot entries must be unique")
    if selected - allowed or unselected - allowed:
        errors.append(
            "recovery selector contains slot outside the static 14-member whitelist"
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


def _receipt_field_values(
    text: str, required_keys: tuple[str, ...], errors: list[str]
) -> dict[str, str]:
    values: dict[str, str] = {}
    for key in required_keys:
        matches = re.findall(
            rf"^{re.escape(key)}: (.+)$", text, flags=re.MULTILINE
        )
        if len(matches) != 1:
            errors.append(f"M2 receipt field must occur exactly once: {key}")
        else:
            values[key] = matches[0]
    observed_t22_keys = set(
        re.findall(r"^(t2\.2-[a-z0-9.-]+): .+$", text, flags=re.MULTILINE)
    )
    expected_t22_keys = {key for key in required_keys if key.startswith("t2.2-")}
    if observed_t22_keys != expected_t22_keys:
        errors.append(
            "M2 receipt T2.2 key set mismatch: "
            f"missing {sorted(expected_t22_keys - observed_t22_keys)}, "
            f"unexpected {sorted(observed_t22_keys - expected_t22_keys)}"
        )
    return values


def _validate_m2_receipt(
    errors: list[str],
    project_root: Path,
    formal_cards: set[str],
    raw_blobs: set[str],
    selector_result: str | None,
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

    required_keys = (
        "m1-freeze-receipt-sha256",
        "t1.8-independent-acceptance-sha256",
        "t2.1-r01-r08-sha256",
        "t2.3-seed-lenses-v2-sha256",
        "t2.2-active-architecture-path",
        "t2.2-active-architecture-commit",
        "t2.2-active-architecture-sha256",
        "t2.2-active-architecture-review-path",
        "t2.2-active-architecture-review-commit",
        "t2.2-active-architecture-review-sha256",
        "t2.2-active-architecture-review-result",
        "t2.2-quality-audit-path",
        "t2.2-quality-audit-commit",
        "t2.2-quality-audit-sha256",
        "t2.2-quality-audit-result",
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
        "t2.2-history-v2-architecture-commit",
        "t2.2-history-v2-architecture-sha256",
        "t2.2-history-v2-review-path",
        "t2.2-history-v2-review-commit",
        "t2.2-history-v2-review-sha256",
        "t2.2-history-v2-review-result",
    )
    fields = _receipt_field_values(receipt, required_keys, errors)

    fixed_values = {
        "t2.2-active-architecture-path": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture"
        ][0],
        "t2.2-active-architecture-commit": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture"
        ][1],
        "t2.2-active-architecture-sha256": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture"
        ][2],
        "t2.2-active-architecture-review-path": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture-review"
        ][0],
        "t2.2-active-architecture-review-commit": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture-review"
        ][1],
        "t2.2-active-architecture-review-sha256": RECOVERY_ARCHITECTURE_IDENTITIES[
            "active-architecture-review"
        ][2],
        "t2.2-active-architecture-review-result": "PASS",
        "t2.2-quality-audit-path": RECOVERY_ARCHITECTURE_IDENTITIES[
            "quality-audit"
        ][0],
        "t2.2-quality-audit-commit": RECOVERY_ARCHITECTURE_IDENTITIES[
            "quality-audit"
        ][1],
        "t2.2-quality-audit-sha256": RECOVERY_ARCHITECTURE_IDENTITIES[
            "quality-audit"
        ][2],
        "t2.2-quality-audit-result": "CONFIRMED_PASS",
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
        "t2.2-history-v2-architecture-commit": (
            "037f33b0893208a232efa4aaeb23866885ec5fd0"
        ),
        "t2.2-history-v2-architecture-sha256": (
            "1154110c3a3bff65e4dc2ceb8244e724f0da60924c4e32ba4afa413600a2043a"
        ),
        "t2.2-history-v2-review-path": (
            "diagnostics/T2.2-recovery-architecture-v2-preflight-review.md"
        ),
        "t2.2-history-v2-review-commit": (
            "4bc9feca20f41e9c41158885cad41683f4d227b2"
        ),
        "t2.2-history-v2-review-sha256": (
            "9d2c80e23e30018c4dc4283c56315ab2df2198344b98dda91cebae6755f92e13"
        ),
        "t2.2-history-v2-review-result": "FAIL",
    }
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
    recovery_blockers = [
        project_root / relative_path
        for relative_path in RECOVERY_BLOCKER_ARTIFACT_POLICY
    ]
    if any(path.exists() for path in recovery_blockers):
        errors.append("M2 receipt forbidden while any recovery blocker exists")
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
    postflight = _regular_file_content_if_present(
        "diagnostics/T2.2-postflight-review-v2.md", errors, project_root
    )
    if postflight is not None and baseline is not None:
        baseline_hash = hashlib.sha256(baseline).hexdigest()
        required_postflight_lines = {
            "review-result: PASS",
            "subjects-unchanged-since-commit: yes",
            "subject-path: diagnostics/T2.2-judge-baseline-v2.md",
            "subject-owner-task: T2.2-R20",
            f"subject-sha256: {baseline_hash}",
        }
        postflight_text = postflight.decode("utf-8", errors="replace")
        missing = sorted(
            line for line in required_postflight_lines if line not in postflight_text
        )
        if missing:
            errors.append(
                f"active v2 postflight review binding/result missing: {missing}"
            )
        commit_matches = re.findall(
            r"^subject-commit: ([0-9a-f]{40})$",
            postflight_text,
            flags=re.MULTILINE,
        )
        if len(commit_matches) != 1:
            errors.append(
                "active v2 postflight review must bind one 40-hex subject commit"
            )
        else:
            _validate_commit_identity(
                "diagnostics/T2.2-judge-baseline-v2.md",
                commit_matches[0],
                baseline_hash,
                errors,
                project_root,
            )


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
