# Discovery Scout V1'（自由 trigger map，冻结候选）

你将收到一个完整阅读单元。目标不是摘要、改写、找主题或复述作者观点，而是寻找能让普通读者重新理解文中关键关系的、可核验的外部知识透镜。

在提出 seed 前，先独立建立一张自由的 `trigger_map`：只记录原文中“某个关系已经出现，但解释它所需的变量仍缺失”的位置。不要套用固定异常类型、预设学科清单或答案菜单；材料若没有这种位置，trigger 可以为 0。trigger_map 只帮助本次 Scout 搜索，后续 Normalizer 和 Judge 看不到它。

然后只保留满足以下最低条件的候选：

- 透镜给原文增加一个原文没有直接命名的解释机制，而不只是换名；
- 能指出原文中的确切英文锚点，并说明重读后发生了什么改变；
- 外部身份具体到可检索、可证伪的概念、模型、研究路线或历史机制；
- 有至少一个可核验来源线索。

不要为了凑数输出。材料若只有静态描述或没有可靠的外部增量，可以返回 0 个 seed。最多 6 个。不得使用本次材料以外的本地文件、历史结果、审计材料、金标、样张或其他 run。

输出一个 JSON 对象，且只含两个顶层字段：

- `trigger_map`：符合 `trigger-map.schema.json`；
- `seed_batch`：与 V0 完全相同，符合 `seed-batch.schema.json`。

trigger_map 不得改变 seed_batch 的字段、每字段长度或 seed 上限。各字段必须简洁，不写完整文章，不预测 Judge 标准。

运行 ID：`{{RUN_ID}}`

阅读单元如下：

<READING_UNIT>
{{EXACT_SOURCE_BYTES_UTF8}}
</READING_UNIT>
