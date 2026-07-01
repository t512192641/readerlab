# ReaderLab Skill IR v0

## Status

This IR evaluates the draft package at `docs/drafts/readerlab-skill-v0/`.

It is not release approval, not installation evidence, and not transferable method validation.

## Owned Job

ReaderLab owns the workflow for turning complex material into a Chinese, body-first, annotatable reading package with:

- a full body or cleaned body track
- AI companion reading support
- design-asset extraction for engineering material
- audit contracts
- annotation triggers
- human review gates

## Trigger Description

The draft `SKILL.md` frontmatter should trigger when the user asks to create a ReaderLab reading package from books, longform material, engineering docs, agent workflow docs, `SKILL.md` files, or mixed folders.

It should not trigger for:

- simple summaries
- generic note cleanup
- ordinary code review
- Skill installation or activation
- permanent LifeAtlas notes
- public benchmark claims

## Workflow Contract

The skill must preserve this workflow:

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

## Resources

Current package resources:

- `SKILL.md`: core instructions and trigger surface.
- `examples/input-request.json`: accepted request shape.
- `examples/route-decision-example.json`: route classification example.
- `checks/readiness-checklist.md`: draft review checklist.
- `evals/trigger-cases.json`: route and near-neighbor trigger cases.
- `evals/output-cases.json`: output quality cases and assertions.

Current external evidence dependencies:

- `docs/readerlab-formal-skill-draft-contract.md`
- `docs/readerlab-skill-ir-v1.md`
- `docs/contracts/location-anchor-v1.md`
- `docs/contracts/trace-validation-v1.md`
- `docs/contracts/comment-replay-v1.md`
- `scripts/readerlab_trace_validator.py`
- `tests/test_readerlab_trace_validator.py`

## Risks

- Trigger may still be broad because ReaderLab overlaps with summary, note cleanup, and Skill authoring.
- Output quality is not model-executed yet; current output eval is assertion design, not live model evidence.
- Real Obsidian UI replay is deferred.
- Current evidence is private/local plus fixture replay, not public external validation.

## Reviewer Gate

Current reviewer answers:

1. What does this skill own? Body-first ReaderLab package production.
2. When should it trigger? Complex material -> ReaderLab reading package.
3. When should it not trigger? Simple summaries, note cleanup, install/activation, public validation claims.
4. Which resources carry behavior? `SKILL.md`, examples, checklist, evals, and existing validator.
5. Which evals prove the contract? Trigger cases, output cases, validator suite, quick skill validation.
6. Which targets can consume the skill without semantic loss? Current draft target only; no activation target is approved.
