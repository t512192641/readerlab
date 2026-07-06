# Research Log

> Authority boundary: 本文件是研究记录和参考线索库，不是当前任务源。各条记录里的“下一轮 / 下一步”只代表当时研究语境；当前执行、读取范围和停止条件以 `docs/current-task.md` 为准。

## 2026-06-30 ReaderLab Skill 化参考调研

本条记录本轮对本地 Skill 包、GitHub 能力库存和外部公开项目的可复用结论。它是 ReaderLab 后续设计参考，不表示已实现。

### 拆书、提炼和深读流程

参考：

- `/Users/tianqiang/技能项目/skills-canonical/packages/cangjie-skill`
- `apple-ouyang/book-to-skill`
- `win4r/book-to-skill`
- `lijigang/ljg-skill-paper`
- `joeseesun/qiaomu-read-helper`

可借鉴模式：

- 先做 Stage 0 全局理解门，再进入地图、提炼或 Skill 化。
- 多视角抽取比单一摘要稳定：结构/框架、原则、案例/证据、反例/误用、术语/概念。
- 精华提炼必须有验证门：来源证据、跨段支撑、解释力、独特性、适用边界。
- 输出应有“缝合”：读者路线、认知增量、先读什么、读完能复述什么。
- 论文深读的“增量意识”可迁移到 ReaderLab：材料到底带来了什么新理解，而不是只复述内容。
- `book-to-skill` 类项目可借鉴主 Skill + 子 Skill、触发/边界、规模判断和真实场景自测；但 ReaderLab 不默认把每本书产成正式 Skill。
- `qiaomu-read-helper` 可借鉴按章节共读和批注响应，尤其是读者问题驱动的陪读方式。

不照抄：

- ReaderLab 不是默认把书变成正式 Skill。
- 不照抄 Claude/Swarm/Org-mode/Denote 等生态假设。
- 不把所有材料都套 RIA++；传记、论文、代码文档、Skill 包的提炼单元不同。

### 材料接入、解析和 source-grounded

参考：

- `/Users/tianqiang/技能项目/skills-canonical/packages/qiaomu-anything-to-notebooklm`
- `/Users/tianqiang/技能项目/skills-canonical/packages/anything-to-notebooklm`
- `microsoft/markitdown`
- `opendatalab/MinerU`
- `rednote-hilab/dots.ocr`
- `ocrmypdf/OCRmyPDF`
- `lijigang/ljg-skill-fetch`
- `PleasePrompto/notebooklm-skill`

可借鉴模式：

- 多源材料先标准化成可审计 source，而不是直接生成上层总结。
- 解析结果必须保留结构和定位：EPUB spine、PDF page/block、heading path、char range、asset paths。
- 每个地图、提炼和导读都必须绑定 `source_scope`，明确是目录级、局部正文还是完整正文。
- NotebookLM 类 source-grounded 思路可借鉴：高层回答必须能追溯到上传/解析材料，但 ReaderLab 仍需自己的来源、置信度和待复核契约。
- 解析器应走 strategy ladder：轻量解析优先，复杂 PDF 再考虑 MinerU 这类重解析器；不默认新增重依赖。
- OCR 和重解析只用于复杂 PDF、扫描件、版面强依赖材料；默认路径仍应是轻量解析和可复核 source registry。
- Obsidian / NotebookLM / llm-wiki 只作为来源可追溯、共读和知识沉淀参考，不默认接入 ReaderLab 工作流。

关键设计：

- `catalog_map`：允许基于目录、章节标题、前言和元信息生成，只能称为结构地图/阅读路线假设。
- `grounded_global_map`：只有覆盖完整正文或明确覆盖范围后生成；每个判断必须有来源范围和覆盖率。

### Skill / Agent workflow 形态

参考：

- Anthropic Skills / Agent Skills specification
- `/Users/tianqiang/技能项目/skills-canonical/packages/codex-task-kit-skills`
- `/Users/tianqiang/技能项目/skills-canonical/packages/mem-kit`
- `/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite`
- `obra/superpowers`
- `yaojingang/yao-meta-skill`
- `agentskills/agentskills`
- `joeseesun/qiaomu-meta-skill`
- `muratcankoylan/Agent-Skills-for-Context-Engineering`
- `vercel-labs/skills`

可借鉴模式：

