# 历史验证器结构审计

> 快照日期：2026-07-25
> 对象：`validate.py`
> 结论：保留原位，不在本轮拆分

## 为什么现在不拆

`validate.py` 共约 9,485 行，但当前生产入口和 active tests 都不调用它。它承担的是早期
clean-seed、T2.4—T2.11 单次实验以及 T2.2 恢复架构的历史回放。把它拆成多个漂亮文件不会
让当前 2.35、Writer 或最终 Skill 更快，反而会改变大量旧命令、路径和历史身份。

因此，“文件很长”本身不是重构理由。本轮只完成调用关系和可提取边界审计。

## 结构分区

| 约略行段 | 责任 | 生命周期判断 |
|---|---|---|
| 1—1098 | clean-seed 常量、artifact policy、读取与 manifest | historical replay |
| 1099—4007 | T2.4—T2.11 逐任务验证器 | expired task-specific |
| 4008—4370 | manifest、树、run.py、materials 等仓库检查 | 部分概念可复用，但现行实现绑定历史根集合 |
| 4371—7190 | T3.6 与 T2.2 recovery policy／hash／receipt 链 | historical recovery |
| 7191—9120 | 定向入口和 synthetic self-tests | historical replay support |
| 9121—9485 | CLI 分派与全量 clean-seed 验证 | historical replay |

## 调用关系

- 当前 README 明确 `python3 -B tests/entry.py` 为 active 健康入口。
- 仓库当前代码没有 `import validate` 或 `from validate` 调用。
- 对 `validate.py` 的命令引用主要存在于 T0—T2.11 历史任务卡、T2.2 recovery 诊断和历史报告。
- 当前 `tools/run.py`、图书内容流 v2 合同和 T2.35 run 均不依赖它。

## 未来只允许按真实复用提取

满足以下条件之一时，才从历史验证器提取代码：

1. 同一机械能力出现两个当前调用方；
2. 当前生产入口需要，而 `tools/run.py` 尚不拥有；
3. 提取后能替换旧重复调用，不是再叠一层 wrapper；
4. 有 active tests 覆盖新 interface 和至少一个真实入口。

优先候选是安全读取、hash／size、排他写入和结构化 manifest；但 `tools/run.py` 已拥有其中
多项，下一步应先比较并深化现有 module，不能从 `validate.py` 复制第二套。

## 明确不做

- 不按行数机械切文件；
- 不迁移旧 T2.4—T2.11 专属检查到 active tests；
- 不让历史 clean-seed 全量 PASS 重新成为当前资格门；
- 不在没有当前调用方时重写 T2.2 recovery；
- 不删除该文件，直到历史回放的保留或替代策略另行获批并验证。
