# ReaderLab V3 文档生命周期索引

状态：稳定索引，不记录动态进度。当前进度只看 `v3/current-task.md`。

## 分类规则

- `current-authority`：仍会约束未来执行；只按 current-task 路由读取，不代表全部默认必读。
- `routed-evidence`：历史、金标、失败产物或验收原始证据；只由回归、追溯或审查角色定点读取，不能定义当前状态。
- `retired-preserved`：已消费、已被取代或不再采用；保留出处，但禁止用于启动、生产、裁判或完成声明。
- 新文件若未进入本索引或 current-task 的明确路由，默认不进入活动权威层。

## Current authority｜之后继续使用

| 范围 | 用途 | 读取条件 |
| --- | --- | --- |
| `AGENTS.md`、`v3/current-task.md` | 默认入口与唯一活动切片 | 每次启动 |
| `v3/README.md`、`v3/document-map.md` | 稳定产品概览与文档身份 | 定位时 |
| `v3/standards/constraint-architecture.md` | 五条总原则、两线规则、预算与分发 | 主控 / 架构审查 |
| `v3/skill/SKILL.md`、`v3/skill/protocols/` | 会话入口与两线编排、独立门 | 主控按线路读取 |
| `v3/skill/roles/` | 裁剪后的执行合同 | Agent 只读自己的合同 |
| `v3/skill/templates/`、`v3/skill/examples/` | 读者页、manifest、冻结正反例 | 被角色合同明确要求时 |
| `book-annotation-rubric.md`、`skill-craft-rubric.md`、`asset-card-cold-start-standard.md` | 绝对质量与冷启动标准 | 对应裁判 / 测试 |
| `regression-suite.md`、`regression-cases/` | 冻结回归索引和逐 case 卡 | 回归角色逐卡读取 |
| `phase4-pilot-definition.md` | 真实 Phase 4 运行闸门 | 仅设计或执行试点时 |
| `v3/asset-layer/` | Phase 5 前的 schema、种子和查重协议 | 仅资产层设计；写回仍需用户确认 |

## Routed evidence｜之后仍会用于回归或追溯

| 范围 | 身份 | 禁止扩大 |
| --- | --- | --- |
| `v3/standards/calibration-log.md`、`blind-eval-r*.md`、`calibration-r*-*.md` | Phase 1 校准与用户判断史 | 不作为当前进度副本 |
| `v3/audit/` | 候选、来源、淘汰和失败链证据 | 不进入读者页，不自证通过 |
| `v3/pilots/022-abundance-phase4-r*` | 022 R1/R2 失败成品 | 只作负例，不作新 Demo 基线 |
| `v3/pilots/gstack-*`、`skill-r3-code-dense-candidate.md` | Skill 历史样本和局部冷启动证据 | 不升级为完整 Skill 线通过 |
| `phase2-phase3-audit-packet.md`、`inheritance.md`、`skill-r2-mini-page.md` | 旧骨架、继承来源和历史迷你页 | 只作设计来源或 case 定位 |
| regression suite、calibration 或 final review 明确引用的最终 raw | 本轮当前验收证据 | 不覆盖旧失败；均非真实运行 |

## Retired preserved｜之后不再用于执行

| 文件或范围 | 状态 | 替代入口 |
| --- | --- | --- |
| `v3/next-session-prompt.md` | `consumed` | `AGENTS.md + v3/current-task.md` |
| `v3/standards/phase4-constraint-redesign-contract.md` | `consumed-design-contract` | constraint architecture、两线协议、角色合同 |
| `v3/standards/gpt-5-5-pro-review-prompt.md` | `superseded-review-prompt` | current-task 路由的独立 Standards / Spec 验收 |
| `v3/pilots/prototype-022-extension-layout-demo/` | `superseded-layout-demo` | 不设当前替代成品；等待获准 fresh Demo |
| `v3/pilots/phase3-dry-run.md` | `historical-not-a-template` | 当前图书模板与 book protocol |
| 未被当前汇总引用的较早 `*-raw.md`、`*-rerun-*.md` | `superseded-result-preserved` | 保留失败演进；不得与上表当前 raw 重复归类，不按文件名猜最新 |
| `v3/.DS_Store` | `repository-noise` | 无；本轮不删除 |

## 维护纪律

- 不通过移动或删除来伪造整洁；先改身份、替代关系和读取路由。
- 历史证据可以继续被使用，但只能证明它当时实际覆盖的范围。
- retired 文件不得重新进入默认入口；若要恢复，必须由用户明确决定并更新 current-task。
- 物理归档、重命名或删除属于单独变更，必须先确认 dirty worktree 与引用影响。
