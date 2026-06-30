# Dev State

## 产品目标

ReaderLab 把复杂材料转成中文可读、可批注、可讨论、可学习、可沉淀的 LifeAtlas 阅读包。材料包括电子书、长文、Markdown 文档、课程资料、访谈稿、代码文档、Skill 包和混合型资料。

当前产品形态应是复杂材料陪读 Skill / Agent 工作流，不是继续扩大的单体生成器脚本。Agent 负责理解、判断、路线和验收粘合；脚本负责重复、稳定、可检查的工具动作。

## 当前路线判断

上一阶段产出了多个 repo 内手工样张：

- 《埃隆之书》v0 / v1。
- 《埃隆之书》method bakeoff。
- 《埃隆之书》片段能力评测。
- `dbs-suite` capability v1。

这些产物有价值，但都不是 product ready，也不证明 ReaderLab 生成器稳定能力。它们暴露出的核心问题是：ReaderLab 不能继续按“仿型功能拼装”推进；必须改成“短板驱动能力学习”。

当前第一优先短板是 **结构化提炼能力**：全书地图、章节地图、重点/亮点提炼背后是同一套能力，不应拆成多个孤立功能。

已完成结构化提炼最小手工闭环，产物在 `docs/reports/readerlab-structured-extraction-min-loop-v0/`。它证明一条生产链方向值得继续：材料定性 -> 主问题 -> 候选池 -> 通过/降级/拒绝 -> 机制传导 -> 结构表达 -> 来源/边界。它仍不是 product ready、不是生成器能力、不是 fresh source-grounded contract。

已完成结构化提炼同题多路线对照，产物在 `docs/reports/readerlab-structured-extraction-bakeoff-v0/`。对照路线包括仓颉-only、李继刚-only、ReaderLab-current、Combo-A、Combo-B。主 Agent 判断：Combo-B 暂时胜出，作为下一轮候选主链；但这只是进入验证，不是生产通过。Combo-B 的顺序是 source-grounded 前置 -> 仓颉候选筛选 -> 李继刚式受控表达。

## 已作废或收窄的旧口径

- “参考项目真实吸收”不能再理解为列项目、贴字段、写 reference-to-implementation matrix 后就算吸收。
- “样张 PASS”只能表示 repo 内手工样张通过某轮审查，不表示人工阅读通过、生成器能力成立或正式 Skill 成立。
- 仓颉、李继刚、乔木、book-to-skill 等仿型不是要全部拼进 ReaderLab；它们只在对应短板上作为解题方法来源。
- 只抽某个仿型的一环不是天然可靠；必须先判断该环节是否依赖原方法上下游。如果强依赖，就不能模块式硬拼，只能整段吸收、延后吸收或登记为未来储备。
- 多个好环节拼在一起也不天然形成好系统；必须证明组合后有新增判断力、来源可靠性或读者收益。没有组合增益证据时，只能算并列参考，不能进入生产链。
- 组合增益必须通过同题多路线对照证明：仓颉-only、李继刚-only、ReaderLab 当前链路、组合路线分别处理同一材料，再由独立评审比较效果。若组合不胜出，必须选择最强单一路线作为主方法，其他仿型降级为辅助 gate、储备或不吸收。
- 本轮同题对照只证明 Combo-B 是下一轮候选主链。它仍必须通过 blind A/B、第二类材料迁移、完整 fresh source-grounded contract 和人工验收，才能进入机制化生产模板。
- 全书地图、章节地图、亮点提炼不再作为三项分散能力管理，统一归入结构化提炼。
- `yao-meta-skill`、CTK、MEM 仍只作为工程审查、调度和状态方法，不作为阅读输出仿型。

## 当前实现事实

- 仓库入口：`/Users/tianqiang/Documents/读书伴侣`。
- 生成脚本：`scripts/readerlab.py`。
- 单元测试：`tests/test_readerlab.py`。
- 当前正式生成器主要支持 Skill 包导入：`import-skills`。
- 图书/长文正式导入尚未进入生成器；《埃隆之书》相关产物均是 repo 内或 LifeAtlas demo/试产样张。
- 已实现 Obsidian `tandem-comments` 读取、定位和回复追加 CLI：`comments-list` / `comments-reply`。
- 当前目录不是 Git 仓库，不能用 `git status` 做变更边界确认；边界核对依赖写入路径、JSON 覆盖检查和 validate 输出。

