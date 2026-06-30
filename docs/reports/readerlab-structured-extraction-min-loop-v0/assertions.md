# Assertions

## 本轮结构化提炼断言

| ID | 断言 | 状态 | 证据 |
|---|---|---|---|
| SE-A01 | 必须诊断旧输出在全书地图、章节/部件地图、亮点提炼上的共同失败原因。 | pass | `audit/90_结构化提炼评估.md` 的旧输出诊断和三个粒度表。 |
| SE-A02 | 必须建立结构化提炼仿型能力矩阵，列包含定性、筛选、排序、组织、边界、表达。 | pass | `audit/90_结构化提炼评估.md` 的矩阵。 |
| SE-A03 | 仓颉、李继刚式深读、source-grounded / NotebookLM 类、ReaderLab 现有能力必须进入矩阵。 | pass | 矩阵四行均覆盖。 |
| SE-A04 | 乔木和 book-to-skill 只在相关时作为补充，不默认拼入。 | pass | `README.md` 和审计文件均标为储备，不进入主链。 |
| SE-A05 | 必须引入 Meta Skill 做横向评估裁判，并覆盖边界、扫描过宽、字段存在风险、output risk、gate 和下一步改进。 | pass | `audit/90_结构化提炼评估.md` 的 Meta Skill 裁判和 Output Risk。 |
| SE-A06 | 必须抽出一条结构化提炼生产链。 | pass | `README.md` 和 `reader/01_结构化提炼小范围重考.md`。 |
| SE-A07 | 小范围重考必须产出全书主线、一个章节/部件地图、3-5 个亮点。 | pass | `reader/01_结构化提炼小范围重考.md` 产出全书主线、部件 II 地图和 5 个亮点。 |
| SE-A08 | 必须说明亮点为什么入选，为什么其他内容降级或拒绝。 | pass | 亮点章节和候选池均有入选、降级、拒绝理由。 |
| SE-A09 | 必须对比旧输出是否减少目录复述、说明缺口、解释传导、说明选点和边界。 | pass | `audit/90_结构化提炼评估.md` 的新旧对比表。 |
| SE-A10 | 不写 LifeAtlas 正式区，不新增依赖，不改 `scripts/readerlab.py`，不安装或启用 Skill。 | pass | 本轮只新增 `docs/reports/readerlab-structured-extraction-min-loop-v0/` 并更新项目状态文档。 |
| SE-A11 | 不能把样张 PASS 当 product ready 或生成器能力。 | pass | `README.md`、读者样张和 assertions 均明确边界。 |
| SE-A12 | 必须更新 `docs/progress.md`。 | pass | 本轮同步更新进度板。 |
| SE-A13 | 必须把“局部抽取仿型环节可能破坏上下游链路，且组合未必产生增益”登记为后续护栏。 | pass | `audit/90_结构化提炼评估.md` 新增局部抽取依赖与组合增益审查；`docs/decisions.md` 新增 D-038。 |
| SE-A14 | 必须把“组合增益要用同题多路线对照证明”登记为后续 gate。 | pass | `docs/decisions.md` 新增 D-039；`current-task` 和审计报告要求多 Agent 对照。 |

## 未解决风险

- 没有 fresh source-grounded contract；来源继承 v0/v1 heading/block/char refs。
- 没有人工逐段 spot-check。
- 没有 blind A/B 或 provider-backed output eval。
- 没有生成器机制化，也没有正式 Skill。
- 《埃隆之书》文明风险、AI、人口、监管、多行星等事实判断必须外部核验。
- 尚未完成李继刚/仓颉/source-grounded 局部环节的上下游依赖与组合增益实证审查；当前只能说手工重考中方向成立。
- 尚未做仓颉-only、李继刚-only、ReaderLab 当前链路、组合路线的同题多路线对照；下一轮必须用该对照决定倾向性方案。
