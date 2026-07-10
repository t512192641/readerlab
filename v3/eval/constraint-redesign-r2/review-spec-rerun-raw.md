# 2026-07-10 约束重构返工：独立 Spec 复验原始输出

## 复验边界

- reviewed_at_utc: `2026-07-10T11:44:49Z`
- reviewed_at_local: `2026-07-10T07:44:49-04:00`
- axis: `Spec`
- verdict_policy: `any blocker => fail`
- previous_spec_fail_preserved: `true`
- real_run_performed: `false`
- rules_or_cases_modified: `false`

首次 Spec fail 保留不改。本次按当前最终文件重新核对首次 `SPEC-B01 / SPEC-B02`、用户其余逐项要求、29/29、声明边界与 dirty worktree 分离；纳入 fact-gate rerun-4 与 RI rerun-5，但只使用它们明确验收的 scope，不把专项 pass 扩大成整条链通过。

## 总 verdict

- final_verdict: `fail`
- blockers: `2`
- passed_requirement_groups: `9`
- non_blocking_items: `3`

首次两个 blocker 的表面字段已大量修复，但端到端 Spec 仍未闭合：

1. `SPEC-B01`：事实逐项枚举、Skill request、fact-checker coverage、manifest/orchestrator 嵌套持久化已闭合；但图书 cognition-candidate 仍没有 fact-checker 必需的类型化 request envelope，完整 handoff 失败。
2. `SPEC-B02`：RI-P01 已有 11 个唯一 dispatch 和完整 nested gate；但它把 `book-fact-checker-1` 记为 executed，同时条件事实门是 not-applicable、request_ref none。当前 fact-checker 合同要求运行时必须收到非空类型化 request，因此该 dispatch 无合法输入，RI-P01 仍不能结构接受。

任何 blocker 必须 fail，因此 Spec 轴继续为 `fail`。

---

## SPEC-B01：事实枚举与完整 handoff

- status: `blocker-open`
- result: `fail`

### 已关闭部分

当前文件已经关闭首次枚举冲突及 Skill 事实链的大部分缺口：

- `judge.md` 与 fact-checker item verdict 统一为 `supported | conflicted | insufficient | out_of_scope`。
- fact-checker 外部事实 `supported` 要求本次定位核实的 high-trust 来源。
- Skill mechanism auditor 能输出非空唯一 `fact_check_request`，列全可见事实，不论 materiality。
- fact-checker 输出 request id、唯一 check id、精确 coverage 集合与 overall。
- Skill judge 能用 check id / claim id 回接 request，并在 coverage 不完整时停止。
- manifest 与 orchestrator 的 `source_and_fact` 均为同形嵌套对象：status、owner、source_provenance、conditional_fact_check、scope、evidence、conflicts。
- judge 明确要求覆盖 request 中全部可见事实，不论 materiality。

`role-cold-start-fact-gate-rerun-4-raw.md` 的 scoped pass 只验证最后两项：manifest/orchestrator 同形，以及 judge 全部可见 facts。它没有复核图书候选到 fact-checker 的输入。

### 仍开放的阻塞

图书 `cognition-candidate.md` 当前只输出：

```yaml
facts_to_check:
  - claim_id
    candidate_id
    anchor_id
    claim_text
    claim_type: source | external | causal
    conclusion_impact: material | non-material
```

但共用 `fact-checker.md` 的允许输入和输出要求：

- 输入必须是类型化 `fact_check_request`。
- `request_id` 必须是非空唯一 id，并精确引用输入 request。
- claim kind 使用 `source-internal | external`。
- coverage 必须比较 request_claim_ids 与 checked_claim_ids。

当前图书上游没有：

- request_id
- request status / trigger
- requested_by
- allowed source boundary
- 与 fact-checker 一致的 kind 枚举
- 可供 coverage 精确比较的 request envelope

`claim_type: causal` 也无法无损映射到 fact-checker 的 `kind: source-internal | external`，且没有权威映射规则。

### 影响

