# ReaderLab v0.4 final-report 候选（修正版）

> **报告性质：内部证据总结，不是产品 acceptance。**
>
> 本报告只汇总本轮正式目录中已提供的 C5、K10、C1 合同链证据及明确允许的历史基线。它不修改既有产物，不把空白用户表单解释为接受，不产生 promotion、生产集成或发布结论。

## 本轮创建或修改过的全部 run 和文件清单

### 项目内正式文件

本轮正式目录共 21 个文件。正式根 manifest 是 `00-run-manifest.md`；`control/` 只含以下 6 个 stage task Markdown，不把过时的 `control/run-manifest.md` 列为正式文件。

- `v3/experiments/discovery-v0.4-contract-writer/00-run-manifest.md`：实际执行态 manifest；状态为 `executed-to-user-review-stop`，停止于 C5 用户审阅入口。
- `v3/experiments/discovery-v0.4-contract-writer/01-candidate-contracts/C1.md`：C1 为 `HOLD/L1`，不进入 Expert 或 Writer。
- `v3/experiments/discovery-v0.4-contract-writer/01-candidate-contracts/C5.md`：C5 为 `CORE（暂定）/L2`，允许完整链，禁止 L3。
- `v3/experiments/discovery-v0.4-contract-writer/01-candidate-contracts/K10.md`：K10 为 `DEEPENING/L2`，停止在 observation structure。
- `v3/experiments/discovery-v0.4-contract-writer/02-routing-audit.md`：三条候选路由独立闭合。
- `v3/experiments/discovery-v0.4-contract-writer/C5/03-expert-asset-audit.md`：`ASSET_SUFFICIENT`，允许 Writer handoff。
- `v3/experiments/discovery-v0.4-contract-writer/C5/04-structured-knowledge-asset.md`：结构化知识资产已冻结供 Writer 使用。
- `v3/experiments/discovery-v0.4-contract-writer/C5/05-writer-packet.md`：Writer 输入与保真边界已形成。
- `v3/experiments/discovery-v0.4-contract-writer/C5/06-writer-draft-v1.md`：Writer v1 已实际生成，随后被 Fidelity 返回。
- `v3/experiments/discovery-v0.4-contract-writer/C5/06-writer-draft-v2.md`：唯一一次 v2，补齐边界与来源归属。
- `v3/experiments/discovery-v0.4-contract-writer/C5/07-semantic-fidelity-review-v1.md`：终局为 `RETURN_WRITER`。
- `v3/experiments/discovery-v0.4-contract-writer/C5/07-semantic-fidelity-review-v2.md`：终局为 `FIDELITY_PASS`。
- `v3/experiments/discovery-v0.4-contract-writer/C5/08-cold-read-review-v1.md`：终局为 `COLD_READ_PASS`，8 题全 PASS。
- `v3/experiments/discovery-v0.4-contract-writer/09-USER-REVIEW-C5.md`：C5 v2 陪读稿与产品负责人审阅表已形成，表单仍为空。
- `v3/experiments/discovery-v0.4-contract-writer/10-final-report.md`：原内部证据总结候选，保留为正式目录文件。
- `v3/experiments/discovery-v0.4-contract-writer/control/contract-task.md`：合同 stage task 定义；自身保留 `control-only / not-executed` 控制元数据。
- `v3/experiments/discovery-v0.4-contract-writer/control/routing-task.md`：路由 stage task 定义；自身保留 `control-only / not-executed` 控制元数据。
- `v3/experiments/discovery-v0.4-contract-writer/control/expert-audit-task.md`：Expert asset audit stage task 定义；自身保留 `control-only / not-executed` 控制元数据。
- `v3/experiments/discovery-v0.4-contract-writer/control/writer-task.md`：Writer stage task 定义；自身保留 `control-only / not-executed` 控制元数据。
- `v3/experiments/discovery-v0.4-contract-writer/control/fidelity-review-task.md`：Fidelity review stage task 定义；自身保留 `control-only / not-executed` 控制元数据。
- `v3/experiments/discovery-v0.4-contract-writer/control/cold-read-task.md`：cold-read stage task 定义；自身保留 `control-only / not-executed` 控制元数据。

### 项目外工作文件

- `/private/tmp/readerlab-v0.4-contract-writer-candidate/` + 2 个报告文件：`10-final-report.md` 作为只读来源，`10-final-report-corrected.md` 为本次覆盖写入的修正版；未修改其他工作文件。

## 1. C5 从合同到最终陪读稿是否完成

