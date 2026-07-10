---
id: RI-N05
kind: derived-structure
line: run-integrity
freeze_status: frozen
historical_run: false
independent_execution_result: reject-matched
future_raw_result_path: v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n05
---

# RI-N05：样本影响结论但未确认就开跑

这是由当前运行合同派生的结构测试，不是历史运行，也不证明发生过 fresh run。

## 最小运行场景输入

```yaml
run_id: fixture-ri-n05
status: running
mode: fresh
sample:
  basis: proposed
  authority_or_reason: 执行者选择最短章节以降低任务量
  affects_capability_claim: true
  confirmation_required: true
  user_confirmation: pending
stages:
  executed:
    - source-read
```

## 规范依据

- `v3/skill/templates/run-manifest.md` 的结束检查：样本影响结论时，用户确认未通过不得开跑。
- `v3/standards/phase4-pilot-definition.md` 的开跑前闸门：不得静默选择更容易通过的样本或用更小切片替代固定样本。

## Expected

`reject`

## 必须保持的行为

当 `affects_capability_claim: true` 且 `user_confirmation: pending` 时，任何生产阶段已执行都构成越过确认门；运行必须停在等待用户，而不是继续后补确认。

## 独立执行

- result: `reject (matched)`
- raw result: `v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n05`
