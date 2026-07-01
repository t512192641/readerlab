# ReaderLab Skill IR v0

> Authority boundary: 本文件是 Skill IR 草案，不是当前任务源，也不表示已包装、安装或发布。当前执行以 `docs/current-task.md` 为准。

## 状态

- IR 状态：`draft-v0`
- 负责人：ReaderLab 项目
- 成熟度：薄骨架，可供样张重做 worker 使用；尚不能包装、安装或发布为正式 Skill
- 方法来源：`/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/references/skill-ir-method.md`、`output-eval-method.md`、`skill-engineering-method.md`
- 边界：本 IR 把 ReaderLab 定义为可复用的复杂材料陪读工作流；不安装 Skill，不修改全局 Codex 状态，不替代项目规则。

## Recurring job

ReaderLab 负责的重复任务是：把复杂材料转成中文可读、来源可追溯、可批注、可复核的 LifeAtlas 阅读包。

材料包括书籍、长文、Markdown 文档、课程资料、访谈稿、代码文档、Skill 包和混合材料。ReaderLab 的核心承诺不是“生成摘要”，而是提供一个阅读工作流：人能理解材料、在正文附近批注，Codex 能基于本地来源上下文回应。

## 触发描述草案

当用户要把复杂材料转换、重建、评估或改进为 LifeAtlas / Obsidian 阅读包，并且需要来源引用、阅读路线、地图、提炼、批注保护和人工验收边界时，使用 ReaderLab。适用于书籍、长文、Skill 包、代码文档和混合材料。不用于一次性摘要、普通翻译、无关写作、正式 LifeAtlas `300/600/800` 沉淀、全局 Skill 安装或外部工具接入。

## 应触发

- 用户要求导入、重建、验证或改进 ReaderLab 阅读包。
- 任务涉及 source-grounded 阅读地图、目录地图、全局地图、能力地图、提炼或批注保护。
- 输入材料复杂，需要先理解结构再生成读者 Markdown。
- 用户要求判断旧 ReaderLab 产物是否足够适合人工阅读。
- 用户要求围绕 ReaderLab 页面附近批注做回复。
- 任务需要区分机器完成和人工验收。

## 不应触发

- 没有阅读包、来源地图或批注需求的短翻译、改写、总结。
- 不需要来源覆盖率、位置引用或 ReaderLab 状态的普通读书笔记。
- 安装、启用或发布全局 Codex Skills。
- 写入 LifeAtlas `300/600/800` 正式沉淀区。
- 未经明确批准克隆、更新或修改 upstream / canonical source package。
- 用户只要求 ReaderLab 包工作时，不应顺手搭新 UI、数据库、RAG 系统或批注系统。

## Near-neighbor 边界

| 相邻能力 | 为什么容易混淆 | ReaderLab 边界 |
|---|---|---|
| 通用总结器 | 都会压缩长材料 | ReaderLab 必须保留来源范围、位置引用、覆盖率、读者路线和人工状态。 |
| book-to-skill | 都会提炼可复用原则 | ReaderLab 可以产出候选，不默认创建正式 Skill。 |
| PDF/OCR 管线 | 都会解析来源文档 | ReaderLab 把解析作为 source preparation；解析结果不是最终理解。 |
| Obsidian 知识管理 | 都写 Markdown | ReaderLab 产出 source-grounded 阅读包和批注上下文，不默认整理整个 vault。 |
| NotebookLM 式 source QA | 都强调来源 | ReaderLab 使用本地契约和 LifeAtlas 状态，不默认接入外部工具。 |
| CTK/MEM | 都提供工作流和状态纪律 | CTK/MEM 管任务和记忆，ReaderLab 管复杂材料阅读产物。 |

## 工作流

1. 输入和边界检查
   - 确认材料类型、输入路径、目标包路径、破坏性风险，以及当前任务是设计、生成、评估还是批注回复。
   - 遇到凭证、付费服务、依赖、source package 改动、全局 Skill 状态、生产类数据或 LifeAtlas `300/600/800` 写入时暂停并征求明确批准。
