# Phase 4 第二个 Skill 试点候选

## 候选

`codex-claude-bridge`

来源路径：`/Users/tianqiang/技能项目/skills-canonical/packages/codex-claude-bridge`

## 为什么选它

这个包比 `gstack/spec` 更适合测试技术负责人页上限：它不是单纯流程 prompt，而是一个真实的 Codex 监督 Claude 执行循环的桥接系统。

已观察到的材料结构：

- Skill 主文档：`SKILL.md`
- 主脚本：`scripts/bridge.py`，4282 行
- fake matrix 测试：`scripts/test_bridge_fake_matrix.py`，2478 行
- hook 安装脚本：`scripts/install_project_hook.py`，111 行
- hook 回调：`scripts/hooks/claude_hook_notify.py`
- prompt 模板：`scripts/prompts/claude_worker.md`、`scripts/prompts/codex_supervisor.md`
- schema：`scripts/schemas/codex_decision.schema.json`
- 项目状态文档：`docs/dev-state.md`、`docs/decisions.md`、release notes

## 它能测试什么

- 真实脚本和状态目录如何配合。
- hook 事件、bridge state、dispatch、recover、audit report 的数据流。
- 为什么需要 lock、token、fallback exit event、bounded stdout/stderr tail。
- 技术负责人页能否用非工程师语言讲清“Codex 做决策层，Claude 做执行层”的工程边界。
- 资产卡能否沉淀“监督循环”“hook-driven completion”“bounded acceptance note”等可复用设计。

## 建议

报给用户选择为 Phase 4 第二个 Skill 试点候选。用户确认前不生成试点包。
