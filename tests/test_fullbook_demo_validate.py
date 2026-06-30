import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "readerlab_fullbook_demo_validate.py"
PACK = ROOT / "docs" / "reports" / "readerlab-fullbook-demo-v0"

_VALIDATOR_SPEC = importlib.util.spec_from_file_location("readerlab_fullbook_demo_validate", SCRIPT)
validator = importlib.util.module_from_spec(_VALIDATOR_SPEC)
assert _VALIDATOR_SPEC and _VALIDATOR_SPEC.loader
sys.modules[_VALIDATOR_SPEC.name] = validator
_VALIDATOR_SPEC.loader.exec_module(validator)


def _copy_pack(tmp: str) -> Path:
    copied = Path(tmp) / "pack"
    shutil.copytree(PACK, copied)
    return copied


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class FullbookDemoValidatorTests(unittest.TestCase):
    def test_current_fullbook_demo_passes(self) -> None:
        result = subprocess.run(
            ["python3", str(SCRIPT), str(PACK)],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS ReaderLab fullbook demo validation", result.stdout)

    def test_rejects_missing_spine_location(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "location-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["locations"] = data["locations"][:-1]
            data["spine_coverage"]["registered_spine_count"] = 35
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("36" in error and "locations" in error for error in errors), errors)

    def test_rejects_non_pending_human_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "grounded-global-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["human_status"] = "accepted"
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("human_status" in error and "pending" in error for error in errors), errors)

    def test_rejects_full_global_map_without_full_location_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "location-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["source_scope"]["coverage_status"] = "partial"
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("full coverage requires" in error for error in errors), errors)

    def test_rejects_takeaway_without_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "grounded-global-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["whole_book_takeaways"][0]["location_refs"] = []
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("whole_book_takeaways[0].location_refs" in error for error in errors), errors)

    def test_rejects_assertion_status_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "assertions.md"
            text = target.read_text(encoding="utf-8")
            target.write_text(text.replace("| FULLBOOK-A03 | pass |", "| FULLBOOK-A03 | partial |"), encoding="utf-8")

            errors = validator.validate_pack(copied)
            self.assertTrue(any("FULLBOOK-A03 must be pass" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
