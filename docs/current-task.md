# Current Task

## Authority

本文件是当前执行事实的唯一入口。若 `docs/dev-state.md`、`docs/progress.md`、`docs/next-session-prompt.md`、旧报告、旧 handoff 或 PR 描述与本文件冲突，以本文件为准。

启动时只读：

1. `AGENTS.md`
2. `docs/current-task.md`

其他文件只能按本文件的动作触发读取。

## Active Slice

ReaderLab 已从 demo 验证进入 **Skill 交付设计后的验证实现切片**。

当前目标不是写正式 `SKILL.md`，而是补齐正式 Skill 草案前的两个硬缺口：

```text
1. 最小 trace validator
2. 最小 comment replay fixture
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
- `trace_validator_implemented`: `not_started`
- `comment_replay_verified`: `not_verified`
- `transferable_method_kernel_pass`: `not_verified`
- `skill_draft_not_started`
- `public_external_material_validation_not_started`

禁止使用的旧口径：

- 不得把 15 章高阶讲解通过称为 `reader_package_pass`。
- 不得把 two-demo 或 private validation 称为 `transferable_method_kernel_pass`。
- 不得把 Skill 交付设计文档称为正式可运行 Skill 草案。
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

GitHub state:

- Repository `t512192641/readerlab` verified private by GitHub app.
- Branch: `readerlab-elon-checkpoint`
- PR: `https://github.com/t512192641/readerlab/pull/1`
- Latest pushed commit for delivery design: `577ffb4 Add ReaderLab skill delivery design`

## Next Action

下一步只允许做：

1. 设计并实现最小 trace validator。
2. 用现有 demo/private validation artifacts 做最小 comment replay fixture。
3. 运行验证并更新状态。

最小 trace validator 应检查：

- `location-map.json` 中的 anchors 可被引用。
- `annotation-trigger.json` 的每个 `anchor_ref` 存在。
- reader-facing 核心段落能追溯到 body/source anchor、claim、candidate 或 gate decision。
- promoted candidates 有最终用途或 audit-only 理由。
- skill candidates 满足 trigger / input / steps / output / boundary / evidence。

最小 comment replay fixture 应覆盖：

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

- 创建正式 `SKILL.md`。
- 标记 `formal_skill_draft_started`。
- 标记 `transferable_method_kernel_pass`。
- 把 private/local validation 写成 public external validation。
- reader-facing 暴露 `source refs`、`claim trace`、`lens score`、`machine_status`、`human_status`、`Body Track Gate`、`Claim Ledger`、`Candidate Tournament`、`Skillization Gate`、`Annotation Trigger`。
- trace validator 不能连接 reader paragraph、anchor、claim、candidate/gate。
- comment replay 不能从 comment 回到 body anchor、claim、candidate 和 gate decision。

## Verification Commands

```bash
python3 tests/test_readerlab.py
git diff --check
```

新增 validator 或 replay fixture 后还应运行对应新增测试或命令，并把结果写入 `docs/agent-run-ledger.md`。
