# Current Task

## Authority

本文件是当前执行事实的唯一入口。若 `docs/dev-state.md`、`docs/progress.md`、`docs/next-session-prompt.md`、旧报告或旧 handoff 与本文件冲突，以本文件为准。

## 当前切片

继续 ReaderLab《埃隆之书》单书闭环，但当前阶段已被 GPT Pro review 纠偏：已有产物只能证明 reader-facing 高阶讲解能力，不能证明完整 ReaderLab 阅读包，也不能证明可迁移方法核或 Skill 已成立。

当前阶段是：

```text
GPT Pro review 第八部分行动已执行
-> 状态口径重命名
-> 新增方法核 contracts
-> 两章最小方法核探针
-> 两个内部产品 demo 已通过 writer/reader 双门槛
-> 等用户明确决定是否准备 GPT Pro 审核
```

不要进入正式 ReaderLab Skill 草案、外部书验证、更大范围扩章或 GPT Pro 审核包，除非两个新 demo 已内部通过且用户明确启动审核。

## 当前状态口径

必须使用以下口径：

- `chapter_high_order_explanation_pass`: `15/15`
- `full_book_reader_synthesis_pass`: `1/1`
- `baseline_capability_audit_pass`: `1/1`
- `reader_package_not_verified`
- `transferable_method_kernel_probe_pass`: `2/2`，仅限 `组织设计 / v101-16` 和 `打造特斯拉 / v101-21` 的最小探针
- `two_demo_internal_pass`: `2/2`，仅限 `readerlab-two-demo-run-v0` 的 Demo A / Demo B 内部 writer-reader 验证
- `transferable_method_kernel_pass`: `not_verified`
- `skill_draft_not_started`
- `external_material_validation_not_started`

禁止使用的旧口径：

- 不得把 15 章高阶讲解通过称为 `reader_package_pass`。
- 不得把章节 reader 页称为完整 ReaderLab 阅读包。
- 不得把 baseline 横评通过称为方法论或 Skill 草案完成。
- 不得把两章方法核探针称为可迁移方法已经成立。

## 新增方法核证据

GPT Pro 第八部分要求的六个 contract 已新增：

- `docs/contracts/body-track-gate-v1.md`
- `docs/contracts/material-profile-v1.md`
- `docs/contracts/claim-ledger-v1.md`
- `docs/contracts/candidate-tournament-v1.md`
- `docs/contracts/skillization-gate-v1.md`
- `docs/contracts/annotation-trigger-v1.md`

两章最小方法核探针：

- `docs/reports/readerlab-method-kernel-v0/`
- `docs/reports/readerlab-method-kernel-v0/chapters/03_组织设计/`
- `docs/reports/readerlab-method-kernel-v0/chapters/07_打造特斯拉/`
- `docs/reports/readerlab-method-kernel-v0/eval.md`

探针结论：

- 方法核探针：`pass`。
- 完整阅读包：`not_verified`。
- 两章 reader-facing 页是高阶讲解产物，不是完整阅读包页。
- Body Track Gate 明确阻止无完整一手正文轨的章节被标成 `reader_package_pass`。

## 双 demo 内部结果

用户已明确：现在不要写 GPT Pro 审核 prompt。已按合同跑完两个新 demo，两个 demo 均内部通过；是否准备 GPT Pro review packet 仍需用户明确启动。

执行合同：

- `docs/reports/readerlab-two-demo-run-v0/README.md`
- `docs/reports/readerlab-two-demo-run-v0/01_NEXT_SESSION_PROMPT.md`

两个 demo：

1. Demo A：`docs/product-spec.md` 作为 repo-owned longform，完整正文轨落在 `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/10_一手正文/001_正文.md`；reader evaluation：`pass`，`11/12`，无 P0/P1。边界：这证明 repo-owned longform reader package 最小形态，不证明外部书泛化。
2. Demo B：`/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md` 作为 Skill / 工程材料阅读源；净化正文、设计资产、Skillization Gate 和批注触发落在 `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/`；reader evaluation：`pass`，`11/12`，无 P0/P1。边界：只作为阅读材料，未安装、同步或启用 Skill。

主控验证：

- `python3 -m json.tool`：全部 demo JSON 通过。
- reader-facing 禁用内部字段扫描：无命中。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

## 默认读取与动作触发

启动时只读 `AGENTS.md` 和本文件。不要因为本文件列出路径，就在启动阶段展开读取。

执行中按动作触发读取：

- 要复核 GPT Pro 第八部分方案时，读 `~/Downloads/chatgpt-selected-2026-07-01T02-41-22.md`。
- 要复核两章方法核探针时，读 `docs/reports/readerlab-method-kernel-v0/README.md` 和 `docs/reports/readerlab-method-kernel-v0/eval.md`，再按需读具体章节 artifact。
- 要跑下一轮两个 demo 时，先读 `docs/reports/readerlab-two-demo-run-v0/README.md`，再按该合同选择源、调用 writer/reader、落地产物。
- 要更新方法核 contract 时，只读对应 `docs/contracts/*-v1.md`。
- 要确认章节阶段历史结果时，读 `docs/reports/readerlab-elon-chapter-loop-v0/chapter-queue.md`。
- 要追加运行历史时，只读 `docs/agent-run-ledger.md` 顶部最新两条。

