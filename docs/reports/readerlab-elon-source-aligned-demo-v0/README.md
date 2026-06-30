# ReaderLab Elon Reader-Facing Demo v0

## 范围

本目录是《埃隆之书》书籍侧 **reader-facing 原型样张 v0**，用于补足 7 个闭环中的：

```text
2. 样本质量闭环：书籍局部样本 + Skill/工程局部样本
```

本轮只做书籍侧第二部分样张。source alignment 已保留在 `audit/`；reader 页曾按“材料方位图 + 大单元陪读”返工，但人工复核和无上下文审查均判定 reader experience FAIL。它不是 product ready，不证明半自动生成器能力，不写 LifeAtlas 正式区。

## 来源边界

- 原始来源：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- 复用索引：`docs/reports/readerlab-elon-full-product-v0/contracts/location-map.v1.json`
- 复用全书地图候选：`docs/reports/readerlab-elon-full-product-v0/contracts/grounded-global-map.v1.json`
- 复用第二部分 deepread 候选：`docs/reports/readerlab-elon-full-product-v0/contracts/local-deepread.v1.json`
- 本轮新做：将旧 contract 里的位置 refs 和本地 EPUB 短摘录，对齐成可人工审查的 reader-facing 样张，并在返工后把审计语言移回 `audit/`。

引用原则：只使用短 excerpt 和 source refs，不复制大段原文。高层判断必须回链到 EPUB spine / location id / heading path。

## 文件清单

- `reader/00_全书地图.md`：失败样张，曾尝试说明这本书讲什么、怎样组织、第二部分在哪里，但仍偏 AI 框架讲解。
- `reader/01_大单元深读.md`：失败样张，包含正文选读导读、AI 旁批、误读提醒和可批注问题；问题是缺少真正一手正文轨。
- `audit/source-alignment.md`：source refs、EPUB spine、短摘录、主张支撑关系。
- `audit/eval.md`：source alignment、reader experience、product capability 三层评估。

## 当前状态

- source alignment：PASS，证据保留在 `audit/source-alignment.md`。
- reader experience：FAIL。缺少原样正文的一手轨，AI 解释替代了阅读入口。
- product capability：NOT ESTABLISHED，本目录仍只是手工原型样张。
- covered unit：第二部分“极限硬核工作”，标题边界从 `spine-015 / v101-13.xhtml` 开始；实质 source cards 覆盖 `spine-016` 至 `spine-020`，即 `v101-14.xhtml` 至 `v101-18.xhtml`。

## 不声称

- 不声称已经完成整本书产品包。
- 不声称当前样张已经人工验收通过。
- 不声称当前 reader-facing 原型通过。
- 不声称 ReaderLab 生成器能力成立。
- 不声称当前样张可以进入 LifeAtlas `300/600/800` 正式沉淀区。
