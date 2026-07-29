# ReaderLab 资产生命周期与保留清单

> 快照日期：2026-07-29
> 性质：审计投影，不拥有任务状态、产品判词或长期产品决议
> 目的：让历史证据可追溯，但不再占据默认工作入口

## 可重算数量投影

- taskcard-count: `61`
- run-container-count: `45`
- current-run-container-count: `14`
- archived-run-container-count: `31`
- run-file-count: `515`
- archived-run-file-count: `317`
- tracked-run-file-count: `248`
- ignored-run-file-count: `267`
- untracked-visible-run-file-count: `0`

以上数字由 active tests 对真实路径与 Git ignored inventory 重新计算；正文中的说明不得成为
另一份手工计数 owner。

## 1. 结论

当前任务卡、run 容器、run 文件与 Git 状态的数量只见上方可重算投影。较早 legacy run 已完成
迁移前后逐文件身份核对并物理隔离；近期／当前 run 继续位于 `runs/`。其余历史对象尚未全部
取得价值终局，因此当前仍不能声称“全仓文件已经处理”。

当前采用物理隔离与保守保留并行：

- 默认入口只指向当前 owner、现行合同和当前任务；
- 较早 legacy run 移入 `archive/runs/`，默认任务禁止读取；
- ignored payload 暂不删除，直到证明 tracked control evidence 足以恢复其必要事实；
- 已知四个 run 中的 `.DS_Store` 均已物理删除；工具仍保留忽略和 warning 防线，防止 Finder
  再次生成时污染冻结身份。

按宪章 `AUD-SCOPE-001`，下一轮必须覆盖当前仓库内全部项目文件，包括各 run 中生成的 Expert、
Writer、Reader／陪读 Markdown、审核报告、截图和 ignored payload。受限内容可以只做元数据与
生命周期登记，不因盘点获得正文读取权限。

## 2. 任务卡清单

### 当前诊断任务

- `taskcards/T2.40.md`：根据外部 Code Review 修正 Expert Teaching Skill 的版本共存、来源 allowlist、中文表达、内容泄露门、T2.38 replay 与运行元数据；不运行迁移样本或语义 Agent，0.1.0／0.1.1 结果不得混算。
- `taskcards/T2.39.md`：把 T2.38 已验证的 Expert Teaching 控制能力实现为 `readerlab-book-expert-teaching` Skill v0.1 候选；仅做确定性 scaffold、Skill-local tests 与 T2.38 机械回放，不产生新的语义结果，尚未进入生产入口。
- `taskcards/T2.38.md`：固定 U01、固定 Social Connection Model 与冻结来源范围下的 Expert teaching；双门 `SOURCE_FIDELITY_PASS + TEACHING_PASS`，产品包已生成，等待产品负责人审阅，未改变生产入口。
- `taskcards/T2.37.md`：只修复 T2.36 Writer 归属表述并复核 Fidelity／Depth；双门通过，匿名产品包已生成，等待产品审阅，未改变生产入口。
- `taskcards/T2.36.md`：固定 C 的 U01 内容链 seam；已在 `RETURN_WRITER + DEPTH_PASS`
  终局停止。它是本地 diagnostic sidecar，不是生产 runtime、产品判词或下一生产授权。

### 已完成、失败、被替代或仅作历史证据

