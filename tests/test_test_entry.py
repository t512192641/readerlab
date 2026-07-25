from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


TESTS_DIR = Path(__file__).resolve().parent
ENTRY_PATH = TESTS_DIR / "entry.py"
SPEC = importlib.util.spec_from_file_location("readerlab_test_entry", ENTRY_PATH)
assert SPEC is not None and SPEC.loader is not None
ENTRY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ENTRY
SPEC.loader.exec_module(ENTRY)


def _test_ids(test: unittest.TestSuite | unittest.TestCase) -> set[str]:
    if isinstance(test, unittest.TestSuite):
        return {
            test_id
            for child in test
            for test_id in _test_ids(child)
        }
    return {test.id()}


class TestEntryTests(unittest.TestCase):
    def test_inventory_is_exactly_the_active_set(self) -> None:
        ENTRY.validate_inventory(TESTS_DIR)

        active = set(ENTRY.ACTIVE.files)
        discovered = {path.name for path in TESTS_DIR.glob("test_*.py")}

        self.assertEqual(active, discovered)

    def test_active_suite_is_nonzero(self) -> None:
        suite = ENTRY.build_suite(TESTS_DIR)
        test_ids = _test_ids(suite)

        self.assertEqual(
            ENTRY.ACTIVE.purpose,
            (
                "current maintained, runnable test subset; "
                "not a product or full-project qualification gate"
            ),
        )
        self.assertGreater(suite.countTestCases(), 0)
        self.assertTrue(test_ids)


if __name__ == "__main__":
    unittest.main()
