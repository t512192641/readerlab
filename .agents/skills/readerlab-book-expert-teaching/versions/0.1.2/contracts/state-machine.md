# State machine

```text
NONE ── init ──> EXPERT_OPEN
EXPERT_OPEN ── seal-expert ──> REVIEW_OPEN
REVIEW_OPEN ── seal-review ──> REVIEW_TERMINAL
REVIEW_TERMINAL ── dual PASS + build-product-pack ──> PRODUCT_READY
```

`seal-expert` is the only transition that freezes Expert outputs. `seal-review` is the only transition that parses review terminals. A non-dual-pass review is terminal: `build-product-pack` is rejected and no empty product package is created. Repeating a stage, changing a frozen output, changing the Skill fingerprint, using the same Expert/reviewer ID, or drifting an input/Prompt hash is a hard failure. `verify` never evaluates semantic quality or product acceptance; it only verifies the deterministic control evidence.

Version selection is explicit. A run created by `0.1.0` must be verified through the immutable `0.1.0` entry; `0.1.1`, `0.1.2`, and the current dispatcher refuse it. The current dispatcher never falls back to another version when a run's recorded version differs.
