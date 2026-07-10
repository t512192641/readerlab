---
id: RI-N02
kind: derived-structure
line: run-integrity
freeze_status: frozen
historical_run: false
independent_execution_result: reject-matched
future_raw_result_path: v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n02
---

# RI-N02：fresh 覆盖或混写旧输出

这是由当前运行合同派生的结构测试，不是历史运行，也不证明发生过 fresh run。

## 最小运行场景输入

```yaml
run_id: fixture-ri-n02
status: running
mode: fresh
reuse:
  base_generated_artifact: none
  reused_generated_artifacts: none
  reused_without_rerun: []
output:
  new_isolated_directory: /fixtures/runs/existing-readerlab-output
  preexisting: true
  writes_to_previous_run: true
```

## 规范依据

- `v3/skill/templates/run-manifest.md`：fresh 必须使用本次唯一的新隔离目录，且不得写入旧 run。
- `v3/standards/phase4-pilot-definition.md` 的运行真实性：不得覆盖、混写或就地修补旧输出。

## Expected

`reject`

## 必须保持的行为

目录已存在或会写入上一轮，任一项成立都必须拒绝 fresh；文件名变化不能替代 run 级隔离。

## 独立执行

- result: `reject (matched)`
- raw result: `v3/eval/constraint-redesign-r2/regression-run-integrity-rerun-9-raw.md#ri-n02`
