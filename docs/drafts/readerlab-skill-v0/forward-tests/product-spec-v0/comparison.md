# Forward Test Comparison

## Result

Status: `pass_with_warning`

The draft Skill improves the output shape: it prevents a generic summary from replacing the source body and forces route selection, package shape, audit separation, and human review.

## Assertions

| Assertion | Baseline | With draft Skill |
| --- | --- | --- |
| Preserve source body | fail | pass |
| Select material route first | fail | pass |
| Require `10_一手正文/` | fail | pass |
| Separate reader-facing and audit | partial | pass |
| Avoid public/transferable overclaim | partial | pass |
| Human review remains required | partial | pass |

## Warning Found

The draft Skill originally listed product protocols and engineering specs under `skill_or_engineering_doc`, which could misroute `docs/product-spec.md` into `cleaned_body`.

For conceptual product specs, strategy docs, and repo-owned longform docs with no runtime shell or host-specific boilerplate, the safer default is:

```text
book_or_longform -> full_body
```

Use `skill_or_engineering_doc` only when the material is operational, procedural, code/agent workflow oriented, or contains execution shell that needs cleaning.

## Required Draft Fix

Add a route tie-breaker to `SKILL.md`:

- conceptual specs and strategy docs being read as source material default to `book_or_longform`
- operational specs, workflow protocols, runbooks, code docs, and `SKILL.md` default to `skill_or_engineering_doc`
- when unsure, preserve full body first and put cleaning candidates in audit rather than silently removing text
