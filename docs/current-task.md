# Current Task

## Authority

本文件是当前执行事实的唯一入口。若 `docs/dev-state.md`、`docs/progress.md`、`docs/next-session-prompt.md`、旧报告、旧 handoff 或 PR 描述与本文件冲突，以本文件为准。

启动时只读：

1. `AGENTS.md`
2. `docs/current-task.md`

其他文件只能按本文件的动作触发读取。

## Active Slice

ReaderLab 已完成 **repo-local Skill trial pre-release trace hardening 切片**。

当前目标仍不是泛化宣称，也不是 public external validation。正式 ReaderLab Skill 草案已在 `docs/drafts/readerlab-skill-v0/` 创建；用户已于 2026-07-01 明确批准 repo-local activation、烟测、烟测后使用 Meta Skills 验收，以及封版前补丁。当前允许的激活范围仅限 `.agents/skills/readerlab/`，不得全局安装到 `/Users/tianqiang/.codex/skills/`，不得宣称生产可用或 transferable method pass。

```text
已完成：
1. 最小 trace validator
2. 最小 comment replay fixture
3. 正式 Skill 草案实现合同
4. 正式 Skill draft 最小实现计划
5. 用户批准开发 docs/drafts 内的正式草案 `SKILL.md`
6. docs draft `SKILL.md`
7. product-spec forward test + route tie-breaker patch
8. 真实 Obsidian UI replay：插件存储通过，正文段落直接选择未验证
9. repo-local activation：`.agents/skills/readerlab/`
10. repo-local smoke test：pass
11. Meta Skills acceptance：`repo_local_trial_ready`
12. active Skill 边界文案修正：repo-local trial only
13. trace-validation.json 最小样本：A/B private demos 已补
14. trace validator reader-facing paragraph trace 检查：implemented

后补：
15. 严格正文段落直接选择 replay
16. 一次真实小材料 ReaderLab package 使用测试
```

## Current Status

必须使用以下状态口径：

- `chapter_high_order_explanation_pass`: `15/15`
- `full_book_reader_synthesis_pass`: `1/1`
- `baseline_capability_audit_pass`: `1/1`
- `reader_package_not_verified`
- `transferable_method_kernel_probe_pass`: `2/2`
- `two_demo_internal_pass`: `2/2`
- `two_demo_review_hardening_patch`: `done`
- `private_material_validation_local_pass`: `2/2`
- `formal_skill_delivery_design_ready`: `yes`
- `skill_delivery_design_docs`: `created`
- `formal_skill_draft_contract_ready`: `yes`
- `formal_skill_draft_contract_review`: `pass_no_p0_p1`
- `formal_skill_draft_implementation_plan_ready`: `yes`
- `formal_skill_draft_human_approval`: `docs_draft_skill_md_allowed`
- `formal_skill_draft_allowed_path`: `docs/drafts/readerlab-skill-v0/SKILL.md`
- `formal_skill_draft_started`: `docs_draft_only`
- `formal_skill_draft_path`: `docs/drafts/readerlab-skill-v0/SKILL.md`
- `readerlab_skill_repo_local_activation`: `approved`
- `readerlab_skill_repo_local_trial`: `active`
- `readerlab_skill_repo_local_path`: `.agents/skills/readerlab/`
- `readerlab_skill_repo_local_smoke_test`: `pass`
- `readerlab_skill_meta_acceptance`: `repo_local_trial_ready`
- `readerlab_skill_pre_release_trace_hardening`: `done`
- `trace_validation_json_private_demos`: `2/2`
- `trace_validator_implemented`: `minimal_pass`
- `trace_validator_reader_paragraph_trace`: `implemented`
- `comment_replay_fixture_pass`: `1/1`
- `comment_replay_verified`: `fixture_pass_real_obsidian_ui_pass_with_warning`
- `real_obsidian_ui_replay`: `pass_with_warning`
- `real_obsidian_ui_storage_format`: `tandem-comments`
- `real_obsidian_ui_body_prose_selection`: `not_verified`
- `transferable_method_kernel_pass`: `not_verified`
- `global_skill_install_not_started`
- `public_external_material_validation_not_started`

禁止使用的旧口径：

