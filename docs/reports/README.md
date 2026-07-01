# Reports Boundary

本目录是 ReaderLab 的证据库和历史实验区，不是当前任务源。

这里的报告、样张、bakeoff、assertions、audit 和旧 reader 页保留当时的判断、范围、失败条件和验证证据。它们可以被当前任务按需引用，但不能覆盖 `docs/current-task.md`。

读取规则：

- 默认启动不读本目录。
- 只有 `docs/current-task.md` 指定某个报告路径，或当前动作需要追溯证据、更新章节队列、复核旧样张时，才读取对应文件。
- 旧报告里的“下一步 / 当前 / 本轮 / product ready / final boss”等表述只代表当时实验语境。
- 若报告结论与 `docs/current-task.md` 冲突，以 `docs/current-task.md` 为当前执行事实。
