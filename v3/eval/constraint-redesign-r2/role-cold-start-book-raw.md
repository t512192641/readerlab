# 图书角色合同冷启动原始检查

## 检查边界与此前上下文

- checked_at_utc: `2026-07-10T10:57:26Z`
- checked_at_local: `2026-07-10T06:57:26-04:00`
- check_kind: `role-contract-cold-start`
- runtime_status: `runtime-not-run`
- content_generation: `not-run`
- historical_regression_replay: `not-run`
- previous_context_present: `true`

这不是“完全无历史上下文”的审查。同一会话此前已做过运行完整性派生结构回归：当时读取过仓库 `AGENTS.md`、`v3/current-task.md`、`v3/skill/SKILL.md`、run manifest、Phase 4 闸门、独立验收门和 7 张 run-integrity 派生结构卡，并写入对应 raw。此前没有读取本次 8 份图书角色合同、完整图书协议或图书回归证据。

本次新增读取严格限制为：

- `v3/skill/roles/source-map.md`
- `v3/skill/roles/anchor-nominator.md`
- `v3/skill/roles/anchor-merger.md`
- `v3/skill/roles/cognition-candidate.md`
- `v3/skill/roles/fact-checker.md`
- `v3/skill/roles/cognition-judge.md`
- `v3/skill/roles/book-writer.md`
- `v3/skill/roles/cold-reader.md`

未读取完整图书协议、图书回归 case、旧图书回归结果、真实运行产物或生产日志。本次不借此前看过的外部编排声明填补角色合同缺失；调度图和任务数只从上述 8 份合同重建。此前上下文仅用于如实披露本检查并非绝对背景隔离。

## 检查口径

逐角色检查：任务是否单一明确、输入是否足以执行、输出 schema 是否能被下一角色直接消费、禁令是否封住越权、停止条件是否可执行、自足性是否成立、状态枚举是否闭合。

自足性取值：

- `sufficient`：给定合同允许输入后，可独立完成并产生可直接交接的结构化输出。
- `partial`：主要职责可执行，但停止/交接或字段语义仍依赖主控补充。
- `insufficient`：存在无法由允许输入得出的必填输出，或下游所需关键产物无人产出。

---

## 1. source-map

- role: `图书正文 / 来源地图`
- self_sufficiency: `partial`

### 任务

任务边界清楚：从登记原始来源建立完整正文与位置映射，只做允许的轻量清理，不做任何 AI 陪读生产。

### 输入

输入限定为本轮原始图书/长文、范围边界、两条线路规则摘录、轻量清理规则和已确认可剥离旧 AI 块清单。若主控实际把这些内容完整下发，执行者不必读取完整协议。

缺口：合同要求“建立完整正文”，但没有定义原始来源如何随 `body_units` 一起交付，也没有说明 `text_ref` 是正文文本、文件路径、锚点还是另一个 artifact 的引用。

### 输出 schema

- `body_units`: `unit_id`、`text_ref`、`source_locator`
- `source_map`: `source_locator`、`target_unit`、`action`、`reason`
- `anomalies`: `locator`、`issue`、`impact`

`source_map.action` 枚举为 `kept | moved | deleted`，清楚。关键不足是正文产物本身没有确定结构：如果 `text_ref` 不是可解析引用，下游拿不到“已映射正文单元”；如果它是引用，合同没有给引用解析规则或正文 artifact 路径。

### 禁令

禁令清楚，能阻止该角色写摘要、陪读、认知候选或压缩改写原文。

### 停止条件

原始来源未登记、范围不清、正文缺损会改变判断、删除超授权时停止，条件合理。缺口是输出 schema 没有 `status`、`blocked_reason` 或 `return_to`，停止只能靠自由文本上报。

### 状态枚举

- 已有：`action: kept | moved | deleted`
- 缺失：角色整体 `completed | blocked`，以及异常是否阻塞的结构化状态。

### 判断

职责和禁令足以约束工作，但正文 artifact 与停止交接没有闭合，因此不能算完全自足。

---

## 2. anchor-nominator

- role: `图书锚点提名`
- self_sufficiency: `partial`

### 任务

任务单一明确：只找作者论证的承重位置并提交可定位提名，不扩写候选。

### 输入

