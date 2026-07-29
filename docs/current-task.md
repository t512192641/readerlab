# ReaderLab 当前执行切片

> owner：当前任务、run、停止点、允许动作、禁止动作与下一生产授权
> 更新日期：2026-07-29
> current-task: `taskcards/T2.38.md`
> current-run: `runs/T2.38-U01-SOCIAL-CONNECTION-EXPERT-TEACHING-01`
> execution-status: `STOPPED_AFTER_EXPERT_TEACHING_REVIEW`
> product-verdict: `unknown`
> product-verdict-source: `taskcards/T2.38.md`
> next-production-authorization: `none`
> governance-status: `DIAGNOSTIC_EXPERT_TEACHING_IN_PROGRESS`

## 当前目标

只验证固定 U01、固定 Social Connection Model 与 T2.36 冻结来源范围下，Expert 能否直接写出普通读者可独立学习的教学版专家课，并由另一个全新上下文审核来源忠实与教学完整度。该 run 是 diagnostic sidecar；暂停 Writer、ABC、Discovery 和产品装配，不构成生产 runtime 或长期合同变更。

## 当前允许

- 只执行 `taskcards/T2.38.md` 预注册的 Expert teaching、独立来源／教学审核及双门条件性 Expert 产品包步骤。

## 当前禁止

- 不修改 `PRODUCT-DECISIONS.md`、`blueprints/PIPELINE-MAP.md`、`contracts/BOOK-CONTENT-FLOW-v2.md`、历史 run、T2.36/T2.37 或 U01/U02/U03 冻结产物、Skill 或生产入口。
- 不搜索替换 C、不比较 D／ABC、不生成 B、不发明 M1/M2/M3、不增加 Judge／知识库／生产架构。
- 不启动 Writer、ABC、Discovery 或一般产品装配；不读取 T2.36 Expert 正文、T2.36/T2.37 Reader、旧稿、Writer、content lock、判词或 Agent 对话；不搜索新来源、不静默修改 Prompt、不重试或补跑。
- Expert teaching 与审核职责已由两个全新上下文承担；两门均通过后才生成 Expert 产品包。

## 停止点

- Expert teaching 与独立审核终局：`SOURCE_FIDELITY_PASS` + `TEACHING_PASS`。控制层已生成 `acceptance/expert-product-review.md`；产品负责人判词仍为 `unknown`，产品包不构成接受。
- 停止在产品负责人审阅前；不启动 Writer、Reader、ABC、Discovery 或其他产品装配。下一生产授权保持 `none`。
