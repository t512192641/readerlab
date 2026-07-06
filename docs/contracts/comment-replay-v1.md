# Comment Replay Contract v1

## Purpose

`comment-replay.v1` verifies that a reader annotation can return to nearby body text, related claims, candidate decisions, gate outcomes, and a bounded AI reply.

It tests the ReaderLab annotation loop without requiring immediate Obsidian UI automation.

## Required Fields

```json
{
  "contract": "comment-replay.v1",
  "material_id": "string",
  "replays": [
    {
      "replay_id": "CR1",
      "comment": {
        "comment_id": "string",
        "comment_text": "string",
        "comment_source": "mock | obsidian_export | markdown_comment | plugin_export",
        "anchor_ref": "A-BODY-001"
      },
      "context": {
        "body_path": "string",
        "nearby_body_excerpt_ref": "string",
        "location_anchor_ref": "A-BODY-001",
        "claim_refs": ["C1"],
        "candidate_refs": ["K1"],
        "gate_refs": ["body-track-gate", "candidate-tournament"]
      },
      "reply": {
        "reply_text": "string",
        "reply_mode": "explain | challenge | connect | boundary | verify",
        "source_boundary_respected": true,
        "does_not_claim_author_intent_without_evidence": true,
        "does_not_promote_rejected_candidate": true
      },
      "result": "pass | fail",
      "blocking_reasons": ["string"]
    }
  ],
  "checked_at": "YYYY-MM-DD"
}
```

## Minimal Replay Fixture

Before a formal Skill draft, run at least four replay fixtures:

```text
2 comments on a longform/full-body material
2 comments on a Skill/engineering cleaned-body material
```

Each replay must show:

- comment text
- comment anchor
- nearby body text reference
- related claim
- related candidate
- gate decision
- AI reply
- boundary check

## Replay Rules

- The reply must use nearby body context, not only the user's comment.
- The reply must respect claim tiers.
- The reply must not turn composite interpretation into author intent.
- The reply must not promote rejected or downgraded candidates as if they passed.
- The reply must answer in the requested `reply_mode`.
- The reply must be source-adjacent and should not drift into a generic coaching answer.

## Failure Conditions

- `[FAIL]` Comment cannot resolve to a location anchor.
- `[FAIL]` Location anchor cannot resolve to nearby body or cleaned body.
- `[FAIL]` Replay cannot find related claim or candidate decision.
- `[FAIL]` Reply ignores gate decisions.
- `[FAIL]` Reply presents AI interpretation as source fact.
- `[FAIL]` Reply promotes a rejected candidate.
- `[FAIL]` Replay passes without source boundary checks.

## Obsidian Boundary

The current assumption is Obsidian plus an existing annotation plugin. This contract does not replace that plugin.

The first validation can use mock or exported comments. UI automation is not required for the first pass. The purpose is to prove that ReaderLab can map:

```text
comment -> anchor -> nearby body -> claim -> candidate -> gate -> bounded reply
```
