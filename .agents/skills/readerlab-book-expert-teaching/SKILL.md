---
name: readerlab-book-expert-teaching
description: Run the fixed-source, fixed-framework ReaderLab Book Expert Teaching stage as a versioned, auditable Skill. Use when a human controller has already chosen the original text, one external framework, and a closed source allowlist, and needs deterministic run creation, isolated Expert/reviewer handoffs, dual-terminal gating, product-pack assembly, verification, or archiving. This Skill does not discover frameworks, call semantic models, run Writer/Reader/ABC/Discovery, or orchestrate a complete ReaderLab pipeline.
---

# ReaderLab Book Expert Teaching v0.1

Use this Skill only after a human has fixed three inputs: the original text, the external framework identity, and the source-map/allowlist. It standardizes the control layer around one Expert Teaching stage; semantic writing and independent review remain manually launched in fresh contexts using the generated task/read-set files.

## Boundary

- Keep the original text, framework identity, and source map byte-frozen inside a new run.
- Generate narrow Expert and reviewer tasks with closed local read sets and allowlisted source URLs.
- Accept only the two explicit review terminals before building a product package:
  `SOURCE_FIDELITY_PASS` and `TEACHING_PASS`.
- Never discover C, call Writer/Reader/Fidelity/B2, compare ABC, select routes, or make product acceptance decisions.
- Treat this as an artificial/manual orchestration layer, not an integrated ReaderLab runtime.

## Entry point

Run from the repository root:

```bash
python3 .agents/skills/readerlab-book-expert-teaching/scripts/run.py <command> ...
```

The command is deterministic and non-semantic. It reuses `tools/run.py` for stable hashing and exclusive publication; it does not replace that generic run manager.

## Workflow

1. `init` with `--source`, `--framework`, `--source-map`, `--run`, and `--skill-version 0.1.0`.
   It refuses an existing run, copies the three inputs, records bytes/SHA-256, writes task/read-set files, and opens `EXPERT_OPEN`.
2. Launch one fresh Expert context manually. Give it only `control/expert-task.md` and the listed read set. It writes only `raw/expert-teaching-draft.md` and `raw/expert-teaching-source-map.md`.
3. `seal-expert --run ... --agent-id ...` records the Expert metadata, validates UTF-8/non-empty output and the no-M-label rule, freezes the output, and opens `REVIEW_OPEN`.
4. Launch a different fresh reviewer context manually. Give it only `control/review-task.md` and the generated review read set. It writes only `acceptance/expert-teaching-review.md`.
5. `seal-review --run ... --reviewer-id ...` parses the two terminal lines, rejects a reviewer ID equal to the Expert ID, and freezes the review. Any non-dual-pass result is terminal and cannot build a product package.
6. Only after both PASS terminals, run `build-product-pack --run ...`. The controller converts HTML/XHTML-like source into readable Markdown, adds the full teaching draft and fixed product questions, rejects source-map/technical/Writer/M-label leakage, and freezes the package.
7. Run `verify --run ...` before handoff. Run `archive --run ... --output ...` only after verification; the archive hash is printed outside the archive to avoid self-reference.

## Version discipline

`VERSION` is `0.1.0`. Each run records a fingerprint of this Skill's `SKILL.md`, `VERSION`, contracts, and templates. `verify` fails if those files drift. Do not silently edit the Skill between migration samples; record a change receipt and use a new version before mixing results.

## Contracts and templates

Read only the contract needed for the current control question:

- [input-contract.md](contracts/input-contract.md): fixed inputs and initialization.
- [expert-teaching-contract.md](contracts/expert-teaching-contract.md): semantic Expert responsibility.
- [review-contract.md](contracts/review-contract.md): independent source/depth review and terminals.
- [output-contract.md](contracts/output-contract.md): files, product-pack restrictions, and archive evidence.
- [state-machine.md](contracts/state-machine.md): legal transitions and hard stops.

The three files in `templates/` are copied into each run's control layer. They are generic and contain no U01, Young, or other candidate-specific answer.

## Mechanical replay

The T2.38 replay fixture is `tests/fixtures/t2.38-replay.json`. Its test injects the already-frozen T2.38 Expert/review outputs; it never calls a model or opens a new source. Run the Skill-local tests with:

```bash
python3 -m unittest discover -s .agents/skills/readerlab-book-expert-teaching/tests -p 'test_*.py'
```

The fixture is calibration evidence only. It does not grant production integration, product acceptance, or permission to run migration samples.
