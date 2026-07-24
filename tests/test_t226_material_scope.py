from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
MODULE_PATH = WORKSPACE / "scripts" / "t226_material_scope.py"
SPEC = importlib.util.spec_from_file_location("t226_material_scope", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MATERIAL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MATERIAL
SPEC.loader.exec_module(MATERIAL)


class T226MaterialScopeTests(unittest.TestCase):
    def test_real_source_materializes_exact_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary) / "run"
            result = MATERIAL.materialize(WORKSPACE, run_root)
            scope = (run_root / "inputs" / "chapter-scope.xhtml").read_bytes()

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["selected_chapter"], 2)
        self.assertEqual(result["scope_expected_bytes"], 82260)
        self.assertEqual(result["scope_actual_bytes"], 82260)
        self.assertEqual(
            result["scope_actual_sha256"],
            "934624eacafabf192b930519ff19a0c004fb12d8fc477c04922e5835cdaf69c6",
        )
        self.assertTrue(scope.endswith(b"</html>"))
        self.assertFalse(scope.endswith(b"</html>\n"))

    def test_second_materialization_refuses_existing_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary) / "run"
            MATERIAL.materialize(WORKSPACE, run_root)
            with self.assertRaisesRegex(MATERIAL.MaterialError, "already exists"):
                MATERIAL.materialize(WORKSPACE, run_root)

    def test_extract_scope_excludes_exactly_one_trailing_lf(self) -> None:
        source = WORKSPACE / MATERIAL.SOURCE_RELATIVE
        selection = MATERIAL.build_selection(source)
        import zipfile

        with zipfile.ZipFile(source) as archive:
            member = archive.read(selection.selected.member)
        scope = MATERIAL.extract_scope(member)
        self.assertEqual(member[len(scope) :], b"\n")
        self.assertEqual(len(scope), MATERIAL.EXPECTED_SCOPE_BYTES)

    def test_extract_scope_rejects_wrong_end_marker_count(self) -> None:
        with self.assertRaisesRegex(MATERIAL.MaterialError, "marker count mismatch"):
            MATERIAL.extract_scope(b"<html></html></html>\n")

    def test_extract_scope_rejects_wrong_suffix(self) -> None:
        original = MATERIAL.EXPECTED_SCOPE_BYTES
        original_sha = MATERIAL.EXPECTED_SCOPE_SHA256
        try:
            MATERIAL.EXPECTED_SCOPE_BYTES = len(b"<html></html>")
            MATERIAL.EXPECTED_SCOPE_SHA256 = MATERIAL.sha256_bytes(b"<html></html>")
            with self.assertRaisesRegex(MATERIAL.MaterialError, "suffix mismatch"):
                MATERIAL.extract_scope(b"<html></html>\r\n")
        finally:
            MATERIAL.EXPECTED_SCOPE_BYTES = original
            MATERIAL.EXPECTED_SCOPE_SHA256 = original_sha

    def test_extract_scope_rejects_wrong_expected_sha(self) -> None:
        source = WORKSPACE / MATERIAL.SOURCE_RELATIVE
        selection = MATERIAL.build_selection(source)
        import zipfile

        with zipfile.ZipFile(source) as archive:
            member = archive.read(selection.selected.member)
        original = MATERIAL.EXPECTED_SCOPE_SHA256
        try:
            MATERIAL.EXPECTED_SCOPE_SHA256 = "0" * 64
            with self.assertRaisesRegex(MATERIAL.MaterialError, "scope mismatch"):
                MATERIAL.extract_scope(member)
        finally:
            MATERIAL.EXPECTED_SCOPE_SHA256 = original

    def test_materialize_rejects_source_change_after_manifest_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            workspace = temporary_root / "workspace"
            source = workspace / MATERIAL.SOURCE_RELATIVE
            source.parent.mkdir(parents=True)
            shutil.copy2(WORKSPACE / MATERIAL.SOURCE_RELATIVE, source)
            original_write = MATERIAL.exclusive_write

            def write_then_mutate(path: Path, data: bytes) -> None:
                original_write(path, data)
                if path.name == "material-selection-manifest.md":
                    with source.open("ab") as handle:
                        handle.write(b"x")

            MATERIAL.exclusive_write = write_then_mutate
            try:
                with self.assertRaisesRegex(
                    MATERIAL.MaterialError, "source SHA changed"
                ):
                    MATERIAL.materialize(workspace, temporary_root / "run")
            finally:
                MATERIAL.exclusive_write = original_write


if __name__ == "__main__":
    unittest.main()
