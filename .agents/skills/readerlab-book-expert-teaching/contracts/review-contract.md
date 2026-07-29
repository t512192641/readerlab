# Independent review contract

The reviewer runs in a fresh context and reads only the frozen original, framework, source map, Expert course, Expert source map, and review task. The reviewer must not read old runs, Writer/Reader material, product verdicts, hidden reasoning, or route history.

Review two dimensions independently:

## Source fidelity

Check distortion of the framework, later extensions presented as original, teaching organization presented as a formal method, application inference presented as literature fact, and missing boundaries. The terminal is exactly one of:

- `SOURCE_FIDELITY_PASS`
- `RETURN_EXPERT_SOURCE`
- `SOURCE_BLOCKED`

## Teaching completeness

Judge whether a normal reader can restate the core problem/distinction, explain internal relations, understand the independent case, use the framework on another problem, and recognize major misuse boundaries. The terminal is exactly one of:

- `TEACHING_PASS`
- `TEACHING_PARTIAL`
- `TEACHING_FAIL`

The reviewer must put both terminal lines first and must not rewrite the course. Only the pair `SOURCE_FIDELITY_PASS + TEACHING_PASS` can proceed to a product package.
