# Expert Teaching Skill v0.1 Review Map

## 入口

```bash
python3 .agents/skills/readerlab-book-expert-teaching/scripts/run.py <command> ...
```

命令：`init`、`seal-expert`、`seal-review`、`build-product-pack`、`verify`、`archive`。

## 状态机

```text
NONE → EXPERT_OPEN → REVIEW_OPEN → REVIEW_TERMINAL → PRODUCT_READY
```

`REVIEW_TERMINAL` 只有同时为 `SOURCE_FIDELITY_PASS` 和 `TEACHING_PASS` 才能进入
`PRODUCT_READY`；其他终局硬停止且不得创建产品包。

## 输入与输出

`init` 固定 `source.md`、`framework.md`、`source-map.md`，写入 bytes／SHA-256、任务、read set、
Prompt freeze 和 stage 0。人工 Expert 只写两份 `raw/` 文件；`seal-expert` 写 stage 1 并打开审核。
人工审核只写一份 review；`seal-review` 写 stage 2 并记录两个终局。双门通过后控制层把原文转成可读
Markdown，加完整教学课与固定问题，写产品包和 stage 3。`archive` 先 `verify`，再把 run 打包，
archive hash 留在命令输出／外部账本而不写入自身。

## 自动化与人工边界

Skill 自动化目录、输入复制、hash、Prompt/read-set、状态转换、输出非空/UTF-8、Agent ID 隔离、终局
解析、产品包内容门、HTML/XHTML 净化、freeze、verify 和 archive。人工仍决定何时运行、选定原文／框架／
来源范围、启动两个新上下文、实际来源阅读、Expert 写作、独立审核和产品接受。

## 隔离与越界防护

任务文件逐项列出本地 read set 和 source-map allowlist；Skill 记录 Agent ID、模型、reasoning、network、
retry、Prompt modified。它是功能性上下文隔离，不是 OS 级沙箱；Agent 的真实启动与工具读取由人工总控负责。

## T2.38 mechanical replay

`.agents/skills/readerlab-book-expert-teaching/tests/fixtures/t2.38-replay.json` 记录 T2.38 输入／输出
hash。Skill-local test 创建临时 run，使用 T2.36 冻结输入和 T2.38 已冻结 Expert／review 文件注入，
依次调用六个入口中的 `init`、`seal-expert`、`seal-review`、`build-product-pack`、`verify`、`archive`；
不启动模型、不打开新来源、不把临时 run 当新语义实验。

## 明确未实现

Discovery、ABC、Writer、Reader 压缩、Fidelity、B2 装配、Obsidian／tandem-comments、自动产品 Judge、
知识库、自动下一阶段调用和完整 ReaderLab orchestrator 均未实现、未集成、未获得生产资格。
