from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
RUN_SCRIPT = SKILL_DIR / "scripts/run.py"
ROOT = SKILL_DIR.parents[2]
FIXTURE = SKILL_DIR / "tests/fixtures/t2.38-replay.json"


def invoke(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", os.fspath(RUN_SCRIPT), *(os.fspath(arg) for arg in args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class ExpertTeachingSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def make_inputs(self) -> tuple[Path, Path, Path, Path]:
        source = self.root / "source.md"
        framework = self.root / "framework.md"
        source_map = self.root / "source-map.md"
        run = self.root / "runs" / "sample-01"
        source.write_text("<h1>Fixed source</h1><p>A fixed case.</p>", encoding="utf-8")
        framework.write_text("Fixed Framework\nIdentity only.\n", encoding="utf-8")
        source_map.write_text("# Frozen sources\n- https://example.test/primary\n", encoding="utf-8")
        return source, framework, source_map, run

    def init_run(self) -> Path:
        source, framework, source_map, run = self.make_inputs()
        result = invoke(
            "init",
            "--source",
            source,
            "--framework",
            framework,
            "--source-map",
            source_map,
            "--run",
            run,
            "--skill-version",
            "0.1.0",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((run / "run.json").is_file())
        self.assertTrue((run / "control/stage-freezes/stage-0.sha256").is_file())
        return run

    def write_expert(self, run: Path, body: str = "# Teaching\nA complete course.\n") -> None:
        (run / "raw/expert-teaching-draft.md").write_text(body, encoding="utf-8")
        (run / "raw/expert-teaching-source-map.md").write_text(
            "| claim | source | ownership |\n|---|---|---|\n| core | frozen | original |\n",
            encoding="utf-8",
        )

    def seal_expert(self, run: Path, agent: str = "expert-1") -> subprocess.CompletedProcess[str]:
        return invoke(
            "seal-expert",
            "--run",
            run,
            "--agent-id",
            agent,
            "--model",
            "test-model",
            "--reasoning",
            "medium",
            "--network",
            "no",
        )

    def write_review(self, run: Path, fidelity: str = "SOURCE_FIDELITY_PASS", teaching: str = "TEACHING_PASS") -> None:
        (run / "acceptance/expert-teaching-review.md").write_text(
            f"SOURCE_FIDELITY_FINAL: {fidelity}\nTEACHING_FINAL: {teaching}\n\nEvidence.\n",
            encoding="utf-8",
        )

    def seal_review(self, run: Path, reviewer: str = "reviewer-1") -> subprocess.CompletedProcess[str]:
        return invoke(
            "seal-review",
            "--run",
            run,
            "--reviewer-id",
            reviewer,
            "--model",
            "test-model",
            "--reasoning",
            "medium",
            "--network",
            "no",
        )

    def test_init_and_existing_run_refuse_overwrite(self) -> None:
        run = self.init_run()
        source, framework, source_map, _ = self.make_inputs()
        result = invoke(
            "init",
            "--source",
            source,
            "--framework",
            framework,
            "--source-map",
            source_map,
            "--run",
            run,
            "--skill-version",
            "0.1.0",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("overwrite", result.stderr)

    def test_incomplete_expert_output_fails_without_stage_freeze(self) -> None:
        run = self.init_run()
        (run / "raw/expert-teaching-draft.md").write_text("draft", encoding="utf-8")
        result = self.seal_expert(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run / "control/stage-freezes/stage-1.sha256").exists())

    def test_input_hash_drift_fails_verify(self) -> None:
        run = self.init_run()
        (run / "inputs/source.md").write_text("changed", encoding="utf-8")
        result = invoke("verify", "--run", run)
        self.assertNotEqual(result.returncode, 0)
        self.assertRegex(result.stderr, r"(?:input hash drift|freeze hash drift)")

    def test_prompt_hash_drift_fails_verify(self) -> None:
        run = self.init_run()
        (run / "control/expert-task.md").write_text("changed prompt", encoding="utf-8")
        result = invoke("verify", "--run", run)
        self.assertNotEqual(result.returncode, 0)
        self.assertRegex(result.stderr, r"(?:Prompt/template hash drift|freeze hash drift)")

    def test_same_agent_id_is_rejected(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run, "same-agent").returncode, 0)
        self.write_review(run)
        result = self.seal_review(run, "same-agent")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("different", result.stderr)

    def test_non_dual_pass_cannot_build_product(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(run, "RETURN_EXPERT_SOURCE", "TEACHING_PASS")
        self.assertEqual(self.seal_review(run).returncode, 0)
        result = invoke("build-product-pack", "--run", run)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run / "acceptance/expert-product-review.md").exists())

    def test_malformed_review_terminal_fails_seal(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        (run / "acceptance/expert-teaching-review.md").write_text("not a terminal\n", encoding="utf-8")
        result = self.seal_review(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run / "control/stage-freezes/stage-2.sha256").exists())

    def test_dual_pass_builds_readable_product_without_leaks(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(run)
        self.assertEqual(self.seal_review(run).returncode, 0)
        result = invoke("build-product-pack", "--run", run)
        self.assertEqual(result.returncode, 0, result.stderr)
        package = (run / "acceptance/expert-product-review.md").read_text(encoding="utf-8")
        self.assertNotIn("<h1>", package)
        self.assertNotIn("source-map.md", package)
        self.assertNotIn("M1", package)
        self.assertNotIn("Writer", package)
        self.assertEqual(invoke("verify", "--run", run).returncode, 0)

    def test_existing_product_package_is_never_overwritten(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(run)
        self.assertEqual(self.seal_review(run).returncode, 0)
        self.assertEqual(invoke("build-product-pack", "--run", run).returncode, 0)
        original = (run / "acceptance/expert-product-review.md").read_bytes()
        result = invoke("build-product-pack", "--run", run)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((run / "acceptance/expert-product-review.md").read_bytes(), original)

    def test_illegal_transition_is_rejected(self) -> None:
        run = self.init_run()
        self.write_review(run)
        result = self.seal_review(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REVIEW_OPEN", result.stderr)

    def test_archive_verifies_and_lists_run(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(run)
        self.assertEqual(self.seal_review(run).returncode, 0)
        self.assertEqual(invoke("build-product-pack", "--run", run).returncode, 0)
        archive = self.root / "archives" / "sample.tar.gz"
        archive.parent.mkdir()
        result = invoke("archive", "--run", run, "--output", archive)
        self.assertEqual(result.returncode, 0, result.stderr)
        with tarfile.open(archive, "r:gz") as handle:
            names = handle.getnames()
        self.assertIn("sample-01/run.json", names)

    def test_skill_fingerprint_drift_is_detected(self) -> None:
        run = self.init_run()
        state_path = run / "run.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["skill_fingerprint"]["aggregate_sha256"] = "0" * 64
        state_path.write_text(json.dumps(state), encoding="utf-8")
        result = invoke("verify", "--run", run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fingerprint", result.stderr)

    def test_t238_fixture_replay_is_mechanical(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        source = ROOT / fixture["source"]["path"]
        source_map = ROOT / fixture["source_map"]["path"]
        self.assertEqual(source.stat().st_size, 16368)
        framework = self.root / "framework.md"
        framework.write_text("艾丽斯·玛丽恩·杨（Iris Marion Young）的社会联结责任模型（Social Connection Model）\n", encoding="utf-8")
        run = self.root / "runs" / "t238-replay"
        result = invoke(
            "init",
            "--source",
            source,
            "--framework",
            framework,
            "--source-map",
            source_map,
            "--run",
            run,
            "--skill-version",
            fixture["skill_version"],
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        frozen = ROOT / fixture["run"]
        shutil.copyfile(frozen / "raw/expert-teaching-draft.md", run / "raw/expert-teaching-draft.md")
        shutil.copyfile(frozen / "raw/expert-teaching-source-map.md", run / "raw/expert-teaching-source-map.md")
        self.assertEqual(self.seal_expert(run, "t238-expert").returncode, 0)
        shutil.copyfile(frozen / "acceptance/expert-teaching-review.md", run / "acceptance/expert-teaching-review.md")
        self.assertEqual(self.seal_review(run, "t238-review").returncode, 0)
        self.assertEqual(invoke("build-product-pack", "--run", run).returncode, 0)
        self.assertEqual(invoke("verify", "--run", run).returncode, 0)
        archive = self.root / "archives" / "t238-replay.tar.gz"
        archive.parent.mkdir()
        self.assertEqual(invoke("archive", "--run", run, "--output", archive).returncode, 0)
        self.assertTrue(archive.is_file())


if __name__ == "__main__":
    unittest.main()
