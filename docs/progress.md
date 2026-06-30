# ReaderLab Progress

## 口径

本文件记录 ReaderLab 离最终产品目标的距离。当前已完成一次方向重设：产品主线从旧的局部结构化提炼任务，调整为“复杂材料吸收系统 / 正文优先陪读包 / E-R-D-D 阅读智能链 / contract-first 开发”。

分数不是产品质量证明，只是工程管理估算。validator 通过、样张存在、文档齐全都不能自动证明 product ready。

最终目标：ReaderLab 能稳定把复杂材料转成中文可读、可批注、可讨论、可学习、可沉淀的 LifeAtlas 正文优先陪读包，并能证明输出不是空泛摘要。

## 当前总进度

当前估算：**69 / 100**

这次不是简单加分，而是重设口径。旧进度 48/100 建立在“结构化提炼是当前第一短板”的任务框架上；外部强模型建议进入后，产品范围被重新拉回到更高层：产品形态、事实契约、AI 深读、技术洞察、验收机制和生成器机制化。

本轮方向重设：

- 新增：+5，正式固定正文优先陪读包、E-R-D-D、设计资产提炼层、eval gates 和下一轮 contract-first 路线。
- 扣减：-8，取消“下一步继续推进旧结构化提炼候选链路”的默认权重，并承认旧样张/旧任务不能支配产品路线。
- 净变化：-3。

本轮 contract / validator / two-sample proof 最小闭环：

- 新增：+2，落地 `validate-contract` 最小 CLI，可校验样本目录和单个 contract 文件。
- 新增：+2，完成书籍/长文局部样本，包含 source-registry、location-map、catalog-map、local-deepread、rejected/downgraded、output-eval 和 reader-facing markdown。
- 新增：+2，完成 Skill/工程材料 2-3 模块样本，包含 capability-map、技术旁批、rejected/downgraded、output-eval 和 reader-facing markdown。
- 新增：+1，测试覆盖有效样本通过和关键无效 contract 失败，包括缺失 eval gate、未知 refs、空壳 source/location 和 reader/audit 混淆。
- 新增：+1，明确 validator 通过仍不等于人工验收，也不证明完整生成器能力。

净变化：+8。

本轮 Markdown renderer / output-eval runner 最小工程闭环：

- 新增：+2，`render-contract-package` 可从 proof 样本 contract JSON 和 source excerpts 渲染临时双轨阅读包。
- 新增：+2，`eval-rendered-package` 可对 renderer 输出执行最小机器 gate，并保持 `human_status=pending` 边界。
- 新增：+1，两类样本渲染输出均通过 `validate-contract` 和 eval runner。
- 新增：+1，测试覆盖删除 source excerpt、删除 reader 页、删除一手正文段、删除 output-eval gate、机器改写人工 accepted 等失败条件。
- 新增：+1，更新当前任务、开发状态、进度和运行 ledger，明确本轮仍不是完整生成器或人工验收。

净变化：+7。

本轮 Agent workflow / 半自动生成器前置切片：

- 新增：+2，`docs/agent-workflow.md` 明确 script / Agent / human 三方边界和五阶段失败路径。
- 新增：+1，`eval-rendered-package --report-md <path>` 可在成功和失败时写 Markdown 机器评估报告。
- 新增：+1，测试覆盖成功报告的 5 个 runner gate / `human_status pending` 边界、失败报告的失败 gate / 失败原因、默认拒绝覆盖已有报告、拒绝写入 LifeAtlas。
- 未加分：人工读者收益审查仍未完成。
- 未加分：第二类真实材料迁移测试仍未开始。

净变化：+4。

本轮《埃隆之书》source-aligned 长样张 v0：

- 新增：+1，交付 repo 内 `docs/reports/readerlab-elon-source-aligned-demo-v0/`，包含 README、全书地图、大单元深读、source alignment 和 eval。
- 新增：+1，样张覆盖第二部分一个大单元，使用 EPUB spine、旧 location refs、短摘录、处理后的一手正文、AI 深读和降级/拒绝理由，信息量明显高于 toy sample。
- 新增：+2，对抗审查先发现 source refs 错挂；修复 `loc-org-barrier` / `loc-org-communication`、`loc-parallel-processing` 和制造 heading path 后复审 PASS。
- 口径校正：`spine-015 / v101-13.xhtml` 是第二部分标题边界，实质 source cards 覆盖 `v101-14.xhtml` 至 `v101-18.xhtml`；这仍是局部样本质量闭环，不是自动化闭环。
- 未加分：尚未通过用户人工读者收益审查。
- 未加分：仍未进入第二类真实材料迁移测试或半自动生成器。
- 扣减：-4，人工反馈指出 reader-facing 原型未通过：读者页暴露内部 refs、审计字段、机器状态和不自然的“阅读路线 / 主题线索 / 处理过的一手正文”概念，说明产品形态与真实使用体验发生偏离。

净变化：0。

本轮《埃隆之书》reader-facing 原型返工与复核：

- 扣减：-2，用户复核和无上下文子 Agent 均判定 reader experience FAIL：当前页面没有真正一手正文轨，AI 解释替代了阅读入口。
- 未加分：仍不证明完整生成器、半自动流程或 LifeAtlas 正式沉淀能力。

