# ReaderLab 金标与反例

## 这份文件负责什么

这里不是证据账本，也不是旧项目索引。它只回答三个问题：

1. 新项目应当努力接近哪些固定实物；
2. 哪些固定实物已经被产品负责人否决，必须能够拦住；
3. 哪些材料可以参考，但不能当作通过标准。

每个重要案例都已经整理成当前目录内可以直接阅读的 Markdown 文件。新项目不需要访问旧 ReaderLab、旧会话、旧 Prompt、旧 run 或任何绝对路径。

本清单对**目前已有索引、且能确认产品负责人直接判词的范围**是完整的：图书线共 13 个判词组，带入 12 个；唯一未带入的是产品负责人明确要求“不保留”的土星五号案例。它不能证明历史上从未出现过其他未登记判词；那部分必须保持 `unknown`，不能用本清单冒充“历史绝对全集”。

## 正向金标

### 图书线

- [文明生命周期讲堂体](examples/book/positive/civilization-lifecycle.md)：把人物、书和概念组织成一条解释线，改变读者对原文前提的理解。
- [需求池化](examples/book/positive/demand-pooling.md)：用生活例子解释具名概念和机制；基础层够用，可选深读再解释成立条件与失效边界。
- [自动驾驶异常接管](examples/book/positive/automatic-driving-safe-state.md)：紧扣原文承诺，推出原文没有明说但理解承诺所必需的责任边界。

这些案例保护的是“读者实际获得了什么”，不是人物、书目、概念数量、段落顺序或篇幅模板。

### Skills 线

- [gstack/browse 讲解样张](examples/skills/positive/gstack-browse.md)：产品负责人能够明白它怎样运作、为什么这样设计，并确认技术解读教到了。

这只证明这份固定讲解样张。它不证明 Skills 的 E1—E4 已完整实现，也不证明整条 Skills 线通过。

## 必须拦住的反例

### 图书线

- [五条结构完整但没有学习价值的陪读](examples/book/negative/fresh-demo-five-rejected.md)：整体质量一般，没有保留必要。
- [《今日简史》第一章十条失败样张](examples/book/negative/harari-chapter01-rejected.md)：基础理解不等于高手讲解价值。
- [集中式四段延伸](examples/book/negative/phase4-centralized-rejected.md)：离原文太远，像新增阅读材料。
- [就近延伸](examples/book/negative/phase4-nearby-rejected.md)：重点不突出、视角奇怪，像说明文。
- [“创新必须允许失败”三条陪读](examples/book/negative/innovation-failure-rejected.md)：概括、重命名或抽象化原文已经讲清的内容，不能冒充认知增量。
- Lens Core 六条失败样张：[E1](examples/book/negative/lens-core-e1-rejected.md)、[E2](examples/book/negative/lens-core-e2-rejected.md)、[E3](examples/book/negative/lens-core-e3-rejected.md)：不能把解释读者本来就能读懂的内容当作陪读价值。

反例只冻结对应文件的失败，不把某个题材、学科、概念、长度或写法永久列入黑名单。

## 可以参考，但不能作为通过标准

- [事前验尸](examples/book/reference/premortem-non-gold.md)：产品负责人要求保留，但不进入金标；其中一处事实类比也不能直接发布。
- [R01—R08](examples/book/reference/r01-r08-borderline.md)：0 条好、7 条边缘、1 条不好；文件只保留这八条，不混入未经产品负责人逐条判断的 R09—R22。
- [Book Kernel H3](examples/book/reference/book-kernel-h3-borderline.md)：介于有用和没用之间。
- [gstack/spec](examples/skills/reference/gstack-spec-borderline.md)：能讲明运作和设计，但材料太浅、收益有限，也没有完整 E1—E4。

## 明确不带入新项目

- 土星五号／隐性知识：产品负责人选择“不保留”，因此没有迁移它的内容文件。
- R09—R22：没有逐条产品判词，不进入金标。
- 四份机器事实核验材料：只属于旧工程诊断，不进入新项目产品资产。
- 五份旧 Skills V2：没有直接产品负责人判词，不进入金标。
- 冷读分数、controller 结论、机器 pass、旧路径和哈希账本：都不能代替产品判词，也不能成为新项目运行依赖。

## 新项目怎样使用

- 生产端不得读取本目录的判词、分类和反例答案。
- 裁判与回归系统可以按固定文件读取正例和反例，但必须做绝对判断，不能只比较“更像哪一个”。
- 正例只证明固定范围，不能外推整条流水线。
- 反例必须能够被拦住；未知材料仍需要单独验证。
- `audit/manifest.json` 只用于验证当前包内部文件没有被悄悄改动，不属于产品阅读材料，也不包含旧项目路径。
