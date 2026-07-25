# T2.26 v02 使用摘要（无效运行收口）

- terminal: `INVALID_RUN`
- production lead: one recorded control turn; service invocation ID, service token fields, visible-text token fields, hidden-reasoning tokens, and exact model work time are `unknown`.
- semantic/evaluation calls observed: discovery Expert 1, independent comparator 1, candidate-breadth diagnostic 1; retries 0.
- the three semantic roles used fresh `gpt-5.6-terra / medium` contexts.
- role-reported elapsed times were approximately 4, 3, and 2 minutes respectively; these are not service-side exact model-work measurements.
- `usage-ledger.jsonl` contains the production-lead control entry and discovery Expert entry, but omits the comparator and breadth-diagnostic entries; therefore it is incomplete and cannot serve as a complete deterministic call ledger.
- `production-group-ledger.jsonl` likewise omits the comparator and breadth-diagnostic dispatch/completion records; `artifact-registry.jsonl` omits their artifacts and later invalid P1 files.
- no Expert expansion, P2, source audit, Writer, Fidelity, shadow Reader Quality Rater, P3, reveal, issue matching, content-dimensions diagnostic, or C-patch call occurred.
- P1 was not validly entered; no product-gate waiting time is claimed.

No token estimate is inferred from bytes, characters, elapsed time, or Agent output.
