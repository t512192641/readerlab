# Dev State

## Authority Boundary

本文件不是当前任务权威，不作为启动必读。当前执行状态、下一步和阶段门槛以 `docs/current-task.md` 为准。

本文件只保留稳定路径、工具状态、验证命令和已知技术边界。

## Stable Paths

- 仓库：`/Users/tianqiang/Documents/读书伴侣`
- 生成脚本：`scripts/readerlab.py`
- 单元测试：`tests/test_readerlab.py`
- 当前 EPUB：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- 当前章节循环包：`docs/reports/readerlab-elon-chapter-loop-v0/`
- 当前方法核探针包：`docs/reports/readerlab-method-kernel-v0/`
- 高阶讲解方法：`docs/high-order-explanation-method.md`
- 高阶讲解 contract 文档：`docs/contracts/high-order-explanation-v1.md`
- Body Track Gate contract：`docs/contracts/body-track-gate-v1.md`
- Material Profile contract：`docs/contracts/material-profile-v1.md`
- Claim Ledger contract：`docs/contracts/claim-ledger-v1.md`
- Candidate Tournament contract：`docs/contracts/candidate-tournament-v1.md`
- Skillization Gate contract：`docs/contracts/skillization-gate-v1.md`
- Annotation Trigger contract：`docs/contracts/annotation-trigger-v1.md`
- Location Anchor contract：`docs/contracts/location-anchor-v1.md`
- Trace Validation contract：`docs/contracts/trace-validation-v1.md`
- Comment Replay contract：`docs/contracts/comment-replay-v1.md`
- Skill delivery spec：`docs/readerlab-skill-delivery-spec.md`
- Skill IR v1：`docs/readerlab-skill-ir-v1.md`
- two-demo internal run：`docs/reports/readerlab-two-demo-run-v0/`
- private material validation：`docs/reports/readerlab-private-material-validation-v0/`
- 验收 gate：`docs/eval-gates.md`
- 运行账本：`docs/agent-run-ledger.md`

## Tool State

- `scripts/readerlab.py` 主要支持 Skill 包导入、阅读包 validate、contract validate、proof renderer、eval runner、批注读取和回复。
- 图书/长文正式导入生成器尚未完成；当前《埃隆之书》章节循环和方法核探针仍主要依赖 repo 内报告和手工/agent 循环。
- renderer / eval runner 是 proof 级工具，不能代表完整生成器能力或人工阅读验收。
- Markdown 是展示层；source registry、location map、contracts、eval 和人工状态才是事实层。
- 15 个章节的现有通过状态只代表 `chapter_high_order_explanation_pass`，不代表 `reader_package_pass`。
- `readerlab-method-kernel-v0` 只代表两章方法核探针通过，不代表可迁移方法核、正式 Skill 或外部材料验证。
- `readerlab-private-material-validation-v0` 只代表 private/local validation 通过，不代表 public external validation。
- Skill delivery design docs 已创建，但正式 `SKILL.md` 未启动。
- Trace validator 尚未实现；comment replay 尚未验证。

## Baseline Locations

这些 baseline 只在 `docs/current-task.md` 允许进入 final boss 后启用：

| Baseline | 已有对照输出 | 本地/研究来源 |
|---|---|---|
| 仓颉 / cangjie-only | `docs/reports/readerlab-elon-method-bakeoff-v0/cangjie-only.md` | `/Users/tianqiang/技能项目/skills-canonical/packages/cangjie-skill` |
| 李继刚式深读 / ljg-deepread-only | `docs/reports/readerlab-elon-method-bakeoff-v0/ljg-deepread-only.md` | 本地未确认可直接调用 Skill；研究线索见 `docs/research-log.md` |
| book-to-skill | `docs/reports/readerlab-elon-method-bakeoff-v0/book-to-skill-only.md` | 本地未确认可直接调用 Skill；研究线索见 `docs/research-log.md` |
| 乔木共读 / qiaomu-coread-only | `docs/reports/readerlab-elon-method-bakeoff-v0/qiaomu-coread-only.md` | `/Users/tianqiang/技能项目/skills-canonical/packages/qiaomu-anything-to-notebooklm`；`/Users/tianqiang/技能项目/skills-canonical/packages/qiaomu-mondo` |

## Verification Commands

```bash
python3 tests/test_readerlab.py
git diff --check
```

Skill 交付设计后下一步还需要新增并运行：

```bash
# 待实现：trace validator / comment replay fixture 检查命令
```

章节 reader/audit 落地时还要按需运行：

```bash
python3 -m json.tool <contract-json>
rg -n "source refs|claim trace|lens score|machine_status|human_status|Source Anchor|Lens Auction" <reader-md>
```

方法核探针落地时还要检查：

```bash
python3 -m json.tool <method-kernel-json>
rg -n "source refs|claim trace|lens score|machine_status|human_status|Source Anchor|Lens Auction|Body Track Gate|Claim Ledger|Candidate Tournament|Skillization Gate" <reader-facing-md>
```

## Known Boundaries

- `validate` 通过只表示机器规则通过，不表示读者体验通过。
- `delivery_status=deliverable` 或 `completed` 不能冒充人工接受。
- 旧 bakeoff、full-product、source-aligned demo 是证据或历史样本，不是当前章节写作输入。
- `docs/progress.md` 是历史进度快照，不是当前状态权威。
- `docs/next-session-prompt.md` 是从 `docs/current-task.md` 派生的启动提示，不是事实源。
- 无完整一手正文轨的书籍/长文解释页不能标为 `reader_package_pass`。
- candidate pool、claim tiers、Skillization 字段必须影响真实决策；只补字段不算方法核成立。
- `formal_skill_delivery_design_ready` 不能等同于 `formal_skill_draft_started`。
- `transferable_method_kernel_pass` 仍为 `not_verified`。