- `taskcards/T0.1.md`
- `taskcards/T0.2.md`
- `taskcards/T0.3.md`
- `taskcards/T1.1.md`
- `taskcards/T1.2.md`
- `taskcards/T1.3.md`
- `taskcards/T1.4.md`
- `taskcards/T1.5.md`
- `taskcards/T1.6.md`
- `taskcards/T1.7.md`
- `taskcards/T1.8.md`
- `taskcards/T1.9.md`
- `taskcards/T2.1.md`
- `taskcards/T2.2-BLOCKER.md`
- `taskcards/T2.2.md`
- `taskcards/T2.3.md`
- `taskcards/T2.4.md`
- `taskcards/T2.5.md`
- `taskcards/T2.6.md`
- `taskcards/T2.7.md`
- `taskcards/T2.8.md`
- `taskcards/T2.9.md`
- `taskcards/T2.10.md`
- `taskcards/T2.11.md`
- `taskcards/T2.12.md`
- `taskcards/T2.13.md`
- `taskcards/T2.14.md`
- `taskcards/T2.15.md`
- `taskcards/T2.16.md`
- `taskcards/T2.17.md`
- `taskcards/T2.18.md`
- `taskcards/T2.19.md`
- `taskcards/T2.20.md`
- `taskcards/T2.21.md`
- `taskcards/T2.22.md`
- `taskcards/T2.23.md`
- `taskcards/T2.24.md`
- `taskcards/T2.26.md`
- `taskcards/T2.26-v02.md`
- `taskcards/T2.26-v03.md`
- `taskcards/T2.26-v04.md`
- `taskcards/T2.26-v05.md`
- `taskcards/T2.26-v06.md`
- `taskcards/T2.26-v07.md`
- `taskcards/T2.26-v07-p2-recovery.md`
- `taskcards/T2.27.md`
- `taskcards/T2.27-v02.md`
- `taskcards/T2.28.md`
- `taskcards/T2.29.md`
- `taskcards/T2.30.md`
- `taskcards/T2.31.md`
- `taskcards/T2.32.md`
- `taskcards/T2.33.md`
- `taskcards/T2.34.md`
- `taskcards/T2.35.md`

说明：仓库没有 T2.25 任务卡；T2.25 run 存在不等于任务卡存在。以上对象保留原路径，
因为历史文档、判词和验证器使用这些坐标；不得把它们当作当前执行入口。

### 已退役的未来草案

旧路线下九张 T3／T4 未来任务卡从未执行，且现行合同和蓝图已经重新定义后续路线，因此已从
当前工作树删除；需要取证时从本地 Git 提交 `e782605` 恢复。

### 模板

- `taskcards/TEMPLATE.md`：新任务卡的唯一模板；仍需当前明确方案和产品负责人授权。

## 3. run 清单

### 当前诊断 run

- `runs/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01`：Expert teaching 与独立来源／教学完整度审核均通过；产品包已按双门条件机械生成，产品负责人判词仍为 `unknown`。
- `runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01`：T2.36 Writer return；Writer v2 与
  Fidelity／Depth v2 均通过，匿名产品包已生成，等待产品审阅。
- `runs/T2.36-U01-SOCIAL-CONNECTION-DEPTH-SEAM-01`：固定 C 的四角色隔离 seam；Phase 2
  为 `LOCK_FOR_WRITER`，Phase 4 为 `RETURN_WRITER + DEPTH_PASS`，因此没有产品对照包或版本密钥。
  完整本地 payload 与归档按任务卡保留；不构成生产接入或产品接受。

### 历史 run：current profile，可由 `tools/run.py check` 复核结构

- `runs/T2.35-CH08-D3-EXPERT-P2-01`：current profile；run manifest、两个 freeze、
  P2 gate 与产品判词已跟踪，完整原文、Expert、知识卡、来源审核和审阅包继续 ignored
  本地保留，不得由审计移动或重写。

- `runs/T2.27-NARROW-CHAPTER-TO-P2-01`
- `runs/T2.27-NARROW-CHAPTER-TO-P2-02`
- `runs/T2.28-THIRD-CHAPTER-STRESS-01`
- `runs/T2.28-WRITER-COMPRESSION-02`
- `runs/T2.29-NEXT-CHAPTER-C4-TRANSFER-01`
- `runs/T2.30-C008-END-TO-END-01`
- `runs/T2.31-C008-WRITER-PATCH-01`
- `runs/T2.32-CH06-END-TO-END-01`
- `runs/T2.33-CH08-END-TO-END-01`
- `runs/T2.34-CH08-FOUR-WAY-COMPARISON-01`

