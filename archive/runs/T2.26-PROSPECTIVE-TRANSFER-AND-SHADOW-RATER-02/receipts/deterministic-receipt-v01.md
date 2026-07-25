# T2.26 v02 确定性收据（无效运行）

- terminal: `INVALID_RUN`
- frozen taskcard SHA-256: `a36d3be57cdebd83e6890e639622cca02694d6a22d9bebff9be8834dc382971d`
- closeout taskcard SHA-256: `82d1137ec00de3fcf6357e77e4416475178dbdf88531b83227f991517b1ffd1a`
- source SHA-256: `3baf9932c92412f0e7d0ccae993182f55f62e2fab5ec46a3882d675476288664`
- selection payload SHA-256: `60884a78de99b0668c9f1d4bee4d642c12870e801ab419966120eda21dbc5d41`
- selected eligible ID / index: `eligible-07` / `6`
- selected member: `text/part0012.html`; 46095 bytes; SHA-256 `3fa3fa2ac959a2010b1fe006edfb7358bd2f73ae9aa91fd1bea90f6fcf301ae7`
- pre-write chapter scope: 34318 bytes; SHA-256 `845ffeb07a73f3cd248b25f9fc19609d1c8757cbd478b8f72371401dc3b12dda`
- first-written and binary-readback chapter scope: 34318 bytes; SHA-256 `845ffeb07a73f3cd248b25f9fc19609d1c8757cbd478b8f72371401dc3b12dda`
- write mode: exclusive binary create; no corrective overwrite
- frozen Writer contract SHA-256 recorded by `contract-manifest.md`: `3ebba0266f5883b99c25f7beec4ae7d2c6d1476c3d57024cf06ae784c8e6dc61`
- actual Writer contract SHA-256 after discovery: `0c34b2232c5e4e243fc207b6c74c92e1df7f92dd21e379cfab76517d7fbe36c2`
- invalidating difference: `writer-contract-v1.3.md` was mechanically altered after contract freeze while correcting its exact trailing-whitespace extraction. The manifest still binds the earlier SHA.
- semantic production before detection: one discovery Expert, one independent comparator, and one candidate-breadth diagnostic.
- invalid artifacts: candidate pool, comparison, breadth diagnostic, mechanically assembled P1 review pack, and empty P1 verdict form are retained as run evidence but must not be used as a valid product gate or production input.
- P1 status: not validly entered.
- downstream production: not started.
- product acceptance: not requested.
- additional closeout failure: `production-group-ledger.jsonl`, `usage-ledger.jsonl`, and `artifact-registry.jsonl` do not cover all dispatches, completions, calls, and artifacts produced before the stop, so deterministic verification also remains `FAIL`.

The frozen-contract SHA mismatch is independently sufficient to terminate v02 as `INVALID_RUN`. The precise-binary-write correction itself is verified for this run.
