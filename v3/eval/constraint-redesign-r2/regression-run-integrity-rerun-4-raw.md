# Run Integrity 派生结构回归复跑 4：嵌套来源 / 事实门

## 执行边界

- evaluated_at_utc: `2026-07-10T11:38:01Z`
- evaluated_at_local: `2026-07-10T07:38:01-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_files_preserved: `true`
- previous_raw_files_used_as_evidence: `false`

本次只读取当前 7 张 run-integrity case、最新 `SKILL.md`、run manifest、Phase 4 闸门和 judge 协议。已有 raw 保留，未读取、未修改、未作为 verdict 证据；未修改 case 或规则。

判定口径：

- `reject`：合成场景命中当前运行完整性硬拒绝条件。
- `accept-structure-only`：合成 manifest 的 route、来源、样本、复用、隔离、dispatch、嵌套门、状态和声明范围彼此闭合，但不证明任何真实运行。
- 全部 case 均为 `derived-structure / runtime-not-run`。

---

## RI-N01

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

fresh 场景复用了上一 run 的 source map，并表示 source-map 未重跑。当前 Fresh 校验要求 `reused_generated_artifacts: none` 且 `reused_without_rerun: []`；一个旧生成物即足以 reject。嵌套 source_and_fact schema 不改变该输入复用硬门。

### 可声称范围

只证明合成结构应拒绝；不证明真实旧产物被读取。

---

## RI-N02

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

fresh 输出 `preexisting: true` 且 `writes_to_previous_run: true`，违反唯一新隔离目录和不得覆盖、混写、回填上一轮的硬门，应 reject。

### 可声称范围

只证明合成隔离字段非法；不证明真实磁盘污染。

---

## RI-N03

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 嵌套门证据

场景把 `verification.source_and_fact` 写为：

- aggregate `status: pass`
- `source_provenance.status: pass`
- `conditional_fact_check.status: pass`
- 条件事实核查有 `request_ref: fixture-request`
- 其唯一 evidence 却是 `previous-run-audit`

同时，case 的事实证据明确：

- `evidence_origin: previous-run-audit`
- `relocated_and_verified_this_run: false`

### 判断

嵌套结构本身没有让旧 audit 合法化。当前 Fresh 规则只允许旧 URL 作定位线索；条件事实门被触发后，必须在本次重新定位核实并用本次证据覆盖 request claims。`request_ref` 存在只证明请求被引用，不能证明 evidence 是本次核实结果。

因此 `conditional_fact_check: pass` 不成立，聚合 `source_and_fact.status` 也不得 pass；`run_integrity: pass` 与 `status: accepted` 随之不成立。actual 为 reject，与 Expected 匹配。

### 可声称范围

只证明“旧 audit 未在本次核实”仍会被嵌套门拒绝；不判断 URL 或事实本身真假，也不证明真实核查运行过。

---

## RI-N04

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

revision 明确以旧 reader page 为 baseline，场景事实说明 assembly 读取它；manifest 却把复用生成物、未重跑阶段、跳过阶段和 cannot_claim 全部留空。Revision 必须逐项披露复用、实际重跑、未重跑和不可声称范围，故 reject。

### 可声称范围

只证明合成 revision 披露不闭合；不证明真实 revision 或质量结果。

---

## RI-N05

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

样本影响能力结论，确认必需且仍 pending；场景却进入 running 并执行 source-read。当前状态机要求 pending 进入 awaiting-user 且不得 dispatch，因此 reject。

### 可声称范围

只证明合成状态转换非法；不证明用户真实选择或执行发生。

---

## RI-N06

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据与理由

只登记语法检查和资产卡冷启动，source、source map、候选、独立裁判和页面装配均 skipped，却声明完整 fresh 与 run_integrity 通过，且 cannot_claim 为空。声明超出“实际执行 + 对应独立门”交集，应 reject。

### 可声称范围

只证明合成声明越界；不证明两个局部检查真实通过。

---

## RI-P01

- expected: `accept-structure-only`
- actual: `accept-structure-only`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 1. Fresh、route 与样本

- mode 先声明为 fresh。
- route 为 book，mixed handling 不适用，无 child run。
- 原始路径、指纹和实际读取范围齐全。
- 固定全章样本不影响能力声明，确认组合为 `false + not-required`，合法。
- base / reused generated artifacts 均为 none，未重跑复用为空。
- 输出目录标为新目录，未预存且不写旧 run。

结论：fresh 前置结构闭合。

### 2. 11 个实例级 dispatch 与计数

executed 恰有 11 个互不重复的实例 id：source-map 1、anchor-nominator 2、anchor-merger 1、cognition-candidate 3、fact-checker 1、cognition-judge 1、writer 1、cold-reader 1。

- `actual_tasks: 11`
- `task_limit: 12`
- skipped / failed / reused 均为空

实际计费任务数与 executed dispatch 数一致，未超预算；盲区检查并入 cognition judge，没有另计任务。

结论：instance-level dispatch 和预算闭合。

### 3. 嵌套 source_and_fact

当前正例写为：

```yaml
source_and_fact:
  status: pass
  source_provenance:
    status: pass
    owner: source-map
    evidence: [fixture-source-map]
  conditional_fact_check:
    status: not-applicable
    owner: orchestrator
    request_ref: none
    evidence: []
