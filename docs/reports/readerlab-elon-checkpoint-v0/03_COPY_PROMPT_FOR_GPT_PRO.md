# Copy Prompt for GPT Pro

请审查 ReaderLab two-demo checkpoint。不要重写《埃隆之书》总结，不要直接写 ReaderLab Skill，不要做外部书验证。

这轮只有两个 demo：

1. Demo A：长文完整正文轨 demo。材料是 `docs/product-spec.md`，作为 repo-owned longform。它产出完整正文文件和一页 AI 陪读，目的是证明书籍 / 长文类阅读包必须有一手正文轨，AI 讲解不能替代正文。它不证明外部书籍泛化，也没有提交《埃隆之书》版权正文。
2. Demo B：Skill / 工程材料 demo。材料是 `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md`，只作为阅读材料，不安装、不同步、不启用。它产出净化正文、AI 陪读和设计资产说明，目的是证明 ReaderLab 能把复杂 Skill 文档里的命令、机器协议和执行外壳剥离出去，同时保留用途、触发条件、用户意图、流程、约束、失败条件、输出要求和设计亮点。

请判断这两个 demo 是否真的证明了 ReaderLab 最小方法核，而不是只证明写作能力或补齐审计字段。

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
8. 两个 demo 内部通过后，下一步是否应进入外部 GPT Pro 审核后的更广泛材料验证，还是仍需补一个更小的内部缺口？

请输出：

- `Verdict`
- `What is proven`
- `What is still not proven`
- `P0/P1 risks`
- `Assessment of Demo A`
- `Assessment of Demo B`
- `Smallest next action`
- `Stop conditions before Skill draft`
