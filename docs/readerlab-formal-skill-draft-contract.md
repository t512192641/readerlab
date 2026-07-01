# ReaderLab Formal Skill Draft Contract

## Status

This contract defines the gate before a formal ReaderLab Skill draft.

It is not a runnable `SKILL.md`, not a reusable skill package, and not evidence that the transferable method kernel has passed.

Current recorded state after review:

```text
formal_skill_delivery_design_ready: yes
formal_skill_draft_contract_review: pass_no_p0_p1
formal_skill_draft_contract_ready: yes
formal_skill_draft_started: no
skill_draft_not_started
transferable_method_kernel_pass: not_verified
comment_replay_verified: fixture_pass_real_obsidian_ui_deferred
public_external_material_validation_not_started
```

## Purpose

The formal Skill draft may only start after ReaderLab has a contract that keeps four things separate:

- body material that the reader can actually read
- AI companion material that helps the reader understand, question, and discuss
- audit evidence that proves traceability
- human approval that decides whether the next phase is allowed

The Skill must not become a summary generator, a general note-taking template, or a hidden promotion path from local validation to public generalization.

## Skill Input

A future ReaderLab Skill draft must accept one material request with explicit boundaries:

```json
{
  "material_id": "string",
  "title": "string",
  "source_paths": ["file or directory path"],
  "output_root": "target package directory",
  "permission_boundary": "public_ok | private_only | unknown",
  "intended_reader": "string",
  "requested_scope": "whole_package | selected_unit | chapter | file",
  "human_review_required": true
}
```

Required input rules:

- `source_paths` must point to real material or a real source bundle.
- `permission_boundary` must be explicit before any public-facing claim.
- `output_root` must be a preview or package path, not a LifeAtlas permanent sediment area unless the user explicitly approves.
- `human_review_required` must stay true for the first formal draft phase.

Blocked input states:

- source is missing or replaced with sample/mock material without saying so
- permission boundary is unknown but output is reported as public validation
- requested scope is a folder bundle but no unit classification is planned
- user asks for a formal runnable Skill but trace/comment gates have not passed

## Route Decision

The Skill draft must classify the material before generating reader-facing files.

### `book_or_longform`

Use for books, essays, long articles, transcripts, chapters, narrative reports, and longform Markdown.

Body rule:

```text
book_or_longform -> full_body
```

The package must include the complete selected source unit under `10_一手正文/`. AI pages cannot replace the source body.

### `skill_or_engineering_doc`

Use for `SKILL.md`, engineering specs, agent workflow docs, product protocols, code docs, and operational manuals.

Body rule:

```text
skill_or_engineering_doc -> cleaned_body
```

The cleaned body must preserve:

- purpose
- trigger conditions
- user intent
- workflow
- constraints
- failure conditions
- output requirements
- design highlights

Runtime shell, host-specific paths, repeated execution protocol, telemetry, command syntax, and boilerplate may move to audit or appendices. Safety-critical constraints must remain traceable.

### `mixed_material_package`

Use when a folder contains multiple material types, such as source text, templates, scripts, references, and generated examples.

Body rule:

```text
mixed_material_package -> classify_each_unit_then_route
```

The draft must not flatten the folder into one summary. Each meaningful unit must be classified as `book_or_longform`, `skill_or_engineering_doc`, supporting template, supporting script, reference, appendix, or audit-only evidence.

## Required Outputs

Minimum package output:

```text
README.md
source-registry.json
10_一手正文/
20_AI陪读/
audit/
  location-map.json
  trace-to-reader.md
  contracts/
    material-profile.json
    body-track-gate.json
    claim-ledger.json
    candidate-tournament.json
    skillization-gate.json
    annotation-trigger.json
    high-order-explanation.v1.json
    trace-validation.json
  eval.md
```

Additional output for `skill_or_engineering_doc`:

```text
20_AI陪读/design-asset-notes.md
audit/source-cleaning-map.md
```

Additional output for `mixed_material_package`:

```text
audit/unit-classification-map.json
```

Reader-facing outputs must not expose internal field names such as `source refs`, `claim trace`, `lens score`, `machine_status`, `human_status`, `Body Track Gate`, `Claim Ledger`, `Candidate Tournament`, `Skillization Gate`, or `Annotation Trigger`.

## Workflow

The formal draft workflow must follow this state machine:

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

Allowed transitions:

```text
human_review -> revise
human_review -> formal_skill_draft only after explicit user approval
```

Blocked transitions:

