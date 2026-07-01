# Current Task

## Authority

本文件是当前执行事实的唯一入口。新会话启动只读：

1. `AGENTS.md`
2. `docs/current-task.md`

旧报告、旧 prompt、旧 handoff、旧聊天和已删除过程文档都不是当前事实源。

## Active Slice

ReaderLab 已进入 **repo-local Skill trial 后的收尾清理与真实小材料试用前**。

当前已完成：

- ReaderLab 产品主线重设为：一手正文轨 + AI 陪读轨 + audit/contracts/eval 事实层。
- repo-local Skill 已激活：`.agents/skills/readerlab/SKILL.md`。
- trace validator 已能检查 `trace-validation.json` 中 reader-facing paragraph 到 anchor / claim / candidate 或 gate 的连接。
- 最小机器 fixtures 已移到 `tests/fixtures/readerlab/`。
- 《埃隆之书》ReaderLab v1 本地包已重新生成到 LifeAtlas：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-v1_20260701/`
- LifeAtlas 270 目录已清理旧 ReaderLab 生成包：`dbs-suite`、`dbs-suite__v2.15.1_096f726`、`gstack`、Elon 旧 `02/20/40` 过程目录已删除。
- 新的 Obsidian 阅读面决定：正文、陪读和用户批注必须在同一个可批注 Markdown 阅读页发生；不再默认拆成正文文件、AI 陪读文件和预设批注问题文件。

当前仍不能声明：

- production ready
- global Skill installed
- public external validation pass
- `transferable_method_kernel_pass`
- real Obsidian body-prose annotation full pass

## Current Status

- `readerlab_skill_repo_local_trial`: `active`
- `readerlab_skill_repo_local_path`: `.agents/skills/readerlab/`
- `trace_validator_reader_paragraph_trace`: `implemented`
- `trace_validation_fixtures`: `tests/fixtures/readerlab/`
- `real_obsidian_ui_replay`: `pass_with_warning`
- `real_obsidian_ui_body_prose_selection`: `not_verified`
- `reader_package_not_verified`
- `transferable_method_kernel_pass`: `not_verified`
- `public_external_material_validation_not_started`

## Open Skill Work Items

- `RL-SKILL-001`: Elon 试生成暴露出旧 Skill/规格仍偏向“正文轨/AI 陪读轨/批注问题文件”分离结构。已改为默认单页阅读面：每个阅读单元一个可批注 Markdown，正文和陪读同页；不得生成预设批注问题文件。后续需要用真实小材料再跑一次，确认 Skill 不再产出三文件结构。

## Next Action

下一步只做两件事：

1. 用 `.agents/skills/readerlab/` 做一次真实小材料 ReaderLab package 使用测试。
2. 之后再补一次严格正文段落直接选择 Obsidian replay。

`gstack` 原始 Skills 源仓库是用户要继续学习的材料，不删除、不移动。LifeAtlas 270 下旧 `gstack` ReaderLab 生成解读包不是原始 Skills，已清理。

## Verification Commands

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation/demos/A_feel_good_productivity --demo tests/fixtures/readerlab/private-material-validation/demos/B_planning_with_files --cases-json tests/fixtures/readerlab/comment-replay/fixtures/comment-replay-cases.json --fixture-dir tests/fixtures/readerlab/comment-replay/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
git diff --check
```

## Stop Conditions

立即停止并纠正状态，如果出现：

- 删除或移动 `/Users/tianqiang/技能项目/skills-canonical/packages/gstack` 原始 Skills 源仓库。
- 删除 270 目录下用户仍要阅读的电子书或正式阅读材料。
- 全局安装 ReaderLab Skill 到 `/Users/tianqiang/.codex/skills/`。
- 把 repo-local trial 说成生产可用、全局安装、public validation pass 或 transferable method pass。
- 把 `real_obsidian_ui_replay: pass_with_warning` 说成 full pass。
