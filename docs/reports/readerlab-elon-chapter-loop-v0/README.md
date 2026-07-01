# ReaderLab Elon Chapter Loop v0

> Authority boundary: 本文件是章节循环历史报告，不是当前任务源。GPT Pro review 后，章节 `pass` 只能理解为 `chapter_high_order_explanation_pass`。当前事实和下一步以 `docs/current-task.md` 为准。

## Current Phase

历史阶段：当时执行《埃隆之书》完整闭环的章节高阶讲解阶段。

本阶段当时不进入全书总结，不调用或吸收 final boss baseline，不做外部书验证，不开发生成器，不写 LifeAtlas 正式沉淀区。后续已完成 15 章高阶讲解、全书总结和 baseline 横评；但完整 ReaderLab 阅读包仍未验证，正式方法论 / Skill 草案仍未启动。

## Why This Exists

上一轮计划把 final boss baseline 写进了整体方案，但阶段边界表达不够清楚，导致它看起来像马上要执行。当时的正确顺序是：

```text
章节高阶讲解循环全部通过
-> ReaderLab 自己的全书总结通过
-> final boss baseline 对抗
-> 方法核探针 / 用户明确启动后的方法论或 Skill 草案
```

当前最新事实不再由本文件维护，见 `docs/current-task.md`。

## Baseline Shield

以下旧报告和 bakeoff 文件在本阶段只能作为未来 final boss 的候选清单，不能进入章节写作 agent 的输入：

- `docs/reports/readerlab-elon-method-bakeoff-v0/cangjie-only.md`
- `docs/reports/readerlab-elon-method-bakeoff-v0/ljg-deepread-only.md`
- `docs/reports/readerlab-elon-method-bakeoff-v0/book-to-skill-only.md`
- `docs/reports/readerlab-elon-method-bakeoff-v0/qiaomu-coread-only.md`
- `docs/reports/readerlab-elon-full-product-v1/reader/01_主阅读稿.md`

允许主控读取它们来确认“以后有哪些 final boss”，但不得把其中的观点、结构或结论喂给章节写作 agent。

## Final Boss Baseline Locations

当前章节阶段不能使用这些文件作为写作输入；只在 ReaderLab 全书总结 `pass` 后启用。

| Baseline | 已有对照输出 | 本地/研究来源 |
|---|---|---|
| 仓颉 / cangjie-only | `docs/reports/readerlab-elon-method-bakeoff-v0/cangjie-only.md` | `/Users/tianqiang/技能项目/skills-canonical/packages/cangjie-skill` |
| 李继刚式深读 / ljg-deepread-only | `docs/reports/readerlab-elon-method-bakeoff-v0/ljg-deepread-only.md` | 本地未确认可直接调用 Skill；研究线索：`lijigang/ljg-skill-paper`、`lijigang/ljg-skill-fetch`，见 `docs/research-log.md` |
| book-to-skill | `docs/reports/readerlab-elon-method-bakeoff-v0/book-to-skill-only.md` | 本地未确认可直接调用 Skill；研究线索：`apple-ouyang/book-to-skill`、`win4r/book-to-skill`，见 `docs/research-log.md` |
| 乔木共读 / qiaomu-coread-only | `docs/reports/readerlab-elon-method-bakeoff-v0/qiaomu-coread-only.md` | `/Users/tianqiang/技能项目/skills-canonical/packages/qiaomu-anything-to-notebooklm`; `/Users/tianqiang/技能项目/skills-canonical/packages/qiaomu-mondo` |

## Chapter Loop Contract

每章最多五轮：

1. 主控准备输入：正文锚点、baseline summary trap、上一轮硬问题、允许使用的通用镜头。
2. 写作 agent 输出：reader-facing 自然讲解，不暴露内部字段。
3. 读者评价 agent 输出：硬门槛、12 分读者评分、P0/P1/P2 问题、是否有额外收获、是否进入下一轮。
4. 主控回收：把评价转成下一轮约束；如果通过，才落地 reader/audit。

连续两轮卡住时，主控必须降低宏大叙事，回到正文机制链。

## Anti-Overfitting Contract

- 所有方法调整必须写成通用 ReaderLab 规则，不能写成《埃隆之书》专用技巧。
- 每章允许记录 `book observation`，但不能直接升级为 `method rule`。
- 新增 `method rule` 必须说明其跨复杂材料适用性。
- 对长工时、创伤、强控制、英雄叙事和宏大使命，必须使用通用伦理与迁移边界，不为本书开特例。
- 最终方法论 / Skill 草案必须区分通用规则、书籍特例和被拒绝的一次性补丁。

