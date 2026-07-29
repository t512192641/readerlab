# ReaderLab 当前执行切片

> owner：当前任务、run、停止点、允许动作、禁止动作与下一生产授权
> 更新日期：2026-07-26
> current-task: `taskcards/T2.35.md`
> current-run: `runs/T2.35-CH08-D3-EXPERT-P2-01`
> execution-status: `PAUSED_AFTER_EXPERT_ACCEPTANCE`
> product-verdict: `P2_PASS_WORTH_WRITING`
> product-verdict-source: `taskcards/T2.35.md`
> next-production-authorization: `none`
> governance-status: `PRODUCT_CONTRACT_V3_CALIBRATION`
> controller-handoff-status: `CONSUMED_AND_CLOSED`
> controller-handoff-path: `/private/tmp/readerlab-discovery-blind-content-review-handoff-20260726.md`
> source-brief: `/Users/tianqiang/Downloads/readerlab-gpt-pro-core-brief-v3-20260726.md`
> source-brief-sha256: `c9a48332c057a43bac94656900cb27aa7c3609de1989c5df9d4d677eedf0349e`
> next-analysis-slice: `GPT_PRO_INDEPENDENT_ANALYSIS_PENDING_OWNER`
> analysis-material-status: `HISTORICAL_EVIDENCE_PACKAGE_READY_WITH_EXPLICIT_GAPS`
> controller-policy: `docs/decisions.md#d-eng-002--原始证据优先与总控执行熔断`

## 当前目标

把产品负责人和 GPT Pro 共同整理的 v3 产品底稿，与本项目中可逐字追溯的历史产品实物分开
交付，供下一次独立总体分析使用。历史证据不足的材料类型保留为空缺，不再由整理者临时编写
正例、反例、合理沉默样本或展开力度版本。

正式控制字段继续指向最后一个生产对象 T2.35；本切片只是产品合同校准和分析材料准备，不构成
新的生产 taskcard、Prompt 修订、模型实验、生产 promotion 或下一生产授权。

## 当前结论

- v3 没有推翻“借不同认知背景重读原文”的根目标，而是进一步把第一阶段自动陪读收敛到图书和
  思想性长文中的可迁移外部认知框架；技术材料和 Skills 包完全移出本轮分析，不等于永久取消
  ReaderLab 独立的 Skills 产品线。
- 第一阶段偏好“稳定框架型”，但能否可靠识别没有正式名称的稳定框架仍未证实；若做不到，自动
  主线应先收窄到有明确名称、来源、固定结构且可直接核对的“严格理论型”。
- 产品评审对象必须是接近成品、普通读者可顺着原文读懂的陪读文本。知识卡、字段表、短 seed 和
  来源审计只能作为内部证据，不能继续替代产品体验。
- 现有 Discovery 71 个 seed 继续只作错误目标编译的诊断证据，不重新包装为本轮正反样本，也不
  据此比较 V0／V1′。
- 两个尺度已经由产品负责人确认：认知对象必须在本次运行前真实存在、结构稳定、可迁移且可追溯，
  但不强制拥有正式名称；产出密度按实质性主题单元判断，允许单个单元沉默，不机械要求每章至少
  一条。
- 先前由 Agent 临时编写的 4 个正向候选、5 个反例和 3 种展开版本不具备历史证据身份，相关
  底稿、测试包、候选目录和来源研究报告已删除，不再作为本项目证据。
- 重建包只回收当前项目真实历史：3 组完整且获产品接受的正例、5 个有直接产品判词的失败对象、
  4 个逐字节冻结输入和 2 个短固定校准件。
- 历史证据不能满足全部预设材料：“名人角色扮演”没有完整实物；“牵强跨域”和“只有观点没有
  框架”只有历史摘要；没有产品判定过的“合理沉默”完整章节，也没有同一已接受正例的 2—3 种
  展开力度对照。上述缺口没有通过新创作补齐。

## 当前允许

- 产品负责人阅读新底稿，或把 v3 核心底稿与新历史证据包一并交给 GPT Pro。
- 对当前仓库和新证据包做只读核对。

## 当前禁止

- 不重跑 18 次 Scout，不修改 V0／V1′ Prompt、材料或既有原始证据。
- 本轮分析底稿不混入技术材料、Skills 包、技术实现方案或 Skills 设计。
- 不在没有新方案和明确授权时创建或修改 Prompt、schema、taskcard、生产 run 或模型调用。
- 不先建设 Normalizer、模型 Judge、Clusterer、自动 Verifier、成本 dashboard、promotion gate
  或生产集成。
- 不启动 Writer 新迭代，不修改 Writer 语义正文，不让 Writer 占用 Discovery 的预留资源。
- 未经当前任务逐文件授权，不读取 `GOLD-STANDARDS.md`、`examples/`、`archive/`；永不读取旧
  ReaderLab。
- 不根据 seed 数、token、schema-valid、模型自评或技术完成宣称 V1′ 胜出或生产通过。

## 验收与停止

本切片已经停止在“真实历史证据已机械回收、核验并交给产品负责人”：

- 中文历史证据底稿：
  `/Users/tianqiang/Downloads/readerlab-gpt-pro-historical-evidence-brief-v1-20260726.md`
- 完整历史证据包：
  `/Users/tianqiang/Downloads/readerlab-gpt-pro-historical-evidence-package-v1-20260726.zip`

底稿只陈列已有产品判词，不产生新的产品判词。包内 25 个历史实物／冻结输入副本与源文件逐字节
一致，30 条来源账本 hash 全部匹配，4 个冻结输入未泄漏历史答案；压缩包完整性检查通过。

不自行调用 GPT Pro，不创建新实验，也不进入生产。现有 71 个 seed 的状态继续固定为
`DIAGNOSTIC_ONLY`，V0／V1′ 产品胜负继续为 `NOT_ANSWERED_BY_THIS_EXPERIMENT`。
