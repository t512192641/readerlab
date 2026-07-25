from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_REGISTER = ROOT / "audit/ASSET-LIFECYCLE-REGISTER.md"


class RepositoryAuditGuardrailTests(unittest.TestCase):
    def test_asset_register_exhaustively_lists_taskcards_and_runs(self) -> None:
        text = ASSET_REGISTER.read_text(encoding="utf-8")

        recorded_taskcards = set(
            re.findall(r"`(taskcards/[A-Za-z0-9.-]+\.md)`", text)
        )
        actual_taskcards = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "taskcards").glob("*.md")
        }
        self.assertEqual(recorded_taskcards, actual_taskcards)

        recorded_runs = set(re.findall(r"`(runs/[A-Za-z0-9.-]+)`", text))
        actual_runs = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "runs").iterdir()
            if path.is_dir()
        }
        self.assertEqual(recorded_runs, actual_runs)

        recorded_docs = set(
            re.findall(r"`((?!taskcards/|runs/|examples/)[A-Za-z0-9_./-]+\.md)`", text)
        )
        actual_docs = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*.md")
            if ".git" not in path.parts
            and "runs" not in path.parts
            and "taskcards" not in path.parts
            and "examples" not in path.parts
        }
        self.assertEqual(recorded_docs, actual_docs)

    def test_root_readme_is_navigation_not_historical_state_dump(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertLessEqual(len(readme.splitlines()), 80)
        self.assertIn("CURRENT-STATE.md", readme)
        self.assertIn("ASSET-LIFECYCLE-REGISTER.md", readme)
        recovery_object = "b39a284c10e09ad03b9af8b4899aea34f9b64dc1:README.md"
        self.assertIn(recovery_object.split(":", 1)[0], readme)
        recovery = subprocess.run(
            ["git", "cat-file", "-e", recovery_object],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(recovery.returncode, 0, recovery.stderr)
        for target in re.findall(r"\]\(([^)]+)\)", readme):
            self.assertTrue((ROOT / target).is_file(), target)

    def test_taskcard_template_keeps_known_cost_guardrails(self) -> None:
        template = (ROOT / "taskcards/TEMPLATE.md").read_text(encoding="utf-8")

        self.assertIn("Web Search + Web Fetch", template)
        self.assertIn("禁止 Chrome remote debugging", template)
        self.assertIn("超过 2 个不纳入仓库的临时脚本", template)


if __name__ == "__main__":
    unittest.main()
