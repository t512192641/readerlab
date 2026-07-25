# ReaderLab 当前开发状态

> owner：当前已验证工程事实、缺口与关键证据路径
> 更新日期：2026-07-25
> 当前行动门只见 [`docs/current-task.md`](current-task.md)；本文件不拥有生产授权。

## 已验证事实

- T2.35 业务证据基线 commit 为
  `bcb052e4dcaeac53a273a36608a632b98a98d94b`；治理与 MEM 交接 commit 为
  `0ad5eb1d24de484398898884387c4a061df6966e`。后续产品／工程 owner 文档维护不提高业务
  成熟度。
- `taskcards/T2.35.md` 与 `runs/T2.35-CH08-D3-EXPERT-P2-01/` 的小型控制证据已跟踪；
  完整原文、Expert、知识卡、来源审核和审阅包继续由 Git 忽略并只在本地保留。其身份由 freeze
  和 `tools/run.py check` 复核。
- T2.35 开发收口完成，产品负责人已接受 D3 进入 Writer 的内容资格：
  `P2_PASS_WORTH_WRITING`。本轮未启动 Writer，未生成 Reader，也未取得最终产品接受。
- 完整审阅包默认不进入 Git；active test 通过 `git check-ignore` 约束大 payload 与小型控制
  证据边界。云端模型审核只按任务明确授权。
- `contracts/BOOK-CONTENT-FLOW-v2.md` 已由
  `contracts/BOOK-CONTENT-FLOW-v2-freeze-receipt.md` 绑定冻结身份并完成工程侧技术激活；
  唯一 current pointer 由 `blueprints/PIPELINE-MAP.md` 拥有。
- `python3 -B tests/entry.py` 是当前 active deterministic test 入口；它不是产品 gate 或完整
  项目资格证明。本轮 owner 维护后 active tests 为 36/36 PASS，当前 run 为 11/11 PASS，
  `git diff --check` PASS。
- 图书线第一性原理复盘已经形成新的 owner 结论：核心产品对象、成熟外部知识承重、知识来源范围、
  分级核验与自动 Judge 暂缓由 `PRODUCT-DECISIONS.md` 拥有；失败链和待回归问题由
  `ENGINEERING-LESSONS.md` 拥有。
- 下一阶段只获批仓库外诊断设计，尚未派发。启动方式、范围和停止点见
  `docs/current-task.md` 及其引用的最终 handoff。

## 当前工程缺口

- 图书内容生产 runtime 尚未 `integrated`，真实完整链路尚未 `verified`。
- 如何在不知道名称时召回成熟外部框架：`unknown`。模型参数知识、查询扩展和认知库存路线均未
  经过隐藏目标与负向控制的对照验证。
- “框架垂直样张”能否在不退回微拓展的前提下降低候选期成本：`unknown`。
- Writer v1.3 是否优于精简正向指令或研究后候选方案：`unknown`；当前只有不同任务、不同输入
  下的失败与局部通过，没有同输入 A/B 证据。
- Writer、Fidelity、装配、最终 Judge 的完整端到端组合是否可用：`unknown`。
- Expert 路线能否在未见材料上复现，目标档模型能否稳定达到产品目标：`unknown`。
- 自动 Judge 的职责、接口、正反例覆盖和资格条件尚未冻结，不进入当前开发。
- Skills 线首个获授权真实样张与实现路线：`unknown`。

## 关键路径

- 当前执行切片：`docs/current-task.md`
- 产品 owner：`PRODUCT-DECISIONS.md`
- 工程经验 owner：`ENGINEERING-LESSONS.md`
- 持久工程决定：`docs/decisions.md`
- 长期派生地图：`blueprints/PIPELINE-MAP.md`
- 当前能力投影：`audit/CAPABILITY-MAP.md`
- 开放问题：`audit/FINDINGS-REGISTER.md`
- 资产生命周期：`audit/ASSET-LIFECYCLE-REGISTER.md`
- 运行工具：`tools/run.py`
- Active tests：`tests/entry.py`

## 证据边界

冻结合同、历史任务、run 和产品判词的完整正文仍由其原文件拥有；本文件只保存当前工程结论和
检索路径，不复制运行历史或完整报告。诊断计划、Prompt 候选和临时实验产物在真实运行前不能写成
已实现、已集成或已验证。
