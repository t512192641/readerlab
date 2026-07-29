# C5 · run ledger

> This ledger records deterministic control actions only; it is not a semantic judgment.

- current status: `PRODUCT_READY`
- Expert Agent ID: `019faed9-ec42-7bd0-ba23-511ae1be909d`
- Reviewer Agent ID: `019faedf-5ee5-7f43-9d23-c83d7b295378`
- model: Expert `gpt-5.6-sol`, review `gpt-5.6-terra`; provenance: `controller_declared`
- reasoning: Expert `high`, review `high`; provenance: `controller_declared`
- network: Expert `allowlisted-only`, review `allowlisted-only`; provenance: `controller_declared`
- retries: Expert `no`, review `no`; provenance: `controller_declared`
- Prompt modified: Expert `no`, review `no`; provenance: `controller_declared`
- semantic calls invoked by this Skill: `none`
- external semantic contexts: `controller_declared`
- source access receipts: Expert `raw/expert-source-access.json` (SHA-256 `1144ea14f1d06c29f81055884f7cc6084c7dcf9b85b418cb84719a9abb3ca8cb`), reviewer `acceptance/reviewer-source-access.json` (SHA-256 `42e5301aa1de7a091e69ba60a09a029a12c1a1926a6a6cc7d6d908eabb486cc7`); provenance: `agent_declared`; audit scope: `agent-declared; not a browser or OS-level network audit`
- source boundary: `control/source-boundary.json`; schema: `readerlab-book-expert-teaching/source-boundary/v1`
- archive hash: recorded outside the archive to avoid self-reference

## State transitions

- `NONE` → `EXPERT_OPEN` at `2026-07-29T17:08:47+00:00`
- `EXPERT_OPEN` → `REVIEW_OPEN` at `2026-07-29T17:14:18+00:00`
- `REVIEW_OPEN` → `REVIEW_TERMINAL` at `2026-07-29T17:18:08+00:00`
- `REVIEW_TERMINAL` → `PRODUCT_READY` at `2026-07-29T17:18:15+00:00`
