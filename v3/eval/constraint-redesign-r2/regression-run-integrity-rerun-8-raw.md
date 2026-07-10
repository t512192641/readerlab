# Run Integrity 派生结构回归复跑 8：最终请求与回交字段

## 执行边界

- evaluated_at_utc: `2026-07-10T15:53:48Z`
- evaluated_at_local: `2026-07-10T11:53:48-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_files_preserved: `true`
- previous_raw_files_used_as_evidence: `false`

本次只读取当前 7 张 run-integrity case、`v3/skill/SKILL.md`、run manifest、Phase 4 闸门、独立裁判协议，以及图书 cognition-candidate / cognition-judge / fact-checker 合同。未读取旧 raw 作为 verdict 证据，未修改规则或 case。

判定口径：`reject` 表示合成场景命中当前硬门；`accept-structure-only` 只表示合成字段、handoff、计数和门状态在当前合同下自洽。所有 case 都是派生结构测试，不是历史回放或真实运行。

---

## RI-N01

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

fresh 声明复用旧 source map，并将其列为未重跑。当前 Fresh 合同要求生成产物零复用，故拒绝。

## RI-N02

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

输出目录已存在且写入上一 run，违反唯一隔离目录与不得覆盖、混写、回填旧 run，故拒绝。

## RI-N03

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

条件事实门引用 previous-run audit，且 `relocated_and_verified_this_run: false`。旧 URL 只能作定位线索，不能作为本次 fresh 核实证据；`source_and_fact`、`run_integrity` 与 accepted 均不能成立，故拒绝。

## RI-N04

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

revision 实际读取旧 reader page，却没有列复用生成物、未重跑链段和不可声称范围，披露不闭合，故拒绝。

## RI-N05

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

样本影响能力结论且确认仍为 pending，场景却进入 running 并执行 source-read。状态应停在 awaiting-user 且不得 dispatch，故拒绝。

## RI-N06

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

只执行语法检查与资产卡冷启动、跳过核心 fresh 链段，却声明完整 fresh 流程通过，超出“实际执行 + 对应验收”的交集，故拒绝。

## RI-P01

- expected: `accept-structure-only`
- actual: `accept-structure-only`
- match: `yes`
- runtime: `runtime-not-run`

### Fresh 前置与任务账本

- route 为 `book`；原始路径、指纹、实际读取范围齐全。
- 样本组合为 `false + not-required`；生成产物零复用；输出目录声明为全新隔离目录且不写旧 run。
- executed 有 11 个唯一实例级 dispatch：source-map 1、anchor nomination 2、merge 1、cognition candidate 3、fact-checker 1、cognition judge 1、writer 1、cold-reader 1。
- `actual_tasks: 11`，上限 12；skipped、failed、reused 均为空。三份 request 由一个批量 fact-checker dispatch 处理，任务计数闭合。

### 三份类型化 request

三份 required request 均满足 cognition-candidate 输出合同：

- request id、claim id、candidate id、anchor id 均非空并可区分；三个 request / claim 一一对应。
- 每份都有 `trigger_reason: candidate-necessary-evidence`，没有把候选存在时误写成 no-candidates。
- 每份都有 `allowed_external_source_boundary`：源内事实为 `[]`；两份外部事实均只授权 `fixture-primary-source`，与现有来源引用一致，未开放未声明搜索边界。
- kind、assertion_type、materiality 分别覆盖 source-internal/factual/material、external/factual/non-material、external/causal/material；所有可见事实都进入 request。

### 三条 check、coverage 与停止回交

- `fact_check_batch.request_ids` 与三份 required request id 集合精确相等。
- 三条 check id 非空且唯一；request/claim/candidate/anchor 身份完整，kind、assertion_type、materiality 与各自原 claim 逐项一致。
- 源内 check 回到登记原始 fixture 的 line 10；两条外部 check 均使用允许边界内的 high-trust 来源，并声明 `verified_this_run: true`。在本测试中只核对该结构声明，不把它当真实核实证据。
- 三条 check 均显式提供 `minimal_correction: ""`；supported 时空修正合法，不存在用缺字段掩盖修订要求。
- 三条 coverage 的 `request_claim_ids` 与 `checked_claim_ids` 精确相等，non-material claim 也被覆盖；`complete: true` 均成立。
- 批次顶层提供 `overall: pass`、`blocked_reason: ""`、`return_to: ""`。成功路径空回交合法；若 blocked，当前 fact-checker 合同要求通过这两个字段说明原因和退回对象，本 fixture 没有把阻塞伪装成 pass。

因此 request -> check -> per-request coverage -> overall 的输入、证据和停止回交 schema 闭合。

### Nested gates 与声明边界

- `source_provenance: pass` 并保存 source-map evidence。
- `conditional_fact_check: pass`，request_refs 精确列出三份 request，evidence 指向批次结果。
- 聚合 `source_and_fact: pass` 具备 owner、scope、evidence、conflicts；两个子门没有失败或阻塞。
- absolute value、regression、cold read、run integrity 均为 pass；cold-start/reproduction 明确 not-applicable；没有 pending、blocked、failed 或 awaiting acceptance。
- `can_claim` 只说合成 manifest 的结构可被运行完整性门接受；`cannot_claim` 明确排除真实 fresh、内容质量、用户体验和 ReaderLab 全部能力。

所以 actual 为 `accept-structure-only`。这里的 accepted 只接受自包含 fixture 的结构闭合；没有验证路径、来源、Agent 执行或用户回执的真实性。

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

当前 7 张 run-integrity 派生结构卡 7/7 与 Expected 匹配。RI-P01 新补的 `trigger_reason`、`allowed_external_source_boundary`、`minimal_correction`、`blocked_reason` 与 `return_to` 均符合当前角色合同；三份 request、三条 check、三条 coverage、11 个 dispatch 和 nested source/fact gates 完整闭合。六张负例继续被硬门拒绝。

本结果只能证明当前运行完整性正反例包通过本次静态派生结构复跑。`runtime-not-run`：没有发生真实 fresh/revision、事实核查、内容验收、用户体验验收、Phase 4 或 ReaderLab V3 整体运行。
