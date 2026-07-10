# Run Integrity 派生结构回归复跑 9：统一 Gate 对象

## 执行边界

- evaluated_at_utc: `2026-07-10T16:01:56Z`
- evaluated_at_local: `2026-07-10T12:01:56-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_files_preserved: `true`
- previous_raw_files_used_as_evidence: `false`

本次按当前 run manifest 与 orchestrator 的统一 verification schema，重新读取并判定当前 7 张 run-integrity case。重点检查所有适用 gate 的 `status / owner / scope / evidence / conflicts`，并复核 RI-P01 的 11 个 dispatch、fact fixture 与 nested source/fact gate。旧 raw 未作为 verdict 证据；未修改规则或 case。

`accept-structure-only` 只表示合成 fixture 可表达当前合同；所有 case 都是 `derived-structure / runtime-not-run`，不构成历史回放或真实运行。

---

## RI-N01

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

fresh 显式复用旧 source map，并列入 `reused_without_rerun`。Fresh 的生成产物零复用硬门已被命中；无需靠后续 gate 补救，拒绝成立。

## RI-N02

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

fresh 输出目录已存在且写入上一 run，违反唯一隔离目录与不得覆盖、混写、回填旧 run，拒绝成立。

## RI-N03

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

旧 URL 来自 previous-run audit，且 `relocated_and_verified_this_run: false`。虽然 `source_and_fact` 与 `run_integrity` 现在都使用合法 gate 对象形状：

- `source_and_fact` 有 status、owner、scope、evidence、conflicts 及两个嵌套子门；
- `run_integrity` 有 status、owner、scope、evidence、conflicts；

但对象齐全不能替代证据真实性。条件事实与聚合 evidence 仍指向旧 audit，不能在 fresh 中记 pass；其 `run_integrity: pass` 与 accepted 也随之不成立，故拒绝。

## RI-N04

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

revision 实际读取旧 reader page，却没有列出复用生成物、未重跑链段或不可声称范围。披露链缺失，拒绝成立。

## RI-N05

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

样本影响能力结论且确认仍为 pending，场景却进入 running 并执行 source-read。当前状态机要求 awaiting-user 且不得 dispatch，拒绝成立。

## RI-N06

- expected: `reject`
- actual: `reject`
- match: `yes`
- runtime: `runtime-not-run`

`cold_start_or_reproduction` 与 `run_integrity` 均已改为含 status、owner、scope、evidence、conflicts 的统一对象；`user_experience` 也有 status、owner、scope、evidence。schema 形状现在合法，但场景仍只执行语法检查与资产卡冷启动，核心 fresh 链段被跳过，却声称完整 fresh 流程通过。声明超出执行与验收交集，且 run_integrity 不应为 pass，故拒绝。

## RI-P01

- expected: `accept-structure-only`
- actual: `accept-structure-only`
- match: `yes`
- runtime: `runtime-not-run`

### Fresh 前置与 11 个 dispatch

- route 为 book；原始路径、指纹和实际读取范围齐全。
- 样本组合 `false + not-required` 合法；生成产物零复用；输出声明为全新隔离目录，不写旧 run。
- executed 包含 11 个唯一实例级 dispatch：source-map 1、nominator 2、merger 1、candidate 3、fact-checker 1、judge 1、writer 1、cold-reader 1。
- `actual_tasks: 11`，上限 12；skipped、failed、reused 均为空。一个 fact-checker 批量处理三份 request，计数与固定标准链闭合。

### Fact fixture 与 nested source/fact

- 三份 required request 均有非空唯一 request/claim id、candidate/anchor 身份、`trigger_reason`、kind、assertion_type、materiality 和可见性；源内 request 的外部授权边界为空，两份外部 request 只授权 fixture-primary-source。
- 三条 check id 非空唯一，与 request/claim/candidate/anchor 精确对应；kind、assertion_type、materiality 逐项同形。源内 check 回到登记 fixture，外部 check 均声明 high trust 且本次核实；三条均有 `minimal_correction`。
- 三条 coverage 的 request claims 与 checked claims 精确相等，non-material claim 也被覆盖；batch overall 为 pass，并有 blocked_reason 与 return_to。
- `source_and_fact` 是完整聚合对象：status=pass、owner=orchestrator、scope/evidence/conflicts 均存在；source_provenance 与 conditional_fact_check 各保存 owner 和 evidence，后者 request_refs 精确列三份输入。

request -> check -> per-request coverage -> batch overall -> conditional child gate -> aggregate gate 的结构闭合。

### 统一 Gate 对象

逐项核对当前 manifest / orchestrator 同形 schema：

| gate | status | owner | scope | evidence | conflicts |
|---|---|---|---|---|---|
| source_and_fact | pass | orchestrator | fixture-chapter | fixture-source-map | [] |
| absolute_value | pass | cognition-judge | fixture-candidates | fixture-absolute-verdict | [] |
| regression | pass | regression-runner | fixture-regression-cases | fixture-regression-result | [] |
| cold_read | pass | cold-reader | fixture-reader-page | fixture-cold-read | [] |
| cold_start_or_reproduction | not-applicable | orchestrator | [] | [] | [] |
| run_integrity | pass | run-integrity-reviewer | fixture-ri-p01 | fixture-manifest-review | [] |

`user_experience` 按自己的 schema 为 `{status: not-requested, owner: user, scope: [], evidence: []}`；该对象不定义 conflicts，和 manifest / orchestrator 一致。所有 gate 均不再使用旧标量形状，没有缺 owner、scope、evidence 或适用的 conflicts。

### 声明范围

`can_claim` 只覆盖合成 manifest 的结构接受；`cannot_claim` 明确排除真实 fresh、内容质量、用户体验和 ReaderLab 全部能力。没有 blocked、pending、failed、超预算或 awaiting acceptance。

因此 actual 为 `accept-structure-only`。fixture 内的 pass/evidence 只供 schema 自洽检查；本次没有验证这些引用背后的真实文件、Agent 执行或用户回执。

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

当前 7 张 run-integrity 派生结构卡 7/7 与 Expected 匹配，0 blocker。统一 gate 对象没有削弱六张负例：旧证据、旧输出、隐瞒复用、越过样本确认和扩大声明仍分别被拒绝。RI-P01 的适用 gate 均具有当前合同要求的 status、owner、scope、evidence、conflicts；三份 request/check/coverage、11 个 dispatch 与 nested source/fact gate 闭合，因此只获得 structure-only 接受。

`runtime-not-run`：没有发生真实 fresh/revision、事实核查、内容或用户体验验收、Phase 4 或 ReaderLab V3 整体运行。
