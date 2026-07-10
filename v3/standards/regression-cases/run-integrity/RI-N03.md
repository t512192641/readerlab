---
id: RI-N03
kind: derived-structure
line: run-integrity
freeze_status: frozen
historical_run: false
independent_execution_result: reject-matched
future_raw_result_path: v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n03
---

# RI-N03：旧 URL 冒充本次核实证据

这是由当前运行合同派生的结构测试，不是历史运行，也不证明发生过 fresh run。`fact_evidence` 是本 case 的最小运行证据输入，不是在扩展正式 manifest schema。

## 最小运行场景输入

```yaml
run_id: fixture-ri-n03
status: accepted
mode: fresh
fact_evidence:
  - claim_id: F-01
    url: https://example.invalid/source-used-by-previous-run
    evidence_origin: previous-run-audit
    relocated_and_verified_this_run: false
verification:
  source_and_fact:
    status: pass
    owner: orchestrator
    source_provenance: {status: pass, owner: source-map, evidence: [fixture-source-map]}
    conditional_fact_check: {status: pass, owner: fact-checker, request_refs: [fixture-request], evidence: [previous-run-audit]}
    scope: [fixture-claim]
    evidence: [previous-run-audit]
    conflicts: []
  run_integrity: {status: pass, owner: run-integrity-reviewer, scope: [fixture-ri-n03], evidence: [previous-run-audit], conflicts: []}
```

## 规范依据

- `v3/skill/templates/run-manifest.md` 的 Fresh 校验：旧 URL 只能作为线索，外部事实必须在本次重新定位核实。
- `v3/skill/SKILL.md` 的 Fresh run 与 `v3/standards/phase4-pilot-definition.md` 的运行真实性：旧 audit 不能充当本次已核实证据。

## Expected

`reject`

## 必须保持的行为

`relocated_and_verified_this_run: false` 时不得把来源与事实门或运行完整性门记为通过；保留旧 URL 作为搜索线索不等于证据复用合法。

## 独立执行

- result: `reject (matched)`
- raw result: `v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n03`
