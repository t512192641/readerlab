import json
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_readerlab_package.py"
BOOK_SMOKE = ROOT / "packaging" / "book_route_smoke_test.py"
FIXTURE = ROOT / "tests" / "fixtures" / "readerlab" / "book-route-smoke-v0"

BOOK_SMOKE_SPEC = importlib.util.spec_from_file_location("book_route_smoke_test", BOOK_SMOKE)
assert BOOK_SMOKE_SPEC is not None
book_smoke = importlib.util.module_from_spec(BOOK_SMOKE_SPEC)
assert BOOK_SMOKE_SPEC.loader is not None
BOOK_SMOKE_SPEC.loader.exec_module(book_smoke)


class ReaderLabBookRouteSmokeTests(unittest.TestCase):
    def test_repo_book_route_smoke_passes(self) -> None:
        result = subprocess.run(
            ["python3", str(BOOK_SMOKE)],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["check_class"], "book_route_smoke")
        self.assertTrue(payload["not_reader_acceptance"])
        self.assertTrue(payload["not_production_ready"])
        self.assertEqual(payload["material_family"], "book_longform")
        self.assertEqual(payload["declared_units"], ["chapter-01", "chapter-02"])
        self.assertTrue(payload["config_cross_check"]["source_paths_match_registry"])
        self.assertTrue(payload["config_cross_check"]["declared_units_match_catalog"])
        self.assertEqual(payload["verification_layers"]["configuration_structure"], "pass")
        self.assertEqual(payload["verification_layers"]["runner_contract"], "pass")
        self.assertEqual(payload["verification_layers"]["quality_gate_request"], "pass")
        self.assertEqual(payload["verification_layers"]["reader_evaluation"], "machine_smoke_only")
        self.assertEqual(payload["verification_layers"]["controller"], "human_status_pending_not_reader_package_pass")
        self.assertEqual(payload["verification_layers"]["human_acceptance"], "not_run")
        self.assertTrue(payload["reader_page"]["body_before_companion"])
        self.assertTrue(payload["reader_page"]["chapter_order_preserved"])

    def test_built_package_contains_and_runs_book_route_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                ["python3", str(BUILD_SCRIPT), "--output-dir", tmp, "--force"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            build_payload = json.loads(result.stdout)
            package_root = Path(tmp) / build_payload["package_root"]
            smoke = subprocess.run(
                ["python3", "tests/book_route_smoke_test.py"],
                cwd=package_root,
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(smoke.stdout)

            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["verification_layers"]["controller"], "human_status_pending_not_reader_package_pass")

    def test_config_cross_check_rejects_source_order_mismatch(self) -> None:
        payload = book_smoke.build_run_config_payload(FIXTURE, Path("book-output"))
        payload["source_paths"] = list(reversed(payload["source_paths"]))

        with self.assertRaises(book_smoke.SmokeFailure) as failure:
            book_smoke.assert_config_matches_fixture(payload, FIXTURE)

        self.assertEqual(failure.exception.phase, "configuration_structure")
        self.assertIn("source_paths", failure.exception.message)

    def test_config_cross_check_rejects_declared_unit_order_mismatch(self) -> None:
        payload = book_smoke.build_run_config_payload(FIXTURE, Path("book-output"))
        payload["declared_units"] = list(reversed(payload["declared_units"]))

        with self.assertRaises(book_smoke.SmokeFailure) as failure:
            book_smoke.assert_config_matches_fixture(payload, FIXTURE)

        self.assertEqual(failure.exception.phase, "configuration_structure")
        self.assertIn("declared_units", failure.exception.message)


if __name__ == "__main__":
    unittest.main()
