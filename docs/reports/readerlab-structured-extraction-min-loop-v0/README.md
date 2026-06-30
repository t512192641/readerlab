# ReaderLab Structured Extraction Min Loop v0

## 结论

本目录是 ReaderLab “结构化提炼最小闭环”的 repo 内手工重考报告。它完成的是一条可审查生产链的第一次闭合：

材料定性 -> 主问题 -> 候选池 -> 通过/降级/拒绝 -> 机制传导 -> 结构表达 -> 来源/边界。

本轮结论是：ReaderLab 当前最弱的一门课确实是结构化提炼。旧输出已经会摆出全书地图、章节路线、亮点和断言这些形状，但没有稳定证明它能从同一个主问题推导出部件功能、选点理由、降级边界和来源范围。

当前状态：repo 内手工评估与小范围重考样张，不是 product ready，不是生成器能力证明，不是正式 Skill，不是 fresh source-grounded contract。

## 文件

- `reader/01_结构化提炼小范围重考.md`：用《埃隆之书》重做全书主线、一个部件地图和 5 个亮点提炼。
- `audit/90_结构化提炼评估.md`：旧输出诊断、仿型能力矩阵、Meta Skill 裁判、主 Agent 取舍和新旧对比。
- `assertions.md`：本轮最小闭环断言与剩余风险。

## 输入证据

- `docs/reports/readerlab-fullbook-demo-v0/`
- `docs/reports/readerlab-elon-full-product-v1/`
- `docs/reports/readerlab-elon-fragment-capability-eval-v0/`
- `docs/reports/readerlab-elon-method-bakeoff-v0/`
- `docs/reports/readerlab-elon-full-product-v1/audit/candidate-evidence.v1.json`
- Meta Skill 方法：
  - `/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/references/skill-engineering-method.md`
  - `/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/references/output-eval-method.md`

## 主 Agent 取舍

本轮立即吸收：

- 李继刚式深读的定性逻辑：材料性质、缺口、增量/不增量、机制传导、认知旅程。
- 仓颉的筛选逻辑：候选池、通过/降级/拒绝、V1/V2/V3 式判断。
- source-grounded 的边界纪律：来源范围、位置精度、覆盖边界、人工待复核状态。
- ReaderLab 现有 reader/audit 分离和 LifeAtlas 包装底座。

本轮只做储备：

- 乔木共读：更适合片段深读与误读防护。
- book-to-skill：更适合能力化判断。
- blind A/B、provider-backed output eval、多材料扩测：等小范围链路稳定后再做。

本轮不吸收：

- 仓颉候选池页面外观。
- 李继刚式长篇论文形态。
- NotebookLM / Obsidian API / MinerU / markitdown / OCR 等工具链扩展。
- 把 Meta Skill、CTK、MEM 当作阅读输出仿型。

## 边界

本轮没有写 LifeAtlas `300/600/800`，没有改 `scripts/readerlab.py`，没有新增依赖，没有安装或启用任何 Skill。所有样张状态仍是人工 `pending`，后续若要机制化，必须先补 fresh source-grounded contract、人工 spot-check 和更强 output eval。
