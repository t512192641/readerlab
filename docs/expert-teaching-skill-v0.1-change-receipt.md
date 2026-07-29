# ReaderLab Book Expert Teaching Skill 0.1.1 change receipt

- previous version: `0.1.0`
- new version: `0.1.1`
- baseline commit: `66eeaa1d8a068df3e73848717ee20b0c87b105918`
- branch: `feature/readerlab-book-expert-teaching-skill-v0.1`
- change type: engineering-boundary hardening only

## 修复内容

1. 保留根目录不可变的 0.1.0 实现，增加独立 `versions/0.1.1/`、`CURRENT_VERSION` 和显式 current
   dispatcher；run 的版本、入口和 fingerprint 不一致时 fail closed。
2. 将来源访问改为带 schema 的 `allowed`／`reference_only`／`blocked` allowlist，显式登记 redirect，
   任务只展示 allowed URL，Expert／review 输出的新增或 blocked URL 失败。
3. 把稳定中文表达、教学整理与原作者正式方法的区分写入 0.1.1 合同和实际 Expert task，产品问题改为
   通用中文表达。
4. 将产品正文泄露门从 M1／M2／M3／Writer 关键词改为内部路径、控制标题、评分／深度自证和 route 元数据
   检查；合法正文出现同名词不再误杀。
5. 加强 T2.38 mechanical replay：逐项核验 fixture 输入／输出 hash、新旧产品包身份、archive 条目集合和
   archive 成员 hash；回放仍不调用模型或网络。
6. 修正 manifest／ledger 语义：Skill 自身语义调用为 `none`，外部上下文与模型、reasoning、network、
   retry、Prompt modified 字段标记 `controller_declared`，生产状态为 `not_integrated`。

## 为什么修改

外部 Code Review 指出，单一安装目录会让升级后的 current 实现覆盖历史复验坐标；无结构的 URL 提取会把
reference-only 或未知来源变成隐含网络权限；稳定表达和泄露检查若只停留在说明中无法约束实际任务；回放
如果不逐项校验 hash 和 archive 内容身份，不能证明它仍是同一冻结证据。上述修改只补确定性边界，不改变
Expert Teaching 的语义目标、双门终局或人工编排定位。

## 版本与结果隔离声明

- `0.1.0` 尚未运行迁移样本；本次没有运行迁移样本，也没有启动语义 Agent。
- `0.1.0` 和 `0.1.1` 的 run、fingerprint、产品 hash 和判断结果不得静默混算。
- T2.38 replay 只是既有冻结字节的机械回放，不产生新的语义结果或产品判词。
- 后续若修改 0.1.1 合同、模板或脚本，必须再发布新版本并生成新的 change receipt。

## 验证范围

已登记范围为 Skill-local deterministic tests（24/24）、repository active tests（35/36；唯一失败为基线遗留的
118 个未登记 Markdown 资产穷举项）、T2.38 mechanical replay、quick validation、`git diff --check` 和敏感信息
检查；未授权 Writer、Discovery、ABC、迁移样本或完整 runtime。
