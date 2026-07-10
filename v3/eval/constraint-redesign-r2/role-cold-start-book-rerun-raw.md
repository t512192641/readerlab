# 图书角色合同冷启动复跑原始检查

## 执行边界与上下文披露

- checked_at_utc: `2026-07-10T11:03:29Z`
- checked_at_local: `2026-07-10T07:03:29-04:00`
- check_kind: `role-contract-cold-start-rerun`
- runtime_status: `runtime-not-run`
- content_generation: `not-run`
- historical_regression_replay: `not-run`
- previous_context_present: `true`
- previous_failure_raw_used: `false`

本次是同一会话中的复跑，不是完全无历史上下文。此前已经执行过一次图书 8 合同冷启动并写入首次失败 raw；本次按要求保留该文件，未读取、未引用、未修改它。复核问题清单直接来自本次任务：body artifact/status、提名 links/0 与实例数、归并返工与调查问题、claim schema、fact 映射/聚合、locked anchor_id/返工、writer 最终页面装配、cold-reader 布尔/聚合/0 条。

本次只读以下 9 个文件：

- `v3/skill/roles/README.md`
- `v3/skill/roles/source-map.md`
- `v3/skill/roles/anchor-nominator.md`
- `v3/skill/roles/anchor-merger.md`
- `v3/skill/roles/cognition-candidate.md`
- `v3/skill/roles/fact-checker.md`
- `v3/skill/roles/cognition-judge.md`
- `v3/skill/roles/book-writer.md`
- `v3/skill/roles/cold-reader.md`

未读取完整图书协议、图书回归证据、首次失败 raw、真实运行产物或生产日志。本文件只判断当前 8 份角色合同与角色索引能否独立闭合结构，不声称发生了图书生产、真实 Agent 调度、内容验收或用户体验测试。

## 复核口径

逐角色检查：

1. 任务是否单一且与角色权限一致。
2. 允许输入是否足以产生 schema 中的必填输出。
3. 输出是否能被下一角色直接消费。
4. 禁令是否阻止越权生产或自我验收。
5. 停止条件是否能落入结构化状态并明确返工方向。
6. 合同是否可以在不读取完整协议的前提下自足执行。
7. 状态与业务枚举是否覆盖正常、0 条、失败和阻塞路径。

判定取值：

- `pass`：当前合同可自足执行并完成直接 handoff；允许存在不影响执行的自由文本字段。
- `fail`：仍有允许输入无法产生必填输出、关键状态不可表达或下游无人提供输入。
- `blocked`：限定读取不足以判断。

---

## 角色索引与实例数

`roles/README.md` 明确给出图书线标准实例：

| 阶段 | 角色 | 标准实例数 |
|---|---|---:|
| 一手主体 | source-map | 1 |
| 锚点搜索 | anchor-nominator | 2 |
| 锚点归并 | anchor-merger | 1 |
| 候选生产 | cognition-candidate | 3 |
| 事实复核 | fact-checker | 1 |
| 绝对裁判 | cognition-judge | 1 |
| 成文与最终页面装配 | book-writer | 1 |
| 无上下文冷读 | cold-reader | 1 |

图书执行角色标准任务数：

```text
1 + 2 + 1 + 3 + 1 + 1 + 1 + 1 = 11
```

索引另列共用 orchestrator 1 个实例。若统计“索引中的全部参与角色实例”，总数为 12；但它是调度实例，不属于上述 8 合同的图书执行任务，因此本次图书标准任务数记为 `11`，并单独声明 `orchestrator: 1 coordination instance`，避免把两种口径混成一个数字。

索引还明确了最终判定权边界：事实由 fact-checker 判定，认知价值由 cognition-judge 判定，好读由 cold-reader 报告。生产角色没有取得自己的最终验收权。

---

## 1. source-map

- instances: `1`
- actual_verdict: `pass`
- self_sufficient: `yes`

### 任务

任务单一：从登记原始来源建立完整正文与可追溯位置映射。职责限制为轻量清理、保留顺序、记录位置与异常，不生产陪读或认知候选。

### 输入

输入包括原始来源、明确范围、线路规则摘录、轻量清理规则和获准剥离旧 AI 块清单，足以执行本角色职责。

### 输出 schema

关键修复已经闭合：

- 顶层 `status: not-run | pass | fail | blocked`，并有 `blocked_reason`、`return_to`。
- `body_artifact` 明确提供 `body_ref`、原始快照引用与单元顺序。
- `body_units.text_ref` 被明确要求为 `body_artifact.body_ref` 内可解析的稳定单元引用，不再只是自由描述。
- `source_map.action: kept | moved | deleted`，并记录理由。
- `anomalies` 可以传递缺页、乱码、顺序和来源冲突。

