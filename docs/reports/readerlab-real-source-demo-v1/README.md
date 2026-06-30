# ReaderLab real-source demo v1

本目录用于验证“正文优先陪读包”的真实来源 demo。它不是生成器输出承诺，也不是 product ready 样张。

## 当前样本

### 第一组

- `dbs-good-question/reader/01_dbs-good-question_阅读页.md`
  - 来源：`/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-good-question/SKILL.md`
  - 用途：验证 Skill/工程材料的“净化正文主体 + AI 后置讲解 + 设计资产卡”。
- `elon-success/reader/01_成功之道_阅读页.md`
  - 来源：`/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
  - 章节：TOC “成功之道”，正文内部首标题“成功要素”。
  - 用途：验证书籍完整章节正文先行。

### 第二组

- `dbs-decision/reader/01_dbs-decision_阅读页.md`
  - 来源：`/Users/tianqiang/技能项目/skills-canonical/packages/dbs-suite/dbs-decision/SKILL.md`
  - 用途：验证决策系统类 Skill 的净化正文和设计资产提炼。
- `elon-team/reader/01_打造卓越团队_阅读页.md`
  - 来源：同一本 EPUB。
  - 章节：TOC “打造卓越团队”。
  - 用途：验证另一章完整书籍正文，不让单一章节成为孤例。

## 当前判断

- 读者页应以一手正文或净化正文为主体。
- AI 讲解和设计资产卡后置，不能替代正文。
- source refs、location map、claim trace、machine/human 状态、路径和抽取细节进入 audit。
- 本目录可用于人工评审和产品讨论，不代表自动生成器已经具备同等能力。

## 已知风险

- 这是手工 demo，不证明 `scripts/readerlab.py` 已能自动生成同等结果。
- Skill reader 仍可能像工具说明书；后续要继续判断哪些模板应留在正文、哪些应转入附录。
- 书籍 reader 的注释处理仍需产品决定：留在页面末尾、折叠、还是拆到 audit/附录。
