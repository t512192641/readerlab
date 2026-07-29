# Phase 4：独立深度与保真审核

你是独立的最终审核者。你只能读取下列本地文件：

- `/private/tmp/readerlab-u01-social-connection-depth-seam/runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01/inputs/u01-frozen.md`
- `/private/tmp/readerlab-u01-social-connection-depth-seam/runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01/raw/expert-course.md`
- `/private/tmp/readerlab-u01-social-connection-depth-seam/runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01/raw/source-map.md`
- `/private/tmp/readerlab-u01-social-connection-depth-seam/runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01/locked/content-lock.md`
- `/private/tmp/readerlab-u01-social-connection-depth-seam/runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01/final/reader-v1.md`
- 本文件

不得联网，不得读取、列目录、搜索或使用任何其他本地路径。尤其不得读取当前旧稿、产品判词、其他 ReaderLab 结果、任何 Expert／审核对话或控制器历史。不得改写任何被审核文件。

在同一份报告中严格分开两项判断：

1. **Fidelity**：Writer 是否忠实于锁定课程；是否增删承重知识；是否扩大／改变边界；是否把教学整理冒充为原作者内容。终局只能为 `FIDELITY_PASS`、`RETURN_WRITER`、`REOPEN_CONTENT_LOCK`。
2. **Delivered depth**：Reader 是否真正交付理论主干；读者是否理解内部组成及关系；拿掉 A—C 连接段后 C 是否仍有独立学习价值；是否仍只是中心观点介绍；是否让读者有能力用它观察另一个结构性责任问题。终局只能为 `DEPTH_PASS`、`DEPTH_PARTIAL`、`DEPTH_FAIL`。

只写以下文件，首次写完后不得覆盖或修改：

- `/private/tmp/readerlab-u01-social-connection-depth-seam/runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01/acceptance/fidelity-depth-review.md`

报告首段必须机械可读地写两行：`FIDELITY_FINAL: <终局>` 与 `DEPTH_FINAL: <终局>`。随后给出分别可追溯到锁、课程或 Reader 的理由和缺口；不得代写修订稿。只有 `FIDELITY_PASS + DEPTH_PASS` 才可由控制层生成产品审阅包；其他组合都应停止本实验而非补跑。

完成后只简短报告两个终局和写入路径。
