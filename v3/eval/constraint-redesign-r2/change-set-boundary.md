# 约束重构返工：可分离变更边界

基线：`HEAD 1ed34c4`。本文件只定义建议审查/提交边界；没有暂存、提交、移动、删除或覆盖任何现有文件。

## A. 本轮约束返工集

- 入口与稳定概览：`AGENTS.md`、`v3/README.md`、`v3/current-task.md`、`v3/document-map.md`。
- 总架构与线路规则：`v3/standards/constraint-architecture.md`、`v3/skill/SKILL.md`、`v3/skill/protocols/`。
- 裁剪角色与运行合同：`v3/skill/roles/`、`v3/skill/templates/run-manifest.md`。
- 读者模板、范例与评分接口：本轮已修改的 `v3/skill/templates/`、`v3/skill/examples/`、`v3/standards/book-annotation-rubric.md`、`v3/standards/skill-craft-rubric.md`。
- 真实运行闸门与状态回填：`v3/standards/phase4-pilot-definition.md`、`v3/standards/calibration-log.md` 中 2026-07-10 的约束重构及返工更正记录。
- 回归证据包：`v3/standards/regression-suite.md`、`v3/standards/regression-cases/`、`v3/eval/constraint-redesign-r2/`。

## B. 明确排除并原样保留

- 旧 022 R1/R2 成品：`v3/pilots/022-abundance-phase4-r1.md`、`v3/pilots/022-abundance-phase4-r2.md`。
- 旧 022 R1/R2 audit 与候选：`v3/audit/022-abundance-phase4-r1.md`、`v3/audit/022-abundance-phase4-r2.md`、三份 `v3/audit/022-abundance-phase4-r2-candidates-*.md`。
- 旧版式 Demo：`v3/pilots/prototype-022-extension-layout-demo/`。
- 已消费的一次性启动提示：`v3/next-session-prompt.md`。
- 已退出默认活动层的设计合同：`v3/standards/phase4-constraint-redesign-contract.md`。

## Dirty worktree 保护

- B 组均为基线外未跟踪文件，不能把“未跟踪”误判成“本轮新建”；本轮未改、未删、未移动。
- `v3/standards/calibration-log.md` 与 `v3/standards/phase4-pilot-definition.md` 在返工前已有未提交改动；审查时需按具体 hunk 区分既有记录和本轮更正，不能整文件归因给本轮。
- 若后续需要形成物理提交，应只按 A 组逐文件/逐 hunk 暂存，并在提交前再次核对 `git status --short`；本轮不执行该动作。

## 可声称范围

该边界只证明约束返工文件可与旧 022/Demo 产物分开审查；不证明工作区干净，不证明真实运行、内容质量或 ReaderLab 流水线通过。
