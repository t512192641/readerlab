---
id: RI-N01
kind: derived-structure
line: run-integrity
freeze_status: frozen
historical_run: false
independent_execution_result: reject-matched
future_raw_result_path: v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n01
---

# RI-N01：fresh 复用旧生成产物

这是由当前运行合同派生的结构测试，不是历史运行，也不证明发生过 fresh run。

## 最小运行场景输入

```yaml
run_id: fixture-ri-n01
status: planned
mode: fresh
reuse:
  base_generated_artifact: none
  reused_generated_artifacts:
    - /previous-run/audit/source-map.yaml
  reused_without_rerun:
    - source-map
output:
  new_isolated_directory: /fixtures/runs/fixture-ri-n01
  preexisting: false
  writes_to_previous_run: false
```

## 规范依据

- `v3/skill/templates/run-manifest.md`：fresh 的 `base_generated_artifact`、`reused_generated_artifacts` 和 `reused_without_rerun` 必须分别为 `none`、`none`、`[]`。
- `v3/skill/SKILL.md` 的 Fresh run 与 `v3/standards/phase4-pilot-definition.md` 的运行真实性：旧净化正文、source map、候选、audit 和成品不得作为 fresh 输入。

## Expected

`reject`

## 必须保持的行为

只要 fresh 声明复用了任一旧生成产物，运行完整性门就必须失败；稳定标准和历史金标的允许复用不能扩张到生成产物。

## 独立执行

- result: `reject (matched)`
- raw result: `v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n01`
