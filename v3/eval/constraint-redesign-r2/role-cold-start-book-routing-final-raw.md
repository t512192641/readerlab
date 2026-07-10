# 图书路由最终限定冷启动原始输出

## 执行边界

- evaluated_at_utc: `2026-07-10T16:02:04Z`
- evaluated_at_local: `2026-07-10T12:02:04-04:00`
- test_kind: `static-contract-cold-start`
- real_run_performed: `false`
- content_generated: `false`
- rules_or_summaries_modified: `false`

本次只读取图书线协议、constraint 的任务预算段、roles index、run manifest，以及 anchor-nominator、anchor-merger、cognition-candidate、cognition-judge、book-writer、cold-reader、orchestrator 的当前合同。没有读取历史 case、旧 raw 或真实材料作为 verdict 证据；没有运行 Agent 调度、事实核查、内容生产或 fresh/revision。

判定纪律：A、B 任一链不能仅凭短合同与指定协议无损重建，整体即 `fail`。

## 总 verdict

```yaml
overall: pass
chain_a_anchor_nomination_to_merge: pass
chain_b_all_zero_to_body_only_cold_read: pass
runtime: not-run
```

两条限定链均闭合。A 已把归并主体从“论证任务”改为“同一个认知问题”；B 明确只有 fact-checker skipped，裁判、正文-only 装配与冷读仍实际执行，`actual_tasks` 为 10，不为无早停计划的 11 凑数。

## A. anchor-nominator → anchor-merger

### 冷启动输入

假定两个独立提名实例对同一已映射正文范围交付三条合法提名：

```yaml
instance_1:
  - anchor_id: n1-a
    source_locator: chapter:10
    likely_shallow_or_wrong_reading: 把作者的限制条件读成普遍因果
    investigation_question: 这个因果判断在哪些条件下才成立？
  - anchor_id: n1-b
    source_locator: chapter:10
    likely_shallow_or_wrong_reading: 把作者的价值判断误读为事实判断
    investigation_question: 这里是在描述事实，还是在提出价值主张？
instance_2:
  - anchor_id: n2-a
    source_locator: chapter:12
    likely_shallow_or_wrong_reading: 忽略作者随后给出的适用边界
    investigation_question: 这个因果判断在哪些条件下才成立？
```

三条提名都带 contract 要求的原文定位、读浅/读偏描述和调查问题；两个 instance id 可分别审计。

### 归并重建

当前 anchor-merger 核心职责直接要求：按“是否在解决同一个认知问题”合并重复或互补提名，并保留来源提名关系。由此得到唯一合法的归并行为：

- `n1-a` 与 `n2-a` 调查的是同一个条件边界问题，即使 source locator 不同，允许合并为一个认知锚点；`merged_from` 保留两条来源，`source_locators` 保留两处位置。
- `n1-b` 与前两条位于相同或邻近论证结构也不能仅因位置相同被合并，因为它调查的是“事实判断还是价值主张”这一不同认知问题；应独立保留。
- 两个输出锚点都必须保留自己的 `investigation_question`；不能只保留 `claim_in_text`、位置或抽象的论证任务。
- 单方提出的 `n1-b` 不因缺少多数票自动淘汰；若有证据，可用 `minority_high_potential` 保留。

可重建的最小输出：

```yaml
status: pass
received_instances: [1, 2]
merged_anchors:
  - anchor_id: merged-condition-boundary
    source_locators: [chapter:10, chapter:12]
    merged_from: [n1-a, n2-a]
    investigation_question: 这个因果判断在哪些条件下才成立？
  - anchor_id: retained-fact-value-distinction
    source_locators: [chapter:10]
    merged_from: [n1-b]
    investigation_question: 这里是在描述事实，还是在提出价值主张？
```

### A 判定

- nominator 输出读浅/读偏与调查问题：`pass`。
- 两个实例身份与全部提名可追溯：`pass`。
- merger 归并判据与 book protocol 的“同一认知问题”逐字一致：`pass`。
- 调查问题、来源定位、来源提名关系与少数意见可保留：`pass`。
- 不读取完整协议的 merger Agent 仍能得到正确归并判据：`pass`。

Chain A verdict：`pass`。

## B. 三个 candidate 全 0 → body-only → cold read N/A

### 三份候选输出

三个 cognition-candidate 实例都实际执行，分别返回：

```yaml
status: pass
instance: {instance_id: 1|2|3, required_instances: 3}
candidates: []
fact_check_request:
  request_id: none
  status: not-applicable
  requested_by: cognition-candidate
  trigger_reason: no-candidates
  claims: []
  allowed_external_source_boundary: []
zero_candidate_reason: no-defensible-cognition
```

