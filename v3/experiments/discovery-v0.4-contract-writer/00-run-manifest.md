# ReaderLab v0.4 合同到 Writer Pilot：实际执行态 Run Manifest

version: `v0.4-contract-writer-pilot`
date: `2026-07-30`
status: `executed-to-user-review-stop`

## Run identity

| 字段 | 当前事实 |
|---|---|
| base commit | `db517c81e5fdba740a5a3732c695cc854c24db1d` |
| branch | `review/discovery-v0.4-contract-writer` |
| worktree | `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer` |
| 当前执行停止点 | C5 用户审阅文件 |
| 技术状态 | `verified`：已到 cold-read 技术门，并形成用户审阅入口 |
| 产品 acceptance 状态 | `unknown / pending`；用户审阅文件是正式停止点 |

本 manifest 记录的是本轮已经发生的实际执行链和边界，不是预执行控制草案。它不写入仓库内的
`v3/experiments/discovery-v0.4-contract-writer/control/run-manifest.md`。

## Scope

本轮实际执行并形成证据的范围是：

- C5、K10、C1 三份候选合同；
- 三路由复核；
- C5 Expert asset audit；
- C5 structured asset；
- C5 Writer packet；
- C5 Writer v1、Writer v2；
- C5 fidelity v1、fidelity v2；
- C5 cold-read；
- C5 用户审阅文件；
- final report。

本轮边界：

- 无新种子、无新候选、无搜索、无联网研究；
- 未读取或使用 `GOLD-STANDARDS.md`、`examples/` 作为生产或验收输入；
- 未修改生产流程、Skill、runtime、API、数据库、共享数据或其他正式产品文件；
- C5 仍为 `CORE（暂定）`，最高主张级别为 L2，不得升为 L3；
- K10 只到 `observation structure`，C1 只到 `evidence gap`；二者没有任何下游 Writer 或读者稿；
- 用户审阅未被技术门、模型评分或文件完整度替代；本文件不写产品接受判词。

## Executed evidence chain

以下路径均相对于当前 v0.4 worktree：

| 阶段 | 实际证据 | 状态 |
|---|---|---|
| 合同 | `v3/experiments/discovery-v0.4-contract-writer/01-candidate-contracts/C5.md`、`K10.md`、`C1.md` | 已执行 |
| 路由 | `v3/experiments/discovery-v0.4-contract-writer/02-routing-audit.md` | 已执行，三路由闭合 |
| C5 asset audit | `C5/03-expert-asset-audit.md` | `ASSET_SUFFICIENT` |
| C5 structured asset | `C5/04-structured-knowledge-asset.md` | 已冻结供 Writer 使用 |
| C5 Writer packet | `C5/05-writer-packet.md` | 已交 Writer |
| C5 Writer | `C5/06-writer-draft-v1.md`、`C5/06-writer-draft-v2.md` | v1、v2 均已实际生成 |
| C5 fidelity | `C5/07-semantic-fidelity-review-v1.md`、`C5/07-semantic-fidelity-review-v2.md` | v1 `RETURN_WRITER`；v2 `FIDELITY_PASS` |
| C5 cold-read | `C5/08-cold-read-review-v1.md` | `COLD_READ_PASS` |
| 用户审阅 | `09-USER-REVIEW-C5.md` | 已形成，作为正式停止点 |
| final report | `10-final-report.md` | 已形成内部证据总结 |

## Routes

| 候选 | 分类 | 实际路线 | 本轮终点与禁止下游 |
|---|---|---|---|
| C5 | `CORE（暂定）` | 合同 → 路由 → asset audit → structured asset → Writer packet → Writer → fidelity → cold-read → 用户审阅 | 完整链到用户审阅；最高 L2，禁止 L3 |
| K10 | `DEEPENING` | 合同 → observation structure | 在 observation structure 停止；无 Expert、无 Writer、无任何下游 |
| C1 | `HOLD` | 合同 → evidence gap | 在 evidence gap 停止；无 Expert、无 Writer、无 fidelity、无任何下游 |

路由必须保持独立：不得把 C5 的资产、Writer 版本、fidelity 结果或用户审阅结果复制给 K10/C1，
也不得把 K10/C1 的停止原因改写成 C5 的成功或失败。

## Gates

1. 合同与路由门：C5、K10、C1 各自拥有独立分类、主张上限、允许阶段和停止条件；路由复核已完成。
2. C5 资产门：`ASSET_SUFFICIENT`，允许进入 Writer；该门不等于产品接受。
3. C5 fidelity v1：`RETURN_WRITER`，原因是边界归属与独立教学案例边界保留不完整。
4. C5 fidelity v2：`FIDELITY_PASS`；已补回来源层级、教学整理归属和独立案例不可移植边界。
5. C5 cold-read 门：`COLD_READ_PASS`；8 项检查通过，未发现需返回 Writer 的读者障碍。
6. 用户审阅门：`09-USER-REVIEW-C5.md` 是正式产品停止点。产品 acceptance 仍为
   `unknown / pending`；在用户明确审阅前，不得晋级、promotion、生产集成或发布。

## Revision budget

- C5 Writer 最多允许一次 v2；本轮实际发生一次 v2，且只有这一轮 v2。
- C5 v1 的终局是 `RETURN_WRITER`；C5 v2 的 fidelity 终局是 `FIDELITY_PASS`，随后 cold-read 为
  `COLD_READ_PASS`。
- 不生成 C5 v3，不扩大输入，不新增种子或搜索，不改变合同语义。
- K10 和 C1 没有 Writer 版本预算，因为它们没有进入 Writer；不得借用 C5 的版本或结果。

## User review gate

用户审阅文件：

`/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer/v3/experiments/discovery-v0.4-contract-writer/09-USER-REVIEW-C5.md`

该文件包含 C5 Writer v2 陪读稿和产品负责人审阅表。它是本轮正式停止点；技术门通过只能说明
内容已到用户审阅，不构成产品接受结果。用户审阅前不得把 `FIDELITY_PASS`、`COLD_READ_PASS`、
文件存在或模型评分写成产品接受、promotion 或生产资格。

## Commit and push boundary

用户已明确授权的外部边界仅为：

- 只可在 branch `review/discovery-v0.4-contract-writer` 和 worktree
  `/Users/tianqiang/GitHub/t512192641/readerlab-v0.4-contract-writer` 中提交和推送；
- 目标提交信息：`Run discovery v0.4 contract-to-writer pilot`；
- 推送目标为当前 branch 对应的 `origin` branch；不得 force push；
- 禁止 merge、PR、切换或写入 `main`、生产流程或生产数据；
- 本 manifest 本身不扩大正式文件、生产入口、公共合同或运行时的修改范围。

## Stop conditions

出现以下任一情况，立即停止并保持当前证据，不自动重跑或扩产：

- 用户审阅缺失，或试图用技术门替代产品负责人判词；
- 需要把 C5 升为 L3，或把成本、收益、时序、补偿反应、搭便车、履约结果补写成当前章节事实；
- 需要为 K10 启动 Expert/Writer，或为 C1 越过 evidence gap 启动下游；
- 需要超过一次 C5 v2、生成 v3、增加 seed、搜索、联网研究或读取 `GOLD-STANDARDS/examples`；
- 需要修改生产流程、Skill、runtime、API、数据库、正式合同或共享数据；
- 需要在指定 branch/worktree 之外提交或推送，执行 force push、merge、PR、main 或生产操作；
- 需要覆盖仓库内 `control/run-manifest.md` 或把本轮实际执行链改写成未执行状态。
