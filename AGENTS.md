# AGENTS.md

## 项目目的

ReaderLab 把复杂材料转成中文可读、可批注、可讨论、可沉淀的 LifeAtlas 阅读包。材料可以是电子书、长文、Markdown 文档、课程资料、访谈稿、代码文档、Skill 包或混合型资料。

当前 v0.1 的默认前提是：Obsidian + Markdown + Codex + 现有批注插件。gstack 是第一组复杂压力样本，但项目目标不是 gstack 专项，也不是 Skill 专项。所有规则都应优先服务“复杂材料陪读”：先理解材料内容，再拆成读者能理解的模块，并为每个模块生成导读、正文、关联说明和重点旁批；读者在 Obsidian 正文附近批注后，Codex 能读取批注和上下文并就地回复。

## 启动顺序

每个新会话先读最小真相层：

1. `AGENTS.md`
2. `docs/current-task.md`
3. `docs/dev-state.md`
4. `docs/progress.md`
5. 需要决策背景时读 `docs/decisions.md`
6. 需要运行历史或验证证据时读 `docs/agent-run-ledger.md`

不要从旧聊天、旧 prompt 或 Obsidian 当前画面倒推项目事实。当前事实以仓库文件、LifeAtlas 输出和验证命令为准。

## 关键入口

- 生成脚本：`scripts/readerlab.py`
- 单元测试：`tests/test_readerlab.py`
- 项目说明：`README.md`
- 下一会话启动提示：`docs/next-session-prompt.md`
- 当前压力样本输出：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack`
- 当前压力样本源：`/Users/tianqiang/技能项目/skills-canonical/packages/gstack`

## Memory Map

- `docs/current-task.md`：唯一当前执行切片，只放下一步要做什么。
- `docs/dev-state.md`：当前事实、已知缺口、重要路径，不放流水账。
- `docs/progress.md`：模块化进度板；每轮大迭代后记录总进度、增减项、close/working/blocker。
- `docs/decisions.md`：耐久决策，只记录之后会继续约束实现的判断。
- `docs/agent-run-ledger.md`：运行历史、改动摘要、验证命令和结果。
- `docs/research-log.md`：外部研究和可复用候选结论；只在产生新的可复用研究结论时更新。

## 项目边界

- 不新建第二个 LifeAtlas `270_电子书与书籍资料` 目录。
- 不移动、软链或改写 gstack 源仓库。
- 不新增依赖，除非用户明确批准。
- 不自动写入 LifeAtlas 的 `300/600/800` 正式沉淀区。
- 不自己发明批注系统；优先适配 Obsidian 现有批注插件或 Markdown 原生批注格式。
- 不让 AI 替代人的第一次阅读判断；AI 预处理只负责降低阅读门槛，Codex 回复围绕人的批注和附近上下文。
- 未完成 Skill 不生成占位阅读页，只在主控清单和 manifest 中保留目标路径。
- 不把当前样本包的特殊结构写成 ReaderLab 的通用规则；gstack 只用于暴露和验证复杂材料阅读化问题。
- 面向读者的正文必须服务理解主线；完整原文、执行外壳、代码块、脚本细节和审计证据可以放入附录或包级机制页，不能反复污染每个模块的主阅读页。
- AI 生成的导读和重点旁批是必要的阅读辅助，不能删除；但它们不能替代一手主体内容。
- 主阅读页应尽量保留材料的一手主体信息；命令行、重复执行协议和机器细节可以从主线剔除，改放附录或机制说明。
- 关联模板、脚本、参考资料必须单独展示，不能冒充材料主体。
- 重点与亮点不强行凑数；没有真正值得标的内容时可以为空或写“无特别高亮”。

## 验证命令

```bash
python3 tests/test_readerlab.py
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --skill unfreeze
python3 scripts/readerlab.py validate /Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/gstack --require-complete
```

当前阶段 `--require-complete` 应该失败，因为整包还没有完成。