输入是线路规则摘录和已完成 source map 的正文单元。依赖顺序明确，但它默认 source-map 已交出可读取正文；前一合同的 `text_ref` 未定义会向此处传递。

### 输出 schema

`nominations` 包含锚点 id、原文位置、文本内主张、承重理由、浅读/误读风险、调查问题、前后连接、置信度和少数派标记，基本覆盖职责。

字段缺口：

- `links: []` 没有 item schema，不能判断链接的是正文 locator、anchor id 还是论证关系。
- 没有合法 `0 nominations` 的说明，也没有区分“确实没有承重锚点”和“因输入缺口无法提名”。
- 停止时要求“标记缺口”，但输出没有 `gaps`、`status` 或 `blocked_reason`。

### 禁令

禁令能阻止外部搜索、候选扩写、数量凑数和个人兴趣替代论证重要性。

### 停止条件

来源映射未完成、关键上下文缺失、无法以原文证明承重性时停止，方向正确；但无结构化停止输出。

### 状态枚举

- 已有：`confidence: high | medium | low`；`minority_high_potential: true | false`
- 缺失：提名结果/角色整体状态、输入阻塞状态。

### 判断

正常路径可执行，异常路径和 `links` 的机器可交接性不闭合，属于部分自足。

---

## 3. anchor-merger

- role: `图书锚点归并`
- self_sufficiency: `partial`

### 任务

任务清楚：合并多份提名、去重、保留来源关系、形成入围锚点集，并发现覆盖空白。

### 输入

要求“同一正文范围的全部锚点提名及其原文定位”。这明确了必须发生多份提名，但没有声明提名任务数量、如何确认“全部”已经齐备或每份提名的 producer id。

### 输出 schema

- `merged_anchors`: 能记录 `source_locators`、`merged_from`、论证任务、置信度和少数派高潜标记。
- `coverage_gaps.action`: `retain_gap | request_targeted_nomination`。

主要缺口：

- `request_targeted_nomination` 没有对应的目标正文范围、问题、返回角色和新任务 id，无法直接触发定向返工。
- 归并后不再保留 `claim_in_text`、`investigation_question` 或上下文连接；下游候选角色被告知会收到“对应原文片段”，但该片段不在本合同输出中，只能由主控再次拼装。
- 没有整体 `pass | blocked | return` 状态。

### 禁令

禁令能阻止简单多数票、伪差异、事实补充和提前生产认知候选。

### 停止条件

范围不一致、定位不可核对或需定向补提名时停止并退回主控。逻辑正确，但退回请求没有结构化载体。

### 状态枚举

- 已有：`confidence: high | medium | low`；`minority_high_potential: true | false`；`action: retain_gap | request_targeted_nomination`
- 缺失：归并整体状态与定向返工状态。

### 判断

归并判断本身可做，但精确定向返工与下游原文交接依赖主控额外解释，属于部分自足。

---

## 4. cognition-candidate

- role: `图书认知候选`
- self_sufficiency: `partial`

### 任务

任务边界清楚：每个候选只形成一个可独立裁判的完整认知，不交素材集合、不写成稿、不自评通过。

### 输入

入围锚点、对应原文片段和主控允许的必要证据范围足以约束正常生产；但“允许的必要证据范围”没有本地 schema，只能依赖主控自由文本。

### 输出 schema

候选包含 `candidate_id`、`anchor_id`、唯一判断、默认读法、必要证据、阅读改变、边界和待核事实，主体结构完整。

关键缺口：`facts_to_check: []` 没有 item schema。下一角色输出以 `claim_id` 为主键，但本角色没有规定每条待核事实必须提供 `claim_id`、事实文本、来源类型、影响对象或候选关联。因而候选到事实核查的直接 handoff 不闭合。

### 禁令

禁令能阻止素材堆积、多问题拼接、提前成文和自我宣布通过。

### 停止条件

锚点未锁定、原文不足、关键事实缺失到不可裁判时停止并返回缺口。输出 schema 没有缺口或角色状态字段。

### 状态枚举

- 已有：无明确枚举；集合字段均为自由结构。
- 缺失：候选生产状态、事实待核项状态、停止/退回状态。

### 判断

认知候选主体可生成，但事实核查交接缺少最关键的 claim schema，因此只能部分自足。

