#!/usr/bin/env python3
"""Release-candidate review for the ReaderLab shareable Skill package."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_readerlab_package.py"
INSTALL_SMOKE = ROOT / "packaging" / "install_smoke_test.py"
PACKAGE_INSTALL_SMOKE = ROOT / "tests" / "install_smoke_test.py"


class ReviewFailure(Exception):
    def __init__(self, phase: str, message: str) -> None:
        super().__init__(message)
        self.phase = phase
        self.message = message


def run_command(command: list[str], *, cwd: Path, phase: str) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise ReviewFailure(phase, result.stderr or result.stdout)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {"stdout": result.stdout}
    return {
        "command": command,
        "returncode": result.returncode,
        "payload": payload,
        "stdout_first_line": result.stdout.splitlines()[0] if result.stdout.splitlines() else "",
    }


def require_status(payload: dict[str, Any], *, phase: str, expected: str = "pass") -> None:
    if payload.get("status") != expected:
        raise ReviewFailure(phase, f"expected status {expected!r}, got {payload.get('status')!r}")
    if payload.get("not_production_ready") is not True:
        raise ReviewFailure(phase, "payload must explicitly say not_production_ready: true")
    if payload.get("not_reader_acceptance") is not True:
        raise ReviewFailure(phase, "payload must explicitly say not_reader_acceptance: true")


def require_layered_route_payload(payload: dict[str, Any], *, phase: str) -> dict[str, str]:
    require_status(payload, phase=phase)
    layers = payload.get("verification_layers")
    if not isinstance(layers, dict):
        raise ReviewFailure(phase, "route smoke must expose verification_layers")
    required = {
        "configuration_structure",
        "runner_contract",
        "quality_gate_request",
        "reader_evaluation",
        "human_acceptance",
    }
    missing = sorted(required - set(layers))
    if missing:
        raise ReviewFailure(phase, f"route smoke missing verification layers: {', '.join(missing)}")
    if layers["reader_evaluation"] != "machine_smoke_only":
        raise ReviewFailure(phase, "reader_evaluation must remain machine_smoke_only at RC stage")
    if layers["human_acceptance"] != "not_run":
        raise ReviewFailure(phase, "human_acceptance must remain not_run at RC stage")
    return {str(key): str(value) for key, value in layers.items()}


def require_package_audit(package_root: Path) -> dict[str, Any]:
    audit_path = package_root / "PACKAGE_AUDIT.json"
    if not audit_path.is_file():
        raise ReviewFailure("clean_package_audit", "PACKAGE_AUDIT.json missing")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    require_status(audit, phase="clean_package_audit")
    failures = audit.get("failures")
    if failures:
        raise ReviewFailure("clean_package_audit", f"package audit failures: {failures}")
    forbidden_paths = [
        "docs/reports/",
        "private-material-validation",
        "fixtures/comment-replay/",
        "experiments/",
        "skills-canonical/packages/gstack",
    ]
    paths = [file["path"] for file in audit.get("files", []) if isinstance(file, dict) and "path" in file]
    for path in paths:
        for marker in forbidden_paths:
            if marker in path:
                raise ReviewFailure("clean_package_audit", f"forbidden package path marker: {path}")
    return audit


def summarize_route(name: str, payload: dict[str, Any], *, phase: str) -> dict[str, Any]:
    layers = require_layered_route_payload(payload, phase=phase)
    summary = {
        "status": payload["status"],
        "check_class": payload.get("check_class"),
        "material_family": payload.get("material_family"),
        "verification_layers": layers,
        "not_reader_acceptance": payload.get("not_reader_acceptance"),
        "not_production_ready": payload.get("not_production_ready"),
    }
    if name == "engineering":
        if layers.get("blocking_controller") != "pass":
            raise ReviewFailure(phase, "engineering route must prove blocking_controller: pass")
        summary["engineering_source_scope"] = payload.get("engineering_source_scope")
    return summary


def run_review() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        if BUILD_SCRIPT.is_file():
            build = run_command(
                ["python3", str(BUILD_SCRIPT), "--output-dir", str(tmp_path / "package"), "--force"],
                cwd=ROOT,
                phase="package_build",
            )
            build_payload = build["payload"]
            if build_payload.get("status") != "shareable_package_prepared":
                raise ReviewFailure("package_build", "package builder must produce shareable_package_prepared")
            package_root = tmp_path / "package" / str(build_payload["package_root"])
            review_mode = "repo_build_then_review"
        else:
            if not (ROOT / "PACKAGE_AUDIT.json").is_file():
                raise ReviewFailure("package_build", "package mode requires PACKAGE_AUDIT.json")
            package_root = ROOT
            review_mode = "built_package_self_review"
        audit = require_package_audit(package_root)

        package_smoke = run_command(
            ["python3", "tests/package_smoke_test.py"],
            cwd=package_root,
            phase="package_smoke",
        )
        install_smoke = INSTALL_SMOKE if INSTALL_SMOKE.is_file() else PACKAGE_INSTALL_SMOKE
        if not install_smoke.is_file():
            raise ReviewFailure("install_discovery_smoke", "install smoke entry missing")
        install = run_command(
            [
                "python3",
                str(install_smoke),
                "--package-root",
                str(package_root),
                "--install-root",
                str(tmp_path / "skill-root"),
                "--force",
            ],
            cwd=ROOT,
            phase="install_discovery_smoke",
        )
        require_status(install["payload"], phase="install_discovery_smoke")

        book = run_command(["python3", "tests/book_route_smoke_test.py"], cwd=package_root, phase="book_route")
        longform = run_command(
            ["python3", "tests/longform_route_smoke_test.py"],
            cwd=package_root,
            phase="longform_route",
        )
        engineering = run_command(
            ["python3", "tests/engineering_route_smoke_test.py"],
            cwd=package_root,
            phase="engineering_route",
        )

    return {
        "schema": "readerlab.release-candidate-review.v1",
        "status": "installable_release_candidate",
        "not_production_ready": True,
        "not_reader_acceptance": True,
        "check_class": "release_candidate_review",
        "review_mode": review_mode,
        "clean_package_audit": {
            "status": audit["status"],
            "check_class": audit.get("check_class"),
            "file_count": len(audit.get("files", [])),
            "failures": audit.get("failures", []),
        },
        "package_smoke": {
            "status": "pass",
            "check_class": "package_boundary_structure",
            "stdout_first_line": package_smoke["stdout_first_line"],
        },
        "install_discovery_smoke": {
            "status": install["payload"]["status"],
            "check_class": install["payload"].get("check_class"),
            "commands": sorted((install["payload"].get("commands") or {}).keys()),
        },
        "route_smokes": {
            "book": summarize_route("book", book["payload"], phase="book_route"),
            "longform_report_interview": summarize_route(
                "longform_report_interview",
                longform["payload"],
                phase="longform_route",
            ),
            "skill_engineering": summarize_route("engineering", engineering["payload"], phase="engineering_route"),
        },
        "anti_regression": {
            "production_ready_claim": "blocked",
            "reader_acceptance_claim": "blocked",
            "limited_accept_as_release": "blocked",
            "runner_quality_shortcut": "blocked_by_layered_route_payloads",
            "blocking_controller_bypass": "blocked_by_engineering_route",
            "private_or_local_package_pollution": "blocked_by_clean_package_audit",
        },
        "human_review": "not_run",
        "status_scope": (
            "installable_release_candidate only: package, install/discovery, and three route smokes passed; "
            "friend smoke and reader acceptance are still separate future gates"
        ),
    }


def main() -> int:
    try:
        payload = run_review()
    except ReviewFailure as exc:
        print(
            json.dumps(
                {
                    "schema": "readerlab.release-candidate-review.v1",
                    "status": "fail",
                    "failed_phase": exc.phase,
                    "message": exc.message,
                    "not_production_ready": True,
                    "not_reader_acceptance": True,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
