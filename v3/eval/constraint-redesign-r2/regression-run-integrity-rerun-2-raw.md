# Run Integrity 派生结构回归复跑 2：原始判断

## 执行边界

- evaluated_at_utc: `2026-07-10T11:18:49Z`
- evaluated_at_local: `2026-07-10T07:18:49-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_files_preserved: `true`
- previous_raw_files_used_as_evidence: `false`

本次只按当前 7 张 run-integrity case 与最新运行合同独立复跑。已有 raw 保留，未读取、未修改、未作为本次 verdict 的证据。当前 case 文件自身的旧执行元数据可见，但 actual verdict 逐字段重新得出。

## 读取范围

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

未读取完整 regression-suite、真实 run manifest、运行目录、历史成品或已有 raw；未修改 case 或规则。

## 判定口径

- `reject`：合成结构命中当前运行完整性硬拒绝条件。
- `accept-structure-only`：合成字段之间满足当前结构合同，但没有任何真实运行证据，不能升级成 runtime accept。
- `matches_expected`：本次 actual 是否与当前 case Expected 一致。
- 所有 case 都是 `derived-structure / runtime-not-run`，不构成历史重放或真实执行。

---

## RI-N01

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据

- 场景声明 `mode: fresh`。
- `reused_generated_artifacts` 列出上一 run 的 source map，而 fresh 要求 `none`。
- 场景语义还表明 source-map 未重跑；即使字段层级不是最新正式 schema，也不能消除旧生成物复用事实。
- 新目录和不写旧 run 只能证明输出隔离，不能抵消输入复用。

### 判断

旧 source map 属于 fresh 明确禁止输入，一个字段即足以拒绝。实际 reject 与 Expected 匹配。

### 可声称范围

只能声称合成结构被拒绝；不能声称真实 fresh run 或旧 source map 读取发生过。

---

## RI-N02

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据

- `mode: fresh`。
- `output.preexisting: true`。
- `output.writes_to_previous_run: true`。
- 最新 manifest 和 Phase 4 均要求 fresh 使用本次唯一新目录，不覆盖、混写或回填旧 run。

### 判断

预存目录和写入旧 run 分别都是硬拒绝条件。实际 reject 与 Expected 匹配。

### 可声称范围

只能声称合成输出隔离字段非法；不能声称真实磁盘发生污染。

---

## RI-N03

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据

- 证据来自 `previous-run-audit`。
- `relocated_and_verified_this_run: false`。
- 却同时声明 `source_and_fact: pass`、`run_integrity: pass` 和 `status: accepted`。
- 当前合同只允许旧 URL 作为定位线索，本次必须重新定位核实。

### 判断

证据来源状态与 pass 声明直接矛盾，应 reject。`fact_evidence` 仅作为 case 的最小证据输入，不视为正式 schema 扩展。实际与 Expected 匹配。

### 可声称范围

只能声称给定字段不能支持结构 pass；不能声称 URL 或事实本身真假。

---

## RI-N04

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据

- 场景为 revision，明确以旧 reader page 为 baseline。
- 场景事实说明 assembly 读取该 baseline。
- 但 `reused_generated_artifacts: none`、`reused_without_rerun: []`、`skipped: []`、`cannot_claim: []`。
- 当前 Revision 校验要求逐项披露复用、实际重跑、未重跑与不可声称范围。

### 判断

revision 可复用，但不能隐瞒复用或完整流程不可声称范围。实际 reject 与 Expected 匹配。

### 可声称范围

只能声称合成 revision 披露不闭合；不能声称真实修订运行或质量结果。

---

## RI-N05

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据

- 样本会影响能力结论，且 `confirmation_required: true`。
- `user_confirmation: pending`。
- 状态却为 `running`，并已有 `source-read` 执行项。
- 最新状态转换要求 pending 时 `planned -> awaiting-user`，不得 dispatch。

### 判断

该场景越过样本确认硬门，应 reject。实际与 Expected 匹配。

### 可声称范围

只能声称合成状态转换非法；不能声称真实用户选择或真实 source-read 发生过。

---

## RI-N06

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 证据

- 只执行 markdown 语法检查和资产卡冷启动。
- source-read、source-map、候选、独立内容裁判和页面装配均 skipped。
- 却声明完整 fresh 流程通过、`run_integrity: pass`，且 `cannot_claim` 为空。
- 当前 manifest、Skill、Phase 4 和 judge 都禁止把机器检查、局部页或单卡冷启动升级为完整 fresh。

### 判断

声明范围大于实际执行与验收交集，应 reject。实际与 Expected 匹配。

### 可声称范围

只能声称该结构存在声明越界；由于 runtime-not-run，不能声称两个局部检查真实通过。

---

## RI-P01

- expected: `accept-structure-only`
- actual: `accept-structure-only`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 结构接受证据

- 运行模式预先声明为 `fresh`。
- route 已闭合：`line: book`、`mixed_handling: not-applicable`、无 child run。
- source 为 book，原始路径、指纹和实际读取范围齐全。
- 样本组合合法：`confirmation_required: false` 与 `user_confirmation: not-required` 配对；权威 fixture 固定全章，不需等待确认。
- 生成物零复用：base 与 reused generated 均为 `none`，`reused_without_rerun: []`。
- 输出为新隔离目录：`preexisting: false`、`writes_to_previous_run: false`。
- `actual_tasks: 9` 与 `stages.executed` 的 9 个合成 dispatch 记录一致；无 skipped、failed 或 reused dispatch，且未超 task_limit 12。
- 声明明确限制为“该合成 manifest 的 fresh 结构约束可被接受”，并直接写明 `runtime-not-run`。
- `cannot_claim` 明确排除真实 fresh run、内容质量、用户体验和 ReaderLab 全部能力。
- status 保持 `running`，没有伪装成满足所有最终门的 `accepted` run；内容、回归和冷读门仍为 `not-run`。

### 为什么只能结构接受

本 case 是合成 manifest，不存在可现场核验的真实原始文件、输出目录、dispatch 证据、事实证据、成品或验收回执。内嵌的 `run_integrity: pass` 只是被测试的合成字段，不是本次观察到的运行证据。

因此，本次只能确认字段组合没有触发 current contract 的结构拒绝条件；不能把 `accept-structure-only` 改写成“fresh 运行完整性真实通过”。`status: running` 和多个质量门 `not-run` 也明确阻止完整 accepted 声明。

### 关于任务数

当前限定证据只要求 `actual_tasks` 与本 case 的实际 dispatch 账本一致；两者均为 9。case 没有声明自己是标准 11 任务章级运行，且本次不读取角色实例索引来另行推定运行档位，因此不因标准档位外部假设拒绝这个最小结构正例。

### 判断

actual 为 `accept-structure-only`，与 Expected 匹配；runtime 仍明确为 `runtime-not-run`。

### 可声称范围

只能声称修正后的合成结构在当前合同下可接受。不能声称真实 fresh run 发生或通过、内容质量通过、用户体验通过、Phase 4 通过或 ReaderLab 全能力通过。

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

## 总结论与声称边界

当前 7 张 run-integrity 派生结构 case 全部与 Expected 匹配：六张负例继续被拒绝，修正后的 RI-P01 仅获得 `accept-structure-only`。总 verdict 为 `pass-derived-structure-only`。

这不构成真实运行、历史回放、内容质量验收、用户体验验收、Phase 4 通过或 ReaderLab V3 整体通过。所有 runtime 声明均为 `runtime-not-run`；本次未改任何 case 或规则。
