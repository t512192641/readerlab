from __future__ import annotations

import json
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
ROOT = SKILL_DIR.parents[2]
RUN_SCRIPT = SKILL_DIR / "versions/0.1.2/scripts/run.py"
CURRENT_SCRIPT = SKILL_DIR / "run-current.py"
LEGACY_SCRIPT = SKILL_DIR / "scripts/run.py"
FIXTURE = SKILL_DIR / "tests/fixtures/t2.38-replay.json"
ALLOWLIST_FIXTURE = SKILL_DIR / "tests/fixtures/t2.38-source-allowlist.json"
EXPERT_ACCESS_FIXTURE = SKILL_DIR / "tests/fixtures/t2.38-expert-source-access.json"
REVIEWER_ACCESS_FIXTURE = SKILL_DIR / "tests/fixtures/t2.38-reviewer-source-access.json"
BASELINE_010_FINGERPRINT = "4730c7392c67bd927b9d3609854141f6b8fb6297631381834d1d43275690233f"
SOURCE_ACCESS_SCHEMA = "readerlab-book-expert-teaching/source-access/v1"
SOURCE_ACCESS_AUDIT_SCOPE = "agent-declared; not a browser or OS-level network audit"


def invoke(*args: object, script: Path = RUN_SCRIPT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", os.fspath(script), *(os.fspath(arg) for arg in args)],
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

    def make_inputs(self) -> tuple[Path, Path, Path, Path, Path]:
        source = self.root / "source.md"
        framework = self.root / "framework.md"
        source_map = self.root / "source-map.md"
        allowlist = self.root / "source-allowlist.json"
        run = self.root / "runs" / "sample-01"
        source.write_text("<h1>Fixed source</h1><p>A fixed case.</p>", encoding="utf-8")
        framework.write_text("固定框架\nIdentity only.\n", encoding="utf-8")
        source_map.write_text(
            "# Frozen sources\n"
            "- https://example.test/allowed\n"
            "- https://example.test/reference\n"
            "- https://blocked.example.invalid/source\n",
            encoding="utf-8",
        )
        allowlist.write_text(
            json.dumps(
                {
                    "schema": "readerlab-book-expert-teaching/source-allowlist/v1",
                    "sources": [
                        {
                            "id": "allowed",
                            "url": "https://example.test/allowed",
                            "status": "allowed",
                            "redirects": ["https://example.test/allowed-redirect"],
                        },
                        {
                            "id": "reference",
                            "url": "https://example.test/reference",
                            "status": "reference_only",
                            "redirects": [],
                        },
                        {
                            "id": "blocked",
                            "url": "https://blocked.example.invalid/source",
                            "status": "blocked",
                            "redirects": [],
                        },
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return source, framework, source_map, allowlist, run

    def make_legacy_inputs(self) -> tuple[Path, Path, Path, Path]:
        source = self.root / "legacy-source.md"
        framework = self.root / "legacy-framework.md"
        source_map = self.root / "legacy-source-map.md"
        run = self.root / "runs" / "legacy-01"
        source.write_text("Legacy source\n", encoding="utf-8")
        framework.write_text("Legacy framework\n", encoding="utf-8")
        source_map.write_text("Frozen legacy source map with no URL.\n", encoding="utf-8")
        return source, framework, source_map, run

    def init_run(
        self,
        script: Path = RUN_SCRIPT,
        version: str = "0.1.2",
        run_name: str = "sample-01",
    ) -> Path:
        source, framework, source_map, allowlist, run = self.make_inputs()
        run = self.root / "runs" / run_name
        args = [
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
            version,
        ]
        args.extend(["--source-allowlist", allowlist])
        result = invoke(*args, script=script)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((run / "run.json").is_file())
        self.assertTrue((run / "control/stage-freezes/stage-0.sha256").is_file())
        return run

    def write_expert(
        self,
        run: Path,
        body: str = "# 教学\n完整课程。\n",
        source_map: str | None = None,
        access: dict[str, object] | None = None,
    ) -> None:
        (run / "raw/expert-teaching-draft.md").write_text(body, encoding="utf-8")
        (run / "raw/expert-teaching-source-map.md").write_text(
            source_map or "| claim | source | ownership |\n|---|---|---|\n| core | frozen | original |\n",
            encoding="utf-8",
        )
        self.write_expert_access(run, access)

    def write_expert_access(self, run: Path, access: dict[str, object] | None = None) -> None:
        value = access or {
            "schema": SOURCE_ACCESS_SCHEMA,
            "opened_urls": ["https://example.test/allowed"],
            "cited_only_urls": ["https://example.test/reference"],
            "provenance": "agent_declared",
            "audit_scope": SOURCE_ACCESS_AUDIT_SCOPE,
        }
        (run / "raw/expert-source-access.json").write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    def seal_expert(self, run: Path, agent: str = "expert-1", script: Path = RUN_SCRIPT) -> subprocess.CompletedProcess[str]:
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
            script=script,
        )

    def write_review(
        self,
        run: Path,
        fidelity: str = "SOURCE_FIDELITY_PASS",
        teaching: str = "TEACHING_PASS",
        body: str = "Evidence.\n",
        access: dict[str, object] | None = None,
    ) -> None:
        (run / "acceptance/expert-teaching-review.md").write_text(
            f"SOURCE_FIDELITY_FINAL: {fidelity}\nTEACHING_FINAL: {teaching}\n\n{body}",
            encoding="utf-8",
        )
        value = access or {
            "schema": SOURCE_ACCESS_SCHEMA,
            "opened_urls": ["https://example.test/allowed"],
            "cited_only_urls": ["https://example.test/reference"],
            "provenance": "agent_declared",
            "audit_scope": SOURCE_ACCESS_AUDIT_SCOPE,
        }
        (run / "acceptance/reviewer-source-access.json").write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    def seal_review(self, run: Path, reviewer: str = "reviewer-1", script: Path = RUN_SCRIPT) -> subprocess.CompletedProcess[str]:
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
            script=script,
        )

    def test_init_and_existing_run_refuse_overwrite(self) -> None:
        run = self.init_run()
        source, framework, source_map, allowlist, _ = self.make_inputs()
        result = invoke(
            "init",
            "--source",
            source,
            "--framework",
            framework,
            "--source-map",
            source_map,
            "--source-allowlist",
            allowlist,
            "--run",
            run,
            "--skill-version",
            "0.1.2",
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

    def test_allowlist_statuses_are_structured_and_reference_only_is_not_task_permission(self) -> None:
        run = self.init_run()
        task = (run / "control/expert-task.md").read_text(encoding="utf-8")
        read_set = json.loads((run / "control/expert-read-set.json").read_text(encoding="utf-8"))
        self.assertIn("https://example.test/allowed", task)
        self.assertIn("https://example.test/allowed-redirect", task)
        self.assertNotIn("https://example.test/reference", task)
        self.assertNotIn("https://blocked.example.invalid/source", task)
        self.assertEqual(read_set["source_status_counts"], {"allowed": 1, "blocked": 1, "reference_only": 1})

    def test_invalid_allowlist_schema_is_rejected(self) -> None:
        source, framework, source_map, allowlist, run = self.make_inputs()
        value = json.loads(allowlist.read_text(encoding="utf-8"))
        value["schema"] = "wrong/schema"
        allowlist.write_text(json.dumps(value), encoding="utf-8")
        result = invoke(
            "init",
            "--source", source,
            "--framework", framework,
            "--source-map", source_map,
            "--source-allowlist", allowlist,
            "--run", run,
            "--skill-version", "0.1.2",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema", result.stderr)
        self.assertFalse(run.exists())

    def test_allowlist_unknown_fields_are_rejected(self) -> None:
        source, framework, source_map, allowlist, run = self.make_inputs()
        value = json.loads(allowlist.read_text(encoding="utf-8"))
        value["sources"][0]["implicit_domain_redirect"] = "https://other.example.invalid"
        allowlist.write_text(json.dumps(value), encoding="utf-8")
        result = invoke(
            "init",
            "--source", source,
            "--framework", framework,
            "--source-map", source_map,
            "--source-allowlist", allowlist,
            "--run", run,
            "--skill-version", "0.1.2",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown fields", result.stderr)
        self.assertFalse(run.exists())

    def test_expert_new_url_is_rejected(self) -> None:
        run = self.init_run()
        self.write_expert(run, source_map="New claim: https://new.example.invalid/not-registered\n")
        result = self.seal_expert(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unregistered", result.stderr)
        self.assertFalse((run / "control/stage-freezes/stage-1.sha256").exists())

    def test_reference_only_url_can_be_cited_but_blocked_url_cannot(self) -> None:
        run = self.init_run()
        self.write_expert(run, source_map="Audit citation: https://example.test/reference\n")
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(
            run,
            body="Reference: https://blocked.example.invalid/source\n",
        )
        result = self.seal_review(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("blocked", result.stderr)

    def test_reviewer_new_url_is_rejected(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(run, body="New review source: https://new.example.invalid/not-registered\n")
        result = self.seal_review(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unregistered", result.stderr)

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

    def test_dual_pass_builds_readable_product_and_allows_natural_keywords(self) -> None:
        run = self.init_run()
        self.write_expert(run, body="# 教学\n正文自然提到 M1、M2、M3 和 Writer。\n")
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(run)
        self.assertEqual(self.seal_review(run).returncode, 0)
        result = invoke("build-product-pack", "--run", run)
        self.assertEqual(result.returncode, 0, result.stderr)
        package = (run / "acceptance/expert-product-review.md").read_text(encoding="utf-8")
        self.assertNotIn("<h1>", package)
        self.assertIn("M1、M2、M3 和 Writer", package)
        self.assertNotIn("结构性或同类问题", package)
        self.assertIn("另一个适用情境", package)
        self.assertEqual(invoke("verify", "--run", run).returncode, 0)

    def test_internal_metadata_leakage_is_rejected(self) -> None:
        run = self.init_run()
        self.write_expert(run, body="# 教学\n内部字段 stage-1.sha256 不应进入产品包。\n")
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(run)
        self.assertEqual(self.seal_review(run).returncode, 0)
        result = invoke("build-product-pack", "--run", run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("forbidden", result.stderr)
        self.assertFalse((run / "acceptance/expert-product-review.md").exists())

    def test_chinese_expression_rules_are_in_generated_expert_task(self) -> None:
        run = self.init_run()
        task = (run / "control/expert-task.md").read_text(encoding="utf-8")
        for phrase in ("默认使用中文", "中文译名（英文原名）", "中文名称（英文名称）", "普通中文", "教学整理不等于原作者正式命名的方法"):
            self.assertIn(phrase, task)
        self.assertIn("raw/expert-source-access.json", task)
        self.assertIn(SOURCE_ACCESS_SCHEMA, task)
        self.assertIn("agent_declared", task)

    def test_metadata_uses_controller_declared_provenance(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        state = json.loads((run / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(state["expert"]["metadata_provenance"], "controller_declared")
        manifest = (run / "run-manifest.md").read_text(encoding="utf-8")
        ledger = (run / "run-ledger.md").read_text(encoding="utf-8")
        self.assertIn("semantic calls invoked by this Skill: `none`", manifest)
        self.assertIn("external semantic contexts: `controller_declared`", manifest)
        self.assertIn("production integration: `not_integrated`", manifest)
        self.assertIn("inputs/source-allowlist.json", manifest)
        self.assertIn("provenance: `controller_declared`", ledger)

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
        self.assertIn("sample-01/raw/expert-source-access.json", names)
        self.assertIn("sample-01/acceptance/reviewer-source-access.json", names)
        with tarfile.open(archive, "r:gz") as handle:
            for relative in ("raw/expert-source-access.json", "acceptance/reviewer-source-access.json"):
                member = handle.extractfile(f"sample-01/{relative}")
                self.assertIsNotNone(member)
                assert member is not None
                self.assertEqual(hashlib.sha256(member.read()).hexdigest(), hashlib.sha256((run / relative).read_bytes()).hexdigest())

    def test_skill_fingerprint_drift_is_detected(self) -> None:
        run = self.init_run()
        state_path = run / "run.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["skill_fingerprint"]["aggregate_sha256"] = "0" * 64
        state_path.write_text(json.dumps(state), encoding="utf-8")
        result = invoke("verify", "--run", run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fingerprint", result.stderr)

    def test_010_release_fingerprint_matches_current_root_implementation(self) -> None:
        control_path = SKILL_DIR / "scripts/lib/control.py"
        spec = importlib.util.spec_from_file_location("readerlab_legacy_control", control_path)
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fingerprint = module.skill_fingerprint()
        self.assertEqual(fingerprint["aggregate_sha256"], BASELINE_010_FINGERPRINT)
        self.assertNotIn("scripts/run-current.py", {item["path"] for item in fingerprint["files"]})
        self.assertNotIn("run-current.py", {item["path"] for item in fingerprint["files"]})

    def test_old_fingerprint_file_change_is_rejected_by_010_entry(self) -> None:
        source, framework, source_map, run = self.make_legacy_inputs()
        temp_root = self.root.resolve()
        temporary_skill = temp_root / ".agents/skills/readerlab-book-expert-teaching"
        temporary_skill.parent.mkdir(parents=True)
        shutil.copytree(SKILL_DIR, temporary_skill)
        (temp_root / "tools").mkdir()
        (temp_root / "tools/__init__.py").write_text("", encoding="utf-8")
        shutil.copyfile(ROOT / "tools/run.py", temp_root / "tools/run.py")
        temporary_script = temporary_skill / "scripts/run.py"
        result = invoke(
            "init", "--source", source, "--framework", framework, "--source-map", source_map,
            "--run", run, "--skill-version", "0.1.0", script=temporary_script,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        fingerprint_file = temporary_skill / "agents/openai.yaml"
        original = fingerprint_file.read_bytes()
        fingerprint_file.write_bytes(original + b"\n")
        result = invoke("verify", "--run", run, script=temporary_script)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fingerprint", result.stderr)

    def test_source_map_unregistered_url_fails_init(self) -> None:
        source, framework, source_map, allowlist, run = self.make_inputs()
        source_map.write_text(source_map.read_text(encoding="utf-8") + "https://new.example.invalid/map\n", encoding="utf-8")
        result = invoke(
            "init", "--source", source, "--framework", framework, "--source-map", source_map,
            "--source-allowlist", allowlist, "--run", run, "--skill-version", "0.1.2",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not registered", result.stderr)
        self.assertFalse(run.exists())

    def test_allowlist_canonical_url_missing_from_source_map_fails_init(self) -> None:
        source, framework, source_map, allowlist, run = self.make_inputs()
        value = json.loads(allowlist.read_text(encoding="utf-8"))
        value["sources"].append(
            {
                "id": "extra-primary",
                "url": "https://extra.example.invalid/primary",
                "status": "allowed",
                "redirects": [],
            }
        )
        allowlist.write_text(json.dumps(value), encoding="utf-8")
        result = invoke(
            "init", "--source", source, "--framework", framework, "--source-map", source_map,
            "--source-allowlist", allowlist, "--run", run, "--skill-version", "0.1.2",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing from source map", result.stderr)
        self.assertFalse(run.exists())

    def test_access_receipt_arrays_must_be_disjoint(self) -> None:
        run = self.init_run()
        self.write_expert(
            run,
            access={
                "schema": SOURCE_ACCESS_SCHEMA,
                "opened_urls": ["https://example.test/allowed"],
                "cited_only_urls": ["https://example.test/allowed"],
                "provenance": "agent_declared",
                "audit_scope": SOURCE_ACCESS_AUDIT_SCOPE,
            },
        )
        result = self.seal_expert(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("both access arrays", result.stderr)

    def test_expert_reference_only_opened_is_rejected(self) -> None:
        run = self.init_run()
        self.write_expert(
            run,
            access={
                "schema": SOURCE_ACCESS_SCHEMA,
                "opened_urls": ["https://example.test/reference"],
                "cited_only_urls": [],
                "provenance": "agent_declared",
                "audit_scope": SOURCE_ACCESS_AUDIT_SCOPE,
            },
        )
        result = self.seal_expert(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("only allowed", result.stderr)

    def test_expert_reference_only_cited_only_is_accepted(self) -> None:
        run = self.init_run()
        self.write_expert(
            run,
            access={
                "schema": SOURCE_ACCESS_SCHEMA,
                "opened_urls": ["https://example.test/allowed"],
                "cited_only_urls": ["https://example.test/reference"],
                "provenance": "agent_declared",
                "audit_scope": SOURCE_ACCESS_AUDIT_SCOPE,
            },
        )
        self.assertEqual(self.seal_expert(run).returncode, 0)

    def test_blocked_url_in_any_access_array_is_rejected(self) -> None:
        for field in ("opened_urls", "cited_only_urls"):
            with self.subTest(field=field):
                run = self.init_run(run_name=f"sample-{field}")
                access = {
                    "schema": SOURCE_ACCESS_SCHEMA,
                    "opened_urls": [],
                    "cited_only_urls": [],
                    "provenance": "agent_declared",
                    "audit_scope": SOURCE_ACCESS_AUDIT_SCOPE,
                }
                access[field] = ["https://blocked.example.invalid/source"]
                self.write_expert(run, access=access)
                result = self.seal_expert(run)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("blocked", result.stderr)

    def test_unregistered_url_in_access_receipt_is_rejected(self) -> None:
        run = self.init_run()
        self.write_expert(
            run,
            access={
                "schema": SOURCE_ACCESS_SCHEMA,
                "opened_urls": ["https://unregistered.example.invalid/source"],
                "cited_only_urls": [],
                "provenance": "agent_declared",
                "audit_scope": SOURCE_ACCESS_AUDIT_SCOPE,
            },
        )
        result = self.seal_expert(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unregistered", result.stderr)

    def test_expert_body_unregistered_url_is_rejected(self) -> None:
        run = self.init_run()
        self.write_expert(run, body="正文 https://unregistered.example.invalid/body\n")
        result = self.seal_expert(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unregistered", result.stderr)

    def test_reviewer_access_receipt_has_same_constraints(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        self.write_review(
            run,
            access={
                "schema": SOURCE_ACCESS_SCHEMA,
                "opened_urls": ["https://example.test/reference"],
                "cited_only_urls": [],
                "provenance": "agent_declared",
                "audit_scope": SOURCE_ACCESS_AUDIT_SCOPE,
            },
        )
        result = self.seal_review(run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("only allowed", result.stderr)

    def test_access_receipt_drift_is_detected_by_verify(self) -> None:
        run = self.init_run()
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run).returncode, 0)
        access_path = run / "raw/expert-source-access.json"
        value = json.loads(access_path.read_text(encoding="utf-8"))
        value["cited_only_urls"] = []
        access_path.write_text(json.dumps(value), encoding="utf-8")
        result = invoke("verify", "--run", run)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("freeze hash drift", result.stderr)

    def test_old_version_run_survives_current_upgrade_but_wrong_version_fails(self) -> None:
        source, framework, source_map, run = self.make_legacy_inputs()
        result = invoke(
            "init", "--source", source, "--framework", framework, "--source-map", source_map,
            "--run", run, "--skill-version", "0.1.0", script=LEGACY_SCRIPT,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.write_expert(run)
        self.assertEqual(self.seal_expert(run, script=LEGACY_SCRIPT).returncode, 0)
        self.write_review(run)
        self.assertEqual(self.seal_review(run, script=LEGACY_SCRIPT).returncode, 0)
        self.assertEqual(invoke("verify", "--run", run, script=LEGACY_SCRIPT).returncode, 0)
        wrong = invoke("verify", "--run", run, script=RUN_SCRIPT)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertIn("Skill version", wrong.stderr)
        current = invoke("verify", "--run", run, script=CURRENT_SCRIPT)
        self.assertNotEqual(current.returncode, 0)
        self.assertIn("Skill version", current.stderr)

    def test_current_dispatcher_targets_012(self) -> None:
        run = self.init_run(script=CURRENT_SCRIPT)
        state = json.loads((run / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(state["skill_version"], "0.1.2")

    def _assert_fixture_hashes(self, fixture: dict[str, object]) -> None:
        for key in (
            "source",
            "source_map",
            "source_allowlist",
            "expert_draft",
            "expert_source_map",
            "expert_access",
            "review",
            "reviewer_access",
        ):
            record = fixture[key]
            assert isinstance(record, dict)
            path = ROOT / str(record["path"])
            digest = __import__("hashlib").sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, record["sha256"], key)

    def test_t238_fixture_replay_checks_all_hashes_product_identity_and_archive(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(fixture["skill_version"], "0.1.0")
        self.assertEqual(fixture["replay_skill_version"], "0.1.2")
        self._assert_fixture_hashes(fixture)
        source = ROOT / fixture["source"]["path"]
        source_map = ROOT / fixture["source_map"]["path"]
        source_allowlist = ROOT / fixture["source_allowlist"]["path"]
        framework = self.root / "framework.md"
        framework.write_text("固定框架身份\n", encoding="utf-8")
        run = self.root / "runs" / "t238-replay"
        result = invoke(
            "init", "--source", source, "--framework", framework, "--source-map", source_map,
            "--source-allowlist", source_allowlist, "--run", run, "--skill-version", "0.1.2",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        frozen = ROOT / fixture["run"]
        shutil.copyfile(frozen / "raw/expert-teaching-draft.md", run / "raw/expert-teaching-draft.md")
        shutil.copyfile(frozen / "raw/expert-teaching-source-map.md", run / "raw/expert-teaching-source-map.md")
        shutil.copyfile(ROOT / fixture["expert_access"]["path"], run / "raw/expert-source-access.json")
        self.assertEqual(self.seal_expert(run, "t238-expert").returncode, 0)
        shutil.copyfile(frozen / "acceptance/expert-teaching-review.md", run / "acceptance/expert-teaching-review.md")
        shutil.copyfile(ROOT / fixture["reviewer_access"]["path"], run / "acceptance/reviewer-source-access.json")
        self.assertEqual(self.seal_review(run, "t238-review").returncode, 0)
        self.assertEqual(invoke("build-product-pack", "--run", run).returncode, 0)
        package_sha = __import__("hashlib").sha256((run / "acceptance/expert-product-review.md").read_bytes()).hexdigest()
        self.assertEqual(package_sha, fixture["expected_product"]["v0.1.2_sha256"])
        self.assertEqual(invoke("verify", "--run", run).returncode, 0)

        before_archive = {
            f"{run.name}/{path.relative_to(run).as_posix()}"
            for path in run.rglob("*")
            if path.is_file()
        }
        archive = self.root / "archives" / "t238-replay.tar.gz"
        archive.parent.mkdir()
        self.assertEqual(invoke("archive", "--run", run, "--output", archive).returncode, 0)
        with tarfile.open(archive, "r:gz") as handle:
            self.assertEqual(set(handle.getnames()), before_archive)
            archive_hash_paths = {
                "source": "inputs/source.md",
                "source_map": "inputs/source-map.md",
                "expert_draft": "raw/expert-teaching-draft.md",
                "expert_source_map": "raw/expert-teaching-source-map.md",
                "review": "acceptance/expert-teaching-review.md",
                "expert_access": "raw/expert-source-access.json",
                "reviewer_access": "acceptance/reviewer-source-access.json",
            }
            for key, relative in archive_hash_paths.items():
                member = handle.extractfile(f"{run.name}/{relative}")
                self.assertIsNotNone(member, key)
                assert member is not None
                self.assertEqual(__import__("hashlib").sha256(member.read()).hexdigest(), fixture[key]["sha256"], key)
        for key in ("source", "source_map", "expert_draft", "expert_source_map", "expert_access", "review", "reviewer_access"):
            record = fixture[key]
            frozen_path = run / {
                "source": "inputs/source.md",
                "source_map": "inputs/source-map.md",
                "expert_draft": "raw/expert-teaching-draft.md",
                "expert_source_map": "raw/expert-teaching-source-map.md",
                "expert_access": "raw/expert-source-access.json",
                "review": "acceptance/expert-teaching-review.md",
                "reviewer_access": "acceptance/reviewer-source-access.json",
            }[key]
            digest = __import__("hashlib").sha256(frozen_path.read_bytes()).hexdigest()
            self.assertEqual(digest, record["sha256"], key)
        frozen_product = frozen / "acceptance/expert-product-review.md"
        self.assertEqual(
            __import__("hashlib").sha256(frozen_product.read_bytes()).hexdigest(),
            fixture["expected_product"]["v0.1.0_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
