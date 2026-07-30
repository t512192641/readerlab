status: executed
model: gpt-5.6-terra
reasoning_effort: high
started_at: 2026-07-30T06:42:13Z
finished_at: 2026-07-30T06:42:57Z
input_files:
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E1-thin.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E1-assembled.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E2-thin.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E2-assembled.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E3-thin.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/05-raw-activations/E3-assembled.md
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/03-expert-packs/source-verification.md
output_files:
  - /Users/tianqiang/GitHub/t512192641/readerlab-v0.5-assembled-experts/v3/experiments/discovery-v0.5-assembled-experts/06-identity-audit.md
agent_context: independent
retry: no-retry

# ReaderLab v0.5 独立身份审核

## 判定口径

本审核只判定候选资产的身份、归属和机制来源；不判定其与任何章节的匹配度、质量、排序或结果。`IDENTITY_PASS` 表示候选所指向的是可独立查证的真实资产，候选没有把它临时拼接成新资产，也不是仅以研究领域充当资产。它不意味着候选中假设性的“独立应用案例”已经构成实证案例。

《被发明的传统》在 E1-thin 与 E3-thin 的重复是同一资产在两组原始激活中的重复出现；这不是身份失败，也不在本审核中合并或去重。重复关系留给后续聚类处理。

## E1-thin-01

