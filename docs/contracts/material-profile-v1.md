# Material Profile v1

## Purpose

`material-profile.v1` records what kind of material ReaderLab is handling before claims, candidates, or reader narrative are generated. It keeps material type, coverage, editing risk, and product role explicit.

## Required Fields

```json
{
  "contract": "material-profile.v1",
  "material_id": "string",
  "title": "string",
  "material_type": "book_longform | skill_engineering | code_docs | transcript | mixed | unknown",
  "source_basis": ["string"],
  "coverage": "full | chapter | partial | sample | toc_only | unknown",
  "body_track_status": "present_full_body | present_linked_body | missing | not_applicable",
  "risks": {
    "translation_or_editing": "low | medium | high | unknown",
    "context_loss": "low | medium | high | unknown",
    "external_verification_needed": true,
    "ai_reconstruction_risk": "low | medium | high | unknown"
  },
  "reader_gap_filled": ["string"],
  "reader_gap_not_filled": ["string"]
}
```

## Gate Rules

- Material type must be set before output evaluation.
- Coverage must not be upgraded by inference. A chapter-level probe is not full-book coverage.
- `reader_gap_not_filled` must include any missing body track, missing external verification, or missing annotation workflow.
- External verification need must be recorded when a claim reaches beyond the source.

## Failure Conditions

- `[FAIL]` Coverage is inflated from chapter/sample to full.
- `[FAIL]` Material type is missing or generic when a material-specific contract should apply.
- `[FAIL]` Known context, translation, or AI reconstruction risks are not recorded.
