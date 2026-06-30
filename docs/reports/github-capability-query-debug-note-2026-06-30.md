# GitHub 收藏整理查询链路调试说明

日期：2026-06-30

## 结论

本轮遇到的问题不是“本地能力库没有相关库存”，而是 GitHub 收藏整理项目的正式推荐/检索链路当前不可用。

面向小白可以这样理解：网页服务已经能启动，也能回答“我还活着”；但真正负责“根据问题检索和推荐能力”的那条链路卡住或报错了。所以现在不能用它的失败结果判断库存有没有命中，只能说查询工具本身还没有恢复。

## 已确认事实

- 服务通过 `npm run web` 从 `/Users/tianqiang/Documents/github收藏整理` 启动。
- `http://127.0.0.1:5173/api/health` 返回：

```json
{"ok": true}
```

- `/api/recommend` 的 `POST` 请求长时间无响应或超时。
- `scripts/query-local-capabilities.py --mode search` 会报错，关键错误是：

```text
ImportError: cannot import name '_regex' from partially initialized module 'regex'
```

- 上述报错调用链涉及 `sentence_transformers` / `transformers` / `regex`。
- 本轮临时只读查询过 `data/v5-source-refresh-2026-06-11.sqlite`，查看了 `v5_repo_cards`、`ability_units` 等表，只把它们当作库存线索。
- 这些只读 SQLite 线索不等于正式推荐接口已经恢复，也不等于 ReaderLab 后续可以绕过正式查询链路。

## 风险边界

当前状态不能被表述为“库存里没有结果”。

更准确的说法是：正式查询服务或依赖链路坏了，导致推荐/检索结果不可用。在恢复 `/api/recommend` 和本地查询脚本之前，任何“没有命中”的判断都不可靠。

## 可复制 debug prompt

```text
你是 GitHub收藏整理 项目的调试会话。目标是恢复本地能力库的正式查询链路，不要把问题临时绕成手工 SQLite 查询。

启动规则：
1. 先读全域 AGENTS 和项目 AGENTS。
2. 再按项目声明的 memory map 读取必要状态：current-task、dev-state、decisions、agent-run-ledger。只读完成本次 debug 所需的最小内容。
3. 不要复制整份状态文件到回答里；状态文件是事实源，不是要粘贴的材料。
4. 不要新建无关过程文档、草稿、计划文档或临时 handoff。
5. 按 CTK 的短项目状态启动格式组织上下文：当前事实、目标、非目标、风险、验收标准、最小执行路径。

已知问题事实：
- 服务可以通过 `npm run web` 从 `/Users/tianqiang/Documents/github收藏整理` 启动。
- `http://127.0.0.1:5173/api/health` 返回 `{"ok": true}`。
- `/api/recommend` 的 `POST` 请求长时间无响应或超时。
- `scripts/query-local-capabilities.py --mode search` 报错，关键错误是 `ImportError: cannot import name '_regex' from partially initialized module 'regex'`。
- 报错调用链涉及 `sentence_transformers` / `transformers` / `regex`。
- 曾临时只读查询 `data/v5-source-refresh-2026-06-11.sqlite` 的 `v5_repo_cards`、`ability_units` 等表，但这只是库存线索，不代表正式推荐接口恢复。

debug 目标：
恢复 GitHub收藏整理项目的本地能力库正式查询链路，使 ReaderLab 这类查询可以走项目既有推荐/检索入口，而不是靠手工查 SQLite 表。

非目标：
- 不改 ReaderLab 项目。
- 不把手工 SQLite 查询包装成正式恢复。
- 不新增无关依赖或重构大范围架构，除非先说明必要性、风险和验证方式。
- 不把当前状态解释成“库存没有结果”。

建议检查方向：
1. 确认 `/api/recommend` 请求卡在哪里：入口路由、推荐服务、embedding 初始化、模型加载、SQLite 查询、还是异常未返回。
2. 定位 `regex` / `sentence_transformers` / `transformers` 的导入冲突：优先检查本地文件命名、虚拟环境、依赖版本、缓存和 Python import path。
3. 修复后用最小 ReaderLab 查询做真实请求验证。
4. 如有必要，补一个最小回归检查，防止 health 正常但 recommend/query 脚本实际不可用。

验收标准：
- `http://127.0.0.1:5173/api/health` 仍正常返回 `{"ok": true}`。
- `/api/recommend` 能对 ReaderLab 查询返回 `ok` / `insufficient` / `degraded` 之一，并且不超时。
- `scripts/query-local-capabilities.py --mode search` 不再因为 `regex` / `sentence_transformers` / `transformers` 导入链报错。
- 必要时补一个最小回归检查，覆盖“服务健康但推荐链路不可用”的情况。
- 把本次 debug 的事实、修复、验证命令和剩余风险记录到 GitHub收藏整理项目自己的 `agent-run-ledger` / `dev-state`，不要写到 ReaderLab 的项目记忆里。

最终汇报请区分：
- 服务启动是否恢复；
- 正式推荐接口是否恢复；
- 本地脚本查询是否恢复；
- ReaderLab 查询是否得到可用结果；
- 还有哪些风险未关闭。
```

