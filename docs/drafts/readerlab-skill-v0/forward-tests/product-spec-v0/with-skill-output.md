# With-Skill Output

## Prompt Shape

```text
Use the draft ReaderLab Skill at docs/drafts/readerlab-skill-v0/SKILL.md to turn docs/product-spec.md into a ReaderLab reading package preview.
```

## Request Object

```json
{
  "material_id": "readerlab-product-spec",
  "title": "ReaderLab Product Spec",
  "source_paths": [
    "docs/product-spec.md"
  ],
  "output_root": "docs/drafts/readerlab-skill-v0/forward-tests/product-spec-v0/preview-package",
  "permission_boundary": "private_only",
  "intended_reader": "ReaderLab product owner and future implementing agents",
  "requested_scope": "file",
  "human_review_required": true
}
```

## Route Decision

```json
{
  "route": "book_or_longform",
  "body_mode": "full_body",
  "reason": "The source is a repo-owned conceptual product specification being read as material. It has no runtime shell or host-specific execution boilerplate to clean away. The reader needs the complete product contract."
}
```

## Expected Package Shape

```text
README.md
source-registry.json
10_一手正文/001_正文.md
20_AI陪读/001_reader-facing.md
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

## Reader-Facing Shape

The reader-facing page should explain, in natural Chinese:

- 这份产品规格在界定 ReaderLab 的根问题：复杂材料如何被吸收，而不是被摘要替代。
- 当前材料应先作为正文被完整阅读；AI 陪读只负责降低理解门槛。
- 关键风险是把 ReaderLab 做成摘要器、自动知识库升格器或 Skill 专项工具。
- 批注和沉淀必须保留人工判断边界。

It should not display internal audit labels listed in `docs/current-task.md`.

## Human Review Handoff

```text
machine checks: pending
fixture replay: already available from existing A/B private validation fixture
real Obsidian UI replay: deferred
human status: pending
allowed next step: revise package or run real Obsidian UI replay
```

## With-Skill Verdict

Status: `pass_for_forward_test_design`

Reason: the draft Skill forces route selection, body preservation, output shape, audit separation, and human review boundaries.
