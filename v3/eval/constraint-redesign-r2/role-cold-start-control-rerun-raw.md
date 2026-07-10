# 主控合同输入 / Schema 修订后独立复核原始输出

## 复核身份与边界

- 时间：`2026-07-10T07:09:23-04:00`。
- 本次重新读取：`v3/skill/roles/orchestrator.md`、`v3/skill/roles/README.md`、`v3/skill/templates/run-manifest.md`。
- 本次未读：线路协议、其他角色合同、回归 case / suite、真实 run 产物和其他验收结果。
- 前序上下文：本执行者写过首次失败审查 `role-cold-start-control-raw.md`，也更早做过 Skill case 回归；因此本次不是零历史上下文。复核只以三份修订文件的当前文本为新证据，按首次 raw 的八类缺口逐项对照，不用首次结论替代重判。
- 保留规则：首次失败 raw 保留不改；本次只新增本文件，不修改任何合同、索引或 manifest。
- 复核性质：静态 schema rerun，不执行真实 dispatch、gate、fresh/revision run 或内容生成。

## 总结论

- overall verdict：`fail`。
- 修复进展：首次 raw 的大部分缺口已经实质修复。唯一 manifest 引用、实例级 dispatch、verification 专属枚举、claims 引用、Skill 双门、图书 11 / Skill 5 计数均已闭合或达到可执行合同要求。
- 仍未闭合：
  1. `mixed` 父 manifest 在“拆 child run 或 blocked”之前仍被 schema 强制填写 `route.line: book | skill`，与“不得静默选线”冲突。
  2. stages 映射在两个文件中用词不一致：manifest 明确 `done -> executed`、`reused -> reused_without_rerun`，orchestrator 却写成 `done/skipped/failed/reused` 写入“同名 stages”；实际不存在 `done` 与 `reused` 两个 stage key。
  3. 状态机没有 `planned -> awaiting-user`，也没有 `awaiting-user -> running/failed/accepted` 的恢复路径；而 `planned -> running` 又禁止存在前置 pending，导致开跑前等待用户时 `awaiting-user` 不可达，等待解除后也无合法后继。
- 结论边界：当前修订不能声称“主控 schema 完全闭合”。可以声称“首次八类问题中五类已通过、两类部分通过、一类仍因状态机失败；剩余问题集中在 mixed、stage 命名和 awaiting-user 转换”。

## 逐项复核

### 1. 线路映射

- 首次问题：主控只有 `book | skill`，manifest 只有 `material_type`，`longform / engineering / mixed` 无映射。
- 当前证据：manifest 新增 `route.line: book | skill`、`mixed_handling` 和 `child_run_ids`；正文明确 `longform -> book`、`engineering -> skill`，`mixed` 必须拆 child manifests 或 blocked。
- verdict：`partial`。
- 已修复：普通材料的 `material_type -> line` 映射明确，主控 `run_ref.line` 与 manifest `route.line` 可以对齐。
- 剩余冲突：schema 对所有 manifest 都要求 `route.line: book | skill`。当 `material_type: mixed` 且尚未拆分、状态应为 `blocked` 时，没有 `not-applicable | pending | mixed-parent` 值；父 manifest 仍必须先选 `book` 或 `skill`。这与“拆分前不得静默选线”直接冲突。
- 影响：mixed 父 run 无法同时满足 YAML 枚举和文本规则；审计者也无法区分“父容器无执行线路”与“已选择一条线路”。
- 最小剩余修复：允许 mixed 父 manifest 的 `route.line` 为非执行值，或规定 mixed 不创建父 run manifest、只创建已选线 child manifests，并定义 blocked 记录放在哪里。

### 2. 唯一 manifest 引用

- 首次问题：主控输出没有 `run_id / manifest_path`，source、output、claims 形成第二套摘要事实源。
- 当前证据：主控新增 `run_ref: {run_id, manifest_path, line, mode, status}` 与 `claims_ref`；合同明确 `run_ref`、`verification`、`claims_ref` 必须与同一 manifest 完全一致，不得作为第二事实源；核心职责也要求以唯一 manifest 记录事实。
- verdict：`pass`。
- 判断：run 身份和 claims 已有明确引用，主控镜像字段的同源约束也被写明。静态合同层已闭合；真实运行是否漂移仍需 run 证据验证，不属于本次静态复核。
- 可声称范围：可声称“合同要求唯一 manifest 为事实源”；不可声称任何真实 run 已遵守。

