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

确定性输入清单：

- Skill entry: `.agents/skills/readerlab/SKILL.md`
- Skill checks: `.agents/skills/readerlab/checks/activation-checklist.md`、`.agents/skills/readerlab/checks/readiness-checklist.md`
- Skill eval cases: `.agents/skills/readerlab/evals/trigger-cases.json`、`.agents/skills/readerlab/evals/output-cases.json`
- Skill examples: `.agents/skills/readerlab/examples/input-request.json`、`.agents/skills/readerlab/examples/route-decision-example.json`
- Core scripts: `scripts/readerlab_trace_validator.py`
- Conditional runtime script: `scripts/readerlab.py` can enter the shareable package only after #4 removes hardcoded current-user local path defaults and the package audit confirms no LifeAtlas fixed path remains.
- Supporting validators: `scripts/readerlab_fullbook_demo_validate.py`、`scripts/readerlab_review_pack_validate.py`
- Product docs: `docs/product-spec.md`、`docs/readerlab-package-spec.md`、`docs/eval-gates.md`、`docs/decisions.md`
- Method docs: `docs/ai-reading-method.md`、`docs/high-order-explanation-method.md`、`docs/technical-cofounder-method.md`
- Contracts: `docs/contracts/`
- Smoke fixtures: `tests/fixtures/readerlab/contract-validator-proof-v0/`
- Minimal package tests: only tests introduced or selected by #3 that depend exclusively on the included package fixtures.
- Package boundary docs: `docs/readerlab-v2-package-boundary.md`、`docs/readerlab-v2-shareable-skill-prd.md`、`docs/rfc/2026-07-04-readerlab-v2-installable-skill-package.md`

不得作为可分享包最小测试直接纳入：

- `tests/test_readerlab_trace_validator.py`，当前仍依赖未列入包内的 private-material-validation demos。
- `tests/test_fullbook_demo_validate.py` 和 `tests/test_review_pack_validate.py`，当前仍依赖 `docs/reports/`，而 reports 明确排除在可分享包之外。

这些测试可以继续作为研发仓库 regression；若 #3 要把它们纳入发布包，必须先改造成只依赖包内 fixtures 的 smoke tests。

`tests/fixtures/readerlab/comment-replay/fixtures/` 目前仍依赖包外 demo material，不能作为可分享包 fixture 直接纳入。只有在后续 issue 提交自包含、去私有化、能独立运行的 comment replay demo 后，才允许把它加入包清单。

Because `scripts/readerlab.py` is owned by #4 for configuration externalization, #3 may build the manifest, exclusion rules, and audit shell after #2, but it must not ship a runtime package that includes `scripts/readerlab.py` before #4 has removed current-user path coupling.

可选但必须先提交后才能纳入的 V2 输入：

- `scripts/readerlab_v2_runner.py`
- `scripts/readerlab_v2_case_assembly.py`
- `scripts/readerlab_v2_quality_gate_adapter.py`
- `experiments/readerlab-v2/agent-prompts/`
- `experiments/readerlab-v2/step-contracts/`
- `experiments/readerlab-v2/route-modules/`
- V2 smoke fixtures and tests introduced by #6/#7/#8

如果某项仍是未提交本机文件，#3 包构建器不得把它当成当前包输入；必须等负责该项的 issue 提交后再加入 include inventory。

目标包顶层建议：

```text
readerlab/
  SKILL.md
  checks/
  evals/
  examples/
  scripts/
  docs/
  contracts/
  fixtures/
  tests/
  PACKAGE_BOUNDARY.md
```

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
