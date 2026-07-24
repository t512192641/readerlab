from __future__ import annotations

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(
    os.environ.get(
        "T226_WORKSPACE",
        CANDIDATE_ROOT,
    )
).resolve()
MODULE_PATH = Path(
    os.environ.get(
        "T226_RECOVERY_MODULE",
        WORKSPACE / "scripts" / "t226_p2_recovery.py",
    )
)
SPEC = importlib.util.spec_from_file_location("t226_p2_recovery", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
RECOVERY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RECOVERY)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


class T226P2RecoveryTests(unittest.TestCase):
    def make_fixture_workspace(self, root: Path) -> Path:
        fixture = root / "workspace"
        copy_file(
            WORKSPACE / RECOVERY.PARENT_TASKCARD_REL,
            fixture / RECOVERY.PARENT_TASKCARD_REL,
        )
        for relative in RECOVERY.EXISTING_RUN_FILES:
            source_relative = RECOVERY.RUN_REL / relative
            target = fixture / source_relative
            if source_relative in RECOVERY.FROZEN_FILES:
                copy_file(WORKSPACE / source_relative, target)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"")
        return fixture

    def seed_candidate_control(self, candidate_root: Path) -> None:
        copy_file(
            MODULE_PATH,
            candidate_root / RECOVERY.SCRIPT_REL,
        )
        copy_file(
            Path(__file__),
            candidate_root / RECOVERY.TEST_REL,
        )
        taskcard_source = WORKSPACE / RECOVERY.TASKCARD_REL
        if not taskcard_source.is_file():
            taskcard_source = CANDIDATE_ROOT / RECOVERY.TASKCARD_REL
        copy_file(
            taskcard_source,
            candidate_root / RECOVERY.TASKCARD_REL,
        )

    def write_passing_promotion_receipt(self, candidate_root: Path) -> None:
        receipt = {
            "tests": "PASS",
            "test_exit_code": 0,
            "red_regression": "OBSERVED",
            "red_exit_code": 1,
            "standards": "PASS",
            "spec": "PASS",
            "reviewed_control_hashes": RECOVERY._candidate_control_hashes(
                candidate_root
            ),
            "reviewed_candidate_manifest_sha256": RECOVERY.sha256_bytes(
                (candidate_root / RECOVERY.CANDIDATE_MANIFEST).read_bytes()
            ),
        }
        (candidate_root / RECOVERY.PROMOTION_RECEIPT).write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def synthetic_git_identity(self):
        return mock.patch.object(
            RECOVERY,
            "validate_git_identity",
            return_value={
                "status": "SYNTHETIC_TEST_ONLY",
                "branch": RECOVERY.EXPECTED_BRANCH,
                "head": RECOVERY.EXPECTED_HEAD,
            },
        )

    def test_invalid_v01_does_not_embed_complete_frozen_lesson_bytes(self) -> None:
        package = (WORKSPACE / RECOVERY.PACKAGE_V01_REL).read_bytes()
        counts = {
            candidate_id: package.count(
                (WORKSPACE / lesson_relative).read_bytes()
            )
            for candidate_id, lesson_relative in RECOVERY.LESSON_REL_BY_ID.items()
        }
        self.assertEqual(counts, {"C-01": 0, "C-03": 0})

    def test_rendered_v02_embeds_each_lesson_as_original_bytes_once(self) -> None:
        package, _ = RECOVERY.render_package(WORKSPACE)
        result = RECOVERY.validate_package_bytes(WORKSPACE, package)

        self.assertTrue(result["deterministic_render_equal"])
        self.assertEqual(
            [
                item["complete_original_byte_occurrences"]
                for item in result["lesson_results"]
            ],
            [1, 1],
        )

    def test_neutral_gate_rejects_any_extra_text(self) -> None:
        with self.assertRaisesRegex(
            RECOVERY.RecoveryError,
            "must contain only neutral identity and status",
        ):
            RECOVERY.parse_neutral_gate(
                b"candidate_id: C-01\n"
                b"p1_status: WORTH_EXPANDING\n"
                b"reason: product feedback\n",
                "C-01",
            )

    def test_candidate_root_must_be_outside_workspace(self) -> None:
        inside = WORKSPACE / ".forbidden-recovery-candidate"
        with self.assertRaisesRegex(
            RECOVERY.RecoveryError,
            "outside the workspace",
        ):
            RECOVERY.build_candidate(WORKSPACE, inside)
        self.assertFalse(inside.exists())

    @unittest.skipIf(
        os.environ.get("T226_PROMOTION_TEST_MODE") == "1",
        "real git identity is covered before the promotion test subprocess",
    )
    def test_real_workspace_git_identity_passes(self) -> None:
        result = RECOVERY.validate_git_identity(WORKSPACE)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["branch"], RECOVERY.EXPECTED_BRANCH)
        self.assertEqual(result["head"], RECOVERY.EXPECTED_HEAD)

    def test_wrong_git_identity_is_rejected(self) -> None:
        fake_results = [
            mock.Mock(stdout="wrong-branch\n"),
            mock.Mock(stdout=f"{RECOVERY.EXPECTED_HEAD}\n"),
        ]
        with mock.patch.object(
            RECOVERY.subprocess,
            "run",
            side_effect=fake_results,
        ):
            with self.assertRaisesRegex(
                RECOVERY.RecoveryError,
                "frozen git identity mismatch",
            ):
                RECOVERY.validate_git_identity(WORKSPACE)

    def test_stage_rejects_p2_downstream_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self.make_fixture_workspace(root)
            forbidden = (
                fixture
                / RECOVERY.RUN_REL
                / "acceptance"
                / "p2-product-verdicts.md"
            )
            forbidden.write_text("# forbidden\n", encoding="utf-8")

            with self.synthetic_git_identity():
                with self.assertRaisesRegex(
                    RECOVERY.RecoveryError,
                    "run path allowlist mismatch|downstream artifacts",
                ):
                    RECOVERY.validate_stage(fixture, allow_recovery_files=False)

    def test_promotion_requires_bound_two_axis_pass_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self.make_fixture_workspace(root)
            candidate_root = root / "candidate"
            self.seed_candidate_control(candidate_root)
            with self.synthetic_git_identity():
                RECOVERY.build_candidate(fixture, candidate_root)

            with self.assertRaisesRegex(
                RECOVERY.RecoveryError,
                "test and two-axis review receipt is required",
            ):
                with self.synthetic_git_identity():
                    RECOVERY.promote_control(fixture, candidate_root)
            for relative in RECOVERY.OFFICIAL_CONTROL_RELS:
                self.assertFalse((fixture / relative).exists())

    @unittest.skipIf(
        os.environ.get("T226_PROMOTION_TEST_MODE") == "1",
        "prevents recursive promotion when the hard gate reruns candidate tests",
    )
    def test_full_candidate_to_exclusive_promotion_and_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = self.make_fixture_workspace(root)
            candidate_root = root / "candidate"
            self.seed_candidate_control(candidate_root)
            with self.synthetic_git_identity():
                built = RECOVERY.build_candidate(fixture, candidate_root)
            self.assertEqual(built["candidate_validation"], "PASS")
            self.write_passing_promotion_receipt(candidate_root)

            with self.synthetic_git_identity():
                control = RECOVERY.promote_control(fixture, candidate_root)
            self.assertEqual(control["promotion"], "BYTE_IDENTICAL_O_EXCL_FIRST_WRITE")
            self.assertEqual(control["bound_tests"]["status"], "PASS")
            with self.synthetic_git_identity():
                artifacts = RECOVERY.promote_artifacts(fixture, candidate_root)
            self.assertEqual(
                artifacts["promotion"],
                "BYTE_IDENTICAL_O_EXCL_FIRST_WRITE",
            )
            with self.synthetic_git_identity():
                verified = RECOVERY.verify_official(fixture)
            self.assertEqual(
                verified["technical_state"],
                "READY_FOR_PRODUCT_REVIEW",
            )
            self.assertEqual(verified["product_verdict"], "NOT_MADE")
            self.assertEqual(
                verified["registry"]["claim_scope"],
                "INTEGRITY_ONLY",
            )
            for relative in (
                RECOVERY.OFFICIAL_CONTROL_RELS
                + RECOVERY.OFFICIAL_ARTIFACT_RELS
            ):
                self.assertEqual(
                    (fixture / relative).read_bytes(),
                    (
                        candidate_root / relative
                        if relative in RECOVERY.OFFICIAL_CONTROL_RELS
                        else RECOVERY.candidate_path(candidate_root, relative)
                    ).read_bytes(),
                )

            with self.assertRaisesRegex(
                RECOVERY.RecoveryError,
                "already exists|allowlist mismatch",
            ):
                with self.synthetic_git_identity():
                    RECOVERY.promote_artifacts(fixture, candidate_root)


if __name__ == "__main__":
    unittest.main()
