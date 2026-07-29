# Runner manifest

## 运行身份

- 实际模型：GPT-5（Codex；本会话可见标识）
- 思考强度：unknown
- 唯一搜索工具：本会话内置 Web `search_query` 与 `open`
- 其他搜索、浏览或仓库工具：未使用

## exact inputs 与 SHA-256

| exact input | SHA-256 |
|---|---|
| `pilot-inputs.zip!/pilot-inputs/U01.md` | `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c` |
| `pilot-inputs.zip!/pilot-inputs/U02.md` | `27a0ef436b8d6e57ca9e6cb0cf4b43babe76f6852857edad0c2b6ae30bcf9e04` |
| `pilot-inputs.zip!/pilot-inputs/U03.md` | `0f4af98ac9beb82cea8d4ad708191bf28aa7758645249e0640d6c1d9d5c4f88a` |
| `pilot-inputs.zip!/pilot-inputs/input-manifest.md` | `f875a2c09159313e350da7f0146607a5c6bb5803506887da3350debc033fe1a7` |
| `readerlab-abc-end-to-end-pilot-v1.zip!/readerlab-abc-end-to-end-pilot-v1/03_ABC_ROUTE_TASK.md` | `1fb4b02bd285ed78c3b2b3564ae1e436437e4d780287e83aaf9f06ee737f57a8` |
| `readerlab-abc-end-to-end-pilot-v1.zip!/readerlab-abc-end-to-end-pilot-v1/05_PRODUCT_RULES.md` | `6e233f2185e69c92a92e6b2d3fa1f004420626170577d47b0eac845056b3db22` |
| `readerlab-abc-end-to-end-pilot-v1.zip!/readerlab-abc-end-to-end-pilot-v1/06_OUTPUT_FORMAT.md` | `b6844a8d04429a580356a50ff1a01638fdfff3aff30b45108538d5ea55fa47f5` |

## 逐 U 调用与证据计数

| 单元 | 查询数 | 打开页面数 | 核验来源数 | 前三查询合规 | 至少两个领域表达 |
|---|---:|---:|---:|---|---|
| U01 | 6 | 3 | 3 | 是 | 是：复杂系统／工程事故／供应链 |
| U02 | 6 | 6 | 6 | 是 | 是：非耗竭资源／生物样本／基础设施 |
| U03 | 6 | 9 | 6 | 是 | 是：组织仪式／国家传统／制度解释 |

说明：打开页面数按向 `open` 提交的页面目标计数，包含返回 403、reCAPTCHA 或内部错误的尝试；核验来源数仅计搜索结果或打开页中返回了可辨识书目信息及实质摘要／正文的不同来源。

## 隔离与运行声明

- 未读取 ReaderLab 仓库、仓库上下文、历史材料、历史答案、答案说明或其他 ZIP 条目。
- 未读取、查看或评价 D 直接路线及其任何结果。
- 未使用 Chrome、Browser、仓库工具或其他搜索通道。
- 未发生提示词修改。
- 未发生补跑；本次为单次按冻结任务执行。

## 输出清单

- `U01.md`
- `U02.md`
- `U03.md`
- `bridge-and-candidate-ledger.md`
- `runner-manifest.md`
