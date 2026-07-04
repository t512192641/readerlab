import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_readerlab_package.py"
LONGFORM_SMOKE = ROOT / "packaging" / "longform_route_smoke_test.py"
FIXTURE = ROOT / "tests" / "fixtures" / "readerlab" / "longform-route-smoke-v0"

LONGFORM_SMOKE_SPEC = importlib.util.spec_from_file_location("longform_route_smoke_test", LONGFORM_SMOKE)
assert LONGFORM_SMOKE_SPEC is not None
longform_smoke = importlib.util.module_from_spec(LONGFORM_SMOKE_SPEC)
assert LONGFORM_SMOKE_SPEC.loader is not None
LONGFORM_SMOKE_SPEC.loader.exec_module(longform_smoke)


class ReaderLabLongformRouteSmokeTests(unittest.TestCase):
    def test_repo_longform_route_smoke_passes(self) -> None:
        result = subprocess.run(
            ["python3", str(LONGFORM_SMOKE)],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["check_class"], "longform_report_interview_route_smoke")
        self.assertTrue(payload["not_reader_acceptance"])
        self.assertTrue(payload["not_production_ready"])
        self.assertEqual(payload["material_family"], "longform_report_interview")
        self.assertEqual(payload["declared_units"], ["argument-problem-evidence", "interview-decision-turn"])
        self.assertTrue(payload["config_cross_check"]["source_paths_match_registry"])
        self.assertTrue(payload["config_cross_check"]["declared_units_match_catalog"])
        self.assertTrue(payload["config_cross_check"]["segmentation_logic_declared"])
        self.assertEqual(payload["verification_layers"]["configuration_structure"], "pass")
        self.assertEqual(payload["verification_layers"]["runner_contract"], "pass")
        self.assertEqual(payload["verification_layers"]["quality_gate_request"], "pass")
        self.assertEqual(payload["verification_layers"]["reader_evaluation"], "machine_smoke_only")
        self.assertEqual(payload["verification_layers"]["controller"], "human_status_pending_not_reader_package_pass")
        self.assertEqual(payload["verification_layers"]["human_acceptance"], "not_run")
        self.assertTrue(payload["reader_page"]["body_before_companion"])
        self.assertTrue(payload["reader_page"]["argument_before_interview_turn"])
        self.assertTrue(payload["reader_page"]["companion_tied_to_reading_problem"])

    def test_built_package_contains_and_runs_longform_route_smoke(self) -> None:
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
                ["python3", "tests/longform_route_smoke_test.py"],
                cwd=package_root,
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(smoke.stdout)

            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["verification_layers"]["controller"], "human_status_pending_not_reader_package_pass")

    def test_config_cross_check_rejects_source_order_mismatch(self) -> None:
        payload = longform_smoke.build_run_config_payload(FIXTURE, Path("longform-output"))
        payload["source_paths"] = list(reversed(payload["source_paths"]))

        with self.assertRaises(longform_smoke.SmokeFailure) as failure:
            longform_smoke.assert_config_matches_fixture(payload, FIXTURE)

        self.assertEqual(failure.exception.phase, "configuration_structure")
        self.assertIn("source_paths", failure.exception.message)

    def test_config_cross_check_rejects_declared_unit_order_mismatch(self) -> None:
        payload = longform_smoke.build_run_config_payload(FIXTURE, Path("longform-output"))
        payload["declared_units"] = list(reversed(payload["declared_units"]))

        with self.assertRaises(longform_smoke.SmokeFailure) as failure:
            longform_smoke.assert_config_matches_fixture(payload, FIXTURE)

        self.assertEqual(failure.exception.phase, "configuration_structure")
        self.assertIn("declared_units", failure.exception.message)

    def test_config_cross_check_rejects_blind_segmentation_logic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            shutil.copytree(FIXTURE, fixture)
            payload = longform_smoke.build_run_config_payload(fixture, Path("longform-output"))
            catalog_path = fixture / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["catalog"]["segmentation_logic"] = ["fixed length chunks"]
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

            with self.assertRaises(longform_smoke.SmokeFailure) as failure:
                longform_smoke.assert_config_matches_fixture(payload, fixture)

        self.assertEqual(failure.exception.phase, "configuration_structure")
        self.assertIn("segmentation_logic", failure.exception.message)

    def test_shipped_fixture_reader_display_path_is_evaluable(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/readerlab.py", "eval-rendered-package", str(FIXTURE)],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        payload = json.loads(result.stdout)

        self.assertTrue(payload["passed"])


if __name__ == "__main__":
    unittest.main()
