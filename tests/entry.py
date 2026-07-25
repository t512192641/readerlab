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

def validate_inventory(test_dir: Path = TESTS_DIR) -> None:
    discovered = {path.name for path in test_dir.glob("test_*.py")}
    active = set(ACTIVE.files)
    if discovered != active:
        unclassified = sorted(discovered - active)
        missing = sorted(active - discovered)
        raise TestEntryError(
            "test inventory classification mismatch: "
            f"unclassified={unclassified}, missing={missing}"
        )


def build_suite(test_dir: Path = TESTS_DIR) -> unittest.TestSuite:
    validate_inventory(test_dir)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for filename in ACTIVE.files:
        suite.addTests(
            loader.discover(
                start_dir=str(test_dir),
                pattern=filename,
                top_level_dir=str(test_dir),
            )
        )

    if suite.countTestCases() == 0:
        raise TestEntryError("active test inventory selected zero tests")
    return suite


def run(*, verbosity: int = 2) -> int:
    suite = build_suite()
    print(
        f"ReaderLab test suite: {ACTIVE.name} "
        f"({ACTIVE.purpose}; {suite.countTestCases()} tests)",
        file=sys.stderr,
    )
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the maintained ReaderLab active test inventory."
    )
    parser.parse_args(argv)
    try:
        return run()
    except TestEntryError as error:
        print(f"test entry error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