```

判断：

- 来源证明子门为 pass，有 owner 与 evidence。
- 本合成场景没有声明需核实的外部事实 request，因此条件事实子门明确 not-applicable；`request_ref: none`、evidence 为空与未触发状态一致。
- 聚合门只有在来源证明 pass，且条件事实门 pass 或 not-applicable 时才能 pass；本例满足。
- 11 任务账本中保留标准 fact-checker 实例不改变条件子门的适用性判断：在本限定结构中没有 request claims，条件门没有伪造 pass，也没有拿空 evidence 充当核查成功。

结论：嵌套来源 / 条件事实子门与 aggregate pass 结构闭合。

### 4. accepted 的适用门

- source_and_fact aggregate: pass
- absolute_value: pass
- regression: pass
- cold_read: pass
- cold_start_or_reproduction: not-applicable
- run_integrity: pass
- user_experience: not-requested
- awaiting_user_acceptance: []
- 无 blocked、pending、failed 或超预算

can_claim 只写合成 fresh 结构可接受；cannot_claim 明确排除真实 fresh、内容质量、用户体验和全部能力。对于此结构 fixture，accepted 的适用门和声明范围闭合。

### 5. 为什么仍是 structure-only / runtime-not-run

所有路径、指纹、目录、dispatch、source map evidence 与门状态都是合成输入。本次没有现场读取 fixture source、验证目录、执行 11 个任务、检查 source map、运行事实/价值/回归/冷读门或取得用户回执。

因此只能接受“这种结构可表达并自洽”，不能接受“这些门在真实运行中已通过”。`accept-structure-only` 不等于 runtime pass；runtime 继续是 `runtime-not-run`。

### 可声称范围

只可声称 RI-P01 是当前 nested manifest schema 下的结构正例。不可声称真实 fresh run、内容质量、用户体验、Phase 4 或 ReaderLab 全能力通过。

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

当前 7 张 run-integrity 派生结构 case 全部与 Expected 匹配。嵌套 source_and_fact schema 没有放松旧证据边界：RI-N03 仍因旧 audit 未在本次重新核实而 reject；RI-P01 的来源证明 pass、条件事实 not-applicable、11 个实例级 dispatch、accepted 门和声明范围闭合，因此仅结构接受。

整组 verdict 为 `pass-derived-structure-only`，runtime 为 `not-run`。本结果不构成历史回放、真实运行、内容质量、用户体验、Phase 4 或 ReaderLab V3 整体通过。
