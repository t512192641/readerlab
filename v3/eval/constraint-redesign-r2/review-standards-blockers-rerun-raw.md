# Standards 三项 blocker 限定复核原始输出

## 范围

- reviewed_at: `2026-07-10T12:02:56-04:00`
- fixed_point: `HEAD 1ed34c4`
- branch: `v3/cognitive-compounding`
- review_kind: `scoped-standards-blocker-rerun`
- rules_modified_by_reviewer: `false`
- runtime: `not-run`

本次只复核 `review-standards-final-raw.md` 的 B01—B03：全部 verification gates 的 manifest / orchestrator schema 与状态转换文字、图书全 0 路径的 judge / writer / cold-reader 职责、document map 三类身份与默认入口。未重审其他 Standards 或 Spec 项，未修改规则、case 或汇总。

## 结论

```yaml
scoped_verdict: pass
blockers_retested: 3
blockers_closed: 3
blockers_open_in_this_scope: 0
git_diff_check: pass
runtime: not-run
```

三项原 Standards blocker 均已关闭。该 scoped pass 不覆盖其他独立审查发现，不证明整个 Standards / Spec 双轴通过，也不证明真实运行、内容质量或用户体验。

## B01：manifest / orchestrator verification gates

结果：`pass`。

### 逐字段同形

| gate | manifest | orchestrator | 结论 |
| --- | --- | --- | --- |
| `source_and_fact` | status、owner、source_provenance、conditional_fact_check、scope、evidence、conflicts | 同七字段；两个子门字段和状态枚举相同 | 同形 |
| `absolute_value` | status、owner、scope、evidence、conflicts | 同五字段 | 同形 |
| `regression` | status、owner、scope、evidence、conflicts | 同五字段 | 同形 |
| `cold_read` | status、owner、scope、evidence、conflicts | 同五字段，均含 not-applicable | 同形 |
| `cold_start_or_reproduction` | status、owner、scope、evidence、conflicts | 同五字段，均含 not-applicable | 同形 |
| `run_integrity` | status、owner、scope、evidence、conflicts | 同五字段 | 同形 |
| `user_experience` | status、owner、scope、evidence | 同四字段，owner 均为 user | 同形 |

manifest 的 `required` 占位符与 orchestrator 实际输出的空字符串只表示模板待填写约束，不改变字段类型或枚举。主控可以把完整 verification 对象逐字段写入唯一 manifest，不再需要影子记录。

RI-P01 也已同步为对象形式：absolute value、regression、cold read、cold-start/reproduction、run integrity、user experience 均带各自 owner、scope 和 evidence；其 fixture 没有继续使用旧标量 schema。

### 状态文字

- `running -> awaiting-user` 和 `awaiting-user -> running` 已明确读取 `verification.user_experience.status`，不再把整个对象与标量比较。
- `running -> failed / accepted` 使用“必需门的状态”语义，与各 gate 的 `.status` 枚举一致；accepted 仍要求所有适用门 pass、不适用门明确、无 blocked/pending、预算和 claim 交集闭合。
- source/fact 聚合继续由两个嵌套子门决定，未触发条件事实核查时 request refs 必须为空；该专门聚合规则没有被对象化修订破坏。

B01 关闭。这里只证明静态 schema 与状态文字一致，没有执行真实 manifest 状态转换。

## B02：图书全 0 路径职责

结果：`pass`。

当前 `book-engine.md` 已明确写出完整顺序：

1. 三个 cognition-candidate 实例分别提交合法 0 报告。
2. required request 集合为空时 fact-checker 可以 skipped。
3. cognition-judge 仍须核对三份 0 报告、锚点与盲区，并结算 absolute value pass / selection count 0。
4. book-writer 必须实际装配正文-only 页面，不得 skipped。
5. cold-reader 必须实际检查最终页面并返回 `not-applicable`，不得 skipped。

该协议与角色合同直接一致：

- `book-writer.md` 明确 0 条接受时交付正文-only 页面，并输出 assembled page reference。
- `cold-reader.md` 明确正文-only 页面由该角色结算为 `not-applicable`。
- 既有 `role-cold-start-book-rerun-raw.md` 已按相同路径保存 writer 实际装配、cold-reader 实际返回 N/A 的静态检查结果。

较后的 `role-cold-start-book-fact-handoff-rerun-2-raw.md` 中“writer / cold-reader 可 skipped”的旧句与当前协议冲突，不能再作为当前路径结论；它作为被本轮 blocker 复核取代的历史 raw 保留。按本次任务允许的“无新专项 raw 时直接合同审查”口径，当前合同本身已消除歧义，B02 关闭。

该结果不证明三个真实候选 Agent 曾返回 0，也不证明真实 body-only 页面已生成或冷读已执行。

## B03：document map 分类与默认入口

结果：`pass`。

- `current-authority`、`routed-evidence`、`retired-preserved` 现在按表中范围互斥列示；原先把整个 eval 目录同时覆盖当前 raw 和旧 raw 的重叠已删除。
- 当前 raw 由 regression suite、calibration 或 final review 的明确引用决定；未被这些当前汇总引用的旧 raw 才进入 retired preserved。两集合由“是否被当前汇总明确引用”确定，不再靠文件名猜最新。
- examples 目录当前只列在 current authority；其自身 README 又把实际读取权限收窄到认知裁判和回归执行者按 case 路由，作者、提名者、候选者、成文者和冷读者不得加载。因此没有同时落入 routed / retired，也不会向普通生产角色回流历史答案。
- 默认入口仍只有 `AGENTS.md + v3/current-task.md`。README 与 document map 只作稳定定位，Phase 4、Skill、calibration、历史样本、失败成品和 retired 文件均未回到默认启动链。
- retired 文件若要恢复，仍须用户明确决定并更新 current-task；当前没有移动、删除或重命名历史文件。

B03 关闭。该结果只证明身份表和读取路由静态互斥，不证明 dirty worktree 已物理归档或形成提交。

## 机械检查

- `git diff --check`: exit 0。
- branch: `v3/cognitive-compounding`。
- HEAD: `1ed34c4`。
- 工作区仍 dirty；本执行者没有 reset、checkout、删除、移动、暂存或提交文件。

## Scoped final verdict

```yaml
B01_manifest_orchestrator_schema: pass
B02_book_zero_path_roles: pass
B03_document_lifecycle_routing: pass
scoped_verdict: pass
runtime: not-run
```

可声称：前次 Standards 终验点名的三项 blocker 已按当前文件完成限定静态复核并关闭。

不可声称：整个 Standards 轴、Spec 轴或双轴验收已通过；真实图书线、Skill 线、ReaderLab 流水线、内容质量、用户体验或 Phase 4 已通过；可以开始 Demo。
