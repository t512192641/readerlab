# ReaderLab 当前执行切片

> owner：当前任务、run、停止点、允许动作、禁止动作与下一生产授权
> 更新日期：2026-07-25
> current-task: `taskcards/T2.35.md`
> current-run: `runs/T2.35-CH08-D3-EXPERT-P2-01`
> execution-status: `PAUSED_AFTER_EXPERT_ACCEPTANCE`
> product-verdict: `P2_PASS_WORTH_WRITING`
> product-verdict-source: `taskcards/T2.35.md`
> next-production-authorization: `none`
> governance-status: `READY_FOR_REAUDIT`
> next-diagnostic-plan: `DISCOVERY_LAB_THEN_WRITER_LAB`
> diagnostic-dispatch-status: `approved-design-not-started`

## 当前目标

本轮图书线第一性原理复盘、长期 owner 更新与下一会话执行方案已经收口。下一步由产品负责人把
仓库外最终 handoff 手动交给一个干净总控会话；在该动作发生前，不创建任务、不运行诊断实验，
也不恢复 T2.35 Writer。

由于尚未创建新的正式任务卡，控制字段继续指向最后一个正式生产对象 T2.35；新增的
`next-diagnostic-plan` 与 `diagnostic-dispatch-status` 只记录仓库外诊断准备状态，不构成新的
生产 taskcard 或下一生产授权。

## 当前证据状态

- T2.35 开发收口完成；D3 Expert 的产品判词仍为 `P2_PASS_WORTH_WRITING`，但 Writer、
  Fidelity、装配和 Reader 均未发生。
- 本轮没有改变 T2.35 任务卡、run、冻结证据或产品判词。
- 图书线产品 owner 已重新明确核心交付为“可迁移的外部认知框架”，完整定义只见
  `PRODUCT-DECISIONS.md`。
- 历史失败、C4 辨识力、候选期成本结构和 Writer 待验证问题只见
  `ENGINEERING-LESSONS.md`。
- 下一会话详细实验设计位于
  `/private/tmp/readerlab-next-session-execution-design-20260725.md`；它是诊断方案，不是
  正式生产任务卡。
- 最终启动入口位于 `/private/tmp/readerlab-book-line-handoff-20260725.md`。只有产品负责人
  将其交给新会话才视为诊断派发；文件存在本身不构成启动授权。

## 下一诊断范围

新总控按最终 handoff 顺序组织两个仓库外 Lab：

1. Discovery Lab：对未知成熟外部框架的召回路线做隐藏目标、负向控制和成本对照；
2. Writer Lab：在同一冻结输入上比较当前 v1.3、最小正向方案与研究后候选方案，并分别做
   Fidelity 和匿名产品审阅包。

两个 Lab 只产出诊断证据。它们不得写回生产、决定自动 Judge、修改合同或把技术结果升级为产品
接受。

## 当前允许

- 产品负责人手动把最终 handoff 交给一个干净新会话。
- 新总控按 handoff 明确的定向读取、联网、预算、委派和仓库外写入范围执行诊断。
- 当前仓库可继续做只读状态核验。

## 当前禁止

- 不启动 T2.35 Writer，不在 C-008 上继续重跑，不创建新的正式 Reader 或生产 run。
- 不修改现行合同、正式 Prompt、历史 taskcard、历史 run、Gold、examples 或 archive。
- 不把框架垂直样张、Discovery Adapter、Writer 候选 Prompt 或自动 Judge 写成已验证生产方案。
- 不读取旧 ReaderLab，不使用 Chrome remote debugging、浏览器自动化或 `web-access`。
- 不由当前会话自行创建或派发新总控任务。

## 停止与接续

本切片的停止点是 `READY_FOR_NEW_CONTROLLER_MANUAL_DISPATCH`。新总控完成两个 Lab 后，只提交
研究、原始实验、失败证据、成本、匿名 Writer 审阅包和最小建议；不自行进入生产。任何新的正式
生产授权、合同修改、runtime 实现或自动 Judge 仍须产品负责人另行决定。
