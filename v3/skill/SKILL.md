---
name: readerlab-v3-book-annotation-seat
description: Generate and judge ReaderLab V3 book-side annotation candidates with audit-backed material cards, example-driven drafting, binary self-checks, and pairwise comparison against calibrated gold examples.
---

# ReaderLab V3 Book Annotation Seat

## Product Expectation

This local Skill draft is for the ReaderLab V3 book annotation seat. It is not a globally installed Codex Skill and must not be copied to global Skill locations without explicit approval.

The honest product promise:

- Guaranteed floor: zero instant-death items and a stable `有用` baseline for mid-tier models.
- Not guaranteed: stable `惊艳` density. Surprise depends on model tier, external knowledge freshness, source richness, and material-card quality.
- Human gate remains required before Phase 1 can close.

## Inputs

Required:

- Source chapter or passage path.
- Clean body anchors; old generated companion blocks must be ignored.
- Calibration example library: `v3/skill/examples/book-annotation-examples.md`.
- Production protocol: `v3/skill/protocols/book-engine.md`.

Optional but recommended:

- Prior calibration log: `v3/standards/calibration-log.md`.
- Prior blind eval files for failure regression.

## Workflow

Follow `v3/skill/protocols/book-engine.md` exactly:

1. Selection pass: identify active anchors and create audit-only material cards. A material card must include 2-3 concrete known facts and a specific connection to the anchor. If the facts cannot be written, reject the material.
2. Drafting pass: generate 2-3 candidates per anchor using only approved material cards. The prompt must embed 2 gold examples and 3 counterexamples from `v3/skill/examples/book-annotation-examples.md`.
3. Self-check pass: run the binary checklist. Every hit is fixed locally and rechecked.
4. Judge by pairwise comparison: candidates compete against the gold examples. The winner goes to the reader sheet; losers and reasons stay in audit.

## Reader-Facing Output

Reader-facing sheets may include only:

- user-facing id
- source file
- anchor quote
- final candidate annotation
- user verdict fields

They must not include:

- internal material cards
- blind-eval notes
- scores
- dark-seed labels
- internal ids
- prompt or protocol terms

## Audit Output

Audit files must preserve:

- material cards
- candidate alternatives
- self-check failures and repairs
- pairwise comparison notes
- dark-seed intent when used

## Stop Conditions

Stop and report instead of proceeding if:

- source anchors are generated companion blocks rather than body text
- material cards cannot establish concrete facts
- all candidates are closer to counterexamples than to gold examples
- user-facing output would expose blind-eval or audit content
- the run would claim Phase 1 closure before user verdicts are returned
