# ReaderLab v0.4 Routing Task

version: `v0.4-control-candidate`
date: `2026-07-30`
status: `control-only / not-executed`

## Purpose

本文件只负责对 C5、K10、C1 做彼此独立的路由审计。路由类别是控制状态，不是候选语义结论；
三路由必须分别核对，禁止从一个候选机械复制到另一个候选。

## Input whitelist

路由审计只允许读取：

- `contract-task.md` 的字段与停止门；
- `run-manifest.md` 的基线、范围和执行限制；
- v0.4 用户规范中已冻结的三条路由标签；
- 当前候选 packet 中仅用于确认 ID 和路由身份的控制元数据。

禁止读取候选语义正文、source context、搜索结果、历史答案、Expert／Writer 产物或其他候选的语义
材料；不得据此重新发现、合并或重命名候选。

## Independent route map

| candidate | current class | allowed path | hard stop | next roles |
|---|---|---|---|---|
| `C5` | `CORE` | `Expert → structured asset → Writer → fidelity review → cold-read` | 任一路由输入、合同或门不满足即停止 | 仅按顺序进入上述阶段 |
| `K10` | `DEEPENING` | 只到 `observation structure` | 到 observation structure 后停止 | 不得进入 Writer；不生成下游读者稿 |
| `C1` | `HOLD` | 不启动内容链 | 立即停止 | 不得进入 Expert；不得进入 Writer |

## Fixed output fields

每个候选独立输出一条路由记录，字段固定如下：

```text
candidate_id: C5 | K10 | C1
current_class: CORE | DEEPENING | HOLD
allowed_stages: <exact stage names from the route map>
forbidden_stages: <exactly listed blocked stages>
independence_check: PASS | FAIL
route_check: PASS | STOP
stop_reason: <empty only when route_check is PASS>
next_action: <one permitted control action or STOP>
```

`route_check: PASS` 只表示路由闭合，不表示候选内容值得生产、Expert 合格或 Writer 合格。

## Non-copy rule

- 不得复制上一候选的 `allowed_stages`、`stop_reason`、字段值、外部对象或语义判断。
- 每个候选必须从自身 ID、当前类和冻结控制元数据重新核对；缺失控制元数据即 `STOP`。
- `CORE` 不能自动推导为内容通过；`DEEPENING` 不能自动升级为 Writer；`HOLD` 不能因其他候选
  通过而解冻。

## Stop and acceptance gate

路由发现任何 ID、类别、路径顺序或禁用阶段不一致时，立即停止全部下游，不修正语义、不追加候选、
不重跑搜索。验收门是三条记录各自完整、互不复制，且与上表逐字段一致；这不是产品接受门。
