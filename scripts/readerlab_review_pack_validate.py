#!/usr/bin/env python3
"""Deterministic validator for the ReaderLab absorption review pack."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK_DIR = ROOT / "docs" / "reports" / "readerlab-absorption-review-pack-v0"

REQUIRED_TOP_LEVEL = {
    "schema",
    "material",
    "source_scope",
    "confidence",
    "review_items",
    "machine_status",
    "human_status",
    "display",
}
ALLOWED_COVERAGE_STATUS = {"partial", "sample", "toc_only", "unknown"}
FORBIDDEN_SCHEMA = "readerlab.grounded-global-map.v1"
REQUIRED_FILES = (
    "README.md",
    "absorption-evidence.md",
    "elon/source-registry.v1.json",
    "elon/location-map.v1.json",
    "elon/catalog-map.v1.json",
    "elon/part2-local-deepread.v1.json",
    "elon/assertions.md",
    "dbs/source-registry.v1.json",
    "dbs/location-map.v1.json",
    "dbs/capability-map.v1.json",
    "dbs/assertions.md",
)
SCOPES = ("elon", "dbs")
EXPECTED_ASSERTIONS = {
    "elon/assertions.md": {
        "ELON-A01": "pass",
        "ELON-A02": "pass",
        "ELON-A03": "pass",
        "ELON-A04": "pass",
        "ELON-A05": "partial",
        "ELON-A06": "pass",
        "ELON-A07": "pass",
    },
    "dbs/assertions.md": {
        "DBS-A01": "pass",
        "DBS-A02": "partial",
        "DBS-A03": "partial",
        "DBS-A04": "partial",
        "DBS-A05": "partial",
        "DBS-A06": "pass",
        "DBS-A07": "pass",
    },
}


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _walk_key(value: Any, key: str, path: str = "$") -> list[tuple[str, Any]]:
    hits: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            child_path = f"{path}.{child_key}"
            if child_key == key:
                hits.append((child_path, child_value))
            hits.extend(_walk_key(child_value, key, child_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(_walk_key(item, key, f"{path}[{index}]"))
    return hits


def _walk_ref_lists(value: Any, path: str = "$") -> list[tuple[str, str, Any]]:
    hits: list[tuple[str, str, Any]] = []
    ref_keys = {"location_refs", "source_refs", "primary_location_refs", "derived_location_refs"}
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            child_path = f"{path}.{child_key}"
            if child_key in ref_keys:
                hits.append((child_path, child_key, child_value))
            hits.extend(_walk_ref_lists(child_value, child_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(_walk_ref_lists(item, f"{path}[{index}]"))
    return hits


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _check_required_files(pack_dir: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        path = pack_dir / rel
        if not path.is_file():
            errors.append(f"{rel}: required file missing")
    return errors


def _read_json_files(pack_dir: Path) -> tuple[dict[Path, Any], list[str]]:
    errors: list[str] = []
    payloads: dict[Path, Any] = {}
    json_paths = sorted(pack_dir.rglob("*.json"))
    if not json_paths:
        errors.append(f"{pack_dir}: no JSON files found")
        return payloads, errors

    for path in json_paths:
        try:
            payloads[path] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{_relative(path, pack_dir)}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        except OSError as exc:
            errors.append(f"{_relative(path, pack_dir)}: cannot read JSON: {exc}")
    return payloads, errors


def _scope_for_path(path: Path, pack_dir: Path) -> str | None:
    try:
        rel = path.relative_to(pack_dir)
    except ValueError:
        return None
    return rel.parts[0] if rel.parts and rel.parts[0] in SCOPES else None


def _require_object(data: Any, rel: str) -> list[str]:
    if isinstance(data, dict):
        return []
    return [f"{rel}: top-level JSON value must be an object"]


def _check_common_json(payloads: dict[Path, Any], pack_dir: Path) -> list[str]:
    errors: list[str] = []
    for path, data in payloads.items():
        rel = _relative(path, pack_dir)
        if not isinstance(data, dict):
            errors.append(f"{rel}: top-level JSON value must be an object")
            continue

        missing = sorted(REQUIRED_TOP_LEVEL - set(data))
        if missing:
            errors.append(f"{rel}: missing top-level fields: {', '.join(missing)}")

        schema = data.get("schema")
        if schema == FORBIDDEN_SCHEMA:
            errors.append(f"{rel}: forbidden schema {FORBIDDEN_SCHEMA}")

        for json_path, status in _walk_key(data, "human_status"):
            if status != "pending":
                errors.append(f"{rel}: {json_path} must be pending, got {status!r}")

        for json_path, coverage_status in _walk_key(data, "coverage_status"):
            if coverage_status not in ALLOWED_COVERAGE_STATUS:
                errors.append(
                    f"{rel}: {json_path} has invalid coverage_status {coverage_status!r}; "
                    f"allowed: {', '.join(sorted(ALLOWED_COVERAGE_STATUS))}"
                )
    return errors


def _collect_scope_indexes(payloads: dict[Path, Any], pack_dir: Path) -> tuple[dict[str, set[str]], dict[str, dict[str, dict[str, Any]]], list[str]]:
    errors: list[str] = []
    source_ids_by_scope: dict[str, set[str]] = {}
    locations_by_scope: dict[str, dict[str, dict[str, Any]]] = {}

    for scope in SCOPES:
        source_path = pack_dir / scope / "source-registry.v1.json"
        source_rel = _relative(source_path, pack_dir)
        source_data = payloads.get(source_path)
        source_ids: set[str] = set()
        if source_data is None:
            errors.append(f"{source_rel}: required file missing or unreadable")
        else:
            errors.extend(_require_object(source_data, source_rel))
            sources = source_data.get("sources") if isinstance(source_data, dict) else None
            if not isinstance(sources, list) or not sources:
                errors.append(f"{source_rel}: sources must be a non-empty list")
            else:
                for index, source in enumerate(sources):
                    label = f"{source_rel}: sources[{index}]"
                    if not isinstance(source, dict):
                        errors.append(f"{label} must be an object")
                        continue
                    source_id = source.get("source_id")
                    if not isinstance(source_id, str) or not source_id.strip():
                        errors.append(f"{label}.source_id must be a non-empty string")
                        continue
                    if source_id in source_ids:
                        errors.append(f"{source_rel}: duplicate source_id {source_id!r}")
                    source_ids.add(source_id)
        source_ids_by_scope[scope] = source_ids

        location_path = pack_dir / scope / "location-map.v1.json"
        location_rel = _relative(location_path, pack_dir)
        location_data = payloads.get(location_path)
        locations: dict[str, dict[str, Any]] = {}
        if location_data is None:
            errors.append(f"{location_rel}: required file missing or unreadable")
        else:
            errors.extend(_require_object(location_data, location_rel))
            location_items = location_data.get("locations") if isinstance(location_data, dict) else None
            if not isinstance(location_items, list) or not location_items:
                errors.append(f"{location_rel}: locations must be a non-empty list")
            else:
                for index, location in enumerate(location_items):
                    label = f"{location_rel}: locations[{index}]"
                    if not isinstance(location, dict):
                        errors.append(f"{label} must be an object")
                        continue
                    location_id = location.get("location_id")
                    if not isinstance(location_id, str) or not location_id.strip():
                        errors.append(f"{label}.location_id must be a non-empty string")
                        continue
                    if location_id in locations:
                        errors.append(f"{location_rel}: duplicate location_id {location_id!r}")
                    source_id = location.get("source_id")
                    if not isinstance(source_id, str) or not source_id.strip():
                        errors.append(f"{label}.source_id must be a non-empty string")
                    elif source_id not in source_ids:
                        errors.append(f"{label}.source_id {source_id!r} is not in {scope}/source-registry.v1.json")
                    locations[location_id] = location
        locations_by_scope[scope] = locations
    return source_ids_by_scope, locations_by_scope, errors


def _check_location_refs(payloads: dict[Path, Any], pack_dir: Path, locations_by_scope: dict[str, dict[str, dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    for path, data in payloads.items():
        if not isinstance(data, dict):
            continue
        scope = _scope_for_path(path, pack_dir)
        if scope is None:
            continue
        rel = _relative(path, pack_dir)
        valid_locations = locations_by_scope.get(scope, {})
        for json_path, key, value in _walk_ref_lists(data):
            if not isinstance(value, list):
                errors.append(f"{rel}: {json_path} must be a list of location ids")
                continue
            for index, ref in enumerate(value):
                if not isinstance(ref, str) or not ref.strip():
                    errors.append(f"{rel}: {json_path}[{index}] must be a non-empty location id")
                elif ref not in valid_locations:
                    errors.append(f"{rel}: {json_path}[{index}] {ref!r} is not in {scope}/location-map.v1.json")
            if key == "source_refs" and not value:
                errors.append(f"{rel}: {json_path} must not be empty")
    return errors


def _is_distillation_location(location: dict[str, Any]) -> bool:
    probe = " ".join(
        str(location.get(key, ""))
        for key in ("location_id", "source_id", "path", "block_id", "text_preview")
    ).lower()
    heading_path = location.get("heading_path")
    if isinstance(heading_path, list):
        probe += " " + " ".join(str(part).lower() for part in heading_path)
    return "distillation" in probe or "读后提炼" in probe or "提炼" in probe


def _check_elon_local_deepread(payloads: dict[Path, Any], pack_dir: Path) -> list[str]:
    errors: list[str] = []
    path = pack_dir / "elon" / "part2-local-deepread.v1.json"
    data = payloads.get(path)
    if data is None:
        return [f"{_relative(path, pack_dir)}: required file missing or unreadable"]

    rel = _relative(path, pack_dir)
    if data.get("schema") != "readerlab.local-deepread.v1":
        errors.append(f"{rel}: schema must be readerlab.local-deepread.v1")

    candidates = data.get("local_deepread", {}).get("distillation_candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append(f"{rel}: local_deepread.distillation_candidates must be a non-empty list")
        return errors

    for index, candidate in enumerate(candidates):
        label = f"{rel}: local_deepread.distillation_candidates[{index}]"
        if not isinstance(candidate, dict):
            errors.append(f"{label} must be an object")
            continue
        for key in ("source_refs", "claim_refs"):
            value = candidate.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"{label}.{key} must be a non-empty list")
        boundary = candidate.get("applicability_boundary")
        if not isinstance(boundary, str) or not boundary.strip():
            errors.append(f"{label}.applicability_boundary must be a non-empty string")
        if candidate.get("human_status") != "pending":
            errors.append(f"{label}.human_status must be pending")
    return errors


def _check_elon_a05(payloads: dict[Path, Any], pack_dir: Path, locations_by_scope: dict[str, dict[str, dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    path = pack_dir / "elon" / "part2-local-deepread.v1.json"
    data = payloads.get(path)
    if not isinstance(data, dict):
        return errors

    rel = _relative(path, pack_dir)
    locations = locations_by_scope.get("elon", {})
    top_claims = data.get("claim_refs")
    if not isinstance(top_claims, list) or not top_claims:
        errors.append(f"{rel}: claim_refs must be a non-empty list")
        top_claims = []

    top_claims_by_id: dict[str, dict[str, Any]] = {}
    for index, claim in enumerate(top_claims):
        label = f"{rel}: claim_refs[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{label} must be an object")
            continue
        claim_id = claim.get("claim_id")
        if isinstance(claim_id, str) and claim_id.strip():
            if claim_id in top_claims_by_id:
                errors.append(f"{rel}: duplicate claim_id {claim_id!r}")
            top_claims_by_id[claim_id] = claim
        else:
            errors.append(f"{label}.claim_id must be a non-empty string")
        primary_refs = claim.get("primary_location_refs")
        if not isinstance(primary_refs, list) or not primary_refs:
            errors.append(f"{label}.primary_location_refs must be a non-empty list")
        derived_refs = claim.get("derived_location_refs")
        if not isinstance(derived_refs, list):
            errors.append(f"{label}.derived_location_refs must be a list")

    candidates = data.get("local_deepread", {}).get("distillation_candidates")
    if not isinstance(candidates, list):
        return errors
    for index, candidate in enumerate(candidates):
        label = f"{rel}: local_deepread.distillation_candidates[{index}]"
        if not isinstance(candidate, dict):
            continue
        claim_refs = candidate.get("claim_refs")
        if not isinstance(claim_refs, list) or not claim_refs:
            errors.append(f"{label}.claim_refs must be a non-empty list")
            continue
        for claim_index, claim_ref in enumerate(claim_refs):
            claim_label = f"{label}.claim_refs[{claim_index}]"
            if not isinstance(claim_ref, dict):
                errors.append(f"{claim_label} must be an object")
                continue
            claim_ref_id = claim_ref.get("claim_ref_id")
            if not isinstance(claim_ref_id, str) or not claim_ref_id.strip():
                errors.append(f"{claim_label}.claim_ref_id must be a non-empty string")
                continue
            top_claim = top_claims_by_id.get(claim_ref_id)
            if top_claim is None:
                errors.append(f"{claim_label}.claim_ref_id {claim_ref_id!r} is not in top-level claim_refs")
                continue

            primary_refs = claim_ref.get("primary_location_refs")
            if not isinstance(primary_refs, list) or not primary_refs:
                errors.append(f"{claim_label}.primary_location_refs must be a non-empty list")
                continue
            for ref_index, ref in enumerate(primary_refs):
                if not isinstance(ref, str) or not ref.strip():
                    errors.append(f"{claim_label}.primary_location_refs[{ref_index}] must be a non-empty location id")
                elif ref not in locations:
                    errors.append(f"{claim_label}.primary_location_refs[{ref_index}] {ref!r} is not in elon/location-map.v1.json")
            known_primary_refs = [ref for ref in primary_refs if isinstance(ref, str) and ref in locations]
            if known_primary_refs and all(_is_distillation_location(locations[ref]) for ref in known_primary_refs):
                errors.append(f"{claim_label}.primary_location_refs must not only point to distillation or derived pages")

            top_primary_refs = top_claim.get("primary_location_refs")
            if isinstance(top_primary_refs, list) and top_primary_refs:
                top_primary_set = {ref for ref in top_primary_refs if isinstance(ref, str)}
                candidate_primary_set = {ref for ref in primary_refs if isinstance(ref, str)}
                if not candidate_primary_set or not candidate_primary_set.issubset(top_primary_set):
                    errors.append(
                        f"{claim_label}.primary_location_refs must match or be a non-empty subset of "
                        f"top-level claim {claim_ref_id!r} primary_location_refs"
                    )

            derived_refs = claim_ref.get("derived_location_refs")
            if not isinstance(derived_refs, list):
                errors.append(f"{claim_label}.derived_location_refs must be a list")
            else:
                for ref_index, ref in enumerate(derived_refs):
                    if not isinstance(ref, str) or not ref.strip():
                        errors.append(f"{claim_label}.derived_location_refs[{ref_index}] must be a non-empty location id")
                    elif ref not in locations:
                        errors.append(f"{claim_label}.derived_location_refs[{ref_index}] {ref!r} is not in elon/location-map.v1.json")
    return errors


def _review_item_text(data: dict[str, Any]) -> str:
    return json.dumps(data.get("review_items", []), ensure_ascii=False)


def _check_dbs_capability_map(payloads: dict[Path, Any], pack_dir: Path, locations_by_scope: dict[str, dict[str, dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    path = pack_dir / "dbs" / "capability-map.v1.json"
    data = payloads.get(path)
    if data is None:
        return [f"{_relative(path, pack_dir)}: required file missing or unreadable"]

    rel = _relative(path, pack_dir)
    if data.get("schema") != "readerlab.capability-map.v1":
        errors.append(f"{rel}: schema must be readerlab.capability-map.v1")
    coverage_status = data.get("source_scope", {}).get("coverage_status")
    if coverage_status != "sample":
        errors.append(f"{rel}: source_scope.coverage_status must be sample")
    domain_scope_status = data.get("capability_domains_scope", {}).get("coverage_status")
    if domain_scope_status is not None and domain_scope_status != "sample":
        errors.append(f"{rel}: capability_domains_scope.coverage_status must be sample when present")

    registry_path = pack_dir / "dbs" / "source-registry.v1.json"
    registry = payloads.get(registry_path)
    registry_rel = _relative(registry_path, pack_dir)
    if isinstance(registry, dict):
        registry_coverage_status = registry.get("source_scope", {}).get("coverage_status")
        if registry_coverage_status != "sample":
            errors.append(f"{registry_rel}: source_scope.coverage_status must be sample")

    domains = data.get("capability_domains")
    if not isinstance(domains, list) or not domains:
        errors.append(f"{rel}: capability_domains must be a non-empty list")
        domains = []
    valid_locations = locations_by_scope.get("dbs", {})
    domain_ids: set[str] = set()
    for index, domain in enumerate(domains):
        label = f"{rel}: capability_domains[{index}]"
        if not isinstance(domain, dict):
            errors.append(f"{label} must be an object")
            continue
        domain_id = domain.get("domain_id")
        if not isinstance(domain_id, str) or not domain_id.strip():
            errors.append(f"{label}.domain_id must be a non-empty string")
        elif domain_id in domain_ids:
            errors.append(f"{rel}: duplicate capability domain_id {domain_id!r}")
        else:
            domain_ids.add(domain_id)
        refs = domain.get("source_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{label}.source_refs must be a non-empty list")
            continue
        for ref_index, ref in enumerate(refs):
            if not isinstance(ref, str) or not ref.strip():
                errors.append(f"{label}.source_refs[{ref_index}] must be a non-empty location id")
            elif ref not in valid_locations:
                errors.append(f"{label}.source_refs[{ref_index}] {ref!r} is not in dbs/location-map.v1.json")

    routes = data.get("cross_skill_routes")
    if not isinstance(routes, list) or not routes:
        errors.append(f"{rel}: cross_skill_routes must be a non-empty list")
        routes = []
    route_ids: set[str] = set()
    for index, route in enumerate(routes):
        label = f"{rel}: cross_skill_routes[{index}]"
        if not isinstance(route, dict):
            errors.append(f"{label} must be an object")
            continue
        for key in ("route_id", "from", "to", "when", "uncertainty"):
            value = route.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}.{key} must be a non-empty string")
        route_id = route.get("route_id")
        if isinstance(route_id, str) and route_id.strip():
            if route_id in route_ids:
                errors.append(f"{rel}: duplicate cross_skill_routes route_id {route_id!r}")
            else:
                route_ids.add(route_id)
        from_id = route.get("from")
        if isinstance(from_id, str) and from_id.strip() and from_id not in domain_ids:
            errors.append(f"{label}.from {from_id!r} is not in capability_domains")
        to_id = route.get("to")
        if isinstance(to_id, str) and to_id.strip() and to_id not in domain_ids:
            errors.append(f"{label}.to {to_id!r} is not in capability_domains")

    review_items = data.get("review_items")
    review_item_texts: list[tuple[dict[str, Any], str, str]] = []
    if not isinstance(review_items, list) or not review_items:
        errors.append(f"{rel}: review_items must be a non-empty list")
        review_items = []
    for index, item in enumerate(review_items):
        label = f"{rel}: review_items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        text = json.dumps(item, ensure_ascii=False)
        text_lower = text.lower()
        review_item_texts.append((item, text, text_lower))

    if review_item_texts:
        has_old_global_conflict_blocker = any(
            item.get("status") == "blocked"
            and ("旧" in text or "old" in text_lower)
            and "LifeAtlas" in text
            and "global-map" in text
            and ("冲突" in text or "conflict" in text_lower)
            for item, text, text_lower in review_item_texts
        )
        if not has_old_global_conflict_blocker:
            errors.append(
                f"{rel}: review_items must include a blocked item for the old LifeAtlas global-map conflict"
            )
        if not any("24 Skills" in text for _, text, _ in review_item_texts):
            errors.append(f"{rel}: review_items must mention 24 Skills")
        if not any("cross_skill_routes" in text for _, text, _ in review_item_texts):
            errors.append(f"{rel}: review_items must mention cross_skill_routes")

    readme_path = pack_dir / "README.md"
    assertions_path = pack_dir / "dbs" / "assertions.md"
    try:
        combined = _read_text(readme_path) + "\n" + _read_text(assertions_path) + "\n" + _review_item_text(data)
    except OSError:
        combined = _review_item_text(data)

    required_fragments = {
        "sample": "sample",
        "24 Skills": "24 Skills",
        "cross_skill_routes": "cross_skill_routes",
        "旧/old LifeAtlas": "LifeAtlas",
        "global-map": "global-map",
    }
    for label, fragment in required_fragments.items():
        if fragment not in combined:
            errors.append(f"{rel}: README or review_items must mention {label}")
    if "冲突" not in combined and "conflict" not in combined.lower():
        errors.append(f"{rel}: README or review_items must mention the old global-map conflict")
    if "blocker" not in combined.lower() and "blocked" not in combined.lower():
        errors.append(f"{rel}: README or review_items must mark the old global-map conflict as a blocker")
    return errors


def _assertion_statuses(path: Path, expected_prefix: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        parts = [part.strip().lower() for part in line.strip().strip("|").split("|")]
        if len(parts) < 2:
            continue
        assertion_id = parts[0].upper()
        if not assertion_id.startswith(expected_prefix):
            continue
        result = re.sub(r"[^a-z_ -]", "", parts[1]).strip()
        statuses[assertion_id] = result
    return statuses


def _check_assertions(pack_dir: Path) -> list[str]:
    errors: list[str] = []
    for rel_path, wanted in EXPECTED_ASSERTIONS.items():
        path = pack_dir / rel_path
        rel = _relative(path, pack_dir)
        try:
            prefix = next(iter(wanted)).split("0", 1)[0]
            statuses = _assertion_statuses(path, prefix)
        except OSError as exc:
            errors.append(f"{rel}: cannot read assertions: {exc}")
            continue
        for assertion_id, expected_status in wanted.items():
            actual_status = statuses.get(assertion_id)
            if actual_status is None:
                errors.append(f"{rel}: missing assertion {assertion_id}")
            elif actual_status != expected_status:
                errors.append(f"{rel}: {assertion_id} must be {expected_status}, got {actual_status}")
        unexpected = sorted(set(statuses) - set(wanted))
        for assertion_id in unexpected:
            errors.append(f"{rel}: unexpected assertion {assertion_id}")
    return errors


def validate_pack(pack_dir: Path | str = DEFAULT_PACK_DIR) -> list[str]:
    pack_path = Path(pack_dir)
    errors: list[str] = []
    if not pack_path.exists():
        return [f"{pack_path}: pack directory does not exist"]
    if not pack_path.is_dir():
        return [f"{pack_path}: pack path is not a directory"]

    payloads, json_errors = _read_json_files(pack_path)
    errors.extend(json_errors)
    errors.extend(_check_required_files(pack_path))
    errors.extend(_check_common_json(payloads, pack_path))
    _, locations_by_scope, index_errors = _collect_scope_indexes(payloads, pack_path)
    errors.extend(index_errors)
    errors.extend(_check_location_refs(payloads, pack_path, locations_by_scope))
    errors.extend(_check_elon_local_deepread(payloads, pack_path))
    errors.extend(_check_elon_a05(payloads, pack_path, locations_by_scope))
    errors.extend(_check_dbs_capability_map(payloads, pack_path, locations_by_scope))
    errors.extend(_check_assertions(pack_path))
    return errors


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) > 1 or (args and args[0] in {"-h", "--help"}):
        print("Usage: python3 scripts/readerlab_review_pack_validate.py [PACK_DIR]")
        return 0 if args and args[0] in {"-h", "--help"} else 2

    pack_dir = Path(args[0]) if args else DEFAULT_PACK_DIR
    errors = validate_pack(pack_dir)
    if errors:
        print(f"FAIL ReaderLab review pack validation: {pack_dir}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS ReaderLab review pack validation: {pack_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
