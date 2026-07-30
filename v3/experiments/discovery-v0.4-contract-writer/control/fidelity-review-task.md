# ReaderLab v0.4 Fidelity Review Task

version: `v0.4-control-candidate`
date: `2026-07-30`
status: `control-only / not-executed`

## Purpose

本任务在全新上下文中检查 Writer 是否忠实保留 C5 合同与 structured asset。Reviewer 只记录检查结果，
不得改写、润色或替 Writer／Expert 返工。

## Input whitelist（fresh context）

只能读取以下 3 个输入：

1. C5 contract；
2. C5 structured asset；
3. C5 Writer draft。

禁止读取 source context、candidate seed、teaching draft、expert review、product review、搜索结果、其他
版本、cold-read、历史判词或任何额外材料。不得研究事实，不得打开新来源。

## Fixed output fields

```text
candidate_id: C5
input_set: <contract / asset / draft frozen identities>
cognitive_turn: PASS | FAIL
value_distribution_execution: PASS | FAIL
conditional_judgment: PASS | FAIL
case_diagnosis: PASS | FAIL
author_conclusion_repackaged: NO | YES
fabricated_fact_mechanism: NO | YES
lost_usage: NO | YES
lost_boundary: NO | YES
return_target: NONE | WRITER | EXPERT
return_reason: <field-level control reason; no rewrite>
final: FIDELITY_PASS | RETURN_WRITER | RETURN_EXPERT
stop: PASS | STOP
```

## Check rules

- `cognitive_turn`：草稿必须保留从原文观察到外部结构带来的认知转向，不得退回原文复述。
- `value_distribution_execution`：必须保留 `value-distribution-execution` 及其
  `costs concentrated / benefits dispersed`、`free riding / fulfillment` 关系。
- `conditional_judgment`：不得把最高允许主张升级为无条件、普遍或确定因果断言。
- `case_diagnosis`：当前案例只能是结构的应用诊断，不能变成外部结构的唯一来源或一例冲突结论。
- `author_conclusion_repackaged`：若正文只是把作者原结论换名、换序或加术语，记 `YES`。
- `fabricated_fact_mechanism`：若正文加入 contract／asset 未提供的事实或机制，记 `YES`。
- `lost_usage`：若失去离开当前案例后的用途，记 `YES`。
- `lost_boundary`：若失去条件、适用范围或禁止更强主张的边界，记 `YES`。

## Final mapping

- 全部正向检查通过、两项越界检查均为 `NO`、usage 与 boundary 均为 `NO`：`FIDELITY_PASS`。
- 合同和资产完整，但 Writer 改写、遗漏、捏造或丢失使用／边界：`RETURN_WRITER`。
- 合同或资产本身缺字段、身份／结构／来源不闭合，导致无法判断：`RETURN_EXPERT`。

Reviewer 不得用返回意见直接修复草稿。任何 `RETURN_*` 都是停止门：返回指定角色，保留原始输入，禁止
在本任务内生成 v2。

## Acceptance gate

验收只看字段是否齐全、检查是否基于三份白名单输入、终局是否为规定的三种之一，以及是否没有出现
替写内容。`FIDELITY_PASS` 不是 cold-read 通过，也不是产品负责人接受。
