# Run Integrity 派生结构回归复跑 7：最终图书事实批次 schema

## 执行边界

- evaluated_at_utc: `2026-07-10T11:55:01Z`
- evaluated_at_local: `2026-07-10T07:55:01-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_files_preserved: `true`
- previous_raw_files_used_as_evidence: `false`

本次重新读取当前 7 张 run-integrity case、运行合同、图书协议、cognition-candidate 与 fact-checker 合同。旧 raw 保留，未修改、未作为本次 verdict 证据；未修改 case 或规则。

判定口径：`reject` 表示合成场景命中硬门；`accept-structure-only` 只表示合成 manifest、typed requests、batch checks、coverage、dispatch 与门状态在当前合同下闭合。全部 case 均为 `derived-structure / runtime-not-run`。

---

## RI-N01

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

fresh 复用上一 run 的 source map，并声明未重跑。Fresh 要求生成产物零复用，故 reject。

可声称范围：只证明合成结构应拒绝，不证明真实旧产物被读取。

---

## RI-N02

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

fresh 输出目录已存在且会写入上一 run，违反唯一隔离目录和不得覆盖/混写/回填，故 reject。

可声称范围：只证明合成隔离字段非法，不证明真实磁盘污染。

---

## RI-N03

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

RI-N03 有非空 request ref，但 conditional fact evidence 和 aggregate evidence 仍是 previous-run audit，且 `relocated_and_verified_this_run: false`。Typed request 只解决引用结构，不能替代本次定位核实；Fresh 和 fact-checker 均要求外部事实使用本次 high-trust 证据。因此 conditional fact check、aggregate source_and_fact、run_integrity 与 accepted 均不成立，actual reject 与 Expected 匹配。

可声称范围：只证明 typed request 不能让旧 audit 冒充本次证据；不判断事实真假，也不证明真实核查发生。

---

## RI-N04

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

revision 实际读取旧 reader page，却把复用生成物、未重跑、跳过与 cannot_claim 留空。Revision 披露不闭合，故 reject。

可声称范围：只证明合成 revision 非法，不证明真实 revision 或质量结果。

---

## RI-N05

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

样本影响能力结论，确认必需且 pending；场景却 running 并执行 source-read。当前状态机要求 awaiting-user 且不得 dispatch，故 reject。

可声称范围：只证明合成状态转换非法，不证明用户真实选择或执行发生。

---

## RI-N06

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

只登记语法检查与资产卡冷启动，核心 fresh 链段均 skipped，却声明完整 fresh 和 run_integrity 通过，且 cannot_claim 为空。声明超出执行与验收交集，故 reject。

可声称范围：只证明合成声明越界，不证明局部检查真实通过。

---

## RI-P01

- expected: `accept-structure-only`
- actual: `accept-structure-only`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### Fresh 与运行前置

- route 为 book；原始路径、指纹和读取范围齐全。
- 样本确认组合 `false + not-required` 合法。
- 生成物零复用。
- 输出为新隔离目录，不写旧 run。

前置结构闭合。

### 图书 typed requests

三个 cognition-candidate 实例各有一份 required request：

- request id、claim id、candidate id、anchor id 均非空并分别可追踪。
- kind 使用 `source-internal | external`。
- assertion_type 使用 `factual | causal`，因果断言不再混入来源 kind。
- materiality 使用 `material | non-material`。
- 三份 request 分别覆盖源内事实、外部普通事实和外部因果断言。

这与当前 cognition-candidate 的 typed fact request handoff 一致。

### 最终 batch checks

fact_check_batch 的 request_ids 与三份输入 request id 集合精确相等。三个 checks 均包含最终 schema 所需的 handoff 身份：

- 非空唯一 check id
- request id / claim id
- candidate id / anchor id
- kind
- assertion_type
- materiality
- verdict
- sources 的 ref / locator / trust / verified_this_run

逐项核对：

- check 1 与 claim 1 同为 source-internal / factual / material。
- check 2 与 claim 2 同为 external / factual / non-material。
- check 3 与 claim 3 同为 external / causal / material。
- 三条 verdict 均 supported。
- 两条外部事实都有 high 且 verified_this_run true 的 fixture source；源内事实回到 fixture chapter line 10。

三条 coverage 分别满足 request_claim_ids 与 checked_claim_ids 精确相等，complete 均为 true；non-material claim 同样被检查，没有绕过。batch overall 为 pass。

结论：request → check → per-request coverage → overall 的最终批次 schema 完整闭合。

### 11 个实例级 dispatch

executed 包含 source-map 1、nominator 2、merger 1、candidate 3、fact-checker 1、judge 1、writer 1、cold-reader 1，共 11 个唯一 dispatch。

- `actual_tasks: 11`
- `task_limit: 12`
- skipped / failed / reused 为空

fact-checker 在一个批量任务中处理三份 requests，不扩成三个任务；盲区检查并入 cognition judge。任务计数与固定 11 一致。

### Nested source_and_fact 与 accepted

- source provenance pass，有 source-map evidence。
- conditional fact check pass，request_refs 精确列三份 request，evidence 指向 batch。
- aggregate source_and_fact pass，owner/scope/evidence/conflicts 齐全。
- absolute value、regression、cold read、run integrity 均 pass。
- cold-start/reproduction not-applicable；user experience not-requested。
- 无 blocked、pending、failed、awaiting acceptance 或超预算。

can_claim 只覆盖合成结构接受；cannot_claim 明确排除真实 fresh、内容质量、用户体验和全部能力。accepted 在当前 fixture 内闭合。

### 为什么仍只能 structure-only

本次读取并核对的是自包含 fixture。request、checks、coverage、来源、dispatch 和门结果没有经过现场执行；没有打开 fixture-primary-source、运行 fact-checker、验证 `verified_this_run` 的真实性或取得用户回执。

因此只能接受“最终批次结构可表达且自洽”，不能声称真实核查或 fresh run 通过。actual 为 `accept-structure-only`，runtime 为 `runtime-not-run`。

可声称范围：只可声称 RI-P01 是当前最终 book fact batch schema 下的结构正例；不可声称真实 fresh、事实/内容质量、用户体验、Phase 4 或 ReaderLab 全能力通过。

---

## 汇总

| case | expected | actual | match | kind | runtime |
|---|---|---|---|---|---|
| RI-N01 | reject | reject | yes | derived-structure | runtime-not-run |
| RI-N02 | reject | reject | yes | derived-structure | runtime-not-run |
| RI-N03 | reject | reject | yes | derived-structure | runtime-not-run |
| RI-N04 | reject | reject | yes | derived-structure | runtime-not-run |
| RI-N05 | reject | reject | yes | derived-structure | runtime-not-run |
| RI-N06 | reject | reject | yes | derived-structure | runtime-not-run |
| RI-P01 | accept-structure-only | accept-structure-only | yes | derived-structure | runtime-not-run |

- matched_cases: `7/7`
- mismatched_cases: `0/7`
- blocked_cases: `0/7`
- suite_verdict: `pass-derived-structure-only`
- runtime_verdict: `not-run`

## 总结论

当前 7 张 run-integrity 派生结构卡 7/7 与 Expected 匹配。RI-P01 的 final batch checks 已与 request 的 kind/assertion_type/materiality 逐项一致，三份 coverage 精确闭合；11 dispatch、nested source_and_fact 和 accepted 均结构成立，只获得 structure-only 接受。RI-N03 仍因未本次核实的旧 audit 而 reject。

总 verdict 为 `pass-derived-structure-only`，runtime 为 `not-run`。本结果不构成历史回放、真实运行、事实/内容质量、用户体验、Phase 4 或 ReaderLab V3 整体通过。
