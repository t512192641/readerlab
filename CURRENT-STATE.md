# ReaderLab 当前状态

> owner：当前执行状态、停止点与下一项产品动作
> 快照日期：2026-07-25
> 长期产品责任仍由 [`PRODUCT-DECISIONS.md`](PRODUCT-DECISIONS.md) 拥有；长期派生架构仍由
> [`blueprints/PIPELINE-MAP.md`](blueprints/PIPELINE-MAP.md) 呈现。本文件不改写两者。

## 当前任务与 run

- 当前业务对象：[`taskcards/T2.35.md`](taskcards/T2.35.md)，状态
  `P2_PASS_READY_FOR_PRODUCT_REVIEW`。
- 当前 run：`runs/T2.35-CH08-D3-EXPERT-P2-01/`。
- 已到达的技术停止点：D3 Expert、知识卡、独立来源审核／P2、审阅包以及 production／acceptance
  freeze 已形成；P2 派生状态为 `P2_PASS_WORTH_WRITING`。
- 这只证明 D3 具备在后续另行获批任务中进入 Writer 的资格；当前没有 Reader、产品接受、
  Writer、Fidelity、装配或 P3。

## 业务证据基线与工作树快照

- 业务证据基线 commit：
  `8c45281b0bec4dc82f15b8deb30c5f07ce9e6efb`。其后的纯审计提交不提高业务成熟度。
- 审计控制面基线 commit：
  `5000740a62162f41e5501f6085a48c09fbf383d0`。它固定本次状态治理开始时的审计快照，不表示
  动态仓库 HEAD，也不提高业务成熟度。
- [`taskcards/T2.35.md`](taskcards/T2.35.md) 有未提交业务修改，SHA-256：
  `740717e803b38490a360e00e0badf4e89085b740447254f860fd9edf8560dbc6`。
- `runs/T2.35-CH08-D3-EXPERT-P2-01/` 是未跟踪的当前业务 run；审阅包 SHA-256：
  `4c0248572786e72cbfa0dffed63c15f745a0a47243b5bc5c30221a277f6d101f`，
  production freeze SHA-256：
  `0bde93d07d98e9c7d66fb29a2e2c6c463314b2aa4f723a945e5f4c65af40d385`，
  acceptance freeze SHA-256：
  `c981641cda9133258ce51d5a1c9808c934a309ccc792055f064d7b54f0e387eb`。
- 上述 dirty 状态是当前业务证据的一部分，不得被清理、覆盖或用旧任务状态替代。

## 工程合同状态

- 图书内容流合同
  [`contracts/BOOK-CONTENT-FLOW-v2.md`](contracts/BOOK-CONTENT-FLOW-v2.md) 已通过独立工程审查，
  由 [`contracts/BOOK-CONTENT-FLOW-v2-freeze-receipt.md`](contracts/BOOK-CONTENT-FLOW-v2-freeze-receipt.md)
  绑定冻结身份并完成工程侧技术激活；唯一 current pointer 由
  [`blueprints/PIPELINE-MAP.md`](blueprints/PIPELINE-MAP.md) 拥有。
- 该状态只到 `implemented`／技术激活；内容生产 runtime 尚未 `integrated`，真实链路尚未
  `verified`，产品 `accepted` 仍为 `unknown`。它不授权 Writer 或创建新 run，也不改变下文
  停止点与唯一产品前进行动。

## 当前验证入口

- Active deterministic tests：`python3 -B tests/entry.py`。这是当前可维护、可运行的确定性测试
  子集，不是产品 gate，也不证明全项目或任一完整产品能力已经取得资格。
- 早期 clean-seed validator 已退役并从当前工作树删除；历史身份保存在本地 Git
  `c13ea5a:validate.py`，不再提供当前回放命令，也不构成当前健康信号。

## 当前停止点

仓库当前处于审计控制面的 `RED` 门。T2.35 已冻结对象仍可由产品负责人审阅，但在新的明确
方案、任务卡和授权出现前，停止在产品审阅，不得把 P2 技术通过解释为产品接受或整体流程
通过。

## 唯一产品前进行动

产品负责人审阅
[`runs/T2.35-CH08-D3-EXPERT-P2-01/acceptance/acceptance-report.md`](runs/T2.35-CH08-D3-EXPERT-P2-01/acceptance/acceptance-report.md)，
决定 D3 Expert 是否值得在后续另行获批任务中进入 Writer。

该判断本身不授权 Writer，不授权创建新 run，也不改变图书线的完整长期责任。

## 当前禁止

- 不把 T2.12、T2.25 或任何其他历史任务写成当前下一步。
- 不创建下一次正式生产 run，不调用新的生产语义角色。
- 不启动 Writer、Fidelity、装配、P3、最终 Judge、M2 或 T3。
- 除已技术激活的图书内容流合同 v2 外，不再新增或扩写长期 Prompt、角色、关卡、合同、
  schema、透镜登记册或自动化，也不启动内容生产 runtime。
- 不移动、删除、覆盖或重写历史任务、run、冻结产物及当前 dirty 业务证据。
- 不从旧 ReaderLab 项目补取信息。

## Unknown

- 产品负责人是否接受 T2.35 D3 Expert：`unknown`。
- 若接受，下一张任务卡的目标、读取闭集、模型、预算、验证与停止点：`unknown`。
- 现行 Writer、Fidelity、装配、最终 Judge 和完整端到端组合是否可用：`unknown`。
- Expert 路线能否在冻结条件和未见材料上复现：`unknown`。
- 图书线任何完整端到端能力是否达到资格通过：尚无证据；当前为 `unknown`。
- Skills 线的首个获授权真实样张与实现路线：`unknown`。

## 派生入口规则

README、执行路线图、流水线蓝图和专题路线文档只链接本文件，不复制当前任务、停止点或下一步
正文。历史快照可以保留，但必须明确日期和已失效性质。业务状态变化时先更新本 owner，再同步
派生入口。
