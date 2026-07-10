# 图书事实 Handoff 限定冷启动原始输出

## 复核身份与边界

- 时间：`2026-07-10T07:50:11-04:00`。
- 本次只读：`v3/skill/roles/cognition-candidate.md`、`fact-checker.md`、`cognition-judge.md`、`orchestrator.md`、`v3/skill/templates/run-manifest.md`、`v3/skill/protocols/book-engine.md`。
- 检查范围：三个 cognition-candidate 实例各自 typed request；单一 fact-checker 批量 request_ids / checks / per-request coverage；cognition-judge 的 request/check/claim 引用；0 候选 skipped 路径；枚举与 factual / causal 类型的无损传递。
- 本次未读：其他角色、总 judge、回归 case / suite、真实 run 或旧图书事实结果。
- 上下文声明：本执行者此前做过主控与 Skill 事实门审查；本次不是零上下文，但所有 verdict 只引用六份指定文件。
- 本次不修改规则，只新增该 raw。

## 总结结论

- overall verdict：`fail`。
- 正常非空路径已大体成形：三个实例有独立 instance_id 和 run 内唯一 request / claim id；单一 fact-checker 能批量接收 requests，逐 request 记录 checks 与 coverage；judge 用 request_id + check_id + claim_id 引用；kind 与 assertion_type 可沿 check 无损回看。
- 仍有三个阻断：
  1. cognition-candidate 的 fact_check_request schema 永远是 required + 非空 request_id，无法表示该实例 0 候选时的无 request / not-applicable；prose 与 schema 冲突。
  2. 0 候选 skipped 没有区分“单个实例为 0”与“三个实例合计为 0”，也没有闭合 absolute_value gate 的状态；跳过 judge 后 manifest 没有 `absolute_value: not-applicable`。
  3. fact-checker 批量 overall 把任一候选事实失败升级为整批 fail，并由主控映射成 source_and_fact fail；但 book-engine 要求淘汰该候选、允许其他候选继续，二者语义冲突。
- 另有一项类型映射缺口：request 使用 `materiality`，check 改名为 `conclusion_impact`，没有明确二者必须相等；factual / causal 本身已无损。
- 按“任何缺口 fail”的要求，不能判通过。

## 1. 三个 candidate 实例与 typed request

- 当前实例：`instance_id: 1 | 2 | 3`，`required_instances: 3`。
- 每个非空实例 request：非空唯一 request_id；claim 有非空唯一 claim_id、candidate_id、anchor_id、kind、assertion_type、materiality、visible 与 source refs。
- book-engine：三个认知 Agent 各自提交 typed request，列全源内事实、外部事实与因果断言。
- verdict：非空路径 `pass`；0 候选路径 `fail`。
- 正面判断：三个实例的身份与请求所有权清楚，request / claim id 的 run 内唯一性可避免三批合并后碰撞。
- 直接冲突：结构化输出只允许 `fact_check_request: {request_id: nonempty, status: required}`；同一合同的 prose 又说 0 候选时不派 fact-checker。没有 `request_id: none` 或 `status: not-applicable`，因此 0 候选实例无法产出合法合同对象。
- 混合实例问题：若 instance 1 为 0、instance 2/3 有候选，instance 1 的“主控把下游任务 skipped”不能覆盖整批 fact-checker；当前合同没有定义“只忽略该实例 request，其他 requests 仍批量执行”。
- 最小修复：candidate request 增加 `none / not-applicable`，并明确 per-instance zero 只是不产生该实例 request；只有三实例合并后总候选为 0，才走整条下游 skipped。

## 2. 单一 fact-checker 批量 requests

- 输入：一份或多份 typed requests。
- 输出：request_ids 集合、带 request_id 的逐项 checks、每 request 一条 coverage、批量 overall。
- 覆盖不变量：request_ids 与输入 request id 集合精确相等；每 request 的 request_claim_ids 与 checked_claim_ids 精确相等；check id run 内非空唯一。
- verdict：结构与覆盖 `pass`。
- 判断：单一 fact-checker 能区分三个实例的 requests，并逐 request 证明无遗漏、无多项。checks 保留 candidate_id / anchor_id，可回到候选和原文位置。
- 可声称范围：可声称批量输出 schema 支持多 request；不能声称批量 overall 的业务语义正确，见第 5 节。

## 3. Judge 的 request/check/claim 引用

- judge source_checks：每条为 `{request_id, check_id, claim_id}`。
- judge 另存 `missing_request_claim_ids`，任一 request 或 claim 覆盖未完成即停止。
- verdict：`pass`。
- 判断：三层引用键与 fact-checker 输出齐全，judge 不需要只靠 candidate_id 猜测核查结果；request 粒度与批量事实结果可明确拆回各候选。
- 边界：本判断依赖 request/check/claim id 的全局唯一与 coverage 不变量，当前指定文件已写明。

## 4. 枚举与因果类型无损

- request：
  - `kind: source-internal | external`
  - `assertion_type: factual | causal`
  - `materiality: material | non-material`
- check：
  - `kind: source-internal | external`
  - `assertion_type: factual | causal`
  - `conclusion_impact: material | non-material`
