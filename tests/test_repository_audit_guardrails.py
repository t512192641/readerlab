from __future__ import annotations

import hashlib
import re
import subprocess
import tempfile
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
ASSET_REGISTER = ROOT / "audit/ASSET-LIFECYCLE-REGISTER.md"
CURRENT_STATE = ROOT / "docs/current-task.md"
DEV_STATE = ROOT / "docs/dev-state.md"
COMPATIBILITY_STATE = ROOT / "CURRENT-STATE.md"
FINDINGS_REGISTER = ROOT / "audit/FINDINGS-REGISTER.md"
AUDIT_OPERATING_MODEL = ROOT / "audit/AUDIT-OPERATING-MODEL.md"
AUDITOR_CHARTER = ROOT / "audit/ENGINEERING-AUDITOR-CHARTER.md"
TASKCARD_TEMPLATE = ROOT / "taskcards/TEMPLATE.md"
EXECUTION_ROADMAP = ROOT / "blueprints/EXECUTION-ROADMAP.md"
INCIDENT_GUARDRAILS = ROOT / "audit/INCIDENT-GUARDRAILS.md"
TASK_ID_PATTERN = r"T[0-9]+(?:\.[0-9]+)+(?:-[A-Za-z0-9]+)*"


def _markdown_section(markdown: str, heading: str) -> str:
    start = markdown.index(heading)
    level = len(heading) - len(heading.lstrip("#"))
    remainder = markdown[start + len(heading) :]
    next_heading = re.search(rf"^#{{1,{level}}} ", remainder, re.MULTILINE)
    if next_heading is None:
        return remainder
    return remainder[: next_heading.start()]


def _blocker_paths_owned_by(
    task_id: str,
    existing_blocker_paths: set[str],
    known_task_ids: set[str] | None = None,
) -> list[str]:
    owner_candidates = known_task_ids or {task_id}

    def blocker_owner(path: str) -> str | None:
        filename = PurePosixPath(path).name
        candidates = [
            candidate
            for candidate in owner_candidates
            if filename == f"{candidate}-BLOCKER.md"
            or (
                filename.startswith(f"{candidate}-")
                and filename.endswith("-BLOCKER.md")
            )
        ]
        return max(candidates, key=len) if candidates else None

    return sorted(
        path
        for path in existing_blocker_paths
        if blocker_owner(path) == task_id
    )


def _control_value(markdown: str, key: str) -> str | None:
    key_lines = re.findall(
        rf"^> {re.escape(key)}:.*$",
        markdown,
        re.MULTILINE,
    )
    if len(key_lines) != 1:
        return None
    match = re.fullmatch(
        rf"> {re.escape(key)}: `([^`]+)`",
        key_lines[0],
    )
    return None if match is None else match.group(1)


def _is_authorized_verdict_source(
    verdict_source: str,
    current_task: str,
    current_run: str,
) -> bool:
    source_parts = PurePosixPath(verdict_source).parts
    if (
        not source_parts
        or verdict_source.startswith("/")
        or any(part in {"", ".", ".."} for part in source_parts)
    ):
        return False
    if verdict_source == current_task:
        return True
    run_parts = PurePosixPath(current_run).parts
    return (
        len(source_parts) > len(run_parts)
        and source_parts[: len(run_parts)] == run_parts
    )


def _is_canonical_state_target(
    root: Path,
    relative_path: str,
    parent_name: str,
    target_kind: str,
) -> bool:
    pure_path = PurePosixPath(relative_path)
    if (
        pure_path.as_posix() != relative_path
        or len(pure_path.parts) != 2
        or pure_path.parts[0] != parent_name
        or pure_path.parts[1] in {"", ".", ".."}
    ):
        return False

    name = pure_path.parts[1]
    if target_kind == "taskcard":
        if re.fullmatch(rf"{TASK_ID_PATTERN}\.md", name) is None:
            return False
    elif target_kind == "run":
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name) is None:
            return False
    else:
        raise ValueError(target_kind)

    parent = root / parent_name
    target = root / relative_path
    if parent.is_symlink() or target.is_symlink():
        return False
    if not parent.is_dir():
        return False
    if target.resolve().parent != parent.resolve():
        return False
    return target.is_file() if target_kind == "taskcard" else target.is_dir()


def _verdict_source_resolves_in_scope(
    root: Path,
    verdict_source: str,
    current_task: str,
    current_run: str,
) -> bool:
    source_path = (root / verdict_source).resolve()
    if verdict_source == current_task:
        return source_path == (root / current_task).resolve()
    return source_path.is_relative_to((root / current_run).resolve())


def _is_valid_next_production_authorization(
    root: Path,
    authorization: str,
) -> bool:
    return authorization == "none" or _is_canonical_state_target(
        root,
        authorization,
        "taskcards",
        "taskcard",
    )


