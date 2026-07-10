---
id: RI-N04
kind: derived-structure
line: run-integrity
freeze_status: frozen
historical_run: false
independent_execution_result: reject-matched
future_raw_result_path: v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n04
---

# RI-N04：revision 隐瞒复用和未重跑阶段

这是由当前运行合同派生的结构测试，不是历史运行，也不证明发生过 revision run。

## 最小运行场景输入

```yaml
run_id: fixture-ri-n04
status: accepted
mode: revision
reuse:
  base_generated_artifact: /previous-run/reader-page.md
  reused_generated_artifacts: none
stages:
  executed:
    - assembly
  skipped: []
  failed: []
  reused_without_rerun: []
claims:
  can_claim:
    - 局部版式修订通过
  cannot_claim: []
```

场景事实：`assembly` 直接读取了 `base_generated_artifact`；manifest 却没有列出复用产物、未重跑阶段和不可声称范围。

## 规范依据

- `v3/skill/templates/run-manifest.md` 的 Revision 校验：基线、复用生成物、实际重跑、未重跑链段和 `cannot_claim` 必须逐项声明。
- `v3/skill/SKILL.md` 的 Revision run 与 `v3/standards/phase4-pilot-definition.md` 的运行真实性：revision 只能声称实际局部修订范围。

## Expected

`reject`

## 必须保持的行为

revision 可以复用旧产物，但不能隐瞒复用或用空数组抹去未重跑阶段；缺少任一关键披露时，运行完整性门必须失败。

## 独立执行

- result: `reject (matched)`
- raw result: `v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n04`
