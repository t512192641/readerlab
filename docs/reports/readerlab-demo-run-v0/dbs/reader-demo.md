# `dbs-suite` 能力地图 Demo

## 这份 demo 读什么

这不是 `dbs-suite` 24 个 upstream Skills 的完整地图，而是 ReaderLab 用 sample-level 来源做的一份能力读者样张。它的目标不是列目录，而是帮助读者回答：遇到什么任务，该用哪类能力，为什么用，产出什么，怎么验收。

当前样本覆盖 package metadata 和 7 个代表性位置：入口路由、商业诊断、标题公式、微信公众号 HTML、内容系统、诊断存档、诊断报告。

范围 refs：`dbs-loc-route-core`、`dbs-loc-diagnosis-funnel`、`dbs-loc-title-formula`、`dbs-loc-wechat-html`、`dbs-loc-content-system`、`dbs-loc-save`、`dbs-loc-report`

## 先理解：这是一组商业工作流能力，不是一个万能助手

`dbs-suite` 更像一套任务路由和执行工具箱：先判断问题属于哪一类，再进入对应 Skill。小白读者可以先记住四个能力域：

| 能力域 | 什么时候触发 | 方法原子 | 输出契约 | 怎么验收 | refs |
|---|---|---|---|---|---|
| 入口路由 | 不知道该用哪个 `dbs-*`，或者已有上一步结果要决定下一步 | 识别用户意图，按路由表选 Skill，必要时给 2-3 个下一步 | 选定一个 Skill 或给出有理由的候选路线 | 没有越权做诊断；路线能回到路由表 | `dbs-loc-route-core` |
| 诊断与问题框定 | 用户的问题含糊、假设未查、可能问错问题 | 分层消解语言、假设、逻辑、事实和信息充分性 | 消解原因、有效问题或结构化诊断报告 | 说明问题在哪一层被消解或成立 | `dbs-loc-diagnosis-funnel` |
| 内容表达与发布 | 已有主题或正文，需要标题、表达或公众号排版 | 标题公式匹配、公式编号追溯、Markdown 转 HTML | 带公式来源的标题候选或可发布 HTML | 标题能追到公式；HTML 符合指定样式与输入内容 | `dbs-loc-title-formula`、`dbs-loc-wechat-html` |
| 状态与内容工程 | 结论要跨会话保存、汇总成报告，或把大量材料变成内容系统 | 保存快照、按快照出报告、先审计边界再搭内容工程结构 | 本地快照、报告、内容系统 scaffold 和处理状态 | 不凭空总结；报告可追溯到保存字段；内容系统通过边界和样本检查 | `dbs-loc-content-system`、`dbs-loc-save`、`dbs-loc-report` |

## 读者使用路线

第一次读时，从 `route-core` 开始。它的价值是告诉你 `/dbs` 不是万能分析器，而是入口分流器。你应该先看它如何把“帮我看看”“下一步怎么走”这类模糊请求导向下游能力。

如果问题本身可能是错的，进入诊断域。这里的关键不是马上给建议，而是先判断问题是不是语言陷阱、假设错误、逻辑不成立、事实不足或信息不够。

如果已经有内容对象，再进入内容表达与发布域。标题公式和公众号 HTML 的共同点是：它们都要求输出能追溯，不是随手生成几个看起来好看的结果。

如果工作需要留痕、复盘或扩成系统，进入状态与内容工程域。这里最重要的验收点是来源可追溯：保存不是重新诊断，报告不是凭空总结，内容系统不是还没看材料就开始搭架子。

路线 refs：`dbs-loc-route-core`、`dbs-loc-diagnosis-funnel`、`dbs-loc-title-formula`、`dbs-loc-content-system`

## 跨 Skill 路由怎么读

当前 sample 里有三条代表性路由：

- `route-core -> diagnosis-and-problem-framing`：当用户有具体商业问题或诊断请求时，先从入口路由转入诊断。
- `diagnosis-and-problem-framing -> content-expression-and-publishing`：当业务方向已足够清楚，瓶颈变成内容执行或发布时，再转入内容域。
- `diagnosis-and-problem-framing -> state-and-content-engineering`：当诊断结论需要保存、出报告或变成长期内容系统时，再转入状态与内容工程。

这些路由是 sample 级，不是完整优先级表。`/dbs-good-question`、`/dbs-goal`、hook/resonate/spread/content 等高混淆能力还没有逐项拆边界。

refs：`dbs-loc-route-core`、`dbs-loc-diagnosis-funnel`、`dbs-loc-content-system`

## 验收方式

读这份 demo 时，不要问“文件列全了吗”，而要问四个问题：

1. 触发信号是否清楚：读者能否判断什么时候用这一域？
2. 方法原子是否清楚：它到底做路由、诊断、表达、发布、保存、报告，还是内容工程？
3. 输出契约是否清楚：产物应该长什么样，不能混成泛泛建议？
4. 验收方式是否清楚：未来结果能不能按来源、公式、快照、报告字段或 scaffold 状态复核？

当前断言状态：DBS-A01、A06、A07 为 pass；DBS-A02 到 A05 为 partial，因为它们只覆盖 representative sample，不代表 24 Skills full coverage。

当前人工状态：`pending`。
