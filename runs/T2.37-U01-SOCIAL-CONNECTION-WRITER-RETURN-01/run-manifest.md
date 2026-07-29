# T2.37 U01 Social Connection Writer return · run manifest

## 身份与范围

- 任务：`T2.37`
- run：`runs/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01`
- 分支：`experiment/u01-social-connection-depth-seam`
- 审计基线：`c8ef926216a99c45ae1341d1c74acde94fd92ae3`
- T2.36 源 commit：`2bd7c20938ed5bb17749fe999423ba22819973e3`
- 启动时间：`2026-07-29T05:20:53-0400`
- 固定 C：Iris Marion Young 的 Social Connection Model
- 固定 U01：本 run `inputs/u01-frozen.md`，16368 bytes，SHA-256 `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c`
- 唯一差异：只修复 T2.36 Writer 的两处归属表述，并添加 brief 指定的来源与归属说明
- 状态：`STOPPED_AFTER_PRODUCT_PACK_WAITING_FOR_PRODUCT_REVIEW`
- 实验性质：`diagnostic sidecar; production integration and product acceptance are not claimed`

## 冻结输入

六个输入均从 T2.36 逐字复制到本 run，原始与副本身份见 `control/input-freeze.json` 与
`control/freeze-stage-0.sha256`。T2.36 源文件不在本 run 中覆盖或修改。

## 预注册执行边界

- 两个语义阶段分别由两个全新 Agent 上下文承担，均 `fork_turns="none"`；不得合并职责。
- Writer 与 Fidelity／Depth v2 均禁止联网；不读取旧稿、产品判词、Agent 历史、其他路线或 T2.36 隐藏推理。
- 每阶段仅一次语义执行；重试：`no`；Prompt 修改：`no`；return brief 与阶段任务 hash 在首个调用前冻结。
- Reader v2 不能覆盖 Reader v1；T2.36 所有冻结文件与旧稿在双门前保持未读。
- 只有 `FIDELITY_PASS + DEPTH_PASS` 才允许控制层机械生成产品包；否则停止且不创建条件性文件。

## 执行上下文（完成后补全）

| 阶段 | 角色 | Agent ID | 模型 | reasoning | 精确读取 | 联网 | 终局 |
|---|---|---|---|---|---|---|---|
| 1 | Writer return | `/root/u01_writer_return` | unavailable | unavailable | U01 + Expert + content-lock + Reader v1 + return brief + phase task | no | `PHASE_WRITER_RETURN_FROZEN` |
| 2 | Fidelity／Depth v2 | `/root/u01_fidelity_depth_v2` | unavailable | unavailable | U01 + Expert + source-map + content-lock + Reader v2 + return brief + phase task | no | `FIDELITY_PASS + DEPTH_PASS` |

## 条件性阶段

- 产品对照包仅在 Phase 2 双门通过后由控制层机械装配；比较旧直接路线短稿与 Reader v2，不含 Reader v1。
- 产品包已在双门通过后机械装配；匿名随机映射单独保存在 `acceptance/version-key.md`，产品审阅前不得打开。

## 证据与停止点

- Writer v2 SHA-256：`a329df15d0162ea16479a56554970aba6a29d03ea993bdc9c959834682102a02`
- `acceptance/fidelity-depth-review-v2.md` SHA-256：`8751f9719cddf0972248f5d98c18a2c73c0ab0da26f41a211abe958414522862`
- Fidelity 终局：`FIDELITY_PASS`
- Depth 终局：`DEPTH_PASS`
- 产品对照包：已生成，比较当前旧直接路线短稿与 Reader v2；Reader v1 未进入。
- `acceptance/product-review.md` SHA-256：`0a462fe1c17f049ba3a486c7828ebe9e30fc71416b71933567d075ae3f88bc05`
- `acceptance/version-key.md` SHA-256：`acb0ac703f9ea78fd73bd94069423815e9f10680efc4e23c731b7701ac8fb748`（产品审阅前不得打开）
- 最终停止点：`STOPPED_AFTER_PRODUCT_PACK_WAITING_FOR_PRODUCT_REVIEW`
- 完整归档：`artifacts/T2.37-U01-SOCIAL-CONNECTION-WRITER-RETURN-01.tar.gz`；归档 hash 记录在本任务外部提交证据中，避免把自引用 hash 写入归档内容。
