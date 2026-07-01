# ReaderLab Two-Demo Internal Run v0

## Authority Boundary

This is the execution contract for the next internal demo run. It is not a GPT Pro review prompt and it is not a formal ReaderLab Skill draft.

Current task authority remains `docs/current-task.md`. If this file conflicts with `docs/current-task.md`, update `docs/current-task.md` first.

## Goal

Produce two new ReaderLab demos that are strong enough for later GPT Pro review because they include real artifacts, not only method logic:

1. A book/longform demo that proves Body Track Gate with a complete first-hand body track.
2. A Skill/engineering demo that proves cleaned body text, design-asset extraction, Skillization Gate, and annotation triggers.

The demos must pass internal writer/reader review before any GPT Pro submission packet is prepared.

## Non-Goals

- Do not write a formal ReaderLab Skill.
- Do not do broad external-book validation.
- Do not expand the whole `埃隆之书` package.
- Do not commit copyrighted full text to GitHub.
- Do not create fake sample text, placeholder body text, or demo-only mock data.
- Do not call a demo `reader_package_pass` unless Body Track Gate and internal eval actually pass for that demo.

## Source Selection

### Demo A: Book / Longform Body Track

Purpose: prove that a reader package can include complete first-hand body text plus AI companionship without letting explanation replace the source.

Allowed source priority:

1. User-provided text that the user owns or explicitly approves for inclusion.
2. Public-domain or permissively licensed short book chapter / essay where the full selected text can be committed.
3. Repo-owned longform material if no external source is available, but label it as `longform_owned_material`, not as a book validation.

Disallowed:

- Full copyrighted `埃隆之书` chapters in a GitHub-bound demo.
- AI-generated source text.
- Summary, excerpt, or source anchors pretending to be first-hand body.

If no compliant full-body source is available, stop and report `blocked_missing_compliant_longform_source`.

### Demo B: Skill / Engineering Material

Purpose: prove that ReaderLab can transform engineering/Skill material into cleaned body text, design assets, and guarded Skill candidates.

Default source priority:

```text
1. /Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md
2. /Users/tianqiang/技能项目/skills-canonical/packages/gstack/design-review/SKILL.md
3. /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-xhs-title/SKILL.md
4. /Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-diagnosis/SKILL.md
```

Why these sources:

- `gstack/spec` is the preferred default because it is a complex gstack Skill with enough trigger logic, workflow, tool protocol, execution shell, failure paths, and handoff behavior to stress ReaderLab's cleaned-body and design-asset layers.
- `gstack/design-review` is the gstack fallback when the next session wants a more product/UX-facing complex Skill.
- DB Skills are fallback sources when the next session wants a smaller but still meaningful Skill demo. Prefer `dbs-xhs-title` when the demo should stress formula library / decision matching; use `dbs-diagnosis` when the demo should stress diagnosis/workflow structure.
- Do not run the whole gstack or dbs-suite package for this two-demo pass. Pick exactly one Skill unit for Demo B.

Rules:

- Read only the selected source and directly referenced files needed to understand the Skill.
- Do not install, update, sync, or enable any Skill.
- Do not treat commands, paths, boilerplate, or execution protocol as the main reader body.
- Cleaned body must preserve purpose, trigger, user intent, workflow, constraints, failure conditions, output requirements, and design ideas.

## Output Location

The next session should create artifacts under:

```text
docs/reports/readerlab-two-demo-run-v0/demos/
```

Expected shape:

```text
demos/
  A_longform_body_track/
    README.md
    source-registry.json
    10_一手正文/
      001_正文.md
    20_AI陪读/
      001_reader-facing.md
    audit/
      contracts/
        body-track-gate.json
        material-profile.json
        claim-ledger.json
        candidate-tournament.json
        skillization-gate.json
        annotation-trigger.json
        high-order-explanation.v1.json
      eval.md

  B_skill_engineering/
    README.md
    source-registry.json
    10_一手正文/
      001_净化正文.md
    20_AI陪读/
      001_reader-facing.md
      design-asset-notes.md
    audit/
      contracts/
        body-track-gate.json
        material-profile.json
        claim-ledger.json
        candidate-tournament.json
        skillization-gate.json
        annotation-trigger.json
        high-order-explanation.v1.json
      eval.md
```

