# ReaderLab Package Spec

> Authority boundary: 本文件是阅读包结构规格，不是当前任务源。当前执行事实、下一步和读取范围以 `docs/current-task.md` 为准。

## 目标

定义 ReaderLab 阅读包的目标结构。该结构是正式开发前规格，不代表当前脚本已经完整支持。

## 包级结构

```text
ReaderLab Package/
  00_从这里开始.md
  01_全局讲解.md

  10_一手正文/
    001_章节或模块名.md

  20_AI陪读/
    catalog-map.md
    grounded-global-map.md
    local-deepread/
      001_章节或模块名.deepread.md
    capability-map.md
    design-asset-notes.md
    misread-guards.md

  30_批注与讨论/
    comments-index.md
    codex-replies.md

  40_候选沉淀/
    distillation-candidates.md
    skill-candidates.md

  audit/
    source-registry.json
    location-map.json
    contracts/
      catalog-map.json
      grounded-global-map.json
      high-order-explanation.v1.json
      local-deepread/
      capability-map.json
      distillation-candidates.json
    rejected-downgraded.md
    eval.md
```

## 输出契约

ReaderLab 包必须先满足正文主体，再提供 AI 陪读和 audit。不同材料类型的主体不同：

- 书籍 / 长文：`10_一手正文/` 保留原样正文和章节顺序。默认不压缩、不改写、不重述；除非用户明确要求整理原文，否则只做空格、空行、断行等轻量排版清理。AI 讲解放在正文之后或 `20_AI陪读/`，不能替代正文。
- Skill / 工程材料：`10_一手正文/` 放净化正文。净化正文剥离安装命令、重复模板、执行外壳、机器状态、路径、hash、调试信息，但保留用途、触发条件、用户意图、核心流程、约束、失败条件、输出要求和设计亮点。
- 高阶讲解：用成段语言讲清材料，不把内容拆成导读、旁批、误读提醒等固定栏目。它不是小总结，而是用更大的知识结构给读者提供认知增量：可以引入跨学科思维模型、历史观、产品经验、组织管理、工程系统、商业案例和用户既往经历中的相似结构，但必须解释底层逻辑如何相通，并区分原文依据、AI 解释、外部类比和待验证判断。
- 高阶讲解内部契约：`audit/contracts/high-order-explanation.v1.json` 记录 Source Anchor、Baseline Summary Trap、Upgrade Question、Mechanism Graph、Lens Auction、Judgment Gate、Natural Explanation 和 Delta Eval。该契约只在 audit 层保存，不作为 reader-facing 栏目。
- 设计资产卡：只对 Skill、工程材料、Agent 工作流和类似材料强制出现，必须面向产品负责人说明适用场景、解决问题、原材料依据、可复用做法、使用前提、失败风险和什么时候不要用。
- audit：source refs、location map、claim trace、machine/human 状态、降级/拒绝记录进入 `audit/`。reader-facing 页不把这些内部结构当主内容。

## 入口页

`00_从这里开始.md` 必须回答：

- 这份材料是什么。
- 为什么值得读。
- 当前覆盖范围是什么。
- 从哪里开始读。
- 哪些部分是 AI 判断，哪些是一手材料。
- 哪些内容仍需人工复核。

## 全局讲解

`01_全局讲解.md` 必须回答：

- 材料类型：书、长文、课程、Skill 包、代码文档、混合材料。
- 这份材料整体在讲什么。
- 它由哪些主要部件组成。
- 各部件之间是什么关系。
- 当前已覆盖或当前样张所在的位置。
- 读者读到某一章/模块时，应如何理解它和全文/全包的关系。

这一页应像一个已经读完整份材料的人给读者讲清楚“这本书 / 这个 Skill 包到底在说什么”。不要用内部分析标签替代讲解。`阅读路线` 可以作为内部 Agent 判断，不作为读者页标题。读者页不应暴露 `source refs`、claim trace、机器状态或审计字段。

## 一手正文

`10_一手正文/` 是读者第一次阅读的核心。

正文页结构：

```text
# 章节 / 模块名

## 正文 / 净化正文

## 本章讲解

## 设计资产提炼

## 必要提醒

## 可批注问题
```

规则：

- `正文 / 净化正文` 是页面主体，必须先出现。
- 书籍和长文默认原样保留正文；除非用户明确要求整理原文，否则只允许删除多余空格、空行、断行等不改变意义的格式噪音。
- 书籍和长文不得使用 AI 压缩、改写、概括、导读冒充正文。
- Skill 包和工程材料的 `净化正文` 是剥离安装命令、重复模板、执行外壳和机器噪音后的主体描述文本；必须保留用途、触发条件、用户意图、核心流程、约束、失败条件、输出要求和设计亮点。
- 被剥离的命令、脚本、执行协议、hash、路径和机器证据默认进入 `audit/`、附录或设计资产提炼，不丢失。
- AI 讲解不能替代正文。
- `设计资产提炼` 只在 Skill/工程/Agent 工作流材料中出现。
- 没有真实边界或误读风险时，不强行凑内容。
- 降级/拒绝理由默认进入 `audit/rejected-downgraded.md`，读者页只保留少量自然语言误读提醒。
- 完整原文、hash、命令行、机器执行视图默认进入 `audit/`。

## AI 陪读

`20_AI陪读/` 放结构化 AI 产物。它服务正文阅读，不替代正文阅读：

- `catalog-map.md`：基于目录/文件结构/标题的路线假设。
- `grounded-global-map.md`：覆盖足够时的全局地图。
- `local-deepread/`：局部深读卡。
- 高阶讲解：应让读者获得“我原来没这样看过”的理解，而不是只得到章节摘要。优秀讲解可以旁征博引，但不能脱离材料；如果跨学科类比不能反过来照亮正文，就不要放进读者页。内部按 `high-order-explanation.v1` 先完成正文锚定、普通总结对照、升维问题、机制图、镜头选择、吸收 / 降级 / 拒绝和 delta eval。
- `capability-map.md`：Skill/工程材料的能力地图。
- `design-asset-notes.md`：技术负责人视角下的设计资产提炼。
- `misread-guards.md`：误读防护。

## 批注与讨论

`30_批注与讨论/` 不替代正文附近批注，只提供索引和汇总：

- `comments-index.md`：批注索引。
- `codex-replies.md`：必要时汇总 Codex 回复。

真实批注仍应尽量贴近正文或保留插件原始存储格式。

## 候选沉淀

`40_候选沉淀/` 只放候选，不自动升格：

- `distillation-candidates.md`
- `skill-candidates.md`

任何正式进入 LifeAtlas `300/600/800` 的内容都需要人工确认。

## Audit

`audit/` 是事实层和追溯层，不是普通阅读入口。

必须保留：

- source registry
- location map
- contracts
- rejected / downgraded 清单
- eval
- machine_status / human_status

## 最小可交付包

下一轮开发的最小包只需覆盖：

- 1 个入口页。
- 1 个全局讲解。
- 1 个一手正文局部样本。
- 1 个 AI 陪读局部样本。
- 1 套 audit contracts。
- 1 个 eval。
