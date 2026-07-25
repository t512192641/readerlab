# ReaderLab 当前能力地图

> 快照日期：2026-07-25
> 业务证据基线 commit：`bcb052e4dcaeac53a273a36608a632b98a98d94b`；后续纯审计提交不改变下述业务成熟度
> 业务工作树输入：T2.35 小型控制证据已跟踪，完整语义 payload 继续 ignored 本地保留；当前停止点与生产授权只见 `docs/current-task.md`；治理文件修改不作为业务成熟度证据
> owner：审计层当前能力成熟度投影
> 注意：本图不拥有产品责任、任务状态或产品判词正文；现场变化后必须重新核验。

## 一、成熟度语言

| 等级 | 含义 |
|---|---|
| `未开始` | 尚无本项目实现或真实运行证据 |
| `局部实验` | 在限定样本或手工条件下尝试过 |
| `单次成立` | 至少一次真实目标路径获得所需技术证据和产品接受 |
| `跨样本复现` | 冻结路线在未见材料上再次成立 |
| `资格通过` | 在目标档条件、独立验收和适用回归下证明可复用 |
| `已进入 Skill` | 已接入真实 Skill 入口并验证用户目标路径 |

该语言描述长期能力成熟度，不替代单次任务的 `implemented / integrated / verified / accepted`。

## 二、证据坐标

证据模式：

- `owner fact`：权威 owner 中的产品或长期责任；
- `derived projection`：从直接证据派生的成熟度判断；
- `prior audit observation`：先前审计记录，尚未在当前冷启动中复验；
- `current-point reverified`：本次大审计在上方固定点重新执行或复算。

| ID | 直接坐标与可复核内容 |
|---|---|
| `E01` | `owner fact`：`PRODUCT-DECISIONS.md:21-27` 图书线长期责任；`PRODUCT-DECISIONS.md:105-116` Skills 线 E1—E4 |
| `E02` | `current-point reverified`：T2.35 原审阅包 SHA-256 `4c0248572786e72cbfa0dffed63c15f745a0a47243b5bc5c30221a277f6d101f`；production freeze `0bde93d07d98e9c7d66fb29a2e2c6c463314b2aa4f723a945e5f4c65af40d385`；acceptance freeze `c981641cda9133258ce51d5a1c9808c934a309ccc792055f064d7b54f0e387eb`；`acceptance/product-verdicts.md` 已写明 `P2_PASS_WORTH_WRITING`；当前授权只见状态 owner |
| `E03` | `current-point reverified`：`taskcards/T2.34.md:288-324`，四向比较、六个语义角色、D3 产品选择 |
| `E04` | `current-point reverified`：`contracts/BOOK-CONTENT-FLOW-v2.md` 与其 freeze receipt 已成为现行技术 interface；Writer 以完整 Expert 初稿和语义锁为组织单位，可形成一个或多个 Reader 单元；旧 T1.6／M1 字节保留为历史 |
| `E05` | `current-point reverified`：`contracts/T1.8-independent-acceptance.md:8-68`、`taskcards/T2.2.md`，Judge 合同存在但资格失败 |
| `E06` | `current-point reverified`：`taskcards/T2.28.md:1-10,162-176`、`T2.30.md:1-17,208-218`、`T2.31.md:1-11,175-179`、`T2.33.md:1-9,195-208`，近期 P3 未接受 |
| `E07` | `current-point reverified`：`docs/current-task.md` 是当前执行切片 owner，`docs/dev-state.md` 是当前已验证工程事实 owner；`CURRENT-STATE.md` 仅为兼容入口 |
| `E08` | `current-point reverified`：`python3 -B tests/entry.py` 是唯一当前健康入口；旧 clean-seed validator 与失效的 T2.26 脚本／测试均无当前调用方，已从工作树删除并由本地 Git 保留恢复身份 |
| `E09` | `current-point reverified`：`tools/run.py` 只受控忽略普通 `.DS_Store` 并 warning；已知四个宿主文件均已物理删除，T2.35 check 无 warning，未知宿主文件继续硬失败 |
| `E10` | `current-point reverified`：`lenses/T1.9-seed-lenses.md`、`lenses/T2.3-seed-lenses-v2.md`、`taskcards/T2.35.md:45-53`，透镜资产未接入当前生产 |
| `E11` | `owner fact + derived projection`：`PRODUCT-DECISIONS.md:105-116` 是 Skills 线长期责任；`blueprints/PIPELINE-MAP.md:89-104` 是其派生图 |
| `E12` | `current-point reverified`：`git status --short`、`find taskcards -maxdepth 1 -name '*.md'`、`find runs -mindepth 1 -maxdepth 1 -type d`、`git ls-files runs`，工作树与目录规模 |
| `E13` | `current-point reverified`：图书内容流 v2 已通过三轮独立工程审查，现行 current pointer 由 `blueprints/PIPELINE-MAP.md` 唯一拥有；active 回归锁定 v2 receipt 与旧 T1.3—T1.7 历史哈希 |

## 三、图书解读线

