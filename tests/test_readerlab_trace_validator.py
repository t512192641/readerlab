import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "readerlab_trace_validator.py"
REPORT = ROOT / "docs/reports/readerlab-comment-replay-v0"
PRIVATE_DEMOS = ROOT / "docs/reports/readerlab-private-material-validation-v0/demos"


def run_validator(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(VALIDATOR), *args],
        check=False,
        text=True,
        capture_output=True,
    )


class ReaderLabTraceValidatorTests(unittest.TestCase):
    def test_validate_suite_accepts_private_demo_trace_and_plugin_replay(self) -> None:
        result = run_validator(
            "validate-suite",
            "--demo",
            str(PRIVATE_DEMOS / "A_feel_good_productivity"),
            "--demo",
            str(PRIVATE_DEMOS / "B_planning_with_files"),
            "--cases-json",
            str(REPORT / "fixtures/comment-replay-cases.json"),
            "--fixture-dir",
            str(REPORT / "fixtures"),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["pass"])
        self.assertTrue(payload["comment_replay"]["pass"])
        self.assertEqual(payload["comment_replay"]["plugin_format"], "tandem-comments")

    def test_validate_replay_rejects_missing_anchor_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cases_path = Path(tmp) / "bad-cases.json"
            payload = json.loads((REPORT / "fixtures/comment-replay-cases.json").read_text(encoding="utf-8"))
            for replay in payload["replays"]:
                replay["demo_dir"] = str((REPORT / "fixtures" / replay["demo_dir"]).resolve())
            payload["replays"][0]["anchor_ref"] = "A-BODY-DOES-NOT-EXIST"
            cases_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = run_validator(
                "validate-replay",
                str(cases_path),
                "--fixture-dir",
                str(REPORT / "fixtures"),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing location-map anchor", result.stdout)


if __name__ == "__main__":
    unittest.main()