## 关键产物状态

- `docs/reports/readerlab-elon-full-product-v0/`：历史整书实验产品，人工质量未通过，作为负面基线。
- `docs/reports/readerlab-elon-method-bakeoff-v0/`：四种方法独立输出，证明 v0 字段化吸收不足。现在作为能力学习证据库，不作为直接拼装清单。
- `docs/reports/readerlab-elon-full-product-v1/`：一篇主阅读稿 + 审计附录的手工样张。比 v0 收敛，但仍不是完整产品或生成器能力。
- `docs/reports/readerlab-elon-fragment-capability-eval-v0/`：片段级能力评测样张。证明片段深读与误读防护方向有价值，但不是全书 Top 选点证明，也不是正式 eval。
- `docs/reports/readerlab-dbs-suite-capability-v1/`：24/24 upstream `SKILL.md` 的 capability map 手工样张。证明能力地图方向有价值，但缺真实任务路由反测。
- `docs/reports/readerlab-structured-extraction-min-loop-v0/`：结构化提炼最小闭环手工重考。证明主问题、部件地图、亮点提炼可以共用一条判断链；仍缺 fresh source-grounded spot-check、人工验收、blind A/B 和机制化。
- `docs/reports/readerlab-structured-extraction-bakeoff-v0/`：结构化提炼同题多路线对照。证明局部仿型环节不能默认抽取，组合也不能默认胜出；当前推荐 Combo-B 作为候选主链，仍缺 blind A/B、第二类材料迁移测试、完整 source-grounded contract 和机制化。
- `docs/progress.md`：当前进度板。后续每轮大迭代必须更新。

## 当前能力模块状态

| 模块 | 状态 | 判断 |
|---|---|---|
| 来源真相与项目治理 | close | AGENTS、current-task、dev-state、decisions、ledger 已有基础规则；新增 progress 板。 |
| 材料导入与 Markdown 包 | working | Skill 包路径基本跑通，图书/长文正式导入未进入生成器。 |
| Obsidian 批注闭环 | working | 最小真实链路已验证，批注保护和产品化仍需继续。 |
| 来源审计 / location refs | working | 有 source/location 契约和样张，但 fresh source-grounded contract 仍不足。 |
| 结构化提炼 | working | 最小手工闭环和同题多路线对照已完成；Combo-B 暂定为候选主链。仍缺 blind A/B、第二类材料迁移测试、完整 source-grounded contract、人工验收和机制化。 |
| 片段深读与误读防护 | working | 片段样张方向通过，但还没有 blind A/B 或稳定生产链。 |
| 能力化判断 | working | book-to-skill 思路有帮助，但不能把全书强行 Skill 化。 |
| 产品组织与人工验收 | working-low | 产物仍像报告或样张，未形成完整用户阅读产品。 |
| 生成器机制化 / 正式 Skill | not_started | 不能把手工样张冒充机制化能力。 |

## 下一步

下一轮只做 Combo-B 轻量模板和迁移前验证：

1. 把 Combo-B 整理成轻量验证模板，不做字段拼装；模板必须说明输入、输出、上下游依赖、组合增益假设和质量门。
2. 用 5-8 个候选跑完整 gate，不扩写《埃隆之书》整书内容。
3. 做 Li-only / Cangjie-only / ReaderLab-current / Combo-B 的 blind A/B 或等价盲评包。
4. 用第二类材料做小范围迁移测试。
5. 明确哪些环节可沉入工具，哪些必须保留 Agent 判断。

## 重要约束

- 不新增依赖，除非用户明确批准。
- 不新建第二个 LifeAtlas `270_电子书与书籍资料` 目录。
- 不自动写入 LifeAtlas `300/600/800`。
- 不覆盖旧阅读包，不丢失真实 `tandem-comments` 批注。
- 不让 AI 替代人的第一次阅读判断。
- 不把 validator 绿灯当人工阅读质量通过。
- 不默认生成旁通视角、跨材料 RAG、联网搜索或正式 Skill。
- 不把手工 Demo 冒充正式生成器机制。
