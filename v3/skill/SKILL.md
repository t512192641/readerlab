---
name: readerlab-v3
description: Produce ReaderLab V3 reading packages with body-first source pages, strict book annotation filtering, skill-engineering interpretation, asset candidates, and audit-separated quality gates.
---

# ReaderLab V3

## Boundary

This is a repo-local draft Skill for ReaderLab V3. Do not install or copy it to global Skill locations without explicit approval.

ReaderLab V3 turns complex material into Chinese reading packages for LifeAtlas and Obsidian. It keeps source text first, puts AI help beside it, and keeps audit evidence outside reader pages.

## Product Rule

Visible means selected. A book-side annotation below `有用` must not appear on a reader page. If no annotation survives, deliver an active-point list instead: anchor, why it is worth annotating, and material clues. A short honest list beats a page of 60-point notes.

## Run Modes

- Mid-tier mode: run mechanical coverage fully, publish only strictly selected annotations, and fill gaps with active-point lists.
- Strong-tier mode: run the full annotation seat with richer material cards, 5-7 routes per anchor, and a broader expert seat.
- Quality note: zero instant-death items and no visible low-value notes are the promise. Stable `惊艳` density depends on model tier, source richness, and material depth.

## Inputs

Required:

- Source material path.
- Material type: book or longform, or Skill and engineering material.
- Clean source body. Old generated companion blocks, command wrappers, and audit logs are not source anchors.
- Asset-layer ledgers from `v3/asset-layer/`, if already confirmed by the user.

Recommended:

- Book protocol: `v3/skill/protocols/book-engine.md`.
- Skill protocol: `v3/skill/protocols/skill-engine.md`.
- Judge protocol: `v3/skill/protocols/judge.md`.
- Example library: `v3/skill/examples/`.
- Reader templates: `v3/skill/templates/`.

## Routing

Use the book engine when the source is a book chapter, long article, essay, transcript, or other reading-first material.

Use the Skill engine when the source is an agent Skill, workflow, engineering method, script-backed process, architecture note, or code-heavy operational package.

Mixed materials keep two tracks: body-first reading pages for the human-readable source, and technical lead pages for mechanisms, tradeoffs, data flow, and reusable design assets.

## Workflow

1. Read the relevant asset ledgers, but do not write back to them during generation.
2. Normalize the source into a body-first reading unit.
3. Route to the book engine or Skill engine.
4. Produce audit-only evidence: material cards, candidate alternatives, self-check records, cold-start records, and judge notes.
5. Run the judge protocol.
6. Assemble reader pages from templates.
7. Put new tools, reading moves, open questions, and asset cards into the package's distillation candidate section only.
8. Wait for user confirmation before writing any durable LifeAtlas ledger.

## Book Output

Reader-facing book pages may include:

- chapter title and source path
- source body or anchor cluster
- surviving annotations only
- active-point list when annotations do not survive
- distillation candidate links

They must not include:

- material cards
- blind evaluations
- scores
- dark-seed labels
- prompt text
- internal ids
- protocol terms

## Skill Output

Reader-facing Skill pages must separate:

- source body: cleaned source text that preserves purpose, trigger, flow, constraints, outputs, and failure conditions
- product interpretation: why the workflow exists and what problem it solves
- technical interpretation: how it works, why it is designed this way, and what would break if simplified
- reusable assets: cards that can stand alone for a cold-start agent

## Stop Conditions

Stop and report instead of publishing reader pages if:

- the only available anchors are generated companion blocks
- facts for a material card cannot be written clearly
- book annotations all lose to calibrated gold examples
- Skill asset cards cannot pass cold-start standards
- reader pages would expose audit or calibration material
- the run would claim Phase closure before user verdicts return
