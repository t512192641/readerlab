# Expert Teaching Skill v0.1.2 两样本迁移验证计划

状态：已预注册并冻结；首次语义调用前不得修改本文件、两组运行输入或 0.1.2 Skill。

日期：2026-07-29  
基线 commit：`3fe6d42fa2fb6fa9440ebb62b05066993f804619`  
实验分支：`experiment/expert-teaching-v0.1.2-migration`  
固定入口：`python3 .agents/skills/readerlab-book-expert-teaching/run-current.py`  
Skill：`readerlab-book-expert-teaching 0.1.2`

## 1. 唯一验证问题

验证同一份固定 Skill 在两种知识形态中，能否分别产出普通读者可理解的完整教学课、真实内部知识结构、独立案例、回到原文后的新增认识、可迁移观察／分析能力，以及清楚的来源归属和误用边界。

本轮不测试 Discovery、Writer、Reader、ABC、Fidelity、B2 或总编排。任何非双门通过均按 0.1.2 终局停止，不返工、不发布 0.1.3。

## 2. 样本身份与选择

### 样本 A：机制／预测型

- 历史对象：T2.35。
- 原文：T2.35 冻结完整章节，第 8 章《宗教：神祇只是为国家服务》；输入源文件为 `docs/expert-teaching-v0.1.2-migration-inputs/A/source.xhtml`。
- 原文 bytes：`34512`。
- 原文 SHA-256：`0f4af98ac9beb82cea8d4ad708191bf28aa7758645249e0640d6c1d9d5c4f88a`。
- 固定框架：神圣价值与禁忌交换（sacred values and taboo trade-offs）。
- 知识重点：不可交易性、禁忌交换、物质加码可能反噬、谈判和决策边界；这些是本轮观察对象，不写入框架文件作为答案提示。
- framework 文件 SHA-256：`591681b04f19b3c7357945f244e68bf9c7e064cba87ac1dc196cd0eca51428a9`。
- source map SHA-256：`cafbb2a549ffa5e2b08a5035189ba0e31c386ee0c64e60ca1e987285bc713c19`。
- source allowlist SHA-256：`d028594f15f7515303038946764578179da00f37a3ca26506104ccf35b182048`。
- 运行路径：`runs/EXPERT-TEACHING-V0.1.2-MIGRATION-A-T2.35-01/`。

A 的 framework 只保留框架身份和最小消歧；source map 只从 T2.35 冻结来源审核的稳定 URL、证据类型和边界恢复。新 Expert 不读取 T2.35 Expert 课、knowledge cards、review outcomes、产品判词、Writer 或后续产物，也不读取 T2.35 任务卡中的详细预期理论节点。

### 样本 B：概念／诊断型

- 历史对象：T2.10 伯格知识讲义原文融合正例；选择依据来自历史三组完整且获产品接受正例的机械候选核对。
- 机械选择：排除 T2.35 与 T2.38 后，T2.10 是同时满足冻结原文、预先存在外部框架身份、可恢复冻结来源集合、概念／诊断价值和无需重新 Discovery 的候选中 task ID 最小者。
- 原文：第 13 章《宗教：神祇只是为国家服务》；输入源文件为 `docs/expert-teaching-v0.1.2-migration-inputs/B/source.xhtml`，来自冻结 member `text/part0019.html` 的完整连续 scope。
- 原文 bytes：`13337`。
- 原文 SHA-256：`216f3a01176e10084ee7a011da7f85cd8bb6e6f1558546db6414f9a285b05dad`。
- 固定框架：彼得·伯格《神圣的帷幕》中的宗教合法化机制（Peter L. Berger, *The Sacred Canopy*）。
- framework 文件 SHA-256：`636f8e7ef2bdf297801e33aa06824a012c6656838a86cae6cc81b0a9ca73c6f2`。
- source map SHA-256：`7b44e4ffd14e75c4fb82201b54365ae3cb9a9d4afc7d4a7befeedd815bdcc109`。
- source allowlist SHA-256：`da495145b46b4e621355c4c6c6921b55bed148ad462fbb2a37db18c96cf95f8a`。
- 运行路径：`runs/EXPERT-TEACHING-V0.1.2-MIGRATION-B-T2.10-01/`。

