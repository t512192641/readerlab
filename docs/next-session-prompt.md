# ReaderLab Next Session Prompt

本文件是从 `docs/current-task.md` 派生的启动提示，不是事实源。若两者冲突，以 `docs/current-task.md` 为准。

```text
/goal 从 /Users/tianqiang/Documents/读书伴侣 继续 ReaderLab《埃隆之书》单书闭环。

先读两个入口文件：
1. AGENTS.md
2. docs/current-task.md

启动阶段不要读取 dev-state、progress、next-session-prompt、旧 fullbook、旧 bakeoff、旧报告、长 ledger 或原始聊天。docs/current-task.md 是当前执行事实唯一入口；它会告诉你哪些文件只有在具体动作发生时才需要读取。

当前目标：
- 继续章节阶段，不进入全书总结、final boss baseline、方法论 / Skill 草案或外部书验证。
- 下一章是 `组织设计 / v101-16`。
- 当前覆盖是 15 个正文级章节中 2 个 pass、13 个 not_started。

执行方式：
1. 先只基于 docs/current-task.md 判断当前步骤，不展开其他状态文档。
2. 从 EPUB 准备 `组织设计 / v101-16` 的一手正文输入。
3. 主控准备 8-15 个正文锚点、baseline summary trap、上一轮硬问题和允许镜头；只有 docs/current-task.md 的摘要不足时才读取 high-order 方法全文。
4. 调用写作 agent 产出 reader-facing 自然讲解；写作 agent 不得读取 final boss baseline 或旧全书总结。
5. 调用读者评价 agent 按硬门槛和 12 分 rubric 打分；只有 docs/current-task.md 的通过线不足以支撑评价时才读取 eval gate。
6. 主控回收评价；通过才落地 reader/audit，并在需要更新状态时读取章节队列和轮次文件。

通过线：
硬门槛全过，读者分至少 10/12，读者评价 agent 给出 pass，且没有 P0/P1。

验证：
- 每章落地前检查 reader-facing 不残留内部字段。
- contract JSON 用 `python3 -m json.tool` 检查。
- 正式补丁后运行 `python3 tests/test_readerlab.py` 和 `git diff --check`。

暂停条件：
- 某章五轮仍未 pass。
- 正文源缺失或无法抽取。
- 写作 agent 使用 final boss baseline 或旧全书总结。
- reader-facing 暴露内部字段。
- 章节未全 pass 前进入全书总结或 final boss。
```