### 3. Dispatch 唯一实例与交付证据

- 首次问题：无 dispatch / instance id、stage、依赖、实际输出、证据和 gate 绑定，不能证明图书重复实例独立执行。
- 当前证据：dispatch 新增 `dispatch_id`、`instance_id`、`line`、`stage`、`depends_on`、`input_refs`、`actual_output_refs`、`evidence_refs`、`gate_keys`、`counted_task` 和完整状态；文本明确 `dispatch_id` 唯一，图书两个提名实例与三个候选实例必须分别记录。
- verdict：`pass`。
- 判断：首次识别的实例歧义、交付位置与 gate 绑定缺口均已被直接补上。虽然没有机器 validator，本次评价的是 Markdown 合同，唯一性和分别记录规则已经足够明确。

### 4. Gate 名称与枚举

- 首次问题：自由 `name` 无法保证门齐全；通用 verdict 无法表达 `not-applicable`、`not-requested`、`pending`。
- 当前证据：orchestrator 的 `verification` 固定列出与 manifest 相同的七个 key；每个 key 使用对应专属枚举，并记录 owner、scope、evidence、conflicts。
- verdict：`pass`。
- 判断：六个独立技术门与用户体验门均能无损表达；cold-read 和 cold-start/reproduction 的 `not-applicable`、用户体验的 `not-requested/pending` 已补齐。
- 可声称范围：可声称“主控与 manifest 的 gate key 和状态枚举一致”；不可声称各门真实执行通过。

### 5. Stages 与预算映射

- 首次问题：dispatch 状态与 manifest stages 无映射，`actual_tasks` 无统一计数规则。
- 当前证据：manifest 明确 stages 只记录 dispatch id，并定义 `done -> executed`、`skipped -> skipped`、`failed -> failed`、`reused -> reused_without_rerun`；`budget.actual_tasks` 等于实际计费的非复用、非跳过 dispatch 数。orchestrator 也增加 `counted_task`，并要求预算只统计实际执行且计费的 dispatch。
- verdict：`partial`。
- 已修复：计数原则和 dispatch id 入 stages 的方向已闭合，主控不再维护第二套任务数。
- 剩余直接不一致：orchestrator 写“`done/skipped/failed/reused` 分别写入 manifest 同名 stages”，但 manifest 的 key 是 `executed/skipped/failed/reused_without_rerun`。`done` 与 `reused` 没有同名 stage；只有 manifest 另一处的转换表给出正确映射。
- 影响：按 orchestrator 字面执行会尝试写不存在的 `stages.done` / `stages.reused`；按 manifest 执行则不会。两个权威输入不能同时逐字成立。
- 预算剩余注意：`counted_task` 的布尔值与“实际计费”仍需执行者据事实填写，但当前文字已足够判断 skipped/reused 不计、实际执行任务计入；这不是本次失败主因。
- 最小剩余修复：把 orchestrator 的“同名 stages”改为与 manifest 完全相同的四项显式映射。

### 6. Skill 冷读与冷启动 / 复现双门

- 首次问题：一个 `cold-start-reproducer` 实例承载两门，但主控 schema 无法分别记录，也未明确共用 fact-checker 的 Skill 预算规则。
- 当前证据：orchestrator 分别记录 `cold_read` 和 `cold_start_or_reproduction`，dispatch 可通过 `gate_keys` 同时绑定两门；README 明确由 cold-start-reproducer “分门验证”。README 也明确标准 Skill 为 5 个实例，只有引入外部事实才追加共用 fact-checker，并按协议触发预算审批。
- verdict：`pass`。
- 判断：同一独立实例可产出两个分门结果，两个结果在 schema 中独立保存；条件 fact-checker 不再造成标准五任务计数歧义。
- 可声称范围：可声称“合同可表达 Skill 双门并保持标准 5 实例”；不可声称冷读与复现已经真实执行或由不同 Agent 完成。

### 7. Run 状态转换

