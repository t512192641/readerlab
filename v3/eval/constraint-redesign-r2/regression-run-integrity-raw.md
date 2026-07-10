# Run Integrity 派生结构回归：独立原始判断

## 执行边界

- context: `no-history-context`
- evaluated_at_utc: `2026-07-10T10:53:02Z`
- evaluated_at_local: `2026-07-10T06:53:02-04:00`
- runtime_status: `runtime-not-run`
- test_kind: `derived-structure`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- independent_scope: 只依据本次明确给出的合成 manifest / 场景事实与当前运行合同，判断结构上应接受还是拒绝。
- exclusion: 未读取 `v3/standards/regression-suite.md`、旧回归结果、旧原始输出、真实运行目录或任何历史成品；未修改 case、Skill、协议、模板或标准。

## 读取范围

仅读取以下文件：

- `AGENTS.md`
- `v3/current-task.md`
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

## 判断口径

- `actual_verdict` 只回答：给定合成结构是否满足当前运行完整性合同。
- `matches_expected` 只回答：独立结构判断是否与 case 的冻结 Expected 一致。
- 所有判断均为 `derived-structure`；即使 verdict 为 `accept`，也不证明真实 run 曾发生、真实字段值已被现场核验、内容质量通过或用户体验通过。
- 结构拒绝采用硬门逻辑：任一 fresh 复用、输出污染、必要样本确认缺失、revision 披露缺失或声明越界，都足以拒绝运行完整性。

---

## RI-N01

- kind: `derived-structure`
- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- runtime_status: `runtime-not-run`

### 结构依据

- 场景声明 `mode: fresh`。
- `reused_generated_artifacts` 列出旧 run 的 `/previous-run/audit/source-map.yaml`。
- 场景还声明 `reused_without_rerun: [source-map]`；而正式 manifest 中该字段属于 `stages`，不是 `reuse`。无论按场景语义还是按正式 schema 校验，它都不能成为合法 fresh。
- `v3/skill/SKILL.md`、run manifest 的 Fresh 校验与 Phase 4 运行真实性均要求 fresh 不得把旧 source map 等生成产物作为输入，且 `reused_generated_artifacts: none`、`stages.reused_without_rerun: []`。

### 主要理由

fresh 的核心承诺是从登记原始来源重新执行声明链段。复用旧 source map 已直接破坏零生成产物复用硬门；字段放错层级不能消除这一事实。

### 可声称范围

只能声称：该合成结构被当前 fresh 合同拒绝，且实际判断与 Expected 一致。不能声称：真实 fresh run 被拦截、真实旧产物被发现，或任何内容门已经执行。

---

## RI-N02

- kind: `derived-structure`
- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- runtime_status: `runtime-not-run`

### 结构依据

- 场景声明 `mode: fresh`，但 `output.preexisting: true`。
- 同时声明 `output.writes_to_previous_run: true`。
- run manifest 要求 fresh 的 `new_isolated_directory` 是本次唯一新目录；Phase 4 明确禁止覆盖、混写或回填上一轮。

### 主要理由

目录已经存在和写入旧 run 分别都是独立拒绝条件；两项同时出现，无法形成 fresh 所需的 run 级隔离。

### 可声称范围

只能声称：该合成输出结构不满足 fresh 隔离要求。不能声称：磁盘上的真实目录已被检查、真实旧输出曾被覆盖，或污染已经实际发生。

---

## RI-N03

- kind: `derived-structure`
- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- runtime_status: `runtime-not-run`

### 结构依据

- 场景把事实证据标为 `evidence_origin: previous-run-audit`。
- `relocated_and_verified_this_run: false`，但同时把 `verification.source_and_fact` 与 `verification.run_integrity` 写成 `pass`，且状态为 `accepted`。
- run manifest Fresh 校验、Skill 的 Fresh run 与 Phase 4 运行真实性都只允许旧 URL 作为定位线索，外部事实必须在本次重新定位核实。
- case 已明确 `fact_evidence` 是最小测试输入，不是正式 manifest schema 扩展；本判断只使用它揭示的证据来源事实。

### 主要理由

“保留旧 URL 作为搜索线索”和“本次已经核实该事实”是两种不同状态。未在本次重新定位核实，却把来源事实门和运行完整性门记为通过，属于证据状态与验证声明直接矛盾。

### 可声称范围

只能声称：给定证据来源字段时，`pass` 声明在结构上不成立。不能声称：该 URL 是否真实有效、外部事实本身真假如何，或真实核查曾经失败。

---

## RI-N04

- kind: `derived-structure`
- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- runtime_status: `runtime-not-run`

### 结构依据

- 场景声明 `mode: revision`，并给出 `base_generated_artifact: /previous-run/reader-page.md`。
- 场景事实说明 `assembly` 直接读取该基线，但 manifest 同时写 `reused_generated_artifacts: none`、`stages.reused_without_rerun: []`、`stages.skipped: []`。
- `claims.cannot_claim: []`，没有披露未重跑链段和完整流程不可声称范围。
- run manifest Revision 校验要求明确基线，并逐项列出复用生成物、实际重跑、未重跑链段与 `cannot_claim`；Skill 与 Phase 4 都只允许声称实际局部修订范围。

### 主要理由

