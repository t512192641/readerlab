# Required Files for GPT Pro Review

建议先读这些文件，不要一开始读完整仓库。

## 必读 1：当前事实入口

- `docs/current-task.md`

目的：确认当前状态口径、阶段边界、两个 demo 内部通过事实，以及仍未启动正式 Skill / 外部材料验证。

## 必读 2：本轮执行合同

- `docs/reports/readerlab-two-demo-run-v0/README.md`

目的：确认两个 demo 的目标、边界、停止条件、writer / reader 分工和通过线。

## 必读 3：本 brief

- `docs/reports/readerlab-elon-checkpoint-v0/00_GPT_PRO_REVIEW_BRIEF.md`

目的：明确这次审查不是重写总结，而是审 two-demo 方法核验证是否成立。

## 必读 4：Demo A 入口和评价

- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/README.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/eval.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/20_AI陪读/001_reader-facing.md`

目的：判断完整正文轨、AI 陪读、reader evaluation 和 reader-facing 边界是否成立。

## 必读 5：Demo B 入口和评价

- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/README.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/eval.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/10_一手正文/001_净化正文.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/20_AI陪读/001_reader-facing.md`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/20_AI陪读/design-asset-notes.md`

目的：判断净化正文是否不是摘要、设计资产是否有效、reader-facing 是否没有内部字段污染。

## 必读 6：两个 demo 的核心 contracts

- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/contracts/body-track-gate.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/contracts/claim-ledger.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/contracts/candidate-tournament.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/contracts/skillization-gate.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/contracts/annotation-trigger.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/contracts/body-track-gate.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/contracts/claim-ledger.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/contracts/candidate-tournament.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/contracts/skillization-gate.json`
- `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/contracts/annotation-trigger.json`

目的：判断 gates 是否真实改变输出决策，而不是只作为审计字段。
