# Dev State

## 产品目标

ReaderLab 是复杂材料吸收系统。它把书籍、长文、课程资料、代码文档、Skill 包和混合型资料转成 LifeAtlas 阅读包，让读者能先接触可信的一手正文或净化正文，知道当前章节或模块在整体中的位置，同时获得高阶讲解、技术负责人解剖、误读防护和候选沉淀。

当前正式产品形态是 **正文优先的陪读包**：

- 一手正文轨：书籍/长文原样正文，或 Skill/工程材料净化正文。
- AI 陪读轨：全局讲解、高阶讲解、深读卡、误读防护、候选沉淀。
- 设计资产轨：面向产品负责人的技术负责人解剖和可复用设计卡。

ReaderLab 不替代人的第一次阅读。AI 只降低阅读阻力，不能把自己的提炼挡在一手材料前面。

用户进一步明确：AI 高阶讲解的价值不只是“把这一章总结得更清楚”，但它仍必须讲清重点和要点。它应像一个见识丰富、拥有全局视角的人在陪读：能旁征博引，引入跨学科思维模型、历史观、产品经验、组织管理、工程系统和用户既往经历中的相似结构，把看似不同学科背后的同构逻辑串起来，让读者获得“原来可以这样看”的认知增量。这些例子表达的是需求意向，不是封闭清单；如果有更完善的知识结构，应优先服务“讲清材料 + 建立更大价值观和体系”。高维讲解仍必须受正文约束，区分原文依据、AI 解释性重组、外部类比和待验证判断。

2026-06-30 人工反馈重新校准了读者原型：`Route` / 阅读路由是内部方法，不是读者页产品词；读者页应先提供真正可读的正文，再由 AI 成段讲清材料，而不是展示 source refs、claim trace、机器状态和降级/拒绝理由。

用户进一步明确：书籍/长文默认原样保留正文；Skill 包和工程材料做净化正文；技术负责人层要替产品负责人识别其不容易感知的工程和系统设计，并沉淀成可复用设计资产。当前《埃隆之书》样张 reader experience 判定为 FAIL，不再进入人工复核通过路径。

## 当前路线判断

上一阶段已经完成多种样张和实验：

- gstack / dbs-suite Skill 包导入与批注保护。
- `tandem-comments` 批注读取和回复最小链路。
- 《埃隆之书》v0 / v1 手工样张。
- method bakeoff、片段能力评测、dbs-suite capability map。
- 结构化提炼最小闭环和同题多路线对照。

这些产物是证据库，不是 product ready，也不证明生成器能力成立。当前已确认输出契约：书籍/长文必须有原样正文轨，Skill/工程材料必须有净化正文轨，AI 讲解必须服务正文阅读并提供非摘要型认知增量，技术负责人层必须产出设计资产，audit 事实层不得污染读者主页面。

外部强模型建议已触发方向重估：旧 `docs/current-task.md` 里的局部下一步不再默认继承为项目主线。正式开发前的主线改为：

```text
产品规格冻结
-> contract / validator
-> 两类最小样本
-> Markdown renderer
-> output eval
-> Agent workflow
-> 半自动生成器
```

## 新方法骨架

AI 阅读方法采用 E-R-D-D：

1. Evidence：先建立来源、覆盖、位置、不能下结论的边界。
2. Route：内部结构定位，判断材料类型、阅读单元、主体/外壳/证据/实现细节分层，以及章节/模块在整体中的位置。
3. Deepen：生成深读候选，包括主问题、机制链、原则、案例、反例、术语、技术设计、失败模式、迁移洞察。
4. Decide：通过 Source / Structure / Reader Gain / Transfer-Technical / Overreach gate，决定 Promote、Keep、Downgrade 或 Reject。

Deepen 不能退化为“本章讲了什么”。高阶讲解候选需要显式判断它能否提供更大的世界图景、跨学科同构关系、历史或组织经验连接、迁移边界和误用风险；只是漂亮类比或名人模型堆叠的候选不能 Promote。

