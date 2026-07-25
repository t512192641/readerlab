# 历史验证器结构审计

> 快照日期：2026-07-25
> 对象：`archive/legacy-code/validate-clean-seed.py`
> 结论：已按历史回放整体隔离；当前不拆分、不提取

## 当前判断

`validate.py` 共约 9,485 行，但当前生产入口和 active tests 都不调用它。它承担的是早期
clean-seed、T2.4—T2.11 单次实验以及 T2.2 恢复架构的历史回放。接近一万行、混合多轮
任务责任的单文件不符合当前工程应有的 locality 和 module 结构；没有当前调用方只说明它不在
生产关键路径，不能把这种结构解释为合理。

同时，把它按行数切成多个文件也不会自动减少复杂度，反而可能改变旧命令、路径和历史身份。
正确处置目标是减少当前工程负担，而不是美化全部历史代码。

## 实施终局

- 9,485 行旧实现已原字节迁移到 `archive/legacy-code/validate-clean-seed.py`，SHA-256 为
  `6f7220c9e492c5e94291728c5242f3ce8818b0c0c1148d581700d68763d6b855`。
- 根目录 `validate.py` 只保留 38 行兼容 adapter，并在执行前核对上述固定身份。
- 迁移前后 `python3 -B validate.py --self-test-recovery` 均退出 0，stdout／stderr 的
  SHA-256 完全一致。
- 当前健康入口仍为 `python3 -B tests/entry.py`，没有从旧实现复制第二套通用逻辑。

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

## 下一步处置原则

每一段逻辑必须取得以下终局之一：

- `current-reusable`：现行流程存在真实调用价值，提取到少量深 module；
- `historical-replay`：仍需复验历史身份，退出默认入口并保留明确兼容方式；
- `expired-task-specific`：只服务结束任务，保留证据后列入删除候选；
- `dead-or-duplicated`：无调用或已被现行工具替代，验证后删除；
- `unknown`：证据不足，暂不修改。

只有满足以下条件之一，才把逻辑提取到现行 module：

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
- 不把“历史”当作永久留在根目录和当前工程结构中的理由；
- 不删除任何尚未证明可恢复的历史回放或唯一证据。
