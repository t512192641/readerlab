# B2 tandem-comments fixture

This fixture keeps only nearby cleaned-body excerpts for comment replay
validation. It is not a replacement for the source body.

核心流程附近片段：
复杂任务需要外部化状态；发现要及时落盘；决策前要重新对齐目标；错误要变成下一步策略的输入。

错误处理附近片段：
三次失败后升级、不能原样重试、每次失败都要记录，这使复杂任务更容易被审计和接手。

```tandem-comments
{
  "rl-b2-state-003": {
    "anchor": {
      "exact": "复杂任务需要外部化状态；发现要及时落盘；决策前要重新对齐目标；错误要变成下一步策略的输入。",
      "pos": 170,
      "prefix": "source body.\n\n核心流程附近片段：\n",
      "suffix": "\n\n错误处理附近片段：\n三次失败后升级、不能原样"
    },
    "status": "open",
    "thread": [
      {
        "author": "Reader",
        "ts": "2026-07-01T00:00:00.000Z",
        "text": "这句话是不是可以迁移成 ReaderLab 的通用执行规则？"
      },
      {
        "author": "Codex",
        "ts": "2026-07-01T00:00:00.000Z",
        "text": "可以作为设计原则候选，但不能直接变成正式 Skill。它需要继续拆成触发、输入、步骤、输出、边界和证据，才能进入 Skillization Gate。"
      }
    ]
  },
  "rl-b2-error-004": {
    "anchor": {
      "exact": "三次失败后升级、不能原样重试、每次失败都要记录，这使复杂任务更容易被审计和接手。",
      "pos": 227,
      "prefix": "要变成下一步策略的输入。\n\n错误处理附近片段：\n",
      "suffix": "\n"
    },
    "status": "open",
    "thread": [
      {
        "author": "Reader",
        "ts": "2026-07-01T00:00:00.000Z",
        "text": "这里的三次失败规则，对 ReaderLab 是不是应该做成自动化？"
      },
      {
        "author": "Codex",
        "ts": "2026-07-01T00:00:00.000Z",
        "text": "它适合进入错误处理协议讨论，但不应该被自动提升为 ReaderLab 默认架构。这里的证据只支持“失败要转成策略输入”，不支持复制原 Skill 的宿主外壳。"
      }
    ]
  }
}
```
