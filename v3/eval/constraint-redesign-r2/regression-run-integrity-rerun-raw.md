# Run Integrity 派生结构回归复跑：原始判断

## 执行边界

- evaluated_at_utc: `2026-07-10T11:15:02Z`
- evaluated_at_local: `2026-07-10T07:15:02-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_preserved: `true`
- previous_raw_used_as_evidence: `false`

这是同一会话中的回归复跑，不是盲审或真实运行。首次 raw 被保留，未读取、未修改、未作为本次 actual verdict 的证据。当前 case 文件自身包含上一轮 `independent_execution_result` 与 raw 路径；因为本次要求读取“当前 7 张 case”，这些元数据不可避免地可见，但本次判断按最新合同逐字段重新得出，不复制旧结果。

## 本次读取范围

- `v3/standards/regression-cases/run-integrity/RI-N01.md`
- `v3/standards/regression-cases/run-integrity/RI-N02.md`
- `v3/standards/regression-cases/run-integrity/RI-N03.md`
- `v3/standards/regression-cases/run-integrity/RI-N04.md`
- `v3/standards/regression-cases/run-integrity/RI-N05.md`
- `v3/standards/regression-cases/run-integrity/RI-N06.md`
- `v3/standards/regression-cases/run-integrity/RI-P01.md`
- `v3/skill/SKILL.md`
- `v3/skill/templates/run-manifest.md`
- `v3/standards/phase4-pilot-definition.md`
- `v3/skill/protocols/judge.md`

未读取首次 raw、完整 regression-suite、真实 run manifest、运行目录或历史成品；未修改 case、Skill、模板、Phase 4 闸门或 judge 协议。

## 判断口径

- `actual_verdict` 只判断给定合成场景在最新运行合同下应接受还是拒绝。
- `matches_expected` 比较本次 actual 与 case 当前 Expected。
- 负例只要命中一个硬拒绝条件即为 reject；附加 schema 缺口不会改变已成立的 reject。
- 正例必须满足当前完整结构合同；新增加的 route、dispatch 计数与状态转换约束同样适用，不能因为旧 Expected 是 accept 而忽略。
- 所有 case 都是 `derived-structure` 且 `runtime-not-run`。结构 accept 也不证明真实 run、内容质量或用户体验。

---

## RI-N01

- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- evidence_kind: `derived-structure`
- runtime_status: `runtime-not-run`

### 逐字段证据

- `mode: fresh`
- `reuse.base_generated_artifact: none`
- `reuse.reused_generated_artifacts` 非 `none`，列出旧 run 的 source map。
- 场景还声明 source-map 未重跑；即使该字段放在了与最新正式 schema 不同的 `reuse` 层级，其语义仍明确表示复用了旧生成产物。
- 输出目录字段表面满足隔离，但不能抵消生成产物复用。

### 主要理由

最新 Skill、run manifest Fresh 校验和 Phase 4 运行真实性均禁止把旧 source map、audit、候选或成品作为 fresh 输入。一个旧 source map 即足以拒绝。

### 可声称范围

只能声称该合成 fresh 结构应被拒绝且与 Expected 匹配；不能声称真实旧产物被读取或真实 fresh run 被拦截。

---

## RI-N02

- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- evidence_kind: `derived-structure`
- runtime_status: `runtime-not-run`

### 逐字段证据

- `mode: fresh`
- `output.preexisting: true`
- `output.writes_to_previous_run: true`
- case 使用的目录已存在，且明确会写入上一轮。

### 主要理由

fresh 必须使用本次唯一的新隔离目录。目录预存和写入旧 run 都是独立硬拒绝条件；Phase 4 也明确禁止覆盖、混写和就地修补旧输出。

### 可声称范围

只能声称给定合成输出字段不满足 fresh 隔离；不能声称真实文件系统已污染或任何旧输出实际被覆盖。

---

## RI-N03

- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- evidence_kind: `derived-structure`
- runtime_status: `runtime-not-run`

### 逐字段证据

- `mode: fresh`
- `fact_evidence.evidence_origin: previous-run-audit`
- `relocated_and_verified_this_run: false`
- `verification.source_and_fact: pass`
- `verification.run_integrity: pass`
- `status: accepted`

### 主要理由

最新合同仍只允许旧 URL 作为定位线索，要求本次重新定位核实。未在本次核实却把来源事实门和运行完整性门记为 pass，字段间直接矛盾，应 reject。

`fact_evidence` 按 case 声明仅是最小测试证据，不视为正式 manifest schema 扩展；拒绝依据是它揭示的证据来源与 pass 声明冲突。

### 可声称范围

只能声称该合成证据状态不能支持 pass；不能声称 URL 真假、事实真假或真实核查是否发生。

---

## RI-N04

- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- evidence_kind: `derived-structure`
- runtime_status: `runtime-not-run`

### 逐字段证据

- `mode: revision`
- `base_generated_artifact` 指向旧 reader page。
- 场景事实说明 assembly 直接读取该基线。
- `reused_generated_artifacts: none`
- `stages.reused_without_rerun: []`
- `stages.skipped: []`
- `claims.cannot_claim: []`
- `status: accepted`

### 主要理由

revision 允许复用明确基线，但最新 run manifest、Skill 和 Phase 4 都要求逐项披露复用生成物、实际重跑、未重跑链段和不可声称范围。场景事实与 manifest 披露不一致，且 accepted revision 没有保留完整流程不可声称范围，应 reject。

### 可声称范围

只能声称这张合成 revision manifest 的复用披露不闭合；不能声称真实 assembly 读取了何物或局部修订质量如何。

---

## RI-N05

- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- evidence_kind: `derived-structure`
- runtime_status: `runtime-not-run`

### 逐字段证据

- `sample.basis: proposed`
- 样本理由是执行者选择最短章节以降低任务量。
- `affects_capability_claim: true`
- `confirmation_required: true`
- `user_confirmation: pending`
- `status: running`
- `stages.executed` 已含 `source-read`

### 主要理由

最新状态转换进一步明确：必要样本确认仍 pending 时，只能 `planned -> awaiting-user`，不得产生执行 dispatch。该场景却进入 running 并执行 source-read，越过开跑前硬门，应 reject。

### 可声称范围

只能声称该合成状态转换非法；不能声称用户实际拒绝、真实章节更容易或 source-read 真实发生。

---

## RI-N06

- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- evidence_kind: `derived-structure`
- runtime_status: `runtime-not-run`

### 逐字段证据

- 实际执行只列 markdown 语法检查与资产卡冷启动。
- source-read、source-map、candidate-production、independent-content-judging、reader-page-assembly 明确 skipped。
- `verification.cold_start_or_reproduction: pass`
- `verification.run_integrity: pass`
- `claims.can_claim` 却写完整 fresh 流程通过。
- `claims.cannot_claim: []`
- `status: accepted`

### 主要理由

最新 manifest 仍限制 `can_claim` 为实际执行和对应独立门通过的交集；judge、Skill 和 Phase 4 均禁止用局部机器检查或单卡冷启动升级为完整 fresh。核心链段被跳过时，完整声明和 run_integrity pass 都应拒绝。

### 可声称范围

最多只能从合成字段看出语法检查与单卡冷启动被登记为执行；由于 runtime-not-run，连这两个局部检查也不能声称实际通过。

---

## RI-P01

- expected: `accept`
- actual_verdict: `reject`
- matches_expected: `no`
- evidence_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- conflict: `positive case no longer satisfies latest run-manifest contract`

### 保持成立的正向字段

- 声明 `mode: fresh`。
- 有原始路径、指纹和实际读取范围。
- 样本由权威 fixture 固定，`affects_capability_claim: false`、`confirmation_required: false`、`user_confirmation: not-required`。
- `base_generated_artifact: none`、`reused_generated_artifacts: none`、`stages.reused_without_rerun: []`。
- 输出目录标为新目录，且不写旧 run。
- `cannot_claim` 明确排除内容质量、用户体验和 ReaderLab 全部能力。

### 当前合同下的拒绝证据

1. **缺少 route。** 最新 manifest 要求 `route.line` 是本次唯一执行线路；`book | skill` child run 才可执行，mixed 父 run 必须拆分或 blocked。该 case 完全没有 `route`，却已经 `status: accepted`，无法证明执行线路在开跑前已合法确定。
2. **任务数字与 executed 列表不一致。** `budget.actual_tasks: 10`，但 `stages.executed` 只有 9 项。最新 manifest 明确 `actual_tasks` 等于实际计费的非复用、非跳过 dispatch 数，主控不得维护第二套数字。
3. **stages 未体现最新 dispatch 账本约束。** 最新 manifest 要求 stages 只记录 orchestrator dispatch id；case 列的是通用阶段名，且没有证据表明它们是可追踪 dispatch id。即使暂不单独据此拒绝，前两项已经足够。
4. **accepted 状态缺少完整适用门闭合说明。** 最新状态转换要求所有适用必需门 pass、不适用门明确 not-applicable、无 blocked/pending。case 把 `absolute_value`、`regression`、`cold_read` 留为 not-run，却没有说明这些门在该“accepted” run 中为何不适用。这个问题进一步削弱 accepted，但本次不需要依赖它即可 reject。

### 主要理由

RI-P01 是正例，必须满足当前完整结构合同。route 缺失和任务数字不一致都是最新 manifest 的明确硬约束；因此它不能继续作为合规 accepted fresh manifest，被独立复跑判为 reject。

### 与 Expected 的冲突

当前 Expected 仍是 accept，故 `matches_expected: no`。这不证明运行合同错误，只证明正向 case 尚未同步最新 route、dispatch 账本和 accepted 状态要求。

### 可声称范围

只能声称当前 RI-P01 合成 manifest 在最新结构合同下不再是合规正例。不能声称真实 fresh run 失败、内容质量失败、用户体验失败，或首次 raw 当时的判断不诚实；本次是合同更新后的复跑结果。

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
| RI-P01 | accept | reject | no | derived-structure | runtime-not-run |

- matched_cases: `6/7`
- mismatched_cases: `1/7`
- blocked_cases: `0/7`
- suite_structural_result: `fail`
- failing_case: `RI-P01`
- conflict_type: `positive fixture drifted behind latest manifest contract`

## 最终声称边界

本次只证明：六张负例仍按预期被当前合同拒绝；正向 RI-P01 因缺 route、任务数字不一致及 accepted 闭合不足而与 Expected 冲突，故这组派生结构回归当前为 fail。

本次不构成历史回放、真实 fresh/revision 运行、真实目录检查、内容质量验收、用户体验验收、Phase 4 通过或 ReaderLab V3 整体通过。按任务约束，本次只记录冲突，不修改 RI-P01、run manifest 或任何规则。
