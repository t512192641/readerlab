import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_readerlab_package.py"
INSTALL_SMOKE = ROOT / "packaging" / "install_smoke_test.py"


def build_package(output_dir: Path) -> Path:
    result = subprocess.run(
        ["python3", str(BUILD_SCRIPT), "--output-dir", str(output_dir), "--force"],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)
    return output_dir / payload["package_root"]


class ReaderLabInstallSmokeTests(unittest.TestCase):
    def test_installs_discovers_and_runs_minimal_config_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            package_root = build_package(tmp_path / "build")
            install_root = tmp_path / "skills"

            result = subprocess.run(
                [
                    "python3",
                    str(INSTALL_SMOKE),
                    "--package-root",
                    str(package_root),
                    "--install-root",
                    str(install_root),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(result.stdout)

            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["check_class"], "install_discovery_smoke")
            self.assertTrue(payload["not_reader_acceptance"])
            self.assertTrue(payload["not_production_ready"])
            self.assertEqual(payload["installed_skill_root"], "readerlab")
            self.assertEqual(payload["discovery"]["name"], "readerlab")
            self.assertEqual(payload["discovery"]["entry"], "readerlab/SKILL.md")
            self.assertEqual(payload["commands"]["runtime_config"]["returncode"], 0)
            self.assertTrue((install_root / "readerlab/SKILL.md").is_file())

    def test_reports_install_phase_when_skill_entry_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            package_root = build_package(tmp_path / "build")
            broken_package = tmp_path / "broken-readerlab"
            shutil.copytree(package_root, broken_package)
            (broken_package / "SKILL.md").unlink()

            result = subprocess.run(
                [
                    "python3",
                    str(INSTALL_SMOKE),
                    "--package-root",
                    str(broken_package),
                    "--install-root",
                    str(tmp_path / "skills"),
                ],
                check=False,
                text=True,
                capture_output=True,
            )
            payload = json.loads(result.stdout)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "fail")
            self.assertEqual(payload["failed_phase"], "install")
            self.assertIn("SKILL.md", payload["message"])

    def test_reports_discovery_phase_when_skill_name_is_wrong(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            package_root = build_package(tmp_path / "build")
            broken_package = tmp_path / "broken-readerlab"
            shutil.copytree(package_root, broken_package)
            skill_file = broken_package / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8").replace("name: readerlab", "name: wrong-readerlab", 1),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    "python3",
                    str(INSTALL_SMOKE),
                    "--package-root",
                    str(broken_package),
                    "--install-root",
                    str(tmp_path / "skills"),
                ],
                check=False,
                text=True,
                capture_output=True,
            )
            payload = json.loads(result.stdout)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "fail")
            self.assertEqual(payload["failed_phase"], "discovery")
            self.assertIn("expected skill name", payload["message"])

    def test_blocks_codex_home_skill_root_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            package_root = build_package(tmp_path / "build")
            codex_home = tmp_path / "codex-home"
            env = os.environ.copy()
            env["CODEX_HOME"] = str(codex_home)

            result = subprocess.run(
                [
                    "python3",
                    str(INSTALL_SMOKE),
                    "--package-root",
                    str(package_root),
                    "--install-root",
                    str(codex_home / "skills"),
                    "--force",
                ],
                check=False,
                text=True,
                capture_output=True,
                env=env,
            )
            payload = json.loads(result.stdout)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "fail")
            self.assertEqual(payload["failed_phase"], "install")
            self.assertIn("global Codex Skill directory", payload["message"])
            self.assertFalse((codex_home / "skills/readerlab").exists())


if __name__ == "__main__":
    unittest.main()
