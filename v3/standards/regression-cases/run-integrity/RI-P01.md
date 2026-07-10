---
id: RI-P01
kind: derived-structure
line: run-integrity
freeze_status: frozen
historical_run: false
independent_execution_result: accept-structure-only-matched
future_raw_result_path: v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-p01
---

# RI-P01：合规 fresh manifest

这是由当前运行合同派生的正向结构测试，不是历史运行。下列内容只是供独立审查者判定的合成 manifest，不证明发生过 fresh run，也不证明任何内容质量或用户体验。

## 最小运行场景输入

```yaml
run_id: fixture-ri-p01
started_at: 2000-01-01T00:00:00Z
status: accepted
mode: fresh
route:
  line: book
  mixed_handling: not-applicable
  child_run_ids: []
source:
  material_type: book
  original_paths:
    - /fixtures/source/chapter-01.md
  fingerprints:
    - path: /fixtures/source/chapter-01.md
      size: 2048
      modified_at: 2000-01-01T00:00:00Z
      sha256: fixture-sha256
  actual_read_scope:
    - /fixtures/source/chapter-01.md:1-120
sample:
  basis: fixed-by-authority
  authority_or_reason: case fixture 固定全章
  affects_capability_claim: false
  confirmation_required: false
  user_confirmation: not-required
reuse:
  stable_standards_and_gold:
    - v3/standards/constraint-architecture.md
  base_generated_artifact: none
  reused_generated_artifacts: none
output:
  new_isolated_directory: /fixtures/runs/fixture-ri-p01
  preexisting: false
  writes_to_previous_run: false
budget:
  task_limit: 12
  actual_tasks: 11
  expansion_trigger: none
  user_approved_overrun: false
stages:
  executed:
    - book-source-map-1
    - book-anchor-nominator-1
    - book-anchor-nominator-2
    - book-anchor-merger-1
    - book-cognition-candidate-1
    - book-cognition-candidate-2
    - book-cognition-candidate-3
    - book-fact-checker-1
    - book-cognition-judge-1
    - book-writer-1
    - book-cold-reader-1
  skipped: []
  failed: []
  reused_without_rerun: []
verification:
  source_and_fact:
    status: pass
    owner: orchestrator
    source_provenance: {status: pass, owner: source-map, evidence: [fixture-source-map]}
    conditional_fact_check: {status: pass, owner: fact-checker, request_refs: [fixture-book-request-1, fixture-book-request-2, fixture-book-request-3], evidence: [fixture-fact-check-batch]}
    scope: [fixture-chapter]
    evidence: [fixture-source-map]
    conflicts: []
  absolute_value: {status: pass, owner: cognition-judge, scope: [fixture-candidates], evidence: [fixture-absolute-verdict], conflicts: []}
  regression: {status: pass, owner: regression-runner, scope: [fixture-regression-cases], evidence: [fixture-regression-result], conflicts: []}
  cold_read: {status: pass, owner: cold-reader, scope: [fixture-reader-page], evidence: [fixture-cold-read], conflicts: []}
  cold_start_or_reproduction: {status: not-applicable, owner: orchestrator, scope: [], evidence: [], conflicts: []}
  run_integrity: {status: pass, owner: run-integrity-reviewer, scope: [fixture-ri-p01], evidence: [fixture-manifest-review], conflicts: []}
  user_experience: {status: not-requested, owner: user, scope: [], evidence: []}
claims:
  can_claim:
    - 该合成 manifest 的 fresh 结构约束可被运行完整性门接受（runtime-not-run）
  cannot_claim:
    - 真实 fresh run 已发生
    - 内容质量通过
    - 用户体验通过
    - ReaderLab 全部能力已通过
  reused_results_only: []
  awaiting_user_acceptance: []
```

## 合成 audit evidence

以下对象只让结构审查者核对 request / check / coverage handoff；它们仍是 fixture，不是现场执行证据。