def _blocker_permission_errors(
    markdown: str,
    task_id: str,
    existing_blocker_paths: set[str] | None = None,
    known_task_ids: set[str] | None = None,
) -> list[str]:
    expected_path = f"taskcards/{task_id}-BLOCKER.md"
    permission_lines = re.findall(
        r"^> blocker_permission:.*$",
        markdown,
        re.MULTILINE,
    )
    if len(permission_lines) != 1:
        return ["blocker_permission must appear exactly once"]
    permission_match = re.fullmatch(
        r"> blocker_permission: `([^`]+)`",
        permission_lines[0],
    )
    if permission_match is None:
        return ["invalid blocker_permission syntax"]

    permission = permission_match.group(1)
    if permission not in {"none", expected_path}:
        return ["invalid blocker_permission"]

    title_task_ids = re.findall(
        rf"^# ({TASK_ID_PATTERN})\b",
        markdown,
        re.MULTILINE,
    )
    if title_task_ids != [task_id]:
        return ["task title identity must appear exactly once and match the filename"]

    identity_headings = re.findall(
        r"^## 1\. 任务编号与标题$",
        markdown,
        re.MULTILINE,
    )
    if len(identity_headings) != 1:
        return ["task identity section must appear exactly once"]
    try:
        identity_section = _markdown_section(
            markdown,
            "## 1. 任务编号与标题",
        )
    except ValueError:
        return ["missing task identity section"]
    internal_task_ids = re.findall(
        rf"^`({TASK_ID_PATTERN})`[：:]",
        identity_section,
        re.MULTILINE,
    )
    if internal_task_ids != [task_id]:
        return ["task identity must appear exactly once and match the filename"]

    delivery_headings = re.findall(
        r"^## 4\. 交付文件清单$",
        markdown,
        re.MULTILINE,
    )
    if len(delivery_headings) != 1:
        return ["delivery section must appear exactly once"]
    try:
        delivery_section = _markdown_section(markdown, "## 4. 交付文件清单")
    except ValueError:
        return ["missing delivery section"]

    delivery_paths = [
        code_path or bare_path
        for code_path, bare_path in re.findall(
            r"^- (?:`([^`]+)`|(\S+))\s*$",
            delivery_section,
            re.MULTILINE,
        )
    ]
    blocker_paths = [
        path
        for path in delivery_paths
        if path.endswith("-BLOCKER.md")
    ]
    if permission == "none" and blocker_paths:
        return ["blocker path listed without permission"]
    related_existing_blockers: list[str] = []
    if existing_blocker_paths is not None:
        related_existing_blockers = _blocker_paths_owned_by(
            task_id,
            existing_blocker_paths,
            known_task_ids,
        )
    if permission == "none" and related_existing_blockers:
        return ["blocker file exists without permission"]
    if permission == expected_path and blocker_paths != [expected_path]:
        return ["permitted blocker path must appear exactly once in delivery list"]
    if permission == expected_path and any(
        path != expected_path for path in related_existing_blockers
    ):
        return ["non-canonical blocker file exists for this task"]
    return []


def _taskcard_governance_errors(
    markdown: str,
    task_id: str,
    existing_blocker_paths: set[str] | None = None,
    known_task_ids: set[str] | None = None,
) -> list[str]:
    errors = _blocker_permission_errors(
        markdown,
        task_id,
        existing_blocker_paths,
        known_task_ids,
    )
    if errors:
        return errors

    closeout_lines = re.findall(
        r"^> closeout-result:.*$",
        markdown,
        re.MULTILINE,
    )
    if len(closeout_lines) != 1:
        return ["closeout-result must appear exactly once"]
    closeout_match = re.fullmatch(
        r"> closeout-result: `(IN_PROGRESS|PASS|BLOCKED)`",
        closeout_lines[0],
    )
    if closeout_match is None:
        return ["invalid closeout-result"]

    delivery_section = _markdown_section(markdown, "## 4. 交付文件清单")
    delivery_paths = [
        code_path or bare_path
        for code_path, bare_path in re.findall(
            r"^- (?:`([^`]+)`|(\S+))\s*$",
            delivery_section,
            re.MULTILINE,
        )
    ]
    own_taskcard = f"taskcards/{task_id}.md"
    if delivery_paths.count(own_taskcard) != 1:
        return ["taskcard must authorize its own control-field closeout"]

    if delivery_paths.count("docs/current-task.md") != 1:
        return ["current task requires docs/current-task.md delivery authorization"]
    if delivery_paths.count("docs/dev-state.md") != 1:
        return ["current task requires docs/dev-state.md delivery authorization"]
    return []


