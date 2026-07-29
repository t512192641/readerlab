# 最终报告任务

你是本轮独立报告编写者。只读取：

- `01-input-manifest.md`
- `02-seat-map.md`
- `03-raw-seeds.md`
- `04-clusters-and-screen.md`
- `05-verification.md`
- `06-expert-audit.md`
- `raw/baseline.md`
- `raw/seat-1.md` 至 `raw/seat-5.md`
- `expert-runs/C1/run.json`
- `expert-runs/C5/run.json`
- `expert-runs/C8/run.json`

不得读取仓库其他路径、历史 run、产品判词、其他实验、网页或归档 tar；不得搜索。只写入：

`07-final-report.md`

## 固定资源记录

- 发现语义模型调用：6 次（普通基线 1 + 五席 5）；比较者 1 次；Expert 3 次；Reviewer 3 次；Expert 后审计 1 次。
- 本轮语义模型调用合计：14 次。
- 外部搜索：2 次 `web` 搜索调用、6 个检索词；另有 1 次批量打开调用（5 个候选来源页面）。这些不是模型调用。
- 实验没有调用 Writer、Reader、ABC 或完整编排器。

## 必答问题

用中文回答附件要求的 14 个问题：

1. 基线与五席原始种子数；
2. 分别形成的不同机制簇数（明确去重口径）；
3. 多入口是否扩大召回，还是只改变名称包装；
4. 固定专家、轮换单领域、轮换跨领域、图书互引各自贡献；
5. 扣除作者贡献是否减少原文续写；
6. 神圣价值式结果的轻筛 A/B/C 与 Expert 后终局，说明原因；
7. 多少 A 类种子通过轻核验（区分全体 A 与实际送核验子集）；
8. 多少进入 Expert 的种子仍保留生成剩余（区分完全/部分）；
9. Expert 是否把好种子拉回原文轨道；
10. 是否出现强行跨域、名人标签套用或高频理论扎堆；
11. 搜索调用、模型调用和大致输出规模；
12. 结论只能是 `SUPPORTED`、`PARTIALLY SUPPORTED` 或 `NOT SUPPORTED` 之一；
13. 仍未证明的问题；
14. 下一轮最小改动。

## 结论口径

不要把单章、单次、多提示位运行写成因果证明。应区分：发现层机制覆盖观察、轻核验、Expert 技术终端、应用资格和产品接受。根据 06 审计，建议评估为 `PARTIALLY SUPPORTED`；若不同意，必须以证据解释。
