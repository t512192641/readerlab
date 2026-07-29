# Expert Teaching Skill v0.1.2 Code Review Brief

本轮只审查 Skill 候选的工程实现，不进行新的语义实验，不比较路线，不评价 Writer。

## Review questions

1. 是否形成了可执行的 Skill，而不是复制 T2.38 实验文档？
2. 是否只把已验证的 Expert Teaching 控制能力 Skills 化？
3. 是否存在 U01／Social Connection Model 特化，导致不能替换原文、框架和来源表？
4. 是否能用固定输入和人工注入输出运行新的样本？
5. 状态门、Agent ID 隔离和双门产品包条件是否由代码保证？
6. 是否仍需人工大量创建目录、计算 hash、拼 Prompt 或判断终局？
7. 是否错误声明为完整流水线或生产 runtime？
8. 0.1.0／0.1.1／0.1.2 是否可明确共存、错误版本是否 fail closed、旧 fingerprint 是否不受 dispatcher 污染？
9. 来源 allowlist 的三种状态、source-map／allowlist 闭合、redirect、source-access 回执、输出 URL 边界和 replay hash 是否准确？
10. 中文表达规则、内容泄露门、ledger／manifest 语义和 `not_integrated` 状态是否准确？

## Review surface

- Skill entry and resources: `.agents/skills/readerlab-book-expert-teaching/`，重点为独立的
  `versions/0.1.2/`、`CURRENT_VERSION` 与根目录 `run-current.py`；0.1.1 和根入口是不可变历史实现。
- Deterministic tests: `tests/test_skill.py`、`tests/fixtures/t2.38-replay.json`、结构化 allowlist 和两份
  `t2.38-*-source-access.json` fixture。
- Stage status: `docs/stage-implementation-status.md`。
- Route pointer: `blueprints/PIPELINE-MAP.md`。
- Run and fixture evidence: T2.38 frozen run, read-only。

## Expected non-claims

Code review must not turn deterministic tests into product acceptance, claim semantic generalization from one
fixture, or authorize migration samples、语义 Agent、Writer、Discovery、ABC 或完整 orchestrator。任何对合同、
模板或脚本的未来修改都需要新 Skill 版本和 change receipt；0.1.0 尚未运行迁移样本，0.1.0、0.1.1 与 0.1.2 结果
不得静默混算。模型、reasoning、network、retry 和 Prompt 字段在没有 receipt 时只能写
`controller_declared`，不能写成已验证执行事实。