- `SKILL.md` 应保持瘦，只做触发和总流程；复杂说明放 `references/`，确定性动作放 `scripts/`，证据放 `reports/`。
- 顶层入口只路由，不直接塞满复杂业务逻辑。
- 机器 validate、Agent 自评、人工阅读验收必须分层。
- Skill 包能力地图不能平铺目录；它要回答“遇到什么问题用哪个 Skill、为什么、产出是什么、怎么验收”。
- Skill 工程化必须补 Skill IR、trigger eval、output eval、治理、可移植性和真实输出验证；不能只写漂亮说明。

对 `dbs-suite` 的直接结论：

- 需要 `capability-map.v1`，字段应覆盖能力域、触发信号、方法原子、输入、输出契约、验收方式、读者路线和 Skill 间路由关系。

### yao-meta-skill 对 ReaderLab 的作用

参考：

- `/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/SKILL.md`
- `references/skill-engineering-method.md`
- `references/skill-ir-method.md`
- `references/output-eval-method.md`

结论：

- `yao-meta-skill` 不负责读书；它负责把 ReaderLab 这个流程工程化成可复用、可评估、可治理的 Skill。
- ReaderLab 应先产出 Skill IR v0，再决定文件结构和脚本拆分。
- ReaderLab 应建立 output eval v0，用 baseline vs with-skill 证明样张质量提升。
- output eval 断言应抓真实质量问题，而不是只检查措辞：来源范围、覆盖率、不得假装全书读完、结构解释、精华 source refs、反例/边界、读者路线和人工待复核状态。

### GitHub 能力库复查结果

2026-06-30 复查后，GitHub 能力库 `/api/recommend` 已恢复，三类正式查询均返回 `health_status=ok`。不要继续把它写成当前故障。

正式推荐结果：

- 拆书/深读：5 个 formal 结果。
  - `apple-ouyang/book-to-skill`，fit 0.85
  - `lijigang/ljg-skill-paper`，fit 0.85
  - `kangarooking/cangjie-skill`，fit 0.82
  - `win4r/book-to-skill`，fit 0.8
  - `joeseesun/qiaomu-read-helper`，fit 0.55
- Skill 工程化：5 个 formal 结果。
  - `yaojingang/yao-meta-skill`，fit 0.85
  - `agentskills/agentskills`，fit 0.82
  - `joeseesun/qiaomu-meta-skill`，fit 0.82
  - `muratcankoylan/Agent-Skills-for-Context-Engineering`，fit 0.72
  - `vercel-labs/skills`，fit 0.7
- 材料解析：5 个 formal 结果。
  - `microsoft/markitdown`，fit 0.95
  - `opendatalab/MinerU`，fit 0.95
  - `rednote-hilab/dots.ocr`，fit 0.92
  - `ocrmypdf/OCRmyPDF`，fit 0.55
  - `lijigang/ljg-skill-fetch`，fit 0.55

SQLite 线索不是正式推荐链路强结果，`review_status` 全部 pending，只能参考设计，不能自动启用：

- NotebookLM：`win4r/notebooklm-py`、`PleasePrompto/notebooklm-skill`、`teng-lin/notebooklm-py`
- Obsidian：`coddingtonbear/obsidian-local-rest-api`、`AgriciDaniel/claude-obsidian`
- llm-wiki：`vanillaflava/llm-wiki-skills`、`staruhub/ClaudeSkills llm-wiki`

边界：这些结果只更新 ReaderLab 的设计参考，不表示已安装、启用、拉取、接入或验证任何外部资产。下一轮 IR/eval 必须逐项写清“借什么 / 不借什么 / 翻译成 ReaderLab 的设计是什么”。

## 2026-06-30 参考基准进入 ReaderLab IR 的转译结果

本轮把上一条研究记录中的参考基准正式转译进 `docs/readerlab-skill-ir-v0.md` 的 reference translation matrix。每个基准都写明了“借什么 / 不借什么 / 翻译成 ReaderLab 的设计是什么”。

关键结论：

- 拆书/深读类参考进入 ReaderLab 的 Stage 0 全局理解门、多视角提炼、来源边界、适用边界和读者路线；没有进入“默认把书产成正式 Skill”的目标。
- 材料解析/source-grounded 类参考进入 `source-registry.v1`、`location-map.v1`、轻量解析优先和重解析/OCR approval gate；没有进入默认新增依赖或外部工具接入。
- NotebookLM、Obsidian、llm-wiki 库存线索只转成 source refs、location refs、批注和知识沉淀边界；没有默认启用任何集成。
- Skill 工程化类参考进入 Skill IR、output eval、output risk、trigger/near-neighbor、thin `SKILL.md` 和资源分层；没有进入治理、发布、registry 或多平台 adapter 的全量机制。

