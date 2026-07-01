# ReaderLab Formal Skill Draft Implementation Plan

## Status

This is the minimal implementation plan for entering the formal ReaderLab Skill draft phase after explicit user approval.

The user has approved creating one formal draft file named `SKILL.md` under `docs/drafts/readerlab-skill-v0/`. This remains a draft artifact, not an installed Codex Skill and not a public validation result.

Current allowed state:

```text
formal_skill_draft_contract_ready: yes
formal_skill_draft_human_approval: docs_draft_skill_md_allowed
formal_skill_draft_implementation_plan_ready: yes
formal_skill_draft_allowed_path: docs/drafts/readerlab-skill-v0/SKILL.md
formal_skill_draft_start_allowed: docs_draft_only
transferable_method_kernel_pass: not_verified
real_obsidian_ui_replay: deferred
public_external_material_validation_not_started
```

## Goal

The next implementation phase should produce the smallest reviewable ReaderLab `SKILL.md` draft without activating it as a reusable asset.

The draft must prove that ReaderLab can guide an agent through the full body-first reading-package workflow while keeping deterministic checks, interpretive judgment, and human acceptance separate.

## Non-Goals

This plan does not authorize:

- creating `SKILL.md` outside `docs/drafts/readerlab-skill-v0/`
- creating `.agents/skills/readerlab/`
- installing anything into `/Users/tianqiang/.codex/skills/`
- moving output into LifeAtlas `300/600/800`
- claiming `transferable_method_kernel_pass`
- claiming public external validation
- claiming real Obsidian UI replay has passed

## Minimal Draft Shape

The first formal draft should be a review packet with a draft `SKILL.md`, not an activated Skill.

Suggested files for the next phase:

```text
docs/drafts/readerlab-skill-v0/
  README.md
  SKILL.md
  examples/
    input-request.json
    route-decision-example.json
  checks/
    readiness-checklist.md
```

Important boundary:

```text
docs/drafts/readerlab-skill-v0/SKILL.md is a draft source document.
It must not be copied to .agents/skills/readerlab/ or installed until a later explicit activation step.
```

## Implementation Slices

### Slice 1: Draft Packet Skeleton

Create a non-installed draft packet under `docs/drafts/readerlab-skill-v0/`.

Required content:

- purpose and scope
- supported routes
- required input object
- expected output package shape
- workflow state machine
- agent/script boundary
- gate checklist
- stop conditions
- validation commands

Acceptance:

- exactly one draft `SKILL.md`, located at `docs/drafts/readerlab-skill-v0/SKILL.md`
- no `.agents/skills/readerlab/`
- draft text references existing contracts instead of duplicating all contract content

### Slice 2: Input and Route Contract

Define the exact request object the future Skill accepts:

```json
{
  "material_id": "string",
  "title": "string",
  "source_paths": ["string"],
  "output_root": "string",
  "permission_boundary": "public_ok | private_only | unknown",
  "intended_reader": "string",
  "requested_scope": "whole_package | selected_unit | chapter | file",
  "human_review_required": true
}
```

Route decisions:

- `book_or_longform -> full_body`
- `skill_or_engineering_doc -> cleaned_body`
- `mixed_material_package -> classify_each_unit_then_route`

Agent judgment:

- route selection
- unit classification
- permission-boundary interpretation

Script support:

- source path existence checks
- file metadata capture
- draft request JSON parse checks

### Slice 3: Output Checklist

Define route-specific output requirements.

Common package:

```text
README.md
source-registry.json
10_一手正文/
20_AI陪读/
audit/location-map.json
audit/trace-to-reader.md
audit/contracts/material-profile.json
audit/contracts/body-track-gate.json
audit/contracts/claim-ledger.json
audit/contracts/candidate-tournament.json
audit/contracts/skillization-gate.json
audit/contracts/annotation-trigger.json
audit/contracts/high-order-explanation.v1.json
audit/contracts/trace-validation.json
audit/eval.md
```

Engineering-material additions:

```text
20_AI陪读/design-asset-notes.md
audit/source-cleaning-map.md
```

Mixed-package additions:

```text
audit/unit-classification-map.json
```

Acceptance:

- output checklist matches `docs/readerlab-formal-skill-draft-contract.md`
- reader-facing outputs keep audit field names out of the visible page

### Slice 4: Validation Wiring

The draft must call the current validator as a required pre-review step:

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
```

The draft may describe future validator expansion, but it must not require new validator behavior before the draft can be reviewed.

Current deterministic checks:

- anchors exist and can be referenced
- annotation triggers reference known anchors
- claims and candidates resolve
- Skill candidates include trigger, input, steps, output, boundary, and evidence
- fixture replay resolves comment to body anchor, claim, candidate, gate, and bounded reply

Current non-deterministic checks:

- prose quality
- body cleaning judgment
- claim truth
- design insight quality
- human acceptance

### Slice 5: Human Review Handoff

The draft packet must end with a human review handoff:

```text
machine checks: pass | fail
fixture replay: pass | fail
real Obsidian UI replay: deferred | pass | fail
human status: pending | accepted | rejected
allowed next step: revise | create SKILL.md | stop
```

For this phase, `create SKILL.md` means creating only `docs/drafts/readerlab-skill-v0/SKILL.md`.

Only the user can move a later `allowed next step` to `activate/install Skill`.

## First Draft Acceptance Criteria

The next phase is acceptable when:

- draft packet exists under `docs/drafts/readerlab-skill-v0/`
- draft packet contains `docs/drafts/readerlab-skill-v0/SKILL.md`
- draft `SKILL.md` clearly marks itself as non-installed and not activated
- draft references the contract, IR, and validation contracts
- route and output expectations are unambiguous
- agent/script boundary is explicit
- validation commands are copied exactly
- real Obsidian UI replay remains deferred
- no `.agents/skills/readerlab/` exists

## Stop Conditions

Stop and report if any of these would be required:

- creating `SKILL.md` outside `docs/drafts/readerlab-skill-v0/`
- creating `.agents/skills/readerlab/`
- installing a Skill
- writing outside the repo
- changing LifeAtlas permanent zones
- adding dependencies
- claiming public or transferable validation
- bypassing human review

## Verification Commands

Run after creating the draft packet:

```bash
python3 scripts/readerlab_trace_validator.py validate-suite --demo docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity --demo docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files --cases-json docs/reports/readerlab-comment-replay-v0/fixtures/comment-replay-cases.json --fixture-dir docs/reports/readerlab-comment-replay-v0/fixtures
python3 tests/test_readerlab_trace_validator.py
python3 tests/test_readerlab.py
rg -n "source refs|claim trace|lens score|machine_status|human_status|Body Track Gate|Claim Ledger|Candidate Tournament|Skillization Gate|Annotation Trigger" docs/drafts/readerlab-skill-v0
git diff --check
```