## Execution Roles

### Main Controller

The main controller owns source selection, scope control, final landing, and verification.

The controller must not mark a demo passed from its own writing. It must run a separate reader-evaluation step after the writer output.

### Writer Agent

The writer agent produces the demo artifacts.

Allowed inputs:

- selected source material;
- `docs/contracts/*-v1.md`;
- `docs/high-order-explanation-method.md` only if the summary in `docs/current-task.md` is insufficient;
- `docs/eval-gates.md` only for hard-gate awareness, not for self-scoring.

Disallowed inputs:

- GPT Pro review prompts;
- old fullbook summaries;
- old bakeoff outputs;
- future review packet drafts;
- reader evaluation from the same demo before writing is complete.

Writer output requirements:

- JSON contracts must be concrete and decision-changing.
- Reader-facing pages must be natural Chinese prose.
- Reader-facing pages must not expose `source refs`, `claim trace`, `lens score`, `machine_status`, `human_status`, `Body Track Gate`, `Claim Ledger`, `Candidate Tournament`, or similar internal fields.
- Writer cannot give final pass.

### Reader Evaluation Agent

The reader evaluation agent judges the writer output and cannot rewrite it.

Required inputs:

- source material or body track;
- produced reader-facing page;
- produced audit contracts;
- `docs/eval-gates.md`;
- this run contract.

Required output:

```text
result: pass | fail
hard_gates: pass/fail list
reader_score: N/12
P0: []
P1: []
P2: []
must_fix_before_landing: []
```

For Demo B, the reader evaluation must also judge:

- cleaned body is not a summary;
- design assets are not only terminology explanations;
- Skillization Gate blocks non-repeatable insights;
- commands and machine protocol do not pollute the reader body.

## Pass Criteria

Each demo can be landed only if all are true:

- Body Track Gate passes for that demo type.
- JSON contracts parse with `python3 -m json.tool`.
- Candidate Tournament includes at least one real downgrade or reject.
- Claim Ledger has tiers for every high-level claim.
- Skillization Gate rejects or downgrades candidates missing trigger / input / steps / output / boundary / evidence.
- Annotation Trigger outputs 3-7 body-adjacent questions.
- Reader-facing page has no internal field residue.
- Reader evaluation gives `pass`.
- Reader score is at least `10/12`.
- There are no P0/P1 issues.

Both demos must pass before preparing any GPT Pro review packet.

## Stop Conditions

Stop and do not land a passed demo if any occurs:

- compliant full-body longform source is missing;
- copyrighted full book/chapter text would need to be committed;
- writer uses old fullbook, old bakeoff, or GPT Pro review prompt as writing input;
- reader-facing page exposes internal fields;
- candidate pool has no downgrade/reject;
- claim tiers exist but do not constrain reader-facing wording;
- annotation triggers are generic and not body-adjacent;
- Skill/engineering cleaned body becomes a summary;
- Skillization promotes a non-repeatable insight;
- only one demo passes.

## Verification Commands

Run before reporting completion:

```bash
find docs/reports/readerlab-two-demo-run-v0/demos -name '*.json' -print -exec python3 -m json.tool {} /tmp/readerlab-demo-json.out \;
rg -n "source refs|claim trace|lens score|machine_status|human_status|Body Track Gate|Claim Ledger|Candidate Tournament|Skillization Gate|Annotation Trigger" docs/reports/readerlab-two-demo-run-v0/demos/*/20_AI陪读
python3 tests/test_readerlab.py
git diff --check
```

The `rg` command should return no matches. If it returns matches, the demo cannot be marked passed until fixed.
