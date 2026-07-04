# ReaderLab V2 Runtime Configuration

## Status

This document defines the Issue #4 runtime configuration surface. It is a configuration / structure contract only. It does not claim reader acceptance, production readiness, or a generated clean package.

## Required Fields

ReaderLab runtime commands must not silently fall back to the current developer machine. A run config must provide:

- `source_paths`: user-owned input material paths.
- `output_root`: user-owned output directory root.
- `permission_boundary`: local/user-approved permission boundary. It must not claim public validation or production readiness.
- `material_family`: one of `book_longform`, `longform_report_interview`, or `skill_engineering`.
- `requested_scope`: requested processing scope.
- `human_review_required`: must be `true`.
- `declared_scope`: declared source or route scope.
- `declared_units`: declared unit ids.
- `full_book_required`: whether the route requires full-book coverage.
- `dual_view_required`: whether reader-facing and audit/fact layers are both required.
- `engineering_source_scope`: required only for `skill_engineering`.

## Validation

Validate config shape with:

```bash
python3 scripts/readerlab.py validate-run-config .agents/skills/readerlab/examples/run-config-example.json --no-source-exists-check
```

For a real local run, copy the example config and replace `source_paths` and `output_root` with user-owned paths. Omit `--no-source-exists-check` when validating real paths.

Passing this check means configuration / structure validation only. It is not human reader acceptance and not production readiness.
