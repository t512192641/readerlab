# ReaderLab

这是 ReaderLab 的全新、隔离项目起点。

它只带入五类已经整理并可直接阅读的资产：

1. [产品决议](PRODUCT-DECISIONS.md)
2. [工程经验](ENGINEERING-LESSONS.md)
3. [金标、反例与边缘案例](GOLD-STANDARDS.md)
4. [流水线开发蓝图](blueprints/PIPELINE-MAP.md)
5. [图书与 Skills 借鉴方法](references/BOOK-AND-SKILLS-METHODS.md)

`examples/` 保存可直接阅读的固定案例；`audit/manifest.json` 只负责证明这些文件没有被静默改动。

本项目不包含任何旧 ReaderLab 代码、Prompt、合同、runtime、run、Memory 或旧项目路径，也不允许 Agent 自动回查旧项目。缺失信息必须标为 `unknown`，等待产品负责人在新项目内决定。

当前状态：产品与证据基线已建立；功能代码尚未开始开发。

运行以下命令可验证项目边界：

```bash
python3 validate.py
```
