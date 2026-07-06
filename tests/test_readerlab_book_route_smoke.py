import json
import importlib.util
import shutil
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

    def test_renderer_preserves_whole_chapter_body_for_book_units(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "output"
            subprocess.run(
                ["python3", "scripts/readerlab.py", "render-contract-package", str(FIXTURE), str(output_root)],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = (output_root / "reader/02_章节正文陪读.md").read_text(encoding="utf-8")

        self.assertIn("第一章先让读者停在问题本身", text)
        self.assertIn("第二章把第一章的问题继续往前推", text)
        self.assertEqual(text.count("### 第一章 先看问题，不先看答案"), 1)
        self.assertEqual(text.count("### 第二章 结构比金句更重要"), 1)

    def test_renderer_preserves_whole_chapter_body_for_book_longform_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            output_root = Path(tmp) / "output"
            shutil.copytree(FIXTURE, fixture)
            catalog_path = fixture / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["material"]["type"] = "book_longform"
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            subprocess.run(
                ["python3", "scripts/readerlab.py", "render-contract-package", str(fixture), str(output_root)],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = (output_root / "reader/02_章节正文陪读.md").read_text(encoding="utf-8")

        self.assertIn("第一章先让读者停在问题本身", text)
        self.assertEqual(text.count("### 第一章 先看问题，不先看答案"), 1)

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
