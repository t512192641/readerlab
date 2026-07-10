# 主控样本确认门最终复核原始输出

## 复核边界

- 时间：`2026-07-10T07:16:21-04:00`。
- 本次只复核：`confirmation_required / user_confirmation` 组合不变量，以及 `planned -> running / awaiting-user / failed` 三路。
- 本次读取：仅 `v3/skill/templates/run-manifest.md` 与 `v3/skill/roles/orchestrator.md` 中相关字段、组合规则和状态转换。
- 本次未复核：mixed、dispatch/stages、gate、claims、运行态等待及其他前轮已审项目。
- 上下文声明：本执行者做过前四份主控 raw；本次不是零上下文，但当前 verdict 只依据现行确认门文本。
- 保留规则：前四份 raw 保留不改；本次不修改规则文件。

## 总结论

- scoped verdict：`pass`。
- 上轮唯一剩余阻断已关闭：合法组合被明确冻结，`planned -> running` 只接受两个成功组合，`pending` 与 `declined` 分别进入 awaiting-user 与 failed，无效组合不得开跑。
- 通过范围：只证明样本确认门的静态 schema 与三路转换闭合；本次没有重新执行完整主控冷审查或真实 run。

## 1. 字段组合不变量

- 当前字段：
  - `confirmation_required: true | false`
  - `user_confirmation: not-required | pending | confirmed | declined`
- 当前不变量：
  - `false` 只能搭配 `not-required`；
  - `true` 只能搭配 `pending | confirmed | declined`；
  - 其他组合无效，run 保持 `planned` 并标 schema fail。
- verdict：`pass`。
- 判断：此前可出现的 `false + pending`、`false + confirmed`、`true + not-required` 等矛盾组合已被明确判无效，主控不再拥有自由解释空间。

## 2. `planned -> running`

- 允许条件：来源、route、模式、隔离输出和预算均已填写，且样本确认只能是：
  - `false + not-required`；或
  - `true + confirmed`。
- 禁止条件：`pending`、`declined` 和任意无效字段组合均不得进入 running。
- verdict：`pass`。
- 判断：上轮指出的 `declined` 或 `true + not-required` 绕过确认进入执行的问题已被直接封死。

## 3. `planned -> awaiting-user`

- 条件：必需确认仍为 `pending`；结合组合不变量，只能对应 `true + pending`。
- 保护：awaiting-user 期间不得产生执行 dispatch。
- 后继：确认变为 `confirmed` 时回 `planned` 重新核对，再按 running guard 判断；变为 `declined` 时进入 `failed`。
- verdict：`pass`。
- 判断：等待态有唯一合法入口和正反两个后继，不再悬空，也不能跳过计划态复核直接执行。

## 4. `planned -> failed`

- 条件：
  - 必需样本确认是 `declined`；或
  - 确认字段组合无效且无法在本 run 内修复。
- verdict：`pass`。
- 判断：用户拒绝与不可修复 schema 冲突都有明确终态；无效但可修复的组合保持 planned，修复后重新走三路判断，边界清楚。

## 三路互斥与完备性

| 组合 / 条件 | 合法下一状态 | 结果 |
| --- | --- | --- |
| `false + not-required` 且其他前置完整 | `running` | 无需确认，允许开跑。 |
| `true + confirmed` 且其他前置完整 | `running` | 已确认，允许开跑。 |
| `true + pending` | `awaiting-user` | 不得 dispatch。 |
| `true + declined` | `failed` | 不得 dispatch。 |
| 任意无效组合，可修复 | `planned` | 标 schema fail，修复后重判。 |
| 任意无效组合，不可修复 | `failed` | 终止本 run。 |

- 互斥性：同一合法组合不会同时满足 running、awaiting-user 和 failed。
- 完备性：四个合法组合与无效组合的可修复 / 不可修复分支都有去向。
- scoped verdict：`pass`。

## 最终可声称范围

- 可以声称：样本确认字段不变量和 `planned -> running / awaiting-user / failed` 三路已经闭合；前一轮留下的最后一个状态机 blocker 已修复。
- 不可以仅凭本文件声称：真实 run 已按状态机执行、主控整体完成 fresh 冷启动复验，或其他未在本轮重读的合同项获得新的验收证据。

最终 scoped verdict：`pass`。
