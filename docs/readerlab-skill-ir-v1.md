# ReaderLab Skill IR v1

## Status

This is an intermediate representation for designing a future ReaderLab Skill. It is not a runnable Skill manifest and must not be copied into `SKILL.md` without a separate draft phase.

## IR Object

```json
{
  "ir_version": "readerlab-skill-ir.v1",
  "material": {
    "material_id": "string",
    "title": "string",
    "route": "book_or_longform | skill_or_engineering_doc | mixed_material_package",
    "source_paths": ["string"],
    "permission_boundary": "public_ok | private_only | unknown"
  },
  "body_track": {
    "required_mode": "full_body | cleaned_body | classify_then_route",
    "body_paths": ["string"],
    "cleaning_policy": "string or null",
    "body_track_gate_ref": "audit/contracts/body-track-gate.json"
  },
  "location": {
    "location_map_ref": "audit/location-map.json",
    "anchor_policy_ref": "docs/contracts/location-anchor-v1.md"
  },
  "evidence": {
    "source_registry_ref": "source-registry.json",
    "material_profile_ref": "audit/contracts/material-profile.json",
    "claim_ledger_ref": "audit/contracts/claim-ledger.json",
    "candidate_tournament_ref": "audit/contracts/candidate-tournament.json"
  },
  "reader_outputs": {
    "reader_facing_paths": ["20_AI陪读/001_reader-facing.md"],
    "design_asset_paths": ["20_AI陪读/design-asset-notes.md"],
    "annotation_trigger_ref": "audit/contracts/annotation-trigger.json"
  },
  "gates": {
    "skillization_gate_ref": "audit/contracts/skillization-gate.json",
    "trace_validation_ref": "audit/contracts/trace-validation.json",
    "comment_replay_refs": ["audit/comment-replay/*.json"],
    "eval_ref": "audit/eval.md"
  },
  "status": {
    "machine_status": "draft | schema_checked | trace_checked | replay_checked",
    "human_status": "pending | reviewed | accepted | rejected",
    "allowed_next_step": "revise | human_review | skill_delivery_design | formal_skill_draft"
  }
}
```

## Route Rules

### book_or_longform

Required:

- complete selected body under `10_一手正文/`
- `body-track-gate.allowed_status = reader_package_pass` only if full body exists
- reader-facing page explicitly points back to body
- no AI explanation can stand in for the source body

Forbidden:

- summary-as-body
- excerpt-as-full-body
- private/copyrighted source represented as public validation

### skill_or_engineering_doc

Required:

- cleaned body under `10_一手正文/`
- `body-track-gate.allowed_status = skill_engineering_cleaned_body_pass`
- `source-cleaning-map.md`
- `design-asset-notes.md`

Cleaned body must preserve operational spine:

- purpose
- trigger
- user intent
- workflow
- constraints
- failure conditions
- output requirements
- design highlights

Forbidden:

- command shell as main reader body
- host-specific protocol promoted as ReaderLab architecture
- terminology notes replacing design assets

### mixed_material_package

Required:

- classify each meaningful unit before body construction
- keep source body, templates, scripts, references, and audit evidence separate
- route each unit through `book_or_longform` or `skill_or_engineering_doc`

Forbidden:

- flattening a package into a single summary
- treating scripts/templates as body unless they are the primary material being read

## Workflow State Machine

```text
source_selected
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
-> evaluated
-> human_review
```

Allowed transitions:

- `human_review -> revise`
- `human_review -> formal_skill_draft` only after trace validation and comment replay pass

Blocked transitions:

- `candidates_decided -> formal_skill_draft`
- `skillization_checked -> formal_skill_draft`
- `evaluated -> transferable_method_kernel_pass`

## Deterministic Validator Targets

The first validator should check:

- required files exist for the selected route
- JSON contracts parse
- every annotation trigger has an anchor in location-map
- every reader-facing core paragraph has trace coverage
- every promoted candidate has a final use or explicit audit-only reason
- every skill candidate has trigger / input / steps / output / boundary / evidence

It should not try to judge prose quality, claim truth, or design insight quality.