```yaml
fact_check_requests:
  - {request_id: fixture-book-request-1, status: required, requested_by: cognition-candidate, trigger_reason: candidate-necessary-evidence, claims: [{claim_id: fixture-claim-1, candidate_id: fixture-candidate-1, anchor_id: fixture-anchor, text: fixture fact 1, kind: source-internal, assertion_type: factual, materiality: material, visible: true, existing_source_refs: [/fixtures/source/chapter-01.md:10]}], allowed_external_source_boundary: []}
  - {request_id: fixture-book-request-2, status: required, requested_by: cognition-candidate, trigger_reason: candidate-necessary-evidence, claims: [{claim_id: fixture-claim-2, candidate_id: fixture-candidate-2, anchor_id: fixture-anchor, text: fixture fact 2, kind: external, assertion_type: factual, materiality: non-material, visible: true, existing_source_refs: [fixture-primary-source]}], allowed_external_source_boundary: [fixture-primary-source]}
  - {request_id: fixture-book-request-3, status: required, requested_by: cognition-candidate, trigger_reason: candidate-necessary-evidence, claims: [{claim_id: fixture-claim-3, candidate_id: fixture-candidate-3, anchor_id: fixture-anchor, text: fixture causal claim, kind: external, assertion_type: causal, materiality: material, visible: true, existing_source_refs: [fixture-primary-source]}], allowed_external_source_boundary: [fixture-primary-source]}
fact_check_batch:
  request_ids: [fixture-book-request-1, fixture-book-request-2, fixture-book-request-3]
  checks:
    - {check_id: fixture-check-1, request_id: fixture-book-request-1, claim_id: fixture-claim-1, candidate_id: fixture-candidate-1, anchor_id: fixture-anchor, kind: source-internal, assertion_type: factual, materiality: material, verdict: supported, sources: [{ref: /fixtures/source/chapter-01.md, locator: line-10, trust: high, verified_this_run: true}], minimal_correction: ""}
    - {check_id: fixture-check-2, request_id: fixture-book-request-2, claim_id: fixture-claim-2, candidate_id: fixture-candidate-2, anchor_id: fixture-anchor, kind: external, assertion_type: factual, materiality: non-material, verdict: supported, sources: [{ref: fixture-primary-source, locator: fixture-location-2, trust: high, verified_this_run: true}], minimal_correction: ""}
    - {check_id: fixture-check-3, request_id: fixture-book-request-3, claim_id: fixture-claim-3, candidate_id: fixture-candidate-3, anchor_id: fixture-anchor, kind: external, assertion_type: causal, materiality: material, verdict: supported, sources: [{ref: fixture-primary-source, locator: fixture-location-3, trust: high, verified_this_run: true}], minimal_correction: ""}
  coverage:
    - {request_id: fixture-book-request-1, request_claim_ids: [fixture-claim-1], checked_claim_ids: [fixture-claim-1], material_claim_ids: [fixture-claim-1], complete: true}
    - {request_id: fixture-book-request-2, request_claim_ids: [fixture-claim-2], checked_claim_ids: [fixture-claim-2], material_claim_ids: [], complete: true}
    - {request_id: fixture-book-request-3, request_claim_ids: [fixture-claim-3], checked_claim_ids: [fixture-claim-3], material_claim_ids: [fixture-claim-3], complete: true}
  overall: pass
  blocked_reason: ""
  return_to: ""
```

## 规范依据

- `v3/skill/templates/run-manifest.md` 的 Fresh 校验与结束检查。
- `v3/skill/SKILL.md`、`v3/skill/templates/run-manifest.md` 与 `v3/standards/phase4-pilot-definition.md`：原始源、零生成产物复用、唯一隔离目录、样本依据、实际阶段和声明范围必须闭合。
- `v3/skill/protocols/judge.md` 第 6 节：运行真实性与内容质量分别判定，互不替代。

## Expected

`accept-structure-only`

## 必须保持的行为

仅当 manifest 同时满足原始源可核验、生成产物零复用、输出隔离、样本合规、执行链段和声明范围一致时，结构上接受 fresh 运行完整性；仍不得据此声称内容质量、用户体验或真实 fresh run 已发生。

## 独立执行

- result: `accept-structure-only (matched; runtime-not-run)`
- raw result: `v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-p01`
