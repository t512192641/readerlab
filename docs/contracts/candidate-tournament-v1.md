# Candidate Tournament v1

## Purpose

`candidate-tournament.v1` forces ReaderLab to select, downgrade, or reject candidate ideas before writing. It prevents candidate pools from becoming decorative fields that do not affect output decisions.

## Candidate Types

```text
framework
principle
case
counterexample
term
mechanism
transfer_insight
skill_candidate
annotation_trigger
hazard
```

## Required Fields

```json
{
  "contract": "candidate-tournament.v1",
  "material_id": "string",
  "candidates": [
    {
      "candidate_id": "K1",
      "type": "framework | principle | case | counterexample | term | mechanism | transfer_insight | skill_candidate | annotation_trigger | hazard",
      "candidate": "string",
      "claim_refs": ["C1"],
      "v0_source_support": "pass | weak | fail",
      "v1_cross_context": "pass | weak | fail",
      "v2_predictive_or_actionable": "pass | weak | fail",
      "v3_distinctiveness": "pass | weak | fail",
      "risk_check": "pass | caution | fail",
      "decision": "promote | keep | downgrade | reject",
      "decision_reason": "string"
    }
  ],
  "decision_summary": {
    "promoted": 0,
    "kept": 0,
    "downgraded": 0,
    "rejected": 0
  }
}
```

## Gate Rules

- Candidate fields must affect `promote | keep | downgrade | reject`.
- At least one candidate must be downgraded or rejected in a non-trivial chapter probe.
- V1/V2/V3 scores must be reflected in the decision reason.
- Hazards can be promoted only as warnings, not as adoptable methods.

## Failure Conditions

- `[FAIL]` Candidate pool exists but no candidate is rejected or downgraded.
- `[FAIL]` V1/V2/V3 fields do not change decisions.
- `[FAIL]` All candidates are promoted despite weak evidence or clear hazards.
- `[FAIL]` A candidate is promoted into reader-facing narrative without claim refs.
