# T2.24 分环节成本汇总（最终）

summary-status: FINAL
terminal: TRANSFER_SAMPLE_ACCEPTED
run-start-utc: 2026-07-22T19:03:28.797776+00:00
p1-v01-ready-at-utc: 2026-07-22T19:12:17.284174+00:00
p1-v01-feedback-observed-at-utc: 2026-07-23T04:51:29.679072+00:00
p1-v02-ready-at-utc: 2026-07-23T04:52:17.189909+00:00
p1-verdict-observed-at-utc: 2026-07-23T05:16:41.934126+00:00
p2-ready-at-utc: 2026-07-23T05:23:43.388276+00:00
p2-verdict-observed-at-utc: 2026-07-23T05:38:38.151486+00:00
p3-wait-start-utc: 2026-07-23T05:59:25.902352+00:00
p3-verdict-observed-at-utc: 2026-07-23T06:12:29.610115+00:00
usage-ledger-sha256: 6909227bd80cc30344e60c0f110d1438887adcce857e058907f35785777defa3
p2-verdict-sha256: 34cd5e15cb8d80315b680ef8eec7700c5ebbe8e8cc6368d9094cbf3b6cec3849
product-verdict-sha256: 2b4004aa3e8b12b89eeca58cff26991d6cc7dd0ad94e10f800ee0ebde6f717eb
end-to-end-review-sha256: 75282fae7adb46be10b0ac9ca9288f7b589cb54a515fd8662ace78677f151487

## 当前结论

两堂课均已完成来源审核、原 Expert 最小修正、Writer 交接、独立 Writer 编辑、忠实性检查和确定性装配。产品负责人已接受两段陪读、锚点、互补性和完整章节，终局为 `TRANSFER_SAMPLE_ACCEPTED`。

宿主对 16 次模型调用均未返回 provider usage 或精确 invocation ID，本机也没有已获准且可用的确定性 tokenizer。因此服务端 token 与可见文本 token 覆盖率均为 0/16，全部保持 `unknown`，没有用字符数代替。

## 分环节

| 环节 | 模型调用 | 服务端 token | 可见文本 token | 累计工作时间 | 实际墙钟 | 联网工具耗时 | 重试 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 确定性材料选择 | 0 | 不适用 | 不适用 | 0 ms | 1 ms | 0 ms | 0 |
| 单 Expert 自主发现 | 1 | unknown | unknown | 100,122 ms | 100,122 ms | unknown | 0 |
| 独立比较 + 广度旁路 | 2 | unknown | unknown | 246,412 ms | 153,169 ms | unknown | 0 |
| 同源 Expert 展开 | 3 | unknown | unknown | 330,754 ms | 184,754 ms | unknown | 0 |
| 两路来源审核 | 2 | unknown | unknown | 354,883 ms | 220,179 ms | 24,500 ms | 3 次工具内重试 |
| 两路最小来源修正 | 2 | unknown | unknown | 182,185 ms | 104,589 ms | 0 ms | 0 |
| 两路 Writer 交接 | 2 | unknown | unknown | 140,564 ms | 83,082 ms | 0 ms | 0 |
| 两路 Writer 编辑 | 2 | unknown | unknown | 172,788 ms | 104,184 ms | 0 ms | 0 |
| 两路独立忠实性检查 | 2 | unknown | unknown | 63,956 ms | 53,555 ms | 0 ms | 0 |
| P1 第一版机械装配 | 0 | 不适用 | 不适用 | 0 ms | 1 ms | 0 ms | 0 |
| P1 中文界面返工 | 0 | 不适用 | 不适用 | 0 ms | 47,511 ms | 0 ms | 0 |
| P2 中文审阅包装配 | 0 | 不适用 | 不适用 | 0 ms | 1 ms | 0 ms | 0 |
| P3 完整章节装配 | 0 | 不适用 | 不适用 | 0 ms | 1 ms | 0 ms | 0 |

并行阶段的“累计工作时间”是各调用相加；“实际墙钟”是该阶段首个派发到最后完成，二者未混写。

## 截至 P3 的总计

- 实际模型调用：16
- 模型调用重试：0
- 工具内技术重试：3；均保留在原模型调用内，没有覆盖失败模型调用
- 模型累计工作时间：1,591,664 ms
- 全流程模型关键路径：1,003,634 ms
- 来源审核联网工具耗时：24,500 ms
- P1 第二版产品判断等待：1,464,744 ms
- P2 产品判断等待：894,763 ms
- P3 产品判断等待：783,708 ms
- 正式 run 到最终 P3 判词的完整墙钟：40,140,812 ms
- provider token 覆盖率：0/16
- 可见文本 token 覆盖率：0/16

## 技术失败与额外成本

- 没有模型调用重试，因此没有可单列的重复模型 token。
- 两路来源审核共有 3 次工具内重试：一次依赖检查路径、两次联网结果呈现。宿主没有返回每次重试的独立耗时；来源审核全部联网工具总耗时为 24,500 ms，不能把其中未知部分伪造为重试耗时。
- P1 v01 → v02 的 47,511 ms 是产品界面技术返工，单列于完整运行时间，不计入模型生产时间。

## 调用身份与数据完整度

- `usage-ledger.jsonl` 当前 16 行，每次实际模型调用一行；所有已知 thread ID、模型档位、UTC、输入输出哈希、工具次数和重试原因均已记录。
- 原发现 Expert 及其两个对象分支为满足同源展开、最小修正和锚点交接而合法复用 thread；每次复用均是独立 ledger 行。
- 宿主未提供 invocation ID，字段保持 `null`，没有自造服务端标识。
- 缓存输入、隐藏推理、provider token 和 visible token 均为未知，不以零替代。
- P3 判词已写入；本稿与 ledger 在 T2.24 收口时冻结，不再作为中间态继续追加。
