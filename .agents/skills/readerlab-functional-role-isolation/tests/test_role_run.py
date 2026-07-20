from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "role_run.py"


class RoleRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir="/private/tmp")
        self.root = Path(self.temporary.name)
        self.inputs = self.root / "inputs"
        self.inputs.mkdir()
        (self.inputs / "source.md").write_text(
            "FICTIONAL TEST MATERIAL\n阿蓝星有两个月亮。\n", encoding="utf-8"
        )
        (self.inputs / "brief.md").write_text(
            "写出材料中的事实。PRIVATE-MARKER-7Q\n", encoding="utf-8"
        )
        (self.inputs / "rubric.md").write_text(
            "若候选准确陈述材料事实则 PASS，否则 FAIL。\n", encoding="utf-8"
        )
        self.run = self.root / "run"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def command(self, *arguments: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )
        if ok and completed.returncode != 0:
            self.fail(f"command failed: {completed.stderr}")
        if not ok and completed.returncode == 0:
            self.fail(f"command unexpectedly passed: {completed.stdout}")
        return completed

    def initialize(self) -> None:
        self.command(
            "init",
            "--run",
            str(self.run),
            "--source",
            str(self.inputs / "source.md"),
            "--brief",
            str(self.inputs / "brief.md"),
            "--rubric",
            str(self.inputs / "rubric.md"),
            "--candidate-id",
            "fictional-001",
        )

    def write_candidate(self, **updates: object) -> None:
        value: dict[str, object] = {
            "schema": "readerlab-functional-candidate/v1",
            "candidate_id": "fictional-001",
            "claim": "阿蓝星有两个月亮。",
            "evidence": ["虚构材料明确说阿蓝星有两个月亮。"],
        }
        value.update(updates)
        path = self.run / "producer/output/candidate.json"
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def write_judgment(self, **updates: object) -> None:
        value: dict[str, object] = {
            "schema": "readerlab-functional-judgment/v1",
            "candidate_id": "fictional-001",
            "verdict": "PASS",
            "reasons": ["候选与虚构材料一致。"],
        }
        value.update(updates)
        path = self.run / "judge/output/judgment.json"
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def seal_candidate(self) -> None:
        self.command("seal-candidate", "--run", str(self.run))

    def seal_judgment(self) -> None:
        self.command("seal-judgment", "--run", str(self.run))

    def full_run(self) -> None:
        self.initialize()
        self.write_candidate()
        self.seal_candidate()
        self.write_judgment()
        self.seal_judgment()
        self.command(
            "score",
            "--run",
            str(self.run),
            "--expected-verdict",
            "PASS",
        )

    def test_normal_flow_passes_and_verifies(self) -> None:
        self.full_run()
        completed = self.command("verify", "--run", str(self.run))
        self.assertEqual(json.loads(completed.stdout)["result"], "PASS")

    def test_candidate_is_sealed_before_handoff(self) -> None:
        self.initialize()
        self.write_candidate()
        self.seal_candidate()
        seal = json.loads(
            (self.run / "producer/candidate-seal.json").read_text(encoding="utf-8")
        )
        handoff = json.loads(
            (self.run / "judge/candidate-handoff.json").read_text(encoding="utf-8")
        )
        self.assertLess(seal["sealed_at_ns"], handoff["created_at_ns"])

    def test_existing_run_is_not_overwritten(self) -> None:
        self.initialize()
        completed = self.command(
            "init",
            "--run",
            str(self.run),
            "--source",
            str(self.inputs / "source.md"),
            "--brief",
            str(self.inputs / "brief.md"),
            "--rubric",
            str(self.inputs / "rubric.md"),
            "--candidate-id",
            "fictional-001",
            ok=False,
        )
        self.assertIn("refusing to overwrite", completed.stderr)

    def test_symlink_is_rejected(self) -> None:
        self.initialize()
        candidate = self.run / "producer/output/candidate.json"
        candidate.symlink_to(self.inputs / "source.md")
        completed = self.command(
            "seal-candidate", "--run", str(self.run), ok=False
        )
        self.assertIn("symlink is forbidden", completed.stderr)

    def test_candidate_extra_field_is_rejected(self) -> None:
        self.initialize()
        self.write_candidate(extra="forbidden")
        completed = self.command(
            "seal-candidate", "--run", str(self.run), ok=False
        )
        self.assertIn("fields must be exactly", completed.stderr)

    def test_candidate_id_mismatch_is_rejected(self) -> None:
        self.initialize()
        self.write_candidate(candidate_id="wrong-id")
        completed = self.command(
            "seal-candidate", "--run", str(self.run), ok=False
        )
        self.assertIn("candidate ID mismatch", completed.stderr)

    def test_judgment_cannot_be_sealed_before_candidate(self) -> None:
        self.initialize()
        self.write_judgment()
        completed = self.command(
            "seal-judgment", "--run", str(self.run), ok=False
        )
        self.assertIn("required run files are missing", completed.stderr)

    def test_hidden_key_before_judgment_is_rejected(self) -> None:
        self.initialize()
        self.write_candidate()
        hidden = self.run / "scorer/hidden-key.json"
        hidden.write_text('{"expected_verdict":"PASS"}', encoding="utf-8")
        completed = self.command(
            "seal-candidate", "--run", str(self.run), ok=False
        )
        self.assertIn("unexpected run files", completed.stderr)

    def test_modified_candidate_handoff_is_rejected(self) -> None:
        self.initialize()
        self.write_candidate()
        self.seal_candidate()
        handoff = self.run / "judge/input/candidate.json"
        handoff.write_text(
            handoff.read_text(encoding="utf-8") + "\n", encoding="utf-8"
        )
        self.write_judgment()
        completed = self.command(
            "seal-judgment", "--run", str(self.run), ok=False
        )
        self.assertIn("mismatch", completed.stderr)

    def test_modified_receipt_fails_verify(self) -> None:
        self.full_run()
        receipt_path = self.run / "receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["mechanical_comparison"]["result"] = "FAIL"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        completed = self.command("verify", "--run", str(self.run), ok=False)
        self.assertIn("receipt does not match", completed.stderr)


if __name__ == "__main__":
    unittest.main()
