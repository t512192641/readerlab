# RFC: ReaderLab V2 Installable Skill Package

## Background

ReaderLab V2 当前已经有 PRD 和 GitHub issue 队列，但还不能直接进入多 Agent 开发。原因是：issue 已覆盖发布边界、包构建、配置外置、安装 smoke、三类材料 smoke 和 RC 复核，但质量核验标准、GitHub worker 边界和主控调度规则还需要一个统一事实源。

本 RFC 采用 `Controller-Agent GitHub Workflow SOP`：

```text
RFC -> GitHub Issues -> git worktrees -> worker agents -> PRs -> Codex review -> feedback fixes -> ready-to-merge candidates -> human approval -> merge
```

用户负责产品方向和最终 merge 批准。主控 Codex 负责调度、状态读取、review 触发和风险汇总。Worker Agent 只处理一个 issue、一个 worktree、一个 PR。

## Goal

把 ReaderLab V2 从开发工作区原型推进到 `installable_release_candidate` 候选：

- 有干净、可分享、可安装的 ReaderLab Skill 包边界。
- 能从研发仓库构建最小 Skill 发布包。
- 运行配置不依赖当前用户本机路径。
- 安装 smoke 能证明 Skill 可发现、入口可读、最小命令可运行。
- 图书、长文 / 报告 / 访谈稿、Skill / 工程材料三类路线都有独立 smoke。
- RC 复核明确区分合同、结构、质量 gate、reader evaluation、controller 和人工验收。

## Non-Goals

- 不声明 ReaderLab V2 production ready。
- 不声明完整 GSTACK 包通过。
- 不声明图书、长文、Skill 三路线最终读者质量全部合格。
- 不自动 merge PR。
- 不新增依赖，除非用户另行批准。
- 不写入 LifeAtlas `300/600/800` 正式沉淀区。
- 不修改 GSTACK 原始源仓库。

## Product Quality Verification

所有路径都必须区分“生产时约束”和“验收时约束”。

生产时约束进入 runner、脚本、包构建或 step contract：

- source path / output root / permission boundary / material scope 是否明确。
- 正文或净化正文是否存在，是否没有被 AI 摘要替代。
- evidence layer 是否存在，能否回到来源。
- 产物结构、顺序依赖、失败回指和 blocking controller 是否成立。
- 可分享包是否排除了私有 source、本机路径、实验 reports、旧 handoff 和 GSTACK 原始仓库。

验收时约束进入 Quality Gate、Reader Evaluation、分离读者 Agent 或人工复核：

- 内容完整性。
- 人类读者体验。
- 产品预期：是否像陪读包，而不是摘要包、笔记包或 audit dump。
- 高阶讲解是否提供认知增量。
- Skill / 工程材料的无上下文 Agent 复用价值。

验收问题不能直接变成 runner 字符串检查。只有当问题能反推成稳定、低误伤、可观察、可复跑的前置条件时，才升级为生产约束。

## Required Verification Perspectives

### 1. 合同履约 / 结构合规

验证主体：runner、包构建审计、结构测试。

必须检查：

- 包结构和 reader-facing / audit 分离。
- source registry、location map、case assembly 或等价事实层存在。
- 图书 / 长文保留正文；Skill / 工程材料保留净化正文。
- Skill / 工程材料有 full-source evidence packet。
- Quality Gate packet 有 schema、目标覆盖、失败回指。
- blocking gate 失败时 controller 不能绕过。

### 2. 内容完整性

验证主体：Quality Gate、Reader Evaluation、人工抽查。

必须检查：

- 图书覆盖章节主线、章节关系和全书闭环要求。
- 长文 / 报告 / 访谈稿覆盖论证结构、上下文缺口、证据组或问答结构。
- Skill / 工程材料覆盖完整 Skill 的关键机制、流程、边界、失败条件和输出要求。

### 3. 人类读者体验

验证主体：人类读者视角 Agent 或人工复核。

输入限制：

- 图书 / 长文：只看 reader-facing 阅读页和必要入口页，不看内部 builder、runner 或 full-source-track。
- Skill / 工程材料：主读者 Agent 只看 `<block>.md` 和 `<block>.engineering.md`。

必须检查：

- 读者能否在正文附近理解陪读。
- 页面是否像中文陪读包，而不是审计报告。
- AI 是否没有挡在正文前面。
- 陪读是否贴近正文、不可替换、不过度模板化。

### 4. 产品预期

验证主体：产品负责人复核或 Product Gate。

必须检查：

- 输出是否服务“读材料本身”，不是服务 validator、audit 或 demo。
- 通过声明是否带作用域。
- `limited_accept` 是否没有被说成 production ready。
- 安装 smoke 是否没有被说成读者质量通过。

### 5. 无上下文 Agent 复用

验证主体：无背景 Agent 视角。

输入限制：

- Skill / 工程材料路线中，无上下文 Agent 只看 `<block>.assets.md`。
- 不打开 body、technical notes、full-source-track 或原始 source。

必须检查：

