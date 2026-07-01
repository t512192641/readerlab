# Demo B Trace to Reader

This file is audit-only. It explains how the reader-facing prose consumes the cleaned body, claim ledger, candidate tournament, and Skillization decisions. It is not intended for `20_AI陪读/`.

## Segment B-READ-001

Reader-facing role: tells the reader that the main issue is not the command shell, but how the Skill protects a vague request from becoming a distorted backlog item.

- Body anchors: `B-BODY-001`, `B-BODY-003`
- Claims: `C1`, `C3`
- Candidates: `K2` kept, `K3` promoted
- Decision effect: the page explicitly downgrades runtime shell as the main reading body.

## Segment B-READ-002

Reader-facing role: explains that writing an issue is the result, while protecting user decision quality is the deeper method.

- Body anchors: `B-BODY-001`, `B-BODY-002`
- Claims: `C2`, `C6`
- Candidates: `K1` promoted, `K7` promoted
- Decision effect: the page treats this as ReaderLab interpretation, not a claim that the source author stated this wording.

## Segment B-READ-003

Reader-facing role: describes the workflow from why, scope, evidence, draft review, gates, to backlog-ready handoff.

- Body anchors: `B-BODY-002`, `B-BODY-004`
- Claims: `C6`, `C7`
- Candidates: `K1` promoted, `K7` promoted
- Decision effect: the page keeps the operational spine rather than reducing the source to "a Skill that writes issues."

## Segment B-READ-004

Reader-facing role: identifies structured decision questions as a reusable design pattern, but keeps it scoped to real decisions.

- Body anchors: `B-BODY-003`, `B-BODY-005`
- Claims: `C5`
- Candidates: `K5` downgraded
- Decision effect: the reader page can discuss the pattern, but it does not turn it into a formal ReaderLab Skill.

## Segment B-READ-005

Reader-facing role: rejects overfitting ReaderLab to gstack runtime shell, telemetry, routing, and host-specific paths.

- Body anchors: `B-BODY-003`, `B-BODY-004`
- Claims: `C3`, `C8`
- Candidates: `K3` promoted as cleaning rule, `K4` rejected
- Decision effect: the page says these details are useful as a case of long-running tool state, not as ReaderLab defaults.

## Annotation Re-read Path

The Obsidian plugin can store a comment near a Markdown body paragraph. ReaderLab's remaining responsibility is to map that comment back to a stable body anchor, then recover the relevant claim tier, candidate decision, Skillization result, and reply mode. `location-map.json` and `annotation-trigger.json` now provide that bridge for Demo B.
