from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
RUN_TOOL = ROOT / "tools/run.py"
REQUIRED_CHECKS = (
    "artifact_type",
    "fields",
    "source",
    "synthetic",
    "version",
)


def _run_tool(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, os.fspath(RUN_TOOL), *(os.fspath(arg) for arg in args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _new_run(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "workspace"
    root.mkdir()
    material = root / "material.bin"
    material.write_bytes(b"fixture material")
    run_dir = root / "runs" / "T-01"
    run_dir.parent.mkdir()
    result = _run_tool(
        "new",
        run_dir,
        "--root",
        root,
        "--material",
        material,
        "--source",
        "fixture",
        "--scope",
        "promotion regression",
        "--route",
        "book",
    )
    assert result.returncode == 0, result.stderr
    return run_dir, tmp_path / "candidate.md"


def _write_validator(path: Path, body: str) -> Path:
    path.write_text(
        "from __future__ import annotations\n"
        "import hashlib\n"
        "import json\n"
        "import os\n"
        "from pathlib import Path\n"
        f"{body}\n",
        encoding="utf-8",
    )
    return path


def _pass_validator(path: Path) -> Path:
    return _write_validator(
        path,
        """
candidate = Path(os.environ["READERLAB_CANDIDATE"])
payload = candidate.read_bytes()
print(json.dumps({
    "status": "PASS",
    "candidate_sha256": hashlib.sha256(payload).hexdigest(),
    "candidate_bytes": len(payload),
    "checks": {
        "artifact_type": "PASS",
        "fields": "PASS",
        "source": "PASS",
        "synthetic": "PASS",
        "version": "NOT_APPLICABLE",
    },
}, sort_keys=True))
""".strip(),
    )


def _promote(
    run_dir: Path,
    candidate: Path,
    validator: Path,
) -> subprocess.CompletedProcess[str]:
    return _run_tool(
        "promote",
        run_dir,
        "--candidate",
        candidate,
        "--target",
        "raw/p1-candidates.md",
        "--validator",
        sys.executable,
        validator,
    )


def _load_run_tool() -> object:
    spec = importlib.util.spec_from_file_location("readerlab_run_tool", RUN_TOOL)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RunPromotionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_validator_fail_still_invokes_promotion_but_target_stays_absent(
        self,
    ) -> None:
        run_dir, candidate = _new_run(self.tmp_path)
        (run_dir / "locked/chapter-scope.xhtml").write_bytes(
            b"<p>the only frozen excerpt</p>"
        )
        candidate.write_bytes(b"EXCERPT: fabricated excerpt")
        validator = _write_validator(
            self.tmp_path / "validator_fail.py",
            """
candidate = Path(os.environ["READERLAB_CANDIDATE"]).read_bytes()
scope = (
    Path(os.environ["READERLAB_RUN_DIR"]) / "locked/chapter-scope.xhtml"
).read_bytes()
excerpt = candidate.removeprefix(b"EXCERPT: ")
assert excerpt not in scope
print(json.dumps({
    "status": "FAIL",
    "candidate_sha256": hashlib.sha256(candidate).hexdigest(),
    "candidate_bytes": len(candidate),
    "checks": {name: "FAIL" for name in (
        "artifact_type", "fields", "source", "synthetic", "version"
    )},
}, sort_keys=True))
raise SystemExit(1)
""".strip(),
        )

        result = _promote(run_dir, candidate, validator)

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run_dir / "raw/p1-candidates.md").exists())

    def test_missing_explicit_pass_result_keeps_target_absent(self) -> None:
        run_dir, candidate = _new_run(self.tmp_path)
        candidate.write_bytes(b"candidate")
        validator = _write_validator(self.tmp_path / "validator_empty.py", "pass")

        result = _promote(run_dir, candidate, validator)

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run_dir / "raw/p1-candidates.md").exists())

    def test_explicit_pass_promotes_exact_candidate_bytes(self) -> None:
        run_dir, candidate = _new_run(self.tmp_path)
        candidate_bytes = b"candidate\\x00bytes\\nwithout rewriting"
        candidate.write_bytes(candidate_bytes)
        validator = _pass_validator(self.tmp_path / "validator_pass.py")

        result = _promote(run_dir, candidate, validator)

        self.assertEqual(result.returncode, 0, result.stderr)
        target = run_dir / "raw/p1-candidates.md"
        self.assertEqual(target.read_bytes(), candidate_bytes)
        evidence = json.loads(result.stdout)
        self.assertEqual(evidence["status"], "PROMOTED")
        self.assertEqual(
            evidence["candidate_sha256"],
            hashlib.sha256(candidate_bytes).hexdigest(),
        )
        self.assertEqual(evidence["candidate_bytes"], len(candidate_bytes))
        self.assertEqual(evidence["target"], "raw/p1-candidates.md")
        self.assertEqual(set(evidence["checks"]), set(REQUIRED_CHECKS))

    def test_existing_target_is_never_overwritten(self) -> None:
        run_dir, candidate = _new_run(self.tmp_path)
        candidate.write_bytes(b"replacement")
        target = run_dir / "raw/p1-candidates.md"
        original = b"existing official bytes"
        target.write_bytes(original)
        validator = _pass_validator(self.tmp_path / "validator_pass.py")

        result = _promote(run_dir, candidate, validator)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target.read_bytes(), original)

    def test_reported_synthetic_failure_blocks_promotion(self) -> None:
        run_dir, candidate = _new_run(self.tmp_path)
        candidate.write_bytes(b"synthetic candidate")
        validator = _write_validator(
            self.tmp_path / "validator_synthetic_fail.py",
            """
candidate = Path(os.environ["READERLAB_CANDIDATE"])
payload = candidate.read_bytes()
print(json.dumps({
    "status": "PASS",
    "candidate_sha256": hashlib.sha256(payload).hexdigest(),
    "candidate_bytes": len(payload),
    "checks": {
        "artifact_type": "PASS",
        "fields": "PASS",
        "source": "PASS",
        "synthetic": "FAIL",
        "version": "NOT_APPLICABLE",
    },
}, sort_keys=True))
""".strip(),
        )

        result = _promote(run_dir, candidate, validator)

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run_dir / "raw/p1-candidates.md").exists())

    def test_required_identity_checks_cannot_be_not_applicable(self) -> None:
        run_dir, candidate = _new_run(self.tmp_path)
        candidate.write_bytes(b"candidate with skipped validation")
        validator = _write_validator(
            self.tmp_path / "validator_all_not_applicable.py",
            """
candidate = Path(os.environ["READERLAB_CANDIDATE"])
payload = candidate.read_bytes()
print(json.dumps({
    "status": "PASS",
    "candidate_sha256": hashlib.sha256(payload).hexdigest(),
    "candidate_bytes": len(payload),
    "checks": {
        "artifact_type": "NOT_APPLICABLE",
        "fields": "NOT_APPLICABLE",
        "source": "NOT_APPLICABLE",
        "synthetic": "NOT_APPLICABLE",
        "version": "NOT_APPLICABLE",
    },
}, sort_keys=True))
""".strip(),
        )

        result = _promote(run_dir, candidate, validator)

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run_dir / "raw/p1-candidates.md").exists())

    def test_boolean_candidate_byte_count_is_rejected(self) -> None:
        run_dir, candidate = _new_run(self.tmp_path)
        candidate.write_bytes(b"x")
        validator = _write_validator(
            self.tmp_path / "validator_boolean_bytes.py",
            """
candidate = Path(os.environ["READERLAB_CANDIDATE"])
payload = candidate.read_bytes()
print(json.dumps({
    "status": "PASS",
    "candidate_sha256": hashlib.sha256(payload).hexdigest(),
    "candidate_bytes": True,
    "checks": {
        "artifact_type": "PASS",
        "fields": "PASS",
        "source": "PASS",
        "synthetic": "PASS",
        "version": "NOT_APPLICABLE",
    },
}, sort_keys=True))
""".strip(),
        )

        result = _promote(run_dir, candidate, validator)

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run_dir / "raw/p1-candidates.md").exists())

    def test_post_commit_cleanup_does_not_report_failed_promotion(self) -> None:
        run_dir, candidate = _new_run(self.tmp_path)
        candidate_bytes = b"candidate"
        candidate.write_bytes(candidate_bytes)
        validator = _pass_validator(self.tmp_path / "validator_pass.py")
        run_tool = _load_run_tool()
        fsync_calls = 0
        real_fsync_directory = run_tool._fsync_directory

        def fail_second_directory_fsync(path: Path) -> None:
            nonlocal fsync_calls
            fsync_calls += 1
            if fsync_calls == 2:
                raise OSError("injected cleanup fsync failure")
            real_fsync_directory(path)

        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                run_tool,
                "_fsync_directory",
                side_effect=fail_second_directory_fsync,
            ),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = run_tool.main(
                [
                    "promote",
                    os.fspath(run_dir),
                    "--candidate",
                    os.fspath(candidate),
                    "--target",
                    "raw/p1-candidates.md",
                    "--validator",
                    sys.executable,
                    os.fspath(validator),
                ]
            )

        self.assertEqual(result, 0, stderr.getvalue())
        self.assertEqual(
            (run_dir / "raw/p1-candidates.md").read_bytes(),
            candidate_bytes,
        )
        self.assertEqual(
            list((run_dir / "raw").glob(".readerlab-promote-*")),
            [],
        )
