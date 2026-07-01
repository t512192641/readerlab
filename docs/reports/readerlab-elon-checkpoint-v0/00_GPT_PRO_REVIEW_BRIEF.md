# ReaderLab Two-Demo Checkpoint - GPT Pro Review Brief

## 审查目的

这次不是请你重写《埃隆之书》总结，也不是请你直接写 ReaderLab Skill。

这次请审查：ReaderLab 在 GPT Pro 上轮纠偏后，是否已经用两个内部 demo 证明了最小方法核能产出真实阅读包雏形，而不只是补了字段或写了漂亮讲解。

## 这轮两个 demo 是什么

| Demo | 材料 | 读者看到什么 | 审查它证明什么 | 不证明什么 |
|---|---|---|---|---|
| Demo A：长文正文轨 | `docs/product-spec.md`，repo-owned longform | 完整正文文件 + 一页自然中文 AI 陪读 | 书籍 / 长文类材料必须先有完整一手正文轨，AI 讲解不能替代正文 | 不证明外部书籍泛化，也不使用《埃隆之书》版权正文 |
| Demo B：Skill / 工程材料 | `gstack/spec/SKILL.md`，只作为阅读材料 | 净化正文 + AI 陪读页 + 设计资产说明 | 工程 Skill 材料可以剥离命令和机器协议，保留用途、触发、流程、约束、失败条件、输出要求和设计亮点 | 不代表正式 ReaderLab Skill 已写成，也不安装、同步或启用 gstack |

这两个 demo 的共同审查点：正文轨 / 净化正文是否成立，AI 陪读是否不冒充原文，contracts 是否真实影响 promote / downgrade / reject、Skillization 和批注触发，而不是只补字段。

GPT Pro two-demo review 后已补一个 review hardening patch：

- Demo A / B 增加 `audit/location-map.json`，把正文段落、读者页段落、claim、candidate 和 annotation trigger 接到稳定 anchor。
- Demo A / B 增加 `audit/trace-to-reader.md`，说明 reader-facing 每段如何消费 claim ledger、candidate tournament 和 gate 决策。
- Demo B 增加 `audit/source-cleaning-map.md`，说明 `gstack/spec` 的源内容如何被保留、压缩、移入设计资产、移入 audit 或拒绝进入 reader-facing。
- `body-track-gate.v1` 增加 `skill_engineering_cleaned_body_pass`，用于区分 Skill / 工程材料 cleaned-body 通过和书籍/长文完整 reader package 通过。
- 批注层本轮不重新验证 Obsidian 插件 UI；补的是批注回读时从评论位置回到正文 anchor、claim、candidate 和 gate 的证据链。

当前状态口径以 `docs/current-task.md` 为准：

- `chapter_high_order_explanation_pass`: `15/15`
- `full_book_reader_synthesis_pass`: `1/1`
- `baseline_capability_audit_pass`: `1/1`
- `reader_package_not_verified`
- `transferable_method_kernel_probe_pass`: `2/2`
- `two_demo_internal_pass`: `2/2`
- `transferable_method_kernel_pass`: `not_verified`
- `skill_draft_not_started`
- `external_material_validation_not_started`

## 本轮新增证据

本轮按 `docs/reports/readerlab-two-demo-run-v0/README.md` 跑了两个内部 demo。

Demo A：书籍 / 长文完整正文轨 demo

- 源：`docs/product-spec.md`
- 类型：repo-owned longform，不是外部书籍泛化验证。
- 产物：`docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/`
- 目的：证明完整一手正文轨存在时，AI 陪读页不能替代正文，Body Track Gate 能阻止解释页冒充阅读包。
- reader evaluation：`pass`，`11/12`，P0/P1 为空。

Demo B：Skill / 工程材料 demo

- 源：`/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md`
- 类型：Skill / engineering reading material；只作为阅读材料，未安装、同步或启用。
- 产物：`docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/`
- 目的：证明净化正文、设计资产提炼、Skillization Gate 和批注触发能处理复杂工程 Skill 文档。
- reader evaluation：`pass`，`11/12`，P0/P1 为空。

## 主控验证

本地验证结果：

- 全部 demo JSON contract 通过 `python3 -m json.tool`。
- reader-facing 页禁用字段扫描无命中：`source refs`、`claim trace`、`lens score`、`machine_status`、`human_status`、`Body Track Gate`、`Claim Ledger`、`Candidate Tournament`、`Skillization Gate`、`Annotation Trigger` 均未暴露在 `20_AI陪读`。
- `python3 tests/test_readerlab.py`：PASS，30 tests OK。
- `git diff --check`：PASS。

## 请重点判断

请不要输出泛泛表扬。请直接判断：

1. 两个 demo 是否真的证明了 ReaderLab 最小阅读包方法核，而不是只证明写作能力？
2. Demo A 的 Body Track Gate 是否足够硬，能防止高阶讲解页冒充完整阅读包？
3. Demo B 的净化正文是否保留了用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点，而不是摘要？
4. Claim Ledger 是否真实约束 reader-facing 表述，避免把 AI 解释写成作者原意？
5. Candidate Tournament 是否真实产生 promote / downgrade / reject，而不是装饰字段？
6. Skillization Gate 是否阻止了不满足 trigger / input / steps / output / boundary / evidence 的 insight 被过早 Skill 化？
7. Annotation Trigger 是否真的给出 body-adjacent questions，而不是泛泛讨论题？
8. 新增的 location-map / trace-to-reader 是否足够连接 Obsidian 批注和 ReaderLab 证据链？
9. Demo B 的 source-cleaning-map 是否足够缓解“净化正文不可复核”的风险？
10. 这两个 demo 内部通过后，下一步是否应该准备更广泛材料验证，还是仍需补一个更小的内部缺口？

## 已知边界

- Demo A 是 repo-owned longform，不证明外部书籍泛化。
- Demo B 使用 `gstack/spec` 作为阅读材料，不代表 ReaderLab 已经写成正式 Skill。
- 当前仍不得称为 `transferable_method_kernel_pass`。
- 当前仍不得称为正式 ReaderLab Skill 已启动或完成。
- 当前不得把 15 章高阶讲解通过称为完整 ReaderLab 阅读包通过。

## 希望输出

请按以下结构回答：

1. `Verdict`
2. `What is proven`
3. `What is still not proven`
4. `P0/P1 risks`
5. `Assessment of Demo A`
6. `Assessment of Demo B`
7. `Smallest next action`
8. `Stop conditions before Skill draft`