这是三份可审计的合法 0 报告，不是漏跑、失败或 blocked。

### Fact-checker

主控只汇集 `required` requests。三份 request 均为 `not-applicable`，因此 required request 集合为空：

- fact-checker dispatch：`skipped`；
- manifest `stages.skipped`：记录该唯一 dispatch id；
- `conditional_fact_check.status: not-applicable`；
- `request_refs: []`；
- 不生成空 fact-checker 输出，不计 `actual_tasks`。

来源证明仍须独立为 `pass`；来源证明 pass + 条件事实核查 not-applicable 可由主控聚合为 `source_and_fact.status: pass`。

### Cognition judge

cognition-judge 不是无输入下游。它收到三份合法 0 报告、三个 `zero_candidate_reason` 和锚点证据，必须实际执行：

```yaml
status: pass
batch_gap_check: {status: pass, missing: [], return_questions: []}
verdicts: []
locked_packets: []
selection_count: 0
zero_accept_reason: no-qualified-candidates
```

如果盲区检查发现漏掉可形成完整认知的关键问题，则必须 blocked 并定向退回；本冷启动的 pass 路径只表示合同能表达“检查后确认合法 0”。manifest 的 `absolute_value.status` 由该实际 judge 结果记为 `pass`，不能留在 not-run。

### Writer 装配正文-only

book-writer 仍有完整正文 `body_artifact`、source map 和空的 locked packet 集合作为输入，必须实际执行，不得 skipped。合同直接规定 0 条接受时交付正文-only 页面：

```yaml
status: pass
reader_units: []
reader_page:
  source_body_ref: body-artifact-ref
  assembled_page_ref: body-only-page-ref
  source_body_unchanged: true
  insertions: []
  verification: [body-identity-check]
```

它不能用正文摘要、落选候选或占位陪读补齐页面。

### Cold-reader 实际检查

cold-reader 收到最终读者可见的正文-only 页面，实际检查输入是否确为有效正文-only 组合页。因为没有陪读单元，不生成伪造的 unit recall：

```yaml
reads: []
verdict: not-applicable
blocked_reason: ""
```

`not-applicable` 是实际执行后的门结果，不是 `not-run` 或 skipped。若页面污染、正文无效或生产背景泄漏，才应为 `blocked`。

### Dispatch 与 actual_tasks

标准无早停计划为 11 个执行任务，主控不计入。本路径的实例级账本为：

| 角色 | dispatch 数 | 状态 | actual_tasks |
| --- | ---: | --- | ---: |
| source-map | 1 | done | 1 |
| anchor-nominator | 2 | done | 2 |
| anchor-merger | 1 | done | 1 |
| cognition-candidate | 3 | done | 3 |
| fact-checker | 1 | skipped | 0 |
| cognition-judge | 1 | done | 1 |
| book-writer | 1 | done | 1 |
| cold-reader | 1 | done | 1 |
| **合计** | **11 planned dispatches** | **10 done + 1 skipped** | **10** |

manifest 因此应记录 10 个唯一 id 到 `stages.executed`、fact-checker 的 1 个唯一 id 到 `stages.skipped`，并写 `budget.actual_tasks: 10`。不得把 skipped fact-checker 计为 11，也不得把 judge、writer 或 cold-reader 错误跳过后进一步压低数字。

### B 判定

- 三份合法 0 输出与 request N/A：`pass`。
- fact-checker skipped、条件事实子门 N/A、source/fact 聚合：`pass`。
- cognition-judge 实际运行盲区检查并结算 absolute value pass：`pass`。
- writer 实际装配正文-only 页面：`pass`。
- cold-reader 实际检查并返回 not-applicable：`pass`。
- 11 planned、10 executed、1 skipped、actual_tasks 10：`pass`。

Chain B verdict：`pass`。

## 最终声明边界

本次可以声称：

- 当前短合同能按同一认知问题完成锚点归并，并保留调查问题与少数意见。
- 三 candidate 全 0 的静态路由可无损重建为 fact-checker skipped、judge/writer/cold-reader 实际执行、正文-only、cold-read N/A、actual_tasks 10。

本次不能声称：

- 上述 Agent、事实核查、页面装配或冷读在真实运行中发生过。
- 正文、内容质量、用户体验、图书线、Phase 4 或 ReaderLab 流水线通过。
- 可以据本文件开始 Demo。

最终 verdict：`pass`；`runtime-not-run`。
