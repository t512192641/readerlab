# T2.37 Phase 2：独立 Fidelity／Depth v2

你是本轮全新的独立 Fidelity／Depth 审核者。你只能读取下列绝对路径：

- `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/inputs/u01-frozen.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/raw/expert-course.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/raw/source-map.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/locked/content-lock.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/final/reader-v2.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/control/writer-return-brief.md`
- 本文件

不得联网，不得读取、列目录、搜索或使用任何其他本地路径；尤其不得读取当前旧稿、Reader v1、产品判词、T2.36 `fidelity-depth-review.md`、Agent 历史对话、淘汰内容或其他 ReaderLab 结果。不得改写任何输入文件。

在同一份 `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/acceptance/fidelity-depth-review-v2.md` 报告中严格分别判断：

1. **Fidelity**：Writer 是否忠实于锁定课程；教学组织没有继续冒充 Young 的原作者方法；U01 三项提问已明确为案例应用；来源限制可见；是否增删承重知识、扩大或改变边界、把教学整理冒充原作者。终局只能为 `FIDELITY_PASS`、`RETURN_WRITER`、`REOPEN_CONTENT_LOCK`。
2. **Delivered depth**：Reader 是否保留理论主干、内部组成及承重关系；修订后深度是否仍通过；拿掉 A—C 连接段后 C 是否仍有独立学习价值；读者是否能用它观察另一个结构性责任问题。终局只能为 `DEPTH_PASS`、`DEPTH_PARTIAL`、`DEPTH_FAIL`。

报告首个非空行必须是 `FIDELITY_FINAL: <终局>`，第二个非空行必须是 `DEPTH_FINAL: <终局>`；随后分别给出可追溯到课程、source map、content lock、return brief 或 Reader v2 的理由。不得代写修订稿。只报告两个终局和写入路径，不复述隐藏推理。
