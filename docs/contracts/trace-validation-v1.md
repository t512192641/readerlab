# Trace Validation Contract v1

## Purpose

`trace-validation.v1` makes ReaderLab prove that reader-facing prose is constrained by source evidence, candidate decisions, and gate outcomes.

It is a deterministic completeness check. It does not judge whether the prose is good; it checks whether the prose is traceable.

## Required Fields

```json
{
  "contract": "trace-validation.v1",
  "material_id": "string",
  "reader_paragraphs": [
    {
      "reader_ref": "R1",
      "reader_path": "20_AI陪读/001_reader-facing.md",
      "paragraph_role": "string",
      "anchor_refs": ["A-BODY-001"],
      "claim_refs": ["C1"],
      "candidate_refs": ["K1"],
      "gate_refs": ["body-track-gate", "candidate-tournament"],
      "final_use": "reader_facing | design_asset | annotation_trigger | skill_candidate | audit_only",
      "trace_status": "complete | partial | missing",
      "notes": "string"
    }
  ],
  "candidate_uses": [
    {
      "candidate_ref": "K1",
      "decision": "promote | keep | downgrade | reject",
      "final_use": ["reader_facing", "design_asset", "annotation_trigger", "skill_candidate", "audit_only"],
      "reader_refs": ["R1"],
      "reason": "string"
    }
  ],
  "skill_candidate_traces": [
    {
      "candidate_ref": "K1",
      "has_trigger": true,
      "has_input": true,
      "has_steps": true,
      "has_output": true,
      "has_boundary": true,
      "has_evidence": true,
      "evidence_refs": ["C1", "A-BODY-001"],
      "trace_status": "complete | partial | missing"
    }
  ],
  "result": "pass | fail",
  "blocking_reasons": ["string"],
  "checked_at": "YYYY-MM-DD"
}
```

## Validation Rules

Every reader-facing core paragraph must map to:

- at least one body/source anchor
- at least one claim id
- at least one candidate id or gate decision

Every promoted candidate must map to at least one final use:

- reader-facing
- design asset
- annotation trigger
- skill candidate
- audit-only with explicit reason

Every downgraded or rejected candidate must remain visible in audit and must not reappear as an unbounded reader-facing recommendation.

Every skill candidate must map to:

- trigger
- input
- steps
- output
- boundary
- evidence

## Failure Conditions

- `[FAIL]` Reader-facing core paragraph has no source/body anchor.
- `[FAIL]` Reader-facing core paragraph has no claim id.
- `[FAIL]` Reader-facing core paragraph has no candidate or gate decision.
- `[FAIL]` Promoted candidate has no final use.
- `[FAIL]` Rejected candidate appears as a positive reader-facing recommendation.
- `[FAIL]` Skill candidate lacks trigger / input / steps / output / boundary / evidence.
- `[FAIL]` Trace file is manually descriptive but cannot be machine-checked.

## Initial Validator Scope

The first script should only check completeness and references:

```text
reader_ref exists
anchor_refs exist in location-map
claim_refs exist in claim-ledger
candidate_refs exist in candidate-tournament
skill candidates satisfy six-field completeness
annotation trigger anchors exist
```

It should not judge the truth of claims or the quality of the reader-facing prose.
