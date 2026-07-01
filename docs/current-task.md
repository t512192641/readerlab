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
- 《埃隆之书》整书章节解读已复制到 LifeAtlas：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629/10_中文精读/03_ReaderLab整书章节解读/`

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

## Next Action

下一步只做两件事：

1. 用 `.agents/skills/readerlab/` 做一次真实小材料 ReaderLab package 使用测试。
2. 之后再补一次严格正文段落直接选择 Obsidian replay。

`gstack` 是用户要继续学习的 Skills 材料，不属于本轮清理对象，不删除、不移动。

## Verification Commands

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation/demos/A_feel_good_productivity --demo tests/fixtures/readerlab/private-material-validation/demos/B_planning_with_files --cases-json tests/fixtures/readerlab/comment-replay/fixtures/comment-replay-cases.json --fixture-dir tests/fixtures/readerlab/comment-replay/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
git diff --check
```

## Stop Conditions

立即停止并纠正状态，如果出现：

- 删除或移动 `gstack`。
- 删除 270 目录下用户仍要阅读的电子书或正式阅读材料。
- 全局安装 ReaderLab Skill 到 `/Users/tianqiang/.codex/skills/`。
- 把 repo-local trial 说成生产可用、全局安装、public validation pass 或 transferable method pass。
- 把 `real_obsidian_ui_replay: pass_with_warning` 说成 full pass。
