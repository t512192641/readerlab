# ReaderLab Skill Delivery Spec

## Status

This is a delivery design document, not a formal ReaderLab `SKILL.md`.

Current allowed state:

```text
formal_skill_delivery_design_ready: yes
formal_skill_draft_started: no
transferable_method_kernel_pass: not_verified
comment_replay_verified: not_verified
```

## Purpose

ReaderLab Skill delivery should turn complex material into a Chinese, body-first, annotatable reading package while keeping source evidence, AI explanation, design extraction, and human judgment separated.

The Skill must not behave like a summary generator. Its first responsibility is to preserve or construct the correct body track, then build reader help around that body.

## Material Routes

ReaderLab supports three initial routes:

```text
book_or_longform
skill_or_engineering_doc
mixed_material_package
```

### book_or_longform

Use for books, chapters, essays, long articles, transcripts, and long narrative documents.

Body-track rule:

```text
book_or_longform -> full body track
```

The body must be the complete selected source unit. AI companion pages, summaries, high-order explanations, and annotations cannot replace it.

### skill_or_engineering_doc

Use for `SKILL.md`, engineering specs, code docs, agent workflow docs, product protocols, and operational manuals.

Body-track rule:

```text
skill_or_engineering_doc -> cleaned body track
```

The cleaned body must preserve:

- purpose
- trigger
- user intent
- workflow
- constraints
- failure conditions
- output requirements
- design highlights

Runtime shell, command syntax, path boilerplate, telemetry, repeated templates, and host-specific protocol can move to audit or appendices, but safety-critical constraints must remain traceable.

### mixed_material_package

Use when a folder or source bundle contains multiple material types.

Body-track rule:

```text
mixed_material_package -> classify then route
```

Do not flatten the whole package into one summary. Classify each meaningful unit, select the route, and keep templates, scripts, references, and body material distinct.

## Delivery Workflow

The Skill delivery workflow is:

```text
1. classify material
2. build source-registry
3. build location-map
4. run body-track-gate
5. produce full body / cleaned body
6. build claim-ledger
7. run candidate-tournament
8. run skillization-gate
9. produce annotation-trigger
10. produce reader-facing narrative
11. produce design-asset-notes if engineering material
12. produce trace-to-reader
13. run eval
14. stop for human review
```

The workflow must stop after evaluation. It must not auto-promote a candidate into a formal Skill, LifeAtlas permanent note, or knowledge card without explicit human acceptance.

## Agent / Script Boundary

Scripts can handle deterministic work:

- source scan
- file size, hash, and metadata capture
- package file tree generation
- location-map skeleton generation
- JSON schema validation
- trace chain completeness checks
- package layout checks

Agent judgment must handle interpretive work:

- material type judgment
- body cleaning decisions
- deciding what is body, shell, appendix, or audit
- claim tiering
- candidate promote / keep / downgrade / reject decisions
- Skillization decisions
- annotation trigger quality
- reader-facing narrative
- design asset extraction
- human-review handoff

## Required Outputs

Minimum package shape:

```text
README.md
source-registry.json
10_一手正文/
20_AI陪读/
audit/
  location-map.json
  trace-to-reader.md
  contracts/
    body-track-gate.json
    material-profile.json
    claim-ledger.json
    candidate-tournament.json
    skillization-gate.json
    annotation-trigger.json
    high-order-explanation.v1.json
  eval.md
```

For Skill / engineering materials, also include:

```text
20_AI陪读/design-asset-notes.md
audit/source-cleaning-map.md
```

## Stop Conditions

Do not start a formal ReaderLab Skill draft if any condition holds:

- no trace validator exists
- reader-facing paragraphs cannot trace to claim / candidate / source anchor
- location-map has no stable anchor strategy
- comment replay cannot return from comment to body anchor, claim, candidate, and gate decision
- candidate tournament has no real downgrade or reject
- Skillization promotes insights without trigger / input / steps / output / boundary / evidence
- engineering cleaned body drops purpose, trigger, workflow, constraints, failure conditions, output requirements, or design highlights
- source-cleaning-map cannot explain kept / condensed / moved_to_audit / rejected
- reader-facing exposes internal audit fields
- private/local validation is reported as transferable method pass
- public external validation is claimed before it exists

## Next Design Gate

The next gate is not another large demo. It is:

```text
trace validator design + minimal comment replay fixture
```

Only after those pass should ReaderLab move from delivery design to formal Skill draft.
