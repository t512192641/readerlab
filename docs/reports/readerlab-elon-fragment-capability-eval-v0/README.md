# ReaderLab Elon Fragment Capability Eval v0

## 结论

这是《埃隆之书》片段级能力评测手工样张。它的目标不是继续写全书总纲，而是用 8 个高价值片段测试两件事：

1. ReaderLab 能否把一个片段转成可读、可批注、可迁移、可审查的能力卡。
2. 用户关心的 7 个候选维度本身是否真有评测价值，而不是只是字段堆叠。

当前状态：repo 内手工片段评测样张，不是 product ready，不是 ReaderLab 生成器能力证明，不是正式 Skill，不是 fresh source-grounded contract。

## 文件

- `reader/01_片段能力评测.md`：8 个片段能力卡。
- `audit/90_维度价值审计.md`：评估 7 个维度的价值、臃肿风险和合并建议。
- `assertions.md`：本轮片段评测自检，以及 ELON-A01 到 ELON-A13 的范围化状态。

## 输入证据

- EPUB：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- v1 手工试产包：`docs/reports/readerlab-elon-full-product-v1/`
- 方法 bakeoff：`docs/reports/readerlab-elon-method-bakeoff-v0/`
- v0 location map：`docs/reports/readerlab-elon-full-product-v0/contracts/location-map.v1.json`
- Meta Skill 方法：
  - `/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/references/output-eval-method.md`
  - `/Users/tianqiang/技能项目/skills-canonical/packages/yao-meta-skill/references/skill-ir-method.md`

## 来源口径

每个片段都给出 `location_id`、heading 和 EPUB 内 xhtml path。来源锚点继承 v0 `location-map.v1.json` 和 v1 `candidate-evidence.v1.json`，只到 heading/block/cleaned-char 级精度。

本目录没有重新解析 EPUB，没有生成新的 source registry / location map，没有进行 fresh source-grounded contract 验证。后续如果要升格为正式评测集，必须抽查原文上下文并把这些片段写成可验证 contract。

## 片段选择

| 片段 | 阅读难点 | 选它的原因 |
|---|---|---|
| 本书说明 | 材料边界 | 防止把选编材料当最终事实证据。 |
| 创造价值 | 目标判断 | 防止把目标读成鸡血或自我神话。 |
| 第一性原理 | 概念滥用 | 防止把第一性原理读成反经验口号。 |
| 睡在工厂车间 | 高风险误迁移 | 防止把危机强度读成常态加班制度。 |
| 破除组织壁垒 | 组织机制 | 防止把直接沟通读成越权和混乱。 |
| 算法之道 | 可执行流程 | 检查是否能从原则落到删除、简化、自动化顺序。 |
| 工厂即产品 | 交付系统 | 检查读者能否把制造思维迁移到稳定交付。 |
| AI / 多行星风险 | 宏大叙事 | 防止长期主义把当下代价和证据审查免检。 |

## 核心判断

高价值维度是：`原文问题`、`阅读动作`、`正例/反例`、`审查标准`。它们直接决定片段有没有读者收益、能不能防误读、能不能被评审。

容易臃肿的维度是：`术语/机制` 和 `迁移题`。有机制的片段必须写；没有机制时强写术语会变成标签。能安全迁移的片段才写迁移题；材料边界和文明风险类片段更适合写核验题或边界题。

## v0.1 修订口径

对抗审查后，本样张不再把“每张卡 7 个字段齐全”当作通过标准。正式判断改为：

- 必填核心：片段问题、阅读动作、正反样例、审查标准。
- 条件触发：机制/边界、迁移题/核验题。
- 高风险片段必须标出来源状态和额外复核要求。
