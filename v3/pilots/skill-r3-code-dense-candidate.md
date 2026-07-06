# Phase 4 第二个 Skill 试点候选

## 候选

`gstack/browse`

来源路径：`/Users/tianqiang/技能项目/skills-canonical/packages/gstack/browse`

## 为什么选它

`gstack/browse` 是 GSTACK 内部更适合做第二个 Skill 试点的样本：它不是单一 prompt 流程，而是一个有真实工程结构的浏览器控制系统，能测试技术负责人页是否能把“系统为什么这样设计”讲给非工程读者。

它比 `gstack/spec` 更适合拉高上限：

- `SKILL.md` 入口约 1022 行，包含触发条件、前置状态、运行协议、权限边界和工具调用约束。
- `src/` 下 TypeScript 约 24489 行，覆盖服务端、浏览器管理、CDP、终端 Agent、cookie 导入、写命令、安全分类、会话状态等模块。
- `test/` 下测试约 27321 行，覆盖服务端、权限、安全、CDP、侧边栏、终端会话、cookie、代理、截图、文件投放等行为。
- 主工程文件足够长：`src/server.ts` 约 3170 行，`src/browser-manager.ts` 约 1804 行，`src/cli.ts` 约 1362 行，`src/write-commands.ts` 约 1440 行，`src/terminal-agent.ts` 约 1011 行。

## 它能测试什么

- 技术负责人页能不能解释“为什么浏览器控制要拆成服务端、浏览器管理器、命令层、会话层和安全层”。
- 能不能用非工程师语言讲清 CDP、cookie、截图、文件写入、终端 Agent、SSE / 会话保持这些机制各自解决什么问题。
- 能不能把安全设计讲明白：路径校验、token、来源限制、内容安全、下载清理、代理配置、权限边界。
- 能不能把复杂测试体系讲成产品风险图谱，而不是堆测试文件名。
- 资产卡能否沉淀“浏览器自动化证据链”“会话隔离”“安全出口扫描”“可复用浏览器控制协议”等可复用设计。

## 不选项

不再选择 `codex-claude-bridge`，因为用户明确要求第二个试点仍从 GSTACK 内部选择。

暂不选 `gstack/spec` 或 `gstack/review`，因为它们已经作为前序样本使用过，且更偏流程协议，不足以测试技术负责人页的工程上限。

## 建议

报给用户确认 `gstack/browse` 是否作为 Phase 4 第二个 Skill 试点。用户确认前不生成试点包。
