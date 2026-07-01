import json
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

_READERLAB_SPEC = importlib.util.spec_from_file_location("readerlab", ROOT / "scripts" / "readerlab.py")
readerlab = importlib.util.module_from_spec(_READERLAB_SPEC)
assert _READERLAB_SPEC and _READERLAB_SPEC.loader
sys.modules[_READERLAB_SPEC.name] = readerlab
_READERLAB_SPEC.loader.exec_module(readerlab)


def run_readerlab(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(ROOT / "scripts" / "readerlab.py"), *args],
        check=True,
        text=True,
        capture_output=True,
    )


def run_readerlab_unchecked(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(ROOT / "scripts" / "readerlab.py"), *args],
        check=False,
        text=True,
        capture_output=True,
    )


class ReaderLabTests(unittest.TestCase):
    def write_comment_fixture(
        self,
        root: Path,
        *,
        skill: str = "mover",
        description: str = "诊断 审查 质量判断",
        body: str = "Alpha beta gamma.",
    ) -> tuple[Path, Path, Path]:
        source = root / "skills"
        readings_dir = root / "readings"
        (source / skill).mkdir(parents=True, exist_ok=True)
        (readings_dir / "demo").mkdir(parents=True, exist_ok=True)
        source_text = f"""---
name: {skill}
description: {description}
---

# {skill}

{body}
"""
        (source / skill / "SKILL.md").write_text(source_text, encoding="utf-8")
        (readings_dir / "demo" / f"{skill}.json").write_text(
            json.dumps(
                {
                    "schema": "readerlab.skill-reading.v1",
                    "package": "demo",
                    "skill": skill,
                    "guide": "这个样本用于测试 ReaderLab 批注保护。",
                    "skill_body_translation": source_text,
                    "related_materials_explanation": "没有额外关联材料。",
                    "highlights": "无特别高亮。",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return source, readings_dir, root / "out"

    def import_demo_pack(self, source: Path, readings_dir: Path, dest: Path, *extra: str) -> subprocess.CompletedProcess:
        return run_readerlab(
            "import-skills",
            str(source),
            "--dest",
            str(dest),
            "--book-id",
            "demo",
            "--title",
            "demo",
            "--readings-dir",
            str(readings_dir),
            *extra,
        )

    def reading_page_for_skill(self, book_dir: Path, skill: str) -> Path:
        manifest = json.loads((book_dir / "manifest.json").read_text(encoding="utf-8"))
        record = next(item for item in manifest["skills"] if item["name"] == skill)
        return book_dir / record["reading_page"]

    def write_contract_pack(self, root: Path) -> Path:
        book_dir = root / "contract-pack"
        contract_dir = book_dir / "40_全局理解"
        contract_dir.mkdir(parents=True)
        (book_dir / "10_中文精读").mkdir()
        (book_dir / "10_中文精读" / "unit.md").write_text(
            "# unit\n\n## Skill 正文\n\n已完成的机器阅读页。\n",
            encoding="utf-8",
        )
        common = {
            "material": {"id": "contract-pack", "title": "contract-pack", "type": "mixed-material"},
            "source_scope": {
                "coverage_status": "partial",
                "coverage_note": "只覆盖当前样张声明的来源范围。",
                "items": [
                    {
                        "id": "src-1",
                        "source_ref": "source.md",
                        "range": "section 1",
                        "role": "primary",
                    }
                ],
            },
            "confidence": {"level": "medium", "basis": "来源范围明确，但仍需人工复核。"},
            "review_items": [{"id": "r1", "question": "来源覆盖是否足够？", "status": "open"}],
            "machine_status": "ready",
            "human_status": "pending",
            "display": {
                "markdown_path": "40_全局理解/全局地图.md",
                "relationship": "manual_companion",
            },
        }
        global_map = {
            **common,
            "schema": "readerlab.global-map.v1",
            "global_map": {
                "core_questions": ["这份材料解决什么问题？"],
                "structure_mainline": ["先识别主线，再进入局部阅读。"],
                "unit_relationships": [],
                "concept_method_case_relationships": [],
                "reading_routes": ["先读地图，再读关键单元。"],
            },
        }
        distillation = {
            **common,
            "schema": "readerlab.distillation.v1",
            "distillation": {
                "frameworks": [],
                "principles": [],
                "cases": [],
                "counterexamples": [],
                "terms": [],
                "transferable_insights": ["候选洞察只进入草案层。"],
                "skill_candidates": [],
                "applicability_boundaries": ["不能直接升格为正式 Skill。"],
            },
        }
        (contract_dir / "global-map.json").write_text(
            json.dumps(global_map, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (contract_dir / "distillation.json").write_text(
            json.dumps(distillation, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest = {
            "schema": "readerlab.v0.1",
            "delivery_status": "deliverable",
            "status_semantics": {
                "delivery_status": "machine_pack_delivery_status",
                "machine_status": "per_item_machine_generation_and_coverage_status",
                "human_status": "manual_reading_acceptance_status_not_implied_by_delivery_status",
            },
            "coverage_policy": {
                "reading_page_structure": "main_reading_page_centered",
                "non_body_handling": "codex_absorption_with_trace",
                "reader_visible_evidence_pages": False,
            },
            "skills": [
                {
                    "name": "unit",
                    "source_file": "unit/SKILL.md",
                    "group": "01_核心入口与总览",
                    "reading_page": "10_中文精读/unit.md",
                    "status": "completed",
                    "machine_status": "completed",
                    "human_status": "pending",
                    "coverage": {},
                    "codex_absorption": {"status": "absorbed", "source_refs": ["source.md"]},
                }
            ],
            "reading_units": [{"id": "01_核心入口与总览", "status": "completed"}],
            "source_blocks": [],
            "contract_artifacts": [
                {
                    "schema": "readerlab.global-map.v1",
                    "path": "40_全局理解/global-map.json",
                    "machine_status": "ready",
                    "human_status": "pending",
                },
                {
                    "schema": "readerlab.distillation.v1",
                    "path": "40_全局理解/distillation.json",
                    "machine_status": "ready",
                    "human_status": "pending",
                },
            ],
        }
        (book_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return book_dir

    def append_test_comment(self, page: Path, comment_id: str = "c1", exact: str = "Alpha beta gamma.") -> None:
        text = page.read_text(encoding="utf-8")
        pos = text.index(exact)
        prefix = text[max(0, pos - 20) : pos]
        suffix = text[pos + len(exact) : pos + len(exact) + 20]
        data = {
            comment_id: {
                "anchor": {
                    "exact": exact,
                    "pos": pos,
                    "prefix": prefix,
                    "suffix": suffix,
                },
                "status": "open",
                "thread": [
                    {
                        "author": "Reader",
                        "ts": "2026-06-29T00:00:00.000Z",
                        "text": "这里需要解释。",
                    }
                ],
            }
        }
        page.write_text(text.rstrip() + "\n\n" + readerlab.dump_tandem(data) + "\n", encoding="utf-8")

    def test_markdown_heading_count_ignores_fenced_code_comments(self) -> None:
        text = """# Real Heading

```bash
# Bash comments are not Markdown headings.
echo ok
```

## Another Real Heading
"""
        self.assertEqual(readerlab.count_markdown_headings(text), 2)

    def test_translation_quality_flags_short_english_instruction_residue(self) -> None:
        block = {"id": "demo-0001-paragraph", "kind": "paragraph"}
        issues = readerlab.translation_quality_issues(
            block,
            "If the user asks for a report, generate the final answer in markdown.",
        )
        self.assertIn("short_english_residue:demo-0001-paragraph", issues)

    def test_translation_quality_flags_english_user_prompt_residue(self) -> None:
        block = {"id": "demo-0002-paragraph", "kind": "paragraph"}
        issues = readerlab.translation_quality_issues(
            block,
            "Sure, I can help with that. Ask the user for the target directory.",
        )
        self.assertIn("short_english_residue:demo-0002-paragraph", issues)

    def test_translation_quality_flags_english_code_comments(self) -> None:
        block = {"id": "demo-0003-code", "kind": "code_block"}
        issues = readerlab.translation_quality_issues(
            block,
            "```bash\n# This checks whether the browser session is still valid.\necho ok\n```",
        )
        self.assertIn("code_comment_english_residue:demo-0003-code", issues)

    def test_translation_quality_allows_commands_paths_and_code_spans(self) -> None:
        block = {"id": "demo-0004-paragraph", "kind": "paragraph"}
        issues = readerlab.translation_quality_issues(
            block,
            "运行 `python3 scripts/readerlab.py validate /tmp/book --skill unfreeze`，"
            "再检查 `/Users/tianqiang/LifeAtlas/.../gstack` 的 manifest 状态。",
        )
        self.assertEqual(issues, [])

    def test_translation_quality_allows_chinese_with_technical_terms(self) -> None:
        block = {"id": "demo-0005-paragraph", "kind": "paragraph"}
        issues = readerlab.translation_quality_issues(
            block,
            "这里保留 API、JSON、Git、Codex、status、token 和 model 名称，但说明文字已经中文化。",
        )
        self.assertEqual(issues, [])

    def test_translation_quality_allows_code_commands_variables_and_chinese_comments(self) -> None:
        block = {"id": "demo-0006-code", "kind": "code_block"}
        issues = readerlab.translation_quality_issues(
            block,
            "```bash\n#!/usr/bin/env bash\n# export TOKEN=abc\n# 检查本地会话是否仍然有效\necho \"$TOKEN\"\n```",
        )
        self.assertEqual(issues, [])

    def test_validate_contract_artifacts_and_human_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_dir = self.write_contract_pack(Path(tmp))

            validation = run_readerlab("validate", str(book_dir), "--require-contracts")
            payload = json.loads(validation.stdout)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["require_contracts"])
            self.assertEqual(len(payload["contract_artifacts"]), 2)
            self.assertEqual(payload["contract_artifacts"][0]["schema"], "readerlab.global-map.v1")
            self.assertEqual(payload["contract_artifacts"][0]["source_scope"], "partial")
            self.assertEqual(payload["contract_artifacts"][0]["confidence"], "medium")
            self.assertEqual(
                payload["status_semantics"]["delivery_status"],
                "machine_pack_delivery_status",
            )

            human_gate = run_readerlab_unchecked("validate", str(book_dir), "--require-human-accepted")
            self.assertNotEqual(human_gate.returncode, 0)
            self.assertIn("未人工验收", human_gate.stdout)

            manifest_path = book_dir / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["skills"][0]["human_status"] = "accepted"
            for artifact in manifest["contract_artifacts"]:
                artifact["human_status"] = "accepted"
                artifact_payload = json.loads((book_dir / artifact["path"]).read_text(encoding="utf-8"))
                artifact_payload["human_status"] = "accepted"
                (book_dir / artifact["path"]).write_text(
                    json.dumps(artifact_payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            accepted_validation = run_readerlab(
                "validate",
                str(book_dir),
                "--require-contracts",
                "--require-human-accepted",
            )
            accepted_payload = json.loads(accepted_validation.stdout)
            self.assertTrue(accepted_payload["passed"])
            self.assertEqual(accepted_payload["summary"]["human_cleared_skills"], 1)

            bad_global_map = json.loads((book_dir / "40_全局理解" / "global-map.json").read_text(encoding="utf-8"))
            bad_global_map.pop("review_items")
            (book_dir / "40_全局理解" / "global-map.json").write_text(
                json.dumps(bad_global_map, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            bad_validation = run_readerlab_unchecked("validate", str(book_dir), "--require-contracts")
            self.assertNotEqual(bad_validation.returncode, 0)
            self.assertIn("review_items", bad_validation.stdout)

    def test_validate_contract_cli_accepts_two_minimal_samples(self) -> None:
        samples = [
            ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample",
            ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/skill-engineering-sample",
        ]
        for sample in samples:
            with self.subTest(sample=sample.name):
                validation = run_readerlab("validate-contract", str(sample))
                payload = json.loads(validation.stdout)
                self.assertTrue(payload["passed"])
                self.assertIn("readerlab.source-registry.v1", payload["schemas"])
                self.assertIn("readerlab.location-map.v1", payload["schemas"])
                self.assertIn("readerlab.output-eval.v1", payload["schemas"])

    def test_validate_contract_cli_rejects_core_failures(self) -> None:
        book_sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample"
        skill_sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/skill-engineering-sample"

        with tempfile.TemporaryDirectory() as tmp:
            bad_claim = Path(tmp) / "bad-claim"
            shutil.copytree(book_sample, bad_claim)
            catalog_path = bad_claim / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["claims"][0].pop("source_refs")
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(bad_claim))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("high-level claim 缺少 source refs", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            bad_global = Path(tmp) / "bad-global"
            shutil.copytree(book_sample, bad_global)
            grounded_path = bad_global / "audit/contracts/grounded-global-map.v1.json"
            grounded_path.write_text(
                json.dumps(
                    {
                        "schema": "readerlab.grounded-global-map.v1",
                        "material": {"id": "bad-global", "title": "bad", "type": "book"},
                        "source_scope": {"coverage_status": "partial"},
                        "claims": [
                            {
                                "claim": "This is a full global map despite partial coverage.",
                                "source_refs": ["loc-longform-main-claim"],
                            }
                        ],
                        "machine_status": "ready",
                        "human_status": "pending",
                        "display": {
                            "reader_facing": ["reader/01_局部长文阅读页.md"],
                            "internal_audit": ["audit/contracts/grounded-global-map.v1.json"],
                            "relationship": "separate_reader_and_audit",
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            result = run_readerlab_unchecked("validate-contract", str(bad_global))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("不能生成 grounded global map", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            bad_status = Path(tmp) / "bad-status"
            shutil.copytree(book_sample, bad_status)
            deepread_path = bad_status / "audit/contracts/local-deepread.v1.json"
            deepread = json.loads(deepread_path.read_text(encoding="utf-8"))
            deepread.pop("human_status")
            deepread_path.write_text(json.dumps(deepread, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(bad_status))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("缺少 human_status", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            bad_capability = Path(tmp) / "bad-capability"
            shutil.copytree(skill_sample, bad_capability)
            capability_path = bad_capability / "audit/contracts/capability-map.v1.json"
            capability = json.loads(capability_path.read_text(encoding="utf-8"))
            capability["capability_domains"][0].pop("trigger_signals")
            capability_path.write_text(json.dumps(capability, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(bad_capability))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("trigger_signals", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            missing_capability_module = Path(tmp) / "missing-capability-module"
            shutil.copytree(skill_sample, missing_capability_module)
            capability_path = missing_capability_module / "audit/contracts/capability-map.v1.json"
            capability = json.loads(capability_path.read_text(encoding="utf-8"))
            capability["capability_domains"] = [
                domain
                for domain in capability["capability_domains"]
                if domain["domain_id"] != "output-eval-gate"
            ]
            capability_path.write_text(json.dumps(capability, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(missing_capability_module))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("capability-map 未覆盖 primary_module location refs", result.stdout)
            self.assertIn("loc-output-eval-status", result.stdout)

    def test_validate_contract_cli_rejects_hardened_false_passes(self) -> None:
        book_sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample"

        with tempfile.TemporaryDirectory() as tmp:
            bad_eval = Path(tmp) / "bad-eval"
            shutil.copytree(book_sample, bad_eval)
            eval_path = bad_eval / "audit/contracts/output-eval.v1.json"
            output_eval = json.loads(eval_path.read_text(encoding="utf-8"))
            output_eval["output_eval"]["checks"] = [
                check
                for check in output_eval["output_eval"]["checks"]
                if check["id"] != "machine_not_human"
            ]
            eval_path.write_text(json.dumps(output_eval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(bad_eval))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("machine_not_human", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            bad_refs = Path(tmp) / "bad-refs"
            shutil.copytree(book_sample, bad_refs)
            catalog_path = bad_refs / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["claims"][0]["source_refs"] = ["loc-does-not-exist"]
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(bad_refs))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("未知 source/location ref", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            empty_source = Path(tmp) / "empty-source"
            shutil.copytree(book_sample, empty_source)
            source_path = empty_source / "audit/source-registry.v1.json"
            source_registry = json.loads(source_path.read_text(encoding="utf-8"))
            source_registry["sources"] = []
            source_path.write_text(json.dumps(source_registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(empty_source))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source-registry.sources 必须是非空列表", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            hollow_source = Path(tmp) / "hollow-source"
            shutil.copytree(book_sample, hollow_source)
            source_path = hollow_source / "audit/source-registry.v1.json"
            source_registry = json.loads(source_path.read_text(encoding="utf-8"))
            source_registry["sources"][0].pop("source_path")
            source_path.write_text(json.dumps(source_registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(hollow_source))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("不能作为空壳来源", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            empty_location = Path(tmp) / "empty-location"
            shutil.copytree(book_sample, empty_location)
            location_path = empty_location / "audit/location-map.v1.json"
            location_map = json.loads(location_path.read_text(encoding="utf-8"))
            location_map["locations"] = []
            location_path.write_text(json.dumps(location_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(empty_location))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("location-map.locations 必须是非空列表", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            hollow_location = Path(tmp) / "hollow-location"
            shutil.copytree(book_sample, hollow_location)
            location_path = hollow_location / "audit/location-map.v1.json"
            location_map = json.loads(location_path.read_text(encoding="utf-8"))
            location_map["locations"][0].pop("source_id")
            location_map["locations"][0].pop("path")
            location_map["locations"][0].pop("range")
            location_path.write_text(json.dumps(location_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(hollow_location))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("位置必须挂回来源", result.stdout)
            self.assertIn("不能作为空壳位置", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            mixed_display = Path(tmp) / "mixed-display"
            shutil.copytree(book_sample, mixed_display)
            catalog_path = mixed_display / "audit/contracts/catalog-map.v1.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["display"]["relationship"] = "mixed"
            catalog["display"]["internal_audit"] = list(catalog["display"]["reader_facing"])
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("validate-contract", str(mixed_display))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reader-facing 和 internal audit 混在一起", result.stdout)
            self.assertIn("路径重叠", result.stdout)

    def test_reader_facing_first_hand_body_is_not_only_summary(self) -> None:
        pages = [
            ROOT
            / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample/reader/01_局部长文阅读页.md",
            ROOT
            / "tests/fixtures/readerlab/contract-validator-proof-v0/skill-engineering-sample/reader/01_工程材料阅读页.md",
        ]
        for page in pages:
            with self.subTest(page=page.name):
                text = page.read_text(encoding="utf-8")
                body_match = re.search(r"^## 处理过的一手正文\s*(.*?)(?=^## |\Z)", text, re.M | re.S)
                self.assertIsNotNone(body_match)
                body = body_match.group(1) if body_match else ""
                self.assertNotIn("核心意思是", body)
                self.assertGreaterEqual(len(body), 220)
                self.assertTrue("###" in body or ">" in body)

    def test_render_contract_package_generates_two_samples_and_validates(self) -> None:
        samples = [
            (
                ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample",
                "reader/01_局部长文阅读页.md",
            ),
            (
                ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/skill-engineering-sample",
                "reader/01_工程材料阅读页.md",
            ),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for sample, primary_page in samples:
                with self.subTest(sample=sample.name):
                    out = Path(tmp) / sample.name
                    render = run_readerlab("render-contract-package", str(sample), str(out))
                    render_payload = json.loads(render.stdout)
                    self.assertIn(primary_page, render_payload["rendered_pages"])
                    self.assertTrue((out / primary_page).is_file())
                    self.assertTrue((out / "audit/contracts/output-eval.v1.json").is_file())
                    self.assertNotEqual(
                        (sample / primary_page).read_text(encoding="utf-8"),
                        (out / primary_page).read_text(encoding="utf-8"),
                    )

                    validation = run_readerlab("validate-contract", str(out))
                    validation_payload = json.loads(validation.stdout)
                    self.assertTrue(validation_payload["passed"])

    def test_eval_rendered_package_accepts_two_rendered_outputs(self) -> None:
        samples = [
            ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample",
            ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/skill-engineering-sample",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for sample in samples:
                with self.subTest(sample=sample.name):
                    out = Path(tmp) / sample.name
                    run_readerlab("render-contract-package", str(sample), str(out))
                    evaluation = run_readerlab("eval-rendered-package", str(out))
                    payload = json.loads(evaluation.stdout)
                    self.assertTrue(payload["passed"])
                    self.assertTrue(payload["validate_contract_passed"])
                    self.assertEqual(
                        {gate["id"] for gate in payload["gates"]},
                        {
                            "reader_markdown_exists",
                            "reader_audit_path_separation",
                            "first_hand_body_source_present",
                            "output_eval_9_gates_present",
                            "human_status_not_machine_accepted",
                        },
                    )

    def test_eval_rendered_package_writes_success_report_md(self) -> None:
        sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample"

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rendered"
            report = Path(tmp) / "eval-report.md"
            run_readerlab("render-contract-package", str(sample), str(out))
            evaluation = run_readerlab("eval-rendered-package", str(out), "--report-md", str(report))
            payload = json.loads(evaluation.stdout)
            self.assertTrue(payload["passed"])
            text = report.read_text(encoding="utf-8")
            self.assertIn(f"- target: `{out}`", text)
            self.assertIn("- validate_contract_passed: true", text)
            for gate_id in {
                "reader_markdown_exists",
                "reader_audit_path_separation",
                "first_hand_body_source_present",
                "output_eval_9_gates_present",
                "human_status_not_machine_accepted",
            }:
                self.assertIn(f"- {gate_id}: pass", text)
            self.assertIn("human_status pending", text)
            self.assertIn("not human acceptance", text)

    def test_eval_rendered_package_writes_failure_report_md(self) -> None:
        sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample"

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rendered"
            report = Path(tmp) / "eval-report.md"
            run_readerlab("render-contract-package", str(sample), str(out))
            (out / "reader/01_局部长文阅读页.md").unlink()
            result = run_readerlab_unchecked("eval-rendered-package", str(out), "--report-md", str(report))
            self.assertNotEqual(result.returncode, 0)
            text = report.read_text(encoding="utf-8")
            self.assertIn("- validate_contract_passed: false", text)
            self.assertIn("- reader_markdown_exists: fail", text)
            self.assertIn("reader markdown missing", text)
            self.assertIn("## Failures", text)

    def test_eval_rendered_package_report_path_requires_explicit_overwrite(self) -> None:
        sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample"

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rendered"
            report = Path(tmp) / "eval-report.md"
            report.write_text("SENTINEL DO NOT KEEP\n", encoding="utf-8")
            run_readerlab("render-contract-package", str(sample), str(out))
            result = run_readerlab_unchecked("eval-rendered-package", str(out), "--report-md", str(report))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("report path already exists", result.stderr + result.stdout)
            self.assertEqual(report.read_text(encoding="utf-8"), "SENTINEL DO NOT KEEP\n")

            overwrite = run_readerlab(
                "eval-rendered-package",
                str(out),
                "--report-md",
                str(report),
                "--overwrite-report",
            )
            self.assertTrue(json.loads(overwrite.stdout)["passed"])
            self.assertIn("# ReaderLab Rendered Package Eval Report", report.read_text(encoding="utf-8"))

    def test_eval_rendered_package_report_path_rejects_lifeatlas(self) -> None:
        sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample"

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rendered"
            run_readerlab("render-contract-package", str(sample), str(out))
            result = run_readerlab_unchecked(
                "eval-rendered-package",
                str(out),
                "--report-md",
                "/Users/tianqiang/LifeAtlas/readerlab-report-should-not-write.md",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing to write eval report under LifeAtlas", result.stderr + result.stdout)

    def test_render_contract_package_rejects_missing_source_excerpts(self) -> None:
        sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample"

        with tempfile.TemporaryDirectory() as tmp:
            bad_sample = Path(tmp) / "missing-source-excerpt"
            shutil.copytree(sample, bad_sample)
            (bad_sample / "audit/source-excerpts/longform-fragment.md").unlink()
            result = run_readerlab_unchecked("render-contract-package", str(bad_sample), str(Path(tmp) / "out"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source excerpt not found", result.stderr + result.stdout)

    def test_eval_rendered_package_rejects_missing_reader_gate_and_human_acceptance(self) -> None:
        sample = ROOT / "tests/fixtures/readerlab/contract-validator-proof-v0/book-longform-sample"

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "missing-reader"
            run_readerlab("render-contract-package", str(sample), str(out))
            (out / "reader/01_局部长文阅读页.md").unlink()
            result = run_readerlab_unchecked("eval-rendered-package", str(out))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reader markdown missing", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "missing-first-hand-body"
            run_readerlab("render-contract-package", str(sample), str(out))
            reader_path = out / "reader/01_局部长文阅读页.md"
            reader_path.write_text(
                "# 空壳阅读页\n\n## AI 旁批\n\n这里只有机器旁批，没有处理过的一手正文。\n",
                encoding="utf-8",
            )
            result = run_readerlab_unchecked("eval-rendered-package", str(out))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing actual first-hand body", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "source-path-only"
            run_readerlab("render-contract-package", str(sample), str(out))
            reader_path = out / "reader/01_局部长文阅读页.md"
            reader_path.write_text(
                "# 空壳阅读页\n\n"
                "## 处理过的一手正文\n\n"
                "### 来源：`audit/source-excerpts/longform-fragment.md`\n\n"
                "## AI 旁批\n\n这里只有来源路径，没有实际一手正文。\n",
                encoding="utf-8",
            )
            result = run_readerlab_unchecked("eval-rendered-package", str(out))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing actual first-hand body", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "missing-gate"
            run_readerlab("render-contract-package", str(sample), str(out))
            eval_path = out / "audit/contracts/output-eval.v1.json"
            output_eval = json.loads(eval_path.read_text(encoding="utf-8"))
            output_eval["output_eval"]["checks"] = [
                check
                for check in output_eval["output_eval"]["checks"]
                if check["id"] != "machine_not_human"
            ]
            eval_path.write_text(json.dumps(output_eval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("eval-rendered-package", str(out))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("machine_not_human", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "human-accepted"
            run_readerlab("render-contract-package", str(sample), str(out))
            eval_path = out / "audit/contracts/output-eval.v1.json"
            output_eval = json.loads(eval_path.read_text(encoding="utf-8"))
            output_eval["human_status"] = "accepted"
            eval_path.write_text(json.dumps(output_eval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = run_readerlab_unchecked("eval-rendered-package", str(out))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("human_status must remain pending", result.stdout)

    def test_import_skills_generates_v01_reading_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "skills"
            (source / "spec").mkdir(parents=True)
            (source / "review" / "scripts").mkdir(parents=True)
            (source / "benchmark-models").mkdir(parents=True)
            (source / "unfreeze").mkdir(parents=True)
            (source / "freeze" / "bin").mkdir(parents=True)
            (source / "careful" / "bin").mkdir(parents=True)
            (source / "guard").mkdir(parents=True)
            (source / "gstack-upgrade" / "migrations").mkdir(parents=True)
            (source / "spec" / "SKILL.md").write_text(
                """---
name: spec
description: Turn vague intent into a precise executable spec.
allowed-tools: Read, Write
---

# Spec

Use this when the user wants a vague idea turned into a concrete implementation plan.
""",
                encoding="utf-8",
            )
            (source / "review" / "SKILL.md").write_text(
                """---
name: review
description: Review a plan before implementation.
---

# Review

Check the plan for risks, missing tests, and unclear boundaries.
""",
                encoding="utf-8",
            )
            (source / "review" / "scripts" / "collect-evidence.py").write_text(
                "print('collect evidence')\n",
                encoding="utf-8",
            )
            (source / "benchmark-models" / "SKILL.md").write_text(
                """---
name: benchmark-models
description: Compare model outputs against benchmark cases.
---

# Benchmark Models

Run a suite of prompts against candidate models.

## Prepare Cases

Collect benchmark cases and expected observations.

## Compare Outputs

Record model output quality, cost, latency, and failure patterns.
""",
                encoding="utf-8",
            )
            (source / "unfreeze" / "SKILL.md").write_text(
                """---
name: unfreeze
description: Clear the freeze boundary set by /freeze.
allowed-tools:
  - Bash
  - Read
---

## When to invoke this skill

Use when you want to widen edit scope without ending the session.

# /unfreeze — Clear Freeze Boundary

Remove the edit restriction set by `/freeze`, allowing edits to all directories.

```bash
rm -f "$STATE_DIR/freeze-dir.txt"
```

## Clear the boundary

Tell the user the result and explain that freeze hooks are still registered.
""",
                encoding="utf-8",
            )
            (source / "freeze" / "SKILL.md").write_text(
                """---
name: freeze
description: Restrict file edits to a specific directory for the session.
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"
---

## When to invoke this skill

Blocks Edit and Write outside the allowed path.

# /freeze — Restrict Edits to a Directory

Lock file edits to a specific directory.

```bash
echo "$FREEZE_DIR" > "$STATE_DIR/freeze-dir.txt"
```

## Setup

Ask the user which directory to restrict edits to.

## How it works

The hook reads file_path and denies edits outside the boundary.

## Notes

This prevents accidental edits, not a security boundary.
""",
                encoding="utf-8",
            )
            (source / "freeze" / "bin" / "check-freeze.sh").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )
            (source / "freeze" / "SKILL.md.tmpl").write_text(
                "# Freeze template\n",
                encoding="utf-8",
            )
            (source / "careful" / "SKILL.md").write_text(
                """---
name: careful
description: Safety guardrails for destructive commands.
allowed-tools:
  - Bash
  - Read
---

## When to invoke this skill

Warns before destructive operations.

# /careful — Destructive Command Guardrails

Safety mode checks bash commands before running.

```bash
echo careful
```

## What's protected

| Pattern | Example | Risk |
|---|---|---|
| rm -rf | rm -rf /var/data | Recursive delete |

## Safe exceptions

Build caches can be removed without warning.

## How it works

The hook returns ask when a destructive pattern is found.
""",
                encoding="utf-8",
            )
            (source / "careful" / "bin" / "check-careful.sh").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )
            (source / "guard" / "SKILL.md").write_text(
                """---
name: guard
description: Full safety mode.
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

## When to invoke this skill

Combines careful and freeze.

# /guard — Full Safety Mode

Activates both destructive command warnings and directory-scoped edit restrictions.

```bash
echo guard
```

## Setup

Ask which directory should be restricted.

```bash
echo "$FREEZE_DIR"
```

## What's protected

See careful and freeze.
""",
                encoding="utf-8",
            )
            (source / "gstack-upgrade" / "SKILL.md").write_text(
                """---
name: gstack-upgrade
description: Upgrade gstack to the latest version.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

## When to invoke this skill

Detects install type and runs the upgrade.

# /gstack-upgrade

Upgrade gstack to the latest version and show what's new.

## Inline upgrade flow

### Step 1: Ask the user

```bash
echo AUTO_UPGRADE
```

### Step 2: Detect install type

```bash
echo INSTALL_TYPE
```

### Step 3: Save old version

```bash
echo OLD_VERSION
```

### Step 4: Upgrade

```bash
echo upgrade
```

### Step 5: Write marker

```bash
echo marker
```

### Step 6: Show What's New

Summarize changes.

### Step 7: Continue

Continue the originally invoked skill.

## Standalone usage

Run a forced update check.
""",
                encoding="utf-8",
            )
            (source / "gstack-upgrade" / "migrations" / "v0.15.2.0.sh").write_text(
                "#!/usr/bin/env bash\necho migrate\n",
                encoding="utf-8",
            )
            dest = root / "out"
            readings_dir = root / "readings"
            (readings_dir / "demo").mkdir(parents=True)
            (readings_dir / "demo" / "review.json").write_text(
                json.dumps(
                    {
                        "schema": "readerlab.skill-reading.v1",
                        "package": "demo",
                        "skill": "review",
                        "guide": "这个 Skill 用来在实现前检查计划风险、测试缺口和边界不清的问题。阅读主线是先明确它审什么，再看它如何把计划质量转成可执行的检查项。",
                        "skill_body_translation": """---
name: review
description: 实现前审查计划。
---

# Review

检查计划中的风险、缺失测试和不清楚的边界。""",
                        "related_materials_explanation": "### 人工解释\n\n- 来源：`review/scripts/collect-evidence.py`\n  - 职责：收集审查前的证据入口。机制解释留在关联材料区，不进入 Skill 正文译文。",
                        "highlights": [
                            {
                                "quote": "先检查风险、测试和边界。",
                                "source": "Skill 正文",
                                "comment": "这是审查类 Skill 的最小判断面，适合作为后续深度审查的入口。",
                            }
                        ],
                        "evidence": {
                            "skill_md": "review/SKILL.md",
                            "coverage": "正文译文只覆盖 review/SKILL.md；关联脚本单独说明。",
                            "related_sources": [
                                {
                                    "path": "review/scripts/collect-evidence.py",
                                    "note": "用于验证关联材料不会混入正文。",
                                }
                            ],
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (readings_dir / "demo" / "benchmark-models.json").write_text(
                json.dumps(
                    {
                        "schema": "readerlab.skill-reading.v1",
                        "package": "demo",
                        "skill": "benchmark-models",
                        "guide": "这个 Skill 用来比较模型输出，但当前 Agent 产物只完成了初稿，需要复核覆盖率。",
                        "skill_body_translation": "模型基准测试初稿：运行提示集并比较输出质量。",
                        "related_materials_explanation": "### 人工解释\n\n- 来源：`benchmark-models/SKILL.md`\n  - 职责：说明基准测试流程，当前解释仍需复核。",
                        "highlights": "无特别高亮。",
                        "evidence": {
                            "skill_md": "benchmark-models/SKILL.md",
                            "coverage": "当前只提供短译文，故应生成需复核页面，但不能计入完成。",
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            run_readerlab(
                "import-skills",
                str(source),
                "--dest",
                str(dest),
                "--book-id",
                "demo",
                "--title",
                "demo",
                "--readings-dir",
                str(readings_dir),
            )

            book_dir = dest / "demo"
            self.assertTrue((book_dir / "00_从这里开始.md").exists())
            self.assertTrue((book_dir / "01_轻量拆解手册.md").exists())
            terms_page = book_dir / "02_Skill阅读术语表.md"
            self.assertTrue(terms_page.exists())
            terms_text = terms_page.read_text(encoding="utf-8")
            self.assertIn("## 基础结构", terms_text)
            self.assertIn("## 工具调用", terms_text)
            self.assertIn("## 文件机制", terms_text)
            for term in [
                "frontmatter",
                "hooks",
                "PreToolUse",
                "matcher",
                "command",
                "Bash",
                "Edit",
                "Write",
                "bin/scripts",
                "migrations",
                "template/.tmpl",
                "sections",
                "src/lib",
            ]:
                self.assertIn(term, terms_text)
            self.assertTrue((book_dir / "03_验收标准.md").exists())
            self.assertTrue((book_dir / "04_主控清单.md").exists())
            self.assertTrue((book_dir / "10_中文精读" / "01_核心入口与总览" / "00_本组导读.md").exists())
            self.assertFalse((book_dir / "10_中文精读" / "01_核心入口与总览" / "01_spec.md").exists())
            unfreeze_page = book_dir / "10_中文精读" / "07_流程执行与交付运维" / "unfreeze.md"
            self.assertTrue(unfreeze_page.exists())
            unfreeze_text = unfreeze_page.read_text(encoding="utf-8")
            self.assertIn("## 短导读", unfreeze_text)
            self.assertIn("## 阅读地图", unfreeze_text)
            self.assertIn("## Skill 正文", unfreeze_text)
            self.assertIn("## 关联说明", unfreeze_text)
            self.assertNotIn("## Codex 吸收后的设计提炼", unfreeze_text)
            self.assertNotIn("## 重点与亮点", unfreeze_text)
            self.assertIn("[[02_Skill阅读术语表]]", unfreeze_text)
            self.assertNotIn("## 页面分层", unfreeze_text)
            self.assertNotIn("ReaderLab 后台验收信息", unfreeze_text)
            self.assertNotIn("unfreeze-机制说明.md", unfreeze_text)
            self.assertNotIn("unfreeze-证据附录.md", unfreeze_text)
            skill_body = unfreeze_text.split("## Skill 正文", 1)[1].split("## 关联说明", 1)[0]
            self.assertNotIn("读这个 Skill 时真正该学什么", skill_body)
            self.assertNotIn("这里的机制是什么", skill_body)
            self.assertIn("状态文件", unfreeze_text)
            self.assertIn("unfreeze/SKILL.md.tmpl", unfreeze_text)
            self.assertNotIn("> [!important] 高亮", unfreeze_text)
            self.assertNotIn("> [!important] 重点", unfreeze_text)
            self.assertFalse((book_dir / "11_机制说明").exists())
            self.assertFalse((book_dir / "12_证据附录").exists())
            freeze_page = book_dir / "10_中文精读" / "07_流程执行与交付运维" / "freeze.md"
            freeze_text = freeze_page.read_text(encoding="utf-8")
            self.assertIn("[[02_Skill阅读术语表]]", freeze_text)
            self.assertIn("本页重点术语：`frontmatter`、`bin/scripts`、`template/.tmpl`、`hooks`、`PreToolUse`、`matcher`、`command`、`Edit`、`Write`", freeze_text)
            self.assertIn("### 机制盘点", freeze_text)
            self.assertIn("### 执行机制", freeze_text)
            self.assertIn("freeze/bin/check-freeze.sh", freeze_text)
            self.assertIn("`Edit`", freeze_text)
            self.assertIn("`Write`", freeze_text)
            freeze_body = freeze_text.split("## Skill 正文", 1)[1].split("## 关联说明", 1)[0]
            self.assertNotIn("### 术语速读", freeze_body)
            self.assertNotIn("`PreToolUse`：工具真正执行前的检查点", freeze_body)
            self.assertNotIn("`frontmatter`：`SKILL.md` 顶部", freeze_body)
            upgrade_page = book_dir / "10_中文精读" / "06_Agent工具与迁移工作台" / "gstack-upgrade.md"
            upgrade_text = upgrade_page.read_text(encoding="utf-8")
            self.assertIn("gstack-upgrade/migrations/v0.15.2.0.sh", upgrade_text)
            self.assertIn("迁移脚本", upgrade_text)
            self.assertNotIn("没有声明 hooks", upgrade_text)
            self.assertIn("机制材料", upgrade_text)
            self.assertNotIn("没有发现脚本入口", upgrade_text)
            review_page = book_dir / "10_中文精读" / "02_诊断审查与质量判断" / "review.md"
            self.assertTrue(review_page.exists())
            review_text = review_page.read_text(encoding="utf-8")
            self.assertIn("## Skill 正文", review_text)
            self.assertIn("### 机制盘点", review_text)
            self.assertIn("### 执行机制", review_text)
            self.assertIn("review/scripts/collect-evidence.py", review_text)
            review_body = review_text.split("## Skill 正文", 1)[1].split("## 关联说明", 1)[0]
            self.assertIn("检查计划中的风险、缺失测试和不清楚的边界。", review_body)
            self.assertNotIn("机制解释留在关联材料区", review_body)
            self.assertNotIn("collect-evidence.py", review_body)
            benchmark_page = book_dir / "10_中文精读" / "02_诊断审查与质量判断" / "benchmark-models.md"
            self.assertTrue(benchmark_page.exists())
            benchmark_text = benchmark_page.read_text(encoding="utf-8")
            self.assertIn("# benchmark-models：需复核中文阅读页", benchmark_text)
            self.assertNotIn("# benchmark-models：完整中文阅读页", benchmark_text)
            manifest = json.loads((book_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], "readerlab.v0.1")
            self.assertEqual(manifest["delivery_status"], "in_progress")
            self.assertEqual(manifest["coverage_policy"]["reading_page_structure"], "main_reading_page_centered")
            self.assertEqual(manifest["coverage_policy"]["non_body_handling"], "codex_absorption_with_trace")
            self.assertEqual(manifest["coverage_policy"]["reader_visible_evidence_pages"], False)
            self.assertEqual(len(manifest["skills"]), 8)
            self.assertEqual(len({s["source_file"] for s in manifest["skills"]}), 8)
            self.assertEqual(len({s["reading_page"] for s in manifest["skills"]}), 8)
            self.assertEqual(manifest["skills"][0]["status"], "not_started")
            self.assertEqual(manifest["skills"][0]["machine_status"], "not_started")
            self.assertEqual(manifest["skills"][0]["human_status"], "pending")
            unfreeze = next(s for s in manifest["skills"] if s["name"] == "unfreeze")
            self.assertEqual(unfreeze["status"], "completed")
            self.assertEqual(unfreeze["machine_status"], "completed")
            self.assertEqual(unfreeze["human_status"], "pending")
            self.assertEqual(unfreeze["mechanism_page"], "")
            self.assertEqual(unfreeze["evidence_page"], "")
            self.assertEqual(unfreeze["codex_absorption"]["status"], "absorbed")
            self.assertTrue(unfreeze["codex_absorption"]["source_refs"])
            review = next(s for s in manifest["skills"] if s["name"] == "review")
            self.assertEqual(review["status"], "completed")
            self.assertEqual(review["machine_status"], "completed")
            self.assertEqual(review["human_status"], "pending")
            self.assertEqual(review["reading_source"], "agent_reading")
            self.assertTrue(review["reading_artifact"].endswith("readings/demo/review.json"))
            self.assertEqual(review["coverage"]["reading_source"], "agent_reading")
            self.assertTrue(any(a["path"] == "review/scripts/collect-evidence.py" for a in review["related_artifacts"]))
            benchmark = next(s for s in manifest["skills"] if s["name"] == "benchmark-models")
            self.assertEqual(benchmark["status"], "needs_review")
            self.assertEqual(benchmark["machine_status"], "needs_review")
            self.assertEqual(benchmark["human_status"], "pending")
            self.assertTrue(benchmark["reading_artifact"].endswith("readings/demo/benchmark-models.json"))
            freeze = next(s for s in manifest["skills"] if s["name"] == "freeze")
            self.assertTrue(any(a["path"] == "freeze/bin/check-freeze.sh" for a in freeze["related_artifacts"]))
            self.assertGreaterEqual(freeze["coverage"]["related_artifacts_count"], 2)
            self.assertEqual(freeze["coverage"]["hook_references_resolved"], True)
            upgrade = next(s for s in manifest["skills"] if s["name"] == "gstack-upgrade")
            self.assertTrue(
                any(
                    a["path"] == "gstack-upgrade/migrations/v0.15.2.0.sh" and a["kind"] == "迁移脚本"
                    for a in upgrade["related_artifacts"]
                )
            )
            self.assertIn("source_chars", unfreeze["coverage"])
            self.assertIn("translated_body_chars", unfreeze["coverage"])
            self.assertIn("guide_chars", unfreeze["coverage"])
            self.assertIn("related_chars", unfreeze["coverage"])
            self.assertNotIn("highlights_chars", unfreeze["coverage"])
            self.assertIn("heading_coverage", unfreeze["coverage"])
            self.assertIn("paragraph_coverage", unfreeze["coverage"])
            self.assertIn("code_blocks_handled", unfreeze["coverage"])
            release_group = next(u for u in manifest["reading_units"] if u["id"] == "07_流程执行与交付运维")
            self.assertEqual(release_group["completed_skills"], 2)
            self.assertEqual(release_group["status"], "completed")
            self.assertIn("purpose", release_group)
            self.assertIn("reason", release_group)
            self.assertIn("basis", release_group)
            self.assertIn(release_group["confidence"], {"high", "medium", "low"})
            agent_group = next(u for u in manifest["reading_units"] if u["id"] == "06_Agent工具与迁移工作台")
            self.assertEqual(agent_group["completed_skills"], 1)
            self.assertEqual(agent_group["status"], "completed")
            quality_group = next(u for u in manifest["reading_units"] if u["id"] == "02_诊断审查与质量判断")
            self.assertEqual(quality_group["completed_skills"], 3)
            self.assertEqual(quality_group["needs_review_skills"], 1)
            self.assertEqual(quality_group["status"], "in_progress")
            spec_group = next(u for u in manifest["reading_units"] if u["id"] == "01_核心入口与总览")
            self.assertEqual(spec_group["status"], "not_started")
            self.assertGreater(len(manifest["source_blocks"]), 0)
            self.assertEqual(manifest["source_blocks"][0]["status"], "background_pending")
            for field in ("content_layer", "reader_visibility", "absorption_status"):
                self.assertIn(field, manifest["source_blocks"][0])
            quality_intro = (
                book_dir / "10_中文精读" / "02_诊断审查与质量判断" / "00_本组导读.md"
            ).read_text(encoding="utf-8")
            self.assertIn("当前机器完成 3/4，人工已验收 0/4", quality_intro)
            self.assertIn("validate 只代表机器验收", quality_intro)
            self.assertIn("## 阅读路线判断", quality_intro)
            self.assertIn("判断依据", quality_intro)
            self.assertIn("把握程度", quality_intro)
            self.assertIn("[[benchmark-models]] | `benchmark-models` |", quality_intro)
            self.assertIn("机器需复核 | 人工待验收", quality_intro)
            master_checklist = (book_dir / "04_主控清单.md").read_text(encoding="utf-8")
            self.assertIn("需复核：`10_中文精读/02_诊断审查与质量判断/benchmark-models.md`", master_checklist)
            self.assertNotIn("待生成：`10_中文精读/02_诊断审查与质量判断/benchmark-models.md`", master_checklist)
            self.assertIn("机器完成 3/4", master_checklist)
            self.assertIn("人工已验收 0/4", master_checklist)
            self.assertIn("人工待验收", master_checklist)
            self.assertIn("| 阅读单元 | Skill | 机器状态 | 人工状态 | 入口链接 |", master_checklist)
            self.assertNotIn("| 技能组 | Skill | 源文件 | 目标阅读页 | 机器状态 | 人工验收 |", master_checklist)
            self.assertNotIn("review/SKILL.md", master_checklist)

            validation = run_readerlab("validate", str(book_dir))
            payload = json.loads(validation.stdout)
            self.assertTrue(payload["passed"])
            self.assertEqual(payload["summary"]["completed_skills"], 6)
            self.assertEqual(payload["summary"]["needs_review_skills"], 1)
            self.assertEqual(payload["summary"]["human_accepted_skills"], 0)
            self.assertEqual(payload["summary"]["human_pending_skills"], 8)
            self.assertGreater(payload["summary"]["not_started_skills"], 0)

            skill_validation = run_readerlab("validate", str(book_dir), "--skill", "unfreeze")
            skill_payload = json.loads(skill_validation.stdout)
            self.assertTrue(skill_payload["passed"])
            self.assertEqual(skill_payload["skills"][0]["machine_status"], "completed")
            self.assertEqual(skill_payload["skills"][0]["human_status"], "pending")
            self.assertEqual(skill_payload["skills"][0]["coverage"]["code_blocks_handled"], True)
            upgrade_validation = run_readerlab("validate", str(book_dir), "--skill", "gstack-upgrade")
            upgrade_payload = json.loads(upgrade_validation.stdout)
            self.assertTrue(upgrade_payload["passed"])

            strict_validation = run_readerlab_unchecked("validate", str(book_dir), "--require-complete")
            self.assertNotEqual(strict_validation.returncode, 0)
            self.assertIn("未完成 Skill", strict_validation.stdout)

    def test_ambiguous_pack_outputs_structure_diagnosis_instead_of_manual_grouping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "skills"
            (source / "helper").mkdir(parents=True)
            (source / "helper" / "SKILL.md").write_text(
                """---
name: helper
description: Mixed support notes.
---

# Helper

This file mixes unrelated notes, partial reminders, and vague support text without a stable entry, routing role, reading purpose, or clear workflow.
""",
                encoding="utf-8",
            )
            dest = root / "out"
            run_readerlab(
                "import-skills",
                str(source),
                "--dest",
                str(dest),
                "--book-id",
                "mixed",
                "--title",
                "mixed",
            )
            book_dir = dest / "mixed"
            manifest = json.loads((book_dir / "manifest.json").read_text(encoding="utf-8"))
            record = manifest["skills"][0]
            self.assertEqual(record["group"], "90_材料结构诊断")
            self.assertEqual(record["route_confidence"], "low")
            self.assertEqual(record["structure_status"], "diagnostic")
            self.assertEqual(manifest["material_structure"]["status"], "diagnostic")
            self.assertEqual(manifest["material_structure"]["diagnostic_skills"], ["helper"])
            unit = next(u for u in manifest["reading_units"] if u["id"] == "90_材料结构诊断")
            self.assertEqual(unit["structure_status"], "diagnostic")
            self.assertEqual(unit["confidence"], "low")
            guide = book_dir / "10_中文精读" / "90_材料结构诊断" / "00_本组导读.md"
            self.assertTrue(guide.exists())
            guide_text = guide.read_text(encoding="utf-8")
            self.assertIn("结构诊断", guide_text)
            self.assertNotIn("待人工分组", guide_text)

    def test_human_review_registry_resets_known_accepted_pages_after_structure_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, readings_dir, dest = self.write_comment_fixture(
                root,
                skill="dbs-diagnosis",
                description="商业诊断核心框架",
                body="Alpha beta gamma.",
            )
            package_dir = readings_dir / "dbs-suite"
            package_dir.mkdir(parents=True, exist_ok=True)
            source_text = (source / "dbs-diagnosis" / "SKILL.md").read_text(encoding="utf-8")
            (package_dir / "dbs-diagnosis.json").write_text(
                json.dumps(
                    {
                        "schema": "readerlab.skill-reading.v1",
                        "package": "dbs-suite",
                        "skill": "dbs-diagnosis",
                        "guide": "这个样本用于测试人工验收状态拆分。",
                        "skill_body_translation": source_text,
                        "related_materials_explanation": "没有额外关联材料。",
                        "highlights": "无特别高亮。",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            run_readerlab(
                "import-skills",
                str(source),
                "--dest",
                str(dest),
                "--book-id",
                "dbs-suite",
                "--title",
                "dbs-suite",
                "--readings-dir",
                str(readings_dir),
            )
            book_dir = dest / "dbs-suite"
            manifest = json.loads((book_dir / "manifest.json").read_text(encoding="utf-8"))
            record = manifest["skills"][0]
            self.assertEqual(record["status"], "completed")
            self.assertEqual(record["machine_status"], "completed")
            self.assertEqual(record["human_status"], "pending")
            self.assertEqual(record["human_review"]["reviewer"], "user")
            self.assertEqual(record["human_review"]["source"], "current_goal_manual_review")
            self.assertEqual(record["human_review"]["previous_human_status"], "accepted")
            self.assertIn("旧版人工验收不能自动继承", record["human_review"]["reset_reason"])

            master_checklist = (book_dir / "04_主控清单.md").read_text(encoding="utf-8")
            self.assertIn("机器完成 1/1", master_checklist)
            self.assertIn("人工已验收 0/1", master_checklist)
            self.assertIn("人工待验收", master_checklist)
            group_intro = (
                book_dir / "10_中文精读" / "02_诊断审查与质量判断" / "00_本组导读.md"
            ).read_text(encoding="utf-8")
            self.assertIn("当前机器完成 1/1，人工已验收 0/1", group_intro)

            validation = run_readerlab("validate", str(book_dir), "--skill", "dbs-diagnosis")
            payload = json.loads(validation.stdout)
            self.assertTrue(payload["passed"])
            self.assertEqual(payload["summary"]["completed_skills"], 1)
            self.assertEqual(payload["summary"]["human_accepted_skills"], 0)
            self.assertEqual(payload["skills"][0]["machine_status"], "completed")
            self.assertEqual(payload["skills"][0]["human_status"], "pending")

    def test_block_reading_manifest_merge_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "skills"
            (source / "chunky").mkdir(parents=True)
            (source / "chunky" / "SKILL.md").write_text(
                """---
name: chunky
description: Exercise block translation coverage.
---

# Chunky Skill

Use this skill when a long skill must be translated block by block.

```bash
echo run
```

## Finish

Tell the user what happened and list validation evidence.
""",
                encoding="utf-8",
            )
            manifest_result = run_readerlab(
                "block-manifest",
                str(source / "chunky" / "SKILL.md"),
                "--skill",
                "chunky",
                "--source-file",
                "chunky/SKILL.md",
            )
            block_manifest = json.loads(manifest_result.stdout)
            self.assertEqual(block_manifest["schema"], "readerlab.skill-block-manifest.v1")
            kinds = {block["kind"] for block in block_manifest["blocks"]}
            self.assertIn("frontmatter", kinds)
            self.assertIn("heading", kinds)
            self.assertIn("paragraph", kinds)
            self.assertIn("code_block", kinds)
            self.assertTrue(all(block["source_hash"] for block in block_manifest["blocks"]))
            self.assertTrue(all(block["start_line"] <= block["end_line"] for block in block_manifest["blocks"]))

            def translation_for(block: dict, *, bad_quality: bool = False) -> str:
                if block["kind"] == "frontmatter":
                    return "---\nname: chunky\ndescription: 分块翻译覆盖样例。\n---"
                if block["kind"] == "heading" and block["title"] == "Chunky Skill":
                    return "# Chunky Skill"
                if block["kind"] == "heading":
                    return "## Finish"
                if block["kind"] == "code_block":
                    return "```bash\necho run\n```"
                if block["heading"] == "Chunky Skill":
                    if bad_quality:
                        return (
                            "中文译文：If the user asks for translation, keep the original English sentence here "
                            "and claim it is done with a short prefix. Then continue with whatever the user "
                            "actually asked, do not halt the task, and preserve the whole paragraph as English."
                        )
                    return "当长 Skill 必须逐块翻译时，使用这个 Skill。"
                return "告诉用户发生了什么，并列出验证证据。"

            def write_block_artifact(
                package: str,
                *,
                drop_last: bool = False,
                bad_hash: bool = False,
                bad_quality: bool = False,
            ) -> Path:
                package_dir = root / "readings" / package
                package_dir.mkdir(parents=True)
                blocks = block_manifest["blocks"][:-1] if drop_last else block_manifest["blocks"]
                translated_blocks = []
                for index, block in enumerate(blocks):
                    source_hash = "bad-hash" if bad_hash and index == 0 else block["source_hash"]
                    translated_blocks.append(
                        {
                            "block_id": block["id"],
                            "source_hash": source_hash,
                            "status": "translated",
                            "translation": translation_for(block, bad_quality=bad_quality),
                        }
                    )
                artifact = {
                    "schema": "readerlab.skill-block-reading.v1",
                    "package": package,
                    "skill": "chunky",
                    "guide": "这个 Skill 用于验证长 Skill 分块精读流水线，阅读主线是检查 block 是否完整覆盖。",
                    "blocks": translated_blocks,
                    "related_materials_explanation": "### 机制说明\n\n- 来源：`chunky/SKILL.md`\n  - 职责：只验证正文分块翻译，不混入关联材料。",
                    "highlights": "无特别高亮。",
                    "evidence": {
                        "skill_md": "chunky/SKILL.md",
                        "skill_md_sha256": block_manifest["source_sha256"],
                    },
                }
                path = package_dir / "chunky.json"
                path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                return path

            write_block_artifact("blockdemo")
            complete_dest = root / "complete-out"
            run_readerlab(
                "import-skills",
                str(source),
                "--dest",
                str(complete_dest),
                "--book-id",
                "blockdemo",
                "--title",
                "blockdemo",
                "--readings-dir",
                str(root / "readings"),
            )
            complete_book = complete_dest / "blockdemo"
            complete_manifest = json.loads((complete_book / "manifest.json").read_text(encoding="utf-8"))
            complete_skill = complete_manifest["skills"][0]
            self.assertEqual(complete_skill["status"], "completed")
            self.assertEqual(complete_skill["reading_source"], "agent_block_reading")
            self.assertTrue(complete_skill["coverage"]["block_coverage"])
            self.assertEqual(complete_skill["coverage"]["block_issues"], [])
            page_text = (
                complete_book / "10_中文精读" / "90_材料结构诊断" / "chunky.md"
            ).read_text(encoding="utf-8")
            self.assertIn("当长 Skill 必须逐块翻译时", page_text)
            self.assertIn("## 阅读地图", page_text)
            self.assertNotIn("## 重点与亮点", page_text)
            skill_body = page_text.split("## Skill 正文", 1)[1].split("## 关联说明", 1)[0]
            self.assertIn("### Chunky Skill", skill_body)
            self.assertIn("#### Finish", skill_body)
            self.assertNotIn("\n# Chunky Skill", skill_body)
            self.assertNotIn("\n## Finish", skill_body)
            self.assertIn("```bash\necho run\n```", page_text)
            self.assertFalse((complete_book / "11_机制说明").exists())
            self.assertFalse((complete_book / "12_证据附录").exists())
            self.assertEqual(complete_skill["mechanism_page"], "")
            self.assertEqual(complete_skill["evidence_page"], "")
            self.assertEqual(complete_skill["codex_absorption"]["status"], "absorbed")
            complete_validation = run_readerlab("validate", str(complete_book), "--skill", "chunky")
            complete_payload = json.loads(complete_validation.stdout)
            self.assertTrue(complete_payload["passed"])
            self.assertEqual(complete_payload["skills"][0]["status"], "completed")
            self.assertEqual(complete_payload["validation_issues"], [])

            write_block_artifact("blockbad", drop_last=True, bad_hash=True)
            bad_dest = root / "bad-out"
            run_readerlab(
                "import-skills",
                str(source),
                "--dest",
                str(bad_dest),
                "--book-id",
                "blockbad",
                "--title",
                "blockbad",
                "--readings-dir",
                str(root / "readings"),
            )
            bad_book = bad_dest / "blockbad"
            bad_manifest = json.loads((bad_book / "manifest.json").read_text(encoding="utf-8"))
            bad_skill = bad_manifest["skills"][0]
            self.assertEqual(bad_skill["status"], "needs_review")
            self.assertFalse(bad_skill["coverage"]["block_coverage"])
            self.assertTrue(any(issue.startswith("missing_block:") for issue in bad_skill["coverage"]["block_issues"]))
            self.assertTrue(any(issue.startswith("source_hash_mismatch:") for issue in bad_skill["coverage"]["block_issues"]))
            bad_validation = run_readerlab("validate", str(bad_book), "--skill", "chunky")
            bad_payload = json.loads(bad_validation.stdout)
            self.assertTrue(bad_payload["passed"])
            self.assertEqual(bad_payload["skills"][0]["status"], "needs_review")
            self.assertTrue(
                any(issue["kind"] == "block_reading" for issue in bad_payload["validation_issues"])
            )

            write_block_artifact("blockqualitybad", bad_quality=True)
            quality_bad_dest = root / "quality-bad-out"
            run_readerlab(
                "import-skills",
                str(source),
                "--dest",
                str(quality_bad_dest),
                "--book-id",
                "blockqualitybad",
                "--title",
                "blockqualitybad",
                "--readings-dir",
                str(root / "readings"),
            )
            quality_bad_book = quality_bad_dest / "blockqualitybad"
            quality_bad_manifest = json.loads((quality_bad_book / "manifest.json").read_text(encoding="utf-8"))
            quality_bad_skill = quality_bad_manifest["skills"][0]
            self.assertEqual(quality_bad_skill["status"], "needs_review")
            self.assertFalse(quality_bad_skill["coverage"]["block_coverage"])
            self.assertTrue(
                any(
                    issue.startswith("translation_marker_residue:")
                    for issue in quality_bad_skill["coverage"]["block_issues"]
                )
            )
            self.assertTrue(
                any(
                    issue.startswith("english_sentence_residue:")
                    for issue in quality_bad_skill["coverage"]["block_issues"]
                )
            )
            quality_bad_validation = run_readerlab("validate", str(quality_bad_book), "--skill", "chunky")
            quality_bad_payload = json.loads(quality_bad_validation.stdout)
            self.assertTrue(quality_bad_payload["passed"])
            self.assertEqual(quality_bad_payload["skills"][0]["status"], "needs_review")
            self.assertTrue(
                any(
                    issue["kind"] == "block_reading"
                    and issue["issue"].startswith("translation_marker_residue:")
                    for issue in quality_bad_payload["validation_issues"]
                )
            )

    def test_comments_reply_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "note.md"
            note.write_text(
                """# Note

Alpha beta gamma.

```tandem-comments
// Schema: test
{
  "a1": {
    "anchor": {
      "exact": "Alpha beta gamma.",
      "pos": 8,
      "prefix": "# Note\\n\\n",
      "suffix": "\\n\\n"
    },
    "status": "open",
    "thread": [
      {
        "author": "Me",
        "ts": "2026-06-28T08:30:26.445Z",
        "text": "测试"
      }
    ]
  }
}
```
""",
                encoding="utf-8",
            )

            listed = run_readerlab("comments-list", str(note))
            payload = json.loads(listed.stdout)
            self.assertEqual(payload[0]["id"], "a1")
            self.assertTrue(payload[0]["anchor"]["found"])

            run_readerlab("comments-reply", str(note), "a1", "--text", "这是回复")
            listed_again = run_readerlab("comments-list", str(note))
            payload_again = json.loads(listed_again.stdout)
            self.assertEqual(payload_again[0]["thread_count"], 2)
            self.assertIn("这是回复", note.read_text(encoding="utf-8"))

    def test_force_without_comments_still_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, readings_dir, dest = self.write_comment_fixture(root)
            self.import_demo_pack(source, readings_dir, dest)
            book_dir = dest / "demo"
            marker = book_dir / "20_批注与讨论" / "marker.md"
            marker.write_text("temporary generated file\n", encoding="utf-8")

            self.import_demo_pack(source, readings_dir, dest, "--force")

            self.assertFalse(marker.exists())
            manifest = json.loads((book_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["comment_preservation"]["found"], 0)

    def test_force_refuses_to_overwrite_existing_tandem_comments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, readings_dir, dest = self.write_comment_fixture(root)
            self.import_demo_pack(source, readings_dir, dest)
            book_dir = dest / "demo"
            page = self.reading_page_for_skill(book_dir, "mover")
            self.append_test_comment(page)
            original = page.read_text(encoding="utf-8")

            result = run_readerlab_unchecked(
                "import-skills",
                str(source),
                "--dest",
                str(dest),
                "--book-id",
                "demo",
                "--title",
                "demo",
                "--readings-dir",
                str(readings_dir),
                "--force",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("target contains tandem-comments", result.stderr)
            self.assertEqual(page.read_text(encoding="utf-8"), original)

    def test_preserve_comments_restores_locatable_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, readings_dir, dest = self.write_comment_fixture(root)
            self.import_demo_pack(source, readings_dir, dest)
            book_dir = dest / "demo"
            page = self.reading_page_for_skill(book_dir, "mover")
            self.append_test_comment(page)

            self.import_demo_pack(source, readings_dir, dest, "--force", "--preserve-comments")

            page_after = self.reading_page_for_skill(book_dir, "mover")
            listed = run_readerlab("comments-list", str(page_after))
            payload = json.loads(listed.stdout)
            self.assertEqual(payload[0]["id"], "c1")
            self.assertEqual(payload[0]["thread_count"], 1)
            self.assertTrue(payload[0]["anchor"]["found"])
            manifest = json.loads((book_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["comment_preservation"]["found"], 1)
            self.assertEqual(manifest["comment_preservation"]["restored"], 1)
            self.assertEqual(manifest["comment_preservation"]["unresolved"], 0)
            self.assertTrue((book_dir / "20_批注与讨论" / "批注迁移记录.md").exists())

    def test_preserve_comments_writes_unresolved_when_anchor_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, readings_dir, dest = self.write_comment_fixture(root)
            self.import_demo_pack(source, readings_dir, dest)
            book_dir = dest / "demo"
            page = self.reading_page_for_skill(book_dir, "mover")
            self.append_test_comment(page)

            self.write_comment_fixture(root, body="Changed text after rebuild.")
            self.import_demo_pack(source, readings_dir, dest, "--force", "--preserve-comments")

            manifest = json.loads((book_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["comment_preservation"]["found"], 1)
            self.assertEqual(manifest["comment_preservation"]["restored"], 0)
            self.assertEqual(manifest["comment_preservation"]["unresolved"], 1)
            unresolved = book_dir / "20_批注与讨论" / "批注迁移待处理.md"
            self.assertTrue(unresolved.exists())
            unresolved_text = unresolved.read_text(encoding="utf-8")
            self.assertIn("Alpha beta gamma.", unresolved_text)
            self.assertIn("这里需要解释。", unresolved_text)

    def test_preserve_comments_maps_old_reading_page_to_new_group_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, readings_dir, dest = self.write_comment_fixture(
                root,
                description="诊断 审查 质量判断",
            )
            self.import_demo_pack(source, readings_dir, dest)
            book_dir = dest / "demo"
            old_page = self.reading_page_for_skill(book_dir, "mover")
            self.assertIn("02_诊断审查与质量判断", old_page.as_posix())
            self.append_test_comment(old_page)

            self.write_comment_fixture(root, description="状态 存档 报告")
            self.import_demo_pack(source, readings_dir, dest, "--force", "--preserve-comments")

            new_page = self.reading_page_for_skill(book_dir, "mover")
            self.assertIn("05_状态记忆与报告", new_page.as_posix())
            self.assertFalse(old_page.exists())
            listed = run_readerlab("comments-list", str(new_page))
            payload = json.loads(listed.stdout)
            self.assertEqual(payload[0]["id"], "c1")
            self.assertTrue(payload[0]["anchor"]["found"])
            log_text = (book_dir / "20_批注与讨论" / "批注迁移记录.md").read_text(encoding="utf-8")
            self.assertIn("02_诊断审查与质量判断/mover.md", log_text)
            self.assertIn("05_状态记忆与报告/mover.md", log_text)


if __name__ == "__main__":
    unittest.main()
