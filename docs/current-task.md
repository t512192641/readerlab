# Current Task

## Authority

本文件是当前执行事实的唯一入口。若 `docs/dev-state.md`、`docs/progress.md`、`docs/next-session-prompt.md`、旧报告、旧 handoff 或 PR 描述与本文件冲突，以本文件为准。

启动时只读：

1. `AGENTS.md`
2. `docs/current-task.md`

其他文件只能按本文件的动作触发读取。

## Active Slice

ReaderLab 已完成 **Skill 交付设计后的最小验证实现切片**。

当前目标仍不是泛化宣称，也不是 public external validation。最小 trace validator 和 comment replay fixture 已实现；用户选择暂时跳过真实 Obsidian UI replay，稍后配合补测。

```text
已完成：
1. 最小 trace validator
2. 最小 comment replay fixture

后补：
3. 真实 Obsidian UI / plugin replay
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
- `trace_validator_implemented`: `minimal_pass`
- `comment_replay_fixture_pass`: `1/1`
- `comment_replay_verified`: `fixture_pass_real_obsidian_ui_deferred`
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
- minimal trace validator：
  - `scripts/readerlab_trace_validator.py`
  - `tests/test_readerlab_trace_validator.py`
- comment replay fixture package：
  - `docs/reports/readerlab-comment-replay-v0/`
  - plugin storage format: `tandem-comments`
  - replay cases checked: A2 longform 2 comments + B2 engineering cleaned-body 2 comments

GitHub state:

- Repository `t512192641/readerlab` verified private by GitHub app.
- Branch: `readerlab-elon-checkpoint`
- PR: `https://github.com/t512192641/readerlab/pull/1`
- Latest pushed commit: `a0706bd Add ReaderLab trace validator checkpoint`

## Next Action

用户已决定先跳过真实 Obsidian UI replay，稍后配合补测。下一步允许做：

1. 提交并推送最小 validator / fixture checkpoint。
2. 准备正式 ReaderLab Skill 草案的实现合同，但在用户明确批准前不创建正式 `SKILL.md`。
3. 稍后用户可配合补真实 Obsidian UI replay：从插件真实创建批注，再验证 Codex 能回到 body anchor、claim、candidate 和 gate decision。

最小 trace validator 已检查：

- `location-map.json` 中的 anchors 可被引用。
- `annotation-trigger.json` 的每个 `anchor_ref` 存在。
- replay case 能追溯到 body/source anchor、claim、candidate 或 gate decision。
- skill candidates 满足 trigger / input / steps / output / boundary / evidence。

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
- 把 fixture comment replay 说成真实 Obsidian UI replay。
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
