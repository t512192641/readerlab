import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_readerlab_package.py"
ENGINEERING_SMOKE = ROOT / "packaging" / "engineering_route_smoke_test.py"
FIXTURE = ROOT / "tests" / "fixtures" / "readerlab" / "engineering-route-smoke-v0"

ENGINEERING_SMOKE_SPEC = importlib.util.spec_from_file_location("engineering_route_smoke_test", ENGINEERING_SMOKE)
assert ENGINEERING_SMOKE_SPEC is not None
engineering_smoke = importlib.util.module_from_spec(ENGINEERING_SMOKE_SPEC)
assert ENGINEERING_SMOKE_SPEC.loader is not None
ENGINEERING_SMOKE_SPEC.loader.exec_module(engineering_smoke)


class ReaderLabEngineeringRouteSmokeTests(unittest.TestCase):
    def test_repo_engineering_route_smoke_passes(self) -> None:
        result = subprocess.run(
            ["python3", str(ENGINEERING_SMOKE)],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["check_class"], "skill_engineering_route_smoke")
        self.assertTrue(payload["not_reader_acceptance"])
        self.assertTrue(payload["not_production_ready"])
        self.assertEqual(payload["material_family"], "skill_engineering")
        self.assertTrue(payload["config_cross_check"]["engineering_source_scope_closed"])
        self.assertTrue(payload["config_cross_check"]["full_source_evidence_packet_present"])
        self.assertTrue(payload["config_cross_check"]["asset_cards_cold_start_fields_present"])
        self.assertTrue(payload["config_cross_check"]["blocking_controller_enforced"])
        self.assertEqual(payload["verification_layers"]["configuration_structure"], "pass")
        self.assertEqual(payload["verification_layers"]["runner_contract"], "pass")
        self.assertEqual(payload["verification_layers"]["quality_gate_request"], "pass")
        self.assertEqual(payload["verification_layers"]["reader_evaluation"], "machine_smoke_only")
        self.assertEqual(payload["verification_layers"]["blocking_controller"], "pass")
        self.assertEqual(payload["verification_layers"]["human_acceptance"], "not_run")
        self.assertTrue(payload["reader_pages"]["cleaned_body_before_companion"])
        self.assertTrue(payload["reader_pages"]["asset_cards_have_cold_start_fields"])

    def test_built_package_contains_and_runs_engineering_route_smoke(self) -> None:
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
                ["python3", "tests/engineering_route_smoke_test.py"],
                cwd=package_root,
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(smoke.stdout)

            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["verification_layers"]["blocking_controller"], "pass")

    def test_config_cross_check_rejects_missing_engineering_scope_source(self) -> None:
        payload = engineering_smoke.build_run_config_payload(FIXTURE, Path("engineering-output"))
        payload["engineering_source_scope"] = ["src-engineering-skill-body"]

        with self.assertRaises(engineering_smoke.SmokeFailure) as failure:
            engineering_smoke.assert_config_matches_fixture(payload, FIXTURE)

        self.assertEqual(failure.exception.phase, "configuration_structure")
        self.assertIn("engineering_source_scope", failure.exception.message)

    def test_config_cross_check_rejects_controller_bypass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            shutil.copytree(FIXTURE, fixture)
            payload = engineering_smoke.build_run_config_payload(fixture, Path("engineering-output"))
            controller_path = fixture / "audit/contracts/controller-decision.v1.json"
            controller = json.loads(controller_path.read_text(encoding="utf-8"))
            controller["controller_decision"] = "limited_accept"
            controller_path.write_text(json.dumps(controller, ensure_ascii=False, indent=2), encoding="utf-8")

            with self.assertRaises(engineering_smoke.SmokeFailure) as failure:
                engineering_smoke.assert_config_matches_fixture(payload, fixture)

        self.assertEqual(failure.exception.phase, "controller")
        self.assertIn("blocking gate", failure.exception.message)

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

    def test_render_rejects_engineering_package_without_asset_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            output = Path(tmp) / "output"
            shutil.copytree(FIXTURE, fixture)
            cards_path = fixture / "audit/contracts/technical-asset-cards.v1.json"
            cards_path.unlink()

            result = subprocess.run(
                ["python3", "scripts/readerlab.py", "render-contract-package", str(fixture), str(output)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("technical-asset-cards", result.stderr)

    def test_eval_rejects_engineering_package_with_empty_asset_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            shutil.copytree(FIXTURE, fixture)
            cards_path = fixture / "audit/contracts/technical-asset-cards.v1.json"
            cards = json.loads(cards_path.read_text(encoding="utf-8"))
            cards["cards"] = []
            cards_path.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")

            result = subprocess.run(
                ["python3", "scripts/readerlab.py", "eval-rendered-package", str(fixture)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            payload = json.loads(result.stdout)

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(payload["passed"])
        self.assertIn("technical_asset_cards_cold_start_present", [gate["id"] for gate in payload["gates"]])
        self.assertTrue(any("technical-asset-cards" in failure for failure in payload["failures"]))


if __name__ == "__main__":
    unittest.main()
