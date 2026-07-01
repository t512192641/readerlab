# ReaderLab Activation Hardening

## Result

Status: `ready_for_user_activation_decision`

The draft is ready for a user decision about repo-local activation. It is not activated.

## Checks

- `SKILL.md` length: under 250 lines.
- Frontmatter: `name` and `description` only.
- Trigger boundary: includes both should-trigger and should-not-trigger cases.
- Resource surface: no scripts, no dependencies, no assets.
- Evidence: fixture replay pass, real Obsidian UI replay `pass_with_warning`, product-spec forward test pass with route fix.
- Review status: warning remains for activation because body-prose direct selection replay is not verified.

## Activation Target

Only this target is in scope after explicit user approval:

```text
.agents/skills/readerlab/
```

Out of scope:

```text
/Users/tianqiang/.codex/skills/
LifeAtlas 300/600/800
public package publication
```

## Remaining Warning

Real Obsidian UI replay proved plugin storage and Codex readback. The first test selected visible anchor-list entries rather than body prose sentences.

This warning does not block a repo-local trial if the user accepts the boundary. It should block claims such as production-ready annotation loop or transferable method pass.

## Recommended Next Step

Ask the user whether to activate repo-locally:

```text
Create .agents/skills/readerlab/ from docs/drafts/readerlab-skill-v0/
```

If approved, copy only the package files needed for a Skill trial:

```text
SKILL.md
checks/
evals/
examples/
reports/
```

Then run the smoke tests in `checks/activation-checklist.md`.