按现有正式证据文件，C5 **已完成到最终陪读稿及其技术门**；尚未完成产品 acceptance。文件链如下：

| 阶段 | 文件 | 结论 |
|---|---|---|
| 合同 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/01-candidate-contracts/C5.md` | `CORE（暂定）`，最高 L2，允许完整链，禁止 L3 |
| 路由 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/02-routing-audit.md` | C5 路由闭合：Expert → structured asset → Writer → fidelity → cold-read |
| Expert 资产审计 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/C5/03-expert-asset-audit.md` | `ASSET_SUFFICIENT`，允许 Writer handoff |
| 结构化知识资产 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/C5/04-structured-knowledge-asset.md` | 框架、机制、边界、迁移、来源层级和 Writer-preserve 已冻结 |
| Writer packet | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/C5/05-writer-packet.md` | 四类输入与读者稿合同齐全 |
| Writer v1 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/C5/06-writer-draft-v1.md` | 已生成；随后被 Fidelity 返回 Writer |
| Fidelity v1 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/C5/07-semantic-fidelity-review-v1.md` | `RETURN_WRITER` |
| Writer v2 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/C5/06-writer-draft-v2.md` | 唯一一次允许的 v2，补齐边界归属与独立案例边界 |
| Fidelity v2 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/C5/07-semantic-fidelity-review-v2.md` | `FIDELITY_PASS` |
| Cold-read | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/C5/08-cold-read-review-v1.md` | `COLD_READ_PASS`，8 题全 PASS |
| 最终陪读稿／用户审阅入口 | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/09-USER-REVIEW-C5.md` | v2 陪读稿已提供；产品表单仍为空，未形成 acceptance |

这里的“完成”指文件链和技术门已达到 cold-read；根 manifest 明确记录本轮实际执行到 `executed-to-user-review-stop`，当前停止点是 C5 用户审阅文件。这不表示产品 acceptance，也不表示已经进入生产。

## 2. K10 为什么停在 DEEPENING，准确停止点是什么

K10 已有作者明确的“内部团结／外部区分”双向结果，但缺少共同在场、参与频率、共享情感变化、成员排除规则、越界制裁、仪式后的合作／冲突变化，以及少数群体和异议者的不同经验。因此外部框架只能补充中间结构和取证顺序，不能承担独立 CORE 或 L3 个案主张。

准确停止点是：只冻结“**神圣标记／边界 → 共同参与与情感 → 成员资格 → 越界制裁 → 内部团结／外部排斥**”的观察结构和证据清单；不启动 Expert，不进入 Writer，不生成下游读者稿，不把仪式存在写成已验证的团结、排斥、歧视或制裁因果。

## 3. C1 为什么停在 HOLD，准确停止点是什么

C1 的原文只有神圣化、神选国家、忠诚和牺牲的入口，没有真实交换或补偿提议，也没有提议后的接受、拒绝、愤怒、妥协、退出或参与行为变化。因此最高只能是 L1 的待验证问题，不能把“神圣”直接写成不可交易或补偿反噬。

准确停止点是：只保留“**真实交换／补偿事件 → 可识别反应 → 行为或参与变化 → 排除强制、同侪压力、宣传、组织惩罚和策略性表态**”的证据缺口清单；立即停止，不启动 Expert、Writer、fidelity 或产品验收。

## 4. C5 Expert asset 状态及依据

C5 Expert asset 状态为 **`ASSET_SUFFICIENT`**。

依据是：

- 框架、native problem、机制、使用步骤、认知转向、L1/L2 边界、独立低背景案例、迁移和来源归属均有覆盖；
- 来源映射闭合，且区分固定原文、外部研究、ReaderLab 教学整理和当前应用推论；
- 已保留跨境外溢、非排他性／非竞争性、贡献聚合、成本集中／收益分散、搭便车、分摊、监督、履约、承诺／行动／结果，以及身份／利益／制度执行的竞争解释；
- 三镇水库案例与六问迁移能把框架变成可执行观察，而没有被移植成第 8 章个案事实；
- Expert 审计明确没有需要定向补充的字段，`writer_handoff: ALLOW`；这只证明资产足以约束 Writer，不证明 Writer 已通过，更不证明产品已接受。

## 5. Writer 是否发生语义漂移或个案化：v1/v2 与 Fidelity 结论

结论是：**没有发生实质语义漂移，也没有把 C5 个案化；但 v1 有一个真实的边界归属遗漏，必须返回 Writer。**

| 版本 | Fidelity 证据 | 判断 |
|---|---|---|
| v1 | `cognitive_turn`、`value_distribution_execution`、`conditional_judgment`、`case_diagnosis` 均 PASS；`author_conclusion_repackaged: NO`、`fabricated_fact_mechanism: NO`；但 `lost_boundary: YES`，终局 `RETURN_WRITER` | 核心结构没有漂移，也没有补造具体国家事实；缺少“价值／分配／执行”是 ReaderLab 教学整理、完整四层来源归属，以及三镇水库独立教学案例及不可移植边界的显式保留 |
| v2 | 以上正向检查全部 PASS；`lost_boundary: NO`、`return_target: NONE`、终局 `FIDELITY_PASS` | 明确补回四层来源边界和三镇水库的独立教学定位；仍使用条件句，保留未知证据和身份／利益／制度执行竞争解释，未升为 L3 |

因此，v1 的问题是 fidelity 层的边界不完整，不应被简化成“全链一次通过”；v2 才是可交 cold-read 的版本。

## 6. Cold-read 是否通过：8 题和三项缺口状态

Cold-read 结论为 **`COLD_READ_PASS`**。8 题结果全部为 `PASS`：

| 题号 | 结果 |
|---:|---|
| 1 | PASS |
| 2 | PASS |
| 3 | PASS |
| 4 | PASS |
| 5 | PASS |
| 6 | PASS |
| 7 | PASS |
| 8 | PASS |

三项缺口状态也全部为无缺口：

- `background_required: NO`；
- `internal_terms_required: NO`；
- `causal_chain_gap: NO`。

审查记录的 barrier 是“无明显读者障碍”；普通成年读者可沿条件、机制、边界和迁移顺序理解并使用。

## 7. 本轮唯一 patch，以及是否超过一次 v2

唯一 patch 是 **Writer v1 → Writer v2 的边界／归属 patch**：补明四层来源身份，明确 `value / distribution / execution` 是 ReaderLab 教学整理，并加入三镇水库“独立教学例子、不得移植为 current case 事实”的边界。

没有修改合同、路由、Expert asset 或结构化资产，没有新增来源或种子，也没有生成 v3。实际只发生了一次 v2；**没有超过一次 v2**，符合“最多一次 v2、v2 仍失败即停止”的预算。

## 8. 失败／返工发生在哪一层

失败和返工发生在 **Writer → Fidelity review 层**：`07-semantic-fidelity-review-v1.md` 明确给出 `RETURN_WRITER`，原因是 Writer 层边界归属不完整。

这不是 Expert 层失败：Expert asset 已为 `ASSET_SUFFICIENT`；也不是 cold-read 层失败：v2 通过 Fidelity 后 cold-read 8 题全 PASS。该 `RETURN_WRITER` 不能被最终的 `FIDELITY_PASS` 叙述掩盖，它是本轮真实的失败／返工记录。

## 9. 后续建议的最小 interface prototypes（只列合同接口，不启动新工作）

以下只冻结必要接口，不据此启动新运行：

1. **Contract → Route**：`candidate_id / current_class / allowed_stages / forbidden_stages / independence_check / route_check / stop_reason / next_action`；K10、C1 必须各自落在自己的终端停止点。
2. **Expert asset audit → Writer handoff**：`field_coverage / source_map_closure / expert_review_presence / product_review_presence / asset_status / missing_or_blocking_fields / writer_handoff`；只有 `ASSET_SUFFICIENT + ALLOW` 才能交 Writer。
3. **Structured asset + Writer packet → Writer draft**：`reader_text / framework / difference / new_judgment / claim_limit / transfer / preservation_check / source_trace / stop`；读者正文 600–1000 字，不能添事实或升主张。
4. **Writer draft → Fidelity**：固定检查 `cognitive_turn / value_distribution_execution / conditional_judgment / case_diagnosis / author_conclusion_repackaged / fabricated_fact_mechanism / lost_usage / lost_boundary`，终局只能是 `FIDELITY_PASS / RETURN_WRITER / RETURN_EXPERT`。
5. **Fidelity pass → Cold-read**：8 个固定问题加 `background_required / internal_terms_required / causal_chain_gap`，终局只能是 `COLD_READ_PASS / RETURN_WRITER`。
6. **Cold-read → User review**：只交最终陪读稿和产品负责人审阅表；空白项保持空白，不能由任何技术门推断 acceptance。

## 10. 唯一需要产品负责人读取的文件及当前 acceptance

唯一需要产品负责人读取的文件是：

`/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/09-USER-REVIEW-C5.md`

该文件包含 v2 最终陪读稿和 8 项产品审阅表。表中每项结果仍为空，允许值只是 `ACCEPT / PARTIAL / REJECT`；当前没有任何已填写的产品判词。因此产品 acceptance 状态必须写为 **`unknown / pending`**，不能写成已接受，也不能把 `FIDELITY_PASS` 或 `COLD_READ_PASS` 当作产品 acceptance。

## 跨项核对（不新增报告事项）

### 实验范围与禁止事项

- 无新种子、无新候选、无搜索、无联网研究、无历史材料回收式补写；本报告只使用指定正式目录和明确允许的历史基线。
- 未读取 `GOLD-STANDARDS`、`examples` 或本轮指定之外的候选语义材料。
- 未修改生产流程、技能、runtime、正式合同、数据库、公共 API 或共享数据。
- C5 合同链已实际执行到用户审阅停止点；K10 停在 observation structure，C1 停在 evidence-gap list；二者均没有 Expert、Writer 或任何下游运行。
- 本报告只写入指定的 `/private/tmp/readerlab-v0.4-contract-writer-candidate/10-final-report-corrected.md`，不修改既有正式产物。

### 技术四层状态

| 层 | 当前状态 |
|---|---|
| `implemented` | C5 合同链证据与本内部报告候选文件均存在；K10/C1 的终端控制结果也已记录 |
| `integrated` | C5 已在证据层串到用户审阅入口；没有生产 runtime 或正式路径集成 |
| `verified` | 路由闭合、C5 `ASSET_SUFFICIENT`、Fidelity v2 `FIDELITY_PASS`、cold-read `COLD_READ_PASS`、8 题全 PASS、v2 未超预算 |
| `accepted` | **`unknown / pending`**；等待产品负责人读取唯一用户审阅文件并明确填写判词 |

最高技术状态是 `verified`，不是 `accepted`。

### 成功判据逐项核对

1. 控制集合：正式 `control/` 仅有 6 个 stage task Markdown；不把不存在或过时的 `control/run-manifest.md` 作为正式文件。实际执行态由根 `00-run-manifest.md` 记录，状态为 `executed-to-user-review-stop`。
2. 三路由独立：C5 为 CORE 完整链，K10 为 DEEPENING 观察结构终止，C1 为 HOLD 证据缺口终止；通过。
3. C5 资产门：`ASSET_SUFFICIENT`；通过。
4. Writer 保真门：v1 的 `RETURN_WRITER` 被保留，v2 通过 `FIDELITY_PASS`；通过。
5. Cold-read 门：8 题全 PASS，三项缺口均为 NO；通过。
6. Revision budget：只发生一次 v2，无 v3；通过。
7. 产品门：用户审阅文件已形成，但表单为空；技术门通过不等于产品门通过，当前只能记为 pending。

根 manifest 同时记录本轮明确授权的外部边界：只可在独立 branch/worktree 内 commit/push，不得 merge、PR、切换或写入 `main`、生产流程或生产数据；该边界不等于本报告宣称已经 push，也不改变当前用户审阅停止点。

### C5 主张上限、三镇案例与来源层级边界

C5 的最高主张级别是 **L2**，明确禁止 L3。允许的是跨境外溢、公共品属性、成本集中／收益分散、搭便车、价值／分配／执行、分摊／监督／履约和承诺／行动／结果的条件化分析；不允许把第 8 章具体国家的成本、收益、时序、补偿反应、搭便车或履约结果写成已证事实。

三镇水库是独立、低背景的 ReaderLab 教学例子，只用于演示分摊、搭便车、监测和履约；不是第 8 章事实，不是外部来源案例，不能移植为 current case 证据。

来源层级必须保持为：固定原文 `C5-TEXT`；外部研究 `C5-S1` 至 `C5-S3`；ReaderLab 教学整理 `C5-RL`；当前应用推论 `C5-APP`。四层不可互相冒充；其中 `value / distribution / execution`、三镇水库和迁移六问属于 ReaderLab 教学整理／工具，不是外部作者正式命名或原文事实。

### Remaining risk

- 产品负责人尚未填写 `09-USER-REVIEW-C5.md`，因此 C5 仍是技术上 verified、产品上 pending。
- 根 `00-run-manifest.md` 是本轮实际执行态记录；`control/` 下六份文件只是 stage task 定义，各自的 `control-only / not-executed` 元数据不应被解释为 C5 合同链未执行，也不应替代根 manifest。
- 当前材料仍不足以支持任何 L3 个案结论；若未来需要改变合同、来源、主张级别、停止点或运行范围，必须另行授权，不得从本报告自动启动新工作。
