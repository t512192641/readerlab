---
status: frozen
scope: run-only
---

# T2.2 v4 负向先行校准合同

## 1. 边界与举证责任

本合同只用于本次固定盲包的规则回归，不修改长期产品 owner 或 T1.8，不证明未知材料泛化、裁判资格、M2、T3 或生产许可。

1. 举证责任在 candidate。角色不得用外部知识补写 candidate 没写出的机制、关系、边界或因果链。
2. skeptical reader 先只寻找最强反对理由、未支持关系和裁判不得自行补写的内容，不给最终处置。
3. final judge 必须先逐条处理冻结 objection；驳回只能引用 candidate 自身文字。
4. 硬否决优先，任何正向轴都不能抵消硬否决。
5. 放行必须由 candidate 自身提供全部六类正面证据。
6. `borderline` 只用于没有硬否决、核心价值成立、但恰有一个非承重边界或局部呈现不足的对象。
7. 实质轴 `unknown` 在本次校准中不得放行。

默认读者是正在读本书、具备正常常识和判断力的成年人。有一点新增不等于有足够增量。只有非显然、重要、具体、展开充分、命中原文承重问题且逻辑闭合的补充，才可能值得打断阅读。

## 2. skeptical reader 输出合同

`objection-sheet.json` 顶层必须是：

- `schema`: `readerlab-t2.2-v4-objection-sheet/v1`
- `run_id`: `T2.2-sufficiency-calibration-v4`
- `status`: `frozen`
- `completed_at_utc`: UTC ISO-8601
- `agent`: 含 `id`、`model`、`reasoning`、`fork_turns`、`calls`
- `cases`: 盲包顺序的 12 项

每项必须包含：

- `id`
- `strongest_objection`: 含 `claim`、`weight`、`source_quotes`、`candidate_quotes`
- `source_quotes`
- `candidate_quotes`
- `veto_checks`
- `unsupported_links`
- `judge_must_not_supply`

`weight` 只能为 `load_bearing` 或 `non_load_bearing`。

`veto_checks` 必须恰含以下七项：

- `common_sense_small_step`
- `relabel_or_reorganize`
- `external_not_self_contained`
- `load_bearing_direction_miss`
- `unsupported_causal_link`
- `critical_explanation_gap`
- `substantive_unknown`

每个 veto 必须含：

- `status`: `present` / `absent` / `unknown`
- `weight`: `load_bearing` / `non_load_bearing`
- `source_quotes`: 字符串数组
- `candidate_quotes`: 字符串数组
- `reason`: 为什么成立、不成立或证据不足；candidate 找不到支持时必须明确写出

`unsupported_links` 的每项必须含唯一 `id`、`claim`、`weight`、`source_quotes`、`candidate_quotes`、`missing_support`。

`judge_must_not_supply` 的每项必须含唯一 `id`、`claim`、`weight`、`candidate_quotes`、`missing_from_candidate`。如果所列内容确实未写在 candidate 中，`candidate_quotes` 应为空数组，不得用推断补齐。

skeptical reader 必须对 12 项使用同样强度，不得给最终处置、预测产品答案或把 source 和 candidate 都没写的机制当作事实补进理由。

## 3. final judge 输出合同

`final-judgment.json` 顶层必须是：

- `schema`: `readerlab-t2.2-v4-final-judgment/v1`
- `run_id`: `T2.2-sufficiency-calibration-v4`
- `status`: `frozen`
- `completed_at_utc`: UTC ISO-8601
- `agent`: 含 `id`、`model`、`reasoning`、`fork_turns`、`calls`
- `cases`: 盲包顺序的 12 项

### 3.1 五项原始判断

每项都必须是对象，包含 `value`、`candidate_quotes`、`source_quotes`、`reason`、`boundary`：

- `content_increment.value`: `substantial` / `none` / `unknown`
- `explanation_depth.value`: `sufficient` / `insufficient` / `unknown`
- `source_relevance.value`: `holds` / `does_not_hold` / `unknown`
- `cognitive_leverage.value`: `formed` / `not_formed` / `unknown`
- `presentation_quality.value`: `clear` / `impairs_understanding` / `unknown`

### 3.2 run-only 子类

每项都必须是对象，包含 `value`、`candidate_quotes`、`reason`：