这些 run 的 `run.json` 使用现行 run profile，但业务生命周期已经结束。结构可复核不代表
产品通过，也不表示其路线仍可执行。

### 历史 run：legacy profile，已物理隔离

- `archive/runs/T2.2-sufficiency-calibration-v3`
- `archive/runs/T2.2-sufficiency-calibration-v4`
- `archive/runs/T2.4-IDEA-PILOT-01`
- `archive/runs/T2.5-KNOWLEDGE-LENS-PILOT-01`
- `archive/runs/T2.6-DISCIPLINE-EXPERT-PILOT-01`
- `archive/runs/T2.7-BOUNDED-FRAMEWORK-PILOT-01`
- `archive/runs/T2.8-KNOWLEDGE-OBJECT-PILOT-01`
- `archive/runs/T2.9-BERGER-STUDY-NOTES-PROTOTYPE-01`
- `archive/runs/T2.10-BERGER-INLINE-READING-PROTOTYPE-01`
- `archive/runs/T2.11-NON-BERGER-STUDY-NOTES-PROTOTYPE-01`
- `archive/runs/T2.12-NON-BERGER-INLINE-READING-PROTOTYPE-01`
- `archive/runs/T2.13-COGNITIVE-COLLISION-REPRODUCTION-01`
- `archive/runs/T2.14-UNSEEN-CHAPTER-COGNITIVE-COLLISION-01`
- `archive/runs/T2.15-SECOND-UNSEEN-CHAPTER-COGNITIVE-COLLISION-01`
- `archive/runs/T2.16-STAGED-AUTONOMOUS-DISCOVERY-01`
- `archive/runs/T2.17-STANDALONE-LESSON-SELECTION-GATE-01`
- `archive/runs/T2.18-INDEPENDENT-COMPARATOR-01`
- `archive/runs/T2.19-TRANSFERABILITY-COMPARATOR-01`
- `archive/runs/T2.20-THREE-EXPERT-LESSON-EXPANSION-01`
- `archive/runs/T2.21-WRITER-QUALIFICATION-01`
- `archive/runs/T2.22-PARALLEL-SOURCE-AUDIT-01`
- `archive/runs/T2.23-SOURCE-FIX-AND-INTEGRATION-01`
- `archive/runs/T2.24-UNTOUCHED-CHAPTER-TRANSFER-01`
- `archive/runs/T2.25-WRITER-STYLE-AB-01`
- `archive/runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-01`
- `archive/runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-02`
- `archive/runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-03`
- `archive/runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-04`
- `archive/runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-05`
- `archive/runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-06`
- `archive/runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-07`

上方投影所列 archived run 及其文件已经完成迁移前后逐文件 SHA-256 与数量核对；原 tracked
文件继续由 Git 跟踪，本地 payload 继续保持 ignored。legacy 只表示没有 `run.json` 现行结构，
不表示损坏；默认任务不得搜索或读取历史区。

## 4. 保留和清理规则

| 类别 | 当前处理 | 原因 |
|---|---|---|
| 当前 T2.35 任务卡与 run | 保留原位，审计只读 | 当前判词与停止点只见 `docs/current-task.md` |
| 产品判词、freeze、receipt、hash、失败 blocker | 必须保留 | 它们是接受、拒绝和可复验边界 |
| 已跟踪 control evidence | 必须保留 | 当前唯一可移植证据 |
| 完整审阅包与语义 payload | 默认 ignored、本地保留 | 云端审核必须按任务单独授权；主仓库不靠通用文件名放行 |
| 较早 legacy run | 已迁移到 `archive/runs/` | 仍可追溯，但通过物理路径与读取规则退出默认入口 |
| ignored payload | 暂时保留，备份责任 unknown | 尚未逐文件证明没有唯一语义证据 |
| `.DS_Store` | 已知四个文件均已删除 | 非项目内容；工具继续受控忽略，未知宿主文件仍 hard fail |
| T2.30 已清理的十个临时脚本 | 保持不存在 | 历史任务卡已登记用途，无需恢复 |
| 旧 clean-seed validator | 已从当前工作树删除 | 无当前调用方；9,485 行旧实现和兼容 adapter 不再保留。需要取证时从本地 Git `c13ea5a:validate.py` 恢复 |

