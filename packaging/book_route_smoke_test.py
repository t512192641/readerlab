#!/usr/bin/env python3
"""Book-route smoke for a built or installed ReaderLab shareable package."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def book_fixture_root() -> Path:
    package_fixture = PACKAGE_ROOT / "fixtures" / "book-route-smoke-v0"
    if package_fixture.is_dir():
        return package_fixture
    return PACKAGE_ROOT / "tests" / "fixtures" / "readerlab" / "book-route-smoke-v0"


class SmokeFailure(Exception):
    def __init__(self, phase: str, message: str) -> None:
        super().__init__(message)
        self.phase = phase
        self.message = message


def run_readerlab(*args: str, phase: str) -> dict[str, Any]:
    result = subprocess.run(
        ["python3", "scripts/readerlab.py", *args],
        cwd=PACKAGE_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SmokeFailure(phase, result.stderr or result.stdout)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SmokeFailure(phase, f"readerlab command did not return JSON: {exc}") from exc


def read_json(path: Path, *, phase: str) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SmokeFailure(phase, f"required smoke contract missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SmokeFailure(phase, f"required smoke contract is not valid JSON: {path}: {exc}") from exc


def build_run_config_payload(fixture: Path, output_root: Path) -> dict[str, Any]:
    return {
        "source_paths": [
            str(fixture / "audit/source-excerpts/chapter-01.md"),
            str(fixture / "audit/source-excerpts/chapter-02.md"),
        ],
        "output_root": str(output_root),
        "permission_boundary": "local_private_user_approved_only",
        "material_family": "book_longform",
        "requested_scope": "two ordered chapter fixture smoke",
        "human_review_required": True,
        "declared_scope": "book-route-smoke-v0",
        "declared_units": ["chapter-01", "chapter-02"],
        "full_book_required": True,
        "dual_view_required": True,
    }


def assert_config_matches_fixture(config_payload: dict[str, Any], fixture: Path) -> dict[str, bool]:
    registry = read_json(fixture / "audit" / "source-registry.v1.json", phase="configuration_structure")
    catalog_map = read_json(
        fixture / "audit" / "contracts" / "catalog-map.v1.json",
        phase="configuration_structure",
    )

    config_sources = [Path(path).resolve() for path in config_payload.get("source_paths", [])]
    registry_sources = [
        (fixture / source["source_path"]).resolve()
        for source in registry.get("sources", [])
        if source.get("source_role") == "primary_text"
    ]
    if config_sources != registry_sources:
        raise SmokeFailure(
            "configuration_structure",
            "run config source_paths must match source-registry primary_text paths and order",
        )

    declared_units = list(config_payload.get("declared_units") or [])
    catalog_units = [
        unit["unit_id"]
        for unit in catalog_map.get("catalog", {}).get("reading_units", [])
        if "unit_id" in unit
    ]
    if declared_units != catalog_units:
        raise SmokeFailure(
            "configuration_structure",
            "run config declared_units must match catalog reading_units order",
        )

    return {
        "source_paths_match_registry": True,
        "declared_units_match_catalog": True,
    }


def assert_in_order(text: str, markers: list[str], *, phase: str) -> None:
    cursor = -1
    for marker in markers:
        position = text.find(marker, cursor + 1)
        if position == -1:
            raise SmokeFailure(phase, f"missing marker: {marker}")
        if position <= cursor:
            raise SmokeFailure(phase, f"marker out of order: {marker}")
        cursor = position


def assert_reader_page(output_root: Path) -> dict[str, Any]:
    reader_path = output_root / "reader" / "01_局部长文阅读页.md"
    if not reader_path.is_file():
        raise SmokeFailure("reader_evaluation", f"reader page missing: {reader_path}")
    text = reader_path.read_text(encoding="utf-8")
    assert_in_order(
        text,
        [
            "## 处理过的一手正文",
            "### 来源：`audit/source-excerpts/chapter-01.md`",
            "第一章先让读者停在问题本身",
            "## 第一节 问题从哪里来",
            "### 来源：`audit/source-excerpts/chapter-02.md`",
            "第二章把第一章的问题继续往前推",
            "## 第一节 从章节关系理解观点",
            "## AI 旁批",
            "## 深读判断",
            "## 状态边界",
        ],
        phase="reader_evaluation",
    )
    forbidden = [
        "reader_package_pass",
        "production ready",
        "20_AI陪读",
        "批注问题.md",
    ]
    for marker in forbidden:
        if marker in text:
            raise SmokeFailure("reader_evaluation", f"reader page contains forbidden marker: {marker}")
    return {
        "reader_page": "reader/01_局部长文阅读页.md",
        "body_before_companion": text.index("## 处理过的一手正文") < text.index("## AI 旁批"),
        "chapter_order_preserved": text.index("第一章先让读者停在问题本身")
        < text.index("第二章把第一章的问题继续往前推"),
    }


def run_smoke() -> dict[str, Any]:
    fixture = book_fixture_root()
    if not fixture.is_dir():
        raise SmokeFailure("structure_contract", f"book smoke fixture missing: {fixture}")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        output_root = tmp_path / "book-output"
        run_config = tmp_path / "book-run-config.json"
        config_payload = build_run_config_payload(fixture, output_root)
        run_config.write_text(json.dumps(config_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        config_result = run_readerlab("validate-run-config", str(run_config), phase="configuration_structure")
        if not config_result.get("passed"):
            raise SmokeFailure("configuration_structure", json.dumps(config_result, ensure_ascii=False))
        config_cross_check = assert_config_matches_fixture(config_payload, fixture)

        render_result = run_readerlab(
            "render-contract-package",
            str(fixture),
            str(output_root),
            phase="runner_contract",
        )
        eval_result = run_readerlab("eval-rendered-package", str(output_root), phase="quality_gate_request")
        if not eval_result.get("passed"):
            raise SmokeFailure("quality_gate_request", json.dumps(eval_result, ensure_ascii=False))
        reader_result = assert_reader_page(output_root)

    return {
        "schema": "readerlab.book-route-smoke.v1",
        "status": "pass",
        "check_class": "book_route_smoke",
        "not_reader_acceptance": True,
        "not_production_ready": True,
        "material_family": config_result.get("material_family"),
        "declared_units": config_result.get("declared_units"),
        "config_cross_check": config_cross_check,
        "verification_layers": {
            "configuration_structure": "pass",
            "runner_contract": "pass" if render_result.get("rendered_pages") else "fail",
            "quality_gate_request": "pass",
            "reader_evaluation": "machine_smoke_only",
            "controller": "human_status_pending_not_reader_package_pass",
            "human_acceptance": "not_run",
        },
        "reader_page": reader_result,
    }


def main() -> int:
    try:
        result = run_smoke()
    except SmokeFailure as exc:
        print(
            json.dumps(
                {
                    "schema": "readerlab.book-route-smoke.v1",
                    "status": "fail",
                    "failed_phase": exc.phase,
                    "message": exc.message,
                    "not_reader_acceptance": True,
                    "not_production_ready": True,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
