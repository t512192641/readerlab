# 会话 2：D 路线——直接生成近终稿陪读

## 输入

你只能读取：

- `pilot-inputs/U01.md`
- `pilot-inputs/U02.md`
- `pilot-inputs/U03.md`
- 本任务文件
- `05_PRODUCT_RULES.md`
- `06_OUTPUT_FORMAT.md`

不得读取 ReaderLab 仓库其他文件、历史结果、ABC 路线结果或答案说明。

## 目标

对每个完整主题单元，直接从原文出发，搜索真实存在、可追溯、有认知增量的外部对象 C，并写出最多 1 条近终稿陪读。

允许沉默。

## 每个单元的固定步骤

1. 阅读完整原文。不要摘要替代原文。
2. 直接搜索真实外部认知对象 C。
3. 最多保留 4 个内部候选。
4. 按 `05_PRODUCT_RULES.md` 淘汰反例。
5. 只选择最好的 1 个；没有合格候选则输出 `SILENCE`。
6. 恢复 C 原本真实拥有的 M1/M2/M3 深度。
7. 严格使用 `06_OUTPUT_FORMAT.md` 写近终稿陪读。

## 搜索预算

每个单元：

- 最多 10 个查询；
- 最多打开 15 个页面；
- 至少核验 2 个不同来源；
- 优先一手、出版社、大学、正式论文或权威学术资料。

## 输出

```text
direct-output/
├── U01.md
├── U02.md
├── U03.md
├── candidate-ledger.md
└── runner-manifest.md
```

`candidate-ledger.md` 记录候选、淘汰原因和最终选择，不进入产品盲审。

完成后停止，不得查看或评价 ABC 路线。