按需读取：

- 产品边界：`docs/product-spec.md`
- 包结构：`docs/readerlab-package-spec.md`
- 稳定路径和工具状态：`docs/dev-state.md`
- 耐久决策：`docs/decisions.md`，优先 D-052 之后
- 验收 gate：`docs/eval-gates.md`
- baseline 研究线索：`docs/research-log.md`

不要启动时通读旧 fullbook、bakeoff、long reports、原始聊天或历史账本。

## 下一步

当前最小下一步不是写 Skill，也不是外部书验证，也不是自动提交 GPT Pro 审核。两个内部 demo 已通过，下一步只能由用户决定是否准备 GPT Pro review packet。

若用户明确启动 GPT Pro review packet，审查重点应围绕：

1. Body Track Gate 是否用完整正文轨防止解释页冒充阅读包。
2. Claim Ledger 是否真的约束 reader-facing 表述，而不是只补字段。
3. Candidate Tournament 是否产生真实 promote / downgrade / reject 决策。
4. Skillization / Annotation 分流是否阻止 insight 被过早 Skill 化。
5. Reader-facing narrative 是否确实消费前面 gate 输出，而不是自由发挥。
6. Skill / 工程 demo 是否产出净化正文和设计资产，而不是摘要和术语解释。

不得自动进入正式 Skill 草案、外部书验证或 GitHub 发布。不得把 Demo A 的 repo-owned longform 结果表述成外部书籍泛化通过。

## 高阶讲解通过线

章节级高阶讲解硬门槛任一失败则不能 `chapter_high_order_explanation_pass`：

- reader-facing 不暴露 `source refs`、`claim trace`、`lens score`、`machine/human status` 等内部字段。
- 有明确升维问题，不是章节摘要。
- 有正文内部机制链。
- 至少一个镜头反向照亮正文，不抢正文。
- 自然完成吸收 / 降级 / 拒绝。
- 不美化长工时、创伤、强控制或英雄崇拜。
- 不把局部章节升格成全书结论。

读者评分六项，每项 0-2：重新理解、正文贴合、机制清晰、镜头有效、边界锋利、表达穿透。

通过条件：硬门槛全过，读者分至少 `10/12`，读者评价 agent 给出 `pass`，且没有 P0/P1。

## Reader Package Body Track Gate

书籍 / 长文页要进入 `reader_package_pass`，必须先过 Body Track Gate：

- 页面包含完整章节一手正文，或显式链接到 `10_一手正文/` 下的完整正文文件。
- 高阶讲解页、导读页、摘要页不能替代一手正文。
- “讲解贴合正文锚点”不能替代“一手正文存在”。
- 如果没有完整一手正文轨，该页最多只能标为 `high_order_explanation_pass`。

## 错误退出

- 无完整一手正文轨却标成 `reader_package_pass`：立即停止并纠正状态。
- candidate pool 只有字段、没有影响 promote / downgrade / reject：探针失败。
- 没有 rejected / downgraded 项却声称完成筛选：探针失败。
- 高层判断没有 claim tier：探针失败。
- 把 AI composite interpretation 写成作者原意：探针失败。
- insight 不满足 trigger / input / steps / output / boundary / evidence 却 Skill 化：探针失败。
- annotation question 没有 body-adjacent anchor：探针失败。
- reader-facing 暴露内部字段：该轮不能通过。
- compliant longform body source 缺失：停止，不用假正文、摘要或《埃隆之书》版权章节硬凑 demo。
- 只有一个 demo 通过：不能准备 GPT Pro 审核包。
- 章节高阶讲解未完成前进入全书总结或 final boss：历史错误，不能重复。
- 两个内部 demo 未通过前进入正式 Skill 草案、外部书验证或 GPT Pro 审核：停止并纠正计划。

## Stable Paths

- GPT Pro review 文件：`~/Downloads/chatgpt-selected-2026-07-01T02-41-22.md`
- EPUB：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- 章节队列：`docs/reports/readerlab-elon-chapter-loop-v0/chapter-queue.md`
- 章节轮次：`docs/reports/readerlab-elon-chapter-loop-v0/rounds.md`
- 方法核探针：`docs/reports/readerlab-method-kernel-v0/`
- 双 demo 执行合同：`docs/reports/readerlab-two-demo-run-v0/README.md`
- 双 demo 下一会话 prompt：`docs/reports/readerlab-two-demo-run-v0/01_NEXT_SESSION_PROMPT.md`
- 高阶讲解方法：`docs/high-order-explanation-method.md`
- 高阶讲解 contract：`docs/contracts/high-order-explanation-v1.md`
- 验收 gate：`docs/eval-gates.md`
