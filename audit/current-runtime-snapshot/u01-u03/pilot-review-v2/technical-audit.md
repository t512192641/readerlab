# ReaderLab ABC 最小端到端成品技术审核

## 审核结论

- 实验状态：`EXPERIMENT_VALID_WITH_LIMITATIONS`
- 未触发：`EXPERIMENT_INVALID`
- 技术资格汇总：6 条 `TECH_PASS`；0 条 `TECH_BORDERLINE`；0 条 `TECH_REJECT`
- 审核边界：只标记，不改写成品；技术资格不替代产品判断。

主要限制是：两次运行的思考强度都申报为 `unknown`，且没有原始模型调用日志可独立核验模型参数、隔离声明、提示词修改和补跑声明。现有冻结清单之间没有发现严重不公平或交叉污染的正面证据，因此保留实验有效性，但不得把“未发现”理解为日志级证明。

## 运行公平性核验

| 核验项 | D 直接路线 | ABC 路线 | 判定 |
|---|---|---|---|
| 模型 | `GPT-5（Codex）` | `GPT-5（Codex；本会话可见标识）` | PASS（同一名义模型）；缺少原始调用日志 |
| 思考强度 | `unknown` | `unknown` | UNCERTAIN；无法证明实际强度相同 |
| 搜索工具 | 内置 Web 搜索与网页打开 | 内置 Web `search_query` 与 `open` | PASS（同类工具）；由运行清单声明 |
| 搜索预算 | 每 U 查询不超过 10、打开不超过 15、至少 2 个来源 | 每 U 查询不超过 10、打开不超过 15、至少 2 个来源 | PASS；预算一致，实际调用量不同但均在预算内 |
| 实际查询／打开／来源 | 5／9／7 | 18／18／15 | 记录项；不等于预算不一致 |
| 冻结输入 hashes | 4 个共同输入 hash 全部一致 | 4 个共同输入 hash 全部一致 | PASS |
| 跨路线污染 | 声明未读取另一条路线 | 声明未读取另一条路线 | PASS（清单一致）；缺少环境审计日志 |
| 历史答案／材料 | 声明未读取 | 声明未读取 | PASS（清单一致）；缺少环境审计日志 |
| 提示词修改 | 否 | 否 | PASS（清单一致）；缺少原始调用日志 |
| 补跑 | 否 | 否 | PASS（清单一致）；缺少原始调用日志 |

共同冻结输入 SHA-256 已独立重算：

| exact input | SHA-256 |
|---|---|
| `pilot-inputs.zip!/pilot-inputs/U01.md` | `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c` |
| `pilot-inputs.zip!/pilot-inputs/U02.md` | `27a0ef436b8d6e57ca9e6cb0cf4b43babe76f6852857edad0c2b6ae30bcf9e04` |
| `pilot-inputs.zip!/pilot-inputs/U03.md` | `0f4af98ac9beb82cea8d4ad708191bf28aa7758645249e0640d6c1d9d5c4f88a` |
| `pilot-inputs.zip!/pilot-inputs/input-manifest.md` | `f875a2c09159313e350da7f0146607a5c6bb5803506887da3350debc033fe1a7` |

## 六条成品 H1—H10 审核

### D-U01

| 标准 | 标记 | 技术说明 |
|---|---|---|
| H1 来源真实 | PASS | Young 2006 原始论文真实存在，Cambridge 页面给出 DOI、作者、摘要及模型五项特征；Zheng 2018 论文真实存在。 |
| H2 表达准确 | PASS | 对“社会连接责任模型”的结构性过程、共享、面向未来及通过集体行动履责的概括与原文一致；没有把它写成同等归罪。 |
| H3 连接自然 | PASS | 从“偷走河流”与小股东责任直接连接到结构性不正义中的责任形式，桥梁已写明。 |
| H4 外部知识承重 | PASS | 删除 C 后，“向后归责／面向未来的共享政治责任”的主要增量消失。 |
| H5 非同域专业扩展 | PASS | 虽属政治哲学，但提供责任类型的稳定重构，不只是增加原文伦理细节。 |
| H6 认知回报合格 | PASS | 前置知识低，换回可迁移的责任区分与集体修复视角。 |
| H7 无表面跨域 | PASS | 连接依靠结构性过程、参与关系和责任方向，不依赖宽泛词相似。 |
| H8 无原创伪装 | PASS | 没有把现场新编步骤冒充 Young 的正式框架。 |
| H9 人类可读 | PASS | 概念、例子、边界完整，非专业读者可判断价值。 |
| H10 篇幅与位置合理 | PASS | 正文约 540 字，符合 500—900 字建议，未写成学术备忘录。 |