下游 anchor-nominator 可由 `body_artifact + body_units + source_map` 获得完整、可定位正文。

### 禁令

禁令能阻止摘要、解释、评价、认知候选、知识点选择、压缩和改写，权限边界清楚。

### 停止条件

来源未登记、范围不清、缺损影响内容判断或删除未授权时停止；顶层 `blocked_reason` 和 `return_to` 可承载结构化上报。

### 状态枚举

- role status: `not-run | pass | fail | blocked`
- source action: `kept | moved | deleted`

### 结论

body artifact、引用解析规则与角色状态均已具备；本角色可自足执行并向锚点提名交接。

---

## 2. anchor-nominator

- instances: `2`
- actual_verdict: `pass`
- self_sufficient: `yes`

### 任务

任务清楚：从已映射正文独立提名作者论证承重位置，不扩写候选或读者文案。

### 输入

输入是线路规则摘录和完成 source map 的正文单元。上游现已提供稳定 `body_artifact` 和可解析 `text_ref`，因此输入可直接使用。

### 输出 schema

本次所查三项均闭合：

- `instance: {instance_id: 1 | 2, required_instances: 2}` 明确两次独立实例及总数。
- `links` 已定义 item 为 `{target_locator, relation}`，可定位前后论证关系。
- `zero_nomination_reason: no-load-bearing-anchor | ""` 能区分合法 0 提名与正常有提名输出。

每项 nomination 还含 `claim_in_text`、承重理由、浅读/误读、调查问题、置信度和少数派高潜标记，足以供归并。

### 禁令

禁止外部搜索、候选扩写、最终文案、凑数量和兴趣替代论证重要性，能维持独立搜索职责。

### 停止条件

source map 未完成、上下文缺失或无法用原文证明承重时停止；顶层 status、blocked_reason、return_to 可表达异常。合法 0 则由 `zero_nomination_reason` 表达，不需误记为 blocked。

### 状态枚举

- role status: `not-run | pass | fail | blocked`
- instance id: `1 | 2`
- confidence: `high | medium | low`
- minority flag: boolean
- zero path: `no-load-bearing-anchor | ""`

### 结论

links、0 提名路径和两实例约束均已明确；两名提名者可独立执行并向 merger 交付。

---

## 3. anchor-merger

- instances: `1`
- actual_verdict: `pass`
- self_sufficient: `yes`

### 任务

任务清楚：接收同范围全部提名，合并重复、保留溯源、检查承重结构覆盖并保留少数派高潜发现。

### 输入

输入要求两份同一正文范围提名及其原文定位；`received_instances: [1, 2]` 使 merger 能确认标准实例是否齐备。

### 输出 schema

原检查点已闭合：

- `merged_anchors` 保留 `claim_in_text`、`investigation_question` 和 `context_links`，调查问题与上下文不再在归并时丢失。
- `merged_from` 保留提名溯源。
- `coverage_gaps` 在请求定向补提名时提供 `target_locators`、`question` 和固定 `return_to: anchor-nominator`。
- 顶层 status、blocked_reason、return_to 可表达整批停止与退回。

下游 cognition-candidate 可直接拿到 anchor id、原文位置、文本主张、调查问题与前后关系；主控只需按 ref 提供对应正文片段，不必重建丢失语义。

### 禁令

禁止简单多数票、伪差异、候选生产、事实补充和读者文案，归并角色不会越权。

### 停止条件

范围不同、定位不可核或覆盖缺口需定向补提名时停止。`coverage_gaps` 提供精确目标与问题，由主控调度回 anchor-nominator；“退回主控”和字段中的 `return_to: anchor-nominator` 不冲突，前者是调度主体，后者是返工执行角色。

### 状态枚举

- role status: `not-run | pass | fail | blocked`
- received instances: `[1, 2]`
- confidence: `high | medium | low`
- gap action: `retain_gap | request_targeted_nomination`
- targeted return: `anchor-nominator`

### 结论

归并返工、调查问题、上下文连接和实例齐备检查均可结构化表达，本角色通过。

---

## 4. cognition-candidate

- instances: `3`
- actual_verdict: `pass`
- self_sufficient: `yes`

### 任务

任务单一：围绕入围锚点形成只包含一个判断、可被独立裁判的完整认知；不写最终文案、不自评。

### 输入

