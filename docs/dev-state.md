# ReaderLab 当前开发状态

> owner：当前已验证工程事实、缺口与关键证据路径
> 更新日期：2026-07-29
> 当前行动门只见 [`docs/current-task.md`](current-task.md)；本文件不拥有生产授权。

## 已验证事实

- T2.37 已从 T2.36 逐字复制六个冻结输入并记录原始 SHA-256；return brief、Writer return 任务、
  Fidelity／Depth v2 任务和产品包条件均已冻结。两个新上下文分别完成 Writer v2 与独立复核，
  Fidelity／Depth 均通过；匿名产品对照包已生成，产品负责人审阅仍为 `unknown`。完整证据见
  `runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01/`，不改变生产 runtime 的 `not integrated` 状态。
- T2.36 已完成固定 C 的单一 U01 diagnostic seam：Phase 1 Expert 课、Phase 2 内容锁、独立 Writer 与独立 Fidelity／Depth 审核均有冻结文件和 hash；终局为 `LOCK_FOR_WRITER`、`RETURN_WRITER`、`DEPTH_PASS`。由于 Fidelity 未通过，未修改 Reader、未读取旧稿、未生成产品审阅包或版本密钥。完整证据见 `runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01/` 与 `artifacts/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01.tar.gz`；它不改变生产 runtime 的 `not integrated` 状态。
- T2.35 正式生产状态仍停在 `P2_PASS_WORTH_WRITING`；任务卡、run、冻结证据和生产授权均未
  改变，完整语义 payload 继续本地 ignored。
- Writer 修订稿已获产品负责人 `PASS`。仓库外完整章节候选已完成 Assembly Boundary 与独立
  Fidelity 技术检查；P3 完整章节产品体验尚未 `accepted`，未 promotion、未接入生产。
- Discovery treatment-isolation 已完成三份材料 × V0／V1′ × 三次重复的 18 次真实 Scout；
  18/18 原始结果可解析、可保存，9/9 paired block 的基础调用条件和最终 `seed_batch` 字段合同
  一致，下游语义调用为 0。
- 18 次原始结果已机械装配成 9 组匿名 A/B、71 个 seed；284 项原始语义字段字节对照、9/9
  pair 对齐、54 个 raw/request/receipt hash、21 个冻结文件 hash 和匿名泄漏检查均通过。
- 中文单页 smoke v0.1 与加入材料说明、上下文的 v0.2 均未获产品接受。失败不只是界面：冻结
  seed 普遍把局部原句接到更专业、更晦涩的解释术语，没有交付一套可独立学习和迁移的外部认知
  框架，因此停止完整 71 项产品盲审。
- 根因已定位到共同的 Discovery 合同，而不是 V1′ 独有的 trigger map：通用 Scout 被要求寻找
  “原文未命名的解释机制”，V1′ 再把触发位置限定为“关系已出现但解释变量缺失”；共同 schema
  只容纳短机制和重读变化，没有稳定专家认知背景、框架内核、边界与完整教学空间。两变体在静态
  船舶对照材料上 6/6 均产出、共 23 个 seed，并收敛到相同主题族，复现了目标编译错误。
- 因共同基础目标无效，当前 71 个 seed 只保留为 `diagnostic-only`；它们不能证明哪种专家触发
  方式更好，V0／V1′ 产品胜负为 `unknown`，也没有证据表明模型无法完成正确任务。
- 产品范围已明确继续以可迁移的外部认知框架为主；单个仿生学事实、跨学科趣闻或一般新知暂不
  作为并列 Discovery 入口。
- 产品负责人提供的 v3 核心底稿已读取并完成 SHA-256 身份记录。它进一步确认：第一阶段自动
  “读厚”只讨论图书和思想性长文；产品评审必须面对接近成品的人类可读文本；稳定框架型是产品
  偏好而不是已验证能力；无法可靠识别未命名稳定框架时应先收窄到严格理论型。
- v3 中的技术负责人拆解继续只是一组可被独立模型推翻的工程假设；邻近／正交双通道、库存／
  实时发现混合路线、具体角色、两层展示和预算档位均未被误记为已实现方案或正式合同。
- 临时编写的正反例底稿、冻结测试包、候选目录和候选来源研究报告已删除；这些对象不再构成
  当前证据或后续分析输入。
- 新历史证据包只机械回收现有实物：3 组完整且获产品接受的正例、5 个具有直接产品判词但完成
  层级不同的失败对象、4 个冻结章节和 2 个短固定校准件。25 个复制对象逐字节一致，30 条来源
  账本 hash 全部匹配，4 个中性冻结输入未泄漏历史答案，zip 完整性检查通过。
