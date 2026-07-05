#!/usr/bin/env python3
"""Skill/engineering-material route smoke for a ReaderLab shareable package."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def engineering_fixture_root() -> Path:
    package_fixture = PACKAGE_ROOT / "fixtures" / "engineering-route-smoke-v0"
    if package_fixture.is_dir():
        return package_fixture
    return PACKAGE_ROOT / "tests" / "fixtures" / "readerlab" / "engineering-route-smoke-v0"


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
            str(fixture / "audit/source-excerpts/skill-body.md"),
            str(fixture / "audit/source-excerpts/workflow-guards.md"),
        ],
        "output_root": str(output_root),
        "permission_boundary": "local_private_user_approved_only",
        "material_family": "skill_engineering",
        "requested_scope": "single skill engineering route smoke",
        "human_review_required": True,
        "declared_scope": "engineering-route-smoke-v0",
        "declared_units": ["cleaned-body", "technical-explanation", "asset-cards"],
        "full_book_required": False,
        "dual_view_required": True,
        "engineering_source_scope": ["src-engineering-skill-body", "src-engineering-workflow-guards"],
    }


def assert_config_matches_fixture(config_payload: dict[str, Any], fixture: Path) -> dict[str, bool]:
    registry = read_json(fixture / "audit" / "source-registry.v1.json", phase="configuration_structure")
    asset_cards = read_json(
        fixture / "audit" / "contracts" / "technical-asset-cards.v1.json",
        phase="configuration_structure",
    )
    controller = read_json(
        fixture / "audit" / "contracts" / "controller-decision.v1.json",
        phase="controller",
    )

    config_sources = [Path(path).resolve() for path in config_payload.get("source_paths", [])]
    registry_sources = [
        (fixture / source["source_path"]).resolve()
        for source in registry.get("sources", [])
        if source.get("source_role") == "primary_module"
    ]
    if config_sources != registry_sources:
        raise SmokeFailure(
            "configuration_structure",
            "run config source_paths must match source-registry primary_module paths and order",
        )

    engineering_scope = list(config_payload.get("engineering_source_scope") or [])
    registry_scope = [
        source["source_id"]
        for source in registry.get("sources", [])
        if source.get("source_role") == "primary_module"
    ]
    if engineering_scope != registry_scope:
        raise SmokeFailure(
            "configuration_structure",
            "engineering_source_scope must close over every primary_module source id in order",
        )

    full_source_track = fixture / "audit/full-source-track.md"
    if not full_source_track.is_file():
        raise SmokeFailure("structure_contract", "full-source evidence packet missing: audit/full-source-track.md")
    full_source_text = full_source_track.read_text(encoding="utf-8")
    for source_id in registry_scope:
        if source_id not in full_source_text:
            raise SmokeFailure("structure_contract", f"full-source evidence packet missing source id: {source_id}")

    cards = asset_cards.get("cards")
    if not isinstance(cards, list) or not cards:
        raise SmokeFailure("reader_evaluation", "technical asset cards must be a non-empty list")
    required_fields = ("purpose", "reader", "use_boundary", "selection_rule", "first_action")
    for card in cards:
        missing = [field for field in required_fields if not str(card.get(field) or "").strip()]
        if missing:
            raise SmokeFailure("reader_evaluation", f"asset card missing cold-start fields: {', '.join(missing)}")

    blocking_gates = controller.get("blocking_gates")
    decision = str(controller.get("controller_decision") or "")
    if not isinstance(blocking_gates, list) or not blocking_gates:
        raise SmokeFailure("controller", "controller-decision must declare blocking_gates")
    if any(gate.get("status") == "blocking" for gate in blocking_gates) and decision in {"accept", "limited_accept"}:
        raise SmokeFailure("controller", "blocking gate cannot produce accept or limited_accept")

    return {
        "source_paths_match_registry": True,
        "engineering_source_scope_closed": True,
        "full_source_evidence_packet_present": True,
        "asset_cards_cold_start_fields_present": True,
        "blocking_controller_enforced": True,
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


def assert_reader_pages(output_root: Path) -> dict[str, Any]:
    main_path = output_root / "reader" / "01_工程材料阅读页.md"
    tech_path = output_root / "reader" / "02_技术合伙人旁批.md"
    asset_path = output_root / "reader" / "03_资产卡导出页.md"
    for path in (main_path, tech_path, asset_path):
        if not path.is_file():
            raise SmokeFailure("reader_evaluation", f"reader page missing: {path}")

    main_text = main_path.read_text(encoding="utf-8")
    assert_in_order(
        main_text,
        [
            "## 处理过的一手正文",
            "### 模块1：`audit/source-excerpts/skill-body.md`",
            "这个 Skill 的正文先说明用途",
            "### 模块2：`audit/source-excerpts/workflow-guards.md`",
            "运行保护段要求",
            "## AI 旁批",
        ],
        phase="reader_evaluation",
    )
    tech_text = tech_path.read_text(encoding="utf-8")
    for marker in ("design_structure", "failure_protection", "reuse_point", "cost_and_boundary"):
        if marker not in tech_text:
            raise SmokeFailure("reader_evaluation", f"technical page missing marker: {marker}")
    asset_text = asset_path.read_text(encoding="utf-8")
    for marker in ("purpose", "reader", "use_boundary", "selection_rule", "first_action"):
        if marker not in asset_text:
            raise SmokeFailure("reader_evaluation", f"asset card page missing cold-start field: {marker}")
    forbidden = [
        "production ready",
        "reader_package_pass",
        "完整 GSTACK",
        "limited_accept",
    ]
    combined = "\n".join([main_text, tech_text, asset_text])
    for marker in forbidden:
        if marker in combined:
            raise SmokeFailure("reader_evaluation", f"reader page contains forbidden marker: {marker}")
    return {
        "main_reader_page": "reader/01_工程材料阅读页.md",
        "technical_page": "reader/02_技术合伙人旁批.md",
        "asset_cards_page": "reader/03_资产卡导出页.md",
        "cleaned_body_before_companion": main_text.index("## 处理过的一手正文") < main_text.index("## AI 旁批"),
        "asset_cards_have_cold_start_fields": True,
    }


def run_smoke() -> dict[str, Any]:
    fixture = engineering_fixture_root()
    if not fixture.is_dir():
        raise SmokeFailure("structure_contract", f"engineering smoke fixture missing: {fixture}")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        output_root = tmp_path / "engineering-output"
        run_config = tmp_path / "engineering-run-config.json"
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
        reader_result = assert_reader_pages(output_root)

    return {
        "schema": "readerlab.engineering-route-smoke.v1",
        "status": "pass",
        "check_class": "skill_engineering_route_smoke",
        "not_reader_acceptance": True,
        "not_production_ready": True,
        "material_family": config_result.get("material_family"),
        "engineering_source_scope": config_payload.get("engineering_source_scope"),
        "config_cross_check": config_cross_check,
        "verification_layers": {
            "configuration_structure": "pass",
            "runner_contract": "pass" if len(render_result.get("rendered_pages") or []) >= 3 else "fail",
            "quality_gate_request": "pass",
            "reader_evaluation": "machine_smoke_only",
            "blocking_controller": "pass",
            "human_acceptance": "not_run",
        },
        "reader_pages": reader_result,
    }


def main() -> int:
    try:
        result = run_smoke()
    except SmokeFailure as exc:
        print(
            json.dumps(
                {
                    "schema": "readerlab.engineering-route-smoke.v1",
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