入围锚点、对应正文片段和获准证据范围足以形成候选。角色实例明确为 3 个，每个实例可以输出一批 candidates。

### 输出 schema

claim handoff 已闭合：

- 每个 `facts_to_check` item 都有 `claim_id`、`candidate_id`、`anchor_id`、`claim_text`。
- `claim_type: source | external | causal` 区分核查对象。
- `conclusion_impact: material | non-material` 为 fact-checker 聚合提供必要权重。
- `instance_id: 1 | 2 | 3`、`required_instances: 3` 明确三次候选生产任务。
- `zero_candidate_reason: no-defensible-cognition | ""` 支持合法 0 候选。

候选本体保留判断、默认读法、必要证据、读法变化与边界，能独立进入事实核查和裁判。

### 禁令

禁止素材卡代替完整认知、多个问题拼接、最终成文和自我宣布通过，边界完整。

### 停止条件

锚点未锁定、原文不足或关键事实缺失到无法裁判时停止并返回缺口；顶层状态三字段可承载阻塞和退回。

### 状态枚举

- role status: `not-run | pass | fail | blocked`
- instance id: `1 | 2 | 3`
- claim type: `source | external | causal`
- conclusion impact: `material | non-material`
- zero path: `no-defensible-cognition | ""`

### 结论

事实 claim schema、候选与锚点映射、三实例和 0 候选路径均闭合，本角色通过。

---

## 5. fact-checker

- instances: `1`
- actual_verdict: `pass`
- self_sufficient: `yes`

### 任务

任务清楚：逐项核实事实、来源强度和适用边界，不裁判认知价值、不改写候选主张。

### 输入

上游现在提供结构化待核事实，含 claim、candidate 和 anchor 三层 id、事实文本、类型及结论影响；再结合原始来源、source map 和获准外部来源，足以核查。

### 输出 schema

映射与聚合均闭合：

- `checks` 回写 `claim_id`、`candidate_id`、`anchor_id`，可无损映射回候选和锚点。
- item verdict: `supported | conflicted | insufficient | out_of_scope`。
- 来源信任为 `high | medium | low`。
- `conclusion_impact: material | non-material` 与上游一致。
- 顶层 `overall: pass | fail | blocked`、blocked_reason、return_to 完整。
- 明文聚合规则规定：全部 material claim supported 才 pass；任一 material claim conflicted/insufficient/out_of_scope 则 fail；来源不可访问或身份不明到无法判定则 blocked。

non-material claim 不会被误用来替代 material 硬门；其逐项结果仍保留在 checks 中供裁判看边界。

### 禁令

禁止用文风、趣味、相对最好、常识、搜索摘要、二手转述或不可定位引用作为通过依据，事实判定权边界明确。

### 停止条件

关键来源不可访问、身份不明、结论性冲突无法裁定或需新增付费/敏感来源时停止，均可映射为 blocked 并附原因和返回主体。

### 状态枚举

- item verdict: `supported | conflicted | insufficient | out_of_scope`
- source trust: `high | medium | low`
- conclusion impact: `material | non-material`
- overall: `pass | fail | blocked`

### 结论

claim 映射、来源强度、结论影响和整门聚合规则均已明确，本角色通过。

---

## 6. cognition-judge

- instances: `1`
- actual_verdict: `pass`
- self_sufficient: `yes`

### 任务

任务顺序正确：先做整批关键盲区检查，再对事实核查后的完整认知做绝对淘汰；合法输出 0 条，并锁定接受项的判断边界。

### 输入

输入包含候选、锚点证据、事实核查结果、裁判标准和被明确路由的判例。事实结果现已带 candidate/anchor 映射，因此裁判可以逐项关联。

### 输出 schema

原阻塞已闭合：

- `locked_packets` 现在同时保留 `candidate_id` 与 `anchor_id`，book-writer 不再需要猜测锚点。
- `batch_gap_check.return_questions` 为每个返工问题提供 `target_role: cognition-candidate | fact-checker`、`affected_ids` 和问题文本。
- 顶层 status、blocked_reason、return_to 能表达角色停止。
- item verdict 为 `accept | reject | blocked`。
- `selection_count: 0` 与 `zero_accept_reason: no-qualified-candidates | ""` 明确合法 0 接受路径。

对于锚点搜索/覆盖缺口，anchor-merger 已有定向回 anchor-nominator 的路径；认知裁判在收到完整 merged anchors 后只需要把候选内容盲区或事实问题退回 candidate/fact-checker，当前 target_role 范围与本角色职责一致。

