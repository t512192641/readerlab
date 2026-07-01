# Product Spec Forward Test v0

## Purpose

This forward test checks whether the draft ReaderLab Skill improves behavior on a repo-owned product specification.

Source:

```text
docs/product-spec.md
```

Why this source is useful:

- It is repo-owned and safe to use.
- It is long enough to require a body-first package, not a short answer.
- It is a boundary case: a product spec could be misrouted as an engineering document, but here it should be treated as longform/conceptual source material because the reader needs the full product contract.

## Artifacts

- `baseline-output.md`: likely output without the draft Skill.
- `with-skill-output.md`: expected output under the draft Skill.
- `comparison.md`: assertion comparison and resulting draft changes.

## Boundary

This is a docs-only forward test. It is not model-executed provider evidence and does not install or activate the Skill.
