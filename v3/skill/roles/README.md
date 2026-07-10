# ReaderLab V3 角色合同索引

执行 Agent 只读取自己的角色合同、主控提供的本线路规则摘录和任务输入；完整线路协议仅由主控 / 线路编排读取，不得为了保险加载另一条线路或其他角色合同。

| 线路 | 阶段 | 标准实例数 | 角色合同 |
| --- | --- | ---: | --- |
| 共用 | 调度 | 1 | `orchestrator.md` |
| 图书 | 一手主体 | 1 | `source-map.md` |
| 图书 | 锚点搜索 | 2 | `anchor-nominator.md` |
| 图书 | 锚点归并 | 1 | `anchor-merger.md` |
| 图书 | 候选生产 | 3 | `cognition-candidate.md` |
| 共用 | 事实复核 | 1 | `fact-checker.md` |
| 图书 | 绝对裁判（含盲区检查） | 1 | `cognition-judge.md` |
| 图书 | 成文与最终页面装配 | 1 | `book-writer.md` |
| 图书 | 无上下文冷读 | 1 | `cold-reader.md` |
| Skill | 一手主体 | 1 | `skill-source-integrator.md` |
| Skill | 机制候选 | 1 | `skill-mechanism-auditor.md` |
| Skill | 独立裁判 | 1 | `skill-judge.md` |
| Skill | 读者成文 | 1 | `skill-writer.md` |
| Skill | 独立冷读 / 冷启动 / 复现 | 1 | `cold-start-reproducer.md` |

标准无早停计划不含主控：图书线为 11（`1 + 2 + 1 + 3 + 1 + 1 + 1 + 1`），Skill 线为 5。合法 0 候选时，无输入的下游 dispatch 记为 skipped，实际任务数可以更少；不得为凑 11 伪造空核查。共用事实核查在图书标准计划中计 1；Skill 只有引入外部事实时才追加，并按协议触发预算审批。

同一任务只允许一个角色拥有最终判定权：图书事实可靠由 fact-checker 判定，图书认知价值由 cognition-judge 判定，图书好读由 cold-reader 报告；Skill 来源由 source integrator 证明，机制价值由 skill-judge 判定，表达由 skill-writer 完成，好读与可复用范围由 cold-start-reproducer 分门验证；运行真实性由主控按 run manifest 与独立闸门裁决。
