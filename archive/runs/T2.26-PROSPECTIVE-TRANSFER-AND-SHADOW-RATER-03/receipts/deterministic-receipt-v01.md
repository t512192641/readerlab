# T2.26 v03 确定性收据（控制层无效运行）

- terminal: `INVALID_RUN`
- frozen taskcard SHA-256: `84f02808a502b58c9de8938fcc17b773cc8d999c15c0dfa23e24d7567eded9f5`
- closeout taskcard SHA-256: `56e1fa8bbd1baea99484e3b41f0663765a8041cf5599695e63ff3c1dedfe96e4`
- source SHA-256: `3baf9932c92412f0e7d0ccae993182f55f62e2fab5ec46a3882d675476288664`
- excluded chapters: `7, 13, 14, 15, 16, 19`
- independent selection runs: 2; `IDENTICAL`
- eligible count: 15
- payload: 250 bytes; SHA-256 `16b480aa130a24d8fa1e3e925fb0eaa32740c732271691afd3cf87bdb27e70c3`
- selected zero-based index / ID: `1` / `eligible-02`
- selected chapter / member: chapter 2 / `text/part0006.html`
- selected member: 82261 bytes; SHA-256 `ba0c9aa2a7413d6792cf1b57b821dc38bd3d6777d5a16cb0dcd69c4dd9442e82`
- pre-write chapter scope: 82260 bytes; SHA-256 `934624eacafabf192b930519ff19a0c004fb12d8fc477c04922e5835cdaf69c6`
- first-written and binary-readback chapter scope: 82260 bytes; SHA-256 `934624eacafabf192b930519ff19a0c004fb12d8fc477c04922e5835cdaf69c6`
- Writer contract: 6003 bytes; SHA-256 `9a7a3bcaaf4d81cdc2936a2217ea9a147ea91b2edccf5ee0d83fd06a60462ffe`; exact check `PASS`
- invalid artifact: `control/human-local-review-form-v01.md`; SHA-256 `00eeb01106d9a1e64ca97505a08cb329c54bf364081ca96f5a90885759f5307f`
- invalidating difference: the first-written human local review form is a P1 candidate verdict form. It does not provide the six per-Reader comparable questions, issue fields, or Reader-level terminal required by taskcard section 4.
- corrective overwrite: not performed
- contract manifest: not created
- semantic / evaluation calls: 0
- candidate pool, comparison, breadth diagnostic, P1 review pack, and P1 verdict form: not created
- downstream production: not started
- product acceptance: not requested
- additional closeout failure: `artifact-registry.jsonl` does not register the three ledger files or the two closeout files. Because the registry cannot prove coverage of every existing run artifact, deterministic verification remains `FAIL` independently of the invalid human-review contract.

The invalid human-review contract is sufficient to terminate v03 before any semantic role. The new-chapter selection, exact chapter-scope write, and exact Writer-contract extraction are verified only as control-layer evidence from this invalid run.
