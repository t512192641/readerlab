# Run Integrity 派生结构回归复跑 6：图书批量事实请求

## 执行边界

- evaluated_at_utc: `2026-07-10T11:50:01Z`
- evaluated_at_local: `2026-07-10T07:50:01-04:00`
- test_kind: `derived-structure`
- runtime_status: `runtime-not-run`
- historical_replay: `false`
- real_fresh_run_observed: `false`
- real_revision_run_observed: `false`
- previous_raw_files_preserved: `true`
- previous_raw_files_used_as_evidence: `false`

本次重新读取当前 7 张 run-integrity case、运行合同与图书事实请求相关协议 / 角色合同。旧 raw 保留，未读取、未修改、未作为 verdict 证据；未修改 case 或规则。

判定口径：`reject` 表示合成场景命中硬门；`accept-structure-only` 只表示合成 manifest 与当前角色 handoff 可结构闭合。全部 case 均为 `derived-structure / runtime-not-run`。

---

## RI-N01

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

fresh 复用了上一 run 的 source map，并表示该阶段未重跑。Fresh 要求生成物零复用，故 reject。

可声称范围：只证明合成结构拒绝，不证明真实旧产物被读取。

---

## RI-N02

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

fresh 输出目录已存在且会写入上一 run，违反唯一隔离目录与不得覆盖/混写/回填，故 reject。

可声称范围：只证明合成隔离字段非法，不证明真实磁盘污染。

---

## RI-N03

- expected: `reject`
- actual: `reject`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### 事实请求与证据

RI-N03 现在给出：

- conditional fact check `status: pass`
- owner 为 fact-checker
- `request_refs: [fixture-request]`
- 子门与聚合 evidence 均为 `previous-run-audit`
- `relocated_and_verified_this_run: false`

非空 request ref 只证明结构上引用了请求，不证明请求 claims 已在本次核实。Fresh 明确要求旧 URL / audit 只能作为定位线索，外部事实必须本次重新定位核实；fact-checker 的外部事实 supported 也要求至少一个本次核实的 high-trust 来源。

因此 conditional fact check 不得 pass，source_and_fact aggregate 不得 pass，run_integrity 和 accepted 也不成立。actual reject 与 Expected 匹配。

可声称范围：只证明 typed request 不能把旧 audit 变成本次证据；不判断事实真假，也不证明真实核查发生。

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

只登记语法检查与资产卡冷启动，核心 fresh 链段均 skipped，却声明完整 fresh 与 run_integrity 通过，且 cannot_claim 为空。声明超出执行与验收交集，故 reject。

可声称范围：只证明合成声明越界，不证明局部检查真实通过。

---

## RI-P01

- expected: `accept-structure-only`
- actual: `accept-structure-only`
- match: `yes`
- kind: `derived-structure`
- runtime: `runtime-not-run`

### Fresh 前置

- book route、固定全章来源、指纹与读取范围齐全。
- 样本确认组合 `false + not-required` 合法。
- 生成产物零复用。
- 输出为新隔离目录，不写旧 run。

前置结构闭合。

### 图书 typed fact requests

当前图书 cognition-candidate 合同规定：

- 三个 candidate 实例各提交一个 `fact_check_request`。
- request / claim id 在本 run 内非空且唯一。
- claims 列全 necessary evidence 中需核实的源内事实、外部事实与因果断言。
- kind 统一为 `source-internal | external`，因果性另用 `assertion_type: factual | causal` 表达。
- 0 候选才跳过 fact-checker；本正例存在三份 request refs，不走 0 候选路径。

当前 fact-checker 合同允许一个批量任务接收一份或多份 typed requests，并要求：

- `request_ids` 与输入 request id 集合精确相等。
- 每个 request 分别做 coverage。
- 全部可见事实 supported，外部事实有本次 high-trust 来源，整批才 pass。

RI-P01 的 conditional fact gate 给出：

