# High-Order Explanation Contract v1

## 目的

`high-order-explanation.v1` 是高阶讲解的内部事实契约。它记录 Agent 如何从正文锚点出发，识别普通总结陷阱，生成升维问题、机制图、镜头选择、吸收 / 降级 / 拒绝判断，并最终产出 reader-facing 自然讲解。

该 contract 属于 `audit/contracts/` 或样本 audit 层，不直接作为读者页内容。

## 最低字段

```json
{
  "contract_type": "high-order-explanation.v1",
  "unit_id": "",
  "material_type": "book_longform | skill_engineering | mixed",
  "source_scope": "",
  "source_anchors": [
    {
      "anchor_id": "a01",
      "source_ref": "",
      "what_text_says": "",
      "supports": [],
      "does_not_support": []
    }
  ],
  "baseline_summary_trap": "",
  "upgrade_question": "",
  "mechanism_graph": {
    "input": [],
    "constraint": [],
    "action": [],
    "feedback": [],
    "output": [],
    "failure_mode": [],
    "boundary": []
  },
  "lens_candidates": [
    {
      "lens": "",
      "text_trigger": "",
      "clarifies": "",
      "boundary_power": "",
      "reader_gain": "",
      "overreach_risk": "",
      "scores": {
        "text_trigger_strength": 0,
        "explanatory_power": 0,
        "boundary_power": 0,
        "reader_gain": 0,
        "overreach_risk": 0,
        "total": 0
      },
      "decision": "promote | downgrade | reject"
    }
  ],
  "judgments": {
    "absorb": [],
    "downgrade": [],
    "reject": []
  },
  "reader_facing_explanation": {
    "title": "",
    "body": ""
  },
  "delta_eval": {
    "beyond_summary": false,
    "upgrade_question_present": false,
    "mechanism_present": false,
    "lens_illuminates_text": false,
    "source_boundaries_clear": false,
    "overreach_controlled": false,
    "verdicts_clear": false,
    "reader_gain": ""
  },
  "machine_status": "draft | machine_checked",
  "human_status": "pending | reviewed | accepted | rejected"
}
```

## 字段规则

### source_anchors

- 记录正文锚点，不写宏大解释。
- 每个锚点必须说明它支持什么，也必须说明它不能支持什么。
- 若 source scope 只是局部章节或样本，不能写完整全书结论。

### baseline_summary_trap

- 记录普通总结会怎样讲。
- 只用于内部对照，不进入 reader-facing。
- 最终讲解若只比 baseline 更顺，判 FAIL。

### upgrade_question

必须把表面主题改写成更大的问题：

```text
在什么约束下，谁要把什么资源转化成什么结果，同时避免什么失败？
```

### mechanism_graph

必须把正文内容串成机制，而不是列点。

如果材料无法支撑完整机制图，应显式标注缺口，不得靠 AI 常识补齐。

### lens_candidates

候选镜头至少 3 个，最多 7 个。每个镜头必须有正文触发点和发散风险。

Promote 条件：

- 总分 >= 7。
- `overreach_risk` 不低于 -1。
- 能反向照亮正文。

每篇 reader-facing 高阶讲解最多使用 2 个主镜头和 1 个边界镜头。

### judgments

必须区分：

- `absorb`：可吸收为判断框架或行动方法。
- `downgrade`：有启发但需降级、限场景使用。
- `reject`：不应学习或不应迁移。

reader-facing 可以用自然语言表达这些裁决，但 contract 必须保留结构化判断。

### reader_facing_explanation

读者页只显示自然标题和成段讲解。不展示 source refs、lens score、machine status、human status、claim trace 或内部字段名。

### delta_eval

必须证明新版不是普通总结。若以下任一项为 false，应判定本轮不通过：

- `beyond_summary`
- `upgrade_question_present`
- `mechanism_present`
- `lens_illuminates_text`
- `overreach_controlled`
- `verdicts_clear`

## 最小验收

```text
[ ] 有 8-15 个 source anchors
[ ] 有 baseline summary trap
[ ] 有 upgrade question
[ ] 有 mechanism graph
[ ] 有 3-7 个 lens candidates
[ ] Promote 的 lens 满足照亮测试
[ ] 有 absorb / downgrade / reject
[ ] reader-facing 是自然讲解，不是栏目墙
[ ] delta eval 证明它超过普通总结
[ ] audit 和 reader-facing 分离
```

## 强制失败条件

```text
[FAIL] 只复述本章讲了什么。
[FAIL] 只把旧讲解改写得更流畅。
[FAIL] 没有升维问题。
[FAIL] 没有机制链。
[FAIL] 镜头不是由正文触发，而是外部模型硬套。
[FAIL] 外部类比不能反向照亮正文。
[FAIL] 没有吸收 / 降级 / 拒绝。
[FAIL] 把 AI 解释、外部类比或待验证判断写成原文结论。
[FAIL] reader-facing 暴露 source refs、claim trace、lens score、machine_status 或 human_status 作为主内容。
```