- **ID / 原始组别**：`E1-thin-01` / E1-thin。
- **身份判定**：`IDENTITY_PASS`。
- **资产是否真实存在**：是。所指为 1983 年由 Eric Hobsbawm 与 Terence Ranger 编辑、Cambridge University Press 出版的论文集 *The Invention of Tradition*。
- **来源和归属是否准确**：基本准确。两人是该书编辑；候选所用定义和三项功能应更精确地归到 Hobsbawm 的导论 “Introduction: Inventing Traditions”，而非把导论表述为两位编辑共同作者。这是书内署名粒度的修正，不足以构成归属不明。
- **核心机制是否来自该资产**：是。以重复的仪式／象征实践灌输规范，并藉连续于过去的主张建立效力，是 Hobsbawm 的定义性机制；凝聚群体、赋予制度／权威正当性、社会化信念与价值是其列举的主要功能类型。
- **是否是临时综合**：否。候选没有混入另一理论的必要机制；“重复—连续性—规范／功能”的链条可归回同一导论。
- **是否只是研究领域**：否。它是可署名、可定位的具体历史学概念与文本，而非泛称“民族主义研究”或“传统研究”。
- **是否能脱离当前章节独立成立**：能。该定义可用来分析国家仪式、纪念实践或教育典礼，不依赖本次材料。
- **是否保留原始结构**：是。候选保留定义的重复、仪式／象征性、规范灌输与对过去连续性的要件，并将三项功能作为功能分类，没有简化成“传统全是伪造”。
- **独立案例是否真实支持机制**：候选给出的“研究一项近代国家设立的纪念仪式”是检验步骤，未指认可核验的真实个案，因而不能单独作为实证支持；不影响资产身份。该书自身具体讨论威尔士和苏格兰民族文化、英国王室仪式、英属印度与非洲帝国仪式，足以证明该资产有非当前材料的真实案例范围。
- **证据 URL / 书目信息**：Eric Hobsbawm and Terence Ranger, eds., *The Invention of Tradition* (Cambridge University Press, 1983), [Cambridge 书目页](https://www.cambridge.org/core/books/invention-of-tradition/B9973971357795DC86BE856F321C34B3)；[WorldCat 1983 版记录](https://search.worldcat.org/title/invention-of-tradition/oclc/466055038)。
- **保留理由**：名称、来源、编辑归属与核心机制均可独立追溯；唯一需保留的精确性注记是导论作者应写作 Hobsbawm。

## E3-thin-01

- **ID / 原始组别**：`E3-thin-01` / E3-thin。
- **身份判定**：`IDENTITY_PASS`。
- **资产是否真实存在**：是。与 `E1-thin-01` 指向同一真实资产，而不是一个名称相同的新候选。
- **来源和归属是否准确**：基本准确。书由 Hobsbawm 与 Ranger 编辑；候选使用的定义性表述精确归属应为 Hobsbawm 单独署名的导论。候选没有把 Ranger 错列为概念的单独提出者，但“编……导论”的写法应在正式引文中明确这一点。
- **核心机制是否来自该资产**：是。重复的仪式性／象征性实践、价值规范的灌输、以及宣称与过去连续而在新情境中形成或固定的关系，来自该资产的定义结构。
- **是否是临时综合**：否。候选是对同一概念的较短表述；没有把现代民族国家、宗教或其他理论伪装为概念的组成部分。
- **是否只是研究领域**：否。它不是“历史传统研究”的宽泛标签，而是有明确文本出处的可检验概念。
- **是否能脱离当前章节独立成立**：能。它可独立用于考察非宗教的纪念、教育和国家典礼。
- **是否保留原始结构**：是。保留了定义的必要结构；没有保留 E1 候选额外列出的三项功能，但这不破坏该候选所使用的定义性结构。
- **独立案例是否真实支持机制**：候选的“考察一项新设国家纪念日”仍是一个分析设问，不是已提供书目信息的真实个案，故不能作为独立实证支持。该资产本身的书中案例范围见 Cambridge 书目说明，可证明它不是依赖当前材料的临时解释。
- **证据 URL / 书目信息**：Eric Hobsbawm and Terence Ranger, eds., *The Invention of Tradition* (Cambridge University Press, 1983), [Cambridge 书目页](https://www.cambridge.org/core/books/invention-of-tradition/B9973971357795DC86BE856F321C34B3)；[AfricaMuseum 馆藏记录（明确列编辑）](https://library.africamuseum.be/cgi-bin/koha/opac-detail.pl?biblionumber=291015)。
- **保留理由**：与 E1-thin-01 的重复不改变其可验证身份；编辑与导论作者的粒度需要在引用时清楚区分。

## E3-06

- **ID / 原始组别**：`E3-06` / E3-assembled。
- **身份判定**：`IDENTITY_PASS`。
- **资产是否真实存在**：是。所指为 Raymond Williams 的 *Marxism and Literature*（Oxford University Press, 1977）中的 “Dominant, Residual, and Emergent”。
- **来源和归属是否准确**：准确。Williams 是该书作者；该章题名、三分法与 1977 年 Oxford University Press 版本均可由书目记录核对。
- **核心机制是否来自该资产**：是。主导文化的有效／霸权性位置，过去形成但仍在当下活动的残余，以及新意义、价值与实践的涌现，并伴随选择性吸纳、排斥或压制的关系，属于 Williams 的文化唯物主义论述。候选没有把三者误写成纯年代标签。
- **是否是临时综合**：否。候选虽连及霸权、制度和 formations，但它们都在同一著作相邻的理论论述中；没有拼接外部文化理论。
- **是否只是研究领域**：否。它是 Williams 的具体概念结构，不是“文化研究”这一领域名称。
- **是否能脱离当前章节独立成立**：能。三分法可在有具体制度、实践与权力关系证据的文化史材料中独立使用。
- **是否保留原始结构**：是。候选保留主导／残余／新兴的关系性区分、实际文化效力以及选择性吸纳／边缘化／压制；没有把它降格为旧／中／新的线性排序。
- **独立案例是否真实支持机制**：候选的“研究二十世纪英国公共广播”是可执行的研究设计，未提供可核验的具体广播史证据，故本身不是已证实的独立案例；这不推翻资产身份。Williams 的三分法在非当前材料的文学与文化研究中被可追溯地明确作为分析框架使用。
- **证据 URL / 书目信息**：Raymond Williams, *Marxism and Literature* (Oxford University Press, 1977), [Open Library 书目与目录](https://openlibrary.org/books/OL23242368M/Marxism_and_literature)；[WorldCat 1977 版记录](https://search.worldcat.org/title/Marxism-and-literature/oclc/300371219)；[Stanford University Press 对该章和 residuality 的引用](https://www.sup.org/books/literary-studies-and-literature/remainders/excerpt/introduction)。
- **保留理由**：资产、作者、著作和章节均可独立核验，候选机制与原有结构一致。独立应用例需要另有史料时才可升级为实证案例，但这不是身份淘汰条件。

## 无候选记录

- **E1-assembled**：无候选，不进入身份判定。
- **E2-thin**：无候选，不进入身份判定。
- **E2-assembled**：无候选，不进入身份判定。

允许输入的六份 raw activation 中实际只有以上三组无候选记录；其余三组分别产生了上列候选。不存在可据实填写的第四组“无候选”记录，故不虚构第四项。
