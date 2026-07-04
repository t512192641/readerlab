# ReaderLab V2 Package Build

## Status

This is the Issue #3 package build path. A passing build produces a `shareable_package_prepared` package candidate only. It does not mean installation smoke passed, reader quality passed, or ReaderLab V2 is production ready.

## Build

```bash
python3 scripts/build_readerlab_package.py --output-dir /private/tmp/readerlab-package-smoke --force
```

The command creates:

```text
readerlab/
  SKILL.md
  checks/
  evals/
  examples/
  scripts/
  docs/
  contracts/
  fixtures/
  tests/
  PACKAGE_BOUNDARY.md
  PACKAGE_AUDIT.json
  PACKAGE_MANIFEST.json
```

## Verify The Built Package

```bash
python3 /private/tmp/readerlab-package-smoke/readerlab/tests/package_smoke_test.py
```

The package smoke checks only package boundary structure and audit status. It is not reader acceptance and not production readiness.

## Boundary

The builder copies only files listed in `packaging/readerlab-package-manifest.json`, sanitizes selected package-facing docs, and fails the build if package audit finds forbidden machine paths, excluded fixture commands, reports, private demos, experiment reports, or GSTACK source paths.
