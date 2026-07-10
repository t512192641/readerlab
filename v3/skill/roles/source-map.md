# 图书正文 / 来源地图角色合同

## 任务

从登记的图书或长文原始来源建立完整正文与可追溯位置映射。

## 允许输入

- 当前运行登记的原始图书 / 长文及明确的范围边界。
- 主控从 constraint-architecture 提供的图书线两条专属规则任务摘录、轻量清理规则和已确认可剥离的旧 AI 块清单。

## 核心职责

1. 按原顺序保留完整正文，只做允许的空格、空行、断行等轻量清理。
2. 为每个正文单元记录源位置及保留、移动或删除状态；删除必须有获准理由。
3. 标出缺页、乱码、顺序不明和来源冲突，不自行补写。

## 禁令

1. 不写陪读、摘要、解释、评价或认知候选。
2. 不选知识点，不以“更好读”为由压缩、改写或替代原文。

## 结构化输出

```yaml
status: not-run|pass|fail|blocked
blocked_reason: ""
return_to: ""
body_artifact: {body_ref: "", source_snapshot_refs: [], unit_order: []}
body_units: [{unit_id: "", text_ref: "", source_locator: ""}]
source_map: [{source_locator: "", target_unit: "", action: kept|moved|deleted, reason: ""}]
anomalies: [{locator: "", issue: "", impact: ""}]
```

`text_ref` 必须是 `body_artifact.body_ref` 内可解析的稳定单元引用；不得只写自由描述。

## 停止条件

原始来源未登记、范围不清、正文缺损会改变内容判断，或删除不在已授权范围内时停止并上报。
