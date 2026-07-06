# Location Anchor Contract v1

## Purpose

`location-anchor.v1` defines stable anchors for ReaderLab body text, cleaned body text, reader-facing paragraphs, claims, candidates, annotation triggers, and future comment replay.

Its purpose is to make annotation and audit replay possible without relying only on fragile line numbers or informal headings.

## Required Fields

```json
{
  "contract": "location-anchor.v1",
  "material_id": "string",
  "anchors": [
    {
      "anchor_id": "string",
      "anchor_type": "body_block | cleaned_body_block | reader_paragraph | source_section | appendix_block",
      "path": "string",
      "locator": {
        "line_start": 1,
        "line_end": 1,
        "heading": "string or null",
        "paragraph_index": 1,
        "block_hash": "string or null"
      },
      "role": "string",
      "source_refs": ["string"],
      "claim_refs": ["C1"],
      "candidate_refs": ["K1"],
      "annotation_refs": ["A1"]
    }
  ],
  "checked_at": "YYYY-MM-DD"
}
```

## Anchor Rules

- Every body-adjacent annotation trigger must reference an anchor.
- Every reader-facing core paragraph must have an anchor or a trace entry that references an anchor.
- For longform material, anchors should use paragraph-level IDs where possible, not only headings.
- For Skill / engineering material, anchors must distinguish cleaned body from runtime shell, appendices, templates, and audit-only source sections.
- A line range is acceptable for demo review, but formal Skill draft requires at least one stable locator beyond a line range:
  - paragraph index
  - block hash
  - explicit block id
  - source section id

## Failure Conditions

- `[FAIL]` Annotation trigger has no body/source anchor.
- `[FAIL]` Reader-facing paragraph cannot be traced to any anchor.
- `[FAIL]` Anchor points to an AI explanation when it claims to point to source body.
- `[FAIL]` Skill / engineering anchor cannot distinguish cleaned body from host-specific runtime shell.
- `[FAIL]` Formal Skill draft uses only unstable natural-language anchor descriptions.

## Minimum Demo Acceptance

For demo-level review:

```text
anchor_id + path + line range or heading + claim/candidate/annotation refs
```

For formal Skill draft:

```text
anchor_id + path + paragraph/block locator + block hash or explicit block id + trace refs
```
