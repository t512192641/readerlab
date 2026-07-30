# ReaderLab v0.5｜运行清单

## 身份

- run: `discovery-v0.5-assembled-experts`
- baseline: `eaf36aca572f9af6b4e5f672f73258144922d2d9`
- branch: `review/discovery-v0.5-assembled-experts`
- worktree: `/Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts`
- scope: 真实组装专家与薄卡的同任务配对实验

## 冻结输入身份

- test_source: `docs/expert-teaching-v0.1.2-migration-inputs/A/source.xhtml`
- test_source_sha256: `0f4af98ac9beb82cea8d4ad708191bf28aa7758645249e0640d6c1d9d5c4f88a`
- test_source_size: 34512 bytes

## 控制边界

- 三个专家包冻结前，不读取测试原文或旧实验内容。
- 用户候选卡冻结前，生产端不读取 GOLD-STANDARDS、旧 examples、旧候选、旧 raw seed、C1—C9、K1—K10 或旧判词。
- 组装专家只能使用本 run 中标记为 `VERIFIED` 的资产；薄卡不能含具体资产名称、作者、作品、机制、案例、激活条件或边界。
- 本轮停止于用户候选卡；不运行下游 Expert、Writer、Fidelity、Cold-read、最终陪读稿或生产 Skill 修改。

## 阶段

1. 三个独立上下文组装 E1/E2/E3，并由独立核验上下文审核。
2. 冻结 full 包与匹配 thin 卡，记录 SHA-256。
3. 六个独立阅读上下文使用共同任务完成 0—2 项激活记录。
4. 独立身份审计、匿名化、盲碰撞审计、聚类比较。
5. 只从盲审通过候选生成匿名用户卡，然后停止。

## 外部上下文调用

首轮计划调用：3 个专家构建上下文、1 个专家核验上下文、6 个阅读上下文、1 个身份审计上下文、1 个碰撞审计上下文。实际调用、模型、重试与限制以各 control task 文件为准。

## 状态

- user_acceptance: `unknown`
- CORE: `0`
- current_stop: `用户候选卡生成后立即停止`

## 实际独立上下文

- expert_builders: 3
- expert_verifier: 1
- paired_readers: 6
- identity_audit: 1
- blind_collision_audit: 1
- cluster_comparison: 1
- user_candidate_card: 1
- internal_report: 1
- independent_context_total: 15