def _next_production_authorization_errors(
    root: Path,
    authorization: str,
    existing_blocker_paths: set[str],
    known_task_ids: set[str],
) -> list[str]:
    if authorization == "none":
        return []
    if not _is_valid_next_production_authorization(root, authorization):
        return ["next production authorization is not a canonical taskcard"]

    taskcard_path = root / authorization
    task_id = taskcard_path.stem
    if _blocker_paths_owned_by(
        task_id,
        existing_blocker_paths,
        known_task_ids,
    ):
        return ["next production task already has a blocker file"]
    taskcard_text = taskcard_path.read_text(encoding="utf-8")
    governance_errors = _taskcard_governance_errors(
        taskcard_text,
        task_id,
        existing_blocker_paths,
        known_task_ids,
    )
    if governance_errors:
        return governance_errors
    if _control_value(taskcard_text, "closeout-result") != "IN_PROGRESS":
        return ["next production task must have closeout-result IN_PROGRESS"]
    return []


class RepositoryAuditGuardrailTests(unittest.TestCase):
    def test_retired_legacy_validator_is_absent_from_current_tree(self) -> None:
        self.assertFalse((ROOT / "validate.py").exists())
        self.assertFalse(
            (ROOT / "archive/legacy-code/validate-clean-seed.py").exists()
        )

    def test_asset_register_exhaustively_lists_taskcards_and_runs(self) -> None:
        text = ASSET_REGISTER.read_text(encoding="utf-8")

        recorded_taskcards = set(
            re.findall(r"`(taskcards/[A-Za-z0-9.-]+\.md)`", text)
        )
        actual_taskcards = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "taskcards").glob("*.md")
        }
        self.assertEqual(recorded_taskcards, actual_taskcards)

        recorded_runs = set(re.findall(r"`(runs/[A-Za-z0-9.-]+)`", text))
        actual_runs = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "runs").iterdir()
            if path.is_dir()
        }
        self.assertEqual(recorded_runs, actual_runs)

        recorded_docs = set(
            re.findall(r"`((?!taskcards/|runs/|examples/)[A-Za-z0-9_./-]+\.md)`", text)
        )
        actual_docs = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*.md")
            if ".git" not in path.parts
            and "runs" not in path.parts
            and "taskcards" not in path.parts
            and "examples" not in path.parts
        }
        self.assertEqual(recorded_docs, actual_docs)

    def test_root_readme_is_navigation_not_historical_state_dump(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertLessEqual(len(readme.splitlines()), 80)
        self.assertIn("docs/current-task.md", readme)
        self.assertIn("docs/dev-state.md", readme)
        self.assertIn("CURRENT-STATE.md", readme)
        self.assertIn("ASSET-LIFECYCLE-REGISTER.md", readme)
        recovery_object = "b39a284c10e09ad03b9af8b4899aea34f9b64dc1:README.md"
        self.assertIn(recovery_object.split(":", 1)[0], readme)
        recovery = subprocess.run(
            ["git", "cat-file", "-e", recovery_object],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(recovery.returncode, 0, recovery.stderr)
        for target in re.findall(r"\]\(([^)]+)\)", readme):
            self.assertTrue((ROOT / target).is_file(), target)

    def test_taskcard_template_keeps_known_cost_guardrails(self) -> None:
        template = TASKCARD_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("Web Search + Web Fetch", template)
        self.assertIn("禁止 Chrome remote debugging", template)
        self.assertIn("超过 2 个不纳入仓库的临时脚本", template)
        self.assertIn("完整审阅包默认只在本地保存并由 Git 忽略", template)
        self.assertIn("按任务单独授权准确材料、外部目的地与保留边界", template)

    def test_current_state_matches_current_task_product_verdict(self) -> None:
        state = CURRENT_STATE.read_text(encoding="utf-8")
        current_task = _control_value(state, "current-task")
        current_run = _control_value(state, "current-run")
        verdict = _control_value(state, "product-verdict")
        verdict_source = _control_value(state, "product-verdict-source")

        self.assertIsNotNone(current_task)
        self.assertTrue(
            _is_canonical_state_target(
                ROOT,
                current_task,
                "taskcards",
                "taskcard",
            )
        )
        self.assertIsNotNone(current_run)
        self.assertTrue(
            _is_canonical_state_target(
                ROOT,
                current_run,
                "runs",
                "run",
            )
        )
        self.assertIsNotNone(verdict)
        self.assertIsNotNone(verdict_source)
        self.assertRegex(
            _control_value(state, "execution-status") or "",
            r"^[A-Z][A-Z0-9_]*$",
        )
        self.assertRegex(
            _control_value(state, "governance-status") or "",
            r"^[A-Z][A-Z0-9_]*$",
        )
        next_authorization = _control_value(
            state,
            "next-production-authorization",
        )
        self.assertIsNotNone(next_authorization)
        self.assertTrue(
            _is_valid_next_production_authorization(
                ROOT,
                next_authorization,
            )
        )
        existing_blocker_paths = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*-BLOCKER.md")
            if ".git" not in path.parts
        }
        known_task_ids = {
            path.stem
            for path in (ROOT / "taskcards").glob("*.md")
            if re.fullmatch(TASK_ID_PATTERN, path.stem)
            and not path.stem.endswith("-BLOCKER")
        }
        self.assertEqual(
            _next_production_authorization_errors(
                ROOT,
                next_authorization,
                existing_blocker_paths,
                known_task_ids,
            ),
            [],
        )

        self.assertTrue(
            _is_authorized_verdict_source(
                verdict_source,
                current_task,
                current_run,
            ),
        )
        verdict_source_path = ROOT / verdict_source
        self.assertTrue(verdict_source_path.is_file())
        self.assertTrue(
            _verdict_source_resolves_in_scope(
                ROOT,
                verdict_source,
                current_task,
                current_run,
            )
        )
        if verdict != "unknown":
            verdict_text = (ROOT / verdict_source).read_text(encoding="utf-8")
            verdict_heading = re.search(
                r"^## [^\n]*产品判词[^\n]*$",
                verdict_text,
                re.MULTILINE,
            )
            self.assertIsNotNone(verdict_heading)
            self.assertEqual(
                len(
                    re.findall(
                        r"^## [^\n]*产品判词[^\n]*$",
                        verdict_text,
                        re.MULTILINE,
                    )
                ),
                1,
            )
            verdict_section = _markdown_section(
                verdict_text,
                verdict_heading.group(0),
            )
            self.assertIn(f"`{verdict}`", verdict_section)
            self.assertIn("产品负责人", verdict_section)
        else:
            verdict_evidence = []
            for candidate in [ROOT / current_task, *(ROOT / current_run).rglob("*.md")]:
                if candidate.is_symlink():
                    verdict_evidence.append(candidate.relative_to(ROOT).as_posix())
                    continue
                if re.search(
                    r"^## [^\n]*产品判词[^\n]*$",
                    candidate.read_text(encoding="utf-8"),
                    re.MULTILINE,
                ):
                    verdict_evidence.append(candidate.relative_to(ROOT).as_posix())
            self.assertEqual(verdict_evidence, [])

    def test_standard_mem_layers_have_single_owners_and_compatibility_only(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        compatibility = COMPATIBILITY_STATE.read_text(encoding="utf-8")
        dev_state = DEV_STATE.read_text(encoding="utf-8")
        fixed_layers = (
            "docs/current-task.md",
            "docs/dev-state.md",
            "docs/decisions.md",
            "docs/agent-run-ledger.md",
            "docs/research-log.md",
        )

        for layer in fixed_layers:
            self.assertIn(layer, agents)
            self.assertIn(layer, compatibility)
        for dynamic_field in (
            "current-task",
            "current-run",
            "execution-status",
            "product-verdict",
            "product-verdict-source",
            "next-production-authorization",
            "governance-status",
        ):
            self.assertIsNone(_control_value(compatibility, dynamic_field))
        self.assertNotIn("> next-production-authorization:", dev_state)
        self.assertNotIn("> product-verdict:", dev_state)
        self.assertIn("兼容入口", compatibility)

    def test_findings_register_does_not_duplicate_current_action_state(self) -> None:
        findings = FINDINGS_REGISTER.read_text(encoding="utf-8")
        action_section = _markdown_section(findings, "## 二、当前行动门引用")

        self.assertIn("docs/current-task.md", action_section)
        self.assertIn("docs/dev-state.md", action_section)
        for duplicated_field in (
            "当前产品判断：",
            "当前允许：",
            "当前禁止：",
            "解除 `RED` 的剩余最低条件：",
        ):
            self.assertNotIn(duplicated_field, action_section)
        self.assertNotRegex(
            findings,
            re.compile(r"^- 当前允许：", re.MULTILINE),
        )
        self.assertNotRegex(
            findings,
            re.compile(r"^- 当前禁止：", re.MULTILINE),
        )

    def test_status_sync_incident_records_current_defense_not_stale_action(
        self,
    ) -> None:
        incidents = INCIDENT_GUARDRAILS.read_text(encoding="utf-8")

        for stale_claim in (
            "仍是下一正式生产任务前必须修复的问题",
            "未自动检查业务语义同步",
            "执行现场立即同步产品判词",
            "当前最需要补强的是状态同步",
        ):
            self.assertNotIn(stale_claim, incidents)
        self.assertIn("product-verdict-source", incidents)
        self.assertIn("active test", incidents)
        self.assertIn("下一次真实业务状态变化", incidents)

    def test_audit_control_has_single_cold_start_and_report_order_owner(self) -> None:
        operating_model = AUDIT_OPERATING_MODEL.read_text(encoding="utf-8")
        charter = AUDITOR_CHARTER.read_text(encoding="utf-8")
        normalized_operating_model = re.sub(r"\s+", " ", operating_model)
        normalized_charter = re.sub(r"\s+", " ", charter)

        self.assertIn(
            "报告顺序只由本节拥有",
            normalized_operating_model,
        )
        self.assertIn(
            "冷启动读取顺序只由 `audit/AUDIT-OPERATING-MODEL.md`",
            normalized_charter,
        )
        self.assertIn(
            "正式报告顺序只由 `audit/AUDIT-OPERATING-MODEL.md`",
            normalized_charter,
        )
        self.assertNotIn("每次正式审计至少包含：", charter)
        self.assertIn(
            "长期入口的数量和名单只由"
            " `audit/ENGINEERING-AUDITOR-CHARTER.md`",
            normalized_operating_model,
        )
        entry_section = _markdown_section(
            charter,
            "## 十四、审计控制面的最小入口",
        )
        self.assertEqual(
            len(re.findall(r"^[1-9][0-9]*\. ", entry_section, re.MULTILINE)),
            4,
        )

    def test_taskcard_template_has_consistent_blocker_and_closeout_rules(self) -> None:
        template = TASKCARD_TEMPLATE.read_text(encoding="utf-8")

        permission_field = re.search(
            r"^> blocker_permission: `<([^`]+)>`$",
            template,
            re.MULTILINE,
        )
        self.assertIsNotNone(permission_field)
        self.assertEqual(
            permission_field.group(1),
            "none|taskcards/<任务编号>-BLOCKER.md",
        )
        closeout_field = re.search(
            r"^> closeout-result: `<([^`]+)>`$",
            template,
            re.MULTILINE,
        )
        self.assertIsNotNone(closeout_field)
        self.assertEqual(
            closeout_field.group(1),
            "IN_PROGRESS|PASS|BLOCKED",
        )
        self.assertIn(
            "只有 `blocker_permission` 填写本任务唯一 blocker 路径",
            template,
        )
        self.assertIn(
            "填写 `none` 时禁止列出或创建本任务的任何 blocker 文件",
            template,
        )
        self.assertIn("字段缺失、重复、使用", template)
        self.assertIn("编号不一致或与交付清单", template)

        self.assertIn("## 7. Closeout gate", template)
        self.assertIn(
            "`docs/current-task.md` 的 `product-verdict-source`",
            template,
        )
        self.assertIn("下一生产动作的授权状态", template)
        self.assertIn("closeout-result: PASS|BLOCKED", template)
        self.assertIn(
            "current task 都必须从开始就在交付清单预列 `docs/current-task.md` 与",
            template,
        )
        delivery_section = _markdown_section(template, "## 4. 交付文件清单")
        self.assertIn("- `docs/current-task.md`", delivery_section)
        self.assertIn("- `docs/dev-state.md`", delivery_section)

    def test_state_control_fields_and_verdict_paths_fail_closed(self) -> None:
        state = (
            "> current-task: `taskcards/T2.36.md`\n"
            "> current-run: `runs/T2.36-01`\n"
            "> product-verdict-source: `taskcards/T2.36.md`\n"
        )
        self.assertEqual(
            _control_value(state, "current-task"),
            "taskcards/T2.36.md",
        )
        self.assertIsNone(
            _control_value(
                state + "> current-task: `taskcards/T2.37.md`\n",
                "current-task",
            )
        )
        self.assertIsNone(
            _control_value(
                state + "> current-task: taskcards/T2.37.md\n",
                "current-task",
            )
        )
        self.assertTrue(
            _is_authorized_verdict_source(
                "taskcards/T2.36.md",
                "taskcards/T2.36.md",
                "runs/T2.36-01",
            )
        )
        self.assertTrue(
            _is_authorized_verdict_source(
                "runs/T2.36-01/acceptance/product-verdicts.md",
                "taskcards/T2.36.md",
                "runs/T2.36-01",
            )
        )
        for invalid_source in (
            "runs/T2.36-01/../../taskcards/T2.35.md",
            "runs/T2.36-010/product-verdicts.md",
            "/runs/T2.36-01/product-verdicts.md",
            "../taskcards/T2.36.md",
        ):
            self.assertFalse(
                _is_authorized_verdict_source(
                    invalid_source,
                    "taskcards/T2.36.md",
                    "runs/T2.36-01",
                )
            )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            taskcards_root = temp_root / "taskcards"
            run_root = temp_root / "runs/T2.36-01"
            taskcards_root.mkdir(parents=True)
            run_root.mkdir(parents=True)
            outside = temp_root / "taskcards/T2.35.md"
            outside.write_text("outside", encoding="utf-8")
            symlink_source = run_root / "product-verdicts.md"
            symlink_source.symlink_to(outside)
            self.assertFalse(
                _verdict_source_resolves_in_scope(
                    temp_root,
                    "runs/T2.36-01/product-verdicts.md",
                    "taskcards/T2.36.md",
                    "runs/T2.36-01",
                )
            )
            real_task = taskcards_root / "T2.36.md"
            real_task.write_text("task", encoding="utf-8")
            self.assertTrue(
                _is_canonical_state_target(
                    temp_root,
                    "taskcards/T2.36.md",
                    "taskcards",
                    "taskcard",
                )
            )
            self.assertTrue(
                _is_valid_next_production_authorization(
                    temp_root,
                    "taskcards/T2.36.md",
                )
            )
            self.assertTrue(
                _is_valid_next_production_authorization(
                    temp_root,
                    "none",
                )
            )
            linked_task = taskcards_root / "T2.37.md"
            linked_task.symlink_to(real_task)
            linked_run = temp_root / "runs/T2.37-01"
            linked_run.symlink_to(run_root, target_is_directory=True)
            for path, parent, kind in (
                ("taskcards/T2.37.md", "taskcards", "taskcard"),
                ("runs/T2.37-01", "runs", "run"),
                ("runs/.", "runs", "run"),
                ("runs/..", "runs", "run"),
                ("runs//T2.36-01", "runs", "run"),
            ):
                self.assertFalse(
                    _is_canonical_state_target(
                        temp_root,
                        path,
                        parent,
                        kind,
                    )
                )
            for authorization in (
                "taskcards/T2.37.md",
                "taskcards/..",
                "taskcards/T2..md",
                "../taskcards/T2.36.md",
            ):
                self.assertFalse(
                    _is_valid_next_production_authorization(
                        temp_root,
                        authorization,
                    )
                )

    def test_taskcard_governance_controls_fail_closed(self) -> None:
        def governed_taskcard(
            closeout_line: str,
            extra_delivery: str = "",
            verdict_section: str = "",
            include_memory_state: bool = True,
        ) -> str:
            deliveries = "- `taskcards/T2.36.md`"
            if include_memory_state:
                deliveries += (
                    "\n- `docs/current-task.md`"
                    "\n- `docs/dev-state.md`"
                )
            if extra_delivery:
                deliveries += f"\n{extra_delivery}"
            return (
                "# T2.36 example\n\n"
                "> blocker_permission: `none`\n"
                f"{closeout_line}\n\n"
                "## 1. 任务编号与标题\n\n"
                "`T2.36`：example。\n\n"
                "## 4. 交付文件清单\n\n"
                f"{deliveries}\n\n"
                "## 5. 硬约束\n\n"
                f"{verdict_section}"
            )

        for closeout in ("IN_PROGRESS", "PASS", "BLOCKED"):
            self.assertEqual(
                _taskcard_governance_errors(
                    governed_taskcard(
                        f"> closeout-result: `{closeout}`",
                    ),
                    "T2.36",
                ),
                [],
            )
        for invalid_card in (
            governed_taskcard(""),
            governed_taskcard("> closeout-result: `DONE`"),
            governed_taskcard(
                "> closeout-result: `PASS`\n"
                "> closeout-result: `BLOCKED`"
            ),
            governed_taskcard(
                "> closeout-result: `PASS`",
                "- `taskcards/T2.36.md`",
            ),
            governed_taskcard(
                "> closeout-result: `PASS`",
                include_memory_state=False,
            ),
        ):
            self.assertNotEqual(
                _taskcard_governance_errors(invalid_card, "T2.36"),
                [],
            )
        self.assertEqual(
            _taskcard_governance_errors(
                governed_taskcard(
                    "> closeout-result: `PASS`",
                    verdict_section="## 8. 产品判词\n\n产品负责人：PASS。\n",
                ),
                "T2.36",
            ),
            [],
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            taskcards_dir = temp_root / "taskcards"
            taskcards_dir.mkdir()
            next_task = taskcards_dir / "T2.36.md"
            next_task.write_text(
                governed_taskcard("> closeout-result: `IN_PROGRESS`"),
                encoding="utf-8",
            )
            self.assertEqual(
                _next_production_authorization_errors(
                    temp_root,
                    "taskcards/T2.36.md",
                    set(),
                    {"T2.36"},
                ),
                [],
            )
            for invalid_next in (
                governed_taskcard("> closeout-result: `PASS`"),
                governed_taskcard("> closeout-result: `BLOCKED`"),
                governed_taskcard(
                    "> closeout-result: `IN_PROGRESS`",
                    include_memory_state=False,
                ),
            ):
                next_task.write_text(invalid_next, encoding="utf-8")
                self.assertNotEqual(
                    _next_production_authorization_errors(
                        temp_root,
                        "taskcards/T2.36.md",
                        set(),
                        {"T2.36"},
                    ),
                    [],
                )
            permitted_blocker_card = governed_taskcard(
                "> closeout-result: `IN_PROGRESS`",
                "- `taskcards/T2.36-BLOCKER.md`",
            ).replace(
                "> blocker_permission: `none`",
                "> blocker_permission: `taskcards/T2.36-BLOCKER.md`",
            )
            next_task.write_text(permitted_blocker_card, encoding="utf-8")
            self.assertNotEqual(
                _next_production_authorization_errors(
                    temp_root,
                    "taskcards/T2.36.md",
                    {"taskcards/T2.36-BLOCKER.md"},
                    {"T2.36"},
                ),
                [],
            )
        self.assertNotEqual(
            _taskcard_governance_errors(
                governed_taskcard("> closeout-result: `PASS`"),
                "T2.36",
                {"taskcards/T2.36-BLOCKER.md"},
            ),
            [],
        )
        for noncanonical_blocker in (
            "other/T2.36-BLOCKER.md",
            "taskcards/T2.36-OTHER-BLOCKER.md",
            "taskcards/T2.36-x_y-BLOCKER.md",
        ):
            self.assertNotEqual(
                _taskcard_governance_errors(
                    governed_taskcard("> closeout-result: `PASS`"),
                    "T2.36",
                    {noncanonical_blocker},
                ),
                [],
            )
        self.assertEqual(
            _taskcard_governance_errors(
                governed_taskcard("> closeout-result: `PASS`"),
                "T2.36",
                {"taskcards/T2.36-v02-BLOCKER.md"},
                {"T2.36", "T2.36-v02"},
            ),
            [],
        )

    def test_blocker_permission_is_fail_closed_for_current_and_future_tasks(
        self,
    ) -> None:
        def taskcard(
            permission_line: str,
            delivery_line: str,
            task_id: str = "T2.36",
        ) -> str:
            return (
                f"# {task_id} example\n\n"
                f"{permission_line}\n\n"
                "## 1. 任务编号与标题\n\n"
                f"`{task_id}`：example。\n\n"
                "## 4. 交付文件清单\n\n"
                f"{delivery_line}\n\n"
                "## 5. 硬约束\n"
            )

        permitted_path = "taskcards/T2.36-BLOCKER.md"
        self.assertEqual(
            _blocker_permission_errors(
                taskcard(
                    f"> blocker_permission: `{permitted_path}`",
                    f"- `{permitted_path}`",
                ),
                "T2.36",
            ),
            [],
        )
        self.assertEqual(
            _blocker_permission_errors(
                taskcard("> blocker_permission: `none`", "- `output.md`"),
                "T2.36",
            ),
            [],
        )
        versioned_task_id = "T2.36-v02"
        versioned_path = f"taskcards/{versioned_task_id}-BLOCKER.md"
        self.assertEqual(
            _blocker_permission_errors(
                taskcard(
                    f"> blocker_permission: `{versioned_path}`",
                    f"- `{versioned_path}`",
                    versioned_task_id,
                ),
                versioned_task_id,
            ),
            [],
        )
        for invalid_card in (
            taskcard("", f"- `{permitted_path}`"),
            taskcard("> blocker_permission: `yes`", f"- `{permitted_path}`"),
            taskcard(
                "> blocker_permission: `none`\n"
                "> blocker_permission: yes",
                "- `output.md`",
            ),
            taskcard(
                "> blocker_permission: `taskcards/T2.37-BLOCKER.md`",
                "- `taskcards/T2.37-BLOCKER.md`",
            ),
            taskcard(
                "> blocker_permission: `none`\n"
                "> blocker_permission: `taskcards/T2.36-BLOCKER.md`",
                f"- `{permitted_path}`",
            ),
            taskcard(f"> blocker_permission: `{permitted_path}`", "- `output.md`"),
            taskcard("> blocker_permission: `none`", f"- `{permitted_path}`"),
            taskcard(
                f"> blocker_permission: `{permitted_path}`",
                f"- `{permitted_path}`\n- `{permitted_path}`",
            ),
            taskcard(
                f"> blocker_permission: `{permitted_path}`",
                "- `taskcards/T2.37-BLOCKER.md`",
            ),
            taskcard(
                f"> blocker_permission: `{permitted_path}`",
                f"- `{permitted_path}`",
            ).replace("`T2.36`：example。", "`T2.37`：example。"),
            taskcard(
                f"> blocker_permission: `{permitted_path}`",
                f"- `{permitted_path}`",
            ).replace("# T2.36 example", "# T2.37 example"),
            taskcard(
                "> blocker_permission: `none`",
                "- `other/T2.36-BLOCKER.md`",
            ),
            taskcard(
                "> blocker_permission: `none`",
                "- `output.md`\n\n"
                "## 4. 交付文件清单\n\n"
                f"- `{permitted_path}`",
            ),
            taskcard(
                "> blocker_permission: `none`",
                "- `output.md`",
            ).replace(
                "## 4. 交付文件清单",
                "## 1. 任务编号与标题\n\n"
                "`T2.37`：example。\n\n"
                "## 4. 交付文件清单",
            ),
        ):
            self.assertNotEqual(
                _blocker_permission_errors(invalid_card, "T2.36"),
                [],
            )

        state = CURRENT_STATE.read_text(encoding="utf-8")
        current_task = _control_value(state, "current-task")
        self.assertIsNotNone(current_task)
        current_task_path = ROOT / current_task
        current_task_text = current_task_path.read_text(encoding="utf-8")
        if current_task == "taskcards/T2.35.md":
            self.assertEqual(
                hashlib.sha256(current_task_path.read_bytes()).hexdigest(),
                "b29efb4386ccae4c4720d8a061d4a1bb808359f78f9dc4b4ec4cb35192753eda",
            )
        else:
            existing_blocker_paths = {
                path.relative_to(ROOT).as_posix()
                for path in ROOT.rglob("*-BLOCKER.md")
                if ".git" not in path.parts
            }
            known_task_ids = {
                path.stem
                for path in (ROOT / "taskcards").glob("*.md")
                if re.fullmatch(TASK_ID_PATTERN, path.stem)
                and not path.stem.endswith("-BLOCKER")
            }
            self.assertEqual(
                _taskcard_governance_errors(
                    current_task_text,
                    current_task_path.stem,
                    existing_blocker_paths,
                    known_task_ids,
                ),
                [],
            )

    def test_asset_register_counts_match_repository_projection(self) -> None:
        register = ASSET_REGISTER.read_text(encoding="utf-8")
        recorded = {
            key: int(value)
            for key, value in re.findall(
                r"^- ([a-z-]+): `([0-9]+)`$",
                register,
                re.MULTILINE,
            )
        }

        actual_taskcards = len(list((ROOT / "taskcards").glob("*.md")))
        actual_current_runs = len(
            [path for path in (ROOT / "runs").iterdir() if path.is_dir()]
        )
        actual_archived_runs = len(
            [path for path in (ROOT / "archive/runs").iterdir() if path.is_dir()]
        )
        actual_archived_run_files = len(
            [
                path
                for path in (ROOT / "archive/runs").rglob("*")
                if path.is_file()
            ]
        )
        actual_run_files = len(
            [
                path
                for base in (ROOT / "runs", ROOT / "archive/runs")
                for path in base.rglob("*")
                if path.is_file()
            ]
        )
        ignored = subprocess.run(
            [
                "git",
                "ls-files",
                "--others",
                "--ignored",
                "--exclude-standard",
                "--",
                "runs",
                "archive/runs",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        tracked = subprocess.run(
            ["git", "ls-files", "--", "runs", "archive/runs"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        untracked_visible = subprocess.run(
            [
                "git",
                "ls-files",
                "--others",
                "--exclude-standard",
                "--",
                "runs",
                "archive/runs",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()

        self.assertEqual(recorded.get("taskcard-count"), actual_taskcards)
        self.assertEqual(
            recorded.get("run-container-count"),
            actual_current_runs + actual_archived_runs,
        )
        self.assertEqual(
            recorded.get("current-run-container-count"),
            actual_current_runs,
        )
        self.assertEqual(
            recorded.get("archived-run-container-count"),
            actual_archived_runs,
        )
        self.assertEqual(recorded.get("run-file-count"), actual_run_files)
        self.assertEqual(
            recorded.get("archived-run-file-count"),
            actual_archived_run_files,
        )
        self.assertEqual(recorded.get("tracked-run-file-count"), len(tracked))
        self.assertEqual(recorded.get("ignored-run-file-count"), len(ignored))
        self.assertEqual(
            recorded.get("untracked-visible-run-file-count"),
            len(untracked_visible),
        )

        lifecycle_section = _markdown_section(
            FINDINGS_REGISTER.read_text(encoding="utf-8"),
            "### AUD-007 历史、当前、草案和本地载荷未清楚分层",
        )
        for duplicated_count in ("56", "42", "454", "265"):
            self.assertNotRegex(
                lifecycle_section,
                rf"\b{duplicated_count}\b",
            )

    def test_execution_roadmap_is_explicitly_non_authoritative_history(self) -> None:
        roadmap_header = "\n".join(
            EXECUTION_ROADMAP.read_text(encoding="utf-8").splitlines()[:12]
        )

        self.assertIn("> 生命周期：`historical-conditional`", roadmap_header)
        self.assertIn("> 当前执行授权：`none`", roadmap_header)
        self.assertIn("docs/current-task.md", roadmap_header)


if __name__ == "__main__":
    unittest.main()
