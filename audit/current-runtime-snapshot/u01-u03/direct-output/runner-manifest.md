# D 路线运行清单

## 运行身份

- 实际模型：GPT-5（Codex）
- 思考强度：unknown
- 唯一搜索工具：本会话内置 Web 搜索与网页打开工具
- 路线：D 直接路线

## 逐 U 调用与证据

| 单元 | 查询数 | 打开页面数 | 核验来源数 | 说明 |
|---|---:|---:|---:|---|
| U01 | 1 | 2 | 2 | Cambridge Core 的 Young 原始论文页；Springer 的 Zheng 论文页。 |
| U02 | 1 | 3 | 2 | Washington Law Review 与 Stanford 论文 PDF 成功核验；另有 1 个页面打开返回内部错误，未计入来源数。 |
| U03 | 3 | 4 | 3 | MIT Press 原始论文检索记录、Hartford Institute 学术综述、University of Chicago Press 图书页；4 次页面打开中 2 次因站点 403/重定向失败，均如实计入打开页面数。 |

所有单元均满足：查询不超过 10、打开页面不超过 15、核验至少 2 个不同来源。

## exact inputs SHA-256

| exact input | SHA-256 |
|---|---|
| `pilot-inputs.zip!/pilot-inputs/U01.md` | `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c` |
| `pilot-inputs.zip!/pilot-inputs/U02.md` | `27a0ef436b8d6e57ca9e6cb0cf4b43babe76f6852857edad0c2b6ae30bcf9e04` |
| `pilot-inputs.zip!/pilot-inputs/U03.md` | `0f4af98ac9beb82cea8d4ad708191bf28aa7758645249e0640d6c1d9d5c4f88a` |
| `pilot-inputs.zip!/pilot-inputs/input-manifest.md` | `f875a2c09159313e350da7f0146607a5c6bb5803506887da3350debc033fe1a7` |
| `readerlab-abc-end-to-end-pilot-v1.zip!/readerlab-abc-end-to-end-pilot-v1/02_DIRECT_ROUTE_TASK.md` | `fffe54582635b6c2b9430b8b01b27b517cfc74b0fa2f5bed968840629e4d2fce` |
| `readerlab-abc-end-to-end-pilot-v1.zip!/readerlab-abc-end-to-end-pilot-v1/05_PRODUCT_RULES.md` | `6e233f2185e69c92a92e6b2d3fa1f004420626170577d47b0eac845056b3db22` |
| `readerlab-abc-end-to-end-pilot-v1.zip!/readerlab-abc-end-to-end-pilot-v1/06_OUTPUT_FORMAT.md` | `b6844a8d04429a580356a50ff1a01638fdfff3aff30b45108538d5ea55fa47f5` |

## 隔离与重跑声明

- 未读取 ReaderLab 仓库。
- 未读取、查看或评价 ABC 路线。
- 未读取历史答案、历史结果或其他任务材料。
- 除 exact inputs 外，未读取两个 ZIP 的任何其他条目。
- 运行环境要求读取了全局 `research` Skill 的流程说明；该文件不含 ReaderLab、ABC 路线、历史答案或实验内容。因其后台代理要求与本实验 D 直接路线冲突，未启用后台代理。
- 未使用 Chrome、Browser、仓库工具或其他搜索通道。
- 提示词修改：否。
- 补跑：否。