- 不得把 15 章高阶讲解通过称为 `reader_package_pass`。
- 不得把 two-demo 或 private validation 称为 `transferable_method_kernel_pass`。
- 不得把 Skill 交付设计文档称为正式可运行 Skill 草案。
- 不得把正式 Skill 草案实现合同称为正式可运行 Skill 草案。
- 不得把 `formal_skill_draft_contract_ready` 称为 `formal_skill_draft_started`。
- 不得把 `formal_skill_draft_implementation_plan_ready` 称为 `formal_skill_draft_started`。
- 不得把 repo-local trial 称为全局安装、生产可用或可复用发布版 Skill。
- 不得把 private/local validation 称为 public external validation。

## Current Evidence

已完成并纳入 private checkpoint：

- two-demo internal run：`docs/reports/readerlab-two-demo-run-v0/`
- two-demo review hardening patch：location map、source-cleaning map、trace-to-reader
- private material validation：`docs/reports/readerlab-private-material-validation-v0/`
- Skill delivery design docs：
  - `docs/readerlab-skill-delivery-spec.md`
  - `docs/readerlab-skill-ir-v1.md`
  - `docs/contracts/location-anchor-v1.md`
  - `docs/contracts/trace-validation-v1.md`
  - `docs/contracts/comment-replay-v1.md`
- Formal Skill draft contract：
  - `docs/readerlab-formal-skill-draft-contract.md`
  - independent reviewer result: pass, no P0/P1, P2 addressed
- Formal Skill draft implementation plan：
  - `docs/readerlab-formal-skill-draft-implementation-plan.md`
  - approved scope: create one formal draft `SKILL.md` under `docs/drafts/readerlab-skill-v0/`; no install / no activation
- Formal Skill draft packet：
  - `docs/drafts/readerlab-skill-v0/SKILL.md`
  - `docs/drafts/readerlab-skill-v0/README.md`
  - `docs/drafts/readerlab-skill-v0/examples/input-request.json`
  - `docs/drafts/readerlab-skill-v0/examples/route-decision-example.json`
  - `docs/drafts/readerlab-skill-v0/evals/trigger-cases.json`
  - `docs/drafts/readerlab-skill-v0/evals/output-cases.json`
  - `docs/drafts/readerlab-skill-v0/reports/skill-ir.md`
  - `docs/drafts/readerlab-skill-v0/reports/output-quality-scorecard.md`
  - `docs/drafts/readerlab-skill-v0/reports/review-studio.md`
  - `docs/drafts/readerlab-skill-v0/reports/activation-hardening.md`
  - `docs/drafts/readerlab-skill-v0/checks/activation-checklist.md`
  - `docs/drafts/readerlab-skill-v0/forward-tests/product-spec-v0/`
  - `docs/drafts/readerlab-skill-v0/checks/readiness-checklist.md`
- Repo-local Skill trial：
  - `.agents/skills/readerlab/SKILL.md`
  - `.agents/skills/readerlab/checks/`
  - `.agents/skills/readerlab/evals/`
  - `.agents/skills/readerlab/examples/`
  - `.agents/skills/readerlab/reports/`
- Repo-local smoke and Meta Skills acceptance：
  - `docs/drafts/readerlab-skill-v0/reports/repo-local-smoke-test.md`
  - `docs/drafts/readerlab-skill-v0/reports/meta-skill-acceptance.md`
- Pre-release trace hardening：
  - `docs/drafts/readerlab-skill-v0/reports/pre-release-trace-hardening.md`
  - `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/trace-validation.json`
  - `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/trace-validation.json`
  - `scripts/readerlab_trace_validator.py`
  - `tests/test_readerlab_trace_validator.py`
- minimal trace validator：
  - `scripts/readerlab_trace_validator.py`
  - `tests/test_readerlab_trace_validator.py`
- comment replay fixture package：
  - `docs/reports/readerlab-comment-replay-v0/`
  - plugin storage format: `tandem-comments`
  - replay cases checked: A2 longform 2 comments + B2 engineering cleaned-body 2 comments
- real Obsidian UI replay package：
  - `docs/reports/readerlab-real-obsidian-replay-v0/`
  - `docs/reports/readerlab-real-obsidian-replay-v0/results/comment-replay-real-ui.json`
  - result: `pass_with_warning`
  - warning: comments attached to visible anchor list entries, not direct prose body selections

GitHub state:

- Repository `t512192641/readerlab` verified private by GitHub app.
- Branch: `readerlab-elon-checkpoint`
- PR: `https://github.com/t512192641/readerlab/pull/1`
- Latest pushed commit before this slice: `d535eb3 Activate ReaderLab repo-local skill trial`

## Next Action

用户已批准并完成 repo-local activation、烟测、Meta Skills 验收和封版前 trace hardening。下一步允许做：

