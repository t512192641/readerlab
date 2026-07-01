# 《埃隆之书》章节循环队列

## Phase Gate

本文件只定义章节循环阶段的队列和进入下一阶段的门槛，不定义整个任务的停止标准。

章节阶段的进入下一阶段门槛是：所有正文级章节都达到 `pass`。这里的 `pass` 指 `chapter_high_order_explanation_pass`，不是 `reader_package_pass`。仅仅“有评价结果”不够；`partial` 和 `fail` 都不能进入全书总结阶段。

整个任务的真实完成顺序是：

```text
所有章节高阶讲解 pass
-> ReaderLab 自己的全书总结 pass
-> 其他 Skills / 方法基线产出全书总结
-> 读者评价 agent 做横向对比
-> 方法核探针 / 用户明确启动后的方法论或 Skill 草案
```

当前不能因为某一章 `pass` 停止，也不能因为所有章节“有结果”停止。
当前也不能把 15 章 `pass` 称为完整 ReaderLab 阅读包通过；完整阅读包另需 Body Track Gate 和包级验收。

## Status Vocabulary

- `pass`：章节高阶讲解 reader-facing 通过；读者评价 agent 给出 `pass`，读者 12 分至少 10/12，且无 P0/P1。它不代表完整阅读包通过。
- `partial`：有价值但未通过，必须进入下一轮或方法调整。
- `fail`：当前方法在该章失败，保留报告；它会阻断进入全书总结阶段，不能被当作阶段完成。
- `not_started`：尚未进入章节循环。
- `missing_source`：尚未准备可循环的一手正文输入。
- `non_chapter`：封面、目录、部件页、附录、年表、书单、致谢、作者页等，不进入章节级高阶讲解循环。

## Current Coverage

当前完成度不是“全书跑过后只有两章通过”，也不是“章节阶段已完成”，而是：

```text
正文级章节总数：15
已循环通过：15
未开始：0
失败：0
partial：0
missing_source：0（EPUB 源已确认存在，但多数章节尚未生成 reader 页）
```

原始 EPUB：

```text
/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub
```

## Queue

| Order | Spine | Title | Status | Notes |
|---:|---|---|---|---|
| 1 | v101-10 | 活出目标人生 | pass | 已通过章节循环，11/12，无 P0/P1。 |
| 2 | v101-11 | 物理学家式思考 | pass | 已通过章节循环，11/12，无 P0/P1。 |
| 3 | v101-12 | 工程学的价值 | pass | 已通过章节循环，11.5/12，无 P0/P1。 |
| 4 | v101-14 | 成功之道 | pass | 已通过章节循环。 |
| 5 | v101-15 | 打造卓越团队 | pass | 已通过章节循环，11/12，无 P0/P1。 |
| 6 | v101-16 | 组织设计 | pass | 已通过章节循环，12/12，无 P0/P1。 |
| 7 | v101-17 | 极致紧迫感 | pass | 已通过章节循环，12/12，无 P0/P1。 |
| 8 | v101-18 | 我们必须实干制造 | pass | 已通过章节循环，12/12，无 P0/P1。 |
| 9 | v101-20 | 成为创始人 | pass | 已通过章节循环，12/12，无 P0/P1。 |
| 10 | v101-21 | 打造特斯拉 | pass | 已通过章节循环，12/12，无 P0/P1。 |
| 11 | v101-22 | 创建太空探索技术公司 | pass | 已通过章节循环，12/12，无 P0/P1。 |
| 12 | v101-24 | 建设我们的未来 | pass | 已通过章节循环，12/12，无 P0/P1。 |
| 13 | v101-25 | 丰饶时代 | pass | 已通过章节循环，11/12，无 P0/P1。 |
| 14 | v101-26 | 我们的生存风险 | pass | 已通过章节循环，11/12，无 P0/P1。 |
| 15 | v101-27 | 成为多行星物种 | pass | 已通过章节循环，11/12，无 P0/P1。 |

## Non-Chapter Spine Items

| Spine | Reason |
|---|---|
| cover | 封面。 |
| v101, v101-1, v101-2, v101-3 | 目录 / 目录相关。 |
| v101-4 | 本书说明。 |
| v101-5 | 前言。 |
| v101-6 | 埃里克欢迎辞。 |
| v101-7, v101-8, v101-9 | 第一部分部件页。 |
| v101-13 | 第二部分部件页。 |
| v101-19 | 第三部分部件页。 |
| v101-23 | 第四部分部件页。 |
| v101-28 | 附加原则。 |
| v101-29 | 69 项核心法则。 |
| v101-30 | 年表。 |
| v101-31 | 推荐书单。 |
| v101-32 | 延伸阅读。 |
| v101-33 | 致谢。 |
| v101-34 | 关于作者。 |

## Next Action

章节阶段已完成：所有 15 个正文级章节都达到 `pass`。

ReaderLab 自己的全书总结已经通过：

- Reader page: `docs/reports/readerlab-elon-chapter-loop-v0/reader/16_ReaderLab全书总结_阅读页.md`
- Contract: `docs/reports/readerlab-elon-chapter-loop-v0/audit/contracts/16_ReaderLab全书总结.contract.json`
- Reader evaluation: `docs/reports/readerlab-elon-chapter-loop-v0/audit/evals/16_ReaderLab全书总结.eval.md`

下一阶段可进入仓颉 / 李继刚 / book-to-skill / 乔木等基线总结或 final boss baseline 准备，但本文件不启动下一阶段，也不授权读取旧全书总结、旧 bakeoff、方法论 / Skill 草案或外部书验证。
