from __future__ import annotations

import argparse
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


TESTS_DIR = Path(__file__).resolve().parent


class TestEntryError(RuntimeError):
    """Raised when the test inventory cannot produce a trustworthy signal."""


@dataclass(frozen=True)
class TestSuiteDefinition:
    name: str
    files: tuple[str, ...]
    purpose: str


ACTIVE = TestSuiteDefinition(
    name="active",
    files=(
        "test_book_content_flow_contract.py",
        "test_repository_audit_guardrails.py",
        "test_run_promotion.py",
        "test_test_entry.py",
    ),
    purpose=(
        "current maintained, runnable test subset; "
        "not a product or full-project qualification gate"
    ),
)

HISTORICAL_T226 = TestSuiteDefinition(
    name="historical-t226",
    files=(
        "test_t226_control_contract_preflight.py",
        "test_t226_material_scope.py",
        "test_t226_p2_recovery.py",
    ),
    purpose="frozen T2.26 identity replay",
)

SUITES = {
    definition.name: definition
    for definition in (ACTIVE, HISTORICAL_T226)
}


def validate_inventory(test_dir: Path = TESTS_DIR) -> None:
    discovered = {path.name for path in test_dir.glob("test_*.py")}
    active = set(ACTIVE.files)
    historical = set(HISTORICAL_T226.files)

    overlap = active & historical
    if overlap:
        raise TestEntryError(
            f"test files cannot be active and historical: {sorted(overlap)}"
        )

    classified = active | historical
    if discovered != classified:
        unclassified = sorted(discovered - classified)
        missing = sorted(classified - discovered)
        raise TestEntryError(
            "test inventory classification mismatch: "
            f"unclassified={unclassified}, missing={missing}"
        )


def build_suite(
    suite_name: str,
    test_dir: Path = TESTS_DIR,
) -> unittest.TestSuite:
    validate_inventory(test_dir)
    try:
        definition = SUITES[suite_name]
    except KeyError as error:
        raise TestEntryError(f"unknown test suite: {suite_name}") from error

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for filename in definition.files:
        suite.addTests(
            loader.discover(
                start_dir=str(test_dir),
                pattern=filename,
                top_level_dir=str(test_dir),
            )
        )

    if suite.countTestCases() == 0:
        raise TestEntryError(f"{suite_name} selected zero tests")
    return suite


def run(suite_name: str, *, verbosity: int = 2) -> int:
    suite = build_suite(suite_name)
    definition = SUITES[suite_name]
    print(
        f"ReaderLab test suite: {definition.name} "
        f"({definition.purpose}; {suite.countTestCases()} tests)",
        file=sys.stderr,
    )
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run ReaderLab active tests or an explicit historical replay."
    )
    parser.add_argument(
        "suite",
        nargs="?",
        default=ACTIVE.name,
        choices=tuple(SUITES),
    )
    args = parser.parse_args(argv)
    try:
        return run(args.suite)
    except TestEntryError as error:
        print(f"test entry error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
