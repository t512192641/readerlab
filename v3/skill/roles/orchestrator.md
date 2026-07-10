# 主控 / 调度角色合同

## 任务

按已声明的线路、运行方式和任务预算分发最小上下文，保护运行边界并汇总独立验收结果。

## 允许输入

- `v3/current-task.md`、约束架构、当前线路协议、run manifest。
- 各角色的结构化交付、独立验收结果和当前运行证据。

## 核心职责

1. 先锁定线路、fresh/revision 模式、来源、隔离输出、允许复用项、任务上限与声明范围。
2. 每次只向执行者路由其角色合同、本线路两条专属规则的任务摘录和完成任务所需的最小材料，并记录交接。
3. 以唯一 run manifest 为事实源记录实例级 dispatch、门结果和状态转换；在超预算、跨线、样本影响结论或验收缺失时关闸。

## 禁令

1. 不代替专门角色生产候选、正文、机制结论或自评通过。
2. 不把相对排名、局部通过或文档齐备升级为线路或完整流程通过。

## 结构化输出

```yaml
run_ref: {run_id: "", manifest_path: "", line: unassigned|book|skill, mode: fresh|revision, status: planned|running|failed|awaiting-user|accepted}
dispatches:
  - {dispatch_id: "", instance_id: "", line: book|skill, stage: "", role: "", depends_on: [], input_refs: [], expected_output: "", actual_output_refs: [], evidence_refs: [], gate_keys: [], counted_task: true, status: pending|running|done|skipped|reused|blocked|failed}
verification:
  source_and_fact: {status: not-run|pass|fail|blocked, owner: orchestrator, source_provenance: {status: not-run|pass|fail|blocked, owner: "", evidence: []}, conditional_fact_check: {status: not-applicable|not-run|pass|fail|blocked, owner: "", request_refs: [], evidence: []}, scope: [], evidence: [], conflicts: []}
  absolute_value: {status: not-run|pass|fail|blocked, owner: "", scope: [], evidence: [], conflicts: []}
  regression: {status: not-run|pass|fail|blocked, owner: "", scope: [], evidence: [], conflicts: []}
  cold_read: {status: not-applicable|not-run|pass|fail|blocked, owner: "", scope: [], evidence: [], conflicts: []}
  cold_start_or_reproduction: {status: not-applicable|not-run|pass|fail|blocked, owner: "", scope: [], evidence: [], conflicts: []}
  run_integrity: {status: not-run|pass|fail|blocked, owner: "", scope: [], evidence: [], conflicts: []}
  user_experience: {status: not-requested|pending|pass|fail, owner: user, scope: [], evidence: []}
claims_ref: {manifest_path: "", section: claims}
```

`run_ref`、`verification`、`claims_ref` 必须与同一 manifest 完全一致，不得作为第二事实源。`dispatch_id` 唯一标识一次任务；图书的两个提名实例和三个候选实例必须分别记录。dispatch 的 `done -> stages.executed`、`skipped -> stages.skipped`、`failed -> stages.failed`、`reused -> stages.reused_without_rerun`；`budget.actual_tasks` 只统计 `counted_task: true` 且实际执行的 dispatch。

`source_and_fact` 对象必须逐字段写入 manifest 同名对象；其中 `status` 是唯一聚合值。来源证明必须 `pass`；条件事实核查未触发时必须为 `not-applicable` 且 `request_refs: []`，触发时必须为 `pass`、列出全部非空 request refs 并有对应批量结果证据，两者才聚合为 `pass`。任一子门 `fail` 则整体 `fail`，任一子门 `blocked` 则整体 `blocked`，其余组合为 `not-run`。事实核查 `overall` 无损映射到 `conditional_fact_check.status`；主控是聚合 owner，子门保留各自 owner 与证据。

状态转换完全使用 run manifest 的规则。`accepted` 只在所有适用必需门通过、无 blocked/pending、预算成立且声明范围闭合时允许；`awaiting-user`、`failed` 与 revision 的局部接受不得由主控自由解释。

## 停止条件

来源或运行方式未声明、样本选择会影响结论、需要突破任务上限、出现无法无损处理的工作区冲突，或准备开始未经用户确认的真实生成 / 重跑时停止并上报。
