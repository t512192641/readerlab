# Optional Attachments

这些文件按需读取。不要一开始全部展开。

## Demo A 完整正文轨

- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/10_一手正文/001_正文.md`
- `docs/product-spec.md`

用途：确认 Demo A 的正文轨确实完整保留 repo-owned longform 源，而不是 AI 摘要或改写。

## Private Demo A2 完整正文轨

- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/10_一手正文/001_正文.md`

用途：确认 private longform 的完整正文轨存在。注意：这是 private/copyrighted material，只能在 private repository review 中使用。

## Private demo 完整 contracts

- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/body-track-gate.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/material-profile.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/claim-ledger.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/candidate-tournament.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/skillization-gate.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/annotation-trigger.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/high-order-explanation.v1.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/body-track-gate.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/material-profile.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/claim-ledger.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/candidate-tournament.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/skillization-gate.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/annotation-trigger.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/high-order-explanation.v1.json`

用途：需要复核 private material validation 的 claim tier、candidate decisions、Skillization、annotation triggers 和 high-order explanation contract 时读取。

## 两个 demo 的完整 contract

- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/location-map.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/trace-to-reader.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/contracts/material-profile.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/contracts/high-order-explanation.v1.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/location-map.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/source-cleaning-map.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/trace-to-reader.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/contracts/material-profile.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/contracts/high-order-explanation.v1.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/source-registry.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/source-registry.json`

用途：需要追踪来源、材料类型、AI 解释边界、高阶讲解内部证据、清理过程、reader-facing trace 和批注回读锚点时读取。

## 方法核 contract 定义

- `docs/contracts/body-track-gate-v1.md`
- `docs/contracts/material-profile-v1.md`
- `docs/contracts/claim-ledger-v1.md`
- `docs/contracts/candidate-tournament-v1.md`
- `docs/contracts/skillization-gate-v1.md`
- `docs/contracts/annotation-trigger-v1.md`
- `docs/contracts/high-order-explanation-v1.md`

用途：判断 demo contracts 是否符合当前方法核定义。

## 两章方法核探针

- `docs/reports/readerlab-method-kernel-v0/README.md`
- `docs/reports/readerlab-method-kernel-v0/eval.md`
- `docs/reports/readerlab-method-kernel-v0/chapters/03_组织设计/`
- `docs/reports/readerlab-method-kernel-v0/chapters/07_打造特斯拉/`

用途：需要比较 two-demo 之前的最小方法核探针时读取。注意：两章探针只证明方法核局部成立，不证明完整阅读包。

## 原章节 / baseline 历史证据

- `docs/reports/readerlab-elon-chapter-loop-v0/chapter-queue.md`
- `docs/reports/readerlab-elon-chapter-loop-v0/reader/16_ReaderLab全书总结_阅读页.md`
- `docs/reports/readerlab-elon-chapter-loop-v0/audit/evals/16_ReaderLab全书总结.eval.md`
- `docs/reports/readerlab-elon-chapter-loop-v0/audit/evals/17_baseline横向对比.eval.md`

用途：只在需要确认旧状态为什么被降级为 reader-facing 高阶讲解通过时读取。

## 项目规则与验收

- `AGENTS.md`
- `docs/product-spec.md`
- `docs/readerlab-package-spec.md`
- `docs/eval-gates.md`
- `docs/high-order-explanation-method.md`

用途：判断 ReaderLab 是否偏离产品边界、正文优先原则和 reader-facing / audit 分离原则。
