---
id: RI-N06
kind: derived-structure
line: run-integrity
freeze_status: frozen
historical_run: false
independent_execution_result: reject-matched
future_raw_result_path: v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n06
---

# RI-N06：局部检查扩大为全流程声明

这是由当前运行合同派生的结构测试，不是历史运行，也不证明发生过 fresh run。

## 最小运行场景输入

```yaml
run_id: fixture-ri-n06
status: accepted
mode: fresh
stages:
  executed:
    - markdown-syntax-check
    - asset-card-cold-start
  skipped:
    - source-read
    - source-map
    - candidate-production
    - independent-content-judging
    - reader-page-assembly
verification:
  cold_start_or_reproduction: {status: pass, owner: cold-start-reproducer, scope: [fixture-card], evidence: [fixture-card-check], conflicts: []}
  run_integrity: {status: pass, owner: orchestrator, scope: [fixture-ri-n06], evidence: [fixture-local-checks], conflicts: []}
  user_experience: {status: not-requested, owner: user, scope: [], evidence: []}
claims:
  can_claim:
    - ReaderLab 完整 fresh 流程已通过
  cannot_claim: []
```

## 规范依据

- `v3/skill/templates/run-manifest.md`：`can_claim` 只能覆盖实际执行与对应独立门通过的交集。
- `v3/skill/protocols/judge.md` 第 5、6 节：资产卡冷启动只证明单卡；局部或机器检查不得升级为完整真实运行。
- `v3/skill/SKILL.md` 的完成声明与 `v3/standards/phase4-pilot-definition.md` 的共用边界：最终声明必须逐段区分实际执行、复用、未执行和未验收链段。

## Expected

`reject`

## 必须保持的行为

机器检查、局部页或资产卡冷启动通过时，只能声明对应局部范围；只要完整流程所需链段被跳过，完整 fresh 声明与 `run_integrity: pass` 都必须被拒绝。

## 独立执行

- result: `reject (matched)`
- raw result: `v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n06`