对应产物：

- `docs/readerlab-skill-ir-v0.md`
- `docs/readerlab-output-eval-v0.md`
- `docs/contracts/readerlab-contracts-v0.md`

## 2026-06-30 参考吸收不足的反测结论

本条记录来自 fullbook demo 的 Meta Skill / 仓颉方法补审。结论是：参考项目已经进入设计文档，但还没有充分进入 ReaderLab 的实际输出能力。

反测发现：

- `cangjie-skill` 的多视角深读、案例、反例、术语、可迁移洞察和 V1/V2/V3 验证没有充分进入《埃隆之书》读者页；当前“6 个收获”仍像短摘要。
- `book-to-skill` 类项目强调的读者可走完认知路线还没有落实成稳定页面结构；全书级主线和章节/部分级深读之间的衔接不够。
- source-grounded / NotebookLM 类思路只落实到 spine 级 refs，尚未达到高价值判断对应 heading / block / char refs 的可复核程度。
- `yao-meta-skill` 已用于 IR 和 review gate，但它不是阅读输出仿型参考；下一轮只用它校准 Skill 级 output eval、risk 和 gate，不把它当作内容能力来源。
- CTK/MEM 已进入调度和状态维护模式，但它们不是 ReaderLab 产品能力的仿型参考；下一轮只用它们约束“开发 worker + 对抗审查 worker + 主 Agent 验收”的协作纪律。

下一轮研究/吸收要求：

- 先复查现有 research log、GitHub 能力库 formal 结果、本地 canonical Skill 包，以及可用 prompt/方法资产；同时区分“阅读/来源/Skill 形态仿型参考”和“工程审查/项目协作方法”。
- 必须产出 reference-to-implementation matrix，而不是新增候选清单。每条记录至少包含：参考来源、借鉴设计、不借内容、ReaderLab 落点、要改的产物或 gate、预期改善、验证方法。
- 只选最高杠杆的 3-5 个吸收点进入实现，避免把下一轮做成大而散的二次调研。
- 吸收结果必须用《埃隆之书》和 `dbs-suite` 样张反测：能抓到旧样张问题，能解释新样张哪里明显变好，仍不能把人工状态改成 accepted。

## 2026-06-30 本地 GitHub 能力库补查

用户指出下一轮不应把候选范围圈死，也不应漏掉之前调研过的李继刚等 Skill。本轮用本地 GitHub capability recommend 做了三组补查，服务返回 `health_status=ok`。

补查结果：

- 复杂材料陪读 / 全书深读 / 精华提炼 / 来源可追溯：
  - `lijigang/ljg-skill-paper`，fit 0.65。强相关点是论文深读的原子管线、认知旅程、缺口、增量、机制和可复核结论；虽然偏论文，不是全书陪读，但对 ReaderLab 的“深读不浅化”很有价值。
  - `mli/paper-reading`，fit 0.55。可作为逐段精读表达参考，但领域偏深度学习论文，暂列弱参考。
  - `joeseesun/qiaomu-anything-to-notebooklm`，fit 0.50。对多源中文长内容整理和 NotebookLM 素材化有参考价值，核心不是深读本身。
- source-grounded Markdown / reading package / location refs：
  - `opendatalab/MinerU`，fit 0.78。复杂 PDF / Office 解析强相关，但需安装部署；当前只能作为设计参考，不新增依赖。
  - `microsoft/markitdown`，fit 0.55。适合作为轻量格式转换参考，但不足以单独解决 location refs / citations。
  - `win4r/book-to-skill`，fit 0.55。对技术书 PDF 到 Skill 的路线有参考价值，但不能照搬 Claude Code Skill 输出目标。
- Agent Skill engineering / output eval / trigger eval：
  - `muratcankoylan/Agent-Skills-for-Context-Engineering`，fit 0.72。
  - `warpdotdev/oz-skills`，fit 0.72。
  - `agentskills/agentskills`，fit 0.72。
  - `joeseesun/qiaomu-meta-skill`，fit 0.62。
  - `affaan-m/ECC`，fit 0.55。

执行结论：

