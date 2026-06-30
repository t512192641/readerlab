# ReaderLab 结构化提炼同题多路线对照 v0

## 结论

本轮按 D-039 做同题多路线对照。主 Agent 判断：**Combo-B 暂时胜出，适合作为下一轮候选主链，但不能进入生产链，也不能称为生成器能力**。

Combo-B 的顺序是：

1. source-grounded 前置：先限定原文能说什么、不能说什么。
2. 仓颉候选筛选：再判断什么值得通过、降级或拒绝。
3. 李继刚式受控表达：最后把已经通过或降级的判断写成机制传导和读者可理解的结构。

这个顺序比 Combo-A 更稳，因为 Combo-A 把 source-grounded 放在后面，容易让前面已经形成的强解释变成“事后补证”。Combo-B 的价值不是拼字段，而是让上游来源约束能阻断中游筛选和下游表达。

## 本轮输入

- 基线材料：《埃隆之书》。
- 对照路线：
  - Cangjie-only。
  - Li Jigang-only。
  - ReaderLab-current-chain。
  - Combo-A：李继刚定性 -> 仓颉筛选 -> source-grounded 后置。
  - Combo-B：source-grounded 前置 -> 仓颉筛选 -> 李继刚表达。
- 独立横评：Meta Skill 方法约束下的评估 worker。
- 主 Agent 源文抽查：
  - `v101-16.xhtml`：算法之道顺序明确，删除在优化、加速、自动化之前。
  - `v101-14.xhtml`：睡工厂是紧急边界，不可常态化。
  - `v101-18.xhtml`：工厂即产品，制造系统本身是产品能力。
  - `v101-11.xhtml`：第一性原理和成本拆解。
  - `v101-27.xhtml`：多行星叙事需外部核验。
  - `v101-29.xhtml`：69 法则是混合索引，不能整体升格。

## 主 Agent 最终取舍

| 路线 | 主判断 | 用法 |
|---|---|---|
| Combo-B | 暂时胜出 | 下一轮候选主链，必须过 gate。 |
| Combo-A | 有组合增益但顺序风险更高 | 备选，不作为主顺序。 |
| Li Jigang-only | 最强单一路线 | 只作为受控表达层，不能独立进生产链。 |
| Cangjie-only | 筛选强 | 作为中段候选筛选引擎。 |
| ReaderLab-current-chain | 字段齐但新增判断力不足 | 作为 baseline 和契约雏形。 |

## 不能过度声称

- 本轮不是 LifeAtlas 正式阅读包。
- 本轮不是全书产品重写。
- 本轮没有改 `scripts/readerlab.py`。
- 本轮没有新增依赖、没有安装或启用 Skill。
- 本轮没有写 LifeAtlas `300/600/800`。
- 本轮仍缺 blind A/B、第二类材料迁移测试、完整 fresh source-grounded contract 和人工验收。

## 文件

- `routes/01_同题路线摘要.md`：五条路线的同题输出摘要和主 Agent 审查。
- `audit/90_同题多路线评估.md`：独立评估、组合增益判断、gate 和下一步。
- `assertions.md`：本轮断言、通过项、未通过项和剩余风险。