## 5. 文档资产清单

以下清单覆盖 run、taskcard 和 examples 之外的全部 Markdown 文档。`GOLD-STANDARDS.md`
只登记路径和读取隔离，未读取正文；`examples/` 只登记为受限内容目录，不逐文件展开。

### 当前 owner 与默认导航

- `AGENTS.md`
- `PRODUCT-DECISIONS.md`
- `ENGINEERING-LESSONS.md`
- `docs/current-task.md`
- `docs/dev-state.md`
- `docs/decisions.md`
- `docs/agent-run-ledger.md`
- `docs/research-log.md`
- `CURRENT-STATE.md`
- `README.md`
- `blueprints/PIPELINE-MAP.md`
- `audit/ENGINEERING-AUDITOR-CHARTER.md`
- `audit/AUDIT-OPERATING-MODEL.md`
- `audit/CAPABILITY-MAP.md`
- `audit/FINDINGS-REGISTER.md`
- `audit/ASSET-LIFECYCLE-REGISTER.md`
- `audit/INCIDENT-GUARDRAILS.md`
- `audit/VALIDATOR-DECOMPOSITION.md`
- `docs/stage-implementation-status.md`
- `docs/expert-teaching-skill-v0.1-review-map.md`
- `docs/expert-teaching-skill-v0.1-review-brief.md`
- `docs/expert-teaching-skill-v0.1-change-receipt.md`

`docs/current-task.md` 是唯一当前行动门 owner，`docs/dev-state.md` 是唯一当前已验证工程事实
owner；`CURRENT-STATE.md` 只保留兼容入口。本清单不复制当前判词、停止点或生产授权。

### 现行节点合同与项目专用能力

- `contracts/T1.1-material-intake.md`
- `contracts/T1.2-b1-source.md`
- `contracts/BOOK-CONTENT-FLOW-v2.md`
- `contracts/BOOK-CONTENT-FLOW-v2-freeze-receipt.md`
- `contracts/T1.8-independent-acceptance.md`
- `.agents/skills/readerlab-functional-role-isolation/SKILL.md`
- `.agents/skills/readerlab-book-expert-teaching/SKILL.md`
- `.agents/skills/readerlab-book-expert-teaching/contracts/input-contract.md`
- `.agents/skills/readerlab-book-expert-teaching/contracts/expert-teaching-contract.md`
- `.agents/skills/readerlab-book-expert-teaching/contracts/review-contract.md`
- `.agents/skills/readerlab-book-expert-teaching/contracts/output-contract.md`
- `.agents/skills/readerlab-book-expert-teaching/contracts/state-machine.md`
- `.agents/skills/readerlab-book-expert-teaching/templates/expert-task.md`
- `.agents/skills/readerlab-book-expert-teaching/templates/expert-review-task.md`
- `.agents/skills/readerlab-book-expert-teaching/templates/product-review.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.0/README.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/SKILL.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/contracts/input-contract.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/contracts/expert-teaching-contract.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/contracts/review-contract.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/contracts/output-contract.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/contracts/state-machine.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/templates/expert-task.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/templates/expert-review-task.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/templates/product-review.md`

T1.1 与 T1.2 分别拥有材料准入和 B1 上游节点；v2 是 B1 后至 B2 的现行内容流；T1.8
继续拥有下游独立验收语义，但不证明 Judge 已取得资格。这些合同均尚未组成已验证的完整
runtime；项目 Skill 只在适用任务明确调用时读取，不是当前业务入口。

### 支持性参考，不拥有当前执行状态

