# Expert Teaching Skill v0.1.2 两样本迁移验证 ledger

状态：两组 run 均 `PRODUCT_READY`，技术验证完成；产品负责人审阅与 `accepted` 仍待完成。本轮已停止，不启动 Writer、不修改 Skill、不发布 0.1.3。

## 固定控制信息

- 基线 commit：`3fe6d42fa2fb6fa9440ebb62b05066993f804619`
- 分支：`experiment/expert-teaching-v0.1.2-migration`
- Skill：`readerlab-book-expert-teaching 0.1.2`
- Skill aggregate fingerprint：`da7b0083e4b245df0a81aae0d4124adfd3fc69e015b17819aef08a5cb4e7b818`
- Expert：`gpt-5.6-sol / high`
- Independent Review：`gpt-5.6-terra / high`
- 每个角色均单次调用；无语义重试、无 prompt 修改、无跨样本回灌。
- 预注册计划 SHA-256：`77edf8a3479ffab01baa128cc8637d3b1a478c066d581650a919d77b7d7e0da5`
- 两组输入均在首次语义调用前完成 `init` 并冻结；正式输入 hash 见计划文件及各自 `run-manifest.md`。

## 样本与运行终局

### A：机制／预测型 · T2.35 神圣价值与禁忌交换

- 原文：T2.35 冻结第 8 章《宗教：神祇只是为国家服务》。
- 框架：神圣价值与不可妥协／禁忌交换；关注不可交易性、禁忌交换、物质加码可能反噬，以及谈判和决策边界。
- run：[runs/EXPERT-TEACHING-V0.1.2-MIGRATION-A-T2.35-01/](../runs/EXPERT-TEACHING-V0.1.2-MIGRATION-A-T2.35-01/)
- Expert Agent：`019fae15-dac4-7bd1-bf48-5c494b0c73e1`。
- Reviewer Agent：`019fae20-11bb-7c52-be0b-31521d244e52`。
- 状态链：`init → EXPERT_OPEN → REVIEW_OPEN → REVIEW_TERMINAL → PRODUCT_READY`。
- 双门：`SOURCE_FIDELITY_PASS`；`TEACHING_PASS`。
- 教学稿：21110 bytes，SHA-256 `ac9d1f68bdd7e789cad0beb42e6fe0b3de233803dd6340b1ddbe8b8eb43ada1d`。
- 产品审阅包：`runs/EXPERT-TEACHING-V0.1.2-MIGRATION-A-T2.35-01/acceptance/expert-product-review.md`；冻结包 SHA-256 `5d285fa9ce6bb36fbedf99e7a652293716f3ee79d34438fa07c1fe675962d285`。
- archive：[artifacts/EXPERT-TEACHING-V0.1.2-MIGRATION-A-T2.35-01.tar.gz](../artifacts/EXPERT-TEACHING-V0.1.2-MIGRATION-A-T2.35-01.tar.gz)，62051 bytes，SHA-256 `790b99b64e2beb10261902fe2c8d46edb5f219eba038a2da6e8daddcdafca1b7`。

### B：概念／诊断型 · T2.10 伯格宗教合法化

- 选择：排除 T2.35、T2.38 后，符合预注册条件的候选中 task ID 最小者 T2.10；未重新运行 Discovery，未从历史 Expert 正文反向重建框架。
- 原文：冻结第 13 章《宗教：神祇只是为国家服务》的完整连续 scope。
- 框架：Peter L. Berger《The Sacred Canopy》的宗教合法化机制；框架文件只保留既有外部框架身份和最小消歧。
- run：[runs/EXPERT-TEACHING-V0.1.2-MIGRATION-B-T2.10-01/](../runs/EXPERT-TEACHING-V0.1.2-MIGRATION-B-T2.10-01/)
- Expert Agent：`019fae1b-7e3b-7720-9627-58069239f492`。
- Reviewer Agent：`019fae21-dc09-7323-a3d7-5d0d22ee8e65`。
- 状态链：`init → EXPERT_OPEN → REVIEW_OPEN → REVIEW_TERMINAL → PRODUCT_READY`。
- 双门：`SOURCE_FIDELITY_PASS`；`TEACHING_PASS`。
- 教学稿：13331 bytes，SHA-256 `046cc80a79e1c86f41e66941d34005a1a1432aa93cd3152523a5a808d5e29`。
- 产品审阅包：`runs/EXPERT-TEACHING-V0.1.2-MIGRATION-B-T2.10-01/acceptance/expert-product-review.md`；冻结包 SHA-256 `07c22ec94571aa6ba49b0aba003f9c7b161cd5bc6a3f9d2bc2cc1d2f7e384c2f`。
- archive：[artifacts/EXPERT-TEACHING-V0.1.2-MIGRATION-B-T2.10-01.tar.gz](../artifacts/EXPERT-TEACHING-V0.1.2-MIGRATION-B-T2.10-01.tar.gz)，36622 bytes，SHA-256 `c13387203bd7ce5dd29b879a41a90f8fafde7e9f6351e1377bb83d56a7a451c1`。

## 运行事实与边界

- A Expert 于 `2026-07-29T13:30:45+00:00` 启动；A Reviewer 于 `13:45:45` 启动；A 于 `13:47:44` 达到 `PRODUCT_READY`。
- B Expert 于 `2026-07-29T13:33:21+00:00` 启动；B Reviewer 于 `13:45:45` 启动；B 于 `13:49:19` 达到 `PRODUCT_READY`。
- 两组均使用同一 v0.1.2 版本、同一任务模板、同一模型配置和同一状态机。
- 本轮没有读取历史 Expert 成品、Reader、Writer、产品判词、比较结果或验收答案；产品审阅入口保持独立待填。
- 本轮没有启动 Writer，也没有修改 `CURRENT_VERSION`、`run-current.py`、`versions/0.1.2/`、contracts、templates、scripts 或 tests。

## 技术状态与产品门

- `implemented`：两组输入、Expert 教学稿、来源表、review、产品审阅包和 archive 均已生成。
- `integrated`：两组均按唯一入口和 v0.1.2 状态机完成，但尚未接入 Writer 或其他生产线；本轮不要求接入。
- `verified`：两组 `verify` 均 PASS，且均完成 archive；双门均通过。
- `accepted`：`unknown / pending product owner review`。审核 Agent 的双门结论不替代产品负责人接受。

## 过程例外

- A Expert 与 B Expert 的最终语义产物未重跑。由于 v0.1.2 的 receipt 合同要求固定 `audit_scope` 字符串，控制层在 seal 前对两份 receipt 做了同范围、确定性的 schema 规范化：A 仅规范化 `audit_scope`；B 移除 agent 额外的 `role` 字段并规范化 `audit_scope`。没有改动教学稿、来源表、URL、Prompt 或语义内容；该事件已列入 observation report。
- 最初机械试探的错误 B T2.24 只有 `init`、没有语义调用，未进入正式候选；已移出仓库至项目外取消运行目录，作为取消对象记录，不纳入正式 run 或产品判断。
