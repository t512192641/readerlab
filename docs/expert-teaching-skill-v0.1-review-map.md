# Expert Teaching Skill v0.1.1 Review Map

## 入口

当前版本：

```bash
python3 .agents/skills/readerlab-book-expert-teaching/scripts/run-current.py <command> ...
```

显式入口：

```bash
python3 .agents/skills/readerlab-book-expert-teaching/versions/0.1.1/scripts/run.py <command> ...
python3 .agents/skills/readerlab-book-expert-teaching/scripts/run.py <command> ...  # 历史 0.1.0
```

`CURRENT_VERSION` 当前为 `0.1.1`。历史 0.1.0 根入口不可变；run 的记录版本、入口版本和 fingerprint
必须一致，错误入口 fail closed。

命令：`init`、`seal-expert`、`seal-review`、`build-product-pack`、`verify`、`archive`。

## 状态机

```text
NONE → EXPERT_OPEN → REVIEW_OPEN → REVIEW_TERMINAL → PRODUCT_READY
```

`REVIEW_TERMINAL` 只有同时为 `SOURCE_FIDELITY_PASS` 和 `TEACHING_PASS` 才能进入
`PRODUCT_READY`；其他终局硬停止且不得创建产品包。

## 输入与输出

`init` 固定 `source.md`、`framework.md`、`source-map.md` 和结构化 `source-allowlist.json`，写入
bytes／SHA-256、任务、read set、Prompt freeze 和 stage 0。任务只展示 `allowed` URL 及显式登记的
redirect；`reference_only` 与 `blocked` 不进入网络 allowlist。人工 Expert 只写两份 `raw/` 文件；
`seal-expert` 与 `seal-review` 均拒绝新增或 blocked URL（review 可引用输入中已有的 reference-only URL），
再分别冻结 stage 1／2。双门通过后控制层把原文转成可读 Markdown，加完整教学课与通用中文问题，写产品包
和 stage 3。`archive` 先 `verify`，再把 run 打包；测试同时核验 archive 条目集合和冻结文件 hash，archive
hash 留在命令输出／外部账本而不写入自身。

## 自动化与人工边界

Skill 自动化目录、输入复制、allowlist schema／状态／redirect 验证、hash、Prompt/read-set、状态转换、
输出非空/UTF-8、Agent ID 隔离、终局解析、来源引用边界、产品包内容门、HTML/XHTML 净化、freeze、verify
和 archive。人工仍决定何时运行、选定原文／框架／来源范围、启动两个新上下文、实际来源阅读、Expert 写作、
独立审核和产品接受；Skill 自身语义调用为 `none`。

## 隔离与越界防护

任务文件逐项列出本地 read set 和结构化 source allowlist 的 `allowed` URL；Skill 记录 Agent ID、模型、
reasoning、network、retry、Prompt modified，但这些运行字段标为 `controller_declared`，不是自动核验的
模型执行 receipt。它是功能性上下文隔离，不是 OS 级沙箱；Agent 的真实启动与工具读取由人工总控负责。

## T2.38 mechanical replay

`.agents/skills/readerlab-book-expert-teaching/tests/fixtures/t2.38-replay.json` 记录 T2.38 source、source map、
Expert draft、Expert source map、review、结构化 allowlist 和冻结产品包 hash。Skill-local test 创建临时 run，
逐项校验 fixture hash，使用 T2.36 冻结输入和 T2.38 已冻结 Expert／review 文件注入，依次调用六个入口中的
`init`、`seal-expert`、`seal-review`、`build-product-pack`、`verify`、`archive`；回放后核验新版本产品
hash、旧冻结产品 hash、archive 成员集合和成员 hash。不启动模型、不打开新来源、不把临时 run 当新语义实验。

## v0.1.1 review surface

- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/SKILL.md`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/contracts/`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/templates/`
- `.agents/skills/readerlab-book-expert-teaching/versions/0.1.1/scripts/`
- `.agents/skills/readerlab-book-expert-teaching/CURRENT_VERSION`
- `.agents/skills/readerlab-book-expert-teaching/scripts/run-current.py`
- Skill-local tests and the T2.38 replay fixtures

根目录 `SKILL.md`、contracts、templates、agents、scripts 和 `VERSION` 是历史 0.1.0 实现，保持不变，
只作为明确历史入口和复验坐标。

## 明确未实现

Discovery、ABC、Writer、Reader 压缩、Fidelity、B2 装配、Obsidian／tandem-comments、自动产品 Judge、
知识库、自动下一阶段调用和完整 ReaderLab orchestrator 均未实现、未集成、未获得生产资格。
