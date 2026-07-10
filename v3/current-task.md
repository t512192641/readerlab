# ReaderLab V3 当前任务

状态：静态重构已获用户接受并形成独立干净提交；下一步只准备 fresh 小 Demo 方案。未批准真实运行。

## 已接受范围

- 约束架构、两线协议、角色合同、manifest 与文档生命周期分类。
- Standards / Spec 最终静态终验均 `pass`、0 blocker。
- 29/29 回归匹配；运行完整性 7/7 仅为派生结构验证、`runtime-not-run`。

## 下一切片动作

1. 只读检查登记的 022 原始材料，不读取旧生成中间产物作为输入。
2. 提出 fresh 小 Demo 的精确样本、任务预算、全新隔离目录和验收范围；不运行。
3. 等用户确认样本与声明范围后，才创建 run manifest 并开始真实执行。

## 已完成验证

- `git diff --check` 与新 Markdown 检查通过。
- 独立提交只包含 A 组；B 组保持未跟踪且未进入提交。
- 最终证据：`v3/eval/constraint-redesign-r2/review-standards-final-rerun-raw.md`、`review-spec-final-rerun-raw.md`。

## 不可声称与暂停条件

- 没有真实 fresh/revision run；图书线、Skill 线、Phase 4 和 ReaderLab 流水线均未通过。
- 未经用户确认具体样本，不运行 Demo；不启动 gstack/browse、Phase 5 或 LifeAtlas 回写。
- 不移动、删除、覆盖 B 组历史文件；若 staged 边界混入 B 组，立即停止提交并修正。

## 下一次用户确认

- 用户只需审查并确认将要提出的 fresh 小 Demo 样本与运行范围；确认前保持 `runtime-not-run`。
