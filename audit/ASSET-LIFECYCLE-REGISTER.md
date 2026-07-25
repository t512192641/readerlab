# ReaderLab 资产生命周期与保留清单

> 快照日期：2026-07-25
> 性质：审计投影，不拥有任务状态、产品判词或长期产品决议
> 目的：让历史证据可追溯，但不再占据默认工作入口

## 1. 结论

当前 65 张任务卡和 42 个 run 不适合物理删除。它们包含产品接受、失败原因、冻结身份和
回归坐标；在唯一证据引用尚未逐文件闭合前，删除可能损坏已经取得的成果。

本轮采用逻辑归档：

- 默认入口只指向当前 owner、现行合同和当前任务；
- 历史对象保留原路径，不自动成为执行许可；
- ignored payload 暂不删除，直到证明 tracked control evidence 足以恢复其必要事实；
- `.DS_Store` 是明确物理删除候选，但删除本身不进入本轮。

## 2. 任务卡清单

### 当前业务任务

- `taskcards/T2.35.md`：当前业务任务；产品已判定 Expert 值得进入 Writer，但正文仍可微调，
  后续必须由执行现场重新冻结；本审计不修改。

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

说明：仓库没有 T2.25 任务卡；T2.25 run 存在不等于任务卡存在。以上对象保留原路径，
因为历史文档、判词和验证器使用这些坐标；不得把它们当作当前执行入口。

### 未获当前执行许可的未来草案

- `taskcards/T3.1.md`
- `taskcards/T3.2.md`
- `taskcards/T3.3.md`
- `taskcards/T3.4.md`
- `taskcards/T3.5.md`
- `taskcards/T3.6.md`
- `taskcards/T4.1.md`
- `taskcards/T4.2.md`
- `taskcards/T4.3.md`

这些文件只是旧路线下的未来草案。现行合同、角色和当前状态均优先；任何一张都不能直接启动。

### 模板

- `taskcards/TEMPLATE.md`：新任务卡的唯一模板；仍需当前明确方案和产品负责人授权。

## 3. run 清单

### 当前业务 run

- `runs/T2.35-CH08-D3-EXPERT-P2-01`：当前、current profile、未跟踪业务现场；必须保留，
  不得由审计清理、移动或重写。

### 历史 run：current profile，可由 `tools/run.py check` 复核结构

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

### 历史 run：legacy profile，没有统一 run replay

- `runs/T2.2-sufficiency-calibration-v3`
- `runs/T2.2-sufficiency-calibration-v4`
- `runs/T2.4-IDEA-PILOT-01`
- `runs/T2.5-KNOWLEDGE-LENS-PILOT-01`
- `runs/T2.6-DISCIPLINE-EXPERT-PILOT-01`
- `runs/T2.7-BOUNDED-FRAMEWORK-PILOT-01`
- `runs/T2.8-KNOWLEDGE-OBJECT-PILOT-01`
- `runs/T2.9-BERGER-STUDY-NOTES-PROTOTYPE-01`
- `runs/T2.10-BERGER-INLINE-READING-PROTOTYPE-01`
- `runs/T2.11-NON-BERGER-STUDY-NOTES-PROTOTYPE-01`
- `runs/T2.12-NON-BERGER-INLINE-READING-PROTOTYPE-01`
- `runs/T2.13-COGNITIVE-COLLISION-REPRODUCTION-01`
- `runs/T2.14-UNSEEN-CHAPTER-COGNITIVE-COLLISION-01`
- `runs/T2.15-SECOND-UNSEEN-CHAPTER-COGNITIVE-COLLISION-01`
- `runs/T2.16-STAGED-AUTONOMOUS-DISCOVERY-01`
- `runs/T2.17-STANDALONE-LESSON-SELECTION-GATE-01`
- `runs/T2.18-INDEPENDENT-COMPARATOR-01`
- `runs/T2.19-TRANSFERABILITY-COMPARATOR-01`
- `runs/T2.20-THREE-EXPERT-LESSON-EXPANSION-01`
- `runs/T2.21-WRITER-QUALIFICATION-01`
- `runs/T2.22-PARALLEL-SOURCE-AUDIT-01`
- `runs/T2.23-SOURCE-FIX-AND-INTEGRATION-01`
- `runs/T2.24-UNTOUCHED-CHAPTER-TRANSFER-01`
- `runs/T2.25-WRITER-STYLE-AB-01`
- `runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-01`
- `runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-02`
- `runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-03`
- `runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-04`
- `runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-05`
- `runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-06`
- `runs/T2.26-PROSPECTIVE-TRANSFER-AND-SHADOW-RATER-07`

