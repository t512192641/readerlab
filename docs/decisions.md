# Decisions

本文件只保留仍会约束后续实现的耐久决策。旧阶段细节不再保留为启动上下文；需要查证时看 git 历史或 Codex 会话。

## D-001 ReaderLab 是复杂材料陪读系统

ReaderLab 的目标是把书籍、长文、课程资料、代码文档、Skill 包和混合型资料转成中文可读、可批注、可讨论、可沉淀的 LifeAtlas 阅读包。

它不是摘要器、普通翻译器、代码审查器或 Skill 安装器。

## D-002 正文优先，AI 陪读不能替代一手材料

书籍和长文默认保留完整选定正文；AI 陪读负责解释结构、误读防护、深读和候选沉淀，不能替代正文。

Skill 包和工程材料默认生成净化正文：剥离命令行、重复模板和机器噪音，但保留用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点。

## D-003 Markdown 是展示层，audit/contracts/eval 是事实层

读者页必须自然可读。来源、位置、机器状态、claim、candidate、gate、eval 等进入 `audit/` 或 JSON contract，不污染 reader-facing 页面。

## D-004 不自建批注系统

ReaderLab 默认适配 Obsidian + Markdown + 现有批注插件。当前真实插件格式是 `tandem-comments`。

批注能力当前状态是 `pass_with_warning`：插件存储可读，但严格正文段落直接选择仍未验证。

## D-005 机器通过不等于人工验收

validator 通过只说明结构和引用规则通过；不能说阅读质量通过、产品可生产、public external validation pass 或 transferable method pass。

## D-006 repo-local Skill 是试运行，不是全局安装

当前 ReaderLab Skill 只在本仓库 `.agents/skills/readerlab/` 激活。未经用户明确批准，不安装到 `/Users/tianqiang/.codex/skills/`，不宣称生产可用。

## D-007 trace-validation 是封版前必要 gate

正式包需要 `audit/contracts/trace-validation.json`。validator 必须检查 reader-facing core paragraphs 能追溯到 anchor、claim、candidate 或 gate。

## D-008 gstack 源仓库不属于清理对象

`/Users/tianqiang/技能项目/skills-canonical/packages/gstack` 是用户要继续学习的原始 Skills 材料，不因 ReaderLab 清理动作删除、移动或重写。LifeAtlas 270 下旧 `gstack` ReaderLab 生成解读包不是原始 Skills，已删除。

## D-009 ReaderLab 阅读页必须正文和陪读同页

面向 Obsidian 的默认阅读面是单个可批注 Markdown 页：一手正文或净化正文在页面内，AI 陪读块贴近相关正文段落。不要默认把同一个阅读单元拆成 `01_正文.md`、`02_AI陪读.md`、`03_批注问题.md`，也不要生成预设批注问题文件。批注由用户在正文附近添加。

该决策来自 2026-07-01 Elon 试生成纠偏：先按旧分轨结构生成，随后又按同目录三文件生成，均被判定为不符合真实 Obsidian 阅读体验。此问题应作为 ReaderLab Skill 输出契约缺陷处理，而不是单次执行偏差。