### 禁令

禁止相对最好、机械分数、成文补救、新事实、新论点和第二问题，能保持独立绝对裁判。

### 停止条件

事实未完成、候选锚点失配、关键盲区、判例冲突或需改候选才可通过时停止并定向退回；结构字段足以描述目标和受影响对象。

### 状态枚举

- role status: `not-run | pass | fail | blocked`
- batch gap: `pass | blocked`
- item verdict: `accept | reject | blocked`
- return target: `cognition-candidate | fact-checker`
- zero path: `no-qualified-candidates | ""`

### 结论

locked anchor_id、返工目标、受影响对象和 0 条接受路径均闭合，本角色通过。

---

## 7. book-writer

- instances: `1`
- actual_verdict: `pass`
- self_sufficient: `yes`

### 任务

角色索引把本阶段定义为“成文与最终页面装配”；合同核心职责也明确把通过单元插入对应锚点并交付最终组合页面，而不是只写孤立陪读文案。

### 输入

允许输入现包含：

- 正文 `body_artifact`
- source map
- 锁定包中的 `candidate_id`、`anchor_id`、唯一判断、必要证据、原文落点、边界和禁止枝节
- 线路规则摘录与页面槽位要求

这些输入足以生成 reader unit 并在不改变正文的前提下完成页面装配。

### 输出 schema

最终页面交接已经闭合：

- `reader_units` 保留 unit、anchor、locked candidate、已用证据和边界表达状态。
- `boundary_expressed: true | false | not-applicable` 是完整三态，不再是固定 true。
- `reader_page` 提供 `source_body_ref`、`assembled_page_ref`、固定硬门 `source_body_unchanged: true`、逐项插入位置和 verification 记录。
- 核心职责明确 `selection_count = 0` 时交付正文-only 页面，因此 cold-reader 仍能收到合法最终页面。
- 顶层 status、blocked_reason、return_to 支持停止和退回。

`source_body_unchanged: true` 是本角色必须满足的交付不变量，不需要用 false 表示一个可接受成品；若无法保持 true，应通过 fail/blocked 停止。

### 禁令

禁止重选题、加新事实、搜索补料、拼接落选候选、展开第二问题和泄漏生产术语，成文不会突破锁定包。

### 停止条件

锁定包不全、证据无法自然说清、必须加料或无法保持单一认知时停止并退回裁判；结构状态可承载失败/阻塞与返回目标。

### 状态枚举

- role status: `not-run | pass | fail | blocked`
- boundary expressed: `true | false | not-applicable`
- source body invariant: `true`
- zero accept output: body-only page

### 结论

anchor_id 输入、最终页面装配、正文不变校验和 0 条正文-only 路径均闭合，本角色通过。

---

## 8. cold-reader

- instances: `1`
- actual_verdict: `pass`
- self_sufficient: `yes`

### 任务

任务单一：仅凭最终读者可见页面报告实际理解、读法改变、阅读负担和二次整理需求，不修文、不读取生产过程。

### 输入

book-writer 已明确输出最终 `assembled_page_ref`，且 0 条时也输出正文-only 页面。主控可只把最终可见正文片段和对应陪读单元传给 cold-reader，不需暴露候选、评分或生产理由。

### 输出 schema

原检查点全部闭合：

- `needs_reorganization: true | false` 是完整布尔值。
- verdict 增加 `not-applicable | pass | fail | blocked`。
- 聚合规则明确：有单元时，全部能复述、新增理解与读法改变成立且无需重整才 pass；任一不满足则 fail。
- 正文-only 页面记 `not-applicable`，不会把 0 条合法结果误判为失败或虚假成功。
- 输入污染或组合页面无效记 blocked，并用 blocked_reason 说明。

### 禁令

禁止读取生产过程、候选、评分、裁判理由、提示词和实验目的，也禁止替作者修文或猜意图放行，盲测边界完整。

### 停止条件

输入含非读者背景、正文陪读失配或必须请求生产解释时停止并判测试无效，可直接映射 blocked。

### 状态枚举

- needs reorganization: `true | false`
- verdict: `not-applicable | pass | fail | blocked`

### 结论

布尔、聚合、0 条正文-only 和污染阻塞路径均清楚，本角色通过。

---

## 重建的标准调度图

根据角色索引实例数和 8 份合同，可以独立重建：