2. 来源审计
   - 读取或生成 `source-registry.v1`。
   - 记录来源文件、抽取方法、hash、解析置信度和来源所有权边界。
3. 位置地图
   - 读取或生成 `location-map.v1`。
   - 记录 spine/page/heading/block/char range，让地图、提炼和批注能指回来源。
4. 材料分类和深度门
   - 判断材料是书、长文、Skill 包、代码文档、课程/访谈还是混合材料。
   - 判断当前覆盖率支持 `catalog-map`、`grounded-global-map`、`capability-map`、局部深读，还是只能输出来源诊断。
5. 阅读包规划
   - 定义 reading units 和 reader route。
   - 读者页服务材料主线；完整来源、命令噪音、hash 和审计证据进入契约或附录。
6. 地图和提炼
   - 书籍/长文：只有目录、元信息或局部章节时生成 `catalog-map.v1`；只有完整正文覆盖后才生成 `grounded-global-map.v1`。
   - Skill 包：生成 `capability-map.v1`，不能伪装成图书全书地图。
   - 提炼项在绑定来源、边界和人工状态前只算候选。
7. 批注处理
   - 保护已有 `tandem-comments`。
   - Codex 回复必须使用附近来源上下文，不能覆盖或搬迁用户批注。
8. 验证与评估
   - 跑结构检查、契约检查和包状态检查。
   - 用 output eval case 比较 baseline 和 ReaderLab-guided 输出。
   - 机器状态和人工验收分开。
9. 交接
   - 记录改动文件、生成路径、验证证据、待复核项和下一步 worker 任务。

## Agent / 脚本边界

| 领域 | Agent 判断 | 脚本/工具层 |
|---|---|---|
| 材料类型和路线 | 判断阅读形态、处理深度和地图类型。 | 识别文件类型和包结构。 |
| 来源覆盖 | 判断覆盖率是否足以支持主张。 | 统计文件、字符、页、标题、块、hash、抽取状态。 |
| 位置引用 | 选择哪些位置能支撑某个判断。 | 抽取 spine/page/heading/block/char range 并校验引用格式。 |
| 读者路线 | 设计第一次阅读路线和局部深读路线。 | 把路线字段写入 manifest / contract。 |
| 全局地图 | 解释主线、关系、核心问题和不确定性。 | 校验必填字段和 source refs。 |
| 能力地图 | 识别能力域、触发、方法原子、输出和验证。 | 扫描 Skill 文件、manifest、脚本和支持材料。 |
| 精华提炼 | 选择框架、原则、案例、反例、术语和可迁移洞察。 | 检查每项是否有 source refs、置信度和 review status。 |
| 批注回复 | 理解用户批注和附近上下文。 | 定位批注、保护 fenced data、安全追加回复。 |
| 质量判断 | 判断是否真实可读、诚实、有帮助。 | 跑测试、schema 校验、禁用声明和缺失引用检查。 |

本阶段不能继续把全书地图、能力地图或提炼模板塞进 `scripts/readerlab.py`。只有稳定、低判断含量、失败模式清楚的检查，后续才适合沉入脚本。

## 资源、脚本、报告和契约

- 当前入口脚本：`scripts/readerlab.py`
  - 继续作为 v0.1 工具层，承载现有 import、validate、comment 命令。
  - 本阶段不扩写地图生成模板。
- 当前测试：`tests/test_readerlab.py`
- 既有契约：
  - `docs/contracts/global-map.v1.schema.json`
  - `docs/contracts/distillation.v1.schema.json`
- 新设计契约：
  - `docs/contracts/readerlab-contracts-v0.md`
- Output eval 方案：
  - `docs/readerlab-output-eval-v0.md`
