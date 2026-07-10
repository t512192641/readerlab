# Run Integrity 派生结构回归复跑 5：完整嵌套来源 / 事实门

## 执行边界

- evaluated_at_utc: `2026-07-10T11:41:11Z`
- evaluated_at_local: `2026-07-10T07:41:11-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_files_preserved: `true`
- previous_raw_files_used_as_evidence: `false`

本次只读取当前 7 张 run-integrity case 与最新 `SKILL.md`、run manifest、Phase 4 闸门、judge 协议。旧 raw 保留，未读取、未修改、未作为本次证据；未修改 case 或规则。

判定口径：`reject` 表示合成场景命中当前硬门；`accept-structure-only` 只表示合成字段在当前 schema 下闭合。全部 case 均为 `derived-structure / runtime-not-run`。

---

## RI-N01

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

fresh 复用了上一 run 的 source map，并表示 source-map 未重跑。Fresh 要求生成物零复用；输出隔离不能抵消输入复用，故 reject。

可声称范围：只证明合成结构应拒绝，不证明真实旧产物被读取。

---

## RI-N02

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

fresh 输出目录已存在且会写入上一 run，违反唯一新隔离目录和不得覆盖/混写/回填的硬门，故 reject。

可声称范围：只证明合成隔离字段非法，不证明真实磁盘污染。

---

## RI-N03

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 完整嵌套门证据

`source_and_fact` 当前字段齐全：

- aggregate `status: pass`
- `owner: orchestrator`
- source provenance pass，owner 为 source-map
- conditional fact check pass，owner 为 fact-checker，request_ref 非空
- `scope: [fixture-claim]`
- 顶层与子门 evidence 均指向 `previous-run-audit`
- `conflicts: []`

但 case 的事实状态同时明确：

- `evidence_origin: previous-run-audit`
- `relocated_and_verified_this_run: false`

owner、scope、evidence、conflicts 和 request_ref 的齐全只证明记录结构完整，不能把旧 audit 变成本次核实证据。Fresh 要求旧 URL 只作线索，触发的条件事实门必须覆盖 request 中全部可见事实并在本次重新定位核实。

因此 conditional fact check 不得 pass，aggregate source_and_fact 不得 pass，run_integrity 和 accepted 也不成立。actual reject 与 Expected 匹配。

可声称范围：只证明完整嵌套 schema 仍会拒绝“旧 audit 未本次核实”；不判断事实真假，也不证明真实核查运行过。

---

## RI-N04

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

revision 实际读取旧 reader page baseline，却把复用生成物、未重跑、跳过和 cannot_claim 全部留空。Revision 披露不闭合，故 reject。

可声称范围：只证明合成 revision 非法，不证明真实 revision 或质量结果。

---

## RI-N05

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

样本影响能力结论，确认必需且 pending；场景却进入 running 并执行 source-read。当前状态机要求 awaiting-user 且不得 dispatch，故 reject。

可声称范围：只证明合成状态转换非法，不证明真实用户选择或执行发生。

---

## RI-N06

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

只登记语法检查和资产卡冷启动，核心 fresh 链段均 skipped，却声明完整 fresh 和 run_integrity 通过，且 cannot_claim 为空。声明超出实际执行与对应独立门交集，故 reject。

可声称范围：只证明合成声明越界，不证明局部检查真实通过。

---

## RI-P01

- expected: `accept-structure-only`
- actual: `accept-structure-only`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### Fresh、route、样本和隔离

- mode 先声明为 fresh；route 为 book。
- 原始路径、指纹、实际读取范围齐全。
- 样本确认组合为 `false + not-required`，合法。
- base/reused generated artifacts 为 none，未重跑复用为空。
- 输出为新目录，不写旧 run。

以上结构闭合。

### 11 个唯一实例级 dispatch

executed 正好包含：source-map 1、anchor-nominator 2、anchor-merger 1、cognition-candidate 3、fact-checker 1、cognition-judge 1、writer 1、cold-reader 1，共 11 个互不重复实例 id。

- `actual_tasks: 11`
- `task_limit: 12`
- skipped / failed / reused 均为空

任务计数与 dispatch 账本一致且未超预算；盲区检查并入 cognition judge，不另计任务。

### 完整嵌套 source_and_fact

```yaml
source_and_fact:
  status: pass
  owner: orchestrator
  source_provenance:
    status: pass
    owner: source-map
    evidence: [fixture-source-map]
  conditional_fact_check:
    status: not-applicable
    owner: orchestrator
    request_ref: none
    evidence: []
  scope: [fixture-chapter]
  evidence: [fixture-source-map]
  conflicts: []
```

判断：

- aggregate owner 已明确为 orchestrator。
- scope 明确限定 fixture chapter。
- 来源证明子门有 owner 和证据，状态为 pass。
- 场景没有外部事实 request；条件子门用 not-applicable、request_ref none、空 evidence 表达未触发，没有用空证据伪造 pass。
- aggregate evidence 指向 source map，conflicts 为空。
- 来源证明 pass 且条件事实门 not-applicable，aggregate pass 与当前确定性聚合规则一致。

标准 fact-checker dispatch 的存在不等于条件外部事实门一定被触发；本场景没有 request claims，因此 not-applicable 与 11 任务账本不冲突。

### accepted 与声明范围

- source_and_fact: pass
- absolute_value: pass
- regression: pass
- cold_read: pass
- cold_start_or_reproduction: not-applicable
- run_integrity: pass
- user_experience: not-requested
- awaiting_user_acceptance: []
- 无 blocked、pending、failed 或超预算

所有适用技术门均闭合。can_claim 只覆盖合成结构接受；cannot_claim 明确排除真实 fresh、内容质量、用户体验和全部能力。accepted 在合成字段之间成立。

### 为什么仍只能 structure-only

路径、指纹、目录、dispatch、source map evidence 和门状态都是 fixture 输入。本次没有现场读取 source、检查目录、执行 11 个任务、运行任何验证门或取得用户回执。

所以只能接受“结构可表达且自洽”，不能接受“真实运行已通过”。`accept-structure-only` 不等于 runtime pass；runtime 继续为 `runtime-not-run`。

可声称范围：只可声称 RI-P01 是当前完整 nested manifest schema 下的结构正例；不可声称真实 fresh、内容质量、用户体验、Phase 4 或 ReaderLab 全能力通过。

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

当前 7 张 run-integrity 派生结构卡 7/7 与 Expected 匹配。完整 source_and_fact 顶层 owner/scope/evidence/conflicts 没有放松证据门：RI-N03 仍因旧 audit 未本次核实而 reject；RI-P01 的完整嵌套来源/条件事实门、11 dispatch、accepted 和声明范围闭合，只获得 structure-only 接受。

总 verdict 为 `pass-derived-structure-only`，runtime 为 `not-run`。本结果不构成历史回放、真实运行、内容质量、用户体验、Phase 4 或 ReaderLab V3 整体通过。