技术资格：`TECH_PASS`。

### D-U02

| 标准 | 标记 | 技术说明 |
|---|---|---|
| H1 来源真实 | PASS | Nissenbaum 2004 原始论文与后续形式化论文真实存在，来源可追溯。 |
| H2 表达准确 | PASS | “情境完整性”确以特定情境的信息流规范为核心；角色、信息类型与传递原则的描述准确。 |
| H3 连接自然 | PASS | 直接说明为何数据的土地式所有权隐喻不足，并把问题转为不同情境中的信息流权限。 |
| H4 外部知识承重 | PASS | 删除 C 后，关于信息流合宜性及其参数的主要观察消失。 |
| H5 非同域专业扩展 | PASS | 它不是隐私法细节堆叠，而是把“占有”重构为可迁移的信息流判断。 |
| H6 认知回报合格 | PASS | 理解成本低，能明显改变数据治理的提问方式。 |
| H7 无表面跨域 | PASS | 具体承重关系是情境、角色、信息类型与传递原则。 |
| H8 无原创伪装 | PASS | 未编造操作法；也明确既有惯例仍需规范审查。 |
| H9 人类可读 | PASS | 医疗、招聘、朋友与平台例子足以让非专业读者判断。 |
| H10 篇幅与位置合理 | PASS | 正文约 577 字，符合建议区间。 |

技术资格：`TECH_PASS`。

### D-U03

| 标准 | 标记 | 技术说明 |
|---|---|---|
| H1 来源真实 | PASS | Bellah 1967 原始论文、学术机构转载与 University of Chicago Press 图书页均真实存在。 |
| H2 表达准确 | PASS | 对美国公民宗教的公共神圣语言、仪式、建国叙事及“国家受更高原则约束”的边界概括准确。 |
| H3 连接自然 | PASS | 从“国家借传统宗教”推进到“现代国家自身生产神圣秩序”，方向反转已清楚说明。 |
| H4 外部知识承重 | PASS | 删除 C 后，国家文献、纪念与仪式形成独立神圣体系的观察消失。 |
| H5 非同域专业扩展 | PASS | 不是宗教史细节补充，而是提供现代政治共同体如何神圣化自身的新问题。 |
| H6 认知回报合格 | PASS | 概念容易理解，换回跨国家仪式与政治正当性的可迁移观察。 |
| H7 无表面跨域 | PASS | 由神圣时间、文本、牺牲记忆和超越性约束等具体结构承重。 |
| H8 无原创伪装 | PASS | 未把新编框架冒充 Bellah；跨国适用争议也被标明。 |
| H9 人类可读 | PASS | 就职、纪念、建国文献等例子具体。 |
| H10 篇幅与位置合理 | PASS | 正文约 537 字，符合建议区间。 |

技术资格：`TECH_PASS`。

### ABC-U01

