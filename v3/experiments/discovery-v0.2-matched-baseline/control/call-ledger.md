# v0.2 调用账本

状态：记录本轮所有有效调用、技术失败和同编号重试；不把失败样本静默删除。

## 固定有效样本

| 组 | 运行编号 | 最终输出 | 状态 |
|---|---|---|---|
| plain | 01—05 | `raw/plain-01.md`—`raw/plain-05.md` | 已完成 schema retry，最终 raw 通过字段检查 |
| professional | 01—05 | `raw/professional-01.md`—`raw/professional-05.md` | 初次输出通过字段检查，待封存 |

## 失败与重试

1. 初次十调用并发派发：Agent 容量拒绝，未形成额外样本；随后发现部分已创建的 plain 运行，按编号收齐，不重复计数。
2. plain-01—plain-05 初次输出：均未遵守冻结的 14 个字段合同，原件保存在候选区 `control/failures/plain-*-attempt-1.md`；每个编号各重试一次，重试结果通过后才替换为正式 raw。
3. professional-05 第一次派发：席位卡路径误指向 v0.1，Agent 按白名单停止，未读取替代文件、未写输出；同一编号重试一次，使用正确 v0.2 卡。

## 计数口径

- 发现组最终有效调用：plain 5 + professional 5 = 10。
- schema／路径失败重试：plain 5 + professional-05 1 = 6；这些不增加组内运行编号。
- 第一阶段门槛复核为独立控制调用，不计入两组样本。