- 未来 ReaderLab Skill 包建议形态：
  - `SKILL.md`：只放瘦入口、触发和总流程。
  - `references/`：阅读方法、契约语义、source-grounding、批注、地图和提炼规则。
  - `scripts/`：source scan、location extraction、contract validate、comment locate/reply、稳定后的 output eval runner。
  - `reports/`：output risk、eval scorecard、blind review pack、validation logs。

## Reference-to-implementation matrix

本矩阵是本轮能力补强的执行矩阵，不是候选清单。采用状态只表示进入 ReaderLab v0 设计和下一轮样张反测；所有人工状态仍保持 `pending`。

| 参考来源 | 借什么 | 不借什么 | ReaderLab 落点 | 预期改善 | 《埃隆之书》或 `dbs-suite` 反测 | 状态和原因 |
|---|---|---|---|---|---|---|
| `kangarooking/cangjie-skill` | Stage 0 整体理解、5 类并行抽取、案例/反例/术语、V1/V2/V3 三重验证。 | 默认把书产成正式 Skill；不照搬 RIA-TV++ 文件树。 | `local-deepread.v1.deepread_cards`、`verification.v1_cross_context/v2_predictive/v3_distinctive`、ELON 新断言。 | 防止“6 个收获”退化成短摘要。 | Elon 局部深读必须有框架/原则/案例/反例/术语/可迁移洞察卡，并说明未通过验证的候选。 | 采用；最高杠杆阅读质量补强。 |
| `lijigang/ljg-skill-paper` | 缺口、增量、机制、认知旅程和可复核结论意识。 | 论文模板、审稿长文和领域特定 schema。 | `local-deepread.v1.reading_thesis` 增加 `reader_gain`、`mechanism_chain`、`open_questions`；output eval 检查“主线太浅”。 | 深读从复述转为解释材料带来的新增理解。 | Elon 读者页必须回答这一部分改变了读者对马斯克工作方式的什么理解；DBS 能力地图必须说明每个能力域解决的缺口。 | 采用；用作深度 gate，不作输出模板。 |
| `apple-ouyang/book-to-skill` | 主 Skill + 子 Skill 的认知路线、触发/边界和读者可走完路径。 | Claude/Skill 包装目标；自动 Skill 化。 | 工作流“阅读包规划”；`catalog-map.v1.route_hypothesis`、`reader_routes`、near-neighbor exclusion。 | 防止目录冒充阅读路线。 | Elon catalog 必须区分全书路线假设和已覆盖部件；DBS reader route 必须说明先读、选择、验证。 | 采用；只借路线/边界。 |
| `win4r/book-to-skill` | 按材料规模和格式决定处理深度。 | 所有书籍同一深度、同一输出结构。 | 工作流“材料分类和深度门”；`source_scope.coverage_status` 驱动 catalog/global/local/capability 分流。 | 低覆盖不再被包装成全书理解。 | Elon TOC-only 只能生成 catalog；full spine 仍不能自动等于精选译文正文完成。 | 采用；作为 coverage gate。 |
| `joeseesun/qiaomu-read-helper` | 章节共读、读者问题驱动、批注响应。 | 绑定乔木工具链或新增阅读系统。 | `reader_routes` 和批注处理阶段；worker 任务要求读者页附近可批注。 | 阅读包更像陪读路径，不是报告。 | Elon/DBS 读者页必须给“先读什么、在哪里批注、批注后问什么”的路线；不改变插件。 | 部分采用；当前只落 ReaderLab Markdown + `tandem-comments` 表面。 |
| `qiaomu-anything-to-notebooklm` | 多源材料先标准化、保留 URL/标题/作者/抓取时间/抽取文本，再进入问答或报告。 | NotebookLM CLI、MCP、Playwright、paywall fallback、安装流程。 | `source-registry.v1.sources[].source_role/trust_notes/review_items`；source prep strategy ladder。 | 多源来源边界清楚，不把加工文本当原文。 | Elon/DBS source registry 必须说明原始来源、抽取方法和不完整风险。 | 采用设计，不接入工具；符合不新增依赖。 |
| `anything-to-notebooklm` | 上游多源素材化的一般路径。 | 与 LifeAtlas 本地化冲突的安装和 MCP 假设。 | 与上一行合并到 source prep 边界；不单独建 ReaderLab 功能。 | 避免重复吸收同类项目。 | 反测只检查 source registry，不检查 NotebookLM artifact。 | 放弃单独采用；乔木本地化版本已足够。 |
| `lijigang/ljg-skill-fetch` | 来源、范围、获取路径和可复查事实。 | 无边界拼接素材或把抓取当理解。 | `source-registry.v1` 精度门；`unresolved_source_issues` 和 hash/extraction scope。 | 精华/地图能追到具体来源。 | Elon 高价值主张不能只指向包级或 spine；DBS 能力域必须指向 `SKILL.md`/references/scripts/tests。 | 采用；作为 source/location refs 底座。 |
| `microsoft/markitdown` | 轻量解析优先、格式转换作为 source prep。 | 把 Markdown 转换结果当最终阅读输出。 | 脚本边界：未来可做 parser 候选，但本轮只记录 `extraction_method`。 | 防止解析器过度上升为产品能力。 | 样张只检查 extraction method 和 confidence，不要求运行 markitdown。 | 部分采用；不安装、不运行。 |
| `opendatalab/MinerU` | 复杂 PDF/版面/块级解析的能力边界。 | 默认部署重解析/OCR。 | strategy ladder 和 `location-map.v1.precision_level`；复杂文档进入 approval gate。 | 为未来复杂 PDF 保留块级 refs 方向。 | 当前 Elon EPUB/DBS Markdown 不需要 MinerU；反测检查未错误引入重依赖。 | 设计参考；本轮放弃接入，因为需新增依赖。 |
| NotebookLM 线索 | source-grounded 回答必须回到已登记来源。 | 上传、API、NotebookLM artifact 作为 ReaderLab 默认路径。 | `claim_refs.primary_location_refs`、`location_precision_required`、output eval source precision assertions。 | 高层判断不再只有 spine 级引用。 | Elon 精华必须使用 heading/block/char 级 refs；DBS 能力判断必须回到包内文件位置。 | 采用 source-grounded 纪律，不接入服务。 |
| Obsidian 线索 | Markdown/链接/block id/callout 等 vault-native 阅读表面。 | Obsidian CLI、REST API、vault 整理或新插件依赖。 | 展示层规则：读者页只放阅读主线；审计字段进入 report/appendix。 | 批注体验更干净，内部审计不污染正文。 | Elon fullbook 读者页不得把 pending、spine audit、未写 LifeAtlas 等机器审计混入主阅读段。 | 部分采用；只保留 Markdown 表面和批注兼容。 |
| llm-wiki 线索 | 知识沉淀要有 source refs 和人工确认。 | 自动升格到 wiki 或 LifeAtlas 正式区。 | `human_status=pending`、后续 LifeAtlas 升格 gate。 | 防止候选洞察直接变成知识库结论。 | Elon/DBS 中所有 insight/skill 化候选保持 pending。 | 采用为升格边界；不做集成。 |
| Agent Skills 形态项目：`agentskills/agentskills`、`muratcankoylan/Agent-Skills-for-Context-Engineering`、`vercel-labs/skills` | 瘦入口、resources/scripts/reports 分层、routeable capability、output eval。 | adapter、registry、前端包装和发布机制。 | 未来 Skill 包形态；demo/capability/product-ready 三层 gate；worker report 模板。 | 防止 demo 绿灯被说成产品 ready。 | DBS capability map 要有 route/exclusion；主 Agent 验收必须分三层结论。 | 采用工程形态；不包装、不安装。 |
| `yao-meta-skill` | IR、output eval、risk、gate 方法。 | 阅读输出仿型参考、内容模板、安装治理。 | 本 IR/eval/contracts 的方法来源；审查 worker 的 gate 口径。 | 让能力补强可评估。 | 只用于审查是否 baseline vs with-ReaderLab 有提升。 | 采用为工程审查方法，不进入阅读内容吸收清单。 |

