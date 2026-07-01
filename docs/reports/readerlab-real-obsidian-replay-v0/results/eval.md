# Real Obsidian UI replay eval

Overall: `pass_with_warning`

## What Passed

- Obsidian wrote real plugin comments into the Markdown files.
- The plugin storage format is `tandem-comments`.
- All four comments include `exact`, `prefix`, `suffix`, and `pos`.
- All four `pos` values resolve to the selected text.
- Codex can read each comment and produce a bounded reply tied to the expected claim, candidate decision, and gate.
- After normalizing the visible anchor label such as `L1:` or `E1:`, each comment can be mapped back to the intended body phrase.

## Warning

The comments were attached to the visible test anchor list entries, not directly to the prose sentences in the body paragraphs.

This means the current result proves:

```text
real Obsidian plugin storage -> selected anchor text -> normalized body phrase -> bounded reply
```

It does not yet strictly prove:

```text
real Obsidian plugin storage -> body paragraph selection -> bounded reply
```

## Current Status

Use this status:

```text
real_obsidian_ui_replay: pass_with_warning
real_obsidian_ui_storage_format: tandem-comments
real_obsidian_ui_body_prose_selection: not_verified
```

Do not use:

```text
real_obsidian_ui_replay: full_pass
annotation_loop_production_ready
transferable_method_kernel_pass
public_external_material_validation_pass
```

## Next Step

If strict activation readiness is required, repeat the same test once with comments attached directly to the prose sentences rather than the anchor list entries.