| 标准 | 标记 | 技术说明 |
|---|---|---|
| H1 来源真实 | PASS | Thompson 的原始论文、Cambridge 书章、患者安全论文及 Hormio 2024 著作均真实存在。 |
| H2 表达准确 | PASS | 对多手问题、因果与意志标准、系统中责任缺口的描述与原始及扩展文献一致；Hormio 的个人—集体双层责任也未被歪曲。 |
| H3 连接自然 | PASS | 从长因果链推进到信息、控制与责任被角色分散，连接无需读者补桥。 |
| H4 外部知识承重 | PASS | 删除 C 后，“多手造成责任落点消失”及其判断维度的主要增量消失。 |
| H5 非同域专业扩展 | PASS | 不是伦理学术语加码，而是把复杂性拆为因果、选择、控制和角色结构。 |
| H6 认知回报合格 | PASS | 前置知识低，提供清晰的问题重构。 |
| H7 无表面跨域 | PASS | 具体机制是多主体贡献、分散控制、累积决定与责任缺口。 |
| H8 无原创伪装 | PASS | 没有将问题清单包装成 Thompson 的正式步骤，也未声称责任相同。 |
| H9 人类可读 | PASS | 概念、组织例子和边界均完整。 |
| H10 篇幅与位置合理 | PASS | 正文约 574 字，符合建议区间。 |

技术资格：`TECH_PASS`。

### ABC-U02

| 标准 | 标记 | 技术说明 |
|---|---|---|
| H1 来源真实 | PASS | Kerber 的 IoT 数据权利束论文、Cofone 论文与 ODI 数据托管材料真实存在。 |
| H2 表达准确 | PASS | 权利可拆分配置、技术架构形成事实控制、同意模式的信息与议价不对称及推断数据缺口均有来源支持。 |
| H3 连接自然 | PASS | 原文已提出数据难以按土地方式拥有，成品顺势把“谁拥有”拆成具体权能。 |
| H4 外部知识承重 | PASS | 删除 C 后，法律产权与事实控制的区分及权能拆分的增量消失。 |
| H5 非同域专业扩展 | PASS | 不是财产法细节堆叠，而是把单选所有权转成可迁移的权能配置问题。 |
| H6 认知回报合格 | PASS | 概念成本适中，明显改善问题定义。 |
| H7 无表面跨域 | PASS | 由访问、使用、排除、分享、收益与技术控制等具体关系承重。 |
| H8 无原创伪装 | PASS | 未把逐项追问冒充原作者正式方法，并明确权利束不会自动给出公平答案。 |
| H9 人类可读 | PASS | 先解释权利束，再说明数据上的事实控制，层次清楚。 |
| H10 篇幅与位置合理 | PASS | 正文约 638 字，符合建议区间。 |

技术资格：`TECH_PASS`。

### ABC-U03

| 标准 | 标记 | 技术说明 |
|---|---|---|
| H1 来源真实 | PASS | Swann 与 Buhrmester 的身份融合综述、跨八人群实验和集体仪式纵向研究均真实存在。 |
| H2 表达准确 | PASS | 个人自我不被吞没、个人与社会自我协同、家人般关系与高代价群体行动的概括准确；跨文化实验的小效应、文化差异和量表可能测到一般亲社会性的限制也准确。 |
| H3 连接自然 | PASS | 直接回应传统仪式、现代国家与高代价牺牲的并置，并将“失去自我”改写为“主动自我与群体协同”的可能机制。 |
| H4 外部知识承重 | PASS | 删除 C 后，忠诚并不必然抹掉个人自我的关键区分消失。 |
| H5 非同域专业扩展 | PASS | 社会心理机制为历史叙述带来跨域增量，不是宗教史细节。 |
| H6 认知回报合格 | PASS | 理解成本适中，换回明显的机制与反直觉区分。 |
| H7 无表面跨域 | PASS | 由身份协同、关系纽带、共享本质感与高唤醒等具体机制承重。 |
| H8 无原创伪装 | PASS | 未把身份融合写成历史事件的单因解释，明确证据不能直接证明特定宗教或国家必然制造牺牲。 |
| H9 人类可读 | PASS | 先定义、再连接、后给证据边界，非专业读者可判断。 |
| H10 篇幅与位置合理 | PASS | 正文约 615 字，符合建议区间。 |

技术资格：`TECH_PASS`。

## 独立外部核验记录

本会话只使用内置 Web `search_query` 与 `open`。优先核验以下原始、大学、出版社或正式论文页面：

