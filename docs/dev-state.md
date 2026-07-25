# ReaderLab 当前开发状态

> owner：当前已验证工程事实、缺口与关键证据路径
> 更新日期：2026-07-25
> 当前行动门只见 [`docs/current-task.md`](current-task.md)；本文件不拥有生产授权。

## 已验证事实

- 当前业务证据基线 commit：
  `bcb052e4dcaeac53a273a36608a632b98a98d94b`；后续纯治理修改不提高业务成熟度。
- `taskcards/T2.35.md` 已由上方业务证据 commit 跟踪，SHA-256：
  `b29efb4386ccae4c4720d8a061d4a1bb808359f78f9dc4b4ec4cb35192753eda`。
- `runs/T2.35-CH08-D3-EXPERT-P2-01/` 的 run manifest、production／acceptance freeze、
  D3 P2 gate 与产品判词已跟踪；完整原文、Expert、知识卡、来源审核和完整审阅包仍由 Git
  忽略并只在本地保留。其身份由 freeze 和 `tools/run.py check` 复核。
- 完整审阅包默认不进入 Git；active test 通过 `git check-ignore` 同时约束大 payload 与小型
  控制证据边界。云端模型审核只按任务明确授权。
- `contracts/BOOK-CONTENT-FLOW-v2.md` 已由
  `contracts/BOOK-CONTENT-FLOW-v2-freeze-receipt.md` 绑定冻结身份并完成工程侧技术激活；
  唯一 current pointer 由 `blueprints/PIPELINE-MAP.md` 拥有。
- `python3 -B tests/entry.py` 是当前 active deterministic test 入口；它不是产品 gate 或完整
  项目资格证明。
- 治理一致性修复已经通过全新上下文独立复核；AUD-013 已关闭。AUD-001 只等待下一次真实
  业务状态变化的持续性证据。
- Git 证据收口等待全新上下文复核；当前生产授权仍为 `none`。

## 当前工程缺口

- 图书内容生产 runtime 尚未 `integrated`，真实完整链路尚未 `verified`。
- Writer、Fidelity、装配、最终 Judge 和完整端到端组合是否可用：`unknown`。
- Expert 路线能否在冻结条件和未见材料上复现：`unknown`。
- 图书线任何完整端到端能力是否达到资格通过：`unknown`。
- Skills 线首个获授权真实样张与实现路线：`unknown`。

## 关键路径

- 当前执行切片：`docs/current-task.md`
- 产品 owner：`PRODUCT-DECISIONS.md`
- 工程经验 owner：`ENGINEERING-LESSONS.md`
- 长期派生地图：`blueprints/PIPELINE-MAP.md`
- 当前能力投影：`audit/CAPABILITY-MAP.md`
- 开放问题：`audit/FINDINGS-REGISTER.md`
- 资产生命周期：`audit/ASSET-LIFECYCLE-REGISTER.md`
- 运行工具：`tools/run.py`
- Active tests：`tests/entry.py`

## 证据边界

业务 dirty 状态不得被清理、覆盖或用旧任务状态替代。冻结合同、历史任务、run 和产品判词的
完整正文仍由其原文件拥有；本文件只保存当前结论和检索路径，不复制运行历史或完整报告。
