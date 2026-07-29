# Checkpoint A 材料冻结

## 身份与“未见”边界

三份材料均未出现在本项目当前 Discovery 设计、旧 sidecar 的 A/B/C 开发材料或任何已揭晓样张中；本轮也没有读取 `GOLD-STANDARDS.md`、`examples/`、`archive/` 或旧 ReaderLab 项目。“未见”只指本项目的 Prompt 设计与实验未用过，**不声称模型训练时从未见过这些公版名篇**。材料身份以最终 `source.txt` 字节的 SHA-256 为准。

| ID | 角色 / 领域 | 完整单元边界 | `source.txt` SHA-256 | 字节 |
|---|---|---|---|---:|
| `D-ISO-POS-01-TITANIC` | 正例 / 工程安全与组织决策 | 官方调查报告完整 Section II；从 `II. ACCOUNT...THE DISASTER.` 起，到 Section III 标题前（不含） | `ce8a25860f9fddc56cb235fb8637c0175a767af9f5ec877e5e905f312fd0f9b0` | 33054 |
| `D-ISO-POS-02-FED10` | 正例 / 政治制度 | 完整 Federalist No. X；到 Federalist No. XI 标题前（不含） | `bac96df8b5c83dafb479af7da223a1dfbc6cd22089d91f6093ba1e1852126a64` | 18435 |
| `D-ISO-CTL-01-TITANIC` | 最小对照 / 船舶设备静态描述 | Section I 内完整 `GENERAL.` 小节；到 `CREW AND PASSENGERS.` 前（不含） | `1d9403ee2eb4e3b075e42f61604d990f227b31c13b0e65848746782f11eadaad` | 867 |

## 来源、许可与原始字节

- Titanic 正例与对照来源：Project Gutenberg eBook #39415，1912 年英国政府正式调查报告 *Loss of the Steamship "Titanic"*；下载地址 `https://www.gutenberg.org/cache/epub/39415/pg39415.txt`，书目页 `https://www.gutenberg.org/ebooks/39415`。原始文件 SHA-256：`68755a061177dcca91cc0fa5d7f89790d7562c88706178bf0138dd117ef917ca`。原文件自带说明称扫描材料为 public domain，并附 Project Gutenberg License；在美国可按该许可复制与再利用。
- Federalist 正例来源：Project Gutenberg eBook #18，*The Federalist Papers*；下载地址 `https://www.gutenberg.org/cache/epub/18/pg18.txt`，书目页 `https://www.gutenberg.org/ebooks/18`。原始文件 SHA-256：`a6c9d1135a04d10955fe11d210b7f642e1c2341d4f2c8369b9a832cc97839d94`。原文件自带 Project Gutenberg License；作品为美国公版文本。
- 两个原始文件均按 UTF-8、CRLF 原样保留；提取不改编码、不正规化换行、不翻译。确切边界、字节 offset 与 hash 见 `extraction-manifest.json`；可由 `harness/extract_materials.py` 重放。
- 中国语处理：Scout 读取相同英文原文，以中文形成 seed；锚点只引用冻结单元内的英文原句或段落 ID。禁止预先翻译原文，因为翻译本身会引入额外处理变量。

## 为什么这两份正例能测“新增解释变量”

- Titanic 单元同时包含制度性安全声明、航线惯例、多个冰情信息、速度与能见条件、实际行动和后果，允许发现文本没有命名的外部机制；这里不预先列出答案或框架名。
- Federalist No. X 不因“著名”而入选，而因它对派系、规模、代表与治理给出完整论证，同时仍留下可由外部知识补入的解释变量。那些候选变量只用于材料选择论证，绝不进入 Scout/Normalizer/Judge 的 prompt 或 read-set。

## 为什么对照不会自然召回外部框架

对照只有四段静态设备说明（烟囱用途、排放相对水线、锅炉支撑、蒸汽管连接），与正例共享船舶、锅炉、水线等表面词，却没有预警、判断、行动、冲突、变化或后果链。它允许返回 0 seed；不得因出现海事词汇而强行命名安全框架。它仍可能偶然触发联想，所以它是“最小对照”，不是先验保证的绝对零。

## 同源但不泄漏

Titanic 正例与对照虽来自同一原始文件，但最终字节范围互斥。原始整书只在 provenance/original 区保存，运行时不挂载。每次 Scout 的新建只读工作目录只含一个 `source.txt`、一个变体 prompt 和共同 schema；兄弟单元、原始整书、audit、prior-sidecar 和任何结果都不在 read-set。启动前后对 read-set 做 manifest/hash 校验，发现额外文件即废弃该 run。

## 失败路线

原计划优先取 NASA/JPL 官方网页作为工程正例，但本机对多个 NASA/JPL 文本端点连续出现 TLS `SSL_ERROR_SYSCALL`；未取得可核验完整原文，因此停止该路线。未留下 NASA 半成品，也未把搜索摘要充当材料。
