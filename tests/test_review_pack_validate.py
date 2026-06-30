import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "readerlab_review_pack_validate.py"
PACK = ROOT / "docs" / "reports" / "readerlab-absorption-review-pack-v0"

_VALIDATOR_SPEC = importlib.util.spec_from_file_location("readerlab_review_pack_validate", SCRIPT)
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


class ReviewPackValidatorTests(unittest.TestCase):
    def test_current_review_pack_passes(self) -> None:
        result = subprocess.run(
            ["python3", str(SCRIPT), str(PACK)],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS ReaderLab review pack validation", result.stdout)

    def test_rejects_accepted_human_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "catalog-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["human_status"] = "accepted"
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("human_status" in error and "pending" in error for error in errors), errors)

    def test_rejects_full_coverage_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "dbs" / "capability-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["source_scope"]["coverage_status"] = "full"
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("coverage_status" in error and "full" in error for error in errors), errors)

    def test_rejects_missing_required_source_registry_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "source-registry.v1.json"
            target.unlink()

            errors = validator.validate_pack(copied)
            self.assertTrue(
                any("elon/source-registry.v1.json" in error and "required file missing" in error for error in errors),
                errors,
            )

    def test_rejects_location_source_id_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "dbs" / "location-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["locations"][0]["source_id"] = "dbs-missing-source"
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(
                any("source_id 'dbs-missing-source'" in error and "source-registry" in error for error in errors),
                errors,
            )

    def test_rejects_elon_candidate_primary_refs_only_distillation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "part2-local-deepread.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            candidate = data["local_deepread"]["distillation_candidates"][0]
            candidate["claim_refs"][0]["primary_location_refs"] = ["elon-loc-part2-distillation"]
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(
                any("primary_location_refs" in error and "distillation" in error for error in errors),
                errors,
            )

    def test_rejects_elon_candidate_mismatched_claim_id_and_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "part2-local-deepread.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            candidate_claim_ref = data["local_deepread"]["distillation_candidates"][0]["claim_refs"][0]
            candidate_claim_ref["claim_ref_id"] = "elon-part2-claim-missing"
            candidate_claim_ref["primary_location_refs"] = [
                "elon-loc-part2-shortest-path-communication"
            ]
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(
                any("claim_ref_id 'elon-part2-claim-missing'" in error and "top-level claim_refs" in error for error in errors),
                errors,
            )

    def test_rejects_tampered_assertion_status_and_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "assertions.md"
            text = target.read_text(encoding="utf-8")
            text = text.replace("| ELON-A05 | partial |", "| ELON-A05 | pass |")
            text = text.replace("| ELON-A07 | pass |", "| ELON-A99 | pass |")
            target.write_text(text, encoding="utf-8")

            errors = validator.validate_pack(copied)
            self.assertTrue(any("ELON-A05 must be partial" in error for error in errors), errors)
            self.assertTrue(any("missing assertion ELON-A07" in error for error in errors), errors)

    def test_rejects_empty_dbs_source_registry_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "dbs" / "source-registry.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["sources"] = []
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("sources must be a non-empty list" in error for error in errors), errors)

    def test_rejects_dbs_domain_source_refs_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "dbs" / "capability-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["capability_domains"][0]["source_refs"] = ["dbs-loc-missing"]
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(
                any("dbs-loc-missing" in error and "location-map" in error for error in errors),
                errors,
            )

    def test_rejects_empty_dbs_cross_skill_routes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "dbs" / "capability-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["cross_skill_routes"] = []
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("cross_skill_routes must be a non-empty list" in error for error in errors), errors)

    def test_rejects_duplicate_dbs_cross_skill_route_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "dbs" / "capability-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["cross_skill_routes"][1]["route_id"] = data["cross_skill_routes"][0]["route_id"]
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(
                any("duplicate cross_skill_routes route_id 'route-to-diagnosis'" in error for error in errors),
                errors,
            )

    def test_rejects_dbs_cross_skill_route_unknown_domain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "dbs" / "capability-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["cross_skill_routes"][0]["from"] = "dbs-missing-domain"
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(
                any("dbs-missing-domain" in error and "capability_domains" in error for error in errors),
                errors,
            )

    def test_rejects_empty_dbs_review_items(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "dbs" / "capability-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["review_items"] = []
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("review_items must be a non-empty list" in error for error in errors), errors)

    def test_rejects_forbidden_grounded_global_map_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = _copy_pack(tmp)
            target = copied / "elon" / "catalog-map.v1.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["schema"] = "readerlab.grounded-global-map.v1"
            _write_json(target, data)

            errors = validator.validate_pack(copied)
            self.assertTrue(any("forbidden schema readerlab.grounded-global-map.v1" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