| 能力 | 当前成熟度 | 当前直接证据 | 关键缺口 |
|---|---|---|---|
| 材料进入与范围冻结 | `局部实验` | `[E02][E08]` | 尚无最终 Skill 入口；active 健康信号不能证明语义与产品资格 |
| B1 完整原文 | `局部实验` | `[E02][E08]` | 未形成稳定 runtime 和目标环境资格 |
| 值得停下的问题发现 | `局部实验` | `[E03][E06][E13]` | v2 已解除中央派题冲突；runtime 未集成，未跨未见样本复现 |
| 视角／认知背景选择 | `局部实验` | `[E03][E10][E13]` | v2 已冻结正式透镜优先、真实缺口临时 Expert 与受控偶遇责任；具体匹配与治理仍未资格化 |
| 正式透镜资产 | `局部实验` | `[E10]` | 均未接入当前生产；无登记、调用、晋退和真实资格 |
| Expert 完整认知 | `局部实验` | `[E02][E06][E13]` | T2.35 Expert 检查点已获产品负责人接受；当前路线没有未见材料复现 |
| 内容价值判断 | `局部实验` | P1/P2 和比较在多轮人工运行 | 研发门与最终生产责任未分清；没有稳定资格 |
| 来源／事实／边界审核 | `局部实验` | T2.23、T2.24、T2.30、T2.35 等人工运行 | 尚无统一 runtime；与内容审核是否合并未审定 |
| Writer 编辑责任 | `局部实验` | `[E04][E06]` | 长期合同冲突已关闭；runtime 与 Reader 单元真实能力未资格化 |
| Fidelity 忠实性复核 | `局部实验` | `[E13]` 与多轮手工复核 | v2 已明确独立 gate；未证明稳定发现真实语义改写 |
| B2 锚定与装配 | `局部实验` | `[E06][E13]` | v2 已取消旧 callout 冻结并保留确定性责任；真实 `tandem-comments` interface 仍 unknown |
| B3 读薄 | `未开始` | 只有长期产品责任 | 无当前合同、实现、运行或产品样张 |
| 最终独立 Judge | `局部实验` | `[E05]` | T2.2 资格 `FAIL`，当前不得上岗 |
| 产品负责人最终接受 | `局部实验` | 多轮 P1/P2/P3 判词 | 目前是研发检查点，不等于成熟生产接口 |
| 目标档模型稳定运行 | `未开始` | 最强／不同档模型曾用于实验 | 无冻结路线、未见材料、质量、延迟和成本联合资格 |
| 图书 Skill 编排 | `未开始` | 现有 run 工具提供部分确定性骨架 | 没有真实 Skill 入口或完整后台编排 |
| 图书 Skill 回归与发布 | `未开始` | 无 | 前述能力尚未资格化 |

## 四、Skills 包解读线

| 能力 | 当前成熟度 | 当前直接证据 | 关键缺口 |
|---|---|---|---|
| Skill 包进入、识别与导航 | `未开始` | `[E11]` | 无获授权真实运行 |
| E1 完整中文净化正文 | `未开始` | `[E11]` | 无当前语义样张、产品样张或 runtime |
| E2 非技术陪读 | `未开始` | 只有产品责任 | 无当前样张和合法归零验证 |
| E3 技术讲解 | `未开始` | 只有产品责任 | 无当前样张和可复用机制证据 |
| E4 无背景 Agent 资产卡 | `未开始` | 只有产品责任 | 无独立 Agent 消费验证 |
| E1—E4 分别验收 | `未开始` | 只有长期责任 | 无运行合同、Judge 或产品接受证据 |
| Skills 解读 Skill 编排 | `未开始` | 无 | 共享薄骨架与本线语义流程均未接入 |
| Skills 解读 Skill 回归与发布 | `未开始` | 无 | 尚无第一个被接受的端到端样张 |

## 五、共享工程能力

| 能力 | 当前成熟度 | 当前直接证据 | 关键缺口 |
|---|---|---|---|
| source／scope／hash／freeze | `局部实验` | `[E08][E09]` | 宿主元数据假红灯已关闭；旧 run profile 和语义资格仍有限 |
| 排他 promotion | `局部实验` | 工具与专项测试存在 | active 与历史信号已隔离；真实 Skill 入口尚未接入 |
| 当前状态交接 | `局部实验` | `[E07][E12]` | 单一 owner 与当前任务判词已有自动一致性检查；当前值只见该 owner |
| 活跃测试与历史回放 | `局部实验` | `[E08]` | active 子集与历史回放已分离；active 覆盖仍窄，不是完整资格门 |
| 成本与墙钟观测 | `局部实验` | 后期任务记录部分墙钟与等待 | 口径不完全统一，未接入 Skill 运行 |
| 故障预防与复发审计 | `局部实验` | `audit/INCIDENT-GUARDRAILS.md`；`.DS_Store`、测试 inventory 与当前状态同步已自动化，Chrome／临时脚本有模板防线 | 新 closeout 防线尚待下一次真实业务状态变化证明可持续 |
| 审计控制面 | `局部实验` | 宪章、运行机制、能力地图、问题台账和首次大审计 | 本轮生命周期清理仍需复审；尚未经过多周期稳定运行 |

## 六、当前总体判断

- 图书线已经积累大量研究证据，但没有任何一项完整端到端能力达到 `资格通过`。
- T2.35 只到 Expert 与来源／P2，不是完整图书流程。
- Writer、Fidelity 和装配曾运行，不等于当前组合已经稳定。
- 最终 Judge 有合同和失败考试，没有生产资格。
- B3 与 Skills 包解读线均基本未开始。
- 当前停止点、治理状态与生产授权只见 `docs/current-task.md`，本图不复制。
