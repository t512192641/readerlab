# ReaderLab Skill Activation Checklist

Use this checklist before copying the draft package into a live project Skill path.

Current draft source:

```text
docs/drafts/readerlab-skill-v0/
```

Allowed activation target only after explicit user approval:

```text
.agents/skills/readerlab/
```

Do not install to:

```text
/Users/tianqiang/.codex/skills/
```

## Required Approval

- [ ] User explicitly approves creating `.agents/skills/readerlab/`.
- [ ] User confirms activation is repo-local only.
- [ ] User accepts current `real_obsidian_ui_replay: pass_with_warning` boundary, or requests a body-prose replay retest before activation.

## Pre-Activation Checks

- [ ] `SKILL.md` remains under 250 lines.
- [ ] `SKILL.md` has only `name` and `description` in frontmatter.
- [ ] `description` includes should-trigger and should-not-trigger boundaries.
- [ ] No bundled script is required for v0 activation.
- [ ] No dependency install is required.
- [ ] No LifeAtlas `300/600/800` write is required.
- [ ] `reports/review-studio.md` has no blocker for docs-only use.

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

Do not delete the draft source under `docs/drafts/readerlab-skill-v0/`; it is the review record.

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
