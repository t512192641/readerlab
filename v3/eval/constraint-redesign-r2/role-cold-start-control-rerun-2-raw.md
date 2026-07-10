# 主控合同剩余三项第二次复核原始输出

## 复核边界

- 时间：`2026-07-10T07:12:40-04:00`。
- 本次只复核：mixed 父 manifest 的 `unassigned`、dispatch 到 stages 的精确映射、`planned / awaiting-user / running` 恢复路径。
- 本次读取：仅 `v3/skill/roles/orchestrator.md` 与 `v3/skill/templates/run-manifest.md` 中上述三项相关字段和规则。
- 本次未复核：此前已通过的唯一 manifest、dispatch 实例、gate 枚举、Skill 双门、claims、角色计数及其他协议 / 回归内容。
- 上下文声明：本执行者做过前两次主控 raw 审查；本次不是零上下文，但每项 verdict 均重新以当前两份文件为证据。
- 保留规则：`role-cold-start-control-raw.md` 与 `role-cold-start-control-rerun-raw.md` 保留不改；本次不修改规则文件。

## 总结论

- overall verdict：`fail`。
- 三项结果：`2 pass / 1 fail`。
- 已闭合：mixed 父 manifest 可保持 `unassigned`；dispatch 到四个 stage key 的映射已在主控与 manifest 中完全一致。
- 未闭合：awaiting-user 的正向路径只部分补齐。开跑前 pending 已能进入 awaiting-user，运行后用户体验也能返回 running；但 `sample.user_confirmation` 没有“已确认 / 拒绝”值，声明接受 pending 没有明确返回路径，用户拒绝也没有合法终止转换。
- 可声称范围：可以声称前两项修复通过；不能声称状态机或主控 schema 整体通过。

## 1. Mixed 父 manifest `unassigned`

- verdict：`pass`。
- 当前 schema：manifest `route.line` 已改为 `unassigned | book | skill`；orchestrator `run_ref.line` 使用同一枚举。
- 当前规则：`material_type: mixed` 的父 manifest 保持 `unassigned`，必须拆成独立 child run manifests，或在拆分前标 `blocked`；只有 `book | skill` child run 可进入执行。
- 对上次缺口的结论：已修复。父 manifest 不再被迫提前选择 book 或 skill，blocked 与 split 都有可表达状态，执行只发生在已选线 child run。
- 剩余风险：真实 child_run_ids 与 child manifests 是否一致需真实 run 证据验证，不影响本次静态 schema verdict。
- 可声称范围：可声称“mixed 父 manifest 的未选线状态已闭合”；不可声称真实 mixed run 已成功拆分或执行。

## 2. Dispatch 到 stages 精确映射

- verdict：`pass`。
- manifest 映射：
  - `done -> stages.executed`
  - `skipped -> stages.skipped`
  - `failed -> stages.failed`
  - `reused -> stages.reused_without_rerun`
- orchestrator 映射：与上述四项逐字一致，不再使用“同名 stages”概括。
- 预算规则：manifest 以实际计费的非复用、非跳过 dispatch 计算 `budget.actual_tasks`；orchestrator 只统计 `counted_task: true` 且实际执行的 dispatch。两者在 skipped / reused 不计和实际执行计费的核心语义上一致。
- 对上次缺口的结论：已修复。不存在 `stages.done` 或 `stages.reused` 的错误写法。
- 可声称范围：可声称“合同中的 dispatch→stages 映射已闭合”；不可声称真实 manifest 已无漏记、重复或计数错误。

## 3. `planned / awaiting-user / running` 恢复路径

- verdict：`fail`。
- 已修复路径：
  - `planned -> awaiting-user`：前置用户确认 pending 时可进入，且不得生成执行 dispatch。
  - `awaiting-user -> planned`：前置确认返回后回计划态复核。
  - `running -> awaiting-user`：用户体验或声明接受 pending 时进入。
  - 规则文字允许运行后的用户体验确认返回后回 `running`，再结算门与声明。
- 剩余 schema 缺口一：`sample.user_confirmation` 的枚举仍是 `required | not-required | pending`。它混合“是否需要确认”与“确认结果”，没有 `confirmed / declined` 或同义状态。前置确认返回后，manifest 没有值可以证明用户同意还是拒绝，也无法确定何时满足 `planned -> running` 的“不得有 pending”。
- 剩余转换缺口二：`running -> awaiting-user` 同时覆盖“用户体验 pending”和“声明接受 pending”，但返回规则只明确“运行后的用户体验门”可回 `running`。声明接受返回后走向 `running / accepted / failed` 的路径未定义。
- 剩余转换缺口三：没有用户拒绝路径。前置样本被拒、用户体验判定为 fail、或用户拒绝声明接受时，状态机没有 `awaiting-user -> failed`、`awaiting-user -> cancelled` 或其他合法终态；现有唯一 `running -> failed` 也不能处理尚未开跑的前置拒绝。
- 影响：正向同意路径的一部分可以执行，但同一状态字段无法保存确认结果，声明接受和拒绝分支仍会停在 awaiting-user 或被主控自由解释。因此状态机仍未闭合。
- 最小剩余修复：
  1. 将“是否要求确认”与“确认结果”拆开，或为 `user_confirmation` 增加明确的 `confirmed / declined` 状态。
  2. 明确 `awaiting-user -> running` 同时覆盖运行后的用户体验与声明接受返回。
  3. 为前置拒绝、体验失败和声明拒绝定义明确终态与转换；若采用 `failed` 或新增 `cancelled`，需同步顶层 status 枚举。

## 最终判定

| 剩余项 | verdict | 结论 |
| --- | --- | --- |
| mixed 父 manifest `unassigned` | `pass` | 父 run 可不选线，child run 才执行。 |
| dispatch→stages 精确映射 | `pass` | 四项 key 已逐字一致。 |
| planned / awaiting-user / running 恢复路径 | `fail` | 正向路径部分补齐，但确认结果、声明接受返回和拒绝终态仍缺。 |

最终 overall verdict：`fail`。前两份 raw 应继续保留；本轮只能确认前两项关闭，不能据此升级为主控合同整体通过。
