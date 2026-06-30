# ReaderLab Elon Full Product v1

## 结论

这是《埃隆之书》ReaderLab v1 试产包。v1 不继续修补 v0 的 5 个短 reader 页，而是把读者侧收敛成一篇主阅读稿，再把来源、方法吸收和自检放到审计附录。

当前状态：repo 内手工试产样张，人工阅读质量仍待复核，不是 product ready。

## 打开顺序

1. `reader/01_主阅读稿.md`：给读者直接阅读、批注和讨论的一篇主稿。
2. `audit/method-absorption.md`：说明仓颉、李继刚式深读、乔木共读、book-to-skill 和 ReaderLab 各自被吸收到哪里。
3. `audit/candidate-evidence.v1.json`：候选筛选、V1/V2/V3 证据链、location refs 和 5 个能力候选验证。
4. `audit/90_来源与审计.md`：说明来源、契约引用、人工状态和验证边界。
5. `assertions.md`：v1 自检和 ELON-A01 到 ELON-A13 逐项状态。

## v1 相对 v0 的主要变化

- 不再使用 `framework/principle/case` 等读者无收益的内部类型标签。
- 不再写“先读前言、再读第一部分”这类空泛阅读路线。
- 把“阅读路线”改成正文附近问题、批注触发和误读纠偏。
- 把深读开头改成材料边界、缺口、增量、不增量、机制链和认知旅程。
- 把仓颉式候选池、通过/降级/拒绝链显式写入主稿。
- 只保留 5 个可执行能力，每个都有 `trigger / input / steps / output / boundary`。
- 把完整候选证据链和能力候选验证放进 `audit/candidate-evidence.v1.json`。
- 来源和质量边界放入审计页，不污染主阅读稿。

## 输入证据

- v0 读者页：`docs/reports/readerlab-elon-full-product-v0/reader/*.md`
- v0 契约：`docs/reports/readerlab-elon-full-product-v0/contracts/*.json`
- method bakeoff：`docs/reports/readerlab-elon-method-bakeoff-v0/`
- Meta Skill output eval 口径：`/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/references/output-eval-method.md`

## 明确没有做

- 没有写入 LifeAtlas `300/600/800`。
- 没有修改 EPUB。
- 没有新增依赖。
- 没有修改 `scripts/readerlab.py`。
- 没有更新 `docs/current-task.md`、`docs/dev-state.md`、`docs/agent-run-ledger.md`。
- 没有把 validator 绿灯或文件存在说成人工阅读质量通过。