---

## 5. fact-checker

- role: `事实核查`
- self_sufficiency: `partial`

### 任务

任务清楚：只核实外部事实、来源强度和边界，不裁判认知价值，也不改写价值主张。

### 输入

输入包括待核事实清单、原始来源、source map 和获准高可信外部来源。问题在于上游 `facts_to_check` 没有 item schema，而本角色需要稳定的 `claim_id`；角色合同之间没有定义如何建立该 id。

### 输出 schema

- item verdict: `supported | conflicted | insufficient | out_of_scope`
- overall: `pass | fail | blocked`
- 每项还有来源位置、信任说明、结论影响和最小修正。

关键缺口：

- `checks` 没有 `candidate_id` 或 `anchor_id`，只能靠未定义的 `claim_id` 回接候选。
- `sources[].trust`、`conclusion_impact` 是自由文本，没有最低判定枚举。
- `overall` 如何由逐项 verdict 聚合没有规则，例如 `out_of_scope` 或不改变结论的 `insufficient` 是否必然 fail 不明确。
- `overall: blocked` 时没有顶层 `blocked_reason`。

### 禁令

禁令明确阻止用趣味、文风、相对最好或低可信二手材料替代事实判断。

### 停止条件

关键来源不可访问、身份不明、结论性冲突无法裁定、需付费/敏感来源时停止，覆盖关键风险；结构化输出不足以表达停止原因。

### 状态枚举

- 已有：逐项四态；整门 `pass | fail | blocked`
- 缺失：来源可访问状态、阻塞原因枚举，以及逐项到整门的聚合规则。

### 判断

核查方法与禁令清楚，正常逐项判断可执行；但上游 claim schema、候选映射和整门聚合仍需主控补充，属于部分自足。

---

## 6. cognition-judge

- role: `图书认知裁判`
- self_sufficiency: `partial`

### 任务

任务顺序明确：先做整批关键盲区检查；无关键盲区后再做绝对门淘汰；接受项锁定唯一判断、证据、落点、边界和禁止枝节；合法输出 0 条。

### 输入

输入覆盖候选、锚点、事实核查结果、裁判标准和经回归角色路由的判例。正常判断所需类别齐全，但事实核查结果无法稳定映射候选的问题会传入本角色。

### 输出 schema

- `batch_gap_check.status: pass | blocked`
- item verdict: `accept | reject | blocked`
- `locked_packets` 与 `selection_count`

关键缺口：

- `locked_packets` 保留 `candidate_id` 和 `source_locators`，却没有保留 `anchor_id`。
- 下游 book-writer 的输出要求填写 `anchor_id`，而其允许输入所列锁定包也没有 `anchor_id`；因此 writer 无法仅凭允许输入无损生成自己的必填字段。
- 关键盲区需“定向退回”时只有 `return_questions`，没有 `return_to`、目标 candidate/anchor、返工范围或角色整体 `return` 状态。
- `verdicts.reasons` 是无 item schema 数组；合同要求主因清晰，但没有限制主因数量或分类。

### 禁令

禁令能阻止相对排名、机械高分、成文补救、添加事实和扩成第二问题。

### 停止条件

事实未完成、候选锚点失配、关键盲区、判例冲突和必须修改候选才可通过时停止。覆盖充分，但“退回谁、退回什么”没有结构化闭合。

### 状态枚举

- 已有：批次 `pass | blocked`；逐候选 `accept | reject | blocked`
- 缺失：明确 `returned` 状态、退回目标、整门结果以及锁定包的交接完整性状态。

### 判断

裁判职责和硬门较清楚，但裁判到成文的 `anchor_id` 丢失，以及返工路由未结构化，使其只能部分自足。

---

## 7. book-writer

- role: `图书成文`
- self_sufficiency: `insufficient`

### 任务

任务边界清楚：只把已锁定的单一认知写成自然中文陪读，不重选题、不加料、不暴露生产术语。

### 输入

允许输入是线路规则摘录、页面槽位要求和锁定判断包。锁定包清单包含唯一判断、必要证据、原文落点、边界和禁止枝节，但没有 `anchor_id`。

### 输出 schema

`reader_units` 要求 `unit_id`、`anchor_id`、标题、正文、`locked_candidate_id`、已用证据和边界是否表达。

