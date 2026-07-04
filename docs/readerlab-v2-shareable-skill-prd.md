# ReaderLab V2 可分享 Skill 包 PRD

## Problem Statement

ReaderLab V2 已经证明若干核心方向是对的：正文优先、正文旁陪读、工程材料三层产物、证据层和 reader evaluation / controller 分离。但当前形态仍是一个开发工作区里的原型系统，混有实验目录、历史报告、本机路径、未收口的 V2 文件和有限样本产物。它还不能被清楚地安装成一套干净、独立、可分享给朋友使用的 Codex Skill。

用户真正要的不是“本机某个 demo 能跑”，而是一套完整、独立、干净的 ReaderLab Skills：可以处理图书、长文 / 报告 / 访谈稿、Skill / 工程材料；能保留一手正文或净化正文；能生成中文可读、可批注、可验收的陪读包；也能被安装、复用和有限分享，而不是依赖当前仓库里的脏上下文。

本 PRD 同时解决一个开发过程问题：V1 / V2 已经讨论过并有结论的问题，不应在后续开发中被遗忘或重复追问。后续执行必须把历史失败和已定原则转成明确的防回归约束。

## Solution

把 ReaderLab V2 从“开发工作区里的原型”重整为“可安装、可分享、可验收的 Skill 包候选”。

第一阶段目标不是宣布 production ready，而是进入 `installable_release_candidate`：一个干净包能被安装到 Codex Skill 目录，被 Codex 发现，并在三类材料路线的代表样本上跑过结构与验收流程。每个输出包是否真正读者通过，仍由独立 reader evaluation、Quality Gate、controller 和人工复核决定。

核心策略：

- 保留开发仓库作为研发源头，另建干净发布边界。
- 把 Skill 包需要的 `SKILL.md`、脚本、协议、模板、最小 fixtures、验证命令和使用说明打包出来。
- 把本机路径、实验报告、旧样张、私有源材料、GSTACK 原始仓库引用和历史过程文件排除在发布包之外。
- 让配置项接管输入源、输出根目录、权限边界和材料类型，不让 Skill 依赖用户本机路径。
- 三类材料路线都必须有最小 smoke / regression：图书、长文 / 报告 / 访谈稿、Skill / 工程材料。
- 保持生产约束和验收约束分层：runner 只管生产硬约束，读者体验和复用质量由 Quality Gate / Reader Evaluation / 人工复核判断。

## Historical Anti-Regression

后续开发必须先查历史再重做设计，尤其是下列已确认问题。

1. Elon v1 不是正样本。它只证明“正文和陪读同页”方向修正过，但章节结构、陪读价值、专家感、密度和 reader gate 失败，不能被包装成通过样张。
2. 旧的正文、AI 解读、批注问题三文件分离会破坏 Obsidian 阅读体验。默认阅读单元必须是一页可批注 Markdown，正文和有价值陪读同页。
3. 机器 validator、JSON parse、trace validation、runner 通过不等于读者验收通过。任何“通过”必须说明是合同、结构、质量 gate、reader evaluation、controller 还是人工验收。
4. Python runner 不能用关键词、长度或字段堆叠冒充质量判断。它只能检查来源、正文、证据层、结构、顺序、失败回指和 blocking controller。
5. `limited_accept` 只能表示有限范围接受，不能说成 production ready、reader_package_pass 或 public validation pass。
6. `make-pdf` 和 `setup-deploy` 旧 Skill case 在新 evidence-layer 合同下失败是合理诊断信号，不应继续当代表性正样本。
7. `gstack/spec` 和 `gstack/review` 两个完整单 Skill case 目前只是 `limited_accept` 的 prototype candidate，不代表完整 GSTACK 包通过，也不代表 Skill 路线最终发布通过。
8. Skill / 工程材料必须有净化正文主读页、技术解说页、资产卡导出页。技术解说不能替代净化正文，资产卡也不能要求未来 Agent 先读原始 source 才能用。
9. 图书和长文默认保留原样正文和章节顺序，不能用 AI 导读、摘要或高阶讲解替代正文。
10. 旧实验、报告、私有路径和 LifeAtlas 本机目录不能进入可分享 Skill 包；可分享包只能保留必要模板、协议、脚本、fixtures 和说明。

