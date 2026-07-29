# EXPERT-TEACHING-V0.1.2-MIGRATION-B-T2.10-01 · run ledger

> This ledger records deterministic control actions only; it is not a semantic judgment.

- current status: `PRODUCT_READY`
- Expert Agent ID: `019fae1b-7e3b-7720-9627-58069239f492`
- Reviewer Agent ID: `019fae21-dc09-7323-a3d7-5d0d22ee8e65`
- model: Expert `gpt-5.6-sol`, review `gpt-5.6-terra`; provenance: `controller_declared`
- reasoning: Expert `high`, review `high`; provenance: `controller_declared`
- network: Expert `allowlisted-only`, review `allowlisted-only`; provenance: `controller_declared`
- retries: Expert `no`, review `no`; provenance: `controller_declared`
- Prompt modified: Expert `no`, review `no`; provenance: `controller_declared`
- semantic calls invoked by this Skill: `none`
- external semantic contexts: `controller_declared`
- source access receipts: Expert `raw/expert-source-access.json` (SHA-256 `bd846c0ef305f8032fdefd5c3d53cb7fd60ed7b1a4d7e850d3f02a6741ed13b8`), reviewer `acceptance/reviewer-source-access.json` (SHA-256 `98a96bce8544f41425fbebae22e427a46cf67e44b91471e4bb5942a446f0b077`); provenance: `agent_declared`; audit scope: `agent-declared; not a browser or OS-level network audit`
- source boundary: `control/source-boundary.json`; schema: `readerlab-book-expert-teaching/source-boundary/v1`
- archive hash: recorded outside the archive to avoid self-reference

## State transitions

- `NONE` → `EXPERT_OPEN` at `2026-07-29T13:33:21+00:00`
- `EXPERT_OPEN` → `REVIEW_OPEN` at `2026-07-29T13:45:45+00:00`
- `REVIEW_OPEN` → `REVIEW_TERMINAL` at `2026-07-29T13:49:11+00:00`
- `REVIEW_TERMINAL` → `PRODUCT_READY` at `2026-07-29T13:49:19+00:00`