- `D-ENG-002` 与 `AGENTS.md` 已冻结独立队列、一页运行卡、最多三个 blocker、30 分钟证据启动
  熔断、预注册与下游实现分离、总控三检查点等项目规则。
- 图书内容生产 runtime 仍未 `integrated`；当前全部 Writer／Discovery 结果均为仓库外
  diagnostic sidecar，不改变生产成熟度。

## 当前缺口

- T2.36 的 Reader 尚未通过 Fidelity，且产品包未生成；是否、如何另开一个独立 Writer 修订任务仍需产品负责人重新授权，当前为 `unknown`。
- “怎样更好地触发具有稳定认知背景的专家，从完整原文自然召回成熟外部框架”仍为 `unknown`；
  当前实验没有回答这个问题。
- 修订后的 Discovery 角色、触发方式、Prompt、候选接口和最小验证设计均未形成，也未获实施或
  模型调用授权。
- 两个产品尺度已经确认：认知对象在运行前真实存在、结构稳定、可迁移且可追溯，不强制正式命名；
  密度按实质性主题单元判断，单个单元可沉默，不设每章至少一条。
- 历史证据只能支持 3 组完整正例和 5 个非同类失败对象，不能覆盖预设的全部反例类型；当前没有
  “名人角色扮演”完整实物，没有产品判定过的“合理沉默”章节，也没有同一已接受正例的 2—3 种
  展开力度对照。上述内容仍需未来单独生产并由产品负责人判断，不能由历史整理补写。
- Writer 完整章节尚未取得 P3 产品体验验收。
- Discovery 的跨领域稳定性、成本优势和生产资格均为 `unknown`；三份材料和三次重复不能外推。
- Expert 路线在未见材料上的复现性、目标档模型资格、自动 Judge 职责和 Skills 线实现仍为
  `unknown`。

## 关键证据路径

- 当前执行切片：`docs/current-task.md`
- 总控执行决定：`docs/decisions.md` 的 `D-ENG-002`
- Discovery 独立审计：
  `/Users/tianqiang/Downloads/ReaderLab_Discovery_Execution_Controller_Independent_Audit_20260726.md`
- 产品负责人和 GPT Pro 共同整理的 v3 核心底稿：
  `/Users/tianqiang/Downloads/readerlab-gpt-pro-core-brief-v3-20260726.md`
  （SHA-256：
  `c9a48332c057a43bac94656900cb27aa7c3609de1989c5df9d4d677eedf0349e`）
- 面向下一次 GPT Pro 总体分析的中文历史证据底稿：
  `/Users/tianqiang/Downloads/readerlab-gpt-pro-historical-evidence-brief-v1-20260726.md`
  （SHA-256：
  `e818bdb43a76680c605e5874d506090f241ca76899befe822f803c6c09c88180`）
- 完整历史证据、来源账本、判词副本和 4 个冻结输入：
  `/Users/tianqiang/Downloads/readerlab-gpt-pro-historical-evidence-package-v1-20260726.zip`
  （SHA-256：
  `d4c7ff2cb6343cbe39681404f64317291205cd8f39e3ed37810de05d2a53cb96`）
- Discovery 原始运行报告与账本：
  `/private/tmp/readerlab-new-route-20260726/discovery-isolation/checkpoint-b/evidence/`
- Discovery 云端独立审核包：
  `/private/tmp/ReaderLab_Discovery_Execution_Controller_Audit_20260726.zip`
- Discovery 机械匿名包：
  `/private/tmp/readerlab-discovery-blind-review-20260726/final/`
- 被产品拒绝的中文 smoke：
  `/private/tmp/readerlab-discovery-blind-review-zh-20260726/candidate-smoke/`、
  `/private/tmp/readerlab-discovery-blind-review-zh-20260726/candidate-smoke-v0.2/`
- Writer P3 候选：
  `/private/tmp/readerlab-new-route-20260726/writer-assembly/review/P3-product-review-candidate.md`
- 产品 owner：`PRODUCT-DECISIONS.md`
- 历史工程边界：`ENGINEERING-LESSONS.md`
- 长期派生地图：`blueprints/PIPELINE-MAP.md`
- 现行确定性测试入口：`python3 -B tests/entry.py`

## 证据边界

本文件只保存当前工程事实和检索路径。完整运行历史进入 `docs/agent-run-ledger.md`；正式产品判词
仍由相应 taskcard 或产品负责人原始判词拥有。可解析、可保存、技术检查或独立模型审核都不能替代
产品负责人对 Discovery 内容和 Writer 完整章节的接受。
