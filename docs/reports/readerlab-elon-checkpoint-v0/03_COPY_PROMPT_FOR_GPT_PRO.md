# Copy Prompt for GPT Pro

请审查 ReaderLab private checkpoint。不要重写《埃隆之书》总结，不要直接写 ReaderLab Skill。

仓库已经改为 private，并由 Codex GitHub app 核验 `visibility: private`。因此这次 review packet 包含一个 private/copyrighted longform 的完整正文轨。请只把它作为 private repository review 材料，不要当作 public-domain / publicly redistributable source。

这次有两层证据：

第一层是上轮 two-demo internal checkpoint：

1. Demo A：长文完整正文轨 demo。材料是 `docs/product-spec.md`，作为 repo-owned longform。它产出完整正文文件和一页 AI 陪读，目的是证明书籍 / 长文类阅读包必须有一手正文轨，AI 讲解不能替代正文。它不证明外部书籍泛化，也没有提交《埃隆之书》版权正文。
2. Demo B：Skill / 工程材料 demo。材料是 `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md`，只作为阅读材料，不安装、不同步、不启用。它产出净化正文、AI 陪读和设计资产说明，目的是证明 ReaderLab 能把复杂 Skill 文档里的命令、机器协议和执行外壳剥离出去，同时保留用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点。

第二层是这轮 private material validation：

3. Demo A2：私有长文 / 书籍完整正文轨 demo。材料是 `Feel-Good Productivity 全书完整中译.pdf`，完整正文轨位于 `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/10_一手正文/001_正文.md`。它验证 ReaderLab 在 private longform 上能否保留完整正文轨，并让 AI 陪读从属于正文。它不是 public-source redistribution proof。
4. Demo B2：本地 Skill / 工程材料 demo。材料是 `/Users/tianqiang/wechatFile/01_Skills/Agent技能合集包/planning-with-files/SKILL.md`。它验证 ReaderLab 是否能从另一份 Skill 材料中生成净化正文、设计资产、source-cleaning-map、location-map、trace-to-reader 和 contracts，并区分可迁移方法与宿主插件运行外壳。

请判断这四个 demo/validation artifact 合在一起，是否足以让 ReaderLab 从“受限内部方法核雏形”进入“正式 ReaderLab Skill 交付设计”。不要把它升级成 `transferable_method_kernel_pass`，除非你认为证据确实足够；如果仍不足，请说清最小缺口。

注意：GPT Pro 已指出批注插件本身不是主要风险；风险是批注回读时能否从评论位置稳定回到正文 anchor、claim、candidate 和 gate 决策。本轮已补 `location-map.json` 和 `trace-to-reader.md`，请重点审这条证据链是否够用。

你应先读：

1. `docs/current-task.md`
2. `docs/reports/readerlab-two-demo-run-v0/README.md`
3. `docs/reports/readerlab-elon-checkpoint-v0/00_GPT_PRO_REVIEW_BRIEF.md`
4. `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/README.md`
5. `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/eval.md`
6. `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/20_AI陪读/001_reader-facing.md`
7. `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/README.md`
8. `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/eval.md`
9. `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/10_一手正文/001_净化正文.md`
10. `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/20_AI陪读/001_reader-facing.md`
11. `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/20_AI陪读/design-asset-notes.md`
12. `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/location-map.json`
13. `docs/reports/readerlab-two-demo-run-v0/demos/A_longform_body_track/audit/trace-to-reader.md`
14. `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/location-map.json`
15. `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/source-cleaning-map.md`
16. `docs/reports/readerlab-two-demo-run-v0/demos/B_skill_engineering/audit/trace-to-reader.md`
17. `docs/reports/readerlab-private-material-validation-v0/README.md`
18. `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/README.md`
19. `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/eval.md`
20. `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/20_AI陪读/001_reader-facing.md`
21. `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/README.md`
22. `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/eval.md`
23. `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/10_一手正文/001_净化正文.md`
24. `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/20_AI陪读/001_reader-facing.md`
25. `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/20_AI陪读/design-asset-notes.md`

然后读两个 demo 的核心 contracts：

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
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/source-registry.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/location-map.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/trace-to-reader.md`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/body-track-gate.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/claim-ledger.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/candidate-tournament.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/skillization-gate.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/A_feel_good_productivity/audit/contracts/annotation-trigger.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/source-registry.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/location-map.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/source-cleaning-map.md`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/trace-to-reader.md`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/body-track-gate.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/claim-ledger.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/candidate-tournament.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/skillization-gate.json`
- `docs/reports/readerlab-private-material-validation-v0/demos/B_planning_with_files/audit/contracts/annotation-trigger.json`

按需再读：

- `docs/reports/readerlab-elon-checkpoint-v0/01_REQUIRED_FILES.md`
- `docs/reports/readerlab-elon-checkpoint-v0/02_OPTIONAL_ATTACHMENTS.md`
- `docs/contracts/*-v1.md`
- `docs/reports/readerlab-method-kernel-v0/README.md`
- `docs/reports/readerlab-method-kernel-v0/eval.md`
- `docs/eval-gates.md`

请重点回答：

1. 两个 demo 是否真的证明了 ReaderLab 最小阅读包方法核，而不是只证明写作能力？
2. Demo A 的 Body Track Gate 是否足够硬，能防止高阶讲解页冒充完整阅读包？
3. Demo B 的净化正文是否不是摘要，是否保留了用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点？
4. Claim Ledger 是否真实约束 reader-facing 表述，避免把 AI 解释写成作者原意？
5. Candidate Tournament 是否真实产生 promote / downgrade / reject，而不是装饰字段？
6. Skillization Gate 是否阻止了不满足 trigger / input / steps / output / boundary / evidence 的 insight 被过早 Skill 化？
7. Annotation Trigger 是否真的给出 body-adjacent questions，而不是泛泛讨论题？
8. location-map / trace-to-reader 是否足够把 Obsidian 批注接回 ReaderLab 证据链？
9. Demo B 的 source-cleaning-map 是否足够说明 `gstack/spec` 的净化过程？
10. private material validation 是否足以缓解上一轮“只用 repo-owned longform / gstack 单源”的证明力不足？
11. 现在是否可以进入正式 ReaderLab Skill 交付设计？如果可以，启动前必须保留哪些 stop conditions？

请输出：

- `Verdict`
- `What is proven`
- `What is still not proven`
- `P0/P1 risks`
- `Assessment of Demo A`
- `Assessment of Demo B`
- `Assessment of Private Material Validation`
- `Smallest next action toward usable ReaderLab Skill`
- `Stop conditions before Skill draft`