- `explanation_gap_class.value`: `none` / `critical` / `non_critical` / `unknown`
- `presentation_issue_class.value`: `none` / `critical` / `local` / `unknown`

### 3.3 六类正面证据

`positive_evidence` 必须恰含以下六项：

- `new_claim`
- `non_obvious_and_important`
- `explanation_chain`
- `load_bearing_hit`
- `cognitive_change`
- `logical_closure`

每项必须包含：

- `status`: `supported` / `unsupported` / `unknown`
- `candidate_quotes`: 字符串数组
- `reason`
- `boundary`

六项都必须以 candidate 自身文字为证据；`supported` 时 `candidate_quotes` 不得为空。

### 3.4 objection 处理

`objection_resolutions` 必须包含：

- `strongest_objection`
- `veto_checks`
- `unsupported_links`
- `judge_must_not_supply`

每条 resolution 必须与 objection sheet 的对应项一一绑定，并包含：

- `resolution`: `accepted` / `rejected` / `unresolved`
- `candidate_quotes`: 字符串数组
- `reason`

数组项还必须保留 objection 的 `id`；`veto_checks` 必须以七个固定 veto 名称为键。任何 `rejected` 必须有非空 candidate 引文，否则输出无效。

### 3.5 聚合字段

每题还必须包含：

- `hard_vetoes`: 字符串数组
- `minor_limitations`: 对象数组；每项 `type` 只能为 `explanation_gap` 或 `presentation_issue`，并含 `reason`
- `aggregation_trace`: 含 `derived_hard_block_reasons`、`minor_count`、`derived_disposition`、`reason`
- `final_disposition`: `allow` / `block` / `borderline`

## 4. 机械聚合

verifier 根据结构化字段自行复算，不信任 final judge 自报的处置。

### 4.1 Hard block

命中任一条件即 `block`：

- skeptical reader 任一 veto 为 `present`，且 final judge 未以非空 candidate 引文 `rejected`；
- skeptical reader 任一 `load_bearing` veto 为 `unknown`；
- `content_increment=none`；
- `source_relevance=does_not_hold`；
- `cognitive_leverage=not_formed`；
- `explanation_gap_class=critical`；
- `presentation_issue_class=critical`；
- `content_increment`、`explanation_depth`、`source_relevance` 或 `cognitive_leverage` 任一为 `unknown`；
- 六类正面证据任一为 `unsupported` 或 `unknown`；
- `load_bearing` strongest objection、unsupported link 或 judge-must-not-supply 为 `accepted` 或 `unresolved`；
- `load_bearing` 的 present/unknown veto 为 `accepted` 或 `unresolved`；
- external 类比或事实承担主张但 candidate 不自足；
- 正常成年人可轻易想到的小步、只换术语或重组、承重方向偏移、未支持因果链成立。

呈现轴为 `unknown` 时不能 `allow`；若其余全部满足且仅此一项不足，只能进入 `borderline`。

### 4.2 Borderline

只有同时满足以下条件才为 `borderline`：

- 没有 hard block；
- `content_increment=substantial`；
- `explanation_depth=sufficient`；
- `source_relevance=holds`；
- `cognitive_leverage=formed`；
- `presentation_quality=clear` 或 `unknown`；
- 六类正面证据全部 `supported`；
- 恰好一个 minor limitation；
- 该 limitation 恰为 `explanation_gap_class=non_critical`，或 `presentation_issue_class=local`，或仅 `presentation_quality=unknown`；
- 不能同时存在两个 minor limitation。

### 4.3 Allow

只有同时满足以下条件才为 `allow`：

- 没有 hard block；
- 五项原始判断依次为 `substantial`、`sufficient`、`holds`、`formed`、`clear`；
- explanation gap 与 presentation issue 均为 `none`；
- 六类正面证据全部 `supported`；
- 所有 objections 都以非空 candidate 引文 `rejected`；
- 没有 minor limitation。

其余组合为 `block`。若 final judge 的 `final_disposition`、`aggregation_trace.derived_disposition` 或 hard/minor 字段与 verifier 复算不一致，执行状态为 `BLOCKED`。

## 5. 不得补写

角色只能使用 packet 中的 source 与 candidate。不能查询事实、补充背景、替 candidate 发明机制或把表达顺滑当作逻辑闭合。外部概念或案例若承担主张，candidate 必须自己讲清“它是什么、为何与原文相关、具体增加什么认识”。
