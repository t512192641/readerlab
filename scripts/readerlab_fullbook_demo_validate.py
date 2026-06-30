#!/usr/bin/env python3
"""Deterministic validator for the ReaderLab fullbook demo pack."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK_DIR = ROOT / "docs" / "reports" / "readerlab-fullbook-demo-v0"

REQUIRED_FILES = (
    "README.md",
    "elon/source-registry.v1.json",
    "elon/location-map.v1.json",
    "elon/grounded-global-map.v1.json",
    "elon/fullbook-reader-demo.md",
    "elon/assertions.md",
)
EXPECTED_SPINE_COUNT = 36
EXPECTED_ASSERTIONS = {
    "FULLBOOK-A01": "pass",
    "FULLBOOK-A02": "pass",
    "FULLBOOK-A03": "pass",
    "FULLBOOK-A04": "pass",
    "FULLBOOK-A05": "pass",
    "FULLBOOK-A06": "pass",
}


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _read_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as exc:
        return None, f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    except OSError as exc:
        return None, f"{path}: cannot read JSON: {exc}"


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


def _walk_ref_lists(value: Any, path: str = "$") -> list[tuple[str, Any]]:
    hits: list[tuple[str, Any]] = []
    ref_keys = {"location_refs", "primary_location_refs", "derived_location_refs"}
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            child_path = f"{path}.{child_key}"
            if child_key in ref_keys:
                hits.append((child_path, child_value))
            hits.extend(_walk_ref_lists(child_value, child_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(_walk_ref_lists(item, f"{path}[{index}]"))
    return hits


def _section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    next_match = re.search(r"^## ", text[match.end() :], re.MULTILINE)
    if not next_match:
        return text[match.end() :]
    return text[match.end() : match.end() + next_match.start()]


def _assertion_statuses(text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for line in text.splitlines():
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) >= 2 and parts[0].startswith("FULLBOOK-A"):
            statuses[parts[0]] = parts[1]
    return statuses


def _require_object(data: Any, rel: str) -> list[str]:
    if isinstance(data, dict):
        return []
    return [f"{rel}: top-level JSON value must be an object"]


def _check_required_files(pack_dir: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (pack_dir / rel).is_file():
            errors.append(f"{rel}: required file missing")
    return errors


def _check_human_status(payloads: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for rel, data in payloads.items():
        for json_path, value in _walk_key(data, "human_status"):
            if value != "pending":
                errors.append(f"{rel}: {json_path} must be pending, got {value!r}")
    return errors


def _check_source_registry(source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if source.get("schema") != "readerlab.source-registry.v1":
        errors.append("elon/source-registry.v1.json: schema must be readerlab.source-registry.v1")
    scope = source.get("source_scope")
    if not isinstance(scope, dict) or scope.get("coverage_status") != "full":
        errors.append("elon/source-registry.v1.json: source_scope.coverage_status must be full")
    inventory = source.get("spine_inventory")
    if not isinstance(inventory, dict):
        errors.append("elon/source-registry.v1.json: spine_inventory must be an object")
    else:
        if inventory.get("spine_item_count") != EXPECTED_SPINE_COUNT:
            errors.append("elon/source-registry.v1.json: spine_item_count must be 36")
        if inventory.get("registered_spine_item_count") != EXPECTED_SPINE_COUNT:
            errors.append("elon/source-registry.v1.json: registered_spine_item_count must be 36")
        if inventory.get("missing_spine_items") != []:
            errors.append("elon/source-registry.v1.json: missing_spine_items must be empty for full coverage")
    sources = source.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("elon/source-registry.v1.json: sources must be a non-empty list")
    else:
        source_ids = [item.get("source_id") for item in sources if isinstance(item, dict)]
        if "elon-epub-20260620" not in source_ids:
            errors.append("elon/source-registry.v1.json: missing primary source_id elon-epub-20260620")
    return errors


def _check_location_map(location: dict[str, Any], source_ids: set[str]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    if location.get("schema") != "readerlab.location-map.v1":
        errors.append("elon/location-map.v1.json: schema must be readerlab.location-map.v1")
    scope = location.get("source_scope")
    if not isinstance(scope, dict) or scope.get("coverage_status") != "full":
        errors.append("elon/location-map.v1.json: source_scope.coverage_status must be full")
    coverage = location.get("spine_coverage")
    if not isinstance(coverage, dict):
        errors.append("elon/location-map.v1.json: spine_coverage must be an object")
    else:
        if coverage.get("expected_spine_count") != EXPECTED_SPINE_COUNT:
            errors.append("elon/location-map.v1.json: expected_spine_count must be 36")
        if coverage.get("registered_spine_count") != EXPECTED_SPINE_COUNT:
            errors.append("elon/location-map.v1.json: registered_spine_count must be 36")
        if coverage.get("missing_spine_items") != []:
            errors.append("elon/location-map.v1.json: missing_spine_items must be empty for full coverage")

    items = location.get("locations")
    location_ids: set[str] = set()
    if not isinstance(items, list):
        errors.append("elon/location-map.v1.json: locations must be a list")
        return location_ids, errors
    if len(items) != EXPECTED_SPINE_COUNT:
        errors.append(f"elon/location-map.v1.json: locations must contain 36 items, got {len(items)}")
    expected_ids = {f"elon-spine-{index:03d}" for index in range(1, EXPECTED_SPINE_COUNT + 1)}
    for index, item in enumerate(items):
        label = f"elon/location-map.v1.json: locations[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        location_id = item.get("location_id")
        if not isinstance(location_id, str) or not location_id.strip():
            errors.append(f"{label}.location_id must be a non-empty string")
            continue
        if location_id in location_ids:
            errors.append(f"elon/location-map.v1.json: duplicate location_id {location_id!r}")
        location_ids.add(location_id)
        if item.get("source_id") not in source_ids:
            errors.append(f"{label}.source_id {item.get('source_id')!r} is not in source registry")
        if not item.get("path"):
            errors.append(f"{label}.path must be non-empty")
        if not item.get("spine"):
            errors.append(f"{label}.spine must be non-empty")
    missing = sorted(expected_ids - location_ids)
    if missing:
        errors.append(f"elon/location-map.v1.json: missing expected location ids: {', '.join(missing)}")
    return location_ids, errors


def _check_global_map(global_map: dict[str, Any], location_ids: set[str], source_full: bool, location_full: bool) -> list[str]:
    errors: list[str] = []
    if global_map.get("schema") != "readerlab.grounded-global-map.v1":
        errors.append("elon/grounded-global-map.v1.json: schema must be readerlab.grounded-global-map.v1")
    scope = global_map.get("source_scope")
    if not isinstance(scope, dict) or scope.get("coverage_status") != "full":
        errors.append("elon/grounded-global-map.v1.json: source_scope.coverage_status must be full")
    elif not (source_full and location_full):
        errors.append("elon/grounded-global-map.v1.json: full coverage requires full source registry and location map")

    for key in ("global_map", "whole_book_takeaways", "highlights", "transferable_principles", "confidence", "review_items", "machine_status", "human_status", "display"):
        if key not in global_map:
            errors.append(f"elon/grounded-global-map.v1.json: missing top-level field {key}")

    for key in ("whole_book_takeaways", "highlights", "transferable_principles"):
        value = global_map.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"elon/grounded-global-map.v1.json: {key} must be a non-empty list")
            continue
        for index, item in enumerate(value):
            refs = item.get("location_refs") if isinstance(item, dict) else None
            if not isinstance(refs, list) or not refs:
                errors.append(f"elon/grounded-global-map.v1.json: {key}[{index}].location_refs must be non-empty")

    for json_path, refs in _walk_ref_lists(global_map):
        if not isinstance(refs, list):
            errors.append(f"elon/grounded-global-map.v1.json: {json_path} must be a list")
            continue
        for index, ref in enumerate(refs):
            if ref not in location_ids:
                errors.append(f"elon/grounded-global-map.v1.json: {json_path}[{index}] {ref!r} is not in location-map")
    return errors


def _check_reader_markdown(pack_dir: Path) -> list[str]:
    path = pack_dir / "elon" / "fullbook-reader-demo.md"
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if "不是精选译文完整阅读页" not in text:
        errors.append("elon/fullbook-reader-demo.md: must state it is not a complete selected-translation reading page")
    for phrase in ("还没有精选译文正文", "还不是 LifeAtlas 正式写入", "还没有人工阅读质量验收"):
        if phrase not in text:
            errors.append(f"elon/fullbook-reader-demo.md: missing explicit gap {phrase!r}")

    takeaways = _section(text, "读完全书应带走的 6 个收获")
    highlights = _section(text, "值得标记的亮点")
    if not takeaways:
        errors.append("elon/fullbook-reader-demo.md: missing takeaways section")
    elif len(re.findall(r"refs：`elon-spine-", takeaways)) < 6:
        errors.append("elon/fullbook-reader-demo.md: each takeaway must include elon-spine refs")
    if not highlights:
        errors.append("elon/fullbook-reader-demo.md: missing highlights section")
    elif len(re.findall(r"refs：`elon-spine-", highlights)) < 4:
        errors.append("elon/fullbook-reader-demo.md: each highlight must include elon-spine refs")
    return errors


def _check_assertions(pack_dir: Path) -> list[str]:
    text = (pack_dir / "elon" / "assertions.md").read_text(encoding="utf-8")
    statuses = _assertion_statuses(text)
    errors: list[str] = []
    for assertion_id, expected in EXPECTED_ASSERTIONS.items():
        actual = statuses.get(assertion_id)
        if actual is None:
            errors.append(f"elon/assertions.md: missing assertion {assertion_id}")
        elif actual != expected:
            errors.append(f"elon/assertions.md: {assertion_id} must be {expected}, got {actual}")
    if "人工阅读质量验收仍为 `pending`" not in text:
        errors.append("elon/assertions.md: must keep human review pending")
    return errors


def validate_pack(pack_dir: Path) -> list[str]:
    errors = _check_required_files(pack_dir)
    if errors:
        return errors

    payloads: dict[str, Any] = {}
    for rel in (
        "elon/source-registry.v1.json",
        "elon/location-map.v1.json",
        "elon/grounded-global-map.v1.json",
    ):
        data, error = _read_json(pack_dir / rel)
        if error:
            errors.append(error)
            continue
        payloads[rel] = data
        errors.extend(_require_object(data, rel))
    if errors:
        return errors

    errors.extend(_check_human_status(payloads))

    source = payloads["elon/source-registry.v1.json"]
    location = payloads["elon/location-map.v1.json"]
    global_map = payloads["elon/grounded-global-map.v1.json"]
    errors.extend(_check_source_registry(source))
    source_ids = {item.get("source_id") for item in source.get("sources", []) if isinstance(item, dict)}
    location_ids, location_errors = _check_location_map(location, {source_id for source_id in source_ids if isinstance(source_id, str)})
    errors.extend(location_errors)
    source_full = source.get("source_scope", {}).get("coverage_status") == "full" and source.get("spine_inventory", {}).get("registered_spine_item_count") == EXPECTED_SPINE_COUNT
    location_full = location.get("source_scope", {}).get("coverage_status") == "full" and len(location_ids) == EXPECTED_SPINE_COUNT
    errors.extend(_check_global_map(global_map, location_ids, source_full, location_full))
    errors.extend(_check_reader_markdown(pack_dir))
    errors.extend(_check_assertions(pack_dir))
    return errors


def main(argv: list[str]) -> int:
    pack_dir = Path(argv[1]) if len(argv) > 1 else DEFAULT_PACK_DIR
    errors = validate_pack(pack_dir)
    if errors:
        print("FAIL ReaderLab fullbook demo validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS ReaderLab fullbook demo validation: {_relative(pack_dir, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
