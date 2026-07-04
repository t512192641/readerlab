# 运行保护片段

运行保护段要求：`engineering_source_scope` 必须列出本次工程材料阅读覆盖的主来源，`full-source-track.md` 必须把这些来源闭环记录下来。

## 失败保护

如果 full-source evidence packet 缺失，runner 应阻断；如果资产卡缺少冷启动字段，Quality Gate / Reader Evaluation 应阻断；如果 blocking gate 失败，controller 不能给出接受结论。

## 复用边界

资产卡只能沉淀可操作技术材料：问题、做法、适用前提、风险、边界和来源。它不能要求未来 Agent 在第一步先回读原始 source 才知道怎么用。
