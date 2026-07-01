# Agent Run Ledger

本文件只保留阶段级摘要。旧过程报告和长日志已清理；需要查逐步细节时使用 git 历史或 Codex 会话。

## 2026-07-01 MEM cleanup

- 将 ReaderLab 当前事实压缩到 `docs/current-task.md`、`docs/dev-state.md`、`docs/decisions.md`。
- 删除旧 `docs/reports/`、`docs/drafts/`、旧过程文档和 DBS 测试输入。
- 将 validator 仍需要的样本迁移到 `tests/fixtures/readerlab/`。
- 将《埃隆之书》整书章节解读复制到 LifeAtlas：
  `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/elon-book__readerlab-demo_20260629/10_中文精读/03_ReaderLab整书章节解读/`
- 删除 LifeAtlas 临时批注测试目录：`readerlab-ui-replay-test`。
- 明确 `gstack` 是用户要继续学习的 Skills 材料，本轮未删除、未移动、未重写。

## 2026-07-01 Trace hardening

- repo-local Skill 保持在 `.agents/skills/readerlab/`。
- `scripts/readerlab_trace_validator.py` 增加 `trace-validation.json` 检查。
- `tests/test_readerlab_trace_validator.py` 增加坏引用负向测试。
- A/B validator fixtures 可检查 reader-facing paragraph 到 anchor / claim / candidate 或 gate 的连接。

## 2026-07-01 Repo-local Skill trial

- 创建并激活 repo-local ReaderLab Skill。
- 完成 smoke test 和 Meta Skills acceptance。
- 状态只允许称为 `readerlab_skill_repo_local_trial: active`，不得称为 production ready、global install、public validation pass 或 transferable method pass。

## 2026-07-01 Real Obsidian replay

- 用户在 Obsidian 中完成真实批注。
- Codex 读取到 `tandem-comments` 插件存储。
- 结果为 `pass_with_warning`：插件存储和回读可用，但用户选中的是可见 anchor-list entry，不是严格正文段落 prose selection。

## 2026-07-01 Formal Skill draft

- 完成正式 ReaderLab Skill draft、trigger/output eval、forward test、review studio 和 activation hardening。
- 后续已由 repo-local Skill 替代；历史 draft 已清理。

## 2026-06-30 to 2026-07-01 Method and package validation

- 完成 two-demo internal run、private material validation、comment replay fixture、formal Skill delivery design、formal Skill draft contract。
- 这些长过程报告已清理；当前机器验证样本保留在 `tests/fixtures/readerlab/`。

## 2026-06-29 Elon book chapter loop

- 完成《埃隆之书》章节级 ReaderLab 解读和全书总结。
- 最终读者页已迁移到 LifeAtlas 埃隆书目录。
- 仓库内旧章节循环过程报告已清理。
