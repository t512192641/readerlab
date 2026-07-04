# ReaderLab V2 Install Smoke

## Status

This is the Issue #5 install and discovery smoke. A passing result means a built ReaderLab shareable package can be copied into a clean Skill target, discovered by its `SKILL.md` entry, and run a minimal configuration command.

It is not reader acceptance, not production readiness, and not a three-route material smoke.

## Build A Package

```bash
python3 scripts/build_readerlab_package.py --output-dir <package-build-output-dir> --force
```

## Run Install Smoke

Use a clean temporary Skill root. Do not point this smoke at `~/.codex/skills` unless the user has explicitly approved a real install.

```bash
python3 packaging/install_smoke_test.py \
  --package-root <package-build-output-dir>/readerlab \
  --install-root <clean-temporary-skill-root> \
  --force
```

The smoke verifies:

- install: the package can be copied to `<install-root>/readerlab`;
- discovery: `<install-root>/readerlab/SKILL.md` has `name: readerlab` and a readable description;
- command: the installed package passes `tests/package_smoke_test.py`;
- config: the installed package can run `scripts/readerlab.py validate-run-config examples/run-config-example.json --no-source-exists-check`.

Failures report `failed_phase` as `install`, `discovery`, `command`, or `config`.

For an explicitly approved real local install smoke, pass `--allow-global-codex-skills`. Do not use that flag for routine PR verification.

## Scope

This smoke only proves installation shape, discovery shape, package boundary structure, and minimal runtime-config validation. It does not prove output quality or user-facing reading quality.
