# Current Task

## Authority

本文件是当前执行事实的唯一入口。若 `docs/dev-state.md`、`docs/progress.md`、`docs/next-session-prompt.md`、旧报告或旧 handoff 与本文件冲突，以本文件为准。

## 当前切片

继续 ReaderLab《埃隆之书》单书闭环。章节阶段已经完成，ReaderLab 自己的全书总结已经通过，baseline 阶段已启用并完成横向对比。当前阶段是 GitHub checkpoint / GPT Pro review，不要进入方法论 / Skill 草案或外部书验证，除非用户在 review 后明确启动。

完整链路是：

```text
15 个正文级章节全部 pass
-> ReaderLab 自己的全书总结 pass
-> 仓颉 / 李继刚 / book-to-skill / 乔木等基线总结完成或纳入
-> 读者评价 agent 横向对比
-> 主控提炼可迁移 ReaderLab 方法论 / Skill 草案
-> 验证通过
```

当前覆盖：

- 正文级章节总数：15。
- 已通过：15，`成功之道`、`打造卓越团队`、`组织设计`、`极致紧迫感`、`我们必须实干制造`、`成为创始人`、`打造特斯拉`、`创建太空探索技术公司`、`建设我们的未来`、`丰饶时代`、`我们的生存风险`、`成为多行星物种`、`活出目标人生`、`物理学家式思考`、`工程学的价值`。
- 未开始：0。
- 下一章：none。章节阶段已完成。
- 全书总结：pass。ReaderLab 自己的全书总结已通过，阅读页为 `docs/reports/readerlab-elon-chapter-loop-v0/reader/16_ReaderLab全书总结_阅读页.md`。
- baseline / 横向对比：pass。四个 baseline 已读取并纳入，横向对比记录为 `docs/reports/readerlab-elon-chapter-loop-v0/audit/evals/17_baseline横向对比.eval.md`。
- final boss baseline：enabled。当前已满足并启用 baseline 阶段；未做外部书验证。
- 方法论 / Skill 草案：not_started。
- GitHub checkpoint / GPT Pro review packet：prepared。入口为 `docs/reports/readerlab-elon-checkpoint-v0/00_GPT_PRO_REVIEW_BRIEF.md`。

## 默认读取与动作触发

启动时只读 `AGENTS.md` 和本文件。不要因为本文件列出路径，就在启动阶段展开读取。

执行中按动作触发读取：

- 要更新章节状态时，读 `docs/reports/readerlab-elon-chapter-loop-v0/chapter-queue.md`。
- 要追加本章循环记录时，读 `docs/reports/readerlab-elon-chapter-loop-v0/rounds.md`。
- 要给写作 agent 准备完整方法输入，且本文件里的摘要不足时，读 `docs/high-order-explanation-method.md`。
- 要给读者评价 agent 准备完整验收输入，且本文件里的通过线不足时，读 `docs/eval-gates.md`。
- 要确认章节阶段边界或 baseline shield 时，读 `docs/reports/readerlab-elon-chapter-loop-v0/README.md`。

按需读取：

- 产品边界：`docs/product-spec.md`
- 包结构：`docs/readerlab-package-spec.md`
- 稳定路径和工具状态：`docs/dev-state.md`
- 耐久决策：`docs/decisions.md`，优先 D-046 之后
- 运行历史：`docs/agent-run-ledger.md` 顶部最新两条
- baseline 研究线索：`docs/research-log.md`

不要启动时通读旧 fullbook、bakeoff、long reports 或历史账本。

## 下一步

章节阶段已经完成：15 个正文级章节全部 `pass`。

ReaderLab 自己的全书总结已通过，baseline 阶段已启用并完成横向对比。当前下一步是把完整 checkpoint 同步到 GitHub，并让 GPT Pro 审查 `docs/reports/readerlab-elon-checkpoint-v0/00_GPT_PRO_REVIEW_BRIEF.md` 及其必读 / 可选附件。ReaderLab 可迁移方法论 / Skill 草案尚未启动；启动前不得读取外部书验证材料，不得把 baseline 结果直接当成最终方法论。

## 章节通过线

硬门槛任一失败则不能 `pass`：

- 一手正文没有被 AI 讲解替代。
- reader-facing 不暴露 `source refs`、`claim trace`、`lens score`、`machine/human status` 等内部字段。
- 有明确升维问题，不是章节摘要。
- 有正文内部机制链。
- 至少一个镜头反向照亮正文，不抢正文。
- 自然完成吸收 / 降级 / 拒绝。
- 不美化长工时、创伤、强控制或英雄崇拜。
- 不把局部章节升格成全书结论。

读者评分六项，每项 0-2：重新理解、正文贴合、机制清晰、镜头有效、边界锋利、表达穿透。

通过条件：硬门槛全过，读者分至少 `10/12`，读者评价 agent 给出 `pass`，且没有 P0/P1。

## 错误退出

- 某章五轮仍未 `pass`：停止向后推进，记录 failure report 和方法缺口，不进入全书总结。
- 正文源缺失：标记 `missing_source`，先修来源，不用摘要代替正文。
- 写作 agent 使用 final boss baseline 或旧全书总结：该轮作废，重跑该章。
- reader-facing 暴露内部字段：该轮不能 `pass`。
- 章节未全 `pass` 前进入全书总结或 final boss：立即停止并纠正计划。
- ReaderLab 自己的全书总结未 `pass` 前进入 baseline 或 final boss：立即停止并纠正计划。

## Stable Paths

- EPUB：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- 章节队列：`docs/reports/readerlab-elon-chapter-loop-v0/chapter-queue.md`
- 章节轮次：`docs/reports/readerlab-elon-chapter-loop-v0/rounds.md`
- 仓颉 baseline：`docs/reports/readerlab-elon-method-bakeoff-v0/cangjie-only.md`
- 李继刚 baseline：`docs/reports/readerlab-elon-method-bakeoff-v0/ljg-deepread-only.md`
- book-to-skill baseline：`docs/reports/readerlab-elon-method-bakeoff-v0/book-to-skill-only.md`
- 乔木 baseline：`docs/reports/readerlab-elon-method-bakeoff-v0/qiaomu-coread-only.md`

Baseline 只在所有章节 pass 且 ReaderLab 自己的全书总结 pass 后启用；当前已满足前置条件，baseline 阶段已启用并完成横向对比。下一步是方法论 / Skill 草案，但尚未启动。