- 下一轮不能只围绕 prompt 中点名的少数项目做矩阵。必须从 `docs/research-log.md`、GitHub 能力库正式结果、SQLite pending 线索、本地 canonical Skill 包和 prompt/container/repo card 中重新筛选。
- `lijigang/ljg-skill-paper` 不应被弱化。它虽然不是图书项目，但其“缺口/增量/机制/认知旅程”应进入 ReaderLab 深读质量 gate。
- `lijigang/ljg-skill-fetch`、乔木 NotebookLM、Obsidian、llm-wiki 等线索必须至少进入“检查并说明是否采用/放弃”的矩阵，不允许因为当前 prompt 没列全就漏掉。
- 若现有资产不足以解决 ReaderLab 原始目标，下一轮可以继续扩展本地能力库查询或直接搜索 GitHub；但仍不安装、不启用、不新增依赖。

## 2026-06-30 Reference-to-implementation matrix 落地复查

本轮按用户边界只读复查现有资产，不联网、不安装、不启用、不新增依赖。已读项目真相层、`yao-meta-skill` 三个方法文件、研究日志、`cangjie-skill` 方法文件、乔木 NotebookLM 本地化 Skill、Obsidian Markdown Skill 和本地 GitHub 能力库记录。

复查结论：

- 现有资产足够支撑本轮能力补强，不需要联网扩展。
- `cangjie-skill` 有本地方法证据：Stage 0 整书理解、并行抽取、V1/V2/V3 三重验证，直接转成 `local-deepread.v1.deepread_cards` 和 ELON-A08/A09/A13。
- `lijigang/ljg-skill-paper` 没有本地包，但研究日志和能力库记录已足够确认其“缺口/增量/机制/认知旅程”价值，转成深读质量 gate；不把论文模板照搬为 ReaderLab schema。
- `apple-ouyang/book-to-skill`、`win4r/book-to-skill` 作为能力库/研究日志证据足够；本轮只借路线、边界和规模深度门，不做书到 Skill 包装。
- `qiaomu-read-helper` 只借章节共读和批注响应思路；当前不接入额外工具链。
- `qiaomu-anything-to-notebooklm` 与 `anything-to-notebooklm` 已有本地包；只借多源素材标准化、来源 URL/标题/作者/时间/抽取文本保留，不接 NotebookLM CLI、MCP、Playwright 或 paywall fallback。
- `lijigang/ljg-skill-fetch` 作为来源可追溯线索进入 `source-registry.v1` / `location-map.v1` 精度门；不把抓取当理解。
- `markitdown`、`MinerU`、OCR 类项目只保留 strategy ladder：轻量解析优先，复杂 PDF/扫描件才申请重解析；本轮不接入依赖。
- NotebookLM / Obsidian / llm-wiki 线索分别进入 source-grounded 纪律、Markdown/批注表面、人工升格边界；不上传、不接 API、不整理 vault、不自动升格知识库。
- Agent Skills 形态项目只影响瘦入口、resources/scripts/reports 分层、output eval 和 demo/capability/product-ready gate；不做 adapter、registry、UI 或安装。
- Meta Skill 只作为工程审查方法；CTK/MEM 只作为项目协作方法，不进入阅读输出仿型参考。

本轮落地产物：

- `docs/readerlab-skill-ir-v0.md`：新增 reference-to-implementation matrix，逐项写清借什么、不借什么、ReaderLab 落点、预期改善、反测方式、采用/放弃状态和原因。
- `docs/contracts/readerlab-contracts-v0.md`：补 `local-deepread.v1.deepread_cards`、V1/V2/V3 验证、source/location 精度门、reader-facing/internal-audit 分离、`capability-map.v1.route_decisions` 和 `coverage_plan`。
- `docs/readerlab-output-eval-v0.md`：补 ELON-A08 到 ELON-A13、DBS-A08 到 DBS-A11，以及下一轮样张避免路径。

仍未采用的强相关候选及原因：

- `MinerU`、`dots.ocr`、`OCRmyPDF`：强相关于复杂 PDF/扫描件，但当前样张是 EPUB 和 Skill 包，接入会新增依赖；仅保留设计门。
- `markitdown`：适合作轻量转换，但不能单独解决来源精度和阅读质量；仅记录 extraction method 方向。
- NotebookLM / Obsidian API / llm-wiki 集成：会引入服务、插件、vault 或升格边界，不符合本轮“不新增依赖、不启用、不写正式沉淀区”。
- `anything-to-notebooklm`：与乔木本地化版本重叠，本轮不单独吸收。
- Agent Skills adapter / registry / UI 项目：对未来包装有价值，但当前先做 IR、契约和 output eval，不进入实现。