技术材料额外使用 Design Atom Analysis，分析 trigger、inputs、outputs、workflow、constraints、failure_modes、human_gate、output_contract、verification、risk_control、transferable_pattern 等设计原子。面向读者时，这些原子应翻译成产品负责人可理解、可复用的设计资产，而不是原样展示字段。

## 当前实现事实

- 仓库入口：`/Users/tianqiang/Documents/读书伴侣`。
- 生成脚本：`scripts/readerlab.py`。
- 单元测试：`tests/test_readerlab.py`。
- 当前正式脚本主要支持 Skill 包导入：`import-skills`。
- 新增最小 contract validator CLI：`validate-contract <path>`，支持样本目录和单个 contract JSON 文件。
- 新增最小 renderer CLI：`render-contract-package <sample_dir> <output_dir>`，只从 proof 样本 contract JSON + source excerpts 渲染临时双轨包，不写 LifeAtlas。
- 新增最小 eval runner CLI：`eval-rendered-package <path>`，复用 `validate-contract` 并额外检查 reader/audit 分离、reader markdown 存在、一手正文段回链 source excerpts、output-eval 9 gate 存在和 `human_status` 不冒充 accepted。
- `eval-rendered-package` 支持 `--report-md <path>`，成功和失败都可写 Markdown 机器评估报告；报告不是人工验收。报告默认拒绝覆盖已有文件，且拒绝写入 `/Users/tianqiang/LifeAtlas`。
- 新增 `docs/agent-workflow.md`，明确 script / Agent / human 三方边界，以及输入准备、语义建模、确定性渲染、机器评估与报告、人工审查五阶段失败路径。
- 新增《埃隆之书》书籍侧 source-aligned 长样张 v0：`docs/reports/readerlab-elon-source-aligned-demo-v0/`。
- 该样张覆盖第二部分“极限硬核工作”一个大单元，使用短摘录、EPUB spine、旧 `location-map.v1.json` refs、处理后的一手正文、AI 深读和降级/拒绝理由。
- 覆盖口径：`spine-015 / v101-13.xhtml` 只作为“第二部分”标题边界；实质 source cards 覆盖 `spine-016` 至 `spine-020`，即 `v101-14.xhtml` 至 `v101-18.xhtml`。
- 该样张只用于补 7 个闭环中的 `2. 样本质量闭环`，已通过对抗审查复审的 source alignment 检查；但 reader experience 最终判定为 FAIL，原因是没有真正的一手正文轨，AI 解释替代了阅读入口。它不是 product ready，不证明半自动生成器能力，不写 LifeAtlas。
- 图书/长文正式导入尚未进入生成器。
- 已实现 Obsidian `tandem-comments` 读取、定位和回复追加 CLI：`comments-list` / `comments-reply`。
- 本轮新增 contract proof 样本目录：`docs/reports/readerlab-contract-validator-proof-v0/`。
- `book-longform-sample` 是书籍/长文局部样本，只证明 partial coverage 下的 catalog-map、local-deepread 和 output-eval。
- `skill-engineering-sample` 是 Skill/工程材料 2-3 模块样本，只证明 capability-map 的行为字段和技术边界表达。
- renderer 当前只支持上述两个 proof 样本形态：catalog-map 长文局部样本、capability-map 工程样本。
- eval runner 当前是最小机器检查：包级 contract 校验 + reader/eval/status gate；不是 provider-backed eval，也不是人工阅读验收。
- 现有报告和样张均作为证据或 baseline，不作为正式产品能力证明。
- 当前目录可用 `git status` 做变更边界查看；但验收仍以写入路径、文件内容检查、测试和 validate 输出为准。

## 正式开发前规格

- `docs/product-spec.md`：产品目标、边界、阶段路线。
- `docs/readerlab-package-spec.md`：目标阅读包结构。
- `docs/ai-reading-method.md`：E-R-D-D 方法。
- `docs/technical-cofounder-method.md`：技术材料的设计原子分析。
- `docs/eval-gates.md`：功能、阅读质量、深读质量、技术洞察和失败条件。
- `docs/agent-workflow.md`：半自动生成器前置 workflow，定义 script / Agent / human 边界。

