# ReaderLab V2 可分享 Skill 包边界

## Status

本文定义 ReaderLab V2 从研发工作区生成可分享 Skill 包时的边界。当前目标状态是 `shareable_package_prepared`，后续经安装 smoke、三类材料 smoke 和 RC 复核后，才可能进入 `installable_release_candidate`。

本文不声明 production ready、public validation pass、完整 GSTACK 包通过或三类材料最终读者验收通过。

## Boundary Model

ReaderLab V2 分三层：

1. 研发仓库：保留源码、实验、历史报告、真实样本、测试和开发记录。
2. 可分享 Skill 包：只包含安装和运行 ReaderLab 所需的最小干净资产。
3. 安装目标：用户本机的 Codex Skill 目录或等价干净目标。

可分享 Skill 包必须从研发仓库构建或导出，不能直接把研发工作区整体复制给用户。

## Must Include

可分享 Skill 包至少应包含：

- Skill 入口说明和触发边界。
- ReaderLab 核心脚本或命令入口。
- 运行配置模板。
- 图书 / 长文路线的必要协议和模板。
- Skill / 工程材料路线的必要协议和模板。
- Quality Gate / Reader Evaluation / Controller 的最小协议说明。
- 最小 fixtures 或 smoke 输入，用于验证安装和基本路线。
- 验证命令说明。
- 状态用语说明，避免把局部通过扩大成 production ready。

## Must Exclude

可分享 Skill 包不得包含：

- `experiments/readerlab-v2/reports/` 下的历史报告和真实运行产物。
- 真实私有 source material。
- 当前用户的 LifeAtlas 固定路径。
- GSTACK 原始源仓库内容。
- 临时 handoff 文件。
- 旧失败样张和历史过程日志。
- 凭据、token、个人配置、机器绝对路径缓存。
- 未经用户批准的全局 Codex 配置改动。

## Required Configuration Inputs

Skill 包运行时不得静默依赖当前用户机器路径。必须由配置或参数提供：

- `source_paths`
- `output_root`
- `permission_boundary`
- `material_family`
- `requested_scope`
- `human_review_required`
- `declared_scope`
- `declared_units`
- `full_book_required`
- `dual_view_required`
- `engineering_source_scope`，仅 Skill / 工程材料路线需要

缺少必需参数时必须 stop，并给出最小补救建议。

## Quality Verification Boundary

可分享包必须保留两层核验：

生产时约束：

- 输入、输出、顺序和目标产物存在。
- 来源范围、正文 / 净化正文、证据层和失败回指齐全。
- Quality Gate packet 协议成立。
- blocking gate 失败时 controller 不能绕过。

验收时约束：

- 内容完整性。
- 人类读者体验。
- 产品预期。
- 高阶讲解认知增量。
- 无上下文 Agent 对资产卡的冷启动复用。

验收时约束默认不进入 runner。只有当问题能反推成稳定、低误伤、可观察、可复跑的生产前置条件时，才允许升级为 runner 或生产 prompt 约束。

## Required Review Perspectives

每次 RC 复核必须覆盖：

- 合同履约 / 结构合规。
- 内容完整性。
- 人类读者体验。
- 产品预期。
- 无上下文 Agent 复用。

Skill / 工程材料路线中：

- 人类读者 Agent 只看 `<block>.md` 和 `<block>.engineering.md`。
- 无上下文 Agent 只看 `<block>.assets.md`。
- 无上下文 Agent 不打开 `body.md`、technical notes、full-source-track 或原始 source。

## Historical Anti-Regression

后续开发不得重犯这些已确认问题：

- Elon v1 是负样本，不是通过样张。
- 正文和陪读不能恢复成正文文件、AI 解读文件、预设批注问题文件三分结构。
- 机器 validator、JSON parse、trace validation、runner 通过不等于读者验收通过。
- Python runner 不能用关键词、长度或字段堆叠冒充质量判断。
- `limited_accept` 不能说成 production ready。
- `make-pdf` 和 `setup-deploy` 旧 case 是新合同下的诊断失败样本，不是代表性正样本。
- `gstack/spec` 和 `gstack/review` 是完整单 Skill prototype candidate，不代表完整 GSTACK 包通过。
- 图书和长文默认保留原样正文和章节顺序，不能用 AI 导读、摘要或高阶讲解替代正文。

## Status Ladder

- `dev_worktree`：研发工作区状态，不能分享给普通使用者。
- `shareable_package_prepared`：已生成干净包候选，但未完成安装 smoke。
- `installable_release_candidate`：安装 smoke 和三类路线 smoke 已完成，可作为候选给朋友试用。
- `friend_smoke_passed`：朋友环境的有限 smoke 通过。
- `reader_accepted`：某个具体输出包经过读者验收。

这些状态不能自动升级。每次升级都必须说明刚刚通过的是哪类核验。