B 的 framework 只固定既有社会学知识对象及最小消歧；source map 从冻结的 Berger 来源核验 ledger 恢复原理论骨架、来源身份和误用边界。新 Expert 不读取 T2.9／T2.10 的 Expert、Reader、Writer、产品判词或其他历史产物。

## 3. Skill 与模型冻结

- Skill version：`0.1.2`。
- Skill fingerprint aggregate SHA-256：`da7b0083e4b245df0a81aae0d4124adfd3fc69e015b17819aef08a5cb4e7b818`。
- Expert：`gpt-5.6-sol / high`。
- Independent Review：`gpt-5.6-terra / high`。
- 每个角色只运行一次；不重试、不修改生成 task、不回灌另一样本、不读取历史 Expert／Reader／Writer／产品判词。
- 网络边界：Expert／reviewer 只可打开各自 allowlist 中 `allowed` URL 及明确注册的 redirect；不得开放搜索。`reference_only` 只能引用，不能打开。
- 运行元数据统一记录：`network=allowlisted-only`、`retries=no`、`prompt_modified=no`；语义 agent 的真实 access receipt 必须自报且使用 `agent_declared`。

## 4. 预注册输入闭集

两样本已分别执行 `init`，输入已由 0.1.2 复制进 run 并冻结；复制后的 bytes／SHA 与上列一致。正式 Skill run 只使用各自 run 内的 `inputs/source.md`、`inputs/framework.md`、`inputs/source-map.md`、`inputs/source-allowlist.json` 和 Skill 生成的 closed read set。

产品负责人审阅前禁止打开以下历史对应成品：

- T2.35 Expert、knowledge cards、review outcomes、产品判词、Writer 或后续产物；
- T2.9／T2.10 Expert、Reader、Writer、产品判词或后续历史成品；
- 任何其他历史 Expert、Reader、Writer、产品判词、比较结果或验收答案；
- `GOLD-STANDARDS.md`、`examples/`、`archive/` 及本次运行之外的语义产物。

控制层只为恢复预注册输入读取了 T2.35 冻结章节／冻结来源审核证据、T2.10 的冻结章节选择信息和 Berger 冻结来源核验 ledger；这些材料不会进入新 agent read set。

## 5. 固定运行顺序与停止点

1. A：`init → Expert 人工启动 → seal-expert → Reviewer 人工启动 → seal-review → 双门通过才 build-product-pack → verify → archive`。
2. B：完全相同的顺序和模板；A 的语义产物、观察或 reviewer 结论不得进入 B。
3. 两个产品包冻结后才交给产品负责人审阅；产品负责人只判断理解框架、内部关系、独立案例、原文新增认识、迁移能力、追问点和是否值得进入 Writer。
4. 产品负责人审阅不由审核 Agent 代替；产品判词在产品审阅入口中保持待填，技术双门不等于 `accepted`。
5. 本轮完成后停止；不得启动 Writer、修改 Skill、修改 0.1.2、回灌 Prompt、创建新版本或根据结果返工。

## 6. Observation 预注册

只在两个样本冻结后对照记录，不改变任何输入、Prompt 或结果：

- Expert／reviewer 是否完整填写 source-access receipt；
- 教学稿／来源表中的 URL 是否都能在 receipt 中找到；
- 是否出现英文人名或理论名漂移；
- 是否机械套用 T2.38 七段结构；
- 不同知识形态是否自然产生方法性或迁移性内容；
- 提问欲望来自正常深入空间，还是承重部分没有讲清。

## 7. 预注册承诺

- 两个样本在首次语义调用前同时完成 `init`，本计划及输入 hash 已冻结。
- 不修改 `CURRENT_VERSION`、`run-current.py`、`versions/0.1.2/`、contracts、templates、scripts 或 tests。
- 不把历史 Expert 正文、knowledge cards、review outcomes、产品判词或 Writer／Reader 产物复制进新 run。
- 不把任一历史样本的 Prompt、观察、来源归属或语义答案回灌到另一样本。
- 任何非双门通过按 0.1.2 状态机终止，不现场修补或发布 0.1.3。

## 8. Agent ID

首次人工启动后由控制层把四个全新上下文的 Agent ID 写入 migration ledger 和对应 run 的 seal 元数据；在此之前不预填、不复用历史 ID。
