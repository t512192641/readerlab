# Body Track Gate v1

## Purpose

`body-track-gate.v1` prevents ReaderLab from calling an explanation-only artifact a complete reading package. It decides whether a book/longform chapter has a first-hand body track before any reader package status can be claimed.

## Required Fields

```json
{
  "contract": "body-track-gate.v1",
  "material_id": "string",
  "material_type": "book_longform | skill_engineering | mixed | unknown",
  "body_track": {
    "status": "present_full_body | present_linked_body | missing | not_applicable",
    "body_path": "string or null",
    "link_target": "string or null",
    "coverage": "full_chapter | partial | excerpt | unknown",
    "notes": "string"
  },
  "allowed_status": "reader_package_pass | skill_engineering_cleaned_body_pass | high_order_explanation_pass | audit_only | fail",
  "blocking_reasons": ["string"],
  "checked_at": "YYYY-MM-DD"
}
```

## Gate Rules

- Book and longform pages can be `reader_package_pass` only when first-hand body exists.
- Skill / engineering materials can be `skill_engineering_cleaned_body_pass` only when a cleaned body exists and preserves purpose, trigger, user intent, workflow, constraints, failure conditions, output requirements, and design highlights.
- First-hand body means either the full chapter body is present in the page or the page explicitly links to the corresponding file under `10_一手正文/`.
- For Skill / engineering materials, cleaned body is the body track; runtime shell, command protocol, machine state, paths, telemetry, and repeated templates may be moved to audit, but safety-critical constraints must remain traceable.
- Explanation-only chapter pages can only be `high_order_explanation_pass`.
- “讲解贴合正文锚点” cannot replace “一手正文存在”.
- If body coverage is `partial`, `excerpt`, or `unknown`, the page cannot be marked `reader_package_pass`.

## Failure Conditions

- `[FAIL]` A book/longform chapter has no first-hand body track but is marked `reader_package_pass`.
- `[FAIL]` A reader-facing page uses AI summary,导读, or high-order explanation as the body track.
- `[FAIL]` A body path or link target is recorded but does not point to a readable body artifact.
- `[FAIL]` Body coverage is unknown and the artifact still claims reader package completion.
- `[FAIL]` A Skill / engineering material claims cleaned-body pass while the cleaned body is only a summary or drops safety-critical workflow constraints without audit trace.
