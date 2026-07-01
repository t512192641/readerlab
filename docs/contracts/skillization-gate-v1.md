# Skillization Gate v1

## Purpose

`skillization-gate.v1` prevents good-sounding insights from being mislabeled as reusable Skills. A candidate can become a Skill candidate only when it has a real trigger, input, steps, output, boundary, and evidence.

## Required Fields

```json
{
  "contract": "skillization-gate.v1",
  "material_id": "string",
  "items": [
    {
      "candidate_ref": "K1",
      "candidate": "string",
      "trigger": "string or null",
      "input": "string or null",
      "steps": ["string"],
      "output": "string or null",
      "boundary": "string or null",
      "evidence": ["string"],
      "decision": "skill_candidate | insight_only | case | reading_note | reject",
      "decision_reason": "string"
    }
  ]
}
```

## Gate Rules

- `skill_candidate` requires all six fields: trigger, input, steps, output, boundary, evidence.
- An insight with no repeatable trigger remains `insight_only`.
- A vivid source episode with no reusable operation remains `case`.
- A dangerous pattern can be recorded as hazard or counterexample, but not as Skill.

## Failure Conditions

- `[FAIL]` An insight is Skillized without trigger/input/steps/output/boundary/evidence.
- `[FAIL]` A heroic, coercive, or crisis-only behavior is promoted as reusable Skill.
- `[FAIL]` Skillization ignores downgraded/rejected decisions from candidate tournament.
