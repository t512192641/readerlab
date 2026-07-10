# Run Integrity 派生结构回归复跑 3：原始判断

## 执行边界

- evaluated_at_utc: `2026-07-10T11:29:29Z`
- evaluated_at_local: `2026-07-10T07:29:29-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_files_preserved: `true`
- previous_raw_files_used_as_evidence: `false`

本次只读取当前 7 张 run-integrity case 与最新 `SKILL.md`、run manifest、Phase 4 闸门和 judge 协议。已有 raw 保留，未读取、未修改、未作为 verdict 证据；未修改 case 或规则。

判定口径：

- `reject`：合成场景命中当前运行完整性硬拒绝条件。
- `accept-structure-only`：合成 manifest 的字段、状态、dispatch、门和声明范围在当前合同下闭合；不表示任何真实字段值被现场核验。
- 所有 case 都是 `derived-structure / runtime-not-run`，不构成历史重放、真实 fresh/revision、内容验收或用户体验。

---

## RI-N01

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

场景声明 fresh，却把上一 run 的 source map 列为 `reused_generated_artifacts`，并表示 source-map 未重跑。当前 Fresh 校验要求生成产物零复用；输出目录即使隔离，也不能抵消输入复用。一个硬门已足以 reject。

### 可声称范围

只证明该合成结构应拒绝；不证明真实旧产物被读取或真实 fresh run 被拦截。

---

## RI-N02

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

场景为 fresh，但 `output.preexisting: true` 且 `writes_to_previous_run: true`。当前合同要求唯一新隔离目录，并禁止覆盖、混写或回填上一轮；任一项即 reject。

### 可声称范围

只证明合成隔离字段非法；不证明真实文件系统被污染。

---

## RI-N03

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

证据来自 previous-run audit，`relocated_and_verified_this_run: false`，却把来源事实门、运行完整性门和 accepted 状态写成通过。旧 URL 只能作定位线索，本次必须重新核实；证据来源状态与 pass 声明矛盾，应 reject。

### 可声称范围

只证明该字段组合不能支持 pass；不判断 URL 或事实本身真假。

---

## RI-N04

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

revision 明确以旧 reader page 为 baseline，且场景事实说明 assembly 读取它；manifest 却写 `reused_generated_artifacts: none`、未重跑/跳过为空、`cannot_claim` 为空。Revision 必须逐项披露复用、实际重跑、未重跑与不可声称范围，故 reject。

### 可声称范围

只证明合成 revision 披露不闭合；不证明真实 revision 发生或质量失败。

---

## RI-N05

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

样本会影响能力结论，`confirmation_required: true` 且 `user_confirmation: pending`；状态却为 running 并已有 source-read。当前状态机要求 pending 进入 awaiting-user 且不得 dispatch，因此 reject。

### 可声称范围

只证明合成状态转换非法；不证明用户真实选择或 source-read 真实执行。

---

## RI-N06

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

实际只列语法检查和资产卡冷启动，source、source map、候选、独立裁判和页面装配均 skipped，却声明完整 fresh 流程和 run_integrity 通过，且没有 cannot_claim。声明范围超过“实际执行 + 对应独立门”交集，故 reject。

### 可声称范围

只证明合成声明越界；由于 runtime-not-run，不能声称两个局部检查真实通过。

---

## RI-P01

- expected: `accept-structure-only`
- actual: `accept-structure-only`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 1. Fresh 前置结构

- `mode: fresh` 在 manifest 中先声明。
- route 为 `book`，mixed handling 为 not-applicable，无 child run。
- source 是固定全章 book，有原始路径、指纹与实际读取范围。
- 样本确认组合合法：`confirmation_required: false + user_confirmation: not-required`。
- base/reused generated artifacts 均为 none，`reused_without_rerun: []`。
- 输出目录标为新目录，`preexisting: false`、`writes_to_previous_run: false`。

结论：fresh 的来源、样本、零复用和隔离前置条件结构闭合。

### 2. 11 个唯一实例级 dispatch

`stages.executed` 正好列 11 个互不重复的 dispatch id：

1. `book-source-map-1`
2. `book-anchor-nominator-1`
3. `book-anchor-nominator-2`
4. `book-anchor-merger-1`
5. `book-cognition-candidate-1`
6. `book-cognition-candidate-2`
7. `book-cognition-candidate-3`
8. `book-fact-checker-1`
9. `book-cognition-judge-1`
10. `book-writer-1`
11. `book-cold-reader-1`

这些 id 分别表达图书标准链的 source map 1、提名 2、归并 1、候选 3、事实 1、裁判 1、成文 1、冷读 1；盲区检查并入 cognition judge，没有另加任务。没有 aggregated `anchor-identification` 或 `candidate-production` 代替独立实例。

`budget.actual_tasks: 11` 与 executed 的 11 个非复用、非跳过 dispatch 数一致；task_limit 为 12，未超预算。skipped、failed、reused 均为空。

结论：最新的 instance-level dispatch 与成本阻塞已关闭。

### 3. accepted 的适用门闭合

- `source_and_fact: pass`
- `absolute_value: pass`
- `regression: pass`
- `cold_read: pass`
- `cold_start_or_reproduction: not-applicable`
- `run_integrity: pass`
- `user_experience: not-requested`
- 无 blocked、pending、failed 或 awaiting user acceptance。

对这个合成 book manifest，技术必需门均为 pass；Skill 冷启动/复现明确不适用；用户体验不在该结构 fixture 的请求范围内。任务未超预算，can_claim 只覆盖结构接受，cannot_claim 明确排除真实 run、内容质量、用户体验和全部能力。

因此 `status: accepted` 在合成字段之间可闭合，不再存在上一版 running / not-run 门或任务账本不完整的问题。

### 4. 为什么仍只能 accept-structure-only

这是一张 derived-structure fixture。路径、指纹、目录、11 个 dispatch、各门 pass 和 accepted 都是供结构判断的合成输入，本次没有现场读取 `/fixtures/source/chapter-01.md`、检查输出目录、执行 dispatch、核实事实、运行回归、冷读成品或取得用户回执。

因此可以接受“这种合规结构可表达”，不能接受“这些合成字段在真实运行中已经成立”。case 的 can_claim 和 cannot_claim 已明确这一边界。

`actual: accept-structure-only` 不等于 `runtime pass`；runtime 继续是 `runtime-not-run`。

### 可声称范围

只可声称修正后的 RI-P01 在当前合同下是结构正例。不可声称真实 fresh run 发生或通过、内容质量通过、用户体验通过、Phase 4 通过或 ReaderLab 全能力通过。

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
- negative_cases_preserved: `6/6`
- positive_structure_case_preserved: `1/1`
- suite_verdict: `pass-derived-structure-only`
- runtime_verdict: `not-run`

## 总结论

当前 7 张 run-integrity 派生结构 case 全部与 Expected 匹配。RI-N01—RI-N06 继续 reject；修正后的 RI-P01 已具备 11 个唯一实例级 dispatch、`actual_tasks: 11` 和 accepted 所需的适用门闭合，因此 actual 为 `accept-structure-only`。

整组 verdict 为 `pass-derived-structure-only`，runtime 为 `not-run`。本结果不构成历史回放、真实运行、内容质量、用户体验、Phase 4 或 ReaderLab V3 整体通过。
