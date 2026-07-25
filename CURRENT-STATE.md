# ReaderLab 当前状态兼容入口

> 生命周期：`compatibility-pointer`
> owner：`none`
> 迁移日期：2026-07-25

本文件不再拥有当前任务、run、产品判词、停止点、允许动作、禁止动作、工程事实或下一生产
授权，也不得重新写入这些动态字段。

- 当前唯一执行切片：[`docs/current-task.md`](docs/current-task.md)
- 当前已验证工程事实与缺口：[`docs/dev-state.md`](docs/dev-state.md)
- 持久工程决定：[`docs/decisions.md`](docs/decisions.md)
- 运行与清理历史：[`docs/agent-run-ledger.md`](docs/agent-run-ledger.md)
- 可复用研究索引：[`docs/research-log.md`](docs/research-log.md)

保留本路径只为兼容历史报告、冻结收据和旧链接；所有当前入口必须直接读取标准 MEM owner，
不能把本兼容页恢复成第二份状态正文。
