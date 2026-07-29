# T2.36 U01 Social Connection Depth Seam · run manifest

## 身份与范围

- 任务：`T2.36`
- run：`runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01`
- 分支：`experiment/u01-social-connection-depth-seam`
- 审计基线：`c8ef926216a99c45ae1341d1c74acde94fd92ae3`
- 启动时间：`2026-07-29T04:26:56-0400`
- 固定 C：Iris Marion Young 的 Social Connection Model
- 固定 U01：`inputs/u01-frozen.md`，`16368` bytes，SHA-256 `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c`
- 路径：`固定 C → 完整 Expert 课 → 内容锁 → 独立 Writer → 深度与保真审核`
- 状态：`CLOSEOUT_ARCHIVE_CREATED_STOPPED_AFTER_RETURN_WRITER`
- 实验性质：`diagnostic sidecar; production integration and product acceptance are not claimed`

## 预注册执行边界

- 四个阶段分别由四个新 Agent 上下文承担，均为 `fork_turns="none"`；不能合并角色。
- Phase 1 可用 Web Search + Web Fetch；Phase 2—4 禁网。
- 每位角色仅一次调用；重试：`no`；Prompt 修改：`no`。
- Prompt 冻结清单：`control/prompt-freeze.sha256`（在 Phase 1 启动前生成）。
- 阶段产物通过单独 SHA-256 文件冻结；后续阶段只读取其白名单输入。
- 当前旧稿绝不进入 Phase 1—4；仅在双门通过后用于控制层匿名产品对照。
- token、墙钟、成本：各阶段只能记录运行环境可取得的实际值；不可取得时写 `unavailable`，不估算。
- Expert 研究记录：12 条精确搜索查询、9 个打开页面（其中 1 个 Internal Error）及来源清单已进入 `run-ledger.md` 与冻结 `raw/source-map.md`；未授权的后三阶段没有联网记录。

## 四个执行上下文（待填）

| 阶段 | 角色 | Agent ID | 模型 | reasoning | 精确本地读取 | 联网 |
|---|---|---|---|---|---|---|
| 1 | Expert | `/root/u01_expert_recovery` (初始 `/root/u01_expert` 写入失败，见 ledger) | GPT-5 | unavailable | U01 + phase-1 task | Web Search + Web Fetch |
| 2 | 内容审核／锁定 | `/root/u01_content_review` | unavailable | unavailable | U01 + course + source map + phase-2 task | 禁止 |
| 3 | Writer | `/root/u01_writer` | unavailable | unavailable | U01 + course + content lock + phase-3 task | 禁止 |
| 4 | Fidelity／Depth 审核 | `/root/u01_fidelity_depth` | unavailable | unavailable | U01 + course + source map + content lock + Reader + phase-4 task | 禁止 |

## 技术恢复声明

- 初始 Expert 上下文 `/root/u01_expert` 能读取输入并执行研究，但其首次输出写入被外部 worktree 路径策略拒绝；没有生成任何 `raw/` 文件，也没有向后续角色交接内容。
- 控制层已将同一、未改字节的 run 移入可写工作区；Phase 1 Prompt SHA-256 仍为 `2726b283fb61360c3dff0faab6df06136ca227d6243b56d06805dc93dc48b44a`。
- 依项目的同范围会话失败技术恢复许可，下一次仅替代该未完成的落盘执行；不修改语义 Prompt、不复用失败上下文的未冻结内容、不将其视为结果质量补跑。该异常与恢复会完整进入 run ledger。

## 已冻结交接

| 阶段 | 文件 | SHA-256 | 冻结记录 |
|---|---|---|---|
| 1 Expert | `raw/expert-course.md` | `86540f040d9002ffd5e6bff581a5455c24fdc197e2bfaec712a3d8944df8b65b` | `control/freeze-stage-1.sha256` |
| 1 Expert | `raw/source-map.md` | `f89b357700f05eb8ab9ee12602ddc81a736d28443fa10b4cb53fc0e825d33f0a` | `control/freeze-stage-1.sha256` |
| 2 内容审核 | `locked/content-review.md` | `721e5029312fb81b97fb2f3a30e2b4fbd11dc9611880a0822f3b06f4508610ab` | `control/freeze-stage-2.sha256` |
| 2 内容锁 | `locked/content-lock.md` | `2f0c8ec0b4e06c5957010dec5a68aa8dcd957cdb7344c6acf3553430a969ed47` | `control/freeze-stage-2.sha256` |
| 3 Writer | `final/reader-v1.md` | `49fe703f2e578a477390d621d6d82f566a4d1342baa70ab761f1aac0cee1e71a` | `control/freeze-stage-3.sha256` |
| 4 Fidelity／Depth | `acceptance/fidelity-depth-review.md` | `d801a153a2f948d43ed508c4f2dc27919cc189ddf59a724abada04ccbcdeecfc` | `control/freeze-stage-4.sha256` |

## 条件性停止

- Phase 2 非 `LOCK_FOR_WRITER`：停止；不调用 Writer／最终审核／产品包。
- Phase 4 非 `FIDELITY_PASS + DEPTH_PASS`：停止；不生成产品包。
- 双门通过：控制层机械匿名组装产品包并冻结，等待产品负责人；不解读产品选择。

## 实际终局

- Phase 2：`LOCK_FOR_WRITER`
- Fidelity：`RETURN_WRITER`
- Depth：`DEPTH_PASS`
- 停止点：`STOPPED_AFTER_RETURN_WRITER`。由于 Fidelity 未通过，`acceptance/product-review.md`、`acceptance/version-key.md` 和 `control/freeze-stage-5.sha256` 均未生成；当前旧稿没有被读取。
- 完整 run 压缩包：`artifacts/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01.tar.gz`；它只含本 run 的实际输入、控制、冻结、raw、locked、final 与 Phase 4 审核文件，不含旧稿或未获准的产品包。
- closeout 核验：所有 Stage 0—4 freeze 与 Prompt freeze 的 `shasum -c` 通过；active tests 在本 run 相关登记同步后为 35/36 通过，剩余 1 项是审计基线已存在未跟踪 Markdown 的全树资产枚举失配，见 run ledger。
