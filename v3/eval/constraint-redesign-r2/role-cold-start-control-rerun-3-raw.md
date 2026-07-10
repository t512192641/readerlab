# 主控状态机最终专项复核原始输出

## 复核边界

- 时间：`2026-07-10T07:14:57-04:00`。
- 本次只复核：sample 的 `confirmation_required + user_confirmation`、`planned -> awaiting-user -> planned/failed`、`running -> awaiting-user -> running/failed`、claims 接受 / 拒绝后的回流。
- 本次读取：仅 `v3/skill/templates/run-manifest.md` 与 `v3/skill/roles/orchestrator.md` 中上述状态字段和转换规则。
- 本次未复核：mixed、dispatch/stages、角色数量、gate 枚举及其他已审项目。
- 上下文声明：本执行者做过前三份主控 raw；本次不是零上下文，但 verdict 只依据当前状态机文本重新判断。
- 保留规则：前三份 raw 保留不改；本次不修改任何规则文件。

## 总结论

- overall verdict：`fail`。
- 已修复：状态枚举现在能区分“是否要求确认”和“确认结果”；计划态等待、运行态用户体验等待、claims 接受 / 拒绝回流都已有明确路径。
- 剩余阻断：`confirmation_required` 与 `user_confirmation` 之间没有冻结合法组合，且 `planned -> running` 只排除 `pending`，没有明确排除 `declined`。因此 `confirmation_required: true + user_confirmation: not-required` 或 `declined` 仍可按字面绕过确认进入 running。
- 可声称范围：可以声称正向 / 拒绝分支已被写入；不能声称 sample 确认门或完整状态机已经闭合。

## 1. Sample 确认字段

- 当前字段：
  - `confirmation_required: true | false`
  - `user_confirmation: not-required | pending | confirmed | declined`
- verdict：`fail`。
- 正面进展：此前把“是否需要确认”和“确认结果”混在单一枚举的问题已经拆开；现在有能力表达无需确认、等待、同意和拒绝。
- 缺失不变量：两个字段的合法组合没有定义。至少应冻结：
  - `confirmation_required: false` 只能搭配 `user_confirmation: not-required`；
  - `confirmation_required: true` 只能搭配 `pending | confirmed | declined`，不能搭配 `not-required`。
- 当前风险：`false + pending`、`false + confirmed`、`true + not-required` 都是 schema 允许但语义矛盾的组合；不同主控可自行解释。

## 2. `planned -> awaiting-user -> planned/failed`

- 当前路径：
  - 必需样本确认 `pending`：`planned -> awaiting-user`，不得产生执行 dispatch。
  - 确认变为 `confirmed`：`awaiting-user -> planned`，重新核对。
  - 确认变为 `declined`：`awaiting-user -> failed`，不得 dispatch。
- verdict：`partial`。
- 已修复：等待入口、同意回计划态和拒绝终止均已明确，前一轮缺少拒绝终态的问题已关闭。
- 剩余 guard 缺口：`planned -> running` 只要求样本确认字段已填写且“不为 pending”。`declined` 也是已填写且不为 pending；`confirmation_required: true + user_confirmation: not-required` 同样不为 pending。因此按当前字面，两种非法 / 拒绝状态仍满足 running 的显式条件。
- 最小修复：把进入 running 的条件写成布尔约束：若 `confirmation_required: true`，必须是 `confirmed`；若为 false，必须是 `not-required`；`pending` 进入 awaiting-user，`declined` 只能进入 failed。

## 3. `running -> awaiting-user -> running/failed`

- 当前路径：
  - 用户体验 `pending` 或 `claims.awaiting_user_acceptance` 非空：`running -> awaiting-user`。
  - 用户体验返回 `pass`：`awaiting-user -> running`，重新结算。
  - 用户体验返回 `fail`：`awaiting-user -> failed`。
- verdict：`pass`。
- 判断：用户体验等待的正向和失败回流均已明确，不再悬空。重新进入 running 后仍受 accepted 的无 pending、门通过、预算和 claims 范围条件约束。
- 非阻断注意：如果用户体验和 claims 同时 pending，任一先返回都可能暂时回 running，再因另一项未清空重入 awaiting-user；这是可终止的重复结算，不造成无合法后继。

## 4. Claims 接受 / 拒绝回流

- 当前路径：`claims.awaiting_user_acceptance` 非空时进入 awaiting-user；用户逐项决定后，接受项移入 `can_claim`，拒绝项移入 `cannot_claim`，再回 running 重新结算。
- verdict：`pass`。
- 判断：声明拒绝不必让整个 run 失败；缩小到 `cannot_claim` 后仍可对其余实际执行且通过的链段给出有限 accepted，这与 claims 的范围语义一致。只要 awaiting 列表清空，accepted 的“无 pending + can_claim 只覆盖执行与验收交集”会继续约束最终状态。
- 可声称范围：可声称 claims 的 accepted / declined 回流已闭合；不可声称任何真实声明已经获得用户接受。

## 最终矩阵

| 状态机部分 | verdict | 结论 |
| --- | --- | --- |
| confirmation_required + user_confirmation | `fail` | 有字段，无合法组合不变量。 |
| planned→awaiting→planned/failed | `partial` | 分支已补，但 planned→running 仍可放行 declined / 非法组合。 |
| running→awaiting→running/failed | `pass` | 用户体验正向与失败回流闭合。 |
| claims accepted/declined 回流 | `pass` | 分别进入 can_claim / cannot_claim 后重新结算。 |

最终 overall verdict：`fail`。当前仅剩 sample 确认字段不变量与 planned→running guard；在这两处冻结前，不能把状态机或主控合同升级为通过。
