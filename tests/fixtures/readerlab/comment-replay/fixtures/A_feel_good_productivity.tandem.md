# A2 tandem-comments fixture

This fixture keeps only nearby body excerpts for comment replay validation.
It is not a full body track.

第一个正文附近片段：
如果这件事很好玩，会是什么样子？

第二个正文附近片段：
休息不是一份特别的奖赏。它是一种绝对的必需。

```tandem-comments
{
  "rl-a2-play-001": {
    "anchor": {
      "exact": "如果这件事很好玩，会是什么样子？",
      "pos": 147,
      "prefix": "body track.\n\n第一个正文附近片段：\n",
      "suffix": "\n\n第二个正文附近片段：\n休息不是一份特别的奖赏"
    },
    "status": "open",
    "thread": [
      {
        "author": "Reader",
        "ts": "2026-07-01T00:00:00.000Z",
        "text": "这里的“好玩”是在鼓励逃避任务，还是在改变行动方式？"
      },
      {
        "author": "Codex",
        "ts": "2026-07-01T00:00:00.000Z",
        "text": "这里不能读成逃避任务。它更像是在问：同一个目标能不能换一种更有能量的进入方式。这个回复只依据正文附近的 play/control/connection 线索，不把它扩大成全书结论。"
      }
    ]
  },
  "rl-a2-rest-002": {
    "anchor": {
      "exact": "休息不是一份特别的奖赏。它是一种绝对的必需。",
      "pos": 176,
      "prefix": "很好玩，会是什么样子？\n\n第二个正文附近片段：\n",
      "suffix": "\n"
    },
    "status": "open",
    "thread": [
      {
        "author": "Reader",
        "ts": "2026-07-01T00:00:00.000Z",
        "text": "这里是不是在说休息本身就是系统的一部分，而不是完成任务后的奖励？"
      },
      {
        "author": "Codex",
        "ts": "2026-07-01T00:00:00.000Z",
        "text": "是的，正文附近把休息放在维持系统的位置，而不是奖励位置。ReaderLab 可以把它解释成维护机制，但不能借此宣称这份私有材料已经证明公开长文泛化。"
      }
    ]
  }
}
```
