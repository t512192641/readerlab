# ReaderLab Progress

## Authority Boundary

本文件是历史进度快照，不是当前任务权威。当前执行状态、下一步和阶段门槛以 `docs/current-task.md` 为准。

## 2026-07-01 Snapshot

ReaderLab 当前方向已经从早期 Skill 包翻译 / 结构化提炼实验，转为正文优先的复杂材料陪读包：

```text
一手正文轨 + AI 陪读轨 + audit/contracts/eval 事实层
```

当前《埃隆之书》checkpoint 经 GPT Pro review 后，状态口径已修正：

- `chapter_high_order_explanation_pass`: `15/15`。
- `full_book_reader_synthesis_pass`: `1/1`。
- `baseline_capability_audit_pass`: `1/1`。
- `reader_package_not_verified`。
- `transferable_method_kernel_probe_pass`: `2/2`，仅限 `readerlab-method-kernel-v0` 的 `组织设计` 和 `打造特斯拉` 两章探针。
- `transferable_method_kernel_pass`: `not_verified`。
- `skill_draft_not_started`。
- `private_material_validation_local_pass`: `2/2`。
- `formal_skill_delivery_design_ready`: `yes`。
- `trace_validator_implemented`: `not_started`。
- `comment_replay_verified`: `not_verified`。
- `public_external_material_validation_not_started`。

这个快照不证明 `reader_package_pass`、product ready、生成器能力、正式 Skill 或外部书泛化能力。

## Module Snapshot

| 模块 | 状态 | 说明 |
|---|---|---|
| 产品形态 | close-for-now | 正文优先陪读包方向已确认。 |
| 一手正文轨 | not_verified | 书籍/长文必须保留原样正文；当前章节讲解页没有证明完整 Body Track。 |
| 高阶讲解方法 | working | `high-order-explanation.v1` 已用于 15 章讲解和全书总结，但只证明讲解能力。 |
| 方法核 | probe_pass | `readerlab-method-kernel-v0` 两章探针通过；尚未证明可迁移。 |
| 读者验收 | working | 12 分 rubric 已定义；新增 Body Track Gate 和方法核失败条件。 |
| 技术负责人 / 设计资产层 | working | 方法已定义，仍需真实复杂材料验证。 |
| 生成器机制化 | not_ready | proof 工具不能冒充完整生成器。 |

## Cleanup Note

历史上本文件曾维护长进度板和分数估算，容易与 `current-task.md`、`dev-state.md` 和 `next-session-prompt.md` 产生重复事实。自 2026-07-01 起，本文件只保留低频历史快照；新会话不应启动读取本文件。
