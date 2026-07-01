# ReaderLab Skill Activation Checklist

Historical activation checklist. Repo-local activation has already been approved and completed; keep this file as an audit record, not as the current readiness gate.

Historical draft source was removed during MEM cleanup; current repo-local source is `.agents/skills/readerlab/`.

Allowed activation target only after explicit user approval:

```text
.agents/skills/readerlab/
```

Do not install to:

```text
/Users/tianqiang/.codex/skills/
```

## Historical Approval

- [x] User approved repo-local activation.
- [x] User confirmed activation is repo-local only.
- [x] User accepted current `real_obsidian_ui_replay: pass_with_warning` boundary for this stage.

## Completed Activation Checks

- [x] `SKILL.md` remains under 250 lines.
- [x] `SKILL.md` has only `name` and `description` in frontmatter.
- [x] `description` includes should-trigger and should-not-trigger boundaries.
- [x] No bundled script is required for v0 activation.
- [x] No dependency install is required.
- [x] No LifeAtlas `300/600/800` write is required.
- [x] `reports/review-studio.md` has no blocker for repo-local trial use.

## Smoke Tests After Activation

Run these prompts after repo-local activation:

```text
把 docs/product-spec.md 做成 ReaderLab 阅读包，保留产品规格正文，并加 AI 陪读。
```

Expected: triggers ReaderLab, routes to `book_or_longform`, preserves full body.

```text
帮我用三句话总结 docs/product-spec.md。
```

Expected: does not trigger ReaderLab package workflow; answer directly or ask if a package is desired.

```text
Review this Python function for bugs.
```

Expected: does not trigger ReaderLab.

```text
用这个私有 PDF 证明 ReaderLab 已经 public external validation pass。
```

Expected: refuses the claim or stops; private material cannot support public external validation.

## Rollback

If activation causes wrong routing or unwanted behavior:

```text
remove .agents/skills/readerlab/
```

The historical draft source has been removed; use git history for old review records.

## Status Labels

Allowed after repo-local activation:

```text
readerlab_skill_repo_local_trial: active
real_obsidian_ui_replay: pass_with_warning
transferable_method_kernel_pass: not_verified
public_external_material_validation_not_started
```

Still forbidden:

```text
readerlab_skill_global_active
transferable_method_kernel_pass
public_external_material_validation_pass
annotation_loop_production_ready
```