存在两个阻塞性交接缺口：

1. 输出必填 `anchor_id`，但允许输入和上游 `locked_packets` 都没有该字段。执行者若填写，只能从 locator 猜测或请求主控补字段，违反自足。
2. 本角色只输出陪读 `reader_units`，没有输出“最终读者可见正文 + 对应陪读单元”的装配页；下一角色 cold-reader 明确要求最终读者可见组合输入。8 份合同中没有单独页面装配角色，也没有把装配职责和 schema 放进本合同。

另有歧义：`boundary_expressed: true` 写成固定 literal，像验收要求而非可报告布尔值；如果边界不适用或无法表达，没有合法输出状态。

### 禁令

禁令足以阻止重选题、新事实、落选候选拼接、第二问题和生产术语泄漏。

### 停止条件

锁定包不全、证据说不清、必须加料、无法保持单一任务时退回裁判，方向清楚；schema 没有 `blocked` / `returned` 输出。

### 状态枚举

- 已有：`boundary_expressed: true`，但更像固定约束而非完整枚举。
- 缺失：`true | false | not-applicable` 的明确语义、成文状态、退回状态、最终装配状态。

### 判断

由于允许输入无法产生必填 `anchor_id`，且没有主体与陪读的最终装配产物，合同无法独立完成到 cold-reader 的交接，判定为不自足。

---

## 8. cold-reader

- role: `图书无上下文冷读`
- self_sufficiency: `insufficient`

### 任务

任务单一明确：只看最终读者内容，复述读懂了什么、理解增量、原文读法变化、费力点和是否需二次整理；不修文、不猜作者意图放行。

### 输入

要求“最终读者可见的正文片段与对应陪读单元”和空白输出字段。问题是上游 8 份合同没有任何角色被明确授予最终页面装配职责，也没有相应输出 schema，因此该输入无法由当前角色链直接产出。

### 输出 schema

- `reads`: 单元 id、复述、理解增量、阅读改变、费力点、是否需重整
- `verdict: pass | fail | blocked`
- `blocked_reason`

关键 schema 错误：`needs_reorganization: true` 被写成固定 literal，无法表达 `false`。职责要求判断“是否需要二次整理”，因此 schema 必须至少容纳 true/false；现状会迫使所有 read 都声称需要重整，或让执行者自行改 schema。

另一个缺口是 verdict 聚合规则未定义：什么组合构成 pass、`needs_reorganization: true` 能否仍 pass、多个单元一部分失败时整门如何判断都不明确。

### 禁令

禁令能有效维持盲测：禁止读取生产上下文、替作者修文或凭猜测放行。

### 停止条件

输入污染、正文与陪读失配、必须请求生产解释时停止并判测试无效；这可映射 `blocked`，且 `blocked_reason` 可记录原因，是 8 份合同中停止输出较完整的一份。

### 状态枚举

- 已有：`verdict: pass | fail | blocked`
- 错误/缺失：`needs_reorganization` 仅允许 true；多单元到总 verdict 的聚合规则缺失。

### 判断

角色自身的观察任务可执行，但上游没有合法产生最终组合页面，且 schema 不能表达“不需要二次整理”，因此端到端冷启动不自足。

---

## 重建的调度顺序

仅按 8 份角色合同，可以重建以下主链：

```text
source-map
  -> anchor-nominator × N（并行，同一正文范围）
  -> anchor-merger
       -> 若 request_targeted_nomination：退回 anchor-nominator（目标字段缺失）
  -> cognition-candidate
  -> fact-checker
  -> cognition-judge
       -> 若关键盲区：定向退回上游（目标角色/范围未结构化）
       -> 若 selection_count = 0：无锁定包；后续 writer/cold-reader 是否跳过未规定
  -> book-writer
  -> [最终正文 + 陪读页面装配：当前合同链缺少责任主体与 schema]
  -> cold-reader
```

### 依赖和返工判断

