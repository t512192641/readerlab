# ReaderLab V2 Longform / Report / Interview Route Smoke

## Status

This is the Issue #7 longform / report / interview route smoke. A passing result means a built or installed ReaderLab package can run a small mixed report-and-interview fixture through configuration validation, contract rendering, rendered-package eval, and machine reader-page checks.

It is not full-material acceptance, not production readiness, and not human reader acceptance.

## Run

From the repo root:

```bash
python3 packaging/longform_route_smoke_test.py
```

From a built package root:

```bash
python3 tests/longform_route_smoke_test.py
```

The smoke verifies:

- configuration uses explicit `source_paths` and `output_root`;
- `material_family` is `longform_report_interview`;
- intake contracts declare material type, source scope, context gaps, and segmentation logic;
- declared reading units match the catalog order;
- units are organized by argument structure, evidence group, and interview turn rather than fixed length or file order;
- first-hand body appears before AI companion notes;
- companion notes point to a concrete reading problem near the body;
- structure contract, runner, Quality Gate request, reader evaluation, controller, and human acceptance stay separate.

## Scope

This smoke only covers a repo-local, self-contained fixture under `fixtures/longform-route-smoke-v0`. It must not be described as `reader_package_pass`, production ready, complete report/interview validation, or human acceptance.
