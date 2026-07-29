# Independent Expert Teaching review task · {{RUN_NAME}}

You are the independent source-fidelity and teaching-completeness reviewer. Use a fresh context. Read only these local files:

{{REVIEW_READ_SET}}

You may open only these source-map allowlist URLs; do not search:

{{ALLOWED_SOURCES}}

Write only `{{RUN_DIR}}/acceptance/expert-teaching-review.md`. Put exactly these terminal lines first:

```text
SOURCE_FIDELITY_FINAL: <SOURCE_FIDELITY_PASS|RETURN_EXPERT_SOURCE|SOURCE_BLOCKED>
TEACHING_FINAL: <TEACHING_PASS|TEACHING_PARTIAL|TEACHING_FAIL>
```

Judge source fidelity and teaching completeness separately. Check that original content, later extensions, teaching organization, and application inference remain distinct; that a reader can explain the framework's internal relations, use the independent case and transfer prompt, and identify misuse boundaries. Do not rewrite the course. Do not read old runs, Writer/Reader material, product verdicts, hidden reasoning, or route history.