## 本轮最高杠杆吸收点

1. `local-deepread.v1` 增加深读卡：框架、原则、案例、反例、术语、可迁移洞察都必须有 item-level refs、适用边界和 V1/V2/V3 验证状态。
2. 增加 source/location refs 精度门：高价值主张优先使用 heading/block/char refs；只有确无更窄位置时才允许 spine/page 级引用，并写明原因。
3. 分离 reader-facing 与 internal-audit：读者页只承载阅读主线、路线、局部正文和必要旁批；coverage、hash、pending、validator 证据进入 README/report/appendix。
4. `capability-map.v1` 强化 route/exclusion：能力域必须说明触发信号、不要触发的近邻、跨 Skill 路由和验收方法，不能是目录清单。
5. 建立 demo / Skill capability / product-ready 三层 gate：validator 或 repo demo 通过只到 demo gate；Skill capability 需要 output eval 正向差异；product-ready 需要人工阅读复核。

## Output risk profile

| 风险 | 失败形态 | 防线 |
|---|---|---|
| 低覆盖冒充全覆盖 | TOC 或一个部件被写成“全书地图”。 | `catalog-map.v1` 和 `grounded-global-map.v1` 分开；全书地图必须有覆盖字段。 |
| 目录冒充洞察 | 章节列表被标成全局理解。 | eval 检查关系、核心问题和有来源支撑的主线。 |
| Skill 包能力地图退化成目录 | 只列文件或 Skill。 | `capability-map.v1` 必须有触发信号、方法原子、输出契约、验收和读者路线。 |
| 精华无来源 | “精华”没有 source refs 或适用边界。 | 提炼项必须有位置引用、置信度和 review status。 |
| 机器绿灯冒充人工验收 | validate 通过被写成质量通过。 | 所有契约都有 `machine_status` 和 `human_status`。 |
| 解析器过度使用 | OCR/重解析被当默认方案。 | strategy ladder：轻量解析优先，依赖和重解析需批准。 |
| 工具链绑定 | NotebookLM/Obsidian/Skill 生态变成隐藏依赖。 | IR 只借设计模式，不默认集成。 |
| 上下文膨胀 | `SKILL.md` 变成长手册。 | 瘦入口，细节进 `references/`、`scripts/`、`reports/`、contracts。 |