- verdict：`partial`。
- 已无损：kind 与 assertion_type 字段名、枚举完全一致；judge 通过 check_id 引用完整 check，因此 factual / causal 不会在 judge 输出中丢失。
- 剩余缺口：materiality 被改名为 conclusion_impact。两者枚举值相同，但没有不变量要求 check.conclusion_impact 必须等于 request claim.materiality，也没有允许 fact-checker重分类的规则。
- 影响：fact-checker 可把 request 的 material 改成 non-material，从而改变整批失败影响或 judge 判断，schema 无法判为冲突。
- 最小修复：保留同名 materiality，或明确 `conclusion_impact == request.materiality`；若允许重分类，必须另存原值、变更理由和裁决主体。

## 5. 批量 overall 与候选级淘汰冲突

- fact-checker 当前聚合：全部 requests 的每个可见事实都 supported 才 overall pass；任一事实 conflicted / insufficient / out_of_scope 则整批 fail。
- orchestrator 当前聚合：fact-checker overall 无损映射到 conditional_fact_check.status；子门 fail 会让 source_and_fact 整门 fail。
- manifest accepted：必需门 fail 时不能 accepted。
- book-engine 当前行为：证据不足且会影响判断的“候选直接淘汰”；绝对裁判仍应逐候选判断，允许其他候选通过，也允许最终 0 条陪读作为合法终态。
- verdict：`fail`。
- 冲突示例：三个 requests 中两个完全 supported，一个候选有一条 material causal claim insufficient。fact-checker overall 必须 fail，source_and_fact 整门随之 fail，run 无法 accepted；但 book-engine 要求只淘汰受影响候选，让另外两个进入裁判。
- 根因：批量 overall 同时承担“核查任务是否完整执行”和“所有候选事实是否通过”，把候选筛选失败错误升级为 run gate 失败。
- 最小修复方向：分开批处理完整性与候选级事实 verdict。批量任务可在 requests 全覆盖且无 blocked 时标执行完成；每个 request / candidate 单独产生事实结果供 judge 淘汰。最终 source_and_fact 聚合只覆盖将进入读者页的锁定候选，不能被已淘汰候选拖成整 run fail。

## 6. 0 候选 skipped 路径

- cognition-candidate prose：0 候选时不派 fact-checker，主控把下游任务记为 skipped。
- orchestrator / manifest：dispatch `skipped -> stages.skipped` 已有通用映射；conditional_fact_check 可以 `not-applicable + request_refs: []`。
- verdict：`fail`。
- 已有能力：fact-checker dispatch 可以被标 skipped，conditional fact 子门可记 not-applicable。
- 未闭合一：candidate 的 request schema 无 none / not-applicable，主控无法从合法结构化输出得出“无 request”。
- 未闭合二：没有定义合并三实例后“总候选数为 0”的聚合对象或条件；单实例 0 不应跳过其他实例的事实核查。
- 未闭合三：如果 cognition-judge 也作为下游 skipped，则 manifest `verification.absolute_value` 只有 `not-run | pass | fail | blocked`，没有 `not-applicable`。accepted 要求所有适用必需门通过，但指定文件没有说明 0 候选时 absolute_value 应为 pass、not-run 仍可接受，还是新增 not-applicable。
- 协议冲突：book-engine 要求“通过者可以 0 条”，这更像 judge 应运行并合法返回 `selection_count: 0`；candidate 合同却说 0 候选时把下游任务 skipped。两种路径没有统一。
- 最小修复方向：明确区分：
  - 候选生产总数为 0：fact-checker skipped / not-applicable；judge 是 skipped 还是运行并 pass+0 必须唯一选定，并同步 absolute_value 枚举与 accepted 条件。
  - 候选存在但最终 0 接受：fact-checker 与 judge 正常运行，judge pass + selection_count 0，不能走 skipped。

## Handoff 矩阵

| 链段 | verdict | 结论 |
| --- | --- | --- |
| 3 candidate instances -> typed requests | `partial` | 非空路径通过；0 候选无合法 request 表达。 |
| requests -> 单一 fact-checker 批量输入 | `pass` | request_ids 精确集合可表达。 |
| fact-checker per-request coverage | `pass` | 每 request 精确覆盖，check id 唯一。 |
| checks -> judge request/check/claim refs | `pass` | 三层引用完整。 |
| kind / factual-causal 无损 | `pass` | 字段与枚举一致。 |
| materiality 无损 | `fail` | 改名 conclusion_impact 且无相等不变量。 |
| 批量 overall -> 候选级裁判 | `fail` | 一个坏候选拖垮整门，与逐候选淘汰冲突。 |
| 总候选 0 -> skipped / accepted | `fail` | request、三实例聚合和 absolute_value 状态未闭合。 |

## 最终可声称范围

- 可以声称：非空三实例请求、单一批量 fact-checker、per-request coverage、judge 三层引用和 causal 类型均有可用 schema。
- 不可以声称：0 候选路径合法、materiality 无损、批量 overall 与候选级淘汰一致，或图书事实 handoff 已通过冷启动。

最终 overall verdict：`fail`。
