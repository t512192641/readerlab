# ReaderLab Fullbook Demo v0

## 目标

这个 demo 用《埃隆之书》证明 ReaderLab 可以产出“全书级地图 + 总收获/亮点 + 跨章节主题关系”，而不只做单章节局部深读。

它仍是仓库内开发侧 demo：

- 不写入 LifeAtlas。
- 不修改正式生成器 `scripts/readerlab.py`。
- 不新增依赖。
- 不代表人工阅读验收通过。
- 不输出精选译文正文或完整原文。

## 文件

- `elon/source-registry.v1.json`：登记 EPUB、OPF、TOC 和抽取口径。
- `elon/location-map.v1.json`：登记完整 36 个 EPUB spine item。
- `elon/grounded-global-map.v1.json`：全书级阅读地图、跨章节主题、总收获、亮点和可迁移原则。
- `elon/fullbook-reader-demo.md`：读者可读中文全书导读。
- `elon/assertions.md`：本 demo 的断言状态。

## 覆盖口径

本 demo 的 `coverage_status=full` 只表示：已登记 EPUB OPF spine 中的 36 个 xhtml spine item，并为全书地图中的主张提供 spine 级 refs。

它不表示：

- 已生成逐章精选译文。
- 已完成逐段 char-level 精确引用。
- 已写入 LifeAtlas 正式阅读包。
- 已通过人工阅读质量验收。

## 验收命令

```bash
python3 scripts/readerlab_fullbook_demo_validate.py docs/reports/readerlab-fullbook-demo-v0
python3 tests/test_fullbook_demo_validate.py
python3 tests/test_readerlab.py
```

## 仍缺什么

- 还没有精选译文正文。
- 还不是 LifeAtlas 正式写入。
- 还没有人工 blind review。
- refs 当前是 spine / chapter 级，后续如果进入正式阅读包，需要收窄到章节内 block 或 char range。
