# ReaderLab Pre-Release Trace Hardening

Date: 2026-07-01

## Scope

This patch addresses pre-release issues found after repo-local activation. It does not change the product direction and does not claim production readiness.

## Changes

- Replaced the active Skill's stale pre-activation boundary with a repo-local trial boundary.
- Split validation guidance into:
  - current package validation: `validate-demo <output_root>`
  - historical regression suite: A/B private demos plus comment replay fixture
- Added `audit/contracts/trace-validation.json` to both private validation demos.
- Upgraded `scripts/readerlab_trace_validator.py` to check `trace-validation.json`.
- Added a negative test proving broken reader paragraph trace fails validation.
- Updated readiness checklists to match repo-local trial status.

## Trace Validation Coverage

The validator now checks that each reader-facing core paragraph in `trace-validation.json` has:

- `reader_ref`
- at least one existing `anchor_ref`
- at least one existing `claim_ref`
- at least one existing `candidate_ref` or `gate_ref`
- `trace_status: complete`

It also checks candidate uses, skill candidate traces, evidence references, `result: pass`, and empty `blocking_reasons`.

## Verification

- `python3 /Users/tianqiang/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/readerlab`: PASS.
- `python3 scripts/readerlab_trace_validator.py validate-demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity`: PASS, 7 reader paragraphs checked.
- `python3 scripts/readerlab_trace_validator.py validate-demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files`: PASS, 6 reader paragraphs checked.
- `python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures`: PASS.
- `python3 tests/test_readerlab_trace_validator.py`: PASS, 3 tests OK.
- `python3 tests/test_readerlab.py`: PASS, 30 tests OK.

## Remaining Non-Claims

- Not production ready.
- Not globally installed.
- Not public external validation.
- Not `transferable_method_kernel_pass`.
- Real Obsidian UI replay remains `pass_with_warning`.
