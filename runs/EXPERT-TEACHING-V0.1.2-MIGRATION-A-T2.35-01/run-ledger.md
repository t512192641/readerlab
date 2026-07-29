# EXPERT-TEACHING-V0.1.2-MIGRATION-A-T2.35-01 · run ledger

> This ledger records deterministic control actions only; it is not a semantic judgment.

- current status: `PRODUCT_READY`
- Expert Agent ID: `019fae15-dac4-7bd1-bf48-5c494b0c73e1`
- Reviewer Agent ID: `019fae20-11bb-7c52-be0b-31521d244e52`
- model: Expert `gpt-5.6-sol`, review `gpt-5.6-terra`; provenance: `controller_declared`
- reasoning: Expert `high`, review `high`; provenance: `controller_declared`
- network: Expert `allowlisted-only`, review `allowlisted-only`; provenance: `controller_declared`
- retries: Expert `no`, review `no`; provenance: `controller_declared`
- Prompt modified: Expert `no`, review `no`; provenance: `controller_declared`
- semantic calls invoked by this Skill: `none`
- external semantic contexts: `controller_declared`
- source access receipts: Expert `raw/expert-source-access.json` (SHA-256 `c22e795f8adb1584d9cbf62feb8b9321faaf3dfda6e890bf0da50608604a9e7c`), reviewer `acceptance/reviewer-source-access.json` (SHA-256 `c6bd78bf94af36ca7c2327a2e231d117fa59bdbd5ef917fdf96db29a0f956906`); provenance: `agent_declared`; audit scope: `agent-declared; not a browser or OS-level network audit`
- source boundary: `control/source-boundary.json`; schema: `readerlab-book-expert-teaching/source-boundary/v1`
- archive hash: recorded outside the archive to avoid self-reference

## State transitions

- `NONE` → `EXPERT_OPEN` at `2026-07-29T13:30:45+00:00`
- `EXPERT_OPEN` → `REVIEW_OPEN` at `2026-07-29T13:45:45+00:00`
- `REVIEW_OPEN` → `REVIEW_TERMINAL` at `2026-07-29T13:47:35+00:00`
- `REVIEW_TERMINAL` → `PRODUCT_READY` at `2026-07-29T13:47:44+00:00`
