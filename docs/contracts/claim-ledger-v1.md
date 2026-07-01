# Claim Ledger v1

## Purpose

`claim-ledger.v1` makes every high-level statement carry an evidence tier before it can influence reader-facing narrative, candidate promotion, or Skillization.

## Claim Tiers

- `direct_source_claim`: Directly supported by the source chapter or body artifact.
- `composite_interpretation`: AI synthesis across multiple source details; must not be written as author intent.
- `external_analogy`: External model, analogy, or comparison used to illuminate the source.
- `needs_verification`: Plausible but not established by the current source; cannot be presented as fact.

## Required Fields

```json
{
  "contract": "claim-ledger.v1",
  "material_id": "string",
  "claims": [
    {
      "claim_id": "C1",
      "claim": "string",
      "tier": "direct_source_claim | composite_interpretation | external_analogy | needs_verification",
      "anchor_ref": "string",
      "allowed_reader_use": "state_as_source | explain_as_interpretation | use_as_lens | keep_internal",
      "risk": "string",
      "decision": "promote | keep | downgrade | reject"
    }
  ]
}
```

## Gate Rules

- High-level claims must have a tier.
- `composite_interpretation` can support a reader explanation only when phrased as interpretation.
- `external_analogy` can enter reader-facing narrative only when it reversely clarifies source meaning.
- `needs_verification` must remain internal or be explicitly framed as unverified.

## Failure Conditions

- `[FAIL]` A high-level claim has no tier.
- `[FAIL]` A composite interpretation is written as author intent.
- `[FAIL]` An external analogy is promoted without source-facing explanatory value.
- `[FAIL]` A `needs_verification` claim appears as confirmed fact in reader-facing output.