## Eval 计划

Output eval v0 定义在 `docs/readerlab-output-eval-v0.md`。有效 v0 必须证明 ReaderLab-guided 输出能抓住旧 baseline 的真实失败：

- 低覆盖不能声称全书理解；
- 地图必须包含 source scope、coverage、confidence、review items 和 human status；
- `dbs-suite` 必须用 capability map，不能硬套图书 global map；
- 提炼和亮点不能无来源、无边界；
- validate 或文件存在不能等同人工阅读质量通过。

## Trust boundary

ReaderLab 可以在用户明确任务范围内读写项目文档和允许的 ReaderLab 试产包产物。它不能修改 canonical source package、安装或启用 Skills、新增依赖、写入 LifeAtlas `300/600/800`，也不能在没有明确批准和批注保护检查时覆盖带批注的包。

## Reviewer gate

评审者应能回答：

1. ReaderLab 负责复杂材料陪读包，不负责通用摘要或 Skill 安装。
2. 它触发于 source-grounded 阅读包、地图、提炼、评估、批注和 validate 任务。
3. 它不触发于一次性摘要、正式 LifeAtlas 沉淀、全局 Skill 安装或未经批准的外部集成。
4. 真实行为由 ReaderLab 契约、source/location registry、package manifest、现有工具脚本和未来瘦 Skill 包资产承载。
5. Output eval v0 和 contract check 证明结果是否诚实、可追溯、比 baseline 更好。
6. 当前目标仅是本地 Codex / ReaderLab 工作流；平台包装明确后移。
