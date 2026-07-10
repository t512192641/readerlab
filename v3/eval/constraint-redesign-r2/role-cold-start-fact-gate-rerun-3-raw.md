# 来源与事实门三个剩余冲突第三次复核原始输出

## 复核边界

- 时间：`2026-07-10T07:38:06-04:00`。
- 本次只复核：非空唯一 request/check id 与精确集合覆盖、orchestrator / manifest 的嵌套 source_and_fact 持久化、所有 request 中可见外部事实的 supported + 本次 high-trust 条件。
- 本次读取：机制候选、fact-checker、skill-judge、orchestrator、run-manifest、skill-engine、judge 中与三项相关的当前字段和规则。
- 上一份失败 raw 保留不改；本次不修改规则文件。
- 上下文声明：本执行者做过前两次事实门复核；本次不是零上下文，但 verdict 只依据当前文件逐项重判。

## 总结结论

- overall verdict：`fail`。
- 第 1 项通过：request / claim / check id 已要求非空唯一，coverage.complete 也绑定 request_claim_ids 与 checked_claim_ids 精确集合相等。
- 第 3 项主体通过：request 收集所有可见外部事实，不论 materiality；fact-checker 只有全部 supported 且外部事实具备本次 high-trust 来源才可 overall pass。
- 第 2 项仍失败：manifest 与 orchestrator 都改成嵌套对象，但形状仍不相同。orchestrator 顶层 source_and_fact 还有 owner、scope、evidence、conflicts，manifest 同名对象没有这些字段；“逐字段写入同名对象”无法成立。
- 额外跨文件漂移：judge 聚合说明仍写“覆盖 request 中全部 material claims”，弱于其他文件的“覆盖全部 request claims / 所有可见外部事实”。即便执行链当前更严格，裁判协议仍可被独立读取为较弱门槛。
- 因仍有 schema 冲突，本次必须 fail。

## 1. 非空唯一 ID 与集合精确相等

- verdict：`pass`。
- request：required 时使用本 run 内非空唯一 request id；每个 request claim 使用非空唯一 claim id。
- result：fact-checker 精确回填输入 request_id；每个 check id 在本 run 内非空唯一。
- coverage：`coverage.complete: true` 仅当 `request_claim_ids` 与 `checked_claim_ids` 集合精确相等，无遗漏、无多项。
- judge 回交：以 `{check_id, claim_id}` 引用，并记录 `missing_request_claim_ids`；任一 request claim 覆盖不完整即停止。
- 判断：上一轮的空 id、重复 id、遗漏后自报 complete 和多查项冒充覆盖均已被规则排除。
- 可声称范围：可声称静态 ID / coverage 不变量闭合；不能声称真实 request 已满足。

## 2. Orchestrator 与 manifest 嵌套持久化对象

- verdict：`fail`。
- 已修复部分：manifest `verification.source_and_fact` 不再是标量，已包含：
  - `status`
  - `source_provenance: {status, owner, evidence}`
  - `conditional_fact_check: {status, owner, request_ref, evidence}`
- orchestrator 同名对象包含：
  - `status`
  - `owner: orchestrator`
  - 同样两个子门
  - `scope`
  - 顶层 `evidence`
  - `conflicts`
- 直接冲突：orchestrator 明确要求 source_and_fact 对象“逐字段写入 manifest 同名对象”，但 manifest schema 没有顶层 `owner / scope / evidence / conflicts`。两者虽都嵌套，仍不是同形对象。
- 影响：
  - 按 orchestrator 输出，四个顶层字段在 manifest 无合法位置；
  - 按 manifest 输出，无法保存聚合 owner、整门范围、聚合证据和冲突；
  - “verification 必须与同一 manifest 完全一致”无法逐字段验证。
- 最小剩余修复：让 manifest source_and_fact 与 orchestrator 完全同形，或把 orchestrator 的额外字段移到 manifest 中一个明确、可引用的同 run 记录，并把“逐字段写入同名对象”改成精确引用规则。

## 3. 所有可见外部事实 supported + 本次 high-trust

- verdict：`partial`。
- 通过链段：
  - mechanism auditor：只要候选含任何可见外部事实，就列入 request，不论 materiality；
  - skill-engine：要求有任何可见外部事实时列全 request claims；
  - fact-checker：coverage 完整且 request 中每个可见事实均 supported 才 overall pass；任一缺失 / conflicted / insufficient / out_of_scope 均 fail；
  - external supported：必须至少有一个本次定位核实的 high 来源；
  - skill-judge：任一 request claim 覆盖不完整即停止。
- 主体判断：上一轮 non-material 外部事实可能无证据随 overall pass 的漏洞已被 fact-checker 聚合规则关闭。
- 剩余协议漂移：judge 的来源与事实门聚合句仍写“触发时必须覆盖 request 中全部 material claims 并通过”，没有同步为“全部 request claims / 所有可见外部事实”。该文件虽同时要求可见外部事实回到高可信来源，但结构化聚合说明仍保留较弱范围。
- 影响：只读 judge 的独立裁判可认为 non-material request claim 不在完整覆盖硬门内；只读 fact-checker / skill-engine 的执行者则会要求全部覆盖。当前七文件没有完全一致的门槛表述。
- 最小剩余修复：把 judge 的聚合句从“全部 material claims”改为“全部 request claims；所有可见外部事实不论 materiality 均须 supported，且外部事实至少有本次 high-trust 来源”。

## 三项矩阵

| 项目 | verdict | 结论 |
| --- | --- | --- |
| 非空唯一 request/check id + 精确集合覆盖 | `pass` | ID 与 coverage 不变量已闭合。 |
| orchestrator / manifest 同形嵌套持久化 | `fail` | 都已嵌套，但 manifest 缺四个顶层字段。 |
| 所有可见外部事实 supported + 本次 high-trust | `partial` | 执行链已严格；judge 聚合句仍仅写 material claims。 |

## 最终可声称范围

- 可以声称：ID、精确覆盖和 fact-checker 对所有 request 可见事实的 high-trust supported 门已修复。
- 不可以声称：source_and_fact 能在 orchestrator 与 manifest 间逐字段无损持久化，或七份合同对全部可见事实覆盖门槛完全一致。

最终 overall verdict：`fail`。
