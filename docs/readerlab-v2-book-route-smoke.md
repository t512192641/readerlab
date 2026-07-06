# ReaderLab V2 Book Route Smoke

## Status

This is the Issue #6 book-route smoke. A passing result means a built or installed ReaderLab package can run a small two-chapter book fixture through configuration validation, contract rendering, rendered-package eval, and machine reader-page checks.

It is not full-book acceptance, not production readiness, and not human reader acceptance.

## Run

From the repo root:

```bash
python3 packaging/book_route_smoke_test.py
```

From a built package root:

```bash
python3 tests/book_route_smoke_test.py
```

The smoke verifies:

- configuration uses explicit `source_paths` and `output_root`;
- `material_family` is `book_longform`;
- two declared chapter units remain ordered;
- source body appears before AI companion notes;
- the reader page does not split body, AI explanation, and preset annotation questions into separate reader files;
- machine, reader-evaluation, controller, and human-acceptance states stay separate.

## Scope

This smoke only covers a repo-local, self-contained fixture under `fixtures/book-route-smoke-v0`. It must not be described as `reader_package_pass`, production ready, complete full-book validation, or human acceptance.