- `references/BOOK-AND-SKILLS-METHODS.md`

### 历史合同、路线、专题文档与透镜资产

- `blueprints/EXECUTION-ROADMAP.md`
- `contracts/GLOSSARY.md`
- `contracts/M1-freeze-receipt.md`
- `contracts/T1.3-discovery.md`
- `contracts/T1.4-expert-and-knowledge-card.md`
- `contracts/T1.5-independent-review.md`
- `contracts/T1.6-writer.md`
- `contracts/T1.7-b2-assembly.md`
- `docs/writer-style-guide.md`
- `lenses/T1.9-seed-lenses.md`
- `lenses/T2.3-seed-lenses-v2.md`

旧 M1 术语表由 M1 receipt 绑定原字节，T1.3—T1.7 已被 v2 current pointer 降为历史；
T1.1、T1.2 与 T1.8 仍分别承担现行上下游节点责任。旧的专题路线和 pipeline template
已删除并由 `e782605` 保留恢复身份。风格和透镜文件仍不得覆盖当前 owner 或自动取得生产许可。

### 历史诊断、考试与审计快照

- `diagnostics/T2.1-r01-r08.md`
- `diagnostics/T2.2-blind-packet.md`
- `diagnostics/T2.2-judge-answers.md`
- `diagnostics/T2.2-judge-baseline.md`
- `diagnostics/T2.2-judge-brief.md`
- `diagnostics/T2.2-recovery-architecture-v1.md`
- `diagnostics/T2.2-recovery-architecture-v1-preflight-review.md`
- `diagnostics/T2.2-recovery-architecture-v2.md`
- `diagnostics/T2.2-recovery-architecture-v2-preflight-review.md`
- `diagnostics/T2.2-recovery-architecture-v3.md`
- `diagnostics/T2.2-recovery-architecture-v3-preflight-review.md`
- `diagnostics/T2.2-recovery-architecture-v3-preflight-review-quality-audit.md`
- `diagnostics/T2.2-scoring-key.md`
- `diagnostics/T2.3-seed-lens-diagnostic.md`
- `archive/T2.2-effective-retest-v2/judge-answers.md`
- `archive/T2.2-effective-retest-v2/judge-brief.md`
- `archive/T2.2-effective-retest-v2/packet.md`
- `archive/T2.2-effective-retest-v2/report.md`
- `audit/ENGINEERING-AUDIT-2026-07-25.md`
- `audit/PROJECT-SYSTEM-AUDIT-2026-07-25.md`

它们是失败、资格、恢复或审计证据，不是当前执行接口。保留，不物理删除。

### 受限内容 owner

- `GOLD-STANDARDS.md`
- `examples/`：受限案例目录，本轮没有读取或逐项分类正文。

它们的读取只能由当前任务卡逐文件授权；生命周期盘点不产生读取许可。

## 6. 当前完成度与下一轮前置条件

当前完成：

- taskcard、run 容器和主要文档路径的第一层发现与分类；
- 默认 README 入口降噪；
- 当前／历史测试入口分离；
- `.DS_Store` 假红灯自动防线。

尚未完成：

- 上方投影所列全部 run 文件的逐文件价值判断；
- 上方投影所列 ignored run 文件的唯一证据、备份和删除判断；
- 全仓非 Markdown、截图、临时载荷和配置的逐文件终局；
- 旧 clean-seed validator 已完成退役删除；恢复只依赖本地 Git；
- 任何大规模物理删除。

只有同时满足以下条件，才可移动或删除历史载荷：

1. 列出目标文件及所有仓库引用；
2. 证明其不是唯一产品判词、冻结身份、失败证据或恢复材料；
3. 给出本地 Git 或独立备份恢复路径；
4. 在候选区验证引用和 active tests；
5. 对 ignored 且未跟踪载荷取得产品负责人明确删除授权。

因此，本清单授权的是“看得清、默认不打扰”，不是“现在批量删除”。
