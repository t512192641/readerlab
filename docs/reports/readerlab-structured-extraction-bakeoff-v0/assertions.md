# Assertions

## 已通过

| ID | 断言 | 状态 | 证据 |
|---|---|---|---|
| BE-A01 | 完成同题多路线对照，至少覆盖仓颉-only、李继刚-only、ReaderLab-current、组合路线 | pass | 五条路线均返回同一输出契约结果。 |
| BE-A02 | 至少一个组合路线证明不是并排贴字段 | pass | Combo-B 采用来源约束 -> 候选筛选 -> 受控表达，存在阻断关系。 |
| BE-A03 | 判断局部环节是否可抽离 | pass | 仓颉、李继刚、source-grounded 均标明上下游依赖。 |
| BE-A04 | 引入独立评估 worker | pass | 评估 worker 按 Meta Skill 方法输出排序、gate 和风险。 |
| BE-A05 | 主 Agent 给出最终取舍，不把 worker PASS 当完成 | pass | 主 Agent 仅将 Combo-B 判为候选主链。 |
| BE-A06 | 对《埃隆之书》关键风险点做源文抽查 | pass | 抽查 `v101-11/14/16/18/27/29.xhtml`。 |
| BE-A07 | 明确组合不等于生产通过 | pass | README、评估报告均声明缺 blind A/B、迁移测试和完整 source-grounded contract。 |
| BE-A08 | 不写 LifeAtlas 正式区、不改生成器、不新增依赖 | pass | 本轮只新增/更新 `docs/` 文档。 |

## 未通过 / 保留

| ID | 断言 | 状态 | 原因 |
|---|---|---|---|
| BE-R01 | Combo-B 通过 blind A/B | pending | 本轮只完成同题路线和评估，尚未做盲评包。 |
| BE-R02 | 第二类材料迁移测试 | pending | 本轮只用《埃隆之书》。 |
| BE-R03 | 完整 fresh source-grounded contract | pending | 本轮只有关键源文 spot-check，不是完整 contract。 |
| BE-R04 | ReaderLab 生成器机制化 | not_started | 本轮明确不改 `scripts/readerlab.py`。 |

## 剩余风险

- Combo-B 可能在换材料后失效。
- 李继刚式表达仍可能越界，需要来源门持续约束。
- 仓颉筛选可能偏向可能力化内容，低估读者理解路径。
- 目前的源文抽查是关键点抽查，不是全量证明。
