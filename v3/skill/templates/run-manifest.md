# ReaderLab V3 Run Manifest

复制到本次 run 的 audit 目录，在读取任何生成产物前填写。运行中只更新实际证据，不回填或覆盖旧 run。

```yaml
run_id: required-unique-id
started_at: required-iso-time
status: planned | running | failed | awaiting-user | accepted
mode: fresh | revision

route:
  line: unassigned | book | skill
  mixed_handling: not-applicable | split-into-child-runs | blocked
  child_run_ids: []

source:
  material_type: book | longform | skill | engineering | mixed
  original_paths: []
  fingerprints:
    - path: required
      size: required
      modified_at: required
      sha256: optional
  actual_read_scope: []

sample:
  basis: fixed-by-authority | user-selected | proposed
  authority_or_reason: required
  affects_capability_claim: true | false
  confirmation_required: true | false
  user_confirmation: not-required | pending | confirmed | declined

reuse:
  stable_standards_and_gold: []
  base_generated_artifact: none
  reused_generated_artifacts: none

output:
  new_isolated_directory: required
  preexisting: false
  writes_to_previous_run: false

budget:
  task_limit: required
  actual_tasks: 0
  expansion_trigger: none
  user_approved_overrun: false

stages:
  executed: []
  skipped: []
  failed: []
  reused_without_rerun: []

verification:
  source_and_fact:
    status: not-run | pass | fail | blocked
    owner: orchestrator
    source_provenance: {status: not-run | pass | fail | blocked, owner: required, evidence: []}
    conditional_fact_check: {status: not-applicable | not-run | pass | fail | blocked, owner: required-if-run, request_refs: [], evidence: []}
    scope: []
    evidence: []
    conflicts: []
  absolute_value: {status: not-run | pass | fail | blocked, owner: required, scope: [], evidence: [], conflicts: []}
  regression: {status: not-run | pass | fail | blocked, owner: required, scope: [], evidence: [], conflicts: []}
  cold_read: {status: not-applicable | not-run | pass | fail | blocked, owner: required, scope: [], evidence: [], conflicts: []}
  cold_start_or_reproduction: {status: not-applicable | not-run | pass | fail | blocked, owner: required, scope: [], evidence: [], conflicts: []}
  run_integrity: {status: not-run | pass | fail | blocked, owner: required, scope: [], evidence: [], conflicts: []}
  user_experience: {status: not-requested | pending | pass | fail, owner: user, scope: [], evidence: []}

claims:
  can_claim: []
  cannot_claim: []
  reused_results_only: []
  awaiting_user_acceptance: []
```

`route.line` 是本次 manifest 唯一执行线路。`material_type: longform` 路由到 `book`，`engineering` 路由到 `skill`；`mixed` 父 manifest 保持 `unassigned`，必须拆成独立 child run manifests，或在拆分前标 `blocked`，不得静默选线。只有 `book | skill` child run 可进入执行。

样本确认组合固定为：`confirmation_required: false` 时 `user_confirmation` 只能是 `not-required`；`confirmation_required: true` 时只能是 `pending | confirmed | declined`。其他组合无效，run 保持 `planned` 并标 schema fail。

`stages` 中只记录 orchestrator dispatch id：`done` 且实际执行进入 `executed`，明确不执行进入 `skipped`，失败进入 `failed`，合法复用进入 `reused_without_rerun`。`budget.actual_tasks` 等于实际计费的非复用、非跳过 dispatch 数；主控不另建第二套任务数字。

`verification.source_and_fact.status` 是来源证明与条件事实核查的聚合值：来源证明必须通过；未触发外部事实核查时，条件子门必须为 `not-applicable` 且 `request_refs: []`；触发时必须列出全部非空 request refs、全部 request claims 精确覆盖且 fact-checker `overall: pass`。任一子门失败或阻塞时，聚合门不得为 `pass`；两个子门及证据直接保存在同一 manifest 中，不另建影子记录。

## 模式校验

### Fresh

- `base_generated_artifact: none`、`reused_generated_artifacts: none`、`reused_without_rerun: []`。
- 从登记的原始来源开始，正文/source map、识别、候选、核查、裁判、装配和声明范围内的验收全部新做。
- `new_isolated_directory` 必须是本次唯一的新目录；旧 URL 只作线索，外部事实本次重新定位核实。

任一项不成立，本次不得标记 fresh，也不得声称从零跑通。

### Revision

- `base_generated_artifact` 填写明确基线；`reused_generated_artifacts` 与 `reused_without_rerun` 逐项列出。
- `executed` 只写实际重跑阶段；`cannot_claim` 明确未重跑链段与完整流程。

## 结束检查

- 失败产物保留在本次隔离目录并标状态，不污染上一轮。
- 样本影响结论时，`user_confirmation` 未通过则不得开跑。
- `can_claim` 只能覆盖“实际执行 + 对应独立门通过”的交集。
- 机器检查、局部页、资产卡冷启动或 revision 不得写成整条 ReaderLab 流水线通过。

## 状态转换

- `planned -> running`：来源、route、模式、隔离输出和预算均已填写，且样本确认为 `false + not-required` 或 `true + confirmed`；`pending/declined` 和无效组合均不得进入 running。
- `planned -> awaiting-user`：必需的样本确认仍为 `pending`；此时不得产生执行 dispatch。
- `planned -> failed`：必需的样本确认已为 `declined`，或确认字段组合无效且无法在本 run 内修复。
- `awaiting-user -> planned`：样本确认变为 `confirmed`，回到计划态重新核对。样本确认 `declined` 则进入 `failed`，不得 dispatch。
- `running -> awaiting-user`：没有必需门失败，但 `verification.user_experience.status` 为 `pending`，或 `claims.awaiting_user_acceptance` 非空。
- `awaiting-user -> running`：`verification.user_experience.status` 返回 `pass`，或待确认声明已分别移入 `can_claim/cannot_claim`；随后重新结算门和状态。用户体验返回 `fail` 则进入 `failed`。
- `running -> failed`：任一必需门为 `fail`，或 `blocked` 无法在本 run 内恢复；失败原因进入对应 gate 与 stages。
- `running -> accepted`：所有适用的必需门均 `pass`，不适用门明确为 `not-applicable`，无 `blocked/pending`，任务数未超预算，且 `can_claim` 只覆盖实际执行与验收交集。
- revision 的 `accepted` 只表示声明的局部修订被接受；`cannot_claim` 必须继续排除未重跑链段和完整流程。
