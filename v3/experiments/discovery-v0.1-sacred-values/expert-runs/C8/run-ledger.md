# C8 · run ledger

> This ledger records deterministic control actions only; it is not a semantic judgment.

- current status: `PRODUCT_READY`
- Expert Agent ID: `019faed9-eccc-76b3-b687-239cf6757471`
- Reviewer Agent ID: `019faedf-5e62-7590-8e29-bd611be07ffb`
- model: Expert `gpt-5.6-sol`, review `gpt-5.6-terra`; provenance: `controller_declared`
- reasoning: Expert `high`, review `high`; provenance: `controller_declared`
- network: Expert `allowlisted-only`, review `allowlisted-only`; provenance: `controller_declared`
- retries: Expert `no`, review `no`; provenance: `controller_declared`
- Prompt modified: Expert `no`, review `no`; provenance: `controller_declared`
- semantic calls invoked by this Skill: `none`
- external semantic contexts: `controller_declared`
- source access receipts: Expert `raw/expert-source-access.json` (SHA-256 `beff1c4cb013633b7bd389a1e892c7d2f0cb244c488c594f435d71f1b20e55eb`), reviewer `acceptance/reviewer-source-access.json` (SHA-256 `38c702e86b85d751198453feab1e480b230ee597805ca9e1cc8b2ccbc6a9eac6`); provenance: `agent_declared`; audit scope: `agent-declared; not a browser or OS-level network audit`
- source boundary: `control/source-boundary.json`; schema: `readerlab-book-expert-teaching/source-boundary/v1`
- archive hash: recorded outside the archive to avoid self-reference

## State transitions

- `NONE` → `EXPERT_OPEN` at `2026-07-29T17:08:47+00:00`
- `EXPERT_OPEN` → `REVIEW_OPEN` at `2026-07-29T17:14:18+00:00`
- `REVIEW_OPEN` → `REVIEW_TERMINAL` at `2026-07-29T17:18:08+00:00`
- `REVIEW_TERMINAL` → `PRODUCT_READY` at `2026-07-29T17:18:15+00:00`