- 每张资产卡是否说明问题、做法、来源、前提、风险、边界和不要用的场景。
- 是否能知道第一步怎么调用。
- 是否能识别使用限制和失败信号。
- 是否不需要回读原始 source 才能开始复用。

## Parameter And Configuration Verification

可安装 Skill 包必须验证这些运行参数：

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
- Skill / 工程材料的 `engineering_source_scope`

参数验证标准：

- 缺必需参数时必须 stop，并给出最小补救建议。
- 参数不能静默回退到当前用户本机路径。
- 权限边界不能暗示 public validation。
- `requested_scope` 与后续 block / evaluation 覆盖范围必须闭环。
- 多单元 case 不能执行中偷缩成单 block。

## Issue Plan And Owned Files

### #2 固定可分享包边界

Owned files:

- `docs/readerlab-v2-package-boundary.md`
- `docs/readerlab-v2-shareable-skill-prd.md`
- `docs/current-task.md`
- `docs/agent-run-ledger.md`
- `docs/rfc/2026-07-04-readerlab-v2-installable-skill-package.md`
- package boundary docs introduced by the worker

Forbidden:

- Do not edit runner behavior.
- Do not build package output yet.
- Do not claim production ready.

### #3 构建最小 Skill 发布包

Dependency note:

- #3 may start manifest, exclusion-rule, and audit scaffolding after #2.
- #3 must not ship a runnable package containing `scripts/readerlab.py` until #4 has removed current-user path coupling from that runtime script.

Owned files:

- packaging script / manifest files introduced by the worker
- `.agents/skills/readerlab/SKILL.md`
- package inclusion / exclusion tests introduced by the worker
- docs describing package build usage

Forbidden:

- Do not include real private source material.
- Do not copy experiment reports into the shareable package.
- Do not include package-external fixtures such as current comment replay demos unless a self-contained sanitized fixture is committed first.
- Do not package `scripts/readerlab.py` before #4 removes hardcoded local path defaults.
- Do not install globally.

### #4 外置运行配置

Scheduling note: #4 is a prerequisite for any #3 package output that includes runtime entry scripts.

Owned files:

- `scripts/readerlab.py`
- `scripts/readerlab_v2_runner.py`
- `scripts/readerlab_v2_case_assembly.py`
- related tests
- configuration docs / examples introduced by the worker

Forbidden:

- Do not hardcode LifeAtlas, GSTACK, or experiment report paths as defaults.
- Do not add dependencies.

### #5 安装与发现 smoke

Owned files:

- install smoke script / docs introduced by the worker
- package manifest / installation docs
- related tests

Forbidden:

- Do not modify global Codex config without explicit user approval.
- Do not treat install smoke as reader quality acceptance.

### #6 图书路线 smoke

Owned files:

- book smoke fixture / builder introduced by the worker
- book route tests
- relevant reader-facing gate docs if needed

Forbidden:

- Do not reuse Elon v1 as a passing sample.
- Do not use AI summary as body.
- Do not write to LifeAtlas permanent zones.

### #7 长文 / 报告 / 访谈稿路线 smoke

Owned files:

- longform smoke fixture / builder introduced by the worker
- longform route tests
- route docs if needed

Forbidden:

- Do not let book sample substitute for longform acceptance.
- Do not cut by arbitrary length or file order.

### #8 Skill / 工程材料路线 smoke

Owned files:

- `scripts/readerlab_v2_quality_gate_adapter.py`
- `scripts/readerlab_v2_runner.py`
- Skill / engineering route tests
- smoke fixture / builder introduced by the worker
- relevant route docs

Forbidden:

- Do not modify GSTACK source.
- Do not add a third GSTACK Skill unless explicitly required after #4.
- Do not put acceptance prose quality into runner string checks.

### #9 Release candidate 复核

Owned files:

- RC checklist / audit report introduced by the worker
- `docs/current-task.md`
- `docs/agent-run-ledger.md`
- release status docs introduced by the worker

Forbidden:

- Do not merge PRs.
- Do not claim production ready.
- Do not skip Codex Review.

## GitHub Development Workflow

主控必须按 SOP 执行：

1. 一个 issue 一个 worktree。
2. 一个 worker 只处理一个 issue。
3. 一个 issue 一个 PR。
4. Worker 只改 owned files。
5. Worker 不得 merge、不回滚别人改动、不删除分支。
6. PR 必须包含 `Closes #N`、改动文件、验证方式、剩余风险。
7. 主控触发 Codex GitHub Review。
8. Review finding 派回原 worker。
9. 主控只能标记 ready-to-merge candidate。
10. 最终 merge 必须等待用户明确批准。

## Acceptance For This RFC

本 RFC 通过后，才能开始派 worker 开发 #2。

本 RFC 自身的完成标准：

- 质量核验路径覆盖合同、内容、人类读者、产品预期、无上下文 Agent 复用。
- 可分享 Skill 包包含 / 排除边界已落入 `docs/readerlab-v2-package-boundary.md`。
- 参数验证标准明确。
- GitHub issue owned files 和 forbidden 范围明确。
- 开发方式遵守 Controller-Agent GitHub Workflow SOP。
- 不把任何当前能力说成 production ready。