legacy 只表示没有 `run.json` 现行结构，不表示损坏。T2.26 的确定性代码回放使用
`python3 -B tests/entry.py historical-t226`，且其已知失败不得污染 active 健康信号。

## 4. 保留和清理规则

| 类别 | 当前处理 | 原因 |
|---|---|---|
| 当前 T2.35 任务卡与 run | 保留原位，审计只读 | 正在微调的业务成果 |
| 产品判词、freeze、receipt、hash、失败 blocker | 必须保留 | 它们是接受、拒绝和可复验边界 |
| 已跟踪 control evidence | 必须保留 | 当前唯一可移植证据 |
| 历史任务卡与 run | 逻辑归档 | 仍可追溯，但不进入默认入口 |
| ignored payload | 暂时保留，备份责任 unknown | 尚未逐文件证明没有唯一语义证据 |
| `.DS_Store` | 可删除候选 | 非项目内容；删除不影响 freeze，工具已受控忽略 |
| T2.30 已清理的十个临时脚本 | 保持不存在 | 历史任务卡已登记用途，无需恢复 |
| `validate.py` | 历史回放原位保留 | 没有当前调用方；移动或拆分只有风险，没有当前收益 |

## 5. 文档资产清单

以下清单覆盖 run、taskcard 和 examples 之外的全部 Markdown 文档。`GOLD-STANDARDS.md`
只登记路径和读取隔离，未读取正文；`examples/` 只登记为受限内容目录，不逐文件展开。

### 当前 owner 与默认导航

- `AGENTS.md`
- `PRODUCT-DECISIONS.md`
- `ENGINEERING-LESSONS.md`
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

`CURRENT-STATE.md` 虽是当前 owner，但当前内容已落后于 T2.35 产品判词；在执行现场同步前，
它属于“应修复的当前 owner”，不是可直接派发下游的可靠许可。

### 现行合同与项目专用能力

- `contracts/BOOK-CONTENT-FLOW-v2.md`
- `contracts/BOOK-CONTENT-FLOW-v2-freeze-receipt.md`
- `.agents/skills/readerlab-functional-role-isolation/SKILL.md`

合同 v2 是现行技术 interface，但尚未 runtime integrated；项目 Skill 只在适用任务明确调用
时读取，不是当前业务入口。

### 支持性参考，不拥有当前执行状态

- `contracts/GLOSSARY.md`
- `references/BOOK-AND-SKILLS-METHODS.md`

### 历史合同、路线、专题文档与透镜资产

- `blueprints/EXECUTION-ROADMAP.md`
- `contracts/M1-freeze-receipt.md`
- `contracts/T1.1-material-intake.md`
- `contracts/T1.2-b1-source.md`
- `contracts/T1.3-discovery.md`
- `contracts/T1.4-expert-and-knowledge-card.md`
- `contracts/T1.5-independent-review.md`
- `contracts/T1.6-writer.md`
- `contracts/T1.7-b2-assembly.md`
- `contracts/T1.8-independent-acceptance.md`
- `docs/book-pipeline-current-state-and-skill-roadmap.md`
- `docs/pipeline-template-draft.md`
- `docs/writer-style-guide.md`
- `lenses/T1.9-seed-lenses.md`
- `lenses/T2.3-seed-lenses-v2.md`

这些资产保留原路径用于追溯。旧合同已被 v2 current pointer 降为历史；路线、专题说明、风格和
透镜文件均不得覆盖当前 owner 或自动取得生产许可。

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

## 6. 下一轮物理清理的前置条件

只有同时满足以下条件，才可移动或删除历史载荷：

1. 列出目标文件及所有仓库引用；
2. 证明其不是唯一产品判词、冻结身份、失败证据或恢复材料；
3. 给出本地 Git 或独立备份恢复路径；
4. 在候选区验证引用和 active tests；
5. 对 ignored 且未跟踪载荷取得产品负责人明确删除授权。

因此，本清单授权的是“看得清、默认不打扰”，不是“现在批量删除”。
