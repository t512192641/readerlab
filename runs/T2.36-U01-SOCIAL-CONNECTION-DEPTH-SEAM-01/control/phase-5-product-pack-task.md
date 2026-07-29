# Phase 5：产品对照包（控制层机械装配）

只有 Phase 4 为 `FIDELITY_PASS + DEPTH_PASS` 时才执行。本阶段不创建新语义内容，不调用 Agent，不让任何此前角色读取旧稿。

控制层从以下固定文件机械完整复制：

- U01 运行内冻结原文；
- 当前旧稿 `audit/current-runtime-snapshot/u01-u03/direct-output/U01.md`；
- 新 Reader `final/reader-v1.md`。

把旧稿与新 Reader 用安全随机的 A／B 顺序匿名呈现，生成 `acceptance/product-review.md`。包必须保留 U01 必要上下文，不显示生产方式，不给任何版本优待，并要求产品负责人逐项判断：哪个真正讲清理论、哪个建立内部框架、哪个不只是解释 A 能连接 C、哪个可用于理解另一问题、哪个更愿保留在书里、以及两个是否都不合格。

映射单独写入 `acceptance/version-key.md`；完成前不得向产品负责人展示或在产品审阅前建议打开。二者随后冻结并纳入完整 run 压缩包。
