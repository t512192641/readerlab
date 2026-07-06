---
name: readerlab
description: Create Chinese, body-first, annotatable ReaderLab reading packages from complex material such as books, longform articles, Markdown documents, engineering specs, agent workflow docs, SKILL.md files, or mixed source folders. Use when the user asks Codex to turn material into a ReaderLab package with source body or cleaned body, AI companion notes, design-asset extraction, traceable audit contracts, annotation triggers, and human-review gates. Do not use for simple summaries, generic note cleanup, ordinary code review, installing skills, activating reusable assets, or writing permanent LifeAtlas notes.
---

# ReaderLab

## Repo-Local Trial Boundary

This Skill is active only inside this repository at `.agents/skills/readerlab/`.

Do not install it globally or copy it to `/Users/tianqiang/.codex/skills/` without explicit user approval.

Do not claim:

- production readiness
- `transferable_method_kernel_pass`
- public external validation
- real Obsidian UI replay full pass

Real Obsidian UI replay is `pass_with_warning`: real `tandem-comments` plugin storage is readable, but the first UI test selected visible anchor-list entries rather than body prose sentences.

## Startup

Before creating or updating a ReaderLab package, read:

1. The user's request.
2. The material source paths.
3. `docs/readerlab-package-spec.md`.
4. `docs/eval-gates.md`.
5. `docs/product-spec.md` when product boundary is unclear.

Read route-specific contracts only when needed:

- `docs/contracts/location-anchor-v1.md`
- `docs/contracts/trace-validation-v1.md`
- `docs/contracts/comment-replay-v1.md`

## Input

Require one bounded request:

```json
{
  "material_id": "string",
  "title": "string",
  "source_paths": ["string"],
  "output_root": "string",
  "permission_boundary": "public_ok | private_only | unknown",
  "intended_reader": "string",
  "requested_scope": "whole_package | selected_unit | chapter | file",
  "human_review_required": true
}
```

Stop if source paths are missing, output would enter a permanent LifeAtlas area without approval, or permission boundaries are being used to imply public validation.

## Near Neighbors

Do not use this Skill for:

- simple summaries or abstract book reports
- generic Markdown cleanup
- ordinary code review
- Skill installation or activation
- permanent LifeAtlas knowledge-card writing
- public benchmark claims without public material and explicit evidence

If the user only wants a short explanation, answer directly. If the user wants a reusable or installed Skill, stop and ask for explicit activation approval.

## Route

Classify the material before writing reader-facing output.

Use `book_or_longform` for books, chapters, essays, transcripts, long articles, and narrative reports.

- Body mode: `full_body`.
- Preserve the complete selected source unit inside a single annotatable reader page under `10_中文精读/`.
- AI companion pages cannot replace source body.

Use `skill_or_engineering_doc` for `SKILL.md`, engineering specs, code docs, agent workflow docs, product protocols, and operational manuals.

- Body mode: `cleaned_body`.
- Preserve purpose, trigger conditions, user intent, workflow, constraints, failure conditions, output requirements, and design highlights.
- Move runtime shell, repeated templates, host-specific paths, and telemetry into appendices or audit when they are not the reading body.

Use `mixed_material_package` for folders containing multiple material types.

- Body mode: `classify_each_unit_then_route`.
- Classify source body, templates, scripts, references, examples, appendices, and audit-only evidence separately.
- Do not flatten the folder into one summary.

Route tie-breaker:

- Conceptual product specs, strategy docs, essays, and repo-owned longform docs being read as source material default to `book_or_longform`.
- Operational specs, runbooks, code docs, agent workflow protocols, and `SKILL.md` files default to `skill_or_engineering_doc`.
- When unsure, preserve full body first and move cleaning candidates to audit instead of silently removing text.

## Workflow

Follow this state machine:

```text
source_selected
-> permission_boundary_set
-> material_classified
-> body_track_built
-> source_registered
-> location_anchored
-> claims_tiered
-> candidates_decided
-> skillization_checked
-> annotation_questions_built
-> reader_narrative_written
-> trace_validated
-> fixture_replay_validated
-> evaluated
-> human_review
```

## Outputs

Common package shape:

```text
README.md
source-registry.json
10_中文精读/
  001_阅读单元.md
  002_阅读单元.md
audit/location-map.json
audit/trace-to-reader.md
audit/contracts/material-profile.json
audit/contracts/body-track-gate.json
audit/contracts/claim-ledger.json
audit/contracts/candidate-tournament.json
audit/contracts/skillization-gate.json
audit/contracts/annotation-trigger.json
audit/contracts/high-order-explanation.v1.json
audit/contracts/trace-validation.json
audit/eval.md
```

For Obsidian reading, each reader unit must be a single annotatable Markdown page:

```text
# Unit title

source body paragraph

> 陪读：nearby companion note

source body paragraph
```

Do not split one unit into separate body, companion, and comment-question files. The user adds comments directly in the reader page through Obsidian; generated "annotation question" files are not the default ReaderLab surface.

For engineering material, also create:

```text
audit/source-cleaning-map.md
```

For mixed packages, also create:

```text
audit/unit-classification-map.json
```

## Agent And Script Boundary

Use scripts for deterministic checks:

- source path existence and metadata
- JSON parsing
- package layout checks
- location, claim, candidate, gate, and replay reference checks
- trace validator commands

Use agent judgment for interpretive work:

- route decision
- body cleaning decisions
- claim tiering
- candidate promote / keep / downgrade / reject decisions
- reader-facing explanation
- design asset extraction
- human-review handoff

Do not let scripts decide prose quality, author intent, design insight quality, or human acceptance.

## Validation

Before reporting a draft package as ready, run:

```bash
python3 scripts/readerlab_trace_validator.py validate-demo <output_root>
```

Run the historical regression suite separately:

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo tests/fixtures/readerlab/private-material-validation/demos/A_feel_good_productivity --demo tests/fixtures/readerlab/private-material-validation/demos/B_planning_with_files --cases-json tests/fixtures/readerlab/comment-replay/fixtures/comment-replay-cases.json --fixture-dir tests/fixtures/readerlab/comment-replay/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
git diff --check
```

Also inspect reader-facing outputs so internal audit labels are not visible to the reader.

## Stop Conditions

Stop and report if the task would require:

- installing this Skill globally
- writing outside the approved output root
- writing to LifeAtlas permanent zones without approval
- adding dependencies
- treating fixture replay as real Obsidian UI replay
- claiming public or transferable validation
- bypassing human review
