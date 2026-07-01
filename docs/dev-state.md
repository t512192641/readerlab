# Dev State

## Purpose

本文件只保存稳定事实、路径和验证命令；当前任务以 `docs/current-task.md` 为准。

## Stable Paths

- 仓库：`/Users/tianqiang/Documents/读书伴侣`
- repo-local Skill：`.agents/skills/readerlab/SKILL.md`
- 生成/校验脚本：`scripts/readerlab.py`、`scripts/readerlab_trace_validator.py`
- 单元测试：`tests/test_readerlab.py`、`tests/test_readerlab_trace_validator.py`
- 最小 validator fixtures：`tests/fixtures/readerlab/`
- LifeAtlas 270 目录：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料`
- 《埃隆之书》当前阅读目录：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629`
- 《埃隆之书》整书 ReaderLab 解读：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629/10_中文精读/03_ReaderLab整书章节解读/`
- `gstack` 学习材料：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`

## Core Docs

- `README.md`：项目说明。
- `AGENTS.md`：项目规则和启动顺序。
- `docs/current-task.md`：当前唯一执行事实源。
- `docs/dev-state.md`：稳定路径和命令。
- `docs/decisions.md`：耐久产品/技术决策。
- `docs/agent-run-ledger.md`：历史运行摘要。
- `docs/product-spec.md`、`docs/readerlab-package-spec.md`：产品和包结构。
- `docs/ai-reading-method.md`、`docs/high-order-explanation-method.md`、`docs/technical-cofounder-method.md`：核心方法。
- `docs/contracts/`：事实层 contract。

## Tool State

- `scripts/readerlab_trace_validator.py` 能验证 location-map、claim-ledger、candidate-tournament、annotation-trigger、skillization-gate、trace-validation 和 comment replay fixture 的引用完整性。
- `scripts/readerlab.py` 仍是早期工具集合，不代表完整自动生成器已经完成。
- repo-local Skill 可用于试运行，但不是全局安装版。

## Verification

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation/demos/A_feel_good_productivity --demo tests/fixtures/readerlab/private-material-validation/demos/B_planning_with_files --cases-json tests/fixtures/readerlab/comment-replay/fixtures/comment-replay-cases.json --fixture-dir tests/fixtures/readerlab/comment-replay/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
git diff --check
```

## Boundaries

- `validate` 通过只表示机器规则通过，不表示人工阅读质量通过。
- `gstack` 是用户要继续学习的 Skills 材料，不作为清理对象。
- 不自动写入 LifeAtlas `300/600/800` 正式沉淀区。
- 不把 private/local validation 说成 public external validation。