## User Stories

1. 作为产品 owner，我想拿到一套干净的 ReaderLab Skill 包，以便它不是一个夹杂实验历史和本机路径的运行文件夹。
2. 作为产品 owner，我想把 ReaderLab Skill 安装到 Codex Skill 目录，以便我能像调用其他 Skill 一样调用 ReaderLab。
3. 作为产品 owner，我想把 Skill 包分享给朋友，以便对方可以在自己的材料和输出目录上试用，而不是依赖我的 LifeAtlas 路径。
4. 作为产品 owner，我想 ReaderLab 支持图书，以便长书能保留章节正文、结构地图、正文旁陪读和全书闭环。
5. 作为产品 owner，我想 ReaderLab 支持长文、报告和访谈稿，以便不是只对书或 Skill 有效。
6. 作为产品 owner，我想 ReaderLab 支持 Skill / 工程材料，以便能读懂复杂 workflow、prompt、脚本、工程约束和设计资产。
7. 作为普通读者，我想先看到正文或净化正文，以便 AI 不挡在材料本身前面。
8. 作为普通读者，我想陪读贴在正文附近，以便我不需要在正文页和 AI 解读页之间来回跳。
9. 作为普通读者，我想页面语言像中文陪读包，以便它不是审计报告、脚本日志或字段墙。
10. 作为产品 owner，我想每次验收都说明通过的是哪一类检查，以便不把结构通过误听成读者质量通过。
11. 作为技术负责人，我想 runner 只检查生产硬约束，以便不会用脆弱字符串规则替代读者判断。
12. 作为 reviewer，我想 Quality Gate request 拆开合同履约、内容完整性、人类读者体验、产品预期和 Agent 复用，以便不同失败能追到不同层。
13. 作为未来 Agent，我想资产卡能独立说明问题、做法、前提、风险、边界和来源，以便不打开原始 source 也能冷启动复用。
14. 作为维护者，我想发布包排除旧实验、历史 reports 和私有材料，以便包边界清楚、可审计。
15. 作为维护者，我想有状态用语梯子，以便 `dev_worktree`、`installable_release_candidate`、`friend_smoke_passed`、`reader_accepted` 不被混用。

## Implementation Decisions

- 发布形态分两层：研发仓库继续保留完整实验和历史；可分享 Skill 包是从研发仓库构建出的干净目录。
- 可分享 Skill 包边界以 `docs/readerlab-v2-package-boundary.md` 为准；PRD 只定义产品目标和验收方向。
- Skill 包必须包含：Skill 入口说明、ReaderLab 核心脚本、必要协议 / 模板、最小 fixtures、验证命令、安装说明和状态口径说明。
- Skill 包必须排除：实验 reports、真实私有源材料、本机 LifeAtlas 路径、GSTACK 原始源仓库、临时 handoff、旧失败样张和开发过程日志。
- 配置必须外置：输入 source path、输出 root、权限边界、材料范围、材料类型、是否需要人工复核，都不能硬编码为当前用户本机路径。
- 材料路线保留两大家族：`book_longform` 和 `skill_engineering`。长文 / 报告 / 访谈稿归入 book/longform 家族，但必须有独立验收样本。
- 图书 / 长文路线继续使用结构地图、正文保留、陪读候选、陪读选择、读者页装配、reader evaluation、controller 的链条。
- Skill / 工程路线继续使用 full-source evidence packet、cleaned body、source-cleaning map、reader guidance、technical cofounder notes、asset cards、三份 reader-facing 页面。
- Runner 只承载生产约束：来源范围、正文 / 净化正文、证据层、产物结构、顺序依赖、失败回指、blocking controller。
- Quality Gate / Reader Evaluation 承载验收约束：内容完整性、人类读者体验、产品预期、高阶讲解增量、Agent 冷启动复用。
- 发布状态不能使用 production ready。建议状态梯子为：`dev_worktree`、`shareable_package_boundary_defined`、`shareable_package_prepared`、`installable_release_candidate`、`friend_smoke_passed`、`reader_accepted`。
- 任何验收问题只有在能反推成稳定、低误伤、可观察、可复跑的前置条件后，才升级为 runner 或生产 prompt 约束。