```yaml
status: pass
owner: fact-checker
request_refs:
  - fixture-book-request-1
  - fixture-book-request-2
  - fixture-book-request-3
evidence:
  - fixture-fact-check-batch
```

三份 request refs 与三个候选实例对应，批量 evidence 有合法落点；不再出现“fact-checker executed 但 request none / 子门 not-applicable”的矛盾。

case 还提供了自包含的合成 audit evidence，可逐字段检查：

- 三个 requests 分别具有非空唯一 request id、claim id、candidate id 和 anchor id。
- claims 覆盖 source-internal factual、external factual、external causal 三种组合；因果性由 assertion_type 表达，不再与 source kind 混淆。
- fact_check_batch.request_ids 与三份输入 request id 集合精确相等。
- 三个 checks 的 check id 非空唯一，并分别回接对应 request / claim。
- 每个 request 都有独立 coverage；request_claim_ids 与 checked_claim_ids 精确相等，complete 为 true。
- material 与 non-material 可见事实全部得到 supported；没有以 non-material 绕过核查。
- 外部事实 evidence 均标 high 且 verified_this_run true；源内事实回到 fixture chapter 的定位。
- batch overall 为 pass，与 conditional_fact_check pass 和 request_refs 三项一致。

作为 fixture，它已经能完整表达一个 fact-checker 任务对三份 typed requests 的批量输入、逐项核查、精确 coverage 和聚合通过。

### 11 个 dispatch 与预算

executed 包含 source-map 1、nominator 2、merger 1、candidate 3、fact-checker 1、judge 1、writer 1、cold-reader 1，共 11 个互不重复实例级 dispatch。

- `actual_tasks: 11`
- `task_limit: 12`
- skipped / failed / reused 均为空

事实核查是一个批量任务而不是三次任务，因此仍为标准 11；盲区检查并入 cognition judge，不另计任务。

### Nested gate 与 accepted

- source provenance: pass，有 source-map evidence。
- conditional fact check: pass，有三份 request refs 和 batch result evidence。
- aggregate source_and_fact: pass，owner/scope/evidence/conflicts 齐全。
- absolute value、regression、cold read、run integrity 均 pass。
- cold-start/reproduction 明确 not-applicable；user experience not-requested。
- 无 blocked、pending、failed、awaiting acceptance 或超预算。

can_claim 只覆盖合成结构接受；cannot_claim 明确排除真实 fresh、内容质量、用户体验和全部能力。accepted 在当前合成字段与角色 handoff 间闭合。

### 为什么仍只能 structure-only

本次读取并核对了 fixture 中的具体 request、check 与 coverage 对象；但这些对象、来源、目录、11 dispatch 和各门状态仍全部是合成记录。本次没有真正打开 fixture-primary-source、执行 fact checker、现场验证 `verified_this_run` 声明、运行其余门或取得用户回执。

因此只能接受“合法批量输入与门结构可表达”，不能声称真实事实核查或 fresh run 已通过。actual 为 `accept-structure-only`，runtime 仍为 `runtime-not-run`。

可声称范围：只可声称 RI-P01 是当前 typed book fact request schema 下的结构正例；不可声称真实 fresh、内容质量、用户体验、Phase 4 或 ReaderLab 全能力通过。

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

当前 7 张 run-integrity 派生结构卡 7/7 与 Expected 匹配。RI-P01 现在能表达三个候选实例各自产生 typed request、一个 fact-checker 批量处理三份输入、11 个实例级 dispatch、嵌套 source_and_fact pass 与 accepted；只获得 structure-only 接受。RI-N03 即使有 typed request ref，仍因使用未在本次核实的旧 audit 而 reject。

总 verdict 为 `pass-derived-structure-only`，runtime 为 `not-run`。本结果不构成历史回放、真实运行、事实/内容质量、用户体验、Phase 4 或 ReaderLab V3 整体通过。
