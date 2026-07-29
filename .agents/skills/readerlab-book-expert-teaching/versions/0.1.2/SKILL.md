---
name: readerlab-book-expert-teaching
description: Run the fixed-source, fixed-framework ReaderLab Book Expert Teaching stage v0.1.2 with explicit version selection, closed source boundaries, agent-declared access receipts, isolated Expert/reviewer handoffs, dual-terminal gating, product-pack assembly, verification, or archiving. This Skill does not discover frameworks, call semantic models, run Writer/Reader/ABC/Discovery, or orchestrate a complete ReaderLab pipeline.
---

# ReaderLab Book Expert Teaching v0.1.2

This is the independent `0.1.2` implementation. The historical `0.1.0` implementation remains at the committed root entry and is never overwritten; `0.1.1` remains in its own immutable version directory. Use the current dispatcher only for the version named by `CURRENT_VERSION`; use the explicit historical entry when verifying a historical run. Results from `0.1.0`, `0.1.1`, and `0.1.2` must not be mixed.

## Entry points

Current version:

```bash
python3 .agents/skills/readerlab-book-expert-teaching/run-current.py <command> ...
```

The dispatcher is outside `scripts/` so it cannot change the historical `0.1.0` fingerprint.

Explicit `0.1.1` implementation:

```bash
python3 .agents/skills/readerlab-book-expert-teaching/versions/0.1.1/scripts/run.py <command> ...
```

Historical `0.1.0` implementation:

```bash
python3 .agents/skills/readerlab-book-expert-teaching/scripts/run.py <command> ...
```

The historical entry is intentionally not a compatibility alias for `0.1.1`. A run's recorded `skill_version` and fingerprint must match the implementation entry used for `verify` or `archive`; a mismatch fails closed.

## Boundary

- Keep the original text, framework identity, source map, and structured source allowlist frozen inside a new run.
- The allowlist schema is `readerlab-book-expert-teaching/source-allowlist/v1`; `control/source-boundary.json` proves that every source-map URL is registered and that only explicit redirects may be extra. Canonical allowlist URLs must occur in the source map.
- Only `allowed` URLs and explicitly registered redirects appear in Expert/reviewer tasks. `reference_only` and `blocked` entries never become network permissions.
- Each semantic role writes an exact `readerlab-book-expert-teaching/source-access/v1` receipt. `opened_urls` may contain only `allowed` URLs or their explicit redirects; `cited_only_urls` may contain `allowed` or `reference_only` URLs, never `blocked` or unregistered URLs. Receipts declare `provenance: agent_declared`; this is not browser or OS-level network auditing.
- Reject new or blocked URLs in Expert drafts, source maps, reviewer reports, and access receipts; `reference_only` URLs may be cited but not opened.
- Generate narrow Expert and reviewer tasks with closed local read sets and no open-ended search.
- Accept only `SOURCE_FIDELITY_PASS` plus `TEACHING_PASS` before building a product package.
- Product checks reject internal paths, control titles, scoring metadata, route metadata, and explicit depth self-labels. Natural `M1`, `M2`, `M3`, or `Writer` in fixed text or teaching prose is allowed.
- Treat this as an artificial/manual orchestration layer, not an integrated ReaderLab runtime.

## Workflow

1. `init` requires `--source`, `--framework`, `--source-map`, `--source-allowlist`, `--run`, and `--skill-version 0.1.2`. It validates the structured allowlist and closed source boundary, copies all fixed inputs, records bytes/SHA-256, writes tasks/read sets, and opens `EXPERT_OPEN`.
2. Launch one fresh Expert context manually. Give it only the exact local read set and `allowed` source URLs. It writes the teaching draft, claim-source map, and truthful `raw/expert-source-access.json` receipt while following the stable Chinese expression rules in the task.
3. `seal-expert --run ... --agent-id ...` records controller-declared metadata, validates UTF-8/non-empty output, checks URLs in both Expert outputs and the access receipt, rejects new/blocked source URLs and only obvious depth self-labels, freezes all three outputs, and opens `REVIEW_OPEN`.
4. Launch a different fresh reviewer context manually. Give it only the generated review read set and `allowed` source URLs. It writes the review report and truthful `acceptance/reviewer-source-access.json` receipt.
5. `seal-review --run ... --reviewer-id ...` parses the two terminal lines, checks reviewer report URLs, access receipt, and ID isolation, and freezes both review artifacts. Any non-dual-pass result is terminal and cannot build a product package.
6. Only after both PASS terminals, run `build-product-pack --run ...`. The controller converts HTML/XHTML-like source to readable Markdown, adds the complete course and generic Chinese product questions, applies internal-leakage checks, and freezes the package.
7. Run `verify --run ...` before handoff. Run `archive --run ... --output ...` only after verification; the archive hash is printed outside the archive to avoid self-reference.

## Version discipline

`VERSION` is `0.1.2`. Every run records this version, the version-local Skill fingerprint, the allowlist hash, source-boundary hash, access-receipt hashes, and stage hashes. Do not silently edit this implementation between migration samples; use a new version and a change receipt. `0.1.0`, `0.1.1`, and `0.1.2` results must never be mixed.

## Stable Chinese expression rules

The Expert contract and generated task require: default Chinese; first person names as `中文译名（英文原名）`; first theories as `中文名称（英文名称）`; later references in Chinese; no English-only names or long mixed-language runs; ordinary-language explanation before specialist terms; and an explicit distinction between ReaderLab teaching organization and an author's formal method.

## Contracts and templates

- [input-contract.md](contracts/input-contract.md): four fixed inputs, structured allowlist, and closed source boundary.
- [expert-teaching-contract.md](contracts/expert-teaching-contract.md): semantic Expert responsibility and language rules.
- [review-contract.md](contracts/review-contract.md): independent review, citation boundaries, and terminals.
- [output-contract.md](contracts/output-contract.md): product-pack restrictions and archive evidence.
- [state-machine.md](contracts/state-machine.md): legal transitions and version hard stops.

## Mechanical replay

The T2.38 replay fixture is consumed by repository tests with explicit `0.1.2` allowlist and Expert/reviewer access-receipt fixtures. The test verifies every registered frozen input and output hash, injects already-frozen Expert/review outputs and receipts, checks the expected `0.1.2` product content hash, verifies archive entries and hashes for both receipts, and never calls a model or opens a source.
