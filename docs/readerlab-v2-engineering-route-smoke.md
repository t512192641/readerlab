# ReaderLab V2 Skill / Engineering Route Smoke

## Status

This is the Issue #8 Skill / engineering-material route smoke. A passing result means a built or installed ReaderLab package can run a small self-contained engineering fixture through configuration validation, contract rendering, rendered-package eval, machine reader-page checks, asset-card checks, and blocking-controller checks.

It is not complete GSTACK validation, not production readiness, and not human reader acceptance.

## Run

From the repo root:

```bash
python3 packaging/engineering_route_smoke_test.py
```

From a built package root:

```bash
python3 tests/engineering_route_smoke_test.py
```

The smoke verifies:

- configuration uses explicit `source_paths`, `output_root`, and `engineering_source_scope`;
- source coverage closes through `audit/full-source-track.md`;
- the main reader page begins from cleaned first-hand body rather than AI summary;
- the technical explanation page names design structure, failure protection, reuse point, cost, and boundary;
- the asset-card page includes `purpose`, `reader`, `use_boundary`, `selection_rule`, and `first_action`;
- runner structure, Quality Gate request, reader evaluation, blocking controller, and human acceptance stay separate;
- a blocking gate cannot produce `accept` or `limited_accept`;
- the smoke never promotes machine success to production readiness.

## Scope

This smoke only covers a repo-local, self-contained fixture under `fixtures/engineering-route-smoke-v0`. It must not be described as production ready, complete GSTACK validation, or human acceptance.
