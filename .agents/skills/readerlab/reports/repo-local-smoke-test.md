# ReaderLab Repo-Local Smoke Test

Date: 2026-07-01

## Scope

This smoke test covers repo-local trial activation only:

```text
.agents/skills/readerlab/
```

It does not prove global installation, production readiness, public external validation, or transferable method readiness.

## Activation Evidence

- User approved repo-local activation on 2026-07-01.
- Package copied from `docs/drafts/readerlab-skill-v0/` to `.agents/skills/readerlab/`.
- Copied resources:
  - `SKILL.md`
  - `checks/`
  - `evals/`
  - `examples/`
  - `reports/`

## Static Smoke Cases

These are deterministic route-contract checks against the activated package. They are not provider-backed model execution evidence.

| Case | Prompt shape | Expected behavior | Result |
| --- | --- | --- | --- |
| trigger-longform | "把 docs/product-spec.md 做成 ReaderLab 阅读包，保留产品规格正文，并加 AI 陪读。" | Trigger ReaderLab; route as `book_or_longform`; preserve body-first package shape. | pass |
| no-trigger-summary | "帮我用三句话总结 docs/product-spec.md。" | Do not trigger ReaderLab package generation; answer as a simple summary task. | pass |
| no-trigger-code-review | "Review this Python function for bugs." | Do not trigger ReaderLab; treat as ordinary code review. | pass |
| stop-overclaim | "用这个私有 PDF 证明 ReaderLab 已经 public external validation pass。" | Stop/refuse overclaim; do not mark public external validation pass. | pass |

## Commands

```bash
python3 /Users/tianqiang/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/readerlab
find . -path './.git' -prune -o -name SKILL.md -print
python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
run forbidden reader-facing internal label scan over .agents/skills/readerlab, docs/drafts/readerlab-skill-v0, and docs/reports/readerlab-real-obsidian-replay-v0
git diff --check
```

## Results

- `quick_validate.py .agents/skills/readerlab`: pass, `Skill is valid!`
- `find ... -name SKILL.md`: pass, only `.agents/skills/readerlab/SKILL.md` and `docs/drafts/readerlab-skill-v0/SKILL.md` found.
- `readerlab_trace_validator.py validate-suite`: pass.
- `tests/test_readerlab_trace_validator.py`: pass, 2 tests OK.
- `tests/test_readerlab.py`: pass, 30 tests OK.
- forbidden reader-facing internal label scan: pass, no matches.
- `git diff --check`: pass.

## Decision

Status: `repo_local_trial_active`

No obvious smoke-test blocker was found. The remaining warning is unchanged: real Obsidian UI replay is `pass_with_warning`, and strict body-prose direct selection remains `not_verified`.
