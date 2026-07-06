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
        self.assertTrue(payload["config_cross_check"]["catalog_order_differs_from_source_order"])
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

    def test_renderer_orders_direct_source_refs_by_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            output_root = Path(tmp) / "output"
            shutil.copytree(FIXTURE, fixture)
            catalog_path = fixture / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["catalog"]["reading_units"][0]["source_refs"] = ["src-longform-report-argument"]
            catalog["catalog"]["reading_units"][1]["source_refs"] = ["src-longform-interview-turn"]
            catalog["claims"][0]["source_refs"] = [
                "src-longform-report-argument",
                "src-longform-interview-turn",
            ]
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

            subprocess.run(
                ["python3", "scripts/readerlab.py", "render-contract-package", str(fixture), str(output_root)],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = (output_root / "reader/02_章节正文陪读.md").read_text(encoding="utf-8")

        self.assertLess(text.index("报告开头不是先给结论"), text.index("访谈对象在这里先否认"))

    def test_renderer_keeps_multi_source_unit_title_with_each_excerpt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            output_root = Path(tmp) / "output"
            shutil.copytree(FIXTURE, fixture)
            catalog_path = fixture / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["catalog"]["reading_units"] = [
                {
                    "unit_id": "combined-unit",
                    "title": "同一阅读单元覆盖两个来源",
                    "status": "sample_argument_unit",
                    "source_refs": [
                        "src-longform-report-argument",
                        "src-longform-interview-turn",
                    ],
                },
                {
                    "unit_id": "later-unit",
                    "title": "后续阅读单元",
                    "status": "sample_interview_unit",
                    "source_refs": [],
                },
            ]
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

            subprocess.run(
                ["python3", "scripts/readerlab.py", "render-contract-package", str(fixture), str(output_root)],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = (output_root / "reader/02_章节正文陪读.md").read_text(encoding="utf-8")

        report = text.index("报告开头不是先给结论")
        interview = text.index("访谈对象在这里先否认")
        self.assertLess(text.index("### 同一阅读单元覆盖两个来源"), report)
        self.assertLess(text.index("### 同一阅读单元覆盖两个来源", report), interview)
        self.assertNotIn("### 后续阅读单元", text)

    def test_renderer_preserves_non_adjacent_repeated_source_positions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            output_root = Path(tmp) / "output"
            shutil.copytree(FIXTURE, fixture)
            catalog_path = fixture / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["catalog"]["reading_units"] = [
                {
                    "unit_id": "report-opening",
                    "title": "报告开头",
                    "status": "sample_argument_unit",
                    "source_refs": ["loc-longform-report-tension"],
                },
                {
                    "unit_id": "interview-turn",
                    "title": "访谈转折",
                    "status": "sample_interview_unit",
                    "source_refs": ["loc-longform-interview-turn"],
                },
                {
                    "unit_id": "report-evidence",
                    "title": "报告证据组",
                    "status": "sample_argument_unit",
                    "source_refs": ["loc-longform-report-evidence-group"],
                },
            ]
            catalog["claims"][0]["source_refs"] = [
                "loc-longform-report-tension",
                "loc-longform-interview-turn",
                "loc-longform-report-evidence-group",
            ]
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

            subprocess.run(
                ["python3", "scripts/readerlab.py", "render-contract-package", str(fixture), str(output_root)],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = (output_root / "reader/02_章节正文陪读.md").read_text(encoding="utf-8")

        first_report = text.index("信息量增加并没有自动带来判断质量")
        interview = text.index("新人只看会议纪要")
        second_report = text.index("第一组证据来自周会纪要")
        self.assertLess(first_report, interview)
        self.assertLess(interview, second_report)

    def test_renderer_preserves_adjacent_same_source_units(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            output_root = Path(tmp) / "output"
            shutil.copytree(FIXTURE, fixture)
            catalog_path = fixture / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["catalog"]["reading_units"] = [
                {
                    "unit_id": "report-opening",
                    "title": "报告开头",
                    "status": "sample_argument_unit",
                    "source_refs": ["loc-longform-report-tension"],
                },
                {
                    "unit_id": "report-evidence",
                    "title": "报告证据组",
                    "status": "sample_argument_unit",
                    "source_refs": ["loc-longform-report-evidence-group"],
                },
            ]
            catalog["claims"][0]["source_refs"] = [
                "loc-longform-report-tension",
                "loc-longform-report-evidence-group",
            ]
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

            subprocess.run(
                ["python3", "scripts/readerlab.py", "render-contract-package", str(fixture), str(output_root)],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = (output_root / "reader/02_章节正文陪读.md").read_text(encoding="utf-8")

        first_title = text.index("### 报告开头")
        second_title = text.index("### 报告证据组")
        self.assertLess(first_title, second_title)
        self.assertLess(text.index("信息量增加并没有自动带来判断质量", first_title), second_title)
        self.assertIn("第一组证据来自周会纪要", text[second_title:])
        self.assertNotIn("信息量增加并没有自动带来判断质量", text[second_title:])

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
