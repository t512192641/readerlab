# Baseline Output

## Prompt Shape

```text
把 docs/product-spec.md 做成一个可读的 ReaderLab 材料。
```

## Likely Baseline Behavior Without Skill

A generic answer would likely summarize the product specification into a few sections:

- ReaderLab 是什么
- 它不是什么
- 产品原则
- 输出结构
- 阶段路线

## Missing Or Weak

- It may not preserve `docs/product-spec.md` as a body track.
- It may not create or require `10_一手正文/`.
- It may not distinguish reader-facing material from audit contracts.
- It may not force route selection before writing the output.
- It may not end with human review instead of implying acceptance.
- It may expose internal status language in reader-facing text.

## Baseline Verdict

Status: `fail_for_readerlab_package`

Reason: a summary can explain the product spec, but it does not produce a body-first ReaderLab reading package.