```text
orchestrator（协调，不计入 11 个图书执行任务）
  -> source-map ×1
  -> anchor-nominator ×2（并行独立提名）
  -> anchor-merger ×1
       -> coverage gap: 经 orchestrator 定向回 anchor-nominator
  -> cognition-candidate ×3（并行独立候选生产）
  -> fact-checker ×1（汇总结构化 claims，独立事实门）
  -> cognition-judge ×1（先盲区检查，再绝对价值判断）
       -> content gap: 经 orchestrator 回 cognition-candidate
       -> fact gap: 经 orchestrator 回 fact-checker
       -> selection_count = 0: 仍进入 writer 生成正文-only 页面
  -> book-writer ×1（成文 + 最终页面装配）
  -> cold-reader ×1
       -> 有陪读单元: pass/fail/blocked
       -> 正文-only: not-applicable
```

标准图书执行任务数：`11`。

```text
source-map 1
+ anchor-nominator 2
+ anchor-merger 1
+ cognition-candidate 3
+ fact-checker 1
+ cognition-judge 1
+ book-writer 1
+ cold-reader 1
= 11
```

这是标准首轮实例数。合同允许的返工会新增任务，因此包含定向补提名、候选返工或事实阻塞重跑的实际 run 任务数可能大于 11；本次没有运行 manifest，不能声称任何真实 run 实际使用 11 个任务。

## 原阻塞逐项复核

| 原检查点 | 当前结构证据 | actual |
|---|---|---|
| body artifact / status | source-map 有可解析 body_artifact、稳定 text_ref、统一 status | pass |
| 提名 links | links item 有 target_locator / relation | pass |
| 提名 0 条 | zero_nomination_reason | pass |
| 提名实例数 | README=2；合同 instance_id 1/2 | pass |
| 归并返工 | coverage_gaps 含 target_locators/question/return_to | pass |
| 调查问题保留 | merged_anchors 保留 investigation_question/context_links | pass |
| claim schema | facts_to_check 有三层 id、文本、类型、影响 | pass |
| fact 映射 | checks 回写 claim/candidate/anchor ids | pass |
| fact 聚合 | material claim 的 pass/fail/blocked 明文规则 | pass |
| locked anchor_id | locked_packets 保留 anchor_id | pass |
| judge 返工 | target_role、affected_ids、question | pass |
| writer 最终页面装配 | reader_page + assembled_page_ref + insertions | pass |
| writer 0 条 | body-only 页面 | pass |
| cold-reader 布尔 | needs_reorganization true/false | pass |
| cold-reader 聚合 | 全部单元条件、任一失败、污染 blocked | pass |
| cold-reader 0 条 | body-only -> not-applicable | pass |

## 状态枚举一致性

生产/判断角色中，source-map、anchor-nominator、anchor-merger、cognition-candidate、cognition-judge、book-writer 使用统一角色状态：

```text
not-run | pass | fail | blocked
```

fact-checker 作为事实门使用：

```text
pass | fail | blocked
```

cold-reader 额外需要表达无陪读单元的合法路径，因此使用：

```text
not-applicable | pass | fail | blocked
```

这些差异与角色语义一致，不是枚举冲突。各生产角色还提供 `blocked_reason` 和 `return_to`；精确返工对象分别由 merger 的 coverage gap 和 judge 的 return_questions 表达。

一个非阻塞性余量是部分 `return_to` 仍为自由字符串、writer 的 `verification` item 未细分 schema；但当前职责、停止路径和直接 handoff 不依赖这些字段的额外枚举，不能据此否定本轮指定阻塞已经闭合。

## 最终判断

- role_contracts_reviewed: `8/8`
- role_index_reviewed: `yes`
- standard_execution_tasks: `11`
- coordination_instances_outside_execution_count: `1`
- individual_role_verdicts: `8 pass / 0 fail / 0 blocked`
- original_blockers: `16 pass / 0 fail / 0 blocked`
- deterministic_schedule_reconstructed: `yes`
- zero-acceptance_path_closed: `yes`
- end_to_end_structural_cold_start_verdict: `pass`

当前 8 份角色合同与索引已经可以在不读取完整图书协议的条件下重建标准 11 任务图，并完成 source body、锚点、候选、事实、裁判、成文装配和冷读之间的结构化 handoff。0 条提名、0 条候选、0 条接受以及 blocked/返工路径均有可表达状态。

可声称范围：仅能声称本次限定读取下，8 份当前角色合同的结构冷启动复跑通过，用户点名的原阻塞已闭合，标准实例数可重建为 11。不能声称真实图书 run 已发生、11 个 Agent 已实际调度、完整图书协议通过、历史回归通过、内容质量通过或用户体验通过。