- `source-map -> anchor-nominator`：明确。
- `anchor-nominator -> anchor-merger`：明确要求多份提名，但并行数量未声明。
- `anchor-merger -> cognition-candidate`：主输入关系明确，原文片段需主控额外拼装。
- `cognition-candidate -> fact-checker`：顺序明确，claim item schema 不兼容。
- `fact-checker -> cognition-judge`：顺序明确，claim 到 candidate 的映射缺失。
- `cognition-judge -> book-writer`：顺序明确，`anchor_id` 在 handoff 中丢失。
- `book-writer -> cold-reader`：不能直接连接，中间缺少最终页面装配。

## 任务计数

### 可确定的数量

- 角色种类：`8`
- 串行阶段种类：`8`，但 anchor-nominator 是并行 fan-out；页面装配又是未建模阶段。
- anchor-merger 明确要求“多份锚点提名”，因此 `N >= 2`。

如果暂时假设其余 7 个角色各执行 1 次、页面装配不算独立 Agent 任务，则：

```text
total_tasks = 7 + N
N >= 2
minimum_total_tasks = 9
```

### 无法确定的数量

仅凭 8 份合同无法得到唯一标准任务数，原因是：

- anchor-nominator 的 N 没有固定。
- cognition-candidate、fact-checker、book-writer 和 cold-reader 虽可在一个输出数组中处理多项，但未声明是一批 1 个任务还是按项 fan-out。
- `selection_count = 0` 时 writer 与 cold-reader 是否仍运行未规定。
- 定向补提名、候选返工和事实冲突重跑会新增多少任务未规定。
- 页面装配缺失，无法判断它由主控机械完成、由 book-writer 兼任，还是另计 Agent 任务。

因此，本次冷启动能诚实给出的任务数是：`8 个角色类型；正常链最少 9 个 Agent 任务；精确标准任务数不可由这些合同独立重建`。任何更精确数字都需要读取本次禁止读取的编排协议，或由主控提供 fan-out 配置。

## 跨合同状态枚举检查

现有枚举并不统一：

| 位置 | 枚举 |
|---|---|
| source map action | `kept | moved | deleted` |
| nomination / merged confidence | `high | medium | low` |
| coverage gap action | `retain_gap | request_targeted_nomination` |
| fact item | `supported | conflicted | insufficient | out_of_scope` |
| fact overall | `pass | fail | blocked` |
| judge batch gap | `pass | blocked` |
| judge item | `accept | reject | blocked` |
| cold-reader overall | `pass | fail | blocked` |

主要缺口：

- source-map、anchor-nominator、anchor-merger、cognition-candidate、book-writer 没有角色整体完成/阻塞/退回状态。
- `blocked`、`return`、`request_targeted_nomination` 没有统一的目标角色、原因、受影响 id 和重跑范围字段。
- judge 的 `accept | reject | blocked` 与 fact/cold-reader 的 `pass | fail | blocked` 各自合理，但没有主控可直接消费的共同 envelope。
- `needs_reorganization: true` 不是完整布尔枚举。

一个最小共同 handoff envelope 至少需要能表达：角色、任务 id、`completed | blocked | returned`、原因、返回目标、受影响对象、产物引用和不可声称范围。这里仅指出缺口，不修改合同或提出正式新 schema。

## 最终判断

- role_contracts_reviewed: `8/8`
- individual_roles_fully_sufficient: `0/8`
- individual_roles_partial: `6/8`
- individual_roles_insufficient: `2/8`
- deterministic_role_order_reconstructed: `yes_with_missing_assembly`
- deterministic_standard_task_count_reconstructed: `no`
- minimum_normal_task_count_from_contracts: `9`
- end_to_end_cold_start_verdict: `fail`

主要失败链：

1. `cognition-candidate.facts_to_check` 没有可供 fact-checker 消费的 claim schema。
2. fact-checker 结果没有稳定映射回 candidate。
3. cognition-judge 的 locked packet 丢失 book-writer 必填的 `anchor_id`。
4. book-writer 与 cold-reader 之间缺少最终正文 + 陪读页面装配责任和产物 schema。
5. cold-reader 的 `needs_reorganization` 只能取 true。
6. 合同没有声明 fan-out 数量，无法从角色冷启动重建唯一标准任务数。

可声称范围：仅能声称上述 8 份合同在本次限定读取下的结构冷启动没有闭合，且正常链最少需要 9 个 Agent 任务；不能声称完整图书协议失败、真实图书 run 失败、图书回归失败、内容质量失败或用户体验失败。
