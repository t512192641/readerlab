# gstack/spec R2 资产卡冷启动测试输入

本文件是冷启动测试给无上下文 Agent 的唯一材料。测试记录另存 `v3/pilots/gstack-spec-r2-cold-start-test.md`。

## 卡 1：五问锁 Why 门

| 字段 | 内容 |
| --- | --- |
| purpose | 防止 Agent 把一句模糊愿望直接包装成貌似完整的 issue。 |
| reader | 没读过 `gstack/spec`、但要设计需求澄清流程的 Agent。 |
| use_boundary | 适合“用户已经想进入 backlog，但需求还不能执行”的场景；不适合纯探索、闲聊或尚未决定是否要做的想法。 |
| selection_rule | 如果当前任务还无法回答受影响对象、当前行为、目标行为、为什么现在做、怎样算完成，就先启用本卡。 |
| first_step | 先问五个问题：谁受影响、现在发生什么、应该怎样、为什么现在、怎样算完成。五问未闭合，不进入方案设计。 |
| failure_if_omitted | Agent 会过早给方案，后续执行者只能猜范围、验收和优先级。 |

## 卡 2：读证据后再问技术问题

| 字段 | 内容 |
| --- | --- |
| purpose | 让 Agent 的技术问题建立在仓库事实上，而不是把通用 checklist 丢给用户。 |
| reader | 需要把模糊需求转成工程任务的新 Agent。 |
| use_boundary | 适合项目内功能、bug、重构、架构任务；如果真是绿地任务，也必须先说明搜索了什么且没有证据。 |
| selection_rule | 只要准备问技术实现、数据、接口、测试或架构问题，就必须先读至少一个相关文件、目录或配置，并在问题里引用证据。 |
| first_step | 先搜索或阅读最可能相关的项目证据，再只问无法从证据回答的问题。 |
| failure_if_omitted | 用户会被迫替 Agent 做上下文定位，issue 也会缺少 verified current state。 |

## 卡 3：出口扫描与执行前保护现场

| 字段 | 内容 |
| --- | --- |
| purpose | 防止 spec 在发布、归档或派生执行前泄露敏感内容，或让执行 agent 基于脏 worktree 开工。 |
| reader | 要把 spec 发到 GitHub、归档或交给另一个 agent 执行的 Agent。 |
| use_boundary | 适合任何会把草稿交给外部系统、公开 issue、长期 archive 或新 agent 的流程；不适合只在本地临时思考且不落盘的草稿。 |
| selection_rule | 如果下一步是 issue、archive、spawn agent 或其他离开当前对话的出口，就启用本卡。 |
| first_step | 先对即将送出的精确文本做语义审查和脱敏扫描；若要 spawn agent，再检查当前 worktree 是否有未提交修改，并让用户选择继续、stash 或取消。 |
| failure_if_omitted | 可能把人名负面判断、内部策略、密钥、PII 或半成品工作区状态带到不该去的地方。 |