revision 允许复用，但“允许复用”不等于“可以不披露复用”。场景事实和 manifest 记录不一致，且不可声称范围为空，运行完整性证据不闭合。

### 可声称范围

只能声称：该合成 revision manifest 因披露缺失而应拒绝。不能声称：真实 assembly 实际读取了什么、局部版式修订质量如何，或完整 revision 运行曾发生。

---

## RI-N05

- kind: `derived-structure`
- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- runtime_status: `runtime-not-run`

### 结构依据

- 样本为 `basis: proposed`，选择理由是执行者主动选择更短章节。
- `affects_capability_claim: true`，但 `user_confirmation: pending`。
- manifest 已进入 `status: running`，且 `stages.executed` 已包含 `source-read`。
- run manifest 结束检查与 Phase 4 开跑前闸门都要求：会影响能力结论的样本，在用户确认前不得开跑，也不得静默换成更容易的小切片。

### 主要理由

必要确认是生产开始前的硬门，不是可以在执行后补齐的记录字段。确认仍 pending 时已有阶段执行，已经越过停止点。

### 可声称范围

只能声称：该合成状态序列违反样本确认闸门。不能声称：真实用户曾拒绝样本、真实章节更容易通过，或实际 source-read 已发生。

---

## RI-N06

- kind: `derived-structure`
- expected: `reject`
- actual_verdict: `reject`
- matches_expected: `yes`
- runtime_status: `runtime-not-run`

### 结构依据

- 实际执行仅列 `markdown-syntax-check` 与 `asset-card-cold-start`。
- `source-read`、`source-map`、`candidate-production`、`independent-content-judging`、`reader-page-assembly` 明确列为 skipped。
- 尽管如此，`claims.can_claim` 写为“ReaderLab 完整 fresh 流程已通过”，`claims.cannot_claim` 为空，`verification.run_integrity` 还写为 `pass`。
- run manifest 限定 `can_claim` 为“实际执行 + 对应独立门通过”的交集；judge 第 5、6 节、Skill 完成声明与 Phase 4 共用边界都禁止用机器检查、局部页或单卡冷启动升级成完整 fresh 流程。

### 主要理由

声明覆盖范围显著大于实际执行范围。被跳过的链段正是完整 fresh 所需核心阶段，因此完整流程声明与运行完整性 `pass` 均不成立。

### 可声称范围

只能声称：该合成结构最多支持“语法检查与单卡冷启动已被登记为执行”，且不足以支持完整 fresh 声明；由于本次没有真实运行，也不能进一步声称这两个局部检查实际通过。

---

## RI-P01

- kind: `derived-structure`
- expected: `accept`
- actual_verdict: `accept`
- matches_expected: `yes`
- runtime_status: `runtime-not-run`

### 结构依据

- 模式先声明为 `fresh`；原始路径、指纹、实际读取范围、样本依据与任务预算均有记录。
- `base_generated_artifact: none`、`reused_generated_artifacts: none`、`stages.reused_without_rerun: []`，满足零生成产物复用结构。
- 输出目录标为本次唯一目录，`preexisting: false`、`writes_to_previous_run: false`。
- 样本由 case fixture 权威固定，`affects_capability_claim: false`、`user_confirmation: not-required`，不存在待确认却开跑的结构矛盾。
- `stages.executed` 覆盖该合成声明所列的来源读取、正文/source map、识别、候选、核查、独立裁判、装配与运行完整性复核；`skipped`、`failed`、`reused_without_rerun` 均为空。
- `claims.can_claim` 只指向“该合成 manifest 所描述链段的 fresh 运行完整性”，并在 `cannot_claim` 明确排除内容质量、用户体验和 ReaderLab 全部能力。
- 其他质量门保持 `not-run` / `not-requested`，没有拿运行完整性替代内容质量或用户体验。

### 主要理由

在把所有字段视为合成测试输入、而不是现场真实性证据的前提下，fresh 的来源、零复用、输出隔离、样本、执行阶段和声明范围彼此闭合，没有出现当前合同规定的结构拒绝条件。

### 可声称范围

只能声称：这张合成 manifest 在当前合同下是结构自洽的正例，独立 verdict 与 Expected 一致。不得声称：字段内容已被现场核验、真实 fresh run 已发生、这些阶段真的执行过、运行完整性在真实环境通过、内容质量通过、用户体验通过或 ReaderLab 全部能力通过。

---

## 汇总

| case | expected | actual | match | evidence kind |
|---|---|---|---|---|
| RI-N01 | reject | reject | yes | derived-structure |
| RI-N02 | reject | reject | yes | derived-structure |
| RI-N03 | reject | reject | yes | derived-structure |
| RI-N04 | reject | reject | yes | derived-structure |
| RI-N05 | reject | reject | yes | derived-structure |
| RI-N06 | reject | reject | yes | derived-structure |
| RI-P01 | accept | accept | yes | derived-structure |

- matched_cases: `7/7`
- mismatched_cases: `0`
- blocked_cases: `0`
- suite_structural_result: `pass`
- suite_claim_boundary: 仅证明这 7 张派生结构卡在当前合同下得到预期 verdict；不构成历史回放、真实运行、内容质量、用户体验、Phase 4 或 ReaderLab V3 整体通过。