- 图书标准链的 cognition-candidate → fact-checker 无法只凭合同直接 handoff。
- 主控若临时把 `facts_to_check` 包装成 request，会在合同外发明 request id、kind 映射和取证边界，违反“执行合同不需要完整协议”和唯一事实源要求。
- 图书 fact-checker 结果也无法证明 coverage 对应了原始候选列出的全部事实。
- 因此不能声称事实门“完整 handoff”通过，fact-gate rerun-4 的专项 pass 不得扩大。

### 最小解除条件

让图书 cognition-candidate 直接输出与 Skill 同等严格的类型化 request envelope，或定义一个独立、权威、可无损的 book facts_to_check → fact_check_request 转换合同；同时统一 causal 的表达。修后需对图书候选 → fact-checker → cognition-judge 做一次限定冷启动复跑。

---

## SPEC-B02：RI-P01 11 dispatch 与 nested fact gate

- status: `blocker-open`
- result: `fail`

### 已关闭部分

RI-P01 当前已经满足：

- book route、固定全章来源、合法样本确认、零生成物复用与新隔离目录。
- 11 个唯一实例级 dispatch：1 source map、2 nomination、1 merger、3 candidate、1 fact checker、1 judge、1 writer、1 cold reader。
- `actual_tasks: 11`，与 executed dispatch 数一致且低于 task limit 12。
- source_and_fact 有完整顶层 owner/scope/evidence/conflicts 与两个子门。
- 其他适用技术门为 pass，不适用门明确，accepted 无 pending/blocked。
- can_claim 只写 structure-only，cannot_claim 排除真实 run、内容质量、用户体验和全部能力。

### 仍开放的阻塞

同一 RI-P01 同时记录：

```text
executed: book-fact-checker-1
conditional_fact_check.status: not-applicable
conditional_fact_check.request_ref: none
conditional_fact_check.evidence: []
```

当前 fact-checker 合同却要求：

- 允许输入必须包含类型化 fact_check_request。
- 输出 `request_id` 必须是非空 request id。
- coverage 必须针对该 request 完整结算。

因此，`book-fact-checker-1` 若实际 executed，就没有合同允许的输入，也不能产生合法输出。若条件事实核查确实 not-applicable、request_ref none，则该 fact-checker dispatch 应为 skipped/not-applicable，而不应计入 executed 和 actual_tasks。

更深一层，图书标准链又固定包含 fact-checker 1 个任务；这正说明 `SPEC-B01` 的图书 request envelope 不能缺失。当前 fixture 用“11 个名称齐全”掩盖了 fact-checker 实例没有可执行输入的问题。

### 对 RI rerun-5 的判断

`regression-run-integrity-rerun-5-raw.md` 在其限定读取内确认 11 个 id、nested fields 与声明边界，因此得到 `accept-structure-only`。它没有读取 fact-checker 或 cognition-candidate 角色合同，不能证明 `book-fact-checker-1` 的输入/输出合法。

RI rerun-5 的 `runtime-not-run` 边界是正确的；但其 structure accept 不能在跨文件 Spec 复验中成立。

### 影响

- RI-P01 当前 actual 应为 `reject` 或 `blocked`，不能是 `accept-structure-only`。
- run-integrity 7/7 不成立。
- regression-suite 的 29/29 不成立。
- calibration-log 更正节中的“最终复跑 7/7 匹配”需等待 blocker 修复后才能恢复。

### 最小解除条件

先关闭 SPEC-B01，为图书 fact-checker 提供合法 request。随后让 RI-P01 的 fact-checker dispatch 与 conditional fact subgate 一致：

- 若执行 fact-checker，则提供非空 request_ref、coverage 和合成 evidence，并将子门设为 pass；或
- 若确实 not-applicable，则不要把 fact-checker 记为 executed，并同步说明图书固定 11 任务如何保持。

修后独立重跑 RI-P01，再据 actual 更新 suite。

---

## 用户其余要求复核