- 首次问题：`accepted / failed / awaiting-user` 没有确定性进入条件。
- 当前证据：manifest 新增 `planned -> running`、`running -> awaiting-user`、`running -> failed`、`running -> accepted` 和 revision 局部接受规则；orchestrator 明确完全服从 manifest 状态转换。
- verdict：`fail`。
- 已修复：running 之后的主要终局条件和 revision 的局部接受范围已明确；`accepted` 不再可由主控自由解释。
- 不可达状态：`planned -> running` 要求“不得有前置 pending 用户确认”，但唯一进入 `awaiting-user` 的规则是 `running -> awaiting-user`。当样本确认在开跑前为 `pending` 时，既不能进入 `running`，又没有 `planned -> awaiting-user`，所以 manifest 的 `awaiting-user` 状态不可合法到达。
- 无恢复路径：一旦 `running -> awaiting-user`，规则没有 `awaiting-user -> running`、`awaiting-user -> failed` 或 `awaiting-user -> accepted`。用户完成确认、体验判定或声明接受后，状态机无法继续。
- 失败映射歧义：`running -> failed` 说必需门 `fail` 或不可恢复 `blocked` 会失败，但没有明确被请求的 `user_experience: fail` 是否属于必需门；这可通过定义必需门集合一并消除。
- 最小剩余修复：增加开跑前等待与等待后恢复转换，至少覆盖 `planned -> awaiting-user`、`awaiting-user -> running`，并定义等待后拒绝 / 体验失败如何进入 `failed` 或有限声明终态。

### 8. Claims 与接受范围

- 首次问题：主控只有模糊 `claim_scope`，不能无损表达 manifest 四类 claims；accepted 与 claims 无联动。
- 当前证据：主控改为 `claims_ref: {manifest_path, section: claims}`，并规定必须与同一 manifest 一致；manifest 保留 `can_claim`、`cannot_claim`、`reused_results_only`、`awaiting_user_acceptance`；accepted 要求 `can_claim` 只覆盖执行与验收交集，revision 继续排除未重跑链段和完整流程。
- verdict：`pass`。
- 判断：claims 不再被压成第二套列表，局部 revision 和等待用户接受的范围得到保留。真实内容是否写对仍需独立验收，不属于静态 schema 闭合问题。

## 角色实例计数复核

### 图书线

- README 明确标准任务数不含主控，图书为 `1 + 2 + 1 + 3 + 1 + 1 + 1 + 1 = 11`。
- 重复实例可通过 `dispatch_id + instance_id` 分别记录。
- verdict：`pass`。

### Skill 线

- README 明确标准 Skill 为 5；外部事实触发时才追加 fact-checker 并走预算审批。
- cold-start-reproducer 可用两个独立 gate key 分门输出冷读与冷启动 / 复现结果。
- verdict：`pass`。

## 修复矩阵

| 首次缺口 | rerun verdict | 结论 |
| --- | --- | --- |
| 线路映射 | `partial` | book/longform/skill/engineering 已闭合；mixed 父 manifest 仍被迫选线。 |
| 唯一 manifest 引用 | `pass` | `run_ref + claims_ref + 同源约束` 已建立。 |
| dispatch 实例 | `pass` | 唯一 id、重复实例、依赖、交付和 gate 绑定已补齐。 |
| gate 枚举 | `pass` | 七个 key 与各自枚举一致。 |
| stages / 预算映射 | `partial` | manifest 映射正确；orchestrator “同名 stages”措辞与真实 key 冲突。 |
| Skill 双门 | `pass` | 两门分开记录，标准 5 实例与条件 fact-checker 已澄清。 |
| 状态转换 | `fail` | awaiting-user 开跑前不可达，进入后无恢复路径。 |
| claims | `pass` | 引用 manifest 四类 claims，accepted / revision 范围已绑定。 |

## 最终可声称范围

- 可以声称：
  - 修订已经实质解决唯一 manifest、dispatch 实例、gate 枚举、Skill 双门、claims 和 11 / 5 角色计数问题。
  - 普通 book / longform / skill / engineering 的线路映射已明确。
  - manifest 已提供 running 后的主要 accepted / failed 判断框架。
- 不可以声称：
  - 主控合同 schema 已完全闭合或 rerun 通过。
  - mixed 父 run 能在不选线的前提下合法建 manifest。
  - stages 名称在两个文件中完全一致。
  - awaiting-user 状态可以从计划态进入并在用户回应后恢复。
  - 任何真实 run、角色 dispatch、独立 gate 或 claims 已实际通过。

最终 overall verdict：`fail`。首次失败 raw 应继续保留；修完上述三个剩余合同冲突后再做下一次静态 rerun。