## 已作废或收窄的旧口径

- 当前任务文件不是方向权威；它只能记录当前执行切片。外部强模型或用户方向重判进入后，旧执行切片必须重新评估。
- 结构化提炼实验不是产品主线，只是 AI 陪读层中的局部能力证据。
- 任何路线、组合或样张都不能因为字段齐全而进入生产链；必须证明读者收益、来源可靠性和人工验收边界。
- “参考项目真实吸收”不能理解为列项目、贴字段、写 matrix；必须转成 contract、gate、eval 或读者页改善。
- Markdown 不是事实层。事实层应是 source registry、location map、contract JSON、eval 和人工状态。
- validator 通过不等于人工阅读质量通过。

## 模块状态

| 模块 | 状态 | 判断 |
|---|---|---|
| 产品形态与方向治理 | close-for-now | 正文优先陪读包输出契约已确认：书籍/长文原样正文、Skill/工程净化正文、技术负责人层沉淀设计资产、audit 与读者页分离。 |
| 材料导入与一手正文 | working | Skill 包路径基本可用；书籍/长文正式导入未机制化。下一步必须先满足正文硬边界，不能再用导读或 AI 概括替代正文。 |
| 来源与可信度契约 | working | 已有最小 `validate-contract`，可检查 source/location/status/display/claim refs；renderer 输出可回归通过；仍未形成完整 schema 系统。 |
| AI 陪读与深读方法 | working | 正文契约 demo 已降低“AI 替代正文”的风险，但用户判定当前高阶讲解仍像普通总结；下一步需要重做讲解引擎，让其提供全局视角、跨学科连接和非摘要型认知增量。 |
| 技术负责人 / 设计资产提炼层 | working | 已重新定义为面向产品负责人的隐藏工程设计识别和设计资产沉淀；旧技术旁批样本不足以证明能力。 |
| 批注与讨论 | working | `tandem-comments` 最小链路已验证；产品化索引和迁移仍需继续。 |
| 输出评估与人工验收 | working | `eval-rendered-package` 已能对 renderer 输出执行最小机器 gate，并可写 Markdown 报告；人工读者收益审查仍为 pending。 |
| 生成器机制化 / 正式 Skill | not_started | 只有 proof renderer，不是完整生成器；不能把当前输出冒充产品能力。 |

## 下一步

contract / validator / two-sample proof 的最小闭环已完成第一版，并根据对抗审查补强了空壳来源、缺失 eval gate、未知 refs 和 reader/audit 混淆等 false-pass 风险。

Markdown renderer / output-eval runner 的最小工程切片已完成，并根据对抗审查修复了缺 source excerpt 仍可渲染成功的 false-pass。

Agent workflow / 半自动生成器前置切片已完成机器侧第一版：三方边界文档已落地，eval runner 可输出 Markdown 报告。但人工反馈证明旧 reader-facing 原型会走样；最新结论是已确认并落地输出契约，不是跳到第二类迁移测试或生成器。

用户已明确判定上一轮 proof/toy sample 信息量不足，不能展示 ReaderLab 能力。随后转向《埃隆之书》source-aligned 长样张 v0，并通过对抗审查复审；新的人工反馈判定 reader experience 仍失败。之后 real-source demo v1 证明正文优先契约方向基本成立，但用户再次指出《埃隆之书》高阶讲解“不够爽、不够通透”，仍像普通书籍总结，甚至不如已有 Skill 提炼参考。下一步不是继续加样本，而是先把高屋建瓴、全局视角、跨学科模型和旁征博引式认知增量写成高阶讲解口径，并用小样章重做 AI 陪读层。

不直接开发完整生成器，不继续围绕旧局部链路做路线争论，不写 LifeAtlas 正式沉淀区，不新增依赖。