```text
candidates_decided -> formal_skill_draft
skillization_checked -> formal_skill_draft
evaluated -> transferable_method_kernel_pass
fixture_replay_validated -> real_obsidian_ui_replay_pass
private/local validation -> public_external_material_validation
```

## Agent / Script Boundary

Scripts may do deterministic work:

- scan source files and collect metadata
- generate source registry skeletons
- generate location-map skeletons with stable locator candidates
- validate JSON contracts
- check anchor, claim, candidate, gate, and replay references
- verify package layout and required files
- run `validate-suite` for trace and fixture replay

Agent judgment must do interpretive work:

- decide material route
- decide what belongs in full body, cleaned body, appendix, or audit
- write body cleaning rationale
- tier claims
- promote, keep, downgrade, or reject candidates
- decide whether a candidate is a future Skill candidate
- write reader-facing AI companion prose
- extract design assets from engineering material
- judge whether eval language overclaims
- prepare the human-review handoff

The script must not decide prose quality, author intent, design insight quality, or human acceptance.

## Gates Before Formal `SKILL.md`

A formal runnable `SKILL.md` may not be created until all gates below pass.

### G1: Delivery Design Gate

Required evidence:

- `docs/readerlab-skill-delivery-spec.md`
- `docs/readerlab-skill-ir-v1.md`
- this contract

Pass condition:

```text
formal_skill_delivery_design_ready: yes
formal_skill_draft_contract_ready: yes
```

### G2: Body Track Gate

Pass condition:

- `book_or_longform` has complete selected body
- `skill_or_engineering_doc` has cleaned body plus cleaning map
- `mixed_material_package` has unit classification before body construction

Failure examples:

- summary replaces source body
- engineering cleaning drops purpose, trigger, workflow, constraints, failure conditions, output requirements, or design highlights
- templates/scripts are treated as primary body without classification

### G3: Trace Validation Gate

Pass condition:

- location anchors exist
- annotation triggers reference real anchors
- reader-facing core paragraphs trace to anchor, claim, and candidate or gate decision
- Skill candidates include trigger, input, steps, output, boundary, and evidence

Current validator command:

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
```

### G4: Comment Replay Fixture Gate

Pass condition:

- at least 2 comments on longform/full-body material
- at least 2 comments on Skill/engineering cleaned-body material
- every replay resolves comment -> anchor -> nearby body -> claim -> candidate -> gate -> bounded AI reply
- reply respects source boundary and does not promote rejected candidates

Current status:

```text
comment_replay_fixture_pass: 1/1
comment_replay_verified: fixture_pass_real_obsidian_ui_deferred
```

This gate is a fixture/storage-format gate, not a real Obsidian UI gate.

### G5: Human Approval Gate

Pass condition:

- reviewer reports no P0/P1 issue
- user explicitly approves entering formal Skill draft

Without this approval, the next allowed state is only:

```text
formal_skill_draft_contract_ready: yes
skill_draft_not_started
```

## Real Obsidian UI Replay

Real Obsidian UI replay is a deferred acceptance item, not a blocker for this contract.

Deferred test shape:

```text
reader creates comments in Obsidian plugin
-> exported/plugin storage preserves anchor
-> Codex reads comment and nearby body
-> Codex resolves body anchor, claim, candidate, and gate decision
-> Codex replies with bounded source-adjacent answer
```

Allowed current claim:

```text
fixture replay passed; real Obsidian UI replay deferred
```

Forbidden current claims:

```text
real Obsidian UI replay passed
comment replay fully verified in Obsidian
annotation loop production-ready
```

## Stop Conditions

Stop immediately if any of these happen:

- creates `SKILL.md`
- creates `.agents/skills/readerlab/`
- marks `formal_skill_draft_started`
- marks `transferable_method_kernel_pass`
- reports private/local validation as public external validation
- reports fixture replay as real Obsidian UI replay
- allows formal Skill draft without explicit human approval
- omits the agent/script boundary
- reader-facing page exposes audit field names
- trace validator cannot connect reader paragraph, anchor, claim, candidate, and gate
- comment replay cannot connect comment, body anchor, claim, candidate, gate decision, and bounded reply

## Verification Commands

Run before reporting this contract as ready:

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
git diff --check
```

If these pass and reviewer has no P0/P1, the main session may update `docs/current-task.md` and `docs/agent-run-ledger.md` to record:

```text
formal_skill_draft_contract_ready: yes
skill_draft_not_started
real_obsidian_ui_replay: deferred
```

It must not record:

```text
formal_skill_draft_started
transferable_method_kernel_pass
public_external_material_validation_pass
real_obsidian_ui_replay_pass
```
