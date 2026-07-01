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
- 高阶讲解方法：`docs/high-order-explanation-method.md`
- 高阶讲解 contract 文档：`docs/contracts/high-order-explanation-v1.md`
- 验收 gate：`docs/eval-gates.md`
- 运行账本：`docs/agent-run-ledger.md`

## Tool State

- `scripts/readerlab.py` 主要支持 Skill 包导入、阅读包 validate、contract validate、proof renderer、eval runner、批注读取和回复。
- 图书/长文正式导入生成器尚未完成；当前《埃隆之书》章节循环仍主要依赖 repo 内报告和手工/agent 循环。
- renderer / eval runner 是 proof 级工具，不能代表完整生成器能力或人工阅读验收。
- Markdown 是展示层；source registry、location map、contracts、eval 和人工状态才是事实层。

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

章节 reader/audit 落地时还要按需运行：

```bash
python3 -m json.tool <contract-json>
rg -n "source refs|claim trace|lens score|machine_status|human_status|Source Anchor|Lens Auction" <reader-md>
```

## Known Boundaries

- `validate` 通过只表示机器规则通过，不表示读者体验通过。
- `delivery_status=deliverable` 或 `completed` 不能冒充人工接受。
- 旧 bakeoff、full-product、source-aligned demo 是证据或历史样本，不是当前章节写作输入。
- `docs/progress.md` 是历史进度快照，不是当前状态权威。
- `docs/next-session-prompt.md` 是从 `docs/current-task.md` 派生的启动提示，不是事实源。