净变化：-2。

本轮产品规格收口：

- 新增：+1，明确书籍/长文默认原样保留正文，不压缩、不改写、不用导读替代正文；除非用户明确要求整理原文，只做空格、空行、断行等轻量清理。
- 新增：+1，明确 Skill/工程材料输出净化正文，剥离命令行、重复模板、执行外壳和机器噪音，但保留用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点。
- 新增：+1，技术负责人层重定义为面向产品负责人的设计资产提炼，要求沉淀可复用设计卡。
- 未加分：尚未基于新契约产出合格样张。

净变化：+3。

本轮输出契约确认与落地：

- 新增：+2，用户确认正文优先陪读包输出契约，并将契约写入活跃规格、验收 gate、当前任务、开发状态、进度、决策和运行账本。
- 范围：书籍/长文原样正文、Skill/工程净化正文、高阶讲解成段服务正文、技术负责人层输出设计资产卡、audit 与读者页分离。
- 未加分：尚未按新契约产出合格样张。

净变化：+2。

本轮高阶讲解口径校准：

- 新增：+1，用户明确 AI 陪读的高阶价值不是普通总结，而是高屋建瓴、全局视角、旁征博引、跨学科思维模型和既有经历连接带来的认知增量。
- 扣减：-1，real-source demo v1 虽然降低了正文契约风险，但《埃隆之书》讲解被判定“不够爽、不够通透”，仍像普通书籍总结，不能证明 ReaderLab 体验成立。

净变化：0。

## 模块进度

| 模块 | 权重 | 当前点数 | 状态 | 说明 |
|---|---:|---:|---|---|
| 产品形态与方向治理 | 10 | 10 | close-for-now | 正文优先陪读包输出契约已确认并落地；后续以真实样张反测。 |
| 材料导入与一手正文 | 12 | 7 | working | Skill 包导入可用；但书籍/长文一手正文硬边界尚未机制化，旧样张因缺正文轨失败。 |
| 来源与可信度契约 | 12 | 9 | working | `validate-contract` 已能检查最小 contract 目录和单文件，renderer 输出可回归通过；完整 schema 系统未完成。 |
| AI 陪读与深读方法 | 16 | 10 | working | 正文优先 demo 已证明 AI 不必替代正文，但高阶讲解仍未达到产品预期；下一步要把全局视角、跨学科连接、旁征博引和认知增量做成讲解 gate。 |
| 技术负责人 / 设计资产提炼层 | 10 | 7 | working | 已从技术旁批重定义为面向产品负责人的隐藏工程设计识别和可复用设计卡；尚未用真实复杂包验证。 |
| 批注与讨论 | 8 | 6 | working | `tandem-comments` 最小链路已验证；索引和迁移体验未 close。 |
| 输出评估与人工验收 | 12 | 7 | working | `output-eval.v1` 已进入两个样本并被 validator/eval runner 检查；eval runner 可写 Markdown 报告；人工验收未完成。 |
| 两类材料最小样本 | 10 | 6 | working | 新规格下的长文 proof 和 Skill/工程 proof 已完成；书籍侧《埃隆之书》只证明 source alignment，reader-facing 样张失败，需要按新契约重做。 |
| 生成器机制化与正式 Skill | 10 | 3 | working-low | 已有半自动前置 workflow 文档和 proof renderer/report runner；正式生成器尚未开始，当前 proof renderer 不能冒充生成器能力。 |

## Close / Working / Blocker

### Close

- 根目标：复杂材料陪读 / 吸收系统，而不是摘要器或单体生成器。
- 产品形态：正文优先陪读包。
- 方法骨架：E-R-D-D。
- 技术材料方向：Design Atom Analysis + 设计资产提炼。
- 正式开发前规格文档。
- 机器完成不等于人工验收。
- 当前任务文件不再作为方向权威。

### Working

- contract schema 收紧和 validator 扩展。
- Markdown renderer / output-eval runner 的真实材料适配。
- Agent workflow 的真实材料迁移试运行。
- 书籍/长文局部样本的人工读者收益审查。
- 按新输出契约选择一个小样本重做 reader-facing 样张。
- 重做 AI 高阶讲解口径：不能停在普通总结，必须提供高维视角、跨学科同构连接和受正文约束的认知增量。
- Skill/工程材料局部样本的人工读者收益审查。
- local-deepread、capability-map、output-eval 的事实层和展示层分离。
- 批注索引和 Codex 回复产品化。

### Blocker / Not Started

- 正式图书/长文导入生成器。
- provider-backed 或 blind A/B output eval。
- 人工验收闭环。
- ReaderLab 正式 Skill 包装。
- LifeAtlas `300/600/800` 正式沉淀流程。

## 下一轮计分规则

下一轮如果基于新契约完成最小样张，最多可增加 3 点：

- +3：选择一个小样本按新契约重做 reader-facing 样张，并通过人工读者体验审查。

如发现新规格不适配真实材料，必须扣分；不得为了维持进度而把不稳定样张说成能力成立。
