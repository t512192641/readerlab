# ReaderLab comment replay validation v0

This package validates the next ReaderLab gap without editing existing demo
artifacts.

Scope:

- Use the existing Obsidian plugin storage shape, `tandem-comments`.
- Validate comment replay from a plugin comment anchor back to body text,
  claim, candidate, and gate decision.
- Validate the existing A2/B2 trace chain from `location-map` to claims,
  candidates, annotation triggers, and skillization decisions.

Non-scope:

- It does not modify existing ReaderLab docs, demos, contracts, or tests.
- It does not create a formal ReaderLab `SKILL.md`.
- It does not automate the Obsidian UI. This is a storage-format and replay
  chain test for the current plugin format.

Files:

- `tools/run_trace_replay_validation.py` generates plugin-format fixtures and
  validates the replay chain.
- `fixtures/*.tandem.md` are minimal Obsidian-note fixtures with a
  `tandem-comments` fenced JSON block at the end.
- `results/trace-validation.json` records deterministic trace checks.
- `results/comment-replay.json` records comment replay checks.
- `results/eval.md` summarizes the result in reader-friendly language.
