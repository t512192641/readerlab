# Expert Teaching Skill v0.1 Code Review Brief

本轮只审查 Skill 候选的工程实现，不进行新的语义实验，不比较路线，不评价 Writer。

## Review questions

1. 是否形成了可执行的 Skill，而不是复制 T2.38 实验文档？
2. 是否只把已验证的 Expert Teaching 控制能力 Skills 化？
3. 是否存在 U01／Social Connection Model 特化，导致不能替换原文、框架和来源表？
4. 是否能用固定输入和人工注入输出运行新的样本？
5. 状态门、Agent ID 隔离和双门产品包条件是否由代码保证？
6. 是否仍需人工大量创建目录、计算 hash、拼 Prompt 或判断终局？
7. 是否错误声明为完整流水线或生产 runtime？
8. 阶段实现状态、蓝图 pointer、版本纪律和 T2.38 fixture 是否准确？

## Review surface

- Skill entry and resources: `.agents/skills/readerlab-book-expert-teaching/`。
- Deterministic tests: `tests/test_skill.py` and `tests/fixtures/t2.38-replay.json`。
- Stage status: `docs/stage-implementation-status.md`。
- Route pointer: `blueprints/PIPELINE-MAP.md`。
- Run and fixture evidence: T2.38 frozen run, read-only。

## Expected non-claims

Code review must not turn deterministic tests into product acceptance, claim semantic generalization from one
fixture, or authorize migration samples, Writer, Discovery, ABC, or a complete orchestrator. Any future change
to contracts, templates or scripts requires a new Skill version and change receipt; v0.1.0 and later samples
must not be silently mixed.
