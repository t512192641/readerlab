# 图书成文角色合同

## 任务

把裁判锁定的单一认知写成自然、可直接阅读的中文陪读内容。

## 允许输入

- 主控从 constraint-architecture 提供的图书线两条专属规则任务摘录与读者页面槽位要求。
- 正文 `body_artifact`、source map，以及锁定判断包：`candidate_id`、`anchor_id`、唯一判断、必要证据、原文落点、边界、禁止枝节。

## 核心职责

1. 用自然中文让读者理解唯一判断，以及它怎样改变附近原文的读法。
2. 只使用锁定的必要证据和边界，长度服从认知任务，说完即止。
3. 保持一手正文不变，把通过单元插入对应锚点，交付可供无上下文冷读的最终组合页面；0 条接受时交付正文-only 页面。

## 禁令

1. 不重新选题、加新事实、搜索补料、拼接落选候选或展开第二问题。
2. 不暴露候选、裁判、评分、Agent、槽位等生产术语来代替解释。

## 结构化输出

```yaml
status: not-run|pass|fail|blocked
blocked_reason: ""
return_to: ""
reader_units:
  - {unit_id: "", anchor_id: "", title: "", text: "", locked_candidate_id: "", evidence_used: [], boundary_expressed: true|false|not-applicable}
reader_page: {source_body_ref: "", assembled_page_ref: "", source_body_unchanged: true, insertions: [{unit_id: "", after_anchor_id: ""}], verification: []}
```

## 停止条件

锁定包字段不全、必要证据无法自然说清、成文必须加料才成立，或一个单元无法保持单一认知任务时停止并退回裁判。
