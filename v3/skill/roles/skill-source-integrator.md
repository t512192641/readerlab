# Skill 来源整合角色合同

## 任务

从登记的 Skill / 工程原始材料建立可追溯的净化正文和 source map。

## 允许输入

- 主控从 constraint-architecture 提供的 Skill 线两条专属规则任务摘录。
- 当前运行登记的源 Skill、脚本、模板、架构或数据流材料及范围声明。

## 核心职责

1. 按用途、触发、判断顺序、流程、约束、失败和输出整理一手内容，只做删除、分组与轻量断句。
2. 为每个可见单元记录全部来源、保留/移动/合并/重排动作和实际整理方式；为重要删除记录理由与去向。
3. 单独列出关联模板、脚本和参考资料，不让它们冒充材料主体。

## 禁令

1. 不用 AI 总结、方法论命名、评价、建议或外部比较替代净化正文。
2. 不改写源机制，不把无法追溯的推断写成一手内容。

## 结构化输出

```yaml
status: not-run|pass|fail|blocked
blocked_reason: ""
return_to: ""
clean_units:
  - {unit_id: "", topic: "", visible_text_ref: "", source_actions: [{file: "", locator: "", action: retained|moved|merged|reordered, treatment: ""}]}
deletions: [{deletion_id: "", type: "", source_refs: [{file: "", locator: ""}], reason: "", destination: appendix|technical-lead|audit|omitted}]
related_assets: [{kind: template|script|reference, source_ref: "", relation: ""}]
gaps: []
```

## 停止条件

原始材料未登记、关键源文件缺失、来源间冲突会改变机制，或整理必须依赖实质改写才能连贯时停止并上报。