## Reader 12-Point Rubric

先过硬门槛，任一失败则不能 `pass`：

- 一手正文没有被 AI 讲解替代。
- reader-facing 页面不暴露 `source refs`、`claim trace`、`lens score`、`machine/human status` 等内部字段。
- 有明确升维问题，不是章节摘要。
- 有正文内部机制链。
- 至少一个镜头反向照亮正文，不抢正文。
- 自然完成吸收 / 降级 / 拒绝。
- 不美化长工时、创伤、强控制或英雄崇拜。
- 不把局部章节升格成全书结论。

读者验收 12 分为六项，每项 0-2 分：

| 维度 | 2 分 | 1 分 | 0 分 |
|---|---|---|---|
| 重新理解 | 读完产生“原来这章可以这样看” | 有新说法但不稳定 | 只是复述 |
| 正文贴合 | 关键判断能回到正文场景 | 部分贴合 | 脱离正文 |
| 机制清晰 | 能串起因果链 | 有链条但松散 | 只列重点 |
| 镜头有效 | 镜头反向解释正文 | 镜头有启发但偏装饰 | 镜头抢戏或无效 |
| 边界锋利 | 清楚区分可吸收/需降级/必须拒绝 | 有边界但模糊 | 全部泛化 |
| 表达穿透 | 像见识丰富的人陪读 | 像较好的报告 | 像普通总结 |

通过线：硬门槛全过，读者分至少 `10/12`，读者评价 agent 给出 `pass`，且没有 P0/P1 问题。

## Score Separation

`Lens Auction` 的 `>= 7` 是内部镜头筛选分，只决定某个镜头能否进入 reader-facing。

`12/12` 是读者验收分，只判断最终讲解是否对读者有收获。

两套分数不能混用。

## Queue

完整章节队列见 `chapter-queue.md`。

历史上这里记录的是章节循环早期状态。GPT Pro review 后的最新 scoped 状态为：

- `chapter_high_order_explanation_pass`: `15/15`。
- `full_book_reader_synthesis_pass`: `1/1`。
- `baseline_capability_audit_pass`: `1/1`。
- `reader_package_not_verified`。
- `transferable_method_kernel_probe_pass`: `2/2`，仅限 `readerlab-method-kernel-v0`。
- `skill_draft_not_started`。

章节高阶讲解全部 pass 之后也不是任务结束；它不等于完整阅读包通过。

## Final Boss Gate

只有在以下条件全部满足后，才允许进入 final boss：

1. 所有可用章节均完成章节循环并通过。
2. ReaderLab 自己的全书总结完成并通过同一读者 rubric。
3. 主控确认 baseline 不会反向污染已通过章节。

到那时才使用仓颉、李继刚、book-to-skill 和乔木等 baseline 做 blind / side-by-side 对抗。

final boss 之后还需要主控回收横向对比，提炼可迁移的 ReaderLab 方法论 / Skill 草案。那才是本轮《埃隆之书》闭环的最终目标。

## Correct Completion

旧完整交付清单已被 D-052 细化。只有同时满足以下条件，才可以说更高层级交付成立：

1. 15 个章节高阶讲解全部 `pass`。
2. ReaderLab 自己的全书总结 `pass`。
3. 仓颉 / 李继刚 / book-to-skill / 乔木等基线总结完成或已有可用基线被正式纳入。
4. 读者评价 agent 完成横向对比。
5. Body Track Gate 证明完整一手正文轨存在，才能声称阅读包通过。
6. 方法核通过受限探针和后续可迁移性验证。
7. 用户明确启动后，主控才输出正式方法论 / Skill 草案。
8. 验证通过，并明确这只是《埃隆之书》单书闭环，不等于外部书泛化已验证。

## Error Exit

- 某章五轮仍未 `pass`：停止向后推进，记录 failure report 和方法缺口，不进入全书总结。
- 正文源缺失：标记 `missing_source`，先修来源，不用摘要替代正文。
- 写作 agent 使用 final boss baseline 或旧全书总结：该轮作废，重跑该章。
- reader-facing 暴露内部字段：该轮不能 `pass`。
- 章节未全 `pass` 前进入全书总结或 final boss：立即停止并纠正计划。
