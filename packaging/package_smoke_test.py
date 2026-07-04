#!/usr/bin/env python3
"""Minimal self-test for a built ReaderLab shareable package."""

from __future__ import annotations

import json
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "SKILL.md",
    "checks/readiness-checklist.md",
    "evals/output-cases.json",
    "examples/run-config-example.json",
    "scripts/readerlab.py",
    "scripts/readerlab_trace_validator.py",
    "docs/readerlab-v2-runtime-config.md",
    "docs/contracts/trace-validation-v1.md",
    "fixtures/contract-validator-proof-v0/README.md",
    "PACKAGE_BOUNDARY.md",
    "PACKAGE_AUDIT.json",
)


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (PACKAGE_ROOT / path).is_file()]
    audit_path = PACKAGE_ROOT / "PACKAGE_AUDIT.json"
    audit_status = None
    if audit_path.is_file():
        audit_status = json.loads(audit_path.read_text(encoding="utf-8")).get("status")
    failures = [f"missing required file: {path}" for path in missing]
    if audit_status != "pass":
        failures.append(f"PACKAGE_AUDIT.json status must be pass, got {audit_status!r}")
    if failures:
        print("FAIL ReaderLab package smoke")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS ReaderLab package smoke")
    print("check_class: package_boundary_structure")
    print("not_reader_acceptance: true")
    print("not_production_ready: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
