# Copy Prompt for GPT Pro

请审查这个 ReaderLab checkpoint。不要重写《埃隆之书》总结，也不要直接写 ReaderLab Skill。

你应先读：

1. `docs/reports/readerlab-elon-checkpoint-v0/00_GPT_PRO_REVIEW_BRIEF.md`
2. `docs/current-task.md`
3. `docs/reports/readerlab-elon-chapter-loop-v0/reader/16_ReaderLab全书总结_阅读页.md`
4. `docs/reports/readerlab-elon-chapter-loop-v0/audit/evals/16_ReaderLab全书总结.eval.md`
5. `docs/reports/readerlab-elon-chapter-loop-v0/audit/evals/17_baseline横向对比.eval.md`

按需再读：

- `docs/reports/readerlab-elon-checkpoint-v0/02_OPTIONAL_ATTACHMENTS.md`
- 四个 baseline 原文
- 15 个章节阅读页
- contract JSON 和 rounds

请重点回答：

1. ReaderLab 当前是否真的完成了读者层验证？
2. ReaderLab / GPT Pro 方案的四个低分项是否判断准确？
3. 下一阶段是否应该重建 ReaderLab 方法内核，而不是继续拼贴 baseline 字段？
4. 如果是，方法内核应该是什么执行流程？
5. 怎样设置硬门槛，防止再次只吸收字段、不吸收逻辑？
6. 是否存在更简单的产品路线，能避免 ReaderLab 过度复杂化？

请输出：

- `Verdict`
- `What is proven`
- `What is not proven`
- `Core risk`
- `Recommended next method kernel`
- `Stop conditions`

