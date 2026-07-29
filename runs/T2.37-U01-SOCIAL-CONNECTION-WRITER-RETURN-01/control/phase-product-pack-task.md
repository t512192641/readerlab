# T2.37 Phase 3：产品对照包（控制层机械装配）

只有 `fidelity-depth-review-v2.md` 同时为 `FIDELITY_FINAL: FIDELITY_PASS` 与 `DEPTH_FINAL: DEPTH_PASS` 时才执行。本阶段不调用 Agent，不生成新的理论或写作意见。

在此前阶段已停止且双门通过后，控制层才可读取并机械完整复制：

- `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/inputs/u01-frozen.md`
- `/Users/tianqiang/GitHub/t512192641/readerlab/audit/current-runtime-snapshot/u01-u03/direct-output/U01.md`（当前旧稿；此前阶段严禁读取）
- `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/final/reader-v2.md`

旧稿与新 Reader 用安全随机的 A／B 顺序匿名呈现，只标 Version A／Version B，不显示生产方式、Agent、任务号或路线。完整保留 U01 必要上下文。生成 `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/acceptance/product-review.md`，要求产品负责人判断：

1. 哪个版本真正讲清了理论；
2. 哪个版本建立了框架内部结构；
3. 哪个版本让读者知道如何用该框架观察其他问题；
4. 哪个版本与原文连接更自然；
5. 哪个版本更愿意保留；
6. 新版本是否过长、过重或打断阅读；
7. 两个版本是否都不合格。

映射单独写入 `/Users/tianqiang/GitHub/t512192641/readerlab/runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/acceptance/version-key.md`，完成产品审阅包后冻结；产品审阅前不得打开、展示或提示映射内容。若双门未通过，两个文件均不得创建。
