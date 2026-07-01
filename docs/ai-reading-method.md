# ReaderLab AI Reading Method

## 方法名

E-R-D-D：

```text
Evidence -> Route -> Deepen -> Decide
证据约束 -> 阅读路由 -> 深读生成 -> 升降级决策
```

## 目的

约束 AI 在复杂材料中不要先写漂亮结论，而是先建立证据边界，再做材料结构定位，再生成候选，最后判断哪些内容可以升格。

注意：E-R-D-D 是内部生产方法，不是读者页展示语言。`Route` 不等于给读者输出“阅读路线”，而是 Agent 判断材料类型、阅读单元、主体/外壳/审计分层和章节位置。

## 1. Evidence

AI 先不许总结，只能回答：

- 材料有哪些来源。
- 每个来源是什么角色。
- 覆盖到什么范围。
- 哪些地方是完整覆盖、样本覆盖、目录覆盖或未知。
- 哪些位置可以引用。
- 哪些内容不能下结论。

产物：

- `source-registry.v1`
- `location-map.v1`
- coverage status

失败条件：

- 没有来源引用却写全局判断。
- 低覆盖冒充完整全书理解。
- 把 source refs 当装饰，而不是判断边界。

## 2. Route

AI 接着判断材料结构和读者方位：

- 这是书、长文、课程、Skill 包、代码文档，还是混合材料。
- 应按目录读、按问题读，还是按能力域读。
- 哪些是主体。
- 哪些是外壳。
- 哪些是支撑说明。
- 哪些是实现细节。
- 哪些只属于审计。
- 当前章节/模块为什么出现在这里。
- 它承接前面什么，为后面什么服务。

产物：

- reading unit plan
- `catalog-map.v1`
- `capability-map.v1`
- material structure diagnosis
- reader-facing orientation draft

规则：

- 结构不清楚时输出结构诊断，不强行生成全局地图。
- Skill 包优先按任务路由和能力域组织，不按文件目录机械阅读。
- 面向读者的 Markdown 应改写成“这份材料讲什么 / 这一章在整体中的位置 / 读完要带走什么”，不暴露 `Route`、`source refs` 或内部状态。

## 3. Deepen

AI 不能直接写“重点”。它先生成候选池，再判断哪些内容值得用更高维的讲解带给读者。

候选类型：

```text
main_question
structure_role
mechanism_chain
framework
principle
case
counterexample
term
technical_design
failure_mode
output_contract
transfer_insight
misread_risk
downgrade_candidate
cross_domain_lens
historical_pattern
reader_prior_connection
```

规则：

- “重点”不是一种东西。原则、案例、术语、技术设计、误读风险的判断标准不同。
- 候选必须带来源范围、读者收益和边界。
- 没有机制链时不硬写机制链。
- 高阶讲解候选必须回答：它能给读者带来什么非摘要型认知增量；它连接了哪些看似不同但底层逻辑相同的领域；它是否真的照亮当前正文。
- 可引入跨学科模型、历史经验、商业 / 组织 / 工程案例、用户既往项目中的相似结构，但必须标清这是 AI 的解释性连接，不得冒充原文结论。
- 如果只是“名人观点 + 漂亮类比 + 当前材料”并列摆放，不能 Promote，只能 Downgrade 或 Reject。

## 4. Decide

每个候选经过五个 gate：

```text
Source Gate
Structure Gate
Reader Gain Gate
Transfer / Technical Gate
Overreach Gate
```

输出只能是：

```text
Promote    升格为读者页重点、深读卡或技术洞察
Keep       保留在一手正文，不额外升格
Downgrade  放入附录、背景、案例、执行外壳或审计页
Reject     不进入读者页，只在审计中说明
```

Reader Gain Gate 对高阶讲解的额外要求：

- 是否超过了普通摘要，让读者获得新的判断框架。
- 是否把局部材料放进更大的世界图景、历史结构、跨学科模型或既有经验中重新看。
- 是否解释了不同领域之间的同构关系，而不是只做表面类比。
- 是否明确哪些是原文、哪些是 AI 重组、哪些需要外部验证。

## High-Order Explanation v1

E-R-D-D 中的 Deepen / Decide 对高阶讲解采用 `high-order-explanation.v1` 内部协议。该协议不是读者页展示语言，而是 Agent 生成自然讲解前的质量门：

```text
Source Anchor
-> Baseline Summary Trap
-> Upgrade Question
-> Mechanism Graph
-> Lens Auction
-> Judgment Gate
-> Natural Explanation
-> Delta Eval
```

关键约束：

- Source Anchor：先抽取正文锚点，记录正文支持什么、不能支持什么。
- Baseline Summary Trap：先写普通总结会怎么讲，用来防止最终稿只是更顺的总结。
- Upgrade Question：把主题升级成更大的问题，格式是“在什么约束下，谁如何把什么资源转化成什么结果，同时避免什么失败”。
- Mechanism Graph：把正文观点串成 input / constraint / action / feedback / output / failure_mode / boundary。
- Lens Auction：候选镜头必须由正文触发，并能解释机制、揭示边界、带来认知增量；最多 Promote 2 个主镜头和 1 个边界镜头。
- Judgment Gate：必须完成吸收 / 降级 / 拒绝，不停在“有启发”。
- Natural Explanation：最终写成自然陪读讲解，不展示内部字段。
- Delta Eval：和 baseline summary 对照；没有问题框架、机制、镜头、边界或裁决，判 FAIL。

完整方法见 [`docs/high-order-explanation-method.md`](high-order-explanation-method.md)，audit contract 见 [`docs/contracts/high-order-explanation-v1.md`](contracts/high-order-explanation-v1.md)。

## Deepread Card

真正升格的深读内容必须写成 deepread card。

最低字段：

```yaml
id: deepread-001
type: principle | framework | mechanism | case | counterexample | term | technical_design | transfer_insight
title: ""
source_scope: ""
primary_refs: []
reader_gain: ""
boundary: ""
confidence: low | medium | high
human_status: unreviewed | reviewed | accepted | rejected
```

正文必须回答：

- 这是什么。
- 为什么对理解材料重要。
- 原文依据在哪里。
- 机制链是什么。
- 有什么案例。
- 有什么反例或边界。
- 有什么迁移价值。
- V1 / V2 / V3 是否通过。
- 它和哪些其他学科、历史结构、产品 / 组织 / 工程经验存在同构关系。
- 这些连接哪些来自原文，哪些是 AI 的解释性重组。

## V1 / V2 / V3

- V1：换一个场景是否还能解释。
- V2：它能否预测或指导读者判断。
- V3：它是否区别于普通常识。

不能通过这些检查的内容，不应升格为 deepread card。
