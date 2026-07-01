# Demo B: Skill / Engineering Material

## Scope

本 demo 只把 `gstack/spec/SKILL.md` 当作阅读材料，产出 ReaderLab 的 Skill / 工程材料样本包。未安装、未同步、未启用任何 Skill，也未运行材料中的命令。

## Source

- Material: `gstack/spec`
- Source path: `/Users/tianqiang/技能项目/skills-canonical/packages/gstack/spec/SKILL.md`
- Material type: `skill_engineering`
- Coverage: selected Skill unit, full source file read for this demo

## Package Shape

- `10_一手正文/001_净化正文.md`: 净化正文，保留用途、触发、用户意图、核心流程、约束、失败条件、输出要求和设计亮点。
- `20_AI陪读/001_reader-facing.md`: 面向读者的自然中文陪读页。
- `20_AI陪读/design-asset-notes.md`: 面向产品负责人的设计资产笔记。
- `audit/contracts/*.json`: 方法核审计合同。
- `audit/location-map.json`: 净化正文段落、读者页段落、claim、candidate 和批注触发的稳定锚点。
- `audit/source-cleaning-map.md`: 说明原始 `gstack/spec` 内容如何被保留、压缩、移入设计资产、移入 audit 或拒绝进入 reader-facing。
- `audit/trace-to-reader.md`: 说明 reader-facing 每段如何消费正文、claim 和候选决策。
- `audit/eval.md`: writer 自检，状态仅为 `writer_ready_for_reader_eval`。

## Removed From Clean Body

以下内容没有进入净化正文主体：

- 本机安装、升级、同步、打开网页、提交代码等命令。
- 会话探测、分支探测、遥测、路径、hash、进程、环境变量和调试输出。
- 针对 Claude Code / Conductor / plan mode 的宿主执行外壳。
- 大段重复决策模板和工具调用格式细则。
- 已废弃迁移、vendored gstack、artifact sync 等运维协议。

这些内容在本 demo 中被视为工程外壳、运行时协议或风险控制素材，不作为读者理解该 Skill 的主体。

## Review Hardening

- `location-map.json` 把 annotation triggers 从自然语言段落描述升级为稳定 anchor。
- `source-cleaning-map.md` 补足外部 reviewer 关心的清理可复核性：哪些源内容保留、压缩、移入设计资产、移入 audit 或拒绝进入 reader-facing。
- `trace-to-reader.md` 证明 reader-facing 不是自由发挥，而是消费了 claim ledger、candidate tournament 和 Skillization Gate。
- `body-track-gate.json` 对 Skill / 工程材料使用 `skill_engineering_cleaned_body_pass`，避免把 cleaned-body pass 和完整书籍 reader package pass 混在一起。
