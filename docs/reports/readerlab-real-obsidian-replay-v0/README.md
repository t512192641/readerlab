# ReaderLab Real Obsidian Replay v0

## Purpose

This report tracks the first real Obsidian UI replay test for ReaderLab.

The test verifies:

```text
Obsidian real comment -> plugin storage -> Codex reads comment -> body anchor -> claim/candidate/gate context -> bounded reply
```

## Scope

Current scope:

- two comments on a longform/full-body note
- two comments on a Skill/engineering cleaned-body note
- current Obsidian plugin storage, expected to be `tandem-comments`

Non-scope:

- public external validation
- transferable method pass
- ReaderLab Skill installation or activation
- LifeAtlas permanent `300/600/800` sediment writes

## Vault Test Location

The test files are copied to:

```text
/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/readerlab-ui-replay-test/
```

## User Action

Open the two Markdown files in Obsidian and create one real plugin comment on each marked selection.

Use `instructions.md` for exact file paths, selected text, and comment text.

## Result

`pass_with_warning`

Result files:

- `results/comment-replay-real-ui.json`
- `results/eval.md`

Boundary:

- Real Obsidian plugin storage is verified.
- `tandem-comments` real UI output is readable.
- Comments were attached to visible anchor list entries rather than body prose sentences.
- Strict body paragraph selection replay remains unverified.