1. 用 `.agents/skills/readerlab/` 做一次真实小材料 ReaderLab package 使用测试。
2. 记录 Skill 在真实任务中是否减少路线误判、正文/audit 泄漏和批注入口歧义。
3. 之后再与用户补一次严格正文段落直接选择 replay；当前真实插件存储已经通过但仍是 `pass_with_warning`。

最小 trace validator 已检查：

- `location-map.json` 中的 anchors 可被引用。
- `annotation-trigger.json` 的每个 `anchor_ref` 存在。
- replay case 能追溯到 body/source anchor、claim、candidate 或 gate decision。
- skill candidates 满足 trigger / input / steps / output / boundary / evidence。
- `trace-validation.json` 中 reader-facing core paragraphs 能追溯到 anchor、claim、candidate 或 gate。

最小 comment replay fixture 已覆盖：

- A2 private longform 正文位置 2 条 comment。
- B2 Skill / engineering 净化正文位置 2 条 comment。
- 每条 replay 必须能回到 anchor、nearby body、claim、candidate、gate decision 和 bounded AI reply。

## Allowed Reads

实现 trace validator 时可读：

- `docs/contracts/location-anchor-v1.md`
- `docs/contracts/trace-validation-v1.md`
- `docs/readerlab-skill-ir-v1.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/**/audit/location-map.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/**/audit/contracts/*.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/**/audit/location-map.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/**/audit/contracts/*.json`
- `scripts/readerlab.py`
- `tests/test_readerlab.py`

实现 comment replay fixture 时可读：

- `docs/contracts/comment-replay-v1.md`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/10_一手正文/001_正文.md`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/10_一手正文/001_净化正文.md`
- 对应 demo 的 `location-map.json`、`claim-ledger.json`、`candidate-tournament.json`、`annotation-trigger.json`

实现正式 Skill 草案前合同或后续实现计划时可读：

- `docs/readerlab-formal-skill-draft-contract.md`
- `docs/readerlab-skill-delivery-spec.md`
- `docs/readerlab-skill-ir-v1.md`
- `docs/contracts/location-anchor-v1.md`
- `docs/contracts/trace-validation-v1.md`
- `docs/contracts/comment-replay-v1.md`
- `scripts/readerlab_trace_validator.py`
- `tests/test_readerlab_trace_validator.py`
- `docs/readerlab-formal-skill-draft-implementation-plan.md`

按需读取：

- 产品边界：`docs/product-spec.md`
- 包结构：`docs/readerlab-package-spec.md`
- 稳定路径和工具状态：`docs/dev-state.md`
- 耐久决策：`docs/decisions.md`，优先 D-052 之后
- 验收 gate：`docs/eval-gates.md`

不要读取：

- 旧 fullbook、旧 bakeoff、旧 GPT Pro prompt、旧长报告、原始聊天。
- 除非当前动作明确需要，不要展开 `docs/reports/**` 的历史目录。

## Stop Conditions

立即停止并纠正状态，如果出现：

- 在 `.agents/skills/readerlab/` 和 `docs/drafts/readerlab-skill-v0/` 之外创建 ReaderLab `SKILL.md`。
- 全局安装或启用 ReaderLab Skill 到 `/Users/tianqiang/.codex/skills/`。
- 把 docs draft `SKILL.md` 说成已安装、已启用或生产可复用 Skill。
- 把 repo-local trial 说成生产可用、全局安装、public validation pass 或 transferable method pass。
- 标记 `transferable_method_kernel_pass`。
- 把 fixture comment replay 说成真实 Obsidian UI replay。
- 把 `real_obsidian_ui_replay: pass_with_warning` 说成 full pass 或 production ready。
- 把 private/local validation 写成 public external validation。
- reader-facing 暴露 `source refs`、`claim trace`、`lens score`、`machine_status`、`human_status`、`Body Track Gate`、`Claim Ledger`、`Candidate Tournament`、`Skillization Gate`、`Annotation Trigger`。
- trace validator 不能连接 reader paragraph、anchor、claim、candidate/gate。
- comment replay 不能从 comment 回到 body anchor、claim、candidate 和 gate decision。

## Verification Commands

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
python3 scripts/readerlab_trace_validator.py validate-demo <output_root>
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
git diff --check
```

新增 validator、replay fixture、formal draft contract 或 docs draft `SKILL.md` 后还应运行对应新增测试或命令，并把结果写入 `docs/agent-run-ledger.md`。
