from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
MODULE_PATH = WORKSPACE / "scripts" / "t226_control_contract_preflight.py"
SPEC = importlib.util.spec_from_file_location("t226_control_contract_preflight", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


class T226ControlContractPreflightTests(unittest.TestCase):
    def test_full_preflight_passes_without_chapter_reads_or_semantic_calls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "preflight"
            result = PREFLIGHT.run_preflight(WORKSPACE, output)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["semantic_model_calls"], 0)
        self.assertEqual(result["chapter_body_reads"], 0)
        self.assertEqual(result["contract_structure"]["reader_question_count"], 6)
        self.assertEqual(result["contract_structure"]["reader_issue_field_count"], 11)
        self.assertEqual(result["artifact_registry"]["closure"], "PASS")

    def test_synthetic_preflight_refuses_workspace_output(self) -> None:
        output = WORKSPACE / ".t226-synthetic-preflight-must-not-be-created"
        self.assertFalse(output.exists())
        with self.assertRaisesRegex(
            PREFLIGHT.PreflightError, "must be outside the workspace"
        ):
            PREFLIGHT.run_preflight(WORKSPACE, output)
        self.assertFalse(output.exists())

    def test_official_bootstrap_creates_only_contract_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary) / "run"
            result = PREFLIGHT.bootstrap_contract_bundle(
                WORKSPACE, run_root / "control"
            )
            created = sorted(
                path.relative_to(run_root).as_posix()
                for path in run_root.rglob("*")
                if path.is_file()
            )

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["mode"], "official_contract_bootstrap")
        self.assertEqual(result["semantic_model_calls"], 0)
        self.assertEqual(result["chapter_body_reads"], 0)
        self.assertEqual(result["synthetic_artifacts_created"], 0)
        self.assertEqual(
            created,
            sorted(
                [
                    *(f"control/{name}" for name in PREFLIGHT.CONTRACT_FILENAMES),
                    "control/contract-manifest.md",
                ]
            ),
        )

    def test_v03_p1_candidate_form_is_rejected_as_human_local_review(self) -> None:
        contracts = PREFLIGHT.canonical_contract_bytes(WORKSPACE)
        contracts["human-local-review-form-v01.md"] = b"""# P1 product form

## Candidate

- candidate ID:
- WORTH_EXPANDING / REJECT
"""
        with self.assertRaisesRegex(
            PREFLIGHT.PreflightError, "section marker must occur exactly once"
        ):
            PREFLIGHT.validate_contract_structure(contracts, WORKSPACE)

    def test_human_questions_must_match_reader_rubric(self) -> None:
        contracts = PREFLIGHT.canonical_contract_bytes(WORKSPACE)
        contracts["human-local-review-form-v01.md"] = contracts[
            "human-local-review-form-v01.md"
        ].replace(
            "理论为什么需要在这里出现".encode(),
            "理论是否看起来很专业".encode(),
            1,
        )
        with self.assertRaisesRegex(
            PREFLIGHT.PreflightError, "human review questions do not match"
        ):
            PREFLIGHT.validate_contract_structure(contracts, WORKSPACE)

    def test_human_issue_fields_must_match_reader_rubric(self) -> None:
        contracts = PREFLIGHT.canonical_contract_bytes(WORKSPACE)
        contracts["human-local-review-form-v01.md"] = contracts[
            "human-local-review-form-v01.md"
        ].replace(b"\nartifact_sha\n", b"\nartifact_hash\n", 1)
        with self.assertRaisesRegex(
            PREFLIGHT.PreflightError, "human review issue fields do not match"
        ):
            PREFLIGHT.validate_contract_structure(contracts, WORKSPACE)

    def test_manifest_and_freeze_detect_post_write_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            control = Path(temporary) / "control"
            PREFLIGHT.render_contract_bundle(WORKSPACE, control)
            snapshot = PREFLIGHT.freeze_snapshot(control)
            target = control / "target-reader-contract-v01.md"
            target.write_bytes(target.read_bytes() + b"\n")

            with self.assertRaisesRegex(
                PREFLIGHT.PreflightError, "frozen contract mutation detected"
            ):
                PREFLIGHT.validate_frozen(snapshot, control)
            with self.assertRaisesRegex(
                PREFLIGHT.PreflightError, "differs from canonical frozen bytes"
            ):
                PREFLIGHT.validate_contract_bundle(WORKSPACE, control)

    def test_registry_requires_every_file_and_explicit_self_exemption(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary) / "run"
            control = run_root / "control"
            control.mkdir(parents=True)
            PREFLIGHT.exclusive_write(
                control / "production-group-ledger.jsonl", b'{"status":"complete"}\n'
            )
            PREFLIGHT.exclusive_write(
                run_root / "receipts" / "deterministic-receipt-v01.md",
                b"# receipt\n",
            )
            registry = control / "artifact-registry.jsonl"
            PREFLIGHT.build_artifact_registry(run_root, registry)
            result = PREFLIGHT.validate_artifact_registry(run_root, registry)
            self.assertEqual(result["closure"], "PASS")

            PREFLIGHT.exclusive_write(run_root / "review" / "late-file.md", b"# late\n")
            with self.assertRaisesRegex(
                PREFLIGHT.PreflightError, "artifact registry closure mismatch"
            ):
                PREFLIGHT.validate_artifact_registry(run_root, registry)

    def test_registry_rejects_invalid_self_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary) / "run"
            control = run_root / "control"
            control.mkdir(parents=True)
            PREFLIGHT.exclusive_write(control / "usage-ledger.jsonl", b"{}\n")
            registry = control / "artifact-registry.jsonl"
            PREFLIGHT.build_artifact_registry(run_root, registry)
            registry.write_text(
                registry.read_text(encoding="utf-8").replace(
                    '"status":"self_exempt"', '"status":"frozen"'
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                PREFLIGHT.PreflightError, "self-exemption record is invalid"
            ):
                PREFLIGHT.validate_artifact_registry(run_root, registry)

    def test_official_registry_rejects_synthetic_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary) / "run"
            control = run_root / "control"
            control.mkdir(parents=True)
            PREFLIGHT.exclusive_write(
                control / "production-group-ledger.jsonl",
                b'{"event":"preflight-fixture","status":"complete"}\n',
            )
            registry = control / "artifact-registry.jsonl"
            with self.assertRaisesRegex(
                PREFLIGHT.PreflightError, "contains synthetic fixture"
            ):
                PREFLIGHT.build_artifact_registry(run_root, registry)

    def test_every_generated_synthetic_fixture_is_rejected_individually(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            synthetic_root = temporary_root / "synthetic"
            PREFLIGHT.run_preflight(WORKSPACE, synthetic_root)
            fixture_paths = (
                "control/production-group-ledger.jsonl",
                "control/usage-ledger.jsonl",
                "receipts/deterministic-receipt-v01.md",
                "review/usage-summary.md",
            )
            for index, relative in enumerate(fixture_paths):
                official_root = temporary_root / f"official-{index}"
                target = official_root / relative
                PREFLIGHT.exclusive_write(
                    target, (synthetic_root / relative).read_bytes()
                )
                with self.subTest(relative=relative):
                    with self.assertRaisesRegex(
                        PREFLIGHT.PreflightError, "contains synthetic fixture"
                    ):
                        PREFLIGHT.build_artifact_registry(
                            official_root,
                            official_root / "control" / "artifact-registry.jsonl",
                        )


if __name__ == "__main__":
    unittest.main()
