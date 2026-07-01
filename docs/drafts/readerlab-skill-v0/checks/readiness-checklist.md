# ReaderLab Skill Repo-Local Readiness Checklist

Use this checklist before treating `.agents/skills/readerlab/SKILL.md` as repo-local trial ready.

## Repo-Local Boundary

- [ ] Active package remains under `.agents/skills/readerlab/`.
- [ ] Draft record remains under `docs/drafts/readerlab-skill-v0/`.
- [ ] Skill states that it is repo-local only.
- [ ] Skill is not installed globally under `/Users/tianqiang/.codex/skills/`.
- [ ] Skill does not claim production readiness.
- [ ] Draft does not claim transferable method pass.
- [ ] Draft does not claim public external validation.
- [ ] Skill says real Obsidian UI replay is `pass_with_warning`.

## Skill Metadata

- [ ] `SKILL.md` has only `name` and `description` in YAML frontmatter.
- [ ] `name` is lowercase hyphen-compatible.
- [ ] `description` says what the Skill does and when to use it.

## ReaderLab Contract

- [ ] Input request requires source paths, output root, permission boundary, requested scope, intended reader, and human review.
- [ ] Route decision covers `book_or_longform`, `skill_or_engineering_doc`, and `mixed_material_package`.
- [ ] Near-neighbor prompts are covered by `evals/trigger-cases.json`.
- [ ] Output assertions are covered by `evals/output-cases.json`.
- [ ] Product spec forward test is recorded in `forward-tests/product-spec-v0/`.
- [ ] Skill IR is recorded in `reports/skill-ir.md`.
- [ ] Review status is recorded in `reports/review-studio.md`.
- [ ] Book and longform route preserves the complete selected body.
- [ ] Skill and engineering route preserves cleaned body essentials.
- [ ] Mixed package route classifies each meaningful unit before writing body.
- [ ] Output checklist matches `docs/readerlab-formal-skill-draft-contract.md`.
- [ ] Required package shape includes `audit/contracts/trace-validation.json`.
- [ ] `trace-validation.json` maps reader-facing core paragraphs to anchors, claims, and candidates or gates.
- [ ] Agent/script boundary is explicit.
- [ ] Human review remains required.

## Validation Commands

Run:

```bash
python3 scripts/readerlab_trace_validator.py validate-demo <output_root>
```

Run historical regression separately:

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
git diff --check
```

Manual checks:

- [ ] Reader-facing pages keep internal audit labels out of the visible reading page.
- [ ] Fixture replay is not reported as real Obsidian UI replay.
- [ ] Private/local validation is not reported as public external validation.
