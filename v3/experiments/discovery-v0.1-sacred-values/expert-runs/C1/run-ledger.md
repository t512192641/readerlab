# C1 · run ledger

> This ledger records deterministic control actions only; it is not a semantic judgment.

- current status: `REVIEW_TERMINAL`
- Expert Agent ID: `019faed9-ed7f-73a1-b08c-e7e50d4bd324`
- Reviewer Agent ID: `019faedf-5fae-7cd2-80fa-75e3befe7e27`
- model: Expert `gpt-5.6-sol`, review `gpt-5.6-terra`; provenance: `controller_declared`
- reasoning: Expert `high`, review `high`; provenance: `controller_declared`
- network: Expert `allowlisted-only`, review `allowlisted-only`; provenance: `controller_declared`
- retries: Expert `no`, review `no`; provenance: `controller_declared`
- Prompt modified: Expert `no`, review `no`; provenance: `controller_declared`
- semantic calls invoked by this Skill: `none`
- external semantic contexts: `controller_declared`
- source access receipts: Expert `raw/expert-source-access.json` (SHA-256 `38765ef84a506bdad2d8bbddd0e46f4d6f1e8fcc6dd996198d839878b287ef74`), reviewer `acceptance/reviewer-source-access.json` (SHA-256 `b8063b9f36e7d8ba8d38551244aac483c673bf348d319be6c014756acbded902`); provenance: `agent_declared`; audit scope: `agent-declared; not a browser or OS-level network audit`
- source boundary: `control/source-boundary.json`; schema: `readerlab-book-expert-teaching/source-boundary/v1`
- archive hash: recorded outside the archive to avoid self-reference

## State transitions

- `NONE` → `EXPERT_OPEN` at `2026-07-29T17:08:47+00:00`
- `EXPERT_OPEN` → `REVIEW_OPEN` at `2026-07-29T17:14:47+00:00`
- `REVIEW_OPEN` → `REVIEW_TERMINAL` at `2026-07-29T17:18:08+00:00`