| 要求 | 结果 | 证据与边界 |
|---|---|---|
| 盲区并入裁判，图书固定 11 | `pass` | current-task 第 32 行、constraint、SKILL、roles README、book-engine、cognition-judge 一致；主控不计。 |
| Skill 3—5 任务所有权 | `pass` | source integrator 生产正文/source map，mechanism auditor 生产候选，skill judge 独立裁判，writer 成文，cold-start reproducer 独立冷读/复现；简单材料不允许生产者自评。 |
| 锚点调查问题 | `pass` | nominator 有 shallow/wrong reading 与 investigation_question；merger 保留问题和定向返工。 |
| Skill source map actions / deletion destination | `pass` | clean units 有 retained/moved/merged/reordered+treatment；deletions 有 reason 与 appendix/technical-lead/audit/omitted。 |
| 状态枚举 | `pass_with_B01_handoff_blocker` | 顶层状态、not-applicable、确认组合及 fact item 枚举已对齐；图书 request envelope 仍不闭合。 |
| 历史 / 派生分类 | `pass` | 29 卡分为 16 historical + 13 derived-structure；派生卡不冒充历史。 |
| B-N07 后续用户否定 | `pass` | 后续“未过体验门”覆盖旧 waiting，book raw 限定 reject 范围。 |
| 角色冷启动 raw | `pass_with_scope_warning` | 图书、Skill、主控均保留首次 fail 与定向 rerun；fact-gate rerun-4 仅 scoped pass，不覆盖图书 handoff。 |
| 成本 | `pass_except_RI-P01_semantic_dispatch` | 图书固定 11、Skill 5/简单 3—4，预算规则一致；RI-P01 的 fact-checker 名称虽计数，语义不可执行。 |
| 可分离变更集 | `pass_with_caution` | change-set-boundary 分 A/B，旧 022/Demo 等明确排除；未来仍需逐 hunk staging。 |
| 声明不升级 | `pass` | 所有最新 raw 保持 structure-only/runtime-not-run；calibration 更正覆盖旧宽泛声明；current-task 仍不允许 Demo。 |

## 29/29 复核

- 图书历史回归：`12/12` 仍可保留。
- Skill 回归：`10/10` 仍可保留。
- RI-N01—RI-N06：`6/6` reject 仍可保留。
- RI-P01：当前跨文件 Spec actual 不能 accept，故 mismatch / blocker。
- total: `28/29 supported; 1 blocked-or-mismatched`
- suite_result: `fail`

分类、B-N07 和前 28 张实际证据没有被本次 blocker 推翻；失败集中于 RI-P01 的正向结构与图书 fact handoff。

## 声明边界

正确保留：

- fact-gate rerun-4 只证明最后两个静态冲突关闭。
- RI rerun-5 只证明其限定文件下字段结构与 runtime-not-run 边界。
- role cold-start 均为静态合同检查。
- 未发生真实 fresh/revision、内容生成、用户体验、Phase 4 或 V3 整体通过。

不得声称：

- 完整事实 handoff 通过。
- RI-P01 结构正例通过。
- run-integrity 7/7。
- 全部 29/29。
- Spec 轴通过或可以开始 Demo。

## Dirty worktree 与分离

- `git status --short` 仍显示大量 tracked 修改与基线外未跟踪产物，工作区不干净。
- `change-set-boundary.md` 已将本轮 A 组与旧 022 R1/R2、候选 audit、版式 Demo、已消费提示和旧设计合同 B 组分开。
- calibration-log 与 Phase 4 gate 含返工前未提交内容，物理提交必须逐 hunk 处理。
- 当前只证明可分开审查，不证明已物理暂存或提交。
- `git diff --check`: `pass`。

该项无 blocker，但未来 staging 时必须再次核对 status 和具体 hunk。

## 最终 verdict

```yaml
axis: spec
verdict: fail
blockers:
  - SPEC-B01: book cognition-candidate cannot produce required typed fact_check_request
  - SPEC-B02: RI-P01 executes fact-checker while conditional fact gate is not-applicable with no request
supported_cases: 28/29
runtime: not-run
```

最小下一步：先统一图书候选的 typed fact request handoff，再让 RI-P01 的 fact-checker dispatch 与 nested conditional gate 语义一致并独立复跑。两项关闭前，Spec 必须保持 fail；专项 pass、字段齐全和 11 个任务名称不能替代端到端可执行性。
