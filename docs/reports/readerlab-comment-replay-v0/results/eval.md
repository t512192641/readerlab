# Comment replay validation eval

Overall: pass

What was tested:

- Four mock reader comments were stored with the current Obsidian plugin shape: `tandem-comments` fenced JSON.
- Each comment anchor was checked against `exact`, `pos`, `prefix`, and `suffix` in the fixture body.
- Each replay case was connected back to an existing A2/B2 body anchor, claim, candidate, and gate decision.
- Existing A2/B2 trace maps were checked for location-map, claim-ledger, candidate-tournament, annotation-trigger, and skillization-gate consistency.

Important boundary:

- This validates the plugin storage/replay chain, not the Obsidian UI interaction itself.
- No existing ReaderLab file was modified; this package only adds test fixtures and results.

Result files:

- `results/trace-validation.json`
- `results/comment-replay.json`
