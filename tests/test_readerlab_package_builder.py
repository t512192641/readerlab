import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_readerlab_package.py"


def run_builder(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        check=True,
        text=True,
        capture_output=True,
    )


class ReaderLabPackageBuilderTests(unittest.TestCase):
    def test_builds_shareable_package_with_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_builder("--output-dir", tmp)
            payload = json.loads(result.stdout)
            package_root = Path(tmp) / payload["package_root"]

            self.assertEqual(payload["status"], "shareable_package_prepared")
            self.assertTrue((package_root / "SKILL.md").is_file())
            self.assertTrue((package_root / "checks/readiness-checklist.md").is_file())
            self.assertTrue((package_root / "evals/output-cases.json").is_file())
            self.assertTrue((package_root / "examples/run-config-example.json").is_file())
            self.assertTrue((package_root / "scripts/readerlab.py").is_file())
            self.assertTrue((package_root / "scripts/readerlab_trace_validator.py").is_file())
            self.assertTrue((package_root / "tests/package_smoke_test.py").is_file())
            self.assertTrue((package_root / "docs/product-spec.md").is_file())
            self.assertTrue((package_root / "docs/readerlab-v2-runtime-config.md").is_file())
            self.assertTrue((package_root / "contracts/trace-validation-v1.md").is_file())
            self.assertTrue((package_root / "fixtures/contract-validator-proof-v0/README.md").is_file())
            self.assertTrue((package_root / "PACKAGE_BOUNDARY.md").is_file())
            self.assertTrue((package_root / "PACKAGE_AUDIT.json").is_file())

            audit = json.loads((package_root / "PACKAGE_AUDIT.json").read_text(encoding="utf-8"))
            self.assertEqual(audit["status"], "pass")
            self.assertTrue(audit["not_reader_acceptance"])
            self.assertTrue(audit["not_production_ready"])
            self.assertFalse(audit["failures"])
            audit_paths = {file["path"] for file in audit["files"]}
            self.assertIn("PACKAGE_MANIFEST.json", audit_paths)
            self.assertEqual(audit["audit_file"], "PACKAGE_AUDIT.json")

            package_manifest = json.loads((package_root / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertEqual(package_manifest["package_root"], "readerlab")
            manifest_text = json.dumps(package_manifest, ensure_ascii=False)
            self.assertNotIn("/Users/", manifest_text)
            self.assertNotIn("/private/", manifest_text)
            self.assertNotIn("/tmp/", manifest_text)
            self.assertNotIn("/workspace/", manifest_text)

            smoke = subprocess.run(
                ["python3", str(package_root / "tests/package_smoke_test.py")],
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertIn("PASS ReaderLab package smoke", smoke.stdout)

    def test_package_excludes_reports_and_private_demo_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_builder("--output-dir", tmp)
            package_root = Path(tmp) / "readerlab"
            package_paths = {path.relative_to(package_root).as_posix() for path in package_root.rglob("*") if path.is_file()}

            self.assertFalse(any(path.startswith("docs/reports/") for path in package_paths))
            self.assertFalse(any("private-material-validation" in path for path in package_paths))
            self.assertFalse(any(path.startswith("fixtures/comment-replay/") for path in package_paths))
            self.assertFalse(any("experiments/" in path for path in package_paths))

    def test_package_sanitizes_local_paths_and_external_fixture_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_builder("--output-dir", tmp)
            package_root = Path(tmp) / "readerlab"
            combined = "\n".join(
                path.read_text(encoding="utf-8")
                for path in sorted(package_root.rglob("*"))
                if path.is_file() and path.suffix in {".md", ".json", ".py"}
            )

            self.assertNotIn("/Users/", combined)
            self.assertNotIn("技能项目/skills-canonical/packages/gstack", combined)
            self.assertNotIn(
                "python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation",
                combined,
            )
            self.assertIn("shareable_package_prepared", combined)

    def test_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_builder("--output-dir", tmp)
            result = subprocess.run(
                ["python3", str(SCRIPT), "--output-dir", tmp],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("pass --force", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
