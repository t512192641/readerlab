# ReaderLab《埃隆之书》整书实验产品 v0

本目录是一套仓库内 ReaderLab 实验产品，用于主 Agent 和对抗审查 worker 审核。它不是 LifeAtlas 正式沉淀，不覆盖旧 demo 包，不改原 EPUB，也不表示人工阅读验收通过。

## 打开顺序

1. `reader/00_阅读入口.md`：第一次打开从这里开始。
2. `reader/01_全书阅读路线.md`：看正式标题映射和阅读顺序。
3. `reader/02_全书地图.md`：看核心问题、机制链、案例关系和读者新增理解。
4. `reader/03_深读卡组.md`：重点读第二部分的深读卡。
5. `reader/04_案例_反例_术语.md`：查案例、误读防线和术语。
6. `audit/90_来源与审计.md` 与 `contracts/*.json`：给审核者复核来源和状态。

## 边界

- 来源 EPUB：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- 写入范围：仅本目录。
- 未写入 LifeAtlas `300/600/800`。
- 未修改原 EPUB、旧 LifeAtlas demo 包或 `scripts/readerlab.py`。
- 未新增依赖、未联网、未安装或启用 Skill。
- `machine_status` 与 `human_status` 分离；所有人工状态保持 `pending`。

## 产品形态

读者页是可打开阅读的 Markdown；契约 JSON 是可复核的事实层；`assertions.md` 对 ELON-A01 到 ELON-A13 做逐项自检。当前只能称为 full-product experiment v0，不能称为 product ready。
