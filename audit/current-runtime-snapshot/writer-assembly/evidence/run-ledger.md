# Writer 装配运行记录

## 身份与边界

- 工作根：`/private/tmp/readerlab-new-route-20260726/writer-assembly/`
- 仓库模式：只读
- 起始与结束 HEAD：`90c94450e5d4550da78d775111d364167542f5cd`
- 合法当前 run：`runs/T2.35-CH08-D3-EXPERT-P2-01`
- Reader id：`T235-D3-READER-V2-A1`
- Writer v2 产品状态：`ACCEPTED`
- P3 产品状态：`PENDING`

## 执行记录

1. 冻结当前合同、任务卡、合法 run 的 B1、Expert、锁定知识卡、审核结果、P2 gate 和产品已接受
   Writer v2；记录逐文件 SHA-256。
2. 从 Expert 明示的“实际触发本课的完整段落（逐字）”机械提取锚点；锚点为 767 UTF-8
   bytes，SHA-256 为
   `ad957092bde87bb9eb54ad5fe54ac4939229631024d1e4c0c37afe338d059b77`，
   在冻结 B1 中出现 1 次。
3. 对 Writer v2 只执行两项获准小修：补入“禁忌交换”自然定义；把象征性承认结果收窄为
   “部分愤怒和暴力反对指标”。
4. 机械装配完整章节候选，并验证删除插入块后恢复原 B1、提取边界后恢复 Reader。
5. 用两份互不共享上下文的独立检查分别执行 Assembly Boundary / Exact-Byte Check 与
   Writer Fidelity Check。
6. 两道技术门均通过后，才机械复制出唯一 P3 产品审阅入口；随后停止。

## 失败、偏差与恢复

- 装配脚本第一次预运行把 Reader 末尾换行排除在候选单元之外，得到过一个
  `cbb407…` 的临时章节 hash。该结果在冻结和独立检查前被发现，未进入候选、审阅入口或
 任何正式路径。脚本随后改为保留 Writer 输入全部字节，并重新运行；最终 Reader 与章节
 hash 分别为 `6cd3f522…` 和 `3042da11…`。
- 启动第一道独立检查时，因 Discovery 并发位未释放共发生 5 次
  `agent thread limit reached`。期间候选保持冻结，没有降低独立检查标准，也没有由小组长
 代判。并发位释放后按原 rubric 重新启动成功。
- 没有内容级失败、没有越权小修、没有锚点冲突。

## 独立检查运行参数

### Assembly Boundary / Exact-Byte Check

- 任务：`/root/writer_lead/assembly_check`
- 上下文：`fork_turns=none`
- 角色：`default`
- reasoning effort：`high`
- model override：无；继承当前总控路由，协作工具未暴露最终 backend model id，因此精确
  model id 为 `unknown`
- 终局：`PASS`
- 结果 SHA-256：`70cd60707bde84c163273e5d62bddd7598ef195f941a271eced8b1842ba2a601`

### Writer Fidelity Check

- 任务：`/root/writer_lead/fidelity_check`
- 上下文：`fork_turns=none`
- 角色：`default`
- reasoning effort：`high`
- model override：无；继承当前总控路由，协作工具未暴露最终 backend model id，因此精确
  model id 为 `unknown`
- 终局：`保真通过`
- 结果 SHA-256：`95791c47fb738bbf566b4db0f9018c114de900523b6532760e034cb53c7ab79f`

模型 token 与金额 telemetry 未由协作工具返回，成本为 `unknown`，不得臆测为零。

## 终局

- implemented：候选 Reader、完整章节候选和唯一产品审阅入口均存在。
- integrated：Reader 已在候选层按合法锚点装入完整 B1；未集成生产 B2。
- verified：两道独立技术检查通过，候选与审阅入口 hash 一致。
- accepted：Writer v2 已接受；完整章节 P3 尚未接受。
- promotion：未执行。
