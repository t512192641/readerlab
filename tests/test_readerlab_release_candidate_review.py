import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_SCRIPT = ROOT / "packaging" / "release_candidate_review.py"
BUILD_SCRIPT = ROOT / "scripts" / "build_readerlab_package.py"
REVIEW_SPEC = importlib.util.spec_from_file_location("release_candidate_review", REVIEW_SCRIPT)
assert REVIEW_SPEC is not None
release_candidate_review = importlib.util.module_from_spec(REVIEW_SPEC)
assert REVIEW_SPEC.loader is not None
REVIEW_SPEC.loader.exec_module(release_candidate_review)


class ReaderLabReleaseCandidateReviewTests(unittest.TestCase):
    def test_repo_release_candidate_review_reaches_scoped_rc_status(self) -> None:
        result = subprocess.run(
            ["python3", str(REVIEW_SCRIPT)],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        payload = json.loads(result.stdout)

        self.assertEqual(payload["status"], "installable_release_candidate")
        self.assertEqual(payload["check_class"], "release_candidate_review")
        self.assertTrue(payload["not_production_ready"])
        self.assertTrue(payload["not_reader_acceptance"])
        self.assertEqual(payload["clean_package_audit"]["status"], "pass")
        self.assertEqual(payload["install_discovery_smoke"]["status"], "pass")
        self.assertEqual(payload["route_smokes"]["book"]["verification_layers"]["reader_evaluation"], "machine_smoke_only")
        self.assertEqual(
            payload["route_smokes"]["longform_report_interview"]["verification_layers"]["reader_evaluation"],
            "machine_smoke_only",
        )
        self.assertEqual(
            payload["route_smokes"]["skill_engineering"]["verification_layers"]["blocking_controller"],
            "pass",
        )
        self.assertEqual(payload["human_review"], "not_run")
        self.assertIn("installable_release_candidate only", payload["status_scope"])
        self.assertEqual(payload["anti_regression"]["private_or_local_package_pollution"], "blocked_by_clean_package_audit")

    def test_built_package_contains_release_candidate_review_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["python3", str(BUILD_SCRIPT), "--output-dir", tmp, "--force"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            package_root = Path(tmp) / "readerlab"

            self.assertTrue((package_root / "tests/release_candidate_review.py").is_file())
            self.assertTrue((package_root / "tests/install_smoke_test.py").is_file())
            self.assertTrue((package_root / "docs/readerlab-v2-release-candidate-review.md").is_file())

            smoke = subprocess.run(
                ["python3", "tests/package_smoke_test.py"],
                cwd=package_root,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertIn("PASS ReaderLab package smoke", smoke.stdout)

            rc = subprocess.run(
                ["python3", "tests/release_candidate_review.py"],
                cwd=package_root,
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(rc.stdout)
            self.assertEqual(payload["status"], "installable_release_candidate")
            self.assertEqual(payload["review_mode"], "built_package_self_review")

    def test_built_package_self_review_rejects_files_added_after_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["python3", str(BUILD_SCRIPT), "--output-dir", tmp, "--force"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            package_root = Path(tmp) / "readerlab"
            leak_path = package_root / "docs" / "reports" / "leak.md"
            leak_path.parent.mkdir(parents=True)
            leak_path.write_text("should not ship", encoding="utf-8")

            rc = subprocess.run(
                ["python3", "tests/release_candidate_review.py"],
                cwd=package_root,
                check=False,
                text=True,
                capture_output=True,
            )
            payload = json.loads(rc.stdout)

            self.assertNotEqual(rc.returncode, 0)
            self.assertEqual(payload["status"], "fail")
            self.assertEqual(payload["failed_phase"], "clean_package_audit")
            self.assertIn("forbidden package path marker", payload["message"])

    def test_built_package_self_review_rejects_audited_file_changed_after_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["python3", str(BUILD_SCRIPT), "--output-dir", tmp, "--force"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            package_root = Path(tmp) / "readerlab"
            skill_file = package_root / "SKILL.md"
            skill_file.write_text(skill_file.read_text(encoding="utf-8") + "\n/Users/example/leak\n", encoding="utf-8")

            rc = subprocess.run(
                ["python3", "tests/release_candidate_review.py"],
                cwd=package_root,
                check=False,
                text=True,
                capture_output=True,
            )
            payload = json.loads(rc.stdout)

            self.assertNotEqual(rc.returncode, 0)
            self.assertEqual(payload["status"], "fail")
            self.assertEqual(payload["failed_phase"], "clean_package_audit")
            self.assertIn("audited package file changed after audit", payload["message"])

    def test_route_summary_rejects_failed_contract_layers(self) -> None:
        payload = {
            "status": "pass",
            "check_class": "book_route_smoke",
            "not_reader_acceptance": True,
            "not_production_ready": True,
            "verification_layers": {
                "configuration_structure": "pass",
                "runner_contract": "fail",
                "quality_gate_request": "pass",
                "reader_evaluation": "machine_smoke_only",
                "human_acceptance": "not_run",
            },
        }

        with self.assertRaises(release_candidate_review.ReviewFailure) as failure:
            release_candidate_review.summarize_route("book", payload, phase="book_route")

        self.assertIn("runner_contract", failure.exception.message)


if __name__ == "__main__":
    unittest.main()