- Iris Marion Young 原始论文（Cambridge）：https://www.cambridge.org/core/journals/social-philosophy-and-policy/article/abs/responsibility-and-global-justice-a-social-connection-model/9308EE478561C7CE31E1F5A8F26CBE04
- Helen Nissenbaum 原始论文（Washington Law Review）：https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/
- Robert N. Bellah 原始论文（MIT Press）：https://direct.mit.edu/daed/article/134/4/40/27373/Civil-religion-in-America
- Dennis F. Thompson 原始论文（Cambridge）：https://www.cambridge.org/core/journals/american-political-science-review/article/abs/moral-responsibility-of-public-officials-the-problem-of-many-hands/39DD3FAB7BF7DC7A242407143674F22B
- Martina Eckardt、Wolfgang Kerber 正式论文（Springer）：https://link.springer.com/article/10.1007/s10657-023-09791-8
- Ignacio Cofone 正式论文（Cardozo Law Review）：https://larc.cardozo.yu.edu/clr/vol43/iss2/4/
- Swann、Buhrmester 正式综述（SAGE）：https://journals.sagepub.com/doi/10.1177/0963721414551363
- Purzycki、Lang 跨文化实验（Max Planck 托管正式论文 PDF）：https://www.eva.mpg.de/fileadmin/content_files/ecology/pdfs/Purzycki_2019_IdentityFusion.pdf
- Zabala 等集体仪式纵向研究（Wiley）：https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjso.12723
- Säde Hormio 著作（Springer）：https://link.springer.com/book/10.1007/978-3-031-51753-2

## 冻结路线输出 SHA-256

| 文件 | SHA-256 |
|---|---|
| `direct-output/U01.md` | `ac10e0b99047d6fab303843f3d8542d29879fcdb9c57c789216d0cc34fed586a` |
| `direct-output/U02.md` | `4c12fd91d69d3adccc1f49cfaac5c3377c5f1882f00be9cc7ca471c089689ede` |
| `direct-output/U03.md` | `008521827e0df0f61753fbb69b8f32b286d9724b5b59d40dc64699c98cdbf00c` |
| `direct-output/candidate-ledger.md` | `f4d1337822aa1b85a59ae4a3a578384775af07a4e129b3b652cd1e8458705f56` |
| `direct-output/runner-manifest.md` | `e7f38cdc625b6920b9381f52fe6bee74f776f86a2ad434c5c01e394d534113dc` |
| `abc-output/U01.md` | `598138b65d2479125ce6ee3dd3cf9981aa9d790740aa024f02ee6774e8510eb7` |
| `abc-output/U02.md` | `baeb9e01f3878df08869b5045da77b679d14742ada944e51d49ef07d0293a9b4` |
| `abc-output/U03.md` | `8bfb904826c2addbe827046e62ffa7723f42372090d614640f860e39724a25f7` |
| `abc-output/bridge-and-candidate-ledger.md` | `e53bb3704f71e760dc649134b1495e2b190dfcbb44c5c3faf6198aef020cf79e` |
| `abc-output/runner-manifest.md` | `cd1dd3219282880bcb9b955464ce115349a37c218c25961f2150496785a6a5d8` |

## v2 呈现修复记录

- 修复原因：v1 `blind-review.md` 的“完整原文上下文”直接嵌入冻结 XHTML，HTML 标签与属性噪声妨碍产品负责人阅读。
- 允许变化：仅将三个冻结 XHTML 原文区机械渲染为可读 Markdown；标题改为 Markdown 标题，段落分行留空，HTML entity 解码，纯标签和展示属性移除，数字脚注引用统一为 `[n]`。
- 禁止变化：未摘要、改写、删句或改变可见文字顺序；未重新搜索、重新审核或重新随机；三组顺序、左右成品、产品判断表和路线密钥均保持不变。
- 确定性验证：U01、U02、U03 的原 XHTML 可见文本序列与 v2 原文区在忽略 Markdown 标记、HTML 标签、脚注括号样式及空白差异后全部一致；每组左右成品区逐字一致；匿名泄漏扫描通过；`route-key.md` SHA-256 与 v1 完全一致。
- 技术结论：v1 的实验有效性判定及 6 条技术资格均未改变。