## Testing Decisions

- 最高 seam 是“安装后的 Skill 能在三类材料路线上生成并验收一个最小包”。不要只测单个函数或单个 Markdown 文件。
- 发布包构建测试必须检查包内文件白名单和排除规则，尤其是私有路径、实验 reports、旧 handoff 和真实源材料不能进入包。
- 安装 smoke 必须在一个干净目标目录验证 Skill 可发现、入口说明可读、核心命令可运行。
- 图书路线 smoke 必须证明：正文保留、章节结构不平铺、AI 不替代正文、reader evaluation / controller 状态分开。
- 长文 / 报告 / 访谈稿 smoke 必须证明：论证结构或问答结构驱动阅读单元，不按固定长度或文件顺序盲切。
- Skill / 工程路线 smoke 必须证明：净化正文主读页、工程解说页、资产卡页都存在，且 evidence layer 和 blocking controller 生效。
- 回归测试继续保留现有 V2 runner 和 quality gate adapter 测试；发布阶段新增包边界和安装 smoke。
- 验收报告必须明确每条命令通过的类别：包边界、安装、runner 合同、Quality Gate request、reader evaluation、controller，或人工验收。

## Out of Scope

- 本 PRD 不声明 ReaderLab V2 production ready。
- 本 PRD 不声明完整 GSTACK 包通过。
- 本 PRD 不声明图书、长文、Skill 三路线最终读者质量全部合格。
- 本 PRD 不做公开 marketplace 发布。
- 本 PRD 不自动写入 LifeAtlas `300/600/800` 正式沉淀区。
- 本 PRD 不新增依赖，除非后续用户明确批准。
- 本 PRD 不自建新的批注系统，继续适配 Markdown / Obsidian 现有批注工作流。
- 本 PRD 不把验收 rubric 直接塞进 runner。

## Delivery Plan

1. 固定发布边界：定义干净 Skill 包目录、包含清单、排除清单和状态口径。
2. 外置配置：移除当前路径耦合，让输入源、输出目录、权限边界和材料范围来自配置或命令参数。
3. 建立包构建器：从研发仓库生成可分享 Skill 包，并输出包内容审计；包构建器可以先做 manifest / 排除规则骨架，但包含 runtime script 的可运行包必须等配置外置完成。
4. 建立三路线 smoke：图书、长文 / 报告 / 访谈稿、Skill / 工程材料分别验证。
5. 建立安装 smoke：安装到 Skill 目录后能被发现，并能用最小样本跑通。
6. 复核 Quality Gate：确保验收矩阵拆开多类检查，不回退成一句“读者视角 OK”。
7. 做 clean package audit：确认没有私有路径、旧实验产物、真实源材料和历史报告污染发布包。
8. 进入 release candidate code review：只在包边界、安装、三路线 smoke 和状态口径都通过后，才称 `installable_release_candidate`。

## Acceptance Criteria

- 存在一个干净可构建的 ReaderLab Skill 包目录或等价产物。
- Skill 包可以安装到 Codex Skill 目录并被发现。
- Skill 包不含本机私有源材料、LifeAtlas 固定路径、GSTACK 原始仓库、实验 reports 或旧 handoff。
- 图书、长文 / 报告 / 访谈稿、Skill / 工程材料三类路线都有最小 smoke 或回归样本。
- 所有通过声明都带作用域，不把 `limited_accept` 或 runner 通过说成 production ready。
- 生产约束和验收约束分层仍成立：runner 不能绕过 blocking gate，也不能把质量判断包装成机器硬通过。
- PRD 中的历史防回归项被转成 issue 或执行清单，后续开发不再重复追问已定结论。

## Further Notes

当前阶段应调整为“发布形态明确后的重整开发”，不是正式发布阶段。核心能力仍未完成全类型最终验收；下一步应先把目标、边界、历史防回归和 issue 拆分固定下来，再继续开发和 debug。
