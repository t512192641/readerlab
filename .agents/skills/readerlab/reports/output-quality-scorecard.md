# ReaderLab Draft Output Quality Scorecard v0

## Status

This scorecard is assertion-design evidence, not model-executed evidence.

No provider-backed run has been executed. No blind A/B review has been performed.

## Cases

| Case | Baseline risk | With-skill expected improvement | Status |
| --- | --- | --- | --- |
| O1 longform body-first | Summary replaces body | Requires `10_一手正文/`, trace validation, human review | designed |
| O2 engineering cleaned body | Boilerplate or over-summary | Requires cleaned body essentials, design assets, cleaning map | designed |
| O3 mixed package classification | Folder flattened into summary | Requires unit classification before body construction | designed |
| O4 product spec route tie-breaker | Conceptual spec misrouted as engineering cleanup | Defaults conceptual product specs to full body | forward-tested |

## Assertion Coverage

Covered:

- required package paths
- route-specific body requirements
- audit contract requirements
- human review boundary
- forbidden overclaims

Not yet covered:

- model-executed with-skill output
- baseline output capture
- blind A/B review
- real Obsidian UI replay

## Current Decision

Status: `warn`

Reason: the draft has useful output assertions and one local forward test, but no provider-backed model-executed output comparison yet.

Recommended next fix:

Run a second forward test on a Skill/engineering source before any activation decision.
