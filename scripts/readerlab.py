#!/usr/bin/env python3
"""ReaderLab v0.1 importer and Tandem Comments helper."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TEXT_EXTS = {
    ".md",
    ".mdx",
    ".txt",
    ".rst",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".sh",
    ".html",
    ".css",
    ".tmpl",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "coverage",
    ".cache",
    "__pycache__",
}

SOURCE_BLOCK_RE = re.compile(r"```tandem-comments\n(.*?)\n```\s*$", re.S)

TRIAL_UNIT_ID = "01_核心入口与总览"
TERMS_PAGE_BASENAME = "02_Skill阅读术语表"
TERMS_PAGE_FILENAME = f"{TERMS_PAGE_BASENAME}.md"
DEFAULT_AGENT_READINGS_DIR = Path("data/skill-readings")
LIFEATLAS_ROOT = Path("/Users/tianqiang/LifeAtlas")
CONTRACT_SCHEMA_DIR = Path(__file__).resolve().parents[1] / "docs" / "contracts"
REQUIRED_CONTRACT_SCHEMAS = ("readerlab.global-map.v1", "readerlab.distillation.v1")
HUMAN_CLEARED_STATUSES = {"accepted", "not_required"}
CONTRACT_PACKAGE_REQUIRED_SCHEMAS = {
    "readerlab.source-registry.v1",
    "readerlab.location-map.v1",
    "readerlab.output-eval.v1",
}
CONTRACT_ROUTE_SCHEMAS = {
    "readerlab.catalog-map.v1",
    "readerlab.capability-map.v1",
    "readerlab.grounded-global-map.v1",
}
CONTRACT_FULL_COVERAGE_STATUSES = {
    "full",
    "full_body",
    "full_source",
    "full_skill_inventory",
    "complete",
}
CONTRACT_REF_KEYS = {
    "source_refs",
    "location_refs",
    "primary_refs",
    "primary_location_refs",
    "decision_evidence_refs",
    "evidence_refs",
}
CAPABILITY_CORE_FIELDS = (
    "trigger_signals",
    "near_neighbor_exclusions",
    "method_atoms",
    "required_inputs",
    "output_contract",
    "verification",
    "route_decisions",
)
OUTPUT_EVAL_REQUIRED_CATEGORIES = {
    "reader_audit_separation",
    "audit_evidence_preserved",
    "first_hand_body_not_replaced",
    "ai_reduces_understanding_cost",
    "high_value_details_preserved",
    "source_refs_specific",
    "technical_insights_non_generic",
    "overpromoted_claims_downgraded",
    "machine_not_human",
}
TRIAL_SKILL_NAMES = {
    "spec",
    "office-hours",
    "autoplan",
    "plan-ceo-review",
    "plan-eng-review",
    "plan-design-review",
    "plan-devex-review",
    "plan-tune",
}

READING_UNIT_CLASSIFIERS: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [
    (
        "01_核心入口与总览",
        ("spec", "office-hours", "autoplan"),
        ("入口", "总入口", "路由", "router", "main entry", "规格", "spec", "计划", "澄清"),
    ),
    (
        "02_诊断审查与质量判断",
        ("review", "qa", "guard", "canary", "careful", "benchmark", "diagnosis", "diagnose", "deconstruct", "check", "audit", "evaluate", "evaluating"),
        ("诊断", "审查", "检测", "质量", "对标", "拆解", "评估", "体检", "判断框架", "风险", "qa", "review", "benchmark", "diagnosis"),
    ),
    (
        "03_问题决策与行动系统",
        ("good-question", "decision", "goal", "action", "slowisfast", "learning", "learn"),
        ("问题说明书", "好问题", "可解性", "决策", "目标", "执行力", "行动", "学习", "反馈", "选择", "decision", "goal", "question"),
    ),
    (
        "04_多角色讨论与观点碰撞",
        ("chatroom", "austrian"),
        ("多角色", "专家", "聊天室", "观点碰撞", "讨论", "判官", "并行", "chatroom"),
    ),
    (
        "04_内容资产工程化",
        ("content-system",),
        ("内容资产", "结构化系统", "内容单元", "主题地图", "选题装配", "来源注册", "去重", "工程化"),
    ),
    (
        "04_内容表达与素材模板",
        ("content", "hook", "title", "xhs", "wechat", "html", "spread", "resonate"),
        (
            "内容",
            "标题",
            "文案",
            "公式",
            "素材",
            "模板",
            "小红书",
            "公众号",
            "微信",
            "排版",
            "传播",
            "共鸣",
            "开头",
            "表达",
            "写作",
            "chatroom",
            "title",
            "content",
            "wechat",
            "html",
        ),
    ),
    (
        "05_状态记忆与报告",
        ("save", "restore", "report", "context-save", "context-restore", "memory", "archive", "session", "retro"),
        ("状态", "存档", "恢复", "报告", "记忆", "上下文", "回顾", "留档", "session", "archive", "restore", "report"),
    ),
    (
        "06_Agent工具与迁移工作台",
        ("agent", "migration", "codex", "pair-agent", "setup-browser-cookies", "sync", "skillify", "dbskill-upgrade", "gstack-upgrade"),
        ("agent", "codex", "迁移", "工作台", "同步", "升级", "工具化", "cookies", "skillify", "upgrade"),
    ),
    (
        "07_流程执行与交付运维",
        ("freeze", "unfreeze", "ship", "deploy", "release", "health", "make-pdf", "document-generate", "document-release", "browse", "scrape", "diagram"),
        ("执行", "交付", "发布", "部署", "运维", "冻结", "解冻", "健康", "浏览器", "抓取", "pdf", "流程", "产物", "deploy", "release", "freeze", "unfreeze", "ship", "browse", "scrape"),
    ),
]

READING_UNIT_PURPOSES = {
    "01_核心入口与总览": "先建立整包用途、入口和读法，帮助读者知道从哪里开始。",
    "02_诊断审查与质量判断": "集中阅读诊断、评估、审查和质量判断方法。",
    "03_问题决策与行动系统": "集中阅读如何提出问题、形成决策、设定目标和推动行动。",
    "04_多角色讨论与观点碰撞": "集中阅读多角色讨论、专家视角模拟和观点碰撞方法。",
    "04_内容资产工程化": "集中阅读如何把大量内容素材整理成可追溯、可重组、可持续生长的内容工程。",
    "04_内容表达与素材模板": "集中阅读内容表达、标题公式、素材模板和写作方法。",
    "05_状态记忆与报告": "集中阅读状态保存、恢复、报告、归档和跨会话上下文。",
    "06_Agent工具与迁移工作台": "集中阅读 Agent 工具、迁移、升级、同步和开发者工作台能力。",
    "07_流程执行与交付运维": "集中阅读执行流程、交付发布、运维检查和产物验收。",
}

STRUCTURE_DIAGNOSIS_UNIT = "90_材料结构诊断"
STRUCTURE_DIAGNOSIS_PURPOSE = "记录机器读完整体结构后仍无法形成稳定阅读路线的材料，避免硬塞进错误目录。"

HUMAN_REVIEW_REGISTRY: dict[tuple[str, str], dict[str, str]] = {
    ("dbs-suite", "dbs-diagnosis"): {
        "human_status": "accepted",
        "reviewer": "user",
        "reviewed_at": "2026-06-29",
        "source": "current_goal_manual_review",
        "note": "用户已人工阅读并基本认可该 DB Skill 核心页；机器 validate 仍只代表结构和覆盖验收。",
    },
    ("dbs-suite", "dbs-good-question"): {
        "human_status": "accepted",
        "reviewer": "user",
        "reviewed_at": "2026-06-29",
        "source": "current_goal_manual_review",
        "note": "用户已人工阅读并基本认可该 DB Skill 核心页；机器 validate 仍只代表结构和覆盖验收。",
    },
    ("dbs-suite", "dbs-xhs-title"): {
        "human_status": "accepted",
        "reviewer": "user",
        "reviewed_at": "2026-06-29",
        "source": "current_goal_manual_review",
        "note": "用户已人工阅读并基本认可该 DB Skill 核心页；机器 validate 仍只代表结构和覆盖验收。",
    },
}

TRIAL_SKILL_DESCRIPTIONS_ZH = {
    "spec": "把模糊意图整理成五阶段的可执行规格，核心是先澄清目标、边界和验收方式，再进入实施计划。",
    "office-hours": "用产品顾问式对话帮助用户想清楚方向，适合需求还没成形、需要拆问题和评估取舍的时候。",
    "autoplan": "把计划交给 CEO、设计、工程、开发体验等多个审查 Skill 顺序复核，是典型的编排型 Skill。",
    "plan-ceo-review": "用创始人/CEO 视角审查计划，重点挑战问题是否值得做、目标是否足够高、范围是否该收缩或放大。",
    "plan-eng-review": "用工程负责人视角审查计划，重点看架构、数据流、边界条件、测试策略、性能和落地风险。",
    "plan-design-review": "用设计视角审查计划，重点看交互清晰度、用户路径、反馈状态、视觉层级和可用性。",
    "plan-devex-review": "用开发体验视角审查计划，重点看执行者是否容易理解、开发、调试、验证和维护。",
    "plan-tune": "调校 AI 的追问敏感度，减少无效问题，只保留会改变方案的问题。",
}

GROUP_MVP_ORDER = [
    "spec",
    "office-hours",
    "autoplan",
    "plan-ceo-review",
    "plan-eng-review",
    "plan-design-review",
    "plan-devex-review",
    "plan-tune",
]

COMPLETED_TRANSLATION_BLOCKS: dict[tuple[str, str], dict[str, str]] = {
    (
        "spec",
        "When to invoke this skill",
    ): {
        "status": "passed",
        "translation": """这个 Skill 会把需求提交成 issue；也可以选择在一个新的 worktree 里启动 Claude Code 代理；后续 `/ship` 在合并时可以关闭源 issue。

当用户要求“把这个整理成规格”“提交一个 issue”“写一张任务票”“把它变成 GitHub issue”或“把它放进待办项”时，使用这个 Skill。""",
        "highlights": """> [!important] 重点
> ==它不是只写规格，而是把规格接到 issue、执行代理和 `/ship` 收尾流程。==

旁批：这一句说明 `spec` 的核心价值是把模糊意图推进到可执行工作流，而不是停在文档层。

> [!important] 重点
> ==触发条件全部围绕“把想法变成可跟踪任务”。==

旁批：这些触发词看起来像普通写作请求，但实际路由到的是“需求进入工程队列”的流程。这个边界很重要。""",
        "note": "完整翻译并通过 ReaderLab v0.1 单块验收。",
    }
}

SKILL_MVP_NOTES: dict[str, dict[str, Any]] = {
    "spec": {
        "title": "spec：把模糊意图变成可执行规格",
        "filename": "01_spec_把模糊意图变成可执行规格.md",
        "why": "这是 gstack 里最像“入口章节”的 Skill。它不是帮你写一段漂亮需求，而是把用户的模糊意图推到可执行、可归档、可派发、可由后续 /ship 闭环的工作单元。",
        "use": [
            "当用户要求“把这个想法整理成规格”“写成 issue”“写成任务单”“放进待办队列”时触发。原文触发关键词保留在基本信息里，方便和原 Skill 对照。",
            "如果用户还在探索“要不要做”，它会把用户引向 `office-hours`；如果已经决定要做，它负责把事情写成可执行规格和 issue。",
            "默认路径不是只写文档，而是**创建 issue、归档规格**，并在执行模式下继续**启动执行代理**。"
        ],
        "body": [
            ("入口信息", "文件头声明了 `name: spec`，版本 `0.1.0`，允许工具是 `Bash`、`Read`、`Grep`、`Glob`、`AskUserQuestion`。==这个工具边界说明规格阶段可以读代码、搜索代码、运行必要命令、向用户提问，但默认不直接编辑业务代码。=="),
            ("何时使用", "当用户要求把想法整理成规格、创建 issue、写成任务单、放进待办队列时，使用这个 Skill。它会把需求写成 issue，也可以在新的工作区里启动 Claude Code 执行代理；后续 `/ship` 可以在合并时关闭源 issue。"),
            ("启动前检查", "启动时先检查 gstack 版本、记录会话、识别仓库模式和计划模式、判断是否在 Conductor 环境、检查是否首次运行、读取主动推荐、遥测、检查点、路由、内置 gstack、历史学习记录等状态。==这些启动检查把 Skill 从静态提示词变成了会感知运行环境的工作流。=="),
            ("计划模式规则", "在计划模式下，Skill 指令优先于通用计划模式。`AskUserQuestion` 可以满足计划模式的停顿要求；遇到 `STOP` 点必须停止；只有 Skill 工作流完成或用户取消时，才退出计划模式。"),
            ("第五阶段的路径选择", "后半段给了明确路径：如果用户要求只生成文件，或当前处在计划模式，就走“只生成文件”的路径；如果用户显式要求执行，或处在默认执行模式，就走“创建 issue + 归档规格 + 启动执行代理”的路径。每条路径都要先回显选择结果，让用户可以在真正执行前打断。"),
            ("创建 issue 和归档规格", "创建 issue 前要重新做敏感信息扫描，确保即将发到 GitHub/GitLab 的正文没有高风险内容。`gh` 可用并已认证时直接创建 issue；否则输出可复制的标题和正文。之后还要把规格归档到本地 `~/.gstack/projects/<slug>/specs/`，并记录 issue 编号、链接、分支、计划模式、是否执行、首次引用耗时、完整交付耗时等元信息。"),
            ("启动执行代理机制", "执行路径下，它先检查工作区是否有未提交改动。如果有，必须让用户选择：继续、先暂存再继续、取消。用户回答后立刻重新检查状态，避免等待期间状态变化。然后固定当前提交 SHA，创建唯一分支和工作区，再把归档规格通过标准输入交给 `claude -p`。"),
            ("质量标准", "后面列出 issue 质量标准：利益相关者语境、已验证的当前状态、全景审计表、量化影响、优先级和理由、明确不要碰的内容、依赖图、数据模型、文件表、可测试验收标准、测试金字塔、根因分析、工作量拆分、回滚策略。")
        ],
        "highlights": [
            ("`/spec` 不是写文档，而是“创建 issue + 归档规格 + 可选启动执行代理”。", "这是把“需求澄清”接到“执行系统”的关键。ReaderLab 后续可以借鉴这种从阅读材料到行动草稿的闭环。"),
            ("创建 issue 和归档前都重新做敏感信息扫描。", "同一份内容进入不同出口前重新检查，是很成熟的安全边界意识。"),
            ("工作区改动检查之后还要立刻复核。", "它没有把 git 状态当成静态事实，而是在真正操作前复核，避免用户在等待期间改变状态。"),
            ("Issue 质量标准是一套可迁移写作框架。", "它把好 issue 的标准拆成 14 项，比单纯要求“写清楚”可靠得多。")
        ],
    },
    "office-hours": {
        "title": "office-hours：先判断问题值不值得做",
        "filename": "02_office-hours_YC式问题澄清.md",
        "why": "这是规格生成之前的产品判断入口。它的职责不是写代码，也不是立刻出方案，而是先把问题、用户、需求证据和替代方案问清楚。",
        "use": [
            "当用户还在探索方向、想讨论产品、想判断是否值得做时使用。",
            "它分为“创业诊断模式”和“创作者/构建者模式”：前者偏真实需求与商业判断，后者偏创造力、可展示性和快速成型。",
            "硬边界是只产出设计文档，不做实现。"
        ],
        "body": [
            ("核心定位", "原文把角色定义成“YC 办公时间伙伴”：先理解问题，再提出方案；对创业者要问硬问题，对创作者/构建者要像有品味的协作者。这个定位比“产品顾问”更具体，因为它规定了对不同人群的不同姿态。"),
            ("创业诊断模式", "创业诊断模式的操作原则是：==具体性才有价值，兴趣不是需求，用户的话比创始人的陈述更真实，观察比演示更有用，现状方案才是真竞争对手，早期要从最窄切口开始。==这是一套非常强的产品诊断方法。"),
            ("六个强制问题", "它要求围绕“真实需求证据、现状替代方案、具体用户、最窄切口、观察到的意外、未来适配度”逐个追问。每个问题都要求听到具体行为、具体人、具体代价，而不是“大家都觉得有意思”。"),
            ("创作者/构建者模式", "创作者/构建者模式不用创业式审讯，而是问“最酷版本是什么”“会展示给谁”“最快能做出什么”“已有东西最像什么”“无限时间会加什么”。它关心的是兴奋感、可展示性和探索。"),
            ("前提挑战", "进入方案前，它要求挑战前提：是不是正确问题，什么都不做会怎样，已有代码能不能复用，如果产物是新的可分发制品，用户怎么拿到。这个环节防止 AI 直接顺着用户的第一个想法往下写。"),
            ("替代方案生成", "第四阶段强制生成 2-3 个方案，而且至少包含最小可行方案和理想架构方案。即使有明显推荐，也必须让用户显式选择。这个设计非常适合我们 ReaderLab：AI 可以建议读法，但不能替用户吞掉关键取舍。")
        ],
        "highlights": [
            ("“感兴趣不等于需求。”", "这是产品判断里最值得划线的一句：喜欢、报名、感兴趣都不等于真实需求。"),
            ("每个强制问题都一次只问一个，并且问完停止等待。", "这说明优秀 Skill 会控制对话节奏，而不是一次甩十个问题制造负担。"),
            ("先挑战前提，再生成替代方案。", "它把“是否该做”和“怎么做”分开，避免过早方案化。"),
            ("硬边界：只产出设计文档，不做实现。", "这是 Skill 职责边界的好例子。")
        ],
    },
    "autoplan": {
        "title": "autoplan：把多角色计划审查串成流水线",
        "filename": "03_autoplan_多角色计划审查流水线.md",
        "why": "这是这一组最能体现多 Skill 协作的文件。它不是自己审查一切，而是读取 CEO、设计、工程、开发者体验审查 Skill，并按顺序执行。",
        "use": [
            "当用户有粗略计划，想一次性跑完整审查链路时使用。",
            "它按 CEO → 设计 → 工程 → 开发者体验的顺序执行，不允许并行。",
            "中间问题由 6 条原则自动决策，但“前提判断”和“改变用户原始方向的挑战”必须交给人。"
        ],
        "body": [
            ("一句话定位", "原文的意思是：一个命令输入粗计划，输出经过完整审查的计划。这说明 `autoplan` 的价值不是新增一种审查视角，而是把分散的审查能力编排成流水线。"),
            ("6 条自动决策原则", "它用“选择完整性、处理影响范围内的问题、务实、避免重复、显式胜过聪明、偏向行动”来替代中间提问。这样可以减少人被频繁打断，但仍保留最终审批。"),
            ("决策分类", "它把中间判断分成“机械决策、品味决策、用户方向挑战”。机械决策可以静默自动决定；品味决策可以自动推荐但最终展示；用户方向挑战永远不能自动决定，因为这意味着模型想改变用户原始方向。"),
            ("顺序执行", "CEO、设计、工程、开发者体验必须严格顺序执行，每个阶段完成并写出必要输出后才进下一阶段。这里的顺序有意义：战略先定，设计再看用户体验，工程再看落地，开发者体验最后看开发者使用体验。"),
            ("不压缩审查深度", "它明确要求仍然读取真实代码、差异、文件，仍然产出每个审查章节要求的图、表、登记和产物。==不能把一个审查章节压缩成一行表格。=="),
            ("Codex 边界", "所有发给 Codex 的提示都必须加边界：不要读或执行 `SKILL.md`，也不要进入 Skill 定义目录。这个边界非常重要，因为一个 AI 审查另一个 AI Skill 包时，很容易被技能文件本身带偏。")
        ],
        "highlights": [
            ("编排 Skill 的职责是组织其他 Skill，而不是吞掉其他 Skill。", "这就是我们做 ReaderLab 流水线时应该学的：拆解、精读、批注、沉淀应当各有职责。"),
            ("用户方向挑战永远不自动决定。", "这体现了产品 owner 权限边界：模型可以建议改变方向，但不能替用户改。"),
            ("顺序强约束：CEO → 设计 → 工程 → 开发者体验。", "复杂审查有依赖关系，不能为了快并行掉。"),
            ("发给 Codex 的提示要加文件系统边界。", "这是跨模型协作时很容易被忽略的安全和聚焦设计。")
        ],
    },
    "plan-ceo-review": {
        "title": "plan-ceo-review：从战略和范围挑战计划",
        "filename": "04_plan-ceo-review_战略与范围审查.md",
        "why": "这个 Skill 的核心是防止团队把一个局部方案做得很漂亮，却解决了错误问题。它用创始人/CEO 视角审查计划的价值、范围和长期代价。",
        "use": [
            "当一个计划已经成形，但还需要判断是否值得做、是否太小或太大、是否错过更高杠杆机会时使用。",
            "它适合放在工程审查之前，因为战略方向错了，工程做得再好也浪费。",
            "它不写代码，只审计划。"
        ],
        "body": [
            ("审查姿态", "它要求审查者不是橡皮图章，而是要提前发现会爆炸的隐患，让计划达到更高标准。它允许明确说“废掉这个方案，改用另一个方案”，说明它不是温和润色器。"),
            ("四种范围模式", "它区分“扩大范围、选择性扩大、保持范围、缩小范围”。不同模式下审查姿态完全不同：有时要推高目标，有时只加固现有范围，有时要手术式砍掉不必要部分。"),
            ("CEO 思维模型", "它强调可逆性、战略拐点、反向思考、聚焦、速度校准、指标怀疑、叙事一致性、长期视角、创始人模式、战时/和平状态。==这里最值得学的是：Skill 不只给检查清单，还给认知姿态。=="),
            ("系统审计", "真正审查前要看提交历史、代码差异、暂存记录、TODO/FIXME、近期改动、项目规则、待办事项、架构文档、设计文档、交接说明。这说明它先建立事实，再发表判断。"),
            ("硬要求", "它把“不可静默失败、错误必须有名字、数据流要考虑阴影路径、交互要考虑边界情况、可观测性、图示、延期事项、回滚策略”都提升成计划质量要求。")
        ],
        "highlights": [
            ("“不允许静默失败。”", "这是一条非常可迁移的工程/产品原则：任何失败如果不可见，就是计划缺陷。"),
            ("先选范围模式，再审查。", "同样是审计划，不同目标下的好建议可能相反。这个前置分类值得学习。"),
            ("允许直接否定原方案。", "优秀审查 Skill 必须能指出根本方向错了，而不是只修细节。"),
            ("系统审计发生在第 0 步前。", "先证据，后判断。")
        ],
    },
    "plan-eng-review": {
        "title": "plan-eng-review：把计划压到可落地的工程形态",
        "filename": "05_plan-eng-review_工程落地审查.md",
        "why": "这个 Skill 负责把计划从“听起来合理”审到“工程上真的能安全落地”。它关注架构、复杂度、数据流、测试、性能和退出计划。",
        "use": [
            "当计划已经有方向，需要确认是否存在过度设计、漏测、错误抽象、隐藏复杂度时使用。",
            "它第一步必须用 `AskUserQuestion` 确认审查目标，这是硬停止点。",
            "它适合接在 CEO 审查之后。"
        ],
        "body": [
            ("范围门", "它最前面要求第一工具调用必须是 `AskUserQuestion`，确认要审当前分支、粘贴计划还是指定文件。这个硬门防止 AI 自己去读一堆不相关上下文。"),
            ("工程偏好", "它明确偏好避免重复、测试充分、不过度也不欠设计、覆盖更多边界情况、显式胜过聪明、差异大小合适。这里的价值是把审查者的判断口径写清楚。"),
            ("工程经理认知模式", "它引入影响半径、默认选择成熟技术、渐进改造优先、系统胜过英雄、可逆性、开发运维一体、必要复杂度与偶然复杂度等模式。"),
            ("项目上下文", "它会加载产品摘要和近期决策摘要，避免重复问用户已经存在的上下文，也能发现当前计划是否违背历史决策。"),
            ("第 0 步范围挑战", "正式审查前先问：已有代码是否已解决部分问题，最小变更是什么，复杂度是否超标，标准方案是否存在，待办事项是否相关，是否完整处理，发布分发是否包含在范围内。"),
            ("退出计划模式的门槛", "最后必须确认计划文件末尾有 `## GSTACK REVIEW REPORT`，包含运行/状态/发现表和结论行，最后一行必须是未解决决策状态。这个尾门防止审查报告写一半就退出。")
        ],
        "highlights": [
            ("第一工具调用必须确认审查对象。", "这是一种强约束：先确定对象，再搜证据。"),
            ("复杂度超过阈值要停下来问是否缩小范围。", "不是所有复杂计划都应该被执行，复杂度本身就是风险信号。"),
            ("退出计划模式的门槛以文件结构为验收标准。", "它不是凭感觉说完成，而是检查产物是否满足契约。"),
            ("区分必要复杂度和偶然复杂度。", "这是审查计划时非常实用的判断尺。")
        ],
    },
    "plan-design-review": {
        "title": "plan-design-review：让计划里的体验决策具体化",
        "filename": "06_plan-design-review_设计体验审查.md",
        "why": "这个 Skill 的目标不是给界面打分，而是把缺失的设计决策补回计划里。它把“以后再打磨”视为风险。",
        "use": [
            "当计划涉及页面、组件、交互、设计系统或用户路径时使用。",
            "它默认要生成视觉稿，因为设计审查没有视觉证据就只是观点。",
            "没有界面范围时应退出，不强行审设计。"
        ],
        "body": [
            ("范围门", "和工程审查一样，第一工具调用必须确认审查目标。即使它强调默认生成视觉稿，也必须先知道审什么。"),
            ("设计哲学", "它反对橡皮图章式界面审查，要求让计划里的体验决策变得有意图。输出不是一篇评论，而是更好的计划。"),
            ("gstack 设计器", "它把 AI 视觉稿生成器当主工具：如果有界面且设计器可用，就生成视觉稿，不用先问许可。它认为视觉稿才是设计计划的核心证据。"),
            ("设计原则", "它强调空状态、信息层级、具体性、边界情况、反模板感、响应式不是简单堆叠、可访问性、默认做减法、建立信任。"),
            ("用户体验行为原则", "它引用用户会扫描而不是细读、用户不读说明、用户会选择第一个看起来合理的选项、用户会凑合着用、导航要回答位置、善意储备、移动端代价更高等真实用户行为。"),
            ("优先级", "上下文压力下优先确认范围、生成视觉稿、覆盖交互状态、识别 AI 模板感风险、梳理信息架构、检查用户旅程。说明它知道设计审查里哪些最容易被漏掉。")
        ],
        "highlights": [
            ("视觉稿就是设计工作的计划。", "这是很强的设计观：用户体验不能只靠文字描述验收。"),
            ("空状态也是功能。", "空状态不是占位符，而是用户体验的一部分。"),
            ("具体性胜过感觉词。", "不要写“干净现代”，要写字体、间距、模式、状态。"),
            ("反模板感。", "它明确对抗通用卡片网格和模板感，这对我们做前端也有参考价值。")
        ],
    },
    "plan-devex-review": {
        "title": "plan-devex-review：把开发者体验当成产品质量",
        "filename": "07_plan-devex-review_开发者体验审查.md",
        "why": "这个 Skill 把开发者当用户来审计划。它关心的不只是 API 能不能用，而是一个开发者从发现、安装、hello world、集成、调试、升级到迁移的完整旅程。",
        "use": [
            "当计划涉及 API、CLI、SDK、包、文档、错误信息、agent、MCP、开发者工具时使用。",
            "它尤其适合 gstack 这种开发者工具，因为 Skill 本身就是开发者体验产品的一部分。",
            "它不做实现，只让计划里的开发者体验决策更具体。"
        ],
        "body": [
            ("角色定位", "它把自己定义成“曾经接触过大量开发者工具上手流程的开发者倡导者”。这个角色会关注开发者为什么第 2 分钟放弃，为什么第 5 分钟喜欢上一个工具。"),
            ("开发者体验第一原则", "它列出首次使用零摩擦、增量步骤、边做边学、替我决定但允许覆盖、对抗不确定性、上下文里的代码、速度是功能、制造惊喜时刻。"),
            ("七个开发者体验特征", "可用、可信、可找到、真正有用、有价值、可访问、有吸引力。每一项都有标杆标准。它不是泛泛说“体验好”，而是有评分维度。"),
            ("首次跑通耗时", "首次跑通耗时是核心指标：小于 2 分钟是冠军级，2-5 分钟是有竞争力，5-10 分钟就开始明显掉队，超过 10 分钟是红旗。"),
            ("审查前扫描", "它要读 README、文档目录、包配置、变更日志，扫描快速开始、命令行帮助、错误信息、示例。它关心开发者看到的真实入口，而不是计划里的愿望。"),
            ("自指性", "原文强调：这个 Skill 本身就是开发者工具，所以也要遵守自己的开发者体验原则。这很重要：好的 Skill 会用自己的原则审自己。")
        ],
        "highlights": [
            ("开发者体验就是面向开发者的用户体验。", "开发者不是内部人，也需要被当成用户设计体验。"),
            ("首次跑通小于 2 分钟是冠军级。", "这是非常清晰的量化标准，能直接进入验收。"),
            ("每个错误都要说明问题、原因和修复方式。", "错误信息不是日志文本，而是帮助用户恢复的界面。"),
            ("这个 Skill 本身就是开发者工具。", "自洽性是优秀 Skill 的标志：自己也要符合自己提倡的原则。")
        ],
    },
    "plan-tune": {
        "title": "plan-tune：调校 AI 的追问敏感度",
        "filename": "08_plan-tune_追问敏感度调校.md",
        "why": "这个 Skill 解决一个很实际的问题：AI 以为自己在谨慎，实际可能在不断打断用户、增加沟通成本。它让追问变成可观察、可调校的行为。",
        "use": [
            "当 gstack 问题太多、太少、太早或太泛时使用。",
            "它偏运行习惯调校，不是某个业务计划审查。",
            "它适合放在整组最后看，因为它调整的是前面所有 Skill 的交互风格。"
        ],
        "body": [
            ("核心问题", "AI 工作流常见失败不是只问错问题，也包括问太多问题。plan-tune 的价值在于把问题敏感度显式化，让系统学习什么时候该问、什么时候该直接推进。"),
            ("可迁移原则", "只问会改变方案的问题。能通过读文件、查代码、看上下文回答的问题不要问用户。问题应该具体、可回答，并解释为什么答案会影响后续动作。"),
            ("与其他 Skill 的关系", "`spec` 需要问清边界，`office-hours` 需要逐个追问，审查类 Skill 需要确认目标。但这些都可能变成过度提问。`plan-tune` 像一个调音台，控制整套系统的交互成本。"),
            ("设计亮点", "它不是把“少问问题”写成一句偏好，而是把 `question_tuning` 放进启动状态，让系统能根据配置或历史行为调整。这个思路适合 ReaderLab 后续：如果读者嫌旁批太密，也应该能调节。")
        ],
        "highlights": [
            ("只问会改变方案的问题。", "这是我们后续所有 AI 工作流都该采用的追问原则。"),
            ("问题敏感度是一种可调参数。", "交互风格不该全靠提示词临场发挥，应该有状态和配置。"),
            ("它调的是整组 Skill 的体验。", "这说明有些 Skill 不是业务能力，而是系统行为调校能力。")
        ],
    },
}


@dataclass(frozen=True)
class FileInfo:
    path: Path
    rel: str
    bytes: int
    chars: int
    sha256: str
    kind: str


@dataclass(frozen=True)
class SkillInfo:
    file: FileInfo
    name: str
    title: str
    description: str
    allowed_tools: str
    frontmatter: dict[str, Any]
    group: str
    route_reason: str
    route_basis: tuple[str, ...]
    route_confidence: str
    structure_status: str


@dataclass(frozen=True)
class TandemCommentPage:
    rel_path: str
    comments: dict[str, Any]
    parse_error: str = ""
    raw_block: str = ""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def slugify(value: str) -> str:
    value = value.strip().replace(" ", "-")
    value = re.sub(r"[^\w\-\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "material"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_extensionless_text_candidate(rel_path: Path) -> bool:
    if rel_path.suffix:
        return False
    parts = {p.lower() for p in rel_path.parts}
    return bool({"bin", "scripts"} & parts)


def classify(rel: str, path: Path) -> str:
    name = path.name.lower()
    parts = {p.lower() for p in Path(rel).parts}
    if name == "skill.md":
        return "skill"
    if path.suffix.lower() in {".md", ".mdx", ".txt", ".rst"}:
        return "document"
    if {"scripts", "bin", "lib", "src", "design", "extension"} & parts:
        return "technical-support"
    if {"test", "tests", "__tests__"} & parts:
        return "test-reference"
    return "config-or-support"


def iter_files(source: Path) -> list[FileInfo]:
    files: list[FileInfo] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel_path = path.relative_to(source)
        if any(part in SKIP_DIRS for part in rel_path.parts):
            continue
        rel = rel_path.as_posix()
        if path.suffix.lower() not in TEXT_EXTS and not is_extensionless_text_candidate(rel_path):
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        files.append(
            FileInfo(
                path=path,
                rel=rel,
                bytes=len(raw),
                chars=len(text),
                sha256=hashlib.sha256(raw).hexdigest(),
                kind=classify(rel, path),
            )
        )
    return files


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    raw = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    data: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and current_key:
            data[current_key] = f"{data.get(current_key, '')}\n{line.strip()}".strip()
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        data[current_key] = value.strip().strip('"').strip("'")
    return data, body


def strip_md(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.strip()


def top_heading(text: str, fallback: str) -> str:
    frontmatter, body = parse_frontmatter(text)
    if frontmatter.get("name"):
        return str(frontmatter["name"])
    in_fence = False
    for line in body.splitlines():
        if line.strip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return strip_md(m.group(1))
    name = Path(fallback).stem
    return name if name.lower() != "skill" else Path(fallback).parent.name


def first_meaningful_paragraph(text: str, limit: int = 260) -> str:
    _frontmatter, body = parse_frontmatter(text)
    for para in re.split(r"\n\s*\n", body):
        clean = "\n".join(
            line.strip()
            for line in para.splitlines()
            if line.strip() and not line.strip().startswith(("```", "---"))
        ).strip()
        if len(clean) >= 40:
            return strip_md(clean.replace("\n", " "))[:limit]
    return ""


def skill_name_from_rel(rel: str) -> str:
    parent = Path(rel).parent.as_posix()
    if parent in {"", "."}:
        return "gstack"
    return Path(parent).name


@dataclass(frozen=True)
class RouteDecision:
    group: str
    reason: str
    basis: tuple[str, ...]
    confidence: str
    structure_status: str


def package_entry_names(book_id: str) -> set[str]:
    base_book_id = book_id.split("__", 1)[0]
    normalized = slugify(book_id).lower()
    normalized_base = slugify(base_book_id).lower()
    names = {normalized, normalized_base}
    if normalized.endswith("-suite"):
        names.add(normalized.removesuffix("-suite"))
    if normalized_base.endswith("-suite"):
        names.add(normalized_base.removesuffix("-suite"))
    if normalized.endswith("-skills"):
        names.add(normalized.removesuffix("-skills"))
    if normalized_base.endswith("-skills"):
        names.add(normalized_base.removesuffix("-skills"))
    return {name for name in names if name}


def skill_scope_artifacts(skill_rel: str, files: list[FileInfo]) -> list[FileInfo]:
    skill_dir = Path(skill_rel).parent.as_posix()
    if skill_dir == ".":
        skill_dir = ""
    artifacts = []
    for file in files:
        if file.rel == skill_rel:
            continue
        if not skill_dir and "/" not in file.rel:
            artifacts.append(file)
        elif skill_dir and file.rel.startswith(f"{skill_dir}/"):
            artifacts.append(file)
    return artifacts


def skill_body_excerpt(text: str, limit: int = 4000) -> str:
    _frontmatter, body = parse_frontmatter(text)
    return strip_md(body)[:limit].lower()


def group_for_skill(name: str, title: str = "", description: str = "") -> str:
    normalized_name = name.lower()
    name_tokens = tuple(part for part in re.split(r"[^a-z0-9]+", normalized_name) if part)
    searchable = f"{normalized_name} {title.lower()} {description.lower()}"
    scores: list[tuple[int, str]] = []
    for group, name_keywords, text_keywords in READING_UNIT_CLASSIFIERS:
        score = 0
        for keyword in name_keywords:
            key = keyword.lower()
            if key in name_tokens:
                score += 4
            elif key in normalized_name:
                score += 3
            elif key in searchable:
                score += 1
        for keyword in text_keywords:
            key = keyword.lower()
            if key and key in searchable:
                score += 1
        if score:
            scores.append((score, group))
    if not scores:
        return STRUCTURE_DIAGNOSIS_UNIT
    scores.sort(key=lambda item: (-item[0], item[1]))
    top_score, top_group = scores[0]
    if len(scores) > 1 and scores[1][0] == top_score:
        return STRUCTURE_DIAGNOSIS_UNIT
    return top_group if top_score >= 2 else STRUCTURE_DIAGNOSIS_UNIT


def route_decision_for_skill(
    *,
    book_id: str,
    file_info: FileInfo,
    name: str,
    title: str,
    description: str,
    body_excerpt: str,
    artifacts: list[FileInfo],
) -> RouteDecision:
    normalized_name = name.lower()
    name_tokens = tuple(part for part in re.split(r"[^a-z0-9]+", normalized_name) if part)
    entry_names = package_entry_names(book_id)
    if file_info.rel == "SKILL.md" or normalized_name in entry_names:
        return RouteDecision(
            group="01_核心入口与总览",
            reason="它位于包入口或名称对应整包入口，优先作为读者理解整包用途和阅读顺序的起点。",
            basis=("包入口", "SKILL.md 正文"),
            confidence="high",
            structure_status="clear",
        )
    if "benchmark" in normalized_name:
        return RouteDecision(
            group="02_诊断审查与质量判断",
            reason="集中阅读诊断、评估、审查和质量判断方法。benchmark 类材料的主任务是对标比较和质量判断，名称与正文共同指向这一组。",
            basis=("SKILL.md 正文/说明", "名称辅助线索"),
            confidence="high",
            structure_status="clear",
        )
    if "chatroom" in name_tokens or "austrian" in name_tokens:
        return RouteDecision(
            group="04_多角色讨论与观点碰撞",
            reason="集中阅读多角色讨论、专家视角模拟和观点碰撞方法。chatroom 类材料的主任务是组织角色、视角和讨论回路，不应归入普通内容表达模板。",
            basis=("SKILL.md 正文/说明", "名称辅助线索"),
            confidence="high",
            structure_status="clear",
        )
    if "content-system" in normalized_name or {"content", "system"} <= set(name_tokens):
        return RouteDecision(
            group="04_内容资产工程化",
            reason="集中阅读内容资产工程化。content-system 类材料的主任务是审计素材规模、建立工程骨架、抽取内容单元、维护关系和去重索引，不应归入单篇内容表达模板。",
            basis=("SKILL.md 正文/说明", "名称辅助线索"),
            confidence="high",
            structure_status="clear",
        )
    if {"save", "restore", "report"} & set(name_tokens):
        return RouteDecision(
            group="05_状态记忆与报告",
            reason="集中阅读状态保存、恢复、报告、归档和跨会话上下文。save/restore/report 类材料的主任务是记录、接续或汇总状态，即使正文包含输出模板，也不应归入内容表达组。",
            basis=("SKILL.md 正文/说明", "名称辅助线索"),
            confidence="high",
            structure_status="clear",
        )

    normalized_title = title.lower()
    normalized_desc = description.lower()
    content_text = f"{normalized_title} {normalized_desc} {body_excerpt}"
    scored: list[tuple[int, int, int, str, list[str]]] = []
    for group, name_keywords, text_keywords in READING_UNIT_CLASSIFIERS:
        content_hits = 0
        name_hits = 0
        evidence: list[str] = []
        for keyword in text_keywords:
            key = keyword.lower()
            if key and key in content_text:
                content_hits += 1
        for keyword in name_keywords:
            key = keyword.lower()
            if key and key in content_text:
                content_hits += 1
            if key in name_tokens:
                name_hits += 2
            elif key in normalized_name:
                name_hits += 1
        if content_hits:
            evidence.append("SKILL.md 正文/说明")
        if name_hits:
            evidence.append("名称辅助线索")
        score = content_hits * 4 + name_hits
        if score:
            scored.append((score, content_hits, name_hits, group, evidence))

    if artifacts:
        artifact_kinds = {artifact_category(file.rel) for file in artifacts}
        if {"脚本入口", "代码实现", "迁移脚本"} & artifact_kinds:
            scored.append((2, 0, 1, "06_Agent工具与迁移工作台", ["脚本/代码职责"]))
        if "生成模板" in artifact_kinds:
            scored.append((2, 0, 1, "04_内容表达与素材模板", ["模板职责"]))

    if not scored:
        return RouteDecision(
            group=STRUCTURE_DIAGNOSIS_UNIT,
            reason="读完名称、说明、正文开头和支持文件后，仍看不出它稳定承担哪类阅读任务。",
            basis=("结构诊断",),
            confidence="low",
            structure_status="diagnostic",
        )

    scored.sort(key=lambda item: (-item[0], -item[1], item[3]))
    top_score, top_content_hits, _top_name_hits, top_group, top_evidence = scored[0]
    tied = [item for item in scored if item[0] == top_score and item[3] != top_group]
    if tied or top_content_hits == 0:
        return RouteDecision(
            group=STRUCTURE_DIAGNOSIS_UNIT,
            reason="候选阅读任务并列或只剩名称线索，机器不能可靠判断它的主阅读位置。",
            basis=tuple(sorted(set(top_evidence + ["结构诊断"]))),
            confidence="low",
            structure_status="diagnostic",
        )

    second_score = scored[1][0] if len(scored) > 1 else 0
    confidence = "high" if top_score >= second_score + 4 and top_content_hits >= 2 else "medium"
    status = "clear" if confidence == "high" else "explainable"
    purpose = READING_UNIT_PURPOSES.get(top_group, "这一组承担特定阅读任务。")
    return RouteDecision(
        group=top_group,
        reason=f"{purpose} 该材料的正文/说明主要指向这个任务，名称只作为辅助线索。",
        basis=tuple(sorted(set(top_evidence))),
        confidence=confidence,
        structure_status=status,
    )


def collect_skills(files: list[FileInfo], book_id: str = "") -> list[SkillInfo]:
    skills: list[SkillInfo] = []
    for info in files:
        if info.kind != "skill":
            continue
        text = read_text(info.path)
        fm, _body = parse_frontmatter(text)
        name = str(fm.get("name") or skill_name_from_rel(info.rel))
        title = top_heading(text, info.rel)
        desc = str(fm.get("description") or first_meaningful_paragraph(text) or "需要阅读正文确认用途。")
        allowed = str(fm.get("allowed-tools") or fm.get("allowed_tools") or "未声明")
        decision = route_decision_for_skill(
            book_id=book_id,
            file_info=info,
            name=name,
            title=title,
            description=desc,
            body_excerpt=skill_body_excerpt(text),
            artifacts=skill_scope_artifacts(info.rel, files),
        )
        skills.append(
            SkillInfo(
                file=info,
                name=name,
                title=title,
                description=desc,
                allowed_tools=allowed,
                frontmatter=fm,
                group=decision.group,
                route_reason=decision.reason,
                route_basis=decision.basis,
                route_confidence=decision.confidence,
                structure_status=decision.structure_status,
            )
        )
    return sorted(skills, key=lambda s: (s.group, s.name))


def files_by_rel(files: list[FileInfo]) -> dict[str, FileInfo]:
    return {f.rel: f for f in files}


def skill_dir_rel(skill: SkillInfo) -> str:
    parent = Path(skill.file.rel).parent.as_posix()
    return "" if parent == "." else parent


def is_file_in_skill_scope(skill: SkillInfo, file: FileInfo) -> bool:
    skill_dir = skill_dir_rel(skill)
    if file.rel == skill.file.rel:
        return False
    if not skill_dir:
        return "/" not in file.rel
    return file.rel.startswith(f"{skill_dir}/")


def artifact_category(rel: str) -> str:
    path = Path(rel)
    parts = path.parts
    name = path.name
    if name == "SKILL.md.tmpl":
        return "模板源"
    if "migrations" in parts and path.suffix.lower() == ".sh":
        return "迁移脚本"
    if "bin" in parts or "scripts" in parts:
        return "脚本入口"
    if "sections" in parts:
        return "分段材料"
    if "templates" in parts:
        return "生成模板"
    if "src" in parts or "lib" in parts:
        return "代码实现"
    if "test" in parts or "tests" in parts or name.endswith((".test.ts", ".test.js", ".spec.ts", ".spec.js")):
        return "测试参考"
    if "docs" in parts or path.suffix.lower() in {".md", ".mdx", ".txt"}:
        return "说明文档"
    if name.endswith(".json"):
        return "配置/清单"
    return "支持文件"


def artifact_role(rel: str) -> str:
    category = artifact_category(rel)
    stem = Path(rel).stem.lower()
    if "init" in stem:
        return "初始化工程骨架、目录和基础规则文件，是工程从空目录进入可用态的入口。"
    if "duplicate" in stem or "dedupe" in stem:
        return "生成去重候选或重复检查结果，避免内容资产库里出现同义重复和近似重复。"
    if "link-map" in stem or "relation" in stem:
        return "生成关系索引或主题关系图，帮助读者理解内容单元之间如何连接。"
    if "processing-ledger" in stem or "ledger" in stem:
        return "重建处理账本或进度索引，让系统能知道哪些素材已处理、哪些仍待处理。"
    if "summarize" in stem or "overview" in stem:
        return "输出系统总览或状态汇总，让读者知道当前工程覆盖范围、进度和下一步入口。"
    semantic_roles = (
        (("init", "scaffold"), "初始化工程骨架、目录和基础规则文件，是工程从空目录进入可用态的入口。"),
        (("source", "registry"), "登记来源材料、建立来源注册表，保证后续内容单元能追溯回原始文件。"),
        (("pending", "todo", "queue"), "生成待处理清单或处理队列，说明哪些素材还没有进入结构化流程。"),
        (("unit", "draft"), "生成内容单元草稿，把原始素材转成可复用的结构化节点。"),
        (("sample", "extract"), "从样本文稿抽取首批内容单元，用来验证字段、关系和去重口径是否稳定。"),
        (("relation", "graph", "map"), "生成关系索引或主题关系图，帮助读者理解内容单元之间如何连接。"),
        (("dedupe", "duplicate"), "生成去重候选或重复检查结果，避免内容资产库里出现同义重复和近似重复。"),
        (("overview", "summary"), "输出系统总览或状态汇总，让读者知道当前工程覆盖范围、进度和下一步入口。"),
        (("assemble", "topic"), "把已有内容单元装配成主题地图或选题稿，验证素材能否被重新组合成发布表达。"),
        (("obsidian", "link"), "补全 Obsidian 链接，让内容单元、主题地图和装配稿可以在笔记系统里互相跳转。"),
    )
    for keywords, role in semantic_roles:
        if all(keyword in stem for keyword in keywords):
            return role
    if category == "模板源":
        return "生成当前 `SKILL.md` 的上游模板，解释正文为什么带有自动生成标记。"
    if category == "迁移脚本":
        return "承接版本升级后的状态修复、目录调整或兼容处理，通常由升级流程按版本发现并运行。"
    if category == "脚本入口":
        return "承接 Skill 正文或 hook 调用，执行具体检查、生成、同步或运行逻辑。"
    if category == "分段材料":
        return "把大段审查、计划或输出要求拆成可复用章节，正文通常会引用或装配它。"
    if category == "生成模板":
        return "为目标项目生成代码、配置或示例文件，是 Skill 产物形态的一部分。"
    if category == "代码实现":
        return "实现命令行、服务、浏览器控制或底层能力，说明复杂功能不只在 Markdown 里。"
    if category == "测试参考":
        return "验证 Skill 或底层工具的行为，也说明该能力期望怎样运行。"
    if category == "说明文档":
        return "补充背景、架构或使用说明，帮助理解正文没有展开的机制。"
    if category == "配置/清单":
        return "声明分段、配置、权限或生成规则，是运行和组织结构的一部分。"
    return "支持当前 Skill 的辅助材料。"


def command_references(command: str) -> list[str]:
    refs: list[str] = []
    for match in re.findall(r"(?:gstack/)?([A-Za-z0-9_.-]+/(?:bin|scripts|migrations|sections|src|templates|docs)/[A-Za-z0-9_./-]+)", command):
        refs.append(match.strip("'\""))
    for match in re.findall(r"(?:gstack/)?([A-Za-z0-9_.-]+/SKILL\.md(?:\.tmpl)?)", command):
        refs.append(match.strip("'\""))
    return refs


def discover_skill_artifacts(skill: SkillInfo, files: list[FileInfo]) -> list[FileInfo]:
    by_rel = files_by_rel(files)
    artifacts = [file for file in files if is_file_in_skill_scope(skill, file)]
    hook_text = str(skill.frontmatter.get("hooks") or "")
    for ref in command_references(hook_text):
        if ref in by_rel and by_rel[ref] not in artifacts and ref != skill.file.rel:
            artifacts.append(by_rel[ref])
    return sorted(artifacts, key=lambda f: (artifact_category(f.rel), f.rel))


def build_terms_glossary() -> str:
    return f"""# Skill 阅读术语表

这份术语表供所有 Skill 中文精读页共用。单页只提示本页重点术语，不重复解释整份术语。

## 基础结构

- `frontmatter`：`SKILL.md` 顶部 `---` 包住的 YAML 元数据，用来声明名称、简介、可用工具、触发条件和 hooks。
- `sections`：可复用的正文分段或输出要求，大 Skill 常用它把长流程拆开维护。

## 工具调用

- `hooks`：把额外检查挂到工具调用流程里的机制，不是正文翻译，而是运行时接入点。
- `PreToolUse`：工具真正执行前的检查点；脚本可以在这里允许、询问或拒绝本次工具调用。
- `matcher`：匹配哪些工具调用会触发 hook，例如 `Bash`、`Edit`、`Write`。
- `command`：命中 matcher 后实际运行的命令，通常会调用 `bin/` 或 `scripts/` 里的检查脚本。
- `Bash`：运行 shell 命令的工具，适合做更新、删除、git、构建等动作，所以常被安全脚本检查。
- `Edit`：修改已有文件的工具；目录边界类 hook 会读取它的目标 `file_path`。
- `Write`：新建或覆盖文件的工具；和 `Edit` 一样需要被目录边界检查。

## 文件机制

- `bin/scripts`：可执行脚本目录。正文负责说明意图，脚本负责真正检查命令、读写状态或执行自动化动作。
- `migrations`：版本迁移脚本目录。它通常不作为 hook 自动触发，而是由升级流程按版本发现、排序并运行。
- `template/.tmpl`：模板源文件。它不是读者要执行的正文，而是生成 `SKILL.md`、代码片段或配置样板的上游材料。
- `src/lib`：底层代码实现目录，通常承载 Markdown 正文无法表达的复杂逻辑。
"""


def artifact_reader_terms(artifacts: list[FileInfo]) -> list[str]:
    categories = {artifact_category(artifact.rel) for artifact in artifacts}
    terms = ["frontmatter"]
    if "脚本入口" in categories:
        terms.append("bin/scripts")
    if "迁移脚本" in categories:
        terms.append("migrations")
    if "模板源" in categories or "生成模板" in categories:
        terms.append("template/.tmpl")
    if "分段材料" in categories:
        terms.append("sections")
    if "代码实现" in categories:
        terms.append("src/lib")
    return terms


def hook_reader_terms(skill: SkillInfo) -> list[str]:
    hook_text = str(skill.frontmatter.get("hooks") or "").strip()
    if not hook_text:
        return []

    matchers = {m.strip() for m in re.findall(r"matcher:\s*\"?([^\"\n]+)\"?", hook_text)}
    tool_terms: list[str] = []
    if "Bash" in matchers:
        tool_terms.append("Bash")
    if "Edit" in matchers:
        tool_terms.append("Edit")
    if "Write" in matchers:
        tool_terms.append("Write")
    return ["hooks", "PreToolUse", "matcher", "command", *tool_terms]


def skill_reader_terms(skill: SkillInfo, files: list[FileInfo]) -> list[str]:
    artifacts = discover_skill_artifacts(skill, files)
    terms = [*artifact_reader_terms(artifacts), *hook_reader_terms(skill)]
    return list(dict.fromkeys(terms))


def skill_terms_hint(skill: SkillInfo, files: list[FileInfo]) -> str:
    terms = skill_reader_terms(skill, files)
    term_text = "、".join(f"`{term}`" for term in terms) if terms else "无特别术语"
    return f"阅读前可先看 [[{TERMS_PAGE_BASENAME}]]；本页重点术语：{term_text}。"


def hook_execution_text(skill: SkillInfo, artifacts: list[FileInfo]) -> str:
    hook_text = str(skill.frontmatter.get("hooks") or "").strip()
    mechanism_categories = {"脚本入口", "迁移脚本", "代码实现"}
    mechanism_paths = [f.rel for f in artifacts if artifact_category(f.rel) in mechanism_categories]
    if not hook_text:
        if mechanism_paths:
            mechanisms = "、".join(f"`{p}`" for p in mechanism_paths[:5])
            more = " 等" if len(mechanism_paths) > 5 else ""
            return f"目录里存在会影响理解的机制材料：{mechanisms}{more}。阅读时要把正文指令和这些脚本、迁移或代码实现一起看；后续动作可能由升级流程、命令片段或底层实现承接。"
        return ""

    matchers = re.findall(r"matcher:\s*\"?([^\"\n]+)\"?", hook_text)
    commands = re.findall(r"command:\s*\"?([^\"\n]+)\"?", hook_text)
    matcher_text = "、".join(f"`{m.strip()}`" for m in matchers) if matchers else "未明确声明 matcher"
    unique_commands = list(dict.fromkeys(cmd.strip() for cmd in commands))
    command_rows = "\n".join(f"- `{cmd}`" for cmd in unique_commands) if unique_commands else "- 未解析到 command。"
    resolved = []
    for cmd in unique_commands:
        for ref in command_references(cmd):
            if any(f.rel == ref for f in artifacts):
                resolved.append(ref)
    resolved_text = "、".join(f"`{r}`" for r in sorted(set(resolved))) if resolved else "未在当前扫描范围内解析到脚本文件。"
    return f"""这个 Skill 声明了 hooks，说明它不是只靠说明文字生效，而是在工具调用前/后接入额外检查或动作。

- 触发点：`PreToolUse`，也就是工具执行前先检查。
- 匹配工具：{matcher_text}
- 被调用命令：
{command_rows}
- 已解析到的机制文件：{resolved_text}

读法：先看 `SKILL.md` 如何设置状态和说明流程，再看 hook 调用的脚本如何读取工具输入、状态文件或环境变量，并返回允许、询问或拒绝等决策。"""


def build_auto_related_materials(skill: SkillInfo, files: list[FileInfo]) -> str:
    artifacts = discover_skill_artifacts(skill, files)
    has_hooks = bool(str(skill.frontmatter.get("hooks") or "").strip())
    if not artifacts and not has_hooks:
        return ""
    if artifacts:
        rows = [
            f"| `{artifact.rel}` | {artifact_category(artifact.rel)} | {artifact_role(artifact.rel)} |"
            for artifact in artifacts[:24]
        ]
        if len(artifacts) > 24:
            rows.append(f"| 其余 {len(artifacts) - 24} 个文件 | 支持文件 | 数量较多，先在 `source.md` 和 manifest 中保留后台索引。 |")
        inventory = "\n".join(rows)
    else:
        inventory = "| 未解析到直接机制文件 | hooks | 当前声明了 hook，但未在扫描范围内解析到对应脚本；完整追溯保留在 manifest/source。 |"
    execution = hook_execution_text(skill, artifacts)
    execution_section = f"\n\n### 执行机制\n\n{execution}" if execution else ""
    return f"""### 机制盘点

| 来源文件 | 类型 | 为什么要看 |
|---|---|---|
{inventory}
{execution_section}"""


def build_source(book_id: str, title: str, source: Path, files: list[FileInfo], skills: list[SkillInfo]) -> str:
    rows = "\n".join(
        f"| `{f.rel}` | {f.kind} | {f.chars} | {f.bytes} | `{f.sha256[:12]}` |" for f in files
    )
    skill_rows = "\n".join(
        f"| `{s.name}` | {s.group} | `{s.file.rel}` | {s.description[:120]} |" for s in skills
    )
    return f"""# {title} source

## 来源登记

- 材料 id：`{book_id}`
- 类型：Skills 包
- 源路径：`{source}`
- 生成日期：{dt.date.today().isoformat()}
- ReaderLab 处理方式：只读扫描源包，生成中文阅读材料；不移动、不软链、不修改源仓库。

## Skill 分配

| Skill | 阅读单元 | 源文件 | 简介 |
|---|---|---|---|
{skill_rows}

## 全量文件清单

| 文件 | 类型 | 字符数 | 字节数 | sha256 |
|---|---|---:|---:|---|
{rows}
"""


def grouped_skills(skills: list[SkillInfo]) -> dict[str, list[SkillInfo]]:
    groups: dict[str, list[SkillInfo]] = {}
    for skill in skills:
        groups.setdefault(skill.group, []).append(skill)
    return {k: groups[k] for k in sorted(groups)}


def reading_unit_purpose(group: str) -> str:
    if group == STRUCTURE_DIAGNOSIS_UNIT:
        return STRUCTURE_DIAGNOSIS_PURPOSE
    return READING_UNIT_PURPOSES.get(group, "围绕材料自身结构形成的阅读单元。")


def reading_unit_confidence(items: list[SkillInfo]) -> str:
    confidences = {skill.route_confidence for skill in items}
    if "low" in confidences:
        return "low"
    if "medium" in confidences:
        return "medium"
    return "high"


def reading_unit_status(items: list[SkillInfo]) -> str:
    statuses = {skill.structure_status for skill in items}
    if "diagnostic" in statuses:
        return "diagnostic"
    if "explainable" in statuses:
        return "explainable"
    return "clear"


def reading_unit_basis(items: list[SkillInfo]) -> list[str]:
    basis = sorted({item for skill in items for item in skill.route_basis})
    return basis or ["结构诊断"]


def reading_unit_reason(group: str, items: list[SkillInfo]) -> str:
    if group == STRUCTURE_DIAGNOSIS_UNIT:
        return "这些材料读完入口、正文和支持文件后仍不能形成稳定阅读路线，ReaderLab 不把它们硬塞进其他单元。"
    purpose = reading_unit_purpose(group)
    confidence = reading_unit_confidence(items)
    if confidence == "high":
        return f"{purpose} 组内材料的入口说明、正文职责或支持文件指向一致。"
    return f"{purpose} 组内材料可以解释为同一阅读任务，但仍保留争议点供后续人工验收阅读路线。"


def structure_diagnosis(skills: list[SkillInfo]) -> dict[str, Any]:
    diagnostic = [skill for skill in skills if skill.structure_status == "diagnostic"]
    return {
        "status": "diagnostic" if diagnostic else "clear",
        "diagnostic_skills": [skill.name for skill in diagnostic],
        "diagnostic_count": len(diagnostic),
        "rule": "ReaderLab 不让人替机器分组；读完整体结构仍不清楚时，记录材料结构诊断并暂缓硬塞目录。",
        "reasons": [
            {
                "skill": skill.name,
                "reason": skill.route_reason,
                "basis": list(skill.route_basis),
            }
            for skill in diagnostic
        ],
    }


def route_line(skills_by_name: dict[str, SkillInfo], label: str, names: list[str], note: str) -> str:
    existing = [name for name in names if name in skills_by_name]
    if len(existing) < 2:
        return ""
    route = " → ".join(f"[[{skill_reading_filename(skills_by_name[name]).removesuffix('.md')}]]" for name in existing)
    return f"- **{label}**：{route}。{note}"


def build_task_routes(skills: list[SkillInfo]) -> str:
    skills_by_name = {skill.name: skill for skill in skills}
    routes = [
        route_line(
            skills_by_name,
            "先理解工具箱",
            ["dbs", "dbs-diagnosis", "dbs-save", "dbs-report"],
            "先看总入口和诊断框架，再看如何留档和汇总。",
        ),
        route_line(
            skills_by_name,
            "商业诊断与行动",
            ["dbs", "dbs-diagnosis", "dbs-benchmark", "dbs-action", "dbs-decision"],
            "适合从商业问题、对标、执行阻力走到长期决策记录。",
        ),
        route_line(
            skills_by_name,
            "问题澄清与目标落地",
            ["dbs-goal", "dbs-good-question", "dbs-deconstruct", "dbs-decision"],
            "适合先把模糊目标、伪概念和不可解问题改成可判断任务。",
        ),
        route_line(
            skills_by_name,
            "内容生产与发布",
            ["dbs-content", "dbs-hook", "dbs-xhs-title", "dbs-resonate", "dbs-spread", "dbs-wechat-html"],
            "适合从选题和表达诊断，走到开头、标题、共鸣、传播和公众号排版。",
        ),
        route_line(
            skills_by_name,
            "内容资产工程化",
            ["dbs-content-system", "dbs-content", "dbs-decision"],
            "适合把大量素材变成可追溯、可重组、可持续维护的内容工程。",
        ),
        route_line(
            skills_by_name,
            "多角色讨论",
            ["dbs-chatroom", "dbs-chatroom-austrian", "dbs-content"],
            "适合先做多视角碰撞，再把可用观点转入内容或诊断。",
        ),
        route_line(
            skills_by_name,
            "Agent 工作台迁移",
            ["dbs-agent-migration", "dbs-save", "dbs-report"],
            "适合先理解三端迁移，再保存迁移结论并形成报告。",
        ),
    ]
    rendered = [route for route in routes if route]
    if not rendered:
        return ""
    return "## 按任务读\n\n" + "\n".join(rendered) + "\n\n"


def build_start(book_id: str, title: str, goal: str, skills: list[SkillInfo]) -> str:
    task_routes = build_task_routes(skills)
    return f"""# {title}

这是 ReaderLab v0.1 生成的本地阅读包。它把 `{book_id}` 当作一本可以阅读、批注、讨论和沉淀的书，而不是把源仓库复制成另一个仓库。

## 推荐读法

1. 先读 `01_轻量拆解手册.md`，看这份材料被切成哪些阅读单元。
2. 从 `04_主控清单.md` 选择阅读路线；已生成的正文页可以直接从 `10_中文精读/` 连续阅读。
3. 读正文时优先看每组 `00_本组导读.md`，再进入组内 Skill 页面做 Tandem Comments 批注。
4. `02_试跑记录.md`、`03_验收标准.md` 和 `manifest.json` 用于复核生产状态，不是第一次阅读的前置门槛。
5. 读完并讨论后，再把可复用内容沉淀进 `30_沉淀草稿/`。

{task_routes}
## 这次阅读目标

{goal}

## 边界

- 英文原文不默认塞进阅读页；它只用于覆盖校验。
- 源包不会被 ReaderLab 移动、软链或修改。
- 沉淀草稿不会自动升格为正式 Skill，也不会自动写入 LifeAtlas 的其他区域。
"""


def build_decomposition(title: str, skills: list[SkillInfo]) -> str:
    groups = grouped_skills(skills)
    rows = []
    for group, items in groups.items():
        names = "、".join(f"`{s.name}`" for s in items)
        completed = sum(1 for s in items if manifest_skill_status(skill_coverage_metrics(s)) == "completed")
        mode = f"{completed}/{len(items)} 已完成，按 Skill 完整阅读页推进"
        if group == STRUCTURE_DIAGNOSIS_UNIT:
            mode = f"{completed}/{len(items)} 已完成，结构诊断：不硬塞目录"
        reason = reading_unit_reason(group, items)
        confidence = reading_unit_confidence(items)
        rows.append(f"| {group} | {len(items)} | {names} | {confidence} | {reason} | {mode} |")
    return f"""# {title} 轻量拆解手册

## 这份材料是什么

`{title}` 是一个 Skills 包。它不是单个 Skill，而是一组围绕诊断判断、问题决策、行动推进、内容表达、状态记忆、报告复盘和 Agent 工具迁移的工作流集合。

## 推荐读法

v0.1 先读材料整体结构，再形成阅读路线。对 Skills 包，优先看包入口、路由/总控说明、每个 `SKILL.md` 的正文职责，以及脚本、模板、配置承担的机制职责；文件名和关键词只做最后的辅助线索。

如果机器读完这些线索仍无法形成清晰路线，ReaderLab 记录材料结构诊断，不让用户替机器分组，也不把材料硬塞进看起来整齐但错误的目录。

## 阅读单元列表

| 阅读单元 | Skill 数 | 覆盖范围 | 把握 | 路线理由 | v0.1 处理方式 |
|---|---:|---|---|---|---|
{chr(10).join(rows)}

## 试跑方式

本轮试跑不再把源块当作读者入口，而是为每个 Skill 生成一个目标阅读页。源块、标题、段落、代码块仍会进入 `manifest.json`，只用于后台覆盖校验。

## 哪些单元需要全文翻译

- 所有纳入主控清单的 Skill，其 `SKILL.md` 都应进入 Skill 正文中文化。
- 入口、诊断、决策、行动、内容表达、状态报告和迁移工具类 Skill 优先做完整导读、阅读地图和主体正文。
- 脚本、配置、模板和外部文件先做职责说明；只有当它们解释了核心机制时再进入正文或关联说明。

## 简单验收方式

- 每个 Skill 必须分配到且只分配到一个技能组。
- 每个 Skill 必须有且只有一个目标阅读页。
- 中文精读页以导读、阅读地图、Skill 正文和必要关联说明为主。
- 旧 `highlights` 字段只兼容历史精读产物，不作为生成页面或机器状态的依据。
- `manifest.json` 分别记录源文长度、正文译文长度、导读长度、关联材料长度、标题覆盖、段落覆盖、代码块处理和异常标记。
- Tandem Comments 批注在读完后再进入，不作为初始产物。
"""


def build_acceptance_doc() -> str:
    gates = build_acceptance()["gates"]
    rows = "\n".join(
        f"| `{gate['id']}` | {gate['name']} | {gate['pass_condition']} |"
        for gate in gates
    )
    return f"""# ReaderLab v0.1 验收标准

## 总规则

没达标之前不允许把对应 Skill 标记为完成。ReaderLab 不是按源块交付，而是按“技能组 → Skill 完整阅读页”交付；源块、标题、段落、代码块只做后台覆盖校验。

`validate` 只代表机器验收通过，不代表人工阅读质量已验收。人工验收状态单独记录为 `human_status`。

## 验收门槛

| Gate | 名称 | 通过条件 |
|---|---|---|
{rows}

## 对 Skill 包试跑输出的具体要求

- `04_主控清单.md` 必须列出所有阅读单元、组内 Skill、机器状态、人工状态和入口链接。
- 每个 `SKILL.md` 只属于一个技能组，不能重、不漏。
- 每个 Skill 必须有一个目标中文阅读页。
- 已完成 Skill 的 Skill 正文必须覆盖完整 `SKILL.md`，不能用摘要或导读替代翻译。
- Skill 名、命令、字段、工具名保留英文；解释性文字必须中文化。
- ReaderLab 的导读和关联材料说明不能混进正文译文。
- 技能组状态只能由组内 Skill 状态汇总。
- 整包状态只能由所有技能组状态汇总。

## 机器检查

运行：

```bash
python3 scripts/readerlab.py validate <材料目录>
python3 scripts/readerlab.py validate <材料目录> --require-complete
```

默认检查会输出 Skill、技能组和整包状态，方便局部推进。只有加 `--require-complete` 时，才要求整包全部通过并在未完成时失败。
"""

def human_review_state(book_id: str, skill_name: str) -> dict[str, Any]:
    record = HUMAN_REVIEW_REGISTRY.get((book_id, skill_name))
    if not record:
        return {"human_status": "pending"}
    human_status = record.get("human_status", "pending")
    review = {k: v for k, v in record.items() if k != "human_status"}
    if human_status == "accepted":
        review = {
            **review,
            "previous_human_status": "accepted",
            "reset_reason": "主阅读页结构已改为 main_reading_page_centered，旧版人工验收不能自动继承。",
        }
        return {"human_status": "pending", "human_review": review}
    return {"human_status": human_status, "human_review": review}


def machine_status_label(status: str) -> str:
    return {
        "completed": "机器完成",
        "needs_review": "机器需复核",
        "not_started": "机器未开始",
    }.get(status, status)


def human_status_label(status: str) -> str:
    return {
        "accepted": "人工已验收",
        "pending": "人工待验收",
        "not_required": "无需人工验收",
    }.get(status, status)


def build_master_checklist(book_id: str, skills: list[SkillInfo]) -> str:
    rows: list[str] = []
    for group, items in grouped_skills(skills).items():
        item_metrics = [(skill, skill_coverage_metrics(skill)) for skill in items]
        group_done = sum(1 for _skill, metrics in item_metrics if manifest_skill_status(metrics) == "completed")
        group_accepted = sum(
            1 for skill, _metrics in item_metrics if human_review_state(book_id, skill.name)["human_status"] == "accepted"
        )
        rows.append(
            f"| **{group}** |  | **机器完成 {group_done}/{len(items)}** | **人工已验收 {group_accepted}/{len(items)}** |  |"
        )
        for skill, metrics in item_metrics:
            status = skill_status(metrics)
            machine_status = manifest_skill_status(metrics)
            human_status = human_review_state(book_id, skill.name)["human_status"]
            target = f"10_中文精读/{group}/{skill_reading_filename(skill)}"
            if status == "未完成":
                target_label = f"待生成：`{target}`"
            elif status == "需复核":
                target_label = f"需复核：`{target}` / [[{skill_reading_filename(skill).removesuffix('.md')}]]"
            else:
                target_label = f"[[{skill_reading_filename(skill).removesuffix('.md')}]] (`{target}`)"
            rows.append(
                f"|  | `{skill.name}` | {machine_status_label(machine_status)} | "
                f"{human_status_label(human_status)} | {target_label} |"
            )
    task_routes = build_task_routes(skills)
    return f"""# 主控清单

## 使用方式

这张表是 ReaderLab v0.1 的读者主入口。它只按“技能组 → Skill”展示，不按源块展示。

- `完成`：该 Skill 已有完整中文阅读页，覆盖指标通过。
- `需复核`：已有部分内容或指标偏低，不能算完成。
- `未完成`：只在清单中保留目标路径，不生成占位阅读页。
- `人工待验收`：机器状态不失败，但还没有读者确认阅读质量；不能用 validate 绿灯替代。
- `人工已验收`：指定读者已阅读并认可该页适合继续使用。

{task_routes}
## 清单

| 阅读单元 | Skill | 机器状态 | 人工状态 | 入口链接 |
|---|---|---|---|---|
{chr(10).join(rows)}
"""


def normalize_allowed_tools(value: str) -> str:
    if value == "未声明":
        return "未声明"
    tools = []
    for line in value.splitlines():
        item = line.strip().removeprefix("-").strip()
        if item:
            tools.append(item)
    return "、".join(tools) if tools else value.strip()


def skill_summary_line(skill: SkillInfo) -> str:
    desc = reader_skill_role(skill)
    allowed = normalize_allowed_tools(skill.allowed_tools)
    return f"- `{skill.name}`：{desc} 工具边界：{allowed}。"


def skill_reading_filename(skill: SkillInfo) -> str:
    prefix = f"{GROUP_MVP_ORDER.index(skill.name) + 1:02d}_" if skill.name in GROUP_MVP_ORDER else ""
    return f"{prefix}{slugify(skill.name)}.md"


AGENT_SKILL_READINGS: dict[str, dict[str, str]] = {}
COMPLETED_SKILL_TRANSLATIONS: dict[str, dict[str, str]] = {}

COMPLETED_SKILL_TRANSLATIONS["unfreeze"] = {
    "intro": "这个 Skill 解决的是编辑范围恢复问题：当 `/freeze` 把当前会话限制在某个目录内时，`/unfreeze` 清除冻结边界，让编辑重新允许发生在所有目录。阅读主线是看它如何通过状态文件表达边界，而不是结束会话或卸载 hook。",
    "body": """---
name: unfreeze
version: 0.1.0
description: 清除 `/freeze` 设置的冻结边界，让所有目录重新允许编辑。
triggers:
  - unfreeze edits
  - unlock all directories
  - remove edit restrictions
allowed-tools:
  - Bash
  - Read
---

<!-- 由 SKILL.md.tmpl 自动生成，请不要直接编辑。 -->
<!-- 重新生成命令：bun run gen:skill-docs -->

## 什么时候调用这个 Skill

当你想扩大编辑范围，但不想结束当前会话时使用它。
当用户要求“unfreeze”“unlock edits”“remove freeze”或“allow all edits”时，也使用它。

# /unfreeze：清除冻结边界

移除 `/freeze` 设置的编辑限制，让所有目录都重新允许编辑。

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"unfreeze","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## 清除边界

```bash
eval "$(~/.claude/skills/gstack/bin/gstack-paths)"
STATE_DIR="$GSTACK_STATE_ROOT"
if [ -f "$STATE_DIR/freeze-dir.txt" ]; then
  PREV=$(cat "$STATE_DIR/freeze-dir.txt")
  rm -f "$STATE_DIR/freeze-dir.txt"
  echo "Freeze boundary cleared (was: $PREV). Edits are now allowed everywhere."
else
  echo "No freeze boundary was set."
fi
```

把结果告诉用户。注意，`/freeze` hooks 在本会话里仍然注册着；因为没有状态文件存在，它们会允许所有内容。要重新冻结，请再次运行 `/freeze`。""",
    "related": """- 来源：`unfreeze/SKILL.md.tmpl`
  - 职责：这是 `SKILL.md` 的模板源，当前阅读页的正文来自生成后的 `SKILL.md`。模板说明了这一页由 `bun run gen:skill-docs` 生成，不应直接改生成物。
  - 阅读意义：`unfreeze` 没有单独脚本；它直接通过正文里的 bash 片段删除冻结状态文件。因此关联材料只需要标明模板来源，不需要把模板内容混进 Skill 正文。""",
    "highlights": """> [!important] 重点
> ==清除的是 `/freeze` 设置的编辑限制，让所有目录重新允许编辑。==

旁批（来源：Skill 正文）：这是这个 Skill 解决的问题，不是结束会话，也不是切换项目，而是恢复编辑范围。

> [!important] 重点
> ==`/freeze` hooks 仍然注册，只是没有状态文件时会放行所有编辑。==

旁批（来源：Skill 正文）：这说明 gstack 的冻结机制是“hook + 状态文件”的组合，`unfreeze` 只清掉状态边界，不改 hook 注册。
""",
}

COMPLETED_SKILL_TRANSLATIONS["freeze"] = {
    "intro": "这个 Skill 解决的是编辑范围收窄问题：在调试或改动一个模块时，把 Edit/Write 限制到用户指定目录，防止顺手修到无关文件。阅读主线是看它如何让用户选目录、如何把目录写入状态文件，以及 hook 如何用这个状态文件拦截越界编辑。",
    "body": """---
name: freeze
version: 0.1.0
description: 在当前会话中把文件编辑限制到指定目录。
triggers:
  - freeze edits to directory
  - lock editing scope
  - restrict file changes
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
---
<!-- 由 SKILL.md.tmpl 自动生成，请不要直接编辑。 -->
<!-- 重新生成命令：bun run gen:skill-docs -->

## 什么时候调用这个 Skill

拦截允许路径之外的 Edit 和 Write。调试时用它来避免意外“修复”无关代码，或者在你想把改动范围限制到某个模块时使用。用户要求“freeze”“restrict edits”“only edit this folder”或“lock down edits”时也使用它。

# /freeze：把编辑限制到一个目录

把文件编辑锁定到指定目录。任何指向允许路径之外文件的 Edit 或 Write 操作都会被**阻止**，不只是警告。

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"freeze","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## 设置

询问用户要把编辑限制到哪个目录。使用 AskUserQuestion：

- 问题："Which directory should I restrict edits to? Files outside this path will be blocked from editing."
- 文本输入，不是多选；用户输入一个路径。

用户提供目录路径后：

1. 把它解析为绝对路径：

```bash
FREEZE_DIR=$(cd "<user-provided-path>" 2>/dev/null && pwd)
echo "$FREEZE_DIR"
```

2. 确保末尾有斜杠，并保存到 freeze 状态文件：

```bash
FREEZE_DIR="${FREEZE_DIR%/}/"
eval "$(~/.claude/skills/gstack/bin/gstack-paths)"
STATE_DIR="$GSTACK_STATE_ROOT"
mkdir -p "$STATE_DIR"
echo "$FREEZE_DIR" > "$STATE_DIR/freeze-dir.txt"
echo "Freeze boundary set: $FREEZE_DIR"
```

告诉用户："Edits are now restricted to `<path>/`. Any Edit or Write outside this directory will be blocked. To change the boundary, run `/freeze` again. To remove it, run `/unfreeze` or end the session."

## 工作方式

hook 会从 Edit/Write 工具输入 JSON 中读取 `file_path`，然后检查这个路径是否以 freeze 目录开头。如果不是，它返回 `permissionDecision: "deny"` 来阻止操作。

freeze 边界通过状态文件在会话中持续存在。每次调用 Edit/Write 时，hook 脚本都会读取它。

## 注意事项

- freeze 目录末尾的 `/` 可以避免 `/src` 匹配到 `/src-old`。
- Freeze 只作用于 Edit 和 Write 工具；Read、Bash、Glob、Grep 不受影响。
- 这防止的是意外编辑，不是安全边界；像 `sed` 这样的 Bash 命令仍然可以修改边界之外的文件。
- 要停用它，运行 `/unfreeze` 或结束对话。""",
    "related": """- 来源：`freeze/SKILL.md.tmpl`
  - 职责：`freeze/SKILL.md` 的模板源，说明该 Skill 是由模板生成的，不应直接改生成物。
- 来源：`freeze/bin/check-freeze.sh`
  - 职责：真正执行边界检查的 hook 脚本。它读取 Edit/Write 输入里的目标路径，再读取 `freeze-dir.txt`，决定允许还是拒绝。
  - 阅读意义：`SKILL.md` 负责用户流程和状态写入，`check-freeze.sh` 负责每次工具调用前的强制拦截；两者合起来才构成完整冻结机制。""",
    "highlights": """> [!important] 重点
> ==越界 Edit/Write 会被阻止，不只是警告。==

旁批（来源：Skill 正文）：这把 `/freeze` 和普通“提醒我小心”区分开了；它是硬拦截。

> [!important] 重点
> ==末尾 `/` 防止 `/src` 匹配 `/src-old`。==

旁批（来源：Skill 正文）：这是路径边界判断里容易忽略的细节，直接关系到拦截是否准确。

> [!important] 重点
> ==这不是安全边界，Bash 仍然可能改边界外文件。==

旁批（来源：Skill 正文）：它诚实说明工具层 hook 的边界，避免用户把防误操作机制误解成权限沙箱。""",
}

COMPLETED_SKILL_TRANSLATIONS["careful"] = {
    "intro": "这个 Skill 解决的是破坏性命令风险：它不限制普通编辑，而是在 Bash 执行前识别 `rm -rf`、删库、强推、硬重置等高风险模式，并要求用户确认。阅读主线是看它如何区分危险命令和可接受的清理例外。",
    "body": """---
name: careful
version: 0.1.0
description: 面向破坏性命令的安全护栏。
triggers:
  - be careful
  - warn before destructive
  - safety mode
allowed-tools:
  - Bash
  - Read
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/careful/bin/check-careful.sh"
          statusMessage: "Checking for destructive commands..."
---
<!-- 由 SKILL.md.tmpl 自动生成，请不要直接编辑。 -->
<!-- 重新生成命令：bun run gen:skill-docs -->

## 什么时候调用这个 Skill

在 `rm -rf`、`DROP TABLE`、强制推送、`git reset --hard`、`kubectl delete` 和类似破坏性操作前发出警告。用户可以逐次覆盖警告。接触生产环境、调试线上系统或在共享环境中工作时使用。用户要求“be careful”“safety mode”“prod mode”或“careful mode”时也使用它。

# /careful：破坏性命令护栏

安全模式现在**已激活**。每条 bash 命令在运行前都会检查是否匹配破坏性模式。如果检测到破坏性命令，你会收到警告，并可以选择继续或取消。

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"careful","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## 保护什么

| 模式 | 示例 | 风险 |
|---------|---------|------|
| `rm -rf` / `rm -r` / `rm --recursive` | `rm -rf /var/data` | 递归删除 |
| `DROP TABLE` / `DROP DATABASE` | `DROP TABLE users;` | 数据丢失 |
| `TRUNCATE` | `TRUNCATE orders;` | 数据丢失 |
| `git push --force` / `-f` | `git push -f origin main` | 改写历史 |
| `git reset --hard` | `git reset --hard HEAD~3` | 丢失未提交工作 |
| `git checkout .` / `git restore .` | `git checkout .` | 丢失未提交工作 |
| `kubectl delete` | `kubectl delete pod` | 生产影响 |
| `docker rm -f` / `docker system prune` | `docker system prune -a` | 容器或镜像丢失 |

## 安全例外

这些模式允许直接通过，不发警告：
- `rm -rf node_modules` / `.next` / `dist` / `__pycache__` / `.cache` / `build` / `.turbo` / `coverage`

## 工作方式

hook 从工具输入 JSON 中读取命令，按上面的模式检查。如果匹配，就返回带警告信息的 `permissionDecision: "ask"`。你始终可以覆盖警告并继续。

要停用它，请结束对话或开启一个新对话。Hooks 是会话级的。""",
    "related": """- 来源：`careful/SKILL.md.tmpl`
  - 职责：`careful/SKILL.md` 的模板源，说明生成来源。
- 来源：`careful/bin/check-careful.sh`
  - 职责：在 Bash 工具运行前解析命令并匹配破坏性模式，命中时返回 ask 决策。
  - 阅读意义：`SKILL.md` 告诉用户安全模式的行为和例外，脚本承担实际模式识别。表格里的风险分类应当和脚本规则保持一致。""",
    "highlights": """> [!important] 重点
> ==安全模式检查的是每条 bash 命令，而不是只检查某一次高风险操作。==

旁批（来源：Skill 正文）：这说明 `/careful` 是会话级护栏，不是一次性确认弹窗。

> [!important] 重点
> ==安全例外允许清理构建产物和缓存目录。==

旁批（来源：Skill 正文）：没有这类例外，护栏会把日常开发清理变成高摩擦流程。

> [!important] 重点
> ==命中后返回的是 `ask`，不是直接拒绝。==

旁批（来源：Skill 正文）：它的产品取舍是提醒和确认，而不是替用户禁止所有危险操作。""",
}

COMPLETED_SKILL_TRANSLATIONS["guard"] = {
    "intro": "这个 Skill 是 `/careful` 和 `/freeze` 的组合：既对破坏性 Bash 命令发出确认，又把 Edit/Write 限制在指定目录。阅读主线是看它如何组合两个已有保护，而不是发明第三套安全机制。",
    "body": """---
name: guard
version: 0.1.0
description: 完整安全模式：破坏性命令警告 + 目录级编辑范围限制。
triggers:
  - full safety mode
  - guard against mistakes
  - maximum safety
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/careful/bin/check-careful.sh"
          statusMessage: "Checking for destructive commands..."
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
---
<!-- 由 SKILL.md.tmpl 自动生成，请不要直接编辑。 -->
<!-- 重新生成命令：bun run gen:skill-docs -->

## 什么时候调用这个 Skill

把 `/careful`（在 `rm -rf`、`DROP TABLE`、强制推送等操作前警告）和 `/freeze`（阻止指定目录外的编辑）组合起来。接触生产环境或调试线上系统、需要最高安全级别时使用。用户要求“guard mode”“full safety”“lock it down”或“maximum safety”时也使用它。

# /guard：完整安全模式

同时激活破坏性命令警告和目录级编辑限制。这是 `/careful` + `/freeze` 的单命令组合。

**依赖说明：**这个 Skill 引用了同级 `/careful` 和 `/freeze` Skill 目录下的 hook 脚本。两者都必须已安装；gstack setup 脚本会把它们一起安装。

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"guard","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## 设置

询问用户要把编辑限制到哪个目录。使用 AskUserQuestion：

- 问题："Guard mode: which directory should edits be restricted to? Destructive command warnings are always on. Files outside the chosen path will be blocked from editing."
- 文本输入，不是多选；用户输入一个路径。

用户提供目录路径后：

1. 把它解析为绝对路径：

```bash
FREEZE_DIR=$(cd "<user-provided-path>" 2>/dev/null && pwd)
echo "$FREEZE_DIR"
```

2. 确保末尾有斜杠，并保存到 freeze 状态文件：

```bash
FREEZE_DIR="${FREEZE_DIR%/}/"
eval "$(~/.claude/skills/gstack/bin/gstack-paths)"
STATE_DIR="$GSTACK_STATE_ROOT"
mkdir -p "$STATE_DIR"
echo "$FREEZE_DIR" > "$STATE_DIR/freeze-dir.txt"
echo "Freeze boundary set: $FREEZE_DIR"
```

告诉用户：
- "**Guard mode active.** Two protections are now running:"
- "1. **Destructive command warnings** — rm -rf, DROP TABLE, force-push, etc. will warn before executing (you can override)"
- "2. **Edit boundary** — file edits restricted to `<path>/`. Edits outside this directory are blocked."
- "To remove the edit boundary, run `/unfreeze`. To deactivate everything, end the session."

## 保护什么

完整的破坏性命令模式和安全例外见 `/careful`。
编辑边界如何执行见 `/freeze`。""",
    "related": """- 来源：`guard/SKILL.md.tmpl`
  - 职责：`guard/SKILL.md` 的模板源。
- 来源：`careful/bin/check-careful.sh`
  - 职责：为 guard 的 Bash hook 提供破坏性命令检查。
- 来源：`freeze/bin/check-freeze.sh`
  - 职责：为 guard 的 Edit/Write hook 提供目录边界检查。
  - 阅读意义：`guard` 自己不是新增底层机制，而是把两个已有 hook 组合成一个用户入口。关联材料必须标明跨 Skill 依赖，否则读者会误以为所有逻辑都在 `guard/SKILL.md` 内。""",
    "highlights": """> [!important] 重点
> ==`guard` 是 `/careful` + `/freeze` 的单命令组合。==

旁批（来源：Skill 正文）：这是它的本质定位，适合做组合型 Skill 的阅读样本。

> [!important] 重点
> ==它依赖同级 Skill 目录里的 hook 脚本。==

旁批（来源：Skill 正文）：这个依赖说明很重要，功能完整性不只在当前 `SKILL.md` 里。

> [!important] 重点
> ==关闭编辑边界用 `/unfreeze`，关闭全部保护要结束会话。==

旁批（来源：Skill 正文）：这体现了两个保护层的生命周期不同。""",
}

COMPLETED_SKILL_TRANSLATIONS["gstack-upgrade"] = {
    "intro": "这个 Skill 是本轮的较长流程样本：它负责检测 gstack 是全局 git、局部 git、vendored 还是全局 vendored 安装，然后升级、迁移、清缓存并展示变更。阅读主线是看它如何把“升级”拆成可恢复、可询问、可继续原任务的流程。",
    "body": """---
name: gstack-upgrade
version: 1.1.0
description: 把 gstack 升级到最新版本。
triggers:
  - upgrade gstack
  - update gstack version
  - get latest gstack
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---
<!-- 由 SKILL.md.tmpl 自动生成，请不要直接编辑。 -->
<!-- 重新生成命令：bun run gen:skill-docs -->

## 什么时候调用这个 Skill

检测全局安装和 vendored 安装，运行升级，并展示有什么新变化。用户要求“upgrade gstack”“update gstack”或“get latest version”时使用。

语音触发词： "upgrade the tools", "update the tools", "gee stack upgrade", "g stack upgrade"。

# /gstack-upgrade

把 gstack 升级到最新版本，并展示新增内容。

## 内联升级流程

所有 Skill preamble 在检测到 `UPGRADE_AVAILABLE` 时都会引用这一节。

### 第 1 步：询问用户，或自动升级

首先检查是否启用了自动升级：

```bash
_AUTO=""
[ "${GSTACK_AUTO_UPGRADE:-}" = "1" ] && _AUTO="true"
[ -z "$_AUTO" ] && _AUTO=$(~/.claude/skills/gstack/bin/gstack-config get auto_upgrade 2>/dev/null || true)
echo "AUTO_UPGRADE=$_AUTO"
```

**如果 `AUTO_UPGRADE=true` 或 `AUTO_UPGRADE=1`：**跳过 AskUserQuestion，记录“Auto-upgrading gstack v{old} → v{new}...”，并直接进入第 2 步。如果自动升级中的 `./setup` 失败，就从备份目录恢复，并提醒用户手动重试。

**否则**，使用 AskUserQuestion：
- 问题："gstack **v{new}** is available (you're on v{old}). Upgrade now?"
- 选项：["Yes, upgrade now", "Always keep me up to date", "Not now", "Never ask again"]

选择“Yes, upgrade now”时，进入第 2 步。

选择“Always keep me up to date”时：

```bash
~/.claude/skills/gstack/bin/gstack-config set auto_upgrade true
```

告诉用户自动升级已启用，未来更新会自动安装，然后进入第 2 步。

选择“Not now”时，写入带递增退避的 snooze 状态：第一次 24 小时，第二次 48 小时，第三次及以后 1 周，然后继续当前 Skill，不再提这次升级。

```bash
_SNOOZE_FILE="$HOME/.gstack/update-snoozed"
_REMOTE_VER="{new}"
_CUR_LEVEL=0
if [ -f "$_SNOOZE_FILE" ]; then
  _SNOOZED_VER=$(awk '{print $1}' "$_SNOOZE_FILE")
  if [ "$_SNOOZED_VER" = "$_REMOTE_VER" ]; then
    _CUR_LEVEL=$(awk '{print $2}' "$_SNOOZE_FILE")
    case "$_CUR_LEVEL" in *[!0-9]*) _CUR_LEVEL=0 ;; esac
  fi
fi
_NEW_LEVEL=$((_CUR_LEVEL + 1))
[ "$_NEW_LEVEL" -gt 3 ] && _NEW_LEVEL=3
echo "$_REMOTE_VER $_NEW_LEVEL $(date +%s)" > "$_SNOOZE_FILE"
```

注意：`{new}` 是更新检查输出中的远端版本，需要从结果中替换。告诉用户下一次提醒间隔，并提示可以在 `~/.gstack/config.yaml` 中设置 `auto_upgrade: true`。

选择“Never ask again”时：

```bash
~/.claude/skills/gstack/bin/gstack-config set update_check false
```

告诉用户更新检查已关闭，并给出重新启用命令。然后继续当前 Skill。

### 第 2 步：检测安装类型

```bash
if [ -d "$HOME/.claude/skills/gstack/.git" ]; then
  INSTALL_TYPE="global-git"
  INSTALL_DIR="$HOME/.claude/skills/gstack"
elif [ -d "$HOME/.gstack/repos/gstack/.git" ]; then
  INSTALL_TYPE="global-git"
  INSTALL_DIR="$HOME/.gstack/repos/gstack"
elif [ -d ".claude/skills/gstack/.git" ]; then
  INSTALL_TYPE="local-git"
  INSTALL_DIR=".claude/skills/gstack"
elif [ -d ".agents/skills/gstack/.git" ]; then
  INSTALL_TYPE="local-git"
  INSTALL_DIR=".agents/skills/gstack"
elif [ -d ".claude/skills/gstack" ]; then
  INSTALL_TYPE="vendored"
  INSTALL_DIR=".claude/skills/gstack"
elif [ -d "$HOME/.claude/skills/gstack" ]; then
  INSTALL_TYPE="vendored-global"
  INSTALL_DIR="$HOME/.claude/skills/gstack"
else
  echo "ERROR: gstack not found"
  exit 1
fi
echo "Install type: $INSTALL_TYPE at $INSTALL_DIR"
```

后续步骤会使用这里打印出的安装类型和目录路径。

### 第 3 步：保存旧版本

使用第 2 步输出的安装目录：

```bash
OLD_VERSION=$(cat "$INSTALL_DIR/VERSION" 2>/dev/null || echo "unknown")
```

### 第 4 步：升级

使用第 2 步检测到的安装类型和目录。

**git 安装**（global-git、local-git）：

```bash
cd "$INSTALL_DIR"
STASH_OUTPUT=$(git stash 2>&1)
git fetch origin
git reset --hard origin/main
./setup
```

如果 `$STASH_OUTPUT` 包含 "Saved working directory"，提醒用户本地改动已被 stash，可以在 Skill 目录中运行 `git stash pop` 恢复。

**vendored 安装**（vendored、vendored-global）：

```bash
PARENT=$(dirname "$INSTALL_DIR")
TMP_DIR=$(mktemp -d)
git clone --depth 1 https://github.com/garrytan/gstack.git "$TMP_DIR/gstack"
mv "$INSTALL_DIR" "$INSTALL_DIR.bak"
mv "$TMP_DIR/gstack" "$INSTALL_DIR"
cd "$INSTALL_DIR" && ./setup
rm -rf "$INSTALL_DIR.bak" "$TMP_DIR"
```

### 第 4.5 步：处理本地 vendored 副本

使用第 2 步的安装目录，检查是否还存在本地 vendored 副本，以及 team mode 是否启用：

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
LOCAL_GSTACK=""
if [ -n "$_ROOT" ] && [ -d "$_ROOT/.claude/skills/gstack" ]; then
  _RESOLVED_LOCAL=$(cd "$_ROOT/.claude/skills/gstack" && pwd -P)
  _RESOLVED_PRIMARY=$(cd "$INSTALL_DIR" && pwd -P)
  if [ "$_RESOLVED_LOCAL" != "$_RESOLVED_PRIMARY" ]; then
    LOCAL_GSTACK="$_ROOT/.claude/skills/gstack"
  fi
fi
_TEAM_MODE=$(~/.claude/skills/gstack/bin/gstack-config get team_mode 2>/dev/null || echo "false")
echo "LOCAL_GSTACK=$LOCAL_GSTACK"
echo "TEAM_MODE=$_TEAM_MODE"
```

**如果 `LOCAL_GSTACK` 非空且 `TEAM_MODE` 为 `true`：**移除 vendored 副本。Team mode 使用全局安装作为唯一事实源。

```bash
cd "$_ROOT"
git rm -r --cached .claude/skills/gstack/ 2>/dev/null || true
if ! grep -qF '.claude/skills/gstack/' .gitignore 2>/dev/null; then
  echo '.claude/skills/gstack/' >> .gitignore
fi
rm -rf "$LOCAL_GSTACK"
```

告诉用户已移除 vendored 副本，并提醒准备好后提交 `.gitignore` 改动。

**如果 `LOCAL_GSTACK` 非空且 `TEAM_MODE` 不是 `true`：**从刚升级的主安装复制更新本地副本：

```bash
mv "$LOCAL_GSTACK" "$LOCAL_GSTACK.bak"
cp -Rf "$INSTALL_DIR" "$LOCAL_GSTACK"
rm -rf "$LOCAL_GSTACK/.git"
cd "$LOCAL_GSTACK" && ./setup
rm -rf "$LOCAL_GSTACK.bak"
```

告诉用户本地 vendored 副本也已更新，并提醒准备好后提交 `.claude/skills/gstack/`。

如果 `./setup` 失败，从备份恢复并警告用户：

```bash
rm -rf "$LOCAL_GSTACK"
mv "$LOCAL_GSTACK.bak" "$LOCAL_GSTACK"
```

### 第 4.75 步：运行版本迁移

`./setup` 完成后，运行旧版本到新版本之间的迁移脚本。迁移会处理 `./setup` 单独无法覆盖的状态修复，例如过期配置、孤儿文件和目录结构变化。

```bash
MIGRATIONS_DIR="$INSTALL_DIR/gstack-upgrade/migrations"
if [ -d "$MIGRATIONS_DIR" ]; then
  for migration in $(find "$MIGRATIONS_DIR" -maxdepth 1 -name 'v*.sh' -type f 2>/dev/null | sort -V); do
    # Extract version from filename: v0.15.2.0.sh → 0.15.2.0
    m_ver="$(basename "$migration" .sh | sed 's/^v//')"
    # Run if this migration version is newer than old version
    # (simple string compare works for dotted versions with same segment count)
    if [ "$OLD_VERSION" != "unknown" ] && [ "$(printf '%s\n%s' "$OLD_VERSION" "$m_ver" | sort -V | head -1)" = "$OLD_VERSION" ] && [ "$OLD_VERSION" != "$m_ver" ]; then
      echo "Running migration $m_ver..."
      bash "$migration" || echo "  Warning: migration $m_ver had errors (non-fatal)"
    fi
  done
fi
```

迁移是 `gstack-upgrade/migrations/` 中的幂等 bash 脚本。每个文件命名为 `v{VERSION}.sh`，只在从更旧版本升级时运行。如何新增迁移见 `CONTRIBUTING.md`。

### 第 5 步：写标记并清缓存

```bash
mkdir -p ~/.gstack
echo "$OLD_VERSION" > ~/.gstack/just-upgraded-from
rm -f ~/.gstack/last-update-check
rm -f ~/.gstack/update-snoozed
```

### 第 6 步：展示新增内容

读取 `$INSTALL_DIR/CHANGELOG.md`。找出旧版本到新版本之间的所有版本条目。按主题总结为 5-7 条，不要压倒用户；聚焦用户可见变化，除非内部重构很重要，否则跳过。

格式：

```text
gstack v{new} — upgraded from v{old}!

What's new:
- [bullet 1]
- [bullet 2]
- ...

Happy shipping!
```

### 第 7 步：继续

展示新增内容后，继续用户原本调用的 Skill。升级已经完成，不需要进一步动作。

---

## 单独使用

当直接调用 `/gstack-upgrade`，而不是从 preamble 调用时：

1. 强制执行一次新的更新检查，绕过缓存：

```bash
~/.claude/skills/gstack/bin/gstack-update-check --force 2>/dev/null || \
.claude/skills/gstack/bin/gstack-update-check --force 2>/dev/null || true
```

用输出判断是否有可用升级。

2. 如果输出 `UPGRADE_AVAILABLE <old> <new>`，按上面的第 2-6 步执行。

3. 如果没有输出，说明主安装已是最新；这时检查是否存在过期的本地 vendored 副本。

运行上面的第 2 步 bash 块检测主安装类型和目录，再运行第 4.5 步检测本地 vendored 副本和 team mode。

**如果 `LOCAL_GSTACK` 为空**，告诉用户当前已经是最新版本。

**如果 `LOCAL_GSTACK` 非空且 `TEAM_MODE` 为 `true`：**按第 4.5 步的 team-mode 移除块移除 vendored 副本，并告诉用户全局版本最新、本地过期副本已移除。

**如果 `LOCAL_GSTACK` 非空且 `TEAM_MODE` 不是 `true`**，比较版本：

```bash
PRIMARY_VER=$(cat "$INSTALL_DIR/VERSION" 2>/dev/null || echo "unknown")
LOCAL_VER=$(cat "$LOCAL_GSTACK/VERSION" 2>/dev/null || echo "unknown")
echo "PRIMARY=$PRIMARY_VER LOCAL=$LOCAL_VER"
```

**如果版本不同：**按第 4.5 步的同步块从主安装更新本地副本，并告诉用户从哪个版本更新到哪个版本。

**如果版本相同：**告诉用户已经在最新版本，且全局安装与本地 vendored 副本都已是最新。""",
    "related": """- 来源：`gstack-upgrade/SKILL.md.tmpl`
  - 职责：生成当前 `SKILL.md` 的模板源。
- 来源：`gstack-upgrade/migrations/`
  - 职责：存放版本迁移脚本。`SKILL.md` 没有内嵌具体迁移内容，而是规定如何发现、排序和运行迁移。
- 来源：`CHANGELOG.md`
  - 职责：升级完成后用于提炼用户可见变化。
  - 阅读意义：这个 Skill 的关键不只是“拉最新代码”，而是把升级前询问、安装类型识别、备份恢复、本地副本处理、迁移和变更说明串成一个可恢复流程。""",
    "highlights": """> [!important] 重点
> ==自动升级失败时要从备份恢复，并提示用户手动重试。==

旁批（来源：Skill 正文）：升级流程默认承认失败路径存在，并把恢复动作写进主流程。

> [!important] 重点
> ==安装类型先被明确识别，后续所有步骤都依赖 `INSTALL_TYPE` 和 `INSTALL_DIR`。==

旁批（来源：Skill 正文）：这是流程型 Skill 的关键结构：先把环境事实固定，再分支执行。

> [!important] 重点
> ==升级结束后继续用户原本调用的 Skill。==

旁批（来源：Skill 正文）：这说明升级是内联维护动作，不应该吞掉用户最初的任务。""",
}


def format_highlights(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, list):
        return ""
    rows: list[str] = []
    for item in value:
        if isinstance(item, str):
            text = item.strip()
            if text:
                rows.append(f"> [!important] 重点\n> =={text}==")
            continue
        if not isinstance(item, dict):
            continue
        quote = str(item.get("quote") or item.get("point") or "").strip()
        comment = str(item.get("comment") or item.get("annotation") or "").strip()
        source = str(item.get("source") or "").strip()
        if not quote and not comment:
            continue
        block = "> [!important] 重点"
        if quote:
            block += f"\n> =={quote}=="
        if comment:
            source_text = f"（来源：{source}）" if source else ""
            block += f"\n\n旁批{source_text}：{comment}"
        rows.append(block)
    return "\n\n".join(rows).strip()


def text_field(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = [str(item).strip() for item in value if str(item).strip()]
        return "\n\n".join(parts).strip()
    return ""


def format_evidence(value: Any) -> str:
    if not value:
        return ""
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, dict):
        return ""
    rows: list[str] = []
    source = value.get("skill_md")
    if source:
        rows.append(f"- Skill 正文来源：`{source}`")
    source_sha256 = value.get("skill_md_sha256")
    if source_sha256:
        rows.append(f"- Skill 正文 sha256：`{source_sha256}`")
    coverage = value.get("coverage")
    if coverage:
        rows.append(f"- 覆盖说明：{coverage}")
    for item in value.get("related_sources", []) or []:
        if isinstance(item, str):
            rows.append(f"- 关联来源：`{item}`")
        elif isinstance(item, dict):
            path = str(item.get("path") or "").strip()
            note = str(item.get("note") or "").strip()
            if path:
                rows.append(f"- 关联来源：`{path}`" + (f"：{note}" if note else ""))
    return "\n".join(rows)


def normalize_block_reading(raw: dict[str, Any], path: Path) -> dict[str, Any]:
    skill = str(raw.get("skill") or "").strip()
    if not skill:
        raise ValueError("missing skill")
    blocks = raw.get("blocks")
    if not isinstance(blocks, list):
        raise ValueError("missing blocks")
    translations: list[dict[str, Any]] = []
    body_parts: list[str] = []
    for item in blocks:
        if not isinstance(item, dict):
            continue
        block_id = str(item.get("block_id") or item.get("id") or "").strip()
        source_hash = str(item.get("source_hash") or item.get("sha256") or "").strip()
        status = str(item.get("status") or "").strip() or "translated"
        translation = str(item.get("translation") or item.get("text") or "").strip()
        if not block_id:
            continue
        translations.append(
            {
                "id": block_id,
                "source_hash": source_hash,
                "status": status,
                "translation": translation,
            }
        )
        if translation:
            body_parts.append(translation)
    guide = text_field(raw.get("guide") or raw.get("intro") or "")
    related = text_field(raw.get("related_materials_explanation") or raw.get("related") or "")
    if not guide or not body_parts:
        raise ValueError("missing guide or block translations")
    return {
        "skill": skill,
        "intro": guide,
        "body": "\n\n".join(body_parts),
        "related": related,
        "legacy_highlights": raw.get("highlights") or raw.get("marginalia") or "",
        "source": "agent_block_reading",
        "artifact_path": path.as_posix(),
        "block_reading": True,
        "block_schema": str(raw.get("schema") or ""),
        "block_translations": translations,
    }


def normalize_agent_reading(raw: dict[str, Any], path: Path) -> dict[str, Any]:
    if raw.get("schema") == "readerlab.skill-block-reading.v1":
        return normalize_block_reading(raw, path)
    skill = str(raw.get("skill") or "").strip()
    if not skill:
        raise ValueError("missing skill")
    guide = text_field(raw.get("guide") or raw.get("intro") or "")
    body = text_field(raw.get("skill_body_translation") or raw.get("body") or "")
    related = text_field(raw.get("related_materials_explanation") or raw.get("related") or "")
    if not guide or not body:
        raise ValueError("missing guide or skill_body_translation")
    return {
        "skill": skill,
        "intro": guide,
        "body": body,
        "related": related,
        "legacy_highlights": raw.get("highlights") or raw.get("marginalia") or "",
        "source": "agent_reading",
        "artifact_path": path.as_posix(),
    }


def load_agent_skill_readings(readings_dir: Path, package_id: str) -> dict[str, dict[str, Any]]:
    package_dir = readings_dir / package_id
    if not package_dir.exists():
        return {}
    readings: dict[str, dict[str, str]] = {}
    for path in sorted(package_dir.glob("*.json")):
        try:
            raw = json.loads(read_text(path))
            normalized = normalize_agent_reading(raw, path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            raise SystemExit(f"invalid agent reading artifact: {path}: {exc}") from exc
        expected = path.stem
        if normalized["skill"] != expected:
            raise SystemExit(f"agent reading skill mismatch: {path} declares {normalized['skill']}, expected {expected}")
        readings[normalized["skill"]] = normalized
    return readings


def completed_skill_translation(skill: SkillInfo) -> dict[str, Any] | None:
    return AGENT_SKILL_READINGS.get(skill.name) or COMPLETED_SKILL_TRANSLATIONS.get(skill.name)


def completed_skill_source(skill: SkillInfo) -> str:
    completed = completed_skill_translation(skill)
    if not completed:
        return "none"
    return completed.get("source", "manual_sample")


def sentence_aware_clip(text: str, limit: int) -> str:
    compact = re.sub(r"\s+", " ", strip_md(text)).strip()
    if len(compact) <= limit:
        return compact
    clipped = compact[:limit].rstrip()
    sentence_end = max(clipped.rfind(mark) for mark in "。！？.!?")
    if sentence_end >= max(40, int(limit * 0.55)):
        return clipped[: sentence_end + 1].rstrip()
    soft_break = max(clipped.rfind(mark) for mark in "，；、,; ")
    if soft_break >= max(40, int(limit * 0.6)):
        return clipped[:soft_break].rstrip() + "。"
    return clipped.rstrip("，,；;、：:") + "。"


def first_sentence(text: str, limit: int = 140) -> str:
    compact = re.sub(r"\s+", " ", strip_md(text)).strip()
    if not compact:
        return ""
    match = re.search(r"(.+?[。！？.!?])(?:\s|$)", compact)
    sentence = match.group(1) if match else compact
    return sentence_aware_clip(sentence, limit)


def clean_reader_description(value: str, limit: int = 160) -> str:
    lines = []
    for raw_line in value.splitlines():
        line = raw_line.strip().strip("|").strip()
        if not line:
            continue
        if re.search(r"[\u4e00-\u9fff]", line):
            lines.append(line)
    if not lines:
        for raw_line in value.splitlines():
            line = raw_line.strip().strip("|").strip()
            if line:
                lines.append(line)
                break
    text = re.sub(r"\s+", " ", " ".join(lines)).strip()
    return sentence_aware_clip(text, limit) or "需要阅读正文确认用途。"


def reader_skill_role(skill: SkillInfo) -> str:
    if skill.name in TRIAL_SKILL_DESCRIPTIONS_ZH:
        return TRIAL_SKILL_DESCRIPTIONS_ZH[skill.name]
    completed = completed_skill_translation(skill)
    intro_sentence = first_sentence(completed.get("intro", "")) if completed else ""
    if intro_sentence:
        return intro_sentence
    return clean_reader_description(skill.description)


def ordered_group_skills(skills: list[SkillInfo]) -> list[SkillInfo]:
    trial = [s for s in skills if s.group == TRIAL_UNIT_ID]
    by_name = {s.name: s for s in trial}
    return [by_name[name] for name in GROUP_MVP_ORDER if name in by_name]


def line_offsets(text: str) -> list[int]:
    offsets = [0]
    total = 0
    for line in text.splitlines(keepends=True):
        total += len(line)
        offsets.append(total)
    return offsets


def block_source_hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_skill_block_manifest(
    skill_md: Path,
    *,
    skill_name: str | None = None,
    source_file: str | None = None,
) -> dict[str, Any]:
    text = read_text(skill_md)
    lines = text.splitlines(keepends=True)
    name = skill_name or skill_md.parent.name
    source = source_file or skill_md.name
    blocks: list[dict[str, Any]] = []
    seq = 1

    def add_block(kind: str, start_line: int, end_line: int, title: str = "", heading: str = "") -> None:
        nonlocal seq
        if start_line < 1 or end_line < start_line:
            return
        raw = "".join(lines[start_line - 1 : end_line])
        if not raw.strip():
            return
        block_id = f"{name}-{seq:04d}-{kind.replace('_', '-')}"
        seq += 1
        blocks.append(
            {
                "id": block_id,
                "skill": name,
                "source_file": source,
                "kind": kind,
                "type": kind,
                "title": title or heading or kind,
                "heading": heading,
                "start_line": start_line,
                "end_line": end_line,
                "chars": len(raw),
                "sha256": block_source_hash(raw),
                "source_hash": block_source_hash(raw),
            }
        )

    i = 1
    if lines and lines[0].strip() == "---":
        end = None
        for idx in range(2, len(lines) + 1):
            if lines[idx - 1].strip() == "---":
                end = idx
                break
        if end is not None:
            add_block("frontmatter", 1, end, "文件头信息", "frontmatter")
            i = end + 1

    current_heading = ""
    while i <= len(lines):
        line = lines[i - 1]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith(("```", "~~~")):
            fence = stripped[:3]
            start = i
            i += 1
            while i <= len(lines):
                if lines[i - 1].strip().startswith(fence):
                    break
                i += 1
            end = min(i, len(lines))
            add_block("code_block", start, end, f"代码块：{current_heading or '未命名'}", current_heading)
            i = end + 1
            continue
        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading_match:
            current_heading = strip_md(heading_match.group(2))
            add_block("heading", i, i, current_heading, current_heading)
            i += 1
            continue
        start = i
        while i <= len(lines):
            candidate = lines[i - 1]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if candidate_stripped.startswith(("```", "~~~")):
                break
            if re.match(r"^(#{1,6})\s+(.+?)\s*$", candidate):
                break
            i += 1
        add_block("paragraph", start, i - 1, current_heading or "正文段落", current_heading)
    return {
        "schema": "readerlab.skill-block-manifest.v1",
        "skill": name,
        "source_file": source,
        "source_sha256": block_source_hash(text),
        "blocks": blocks,
    }


def source_blocks_for_skill(skill: SkillInfo) -> list[dict[str, Any]]:
    return build_skill_block_manifest(
        skill.file.path,
        skill_name=skill.name,
        source_file=skill.file.rel,
    )["blocks"]


def source_block_reading_layer(block: dict[str, Any]) -> dict[str, str]:
    kind = str(block.get("kind") or "")
    heading = str(block.get("heading") or block.get("title") or "").lower()
    if kind == "frontmatter":
        return {
            "content_layer": "runtime_shell",
            "reader_visibility": "codex_only",
            "absorption_status": "absorbed",
        }
    if kind == "code_block":
        return {
            "content_layer": "implementation_detail",
            "reader_visibility": "codex_only",
            "absorption_status": "absorbed",
        }
    if any(token in heading for token in ["hook", "tool", "bash", "script", "install", "setup", "配置", "脚本", "工具", "命令"]):
        return {
            "content_layer": "support",
            "reader_visibility": "reader_context",
            "absorption_status": "absorbed",
        }
    return {
        "content_layer": "body",
        "reader_visibility": "main_reading",
        "absorption_status": "included",
    }


def count_markdown_headings(text: str) -> int:
    count = 0
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if in_fence and marker == fence_marker:
                in_fence = False
                fence_marker = ""
            elif not in_fence:
                in_fence = True
                fence_marker = marker
            continue
        if not in_fence and re.match(r"^#{1,6}\s+", line):
            count += 1
    return count


def count_paragraphs(text: str) -> int:
    _fm, body = parse_frontmatter(text)
    chunks = re.split(r"\n\s*\n", body)
    count = 0
    for chunk in chunks:
        clean = chunk.strip()
        if not clean or clean.startswith(("```", "~~~", "<!--")):
            continue
        if re.match(r"^#{1,6}\s+", clean):
            continue
        count += 1
    return count


def count_code_blocks(text: str) -> int:
    return len(re.findall(r"(^|\n)```", text)) // 2 + len(re.findall(r"(^|\n)~~~", text)) // 2


TECHNICAL_ENGLISH_WORDS = {
    "api",
    "artifact",
    "artifacts",
    "askuserquestion",
    "bash",
    "benchmark",
    "block",
    "blocks",
    "branch",
    "checkpoint",
    "claude",
    "codex",
    "config",
    "continuous",
    "dashboard",
    "dry",
    "exitplanmode",
    "false",
    "flag",
    "flags",
    "gbrain",
    "gemini",
    "git",
    "gpt",
    "gstack",
    "headless",
    "inline",
    "judge",
    "json",
    "mode",
    "models",
    "no",
    "noop",
    "path",
    "plan",
    "provider",
    "providers",
    "prompt",
    "prompts",
    "report",
    "review",
    "runbook",
    "skill",
    "skills",
    "status",
    "step",
    "stop",
    "telemetry",
    "token",
    "true",
    "user",
    "yes",
}


def remove_markdown_code_spans(text: str) -> str:
    return re.sub(r"`[^`]*`", " ", text)


SHORT_ENGLISH_INSTRUCTION_RE = re.compile(
    r"(?:^|[\n.!?]\s*)"
    r"(?:[-*>]\s*)?"
    r"(?:If|Only|Append|Ask|Check|Offer|Show|Print|Run|Use|Do not|Don't|Sure)\b"
)

CODE_COMMENT_COMMAND_RE = re.compile(
    r"^(?:"
    r"cd|cp|curl|do|done|echo|export|fi|for|git|if|ln|mkdir|mv|npm|pnpm|python3?|"
    r"rm|set|shellcheck|then|while"
    r")\b"
)


def english_nontechnical_words(text: str) -> list[str]:
    return [
        word.lower()
        for word in re.findall(r"\b[A-Za-z][A-Za-z'-]{3,}\b", text)
        if word.lower() not in TECHNICAL_ENGLISH_WORDS
    ]


def has_short_english_instruction_residue(visible: str) -> bool:
    english_words = english_nontechnical_words(visible)
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", visible))
    if SHORT_ENGLISH_INSTRUCTION_RE.search(visible):
        return bool(english_words) and len(english_words) * 3 > max(chinese_chars, 1)
    instruction_starts = re.findall(
        r"(?:^|[\n.!?]\s*)(?:If|Only|Append|Ask|Check|Offer|Show|Print|Run|Use|Do not|Don't|Sure)\b",
        visible,
    )
    return len(instruction_starts) >= 2 and len(english_words) >= 4 and chinese_chars < 12


def code_comment_has_english_residue(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("# "):
        return False
    comment = stripped[2:].strip()
    if not comment or re.search(r"[\u4e00-\u9fff]", comment):
        return False
    if CODE_COMMENT_COMMAND_RE.match(comment):
        return False
    if re.search(r"[/$=]", comment):
        return False
    words = english_nontechnical_words(comment)
    if len(words) <= 2 and len(comment) <= 32:
        return False
    return len(words) >= 4


def translation_quality_issues(block: dict[str, Any], translation: str) -> list[str]:
    issues: list[str] = []
    block_id = str(block.get("id") or "")
    kind = block.get("kind")
    if "中文译文：" in translation:
        issues.append(f"translation_marker_residue:{block_id}")
    if kind == "code_block":
        if any(code_comment_has_english_residue(line) for line in translation.splitlines()):
            issues.append(f"code_comment_english_residue:{block_id}")
        return issues
    if kind == "frontmatter":
        return issues
    visible = remove_markdown_code_spans(translation)
    english_words = english_nontechnical_words(visible)
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", visible))
    if len(english_words) >= 18 and len(english_words) * 4 > max(chinese_chars, 1):
        issues.append(f"english_sentence_residue:{block_id}")
    if has_short_english_instruction_residue(visible):
        issues.append(f"short_english_residue:{block_id}")
    return issues


def block_translation_issues(skill: SkillInfo, completed: dict[str, Any] | None) -> list[str]:
    if not completed or not completed.get("block_reading"):
        return []
    expected = source_blocks_for_skill(skill)
    submitted = {
        str(item.get("id")): item
        for item in completed.get("block_translations", [])
        if isinstance(item, dict) and item.get("id")
    }
    issues: list[str] = []
    for block in expected:
        block_id = block["id"]
        item = submitted.get(block_id)
        if not item:
            issues.append(f"missing_block:{block_id}")
            continue
        if item.get("source_hash") != block.get("source_hash"):
            issues.append(f"source_hash_mismatch:{block_id}")
        if item.get("status") not in {"translated", "completed"}:
            issues.append(f"block_not_translated:{block_id}")
        translation = str(item.get("translation") or "").strip()
        if not translation:
            issues.append(f"empty_block_translation:{block_id}")
        else:
            issues.extend(translation_quality_issues(block, translation))
    expected_ids = {block["id"] for block in expected}
    for block_id in sorted(set(submitted) - expected_ids):
        issues.append(f"extra_block:{block_id}")
    return issues


def skill_coverage_metrics(skill: SkillInfo, files: list[FileInfo] | None = None) -> dict[str, Any]:
    source_text = read_text(skill.file.path)
    completed = completed_skill_translation(skill)
    translation = completed["body"] if completed else ""
    guide = completed["intro"] if completed else ""
    manual_related = completed.get("related", "") if completed else ""
    auto_related = build_auto_related_materials(skill, files) if files is not None else ""
    related = "\n\n".join(part for part in [manual_related, auto_related] if part)
    artifacts = discover_skill_artifacts(skill, files) if files is not None else []
    source_headings = count_markdown_headings(source_text)
    translated_headings = count_markdown_headings(translation)
    source_paragraphs = count_paragraphs(source_text)
    translated_paragraphs = count_paragraphs(translation)
    source_code_blocks = count_code_blocks(source_text)
    translated_code_blocks = count_code_blocks(translation)
    expected_blocks = source_blocks_for_skill(skill)
    block_issues = block_translation_issues(skill, completed)
    source_chars = skill.file.chars
    translated_body_chars = len(translation)
    ratio = round(translated_body_chars / source_chars, 3) if source_chars else 0
    flags: list[str] = []
    if not completed:
        flags.append("full_translation_pending")
    if completed and translated_headings < source_headings:
        flags.append("heading_coverage_incomplete")
    if completed and translated_paragraphs < max(1, int(source_paragraphs * 0.7)):
        flags.append("paragraph_coverage_low")
    if completed and translated_code_blocks < source_code_blocks:
        flags.append("code_blocks_not_preserved")
    if block_issues:
        flags.append("block_translation_incomplete")
    return {
        "source_chars": source_chars,
        "translated_body_chars": translated_body_chars,
        "reading_source": completed_skill_source(skill),
        "reading_artifact": completed.get("artifact_path", "") if completed else "",
        "guide_chars": len(guide),
        "related_chars": len(related),
        "related_artifacts_count": len(artifacts),
        "has_frontmatter_explanation": bool(completed and "description:" in translation),
        "has_execution_mechanism": bool(auto_related),
        "hook_references_resolved": not str(skill.frontmatter.get("hooks") or "").strip()
        or any(artifact_category(f.rel) == "脚本入口" for f in artifacts),
        "translation_ratio": ratio,
        "source_headings": source_headings,
        "translated_headings": translated_headings,
        "heading_coverage": source_headings == 0 or translated_headings >= source_headings,
        "source_paragraphs": source_paragraphs,
        "translated_paragraphs": translated_paragraphs,
        "paragraph_coverage": source_paragraphs == 0 or translated_paragraphs >= max(1, int(source_paragraphs * 0.7)),
        "source_code_blocks": source_code_blocks,
        "translated_code_blocks": translated_code_blocks,
        "code_blocks_handled": translated_code_blocks >= source_code_blocks,
        "source_blocks": len(expected_blocks),
        "translated_blocks": len(completed.get("block_translations", [])) if completed and completed.get("block_reading") else 0,
        "block_reading": bool(completed and completed.get("block_reading")),
        "block_coverage": bool(completed and completed.get("block_reading")) and not block_issues,
        "block_issues": block_issues,
        "flags": flags,
    }


def build_codex_absorption_record(skill: SkillInfo, files: list[FileInfo], status: str) -> dict[str, Any]:
    completed = completed_skill_translation(skill)
    artifacts = discover_skill_artifacts(skill, files)
    block_layers = [source_block_reading_layer(block) for block in source_blocks_for_skill(skill)]
    absorbed_blocks = sum(1 for layer in block_layers if layer["absorption_status"] in {"absorbed", "trace_only"})
    included_blocks = sum(1 for layer in block_layers if layer["absorption_status"] == "included")
    artifact_refs = [
        {
            "path": artifact.rel,
            "kind": artifact_category(artifact.rel),
            "role": artifact_role(artifact.rel),
            "absorption_status": "absorbed",
        }
        for artifact in artifacts
    ]
    if status in {"completed", "needs_review"}:
        absorption_status = "absorbed"
    elif artifacts or completed:
        absorption_status = "pending"
    else:
        absorption_status = "not_started"
    return {
        "schema": "readerlab.codex-absorption.v1",
        "status": absorption_status,
        "design_notes": (
            "主阅读页保留用途、触发场景、核心流程、判断标准、约束、失败条件和输出契约；"
            "非正文运行外壳由 Codex 吸收后用于解释机制边界。"
        ),
        "mechanism_boundaries": (
            "frontmatter、工具限制、hooks、脚本、模板、测试、目录结构、验证方式和失败处理不默认展开成读者页面；"
            "只有影响理解主线时才进入主阅读页的关联说明。"
        ),
        "transferable_lessons": [
            "先把一手主体和运行外壳分层，再决定哪些内容给人读、哪些内容给 Codex 吸收。",
            "保留追溯来源，但不把源块、行号、hash 和覆盖统计暴露在第一次阅读页。",
        ],
        "source_refs": [{"path": skill.file.rel, "role": "primary_skill_body"}] + artifact_refs,
        "non_body_materials": artifact_refs,
        "source_block_absorption": {
            "included_in_main_reading": included_blocks,
            "absorbed_for_codex": absorbed_blocks,
            "total": len(block_layers),
        },
    }


def skill_status(metrics: dict[str, Any]) -> str:
    if not metrics["translated_body_chars"]:
        return "未完成"
    if not metrics["guide_chars"]:
        return "需复核"
    if metrics["flags"]:
        return "需复核"
    return "完成"


def manifest_skill_status(metrics: dict[str, Any]) -> str:
    status = skill_status(metrics)
    return {"完成": "completed", "需复核": "needs_review", "未完成": "not_started"}[status]


def group_status(skill_records: list[dict[str, Any]]) -> str:
    if all(s["status"] == "completed" for s in skill_records):
        return "completed"
    if any(s["status"] in {"completed", "needs_review"} for s in skill_records):
        return "in_progress"
    return "not_started"


def build_group_intro(book_id: str, group: str, items: list[SkillInfo]) -> str:
    item_metrics = [(skill, skill_coverage_metrics(skill)) for skill in items]
    completed = sum(1 for _skill, metrics in item_metrics if manifest_skill_status(metrics) == "completed")
    accepted = sum(
        1 for skill, _metrics in item_metrics if human_review_state(book_id, skill.name)["human_status"] == "accepted"
    )
    row_items = []
    for i, (skill, metrics) in enumerate(item_metrics, 1):
        status = skill_status(metrics)
        machine_status = manifest_skill_status(metrics)
        human_status = human_review_state(book_id, skill.name)["human_status"]
        target = f"[[{skill_reading_filename(skill).removesuffix('.md')}]]" if status in {"完成", "需复核"} else "待生成"
        row_items.append(
            f"| {i:02d} | {target} | `{skill.name}` | {reader_skill_role(skill)} | "
            f"{machine_status_label(machine_status)} | {human_status_label(human_status)} |"
        )
    rows = "\n".join(
        row_items
    )
    return f"""# {group}

## 章前导读

这一组包含 {len(items)} 个 Skill，当前机器完成 {completed}/{len(items)}，人工已验收 {accepted}/{len(items)}。validate 只代表机器验收，不能替代人工阅读质量判断。

## 阅读路线判断

- 这一组解决的问题：{reading_unit_purpose(group)}
- 为什么这样分：{reading_unit_reason(group, items)}
- 判断依据：{"、".join(reading_unit_basis(items))}
- 把握程度：{reading_unit_confidence(items)}

## 中文精读页

| 顺序 | 目标阅读页 | Skill | 本页要解决的问题 | 机器状态 | 人工验收 |
|---:|---|---|---|---|---|
{rows}

正式中文精读页必须逐个 Skill 生成，并且以主阅读页为中心：导读、阅读地图、正文和必要关联说明服务第一次阅读。机制和证据默认留在 manifest/source 追溯层，不生成镜像目录。未完成 Skill 不生成占位页，避免把“待生成”误当成可读正文。

## 阅读注意

这一页只说明本组进度，不替代具体 Skill 的机制拆解。真正值得学习的写法、hook 链路、脚本职责和输出契约，必须进入各 Skill 自己的中文精读页。
"""


def demote_markdown_headings(text: str, levels: int = 2) -> str:
    lines: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            lines.append(line)
            continue
        if not in_fence:
            match = re.match(r"^(#{1,6})(\s+.+)$", line)
            if match:
                hashes, rest = match.groups()
                lines.append("#" * min(6, len(hashes) + levels) + rest)
                continue
        lines.append(line)
    trailing_newline = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + trailing_newline


def strip_reader_hidden_related_sections(text: str) -> str:
    if not text:
        return ""
    lines = text.splitlines()
    kept: list[str] = []
    section: list[str] = []

    def flush() -> None:
        nonlocal section
        if not section:
            return
        section_text = "\n".join(section)
        heading = section[0].strip()
        hidden_heading = re.match(r"^#{2,6}\s+(内容分层)\s*$", heading)
        hidden_body = re.search(
            r"source_hash|block id|源块|内部源块|覆盖校验|后台校验|无额外材料|没有声明 hooks，也没有发现脚本入口",
            section_text,
            re.I,
        )
        if not hidden_heading and not hidden_body:
            kept.extend(section)
        section = []

    for line in lines:
        if re.match(r"^#{2,6}\s+", line):
            flush()
        section.append(line)
    flush()
    return "\n".join(kept).strip()


def strip_frontmatter_block(text: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[idx + 1 :]).lstrip()
    return text


def strip_html_comments(text: str) -> str:
    return re.sub(r"(?s)<!--.*?-->\n?", "", text).strip()


def strip_generated_preamble(text: str, skill_name: str) -> str:
    lines = text.splitlines()
    start: int | None = None
    end: int | None = None
    workflow_heading = re.compile(rf"^#{{1,6}}\s+/?{re.escape(skill_name)}(?:\b|[：:])")
    plan_footer_seen = False
    for idx, line in enumerate(lines):
        if re.match(r"^#{1,6}\s+(?:预处理脚本|Preamble)", line, re.I):
            start = idx
            continue
        if start is None:
            continue
        if workflow_heading.match(line):
            end = idx
            break
        if re.match(r"^#{1,6}\s+(?:Plan\s+状态页脚|计划\s*状态页脚)", line):
            plan_footer_seen = True
            continue
        if plan_footer_seen and re.match(r"^#{1,6}\s+", line):
            end = idx
            break
    if start is None or end is None or end <= start:
        return text
    return "\n".join(lines[:start] + lines[end:]).strip()


def strip_reader_hidden_code_blocks(text: str) -> str:
    lines = text.splitlines()
    kept: list[str] = []
    block: list[str] = []
    in_fence = False
    fence_marker = ""

    def should_hide_code_block(code: str) -> bool:
        return any(
            token in code
            for token in (
                ".gstack/analytics",
                "skill-usage.jsonl",
                "gstack-timeline-log",
                "TELEMETRY:",
            )
        )

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
                block = [line]
                continue
            if marker == fence_marker:
                block.append(line)
                code = "\n".join(block)
                if not should_hide_code_block(code):
                    kept.extend(block)
                block = []
                in_fence = False
                fence_marker = ""
                continue
        if in_fence:
            block.append(line)
        else:
            kept.append(line)
    if block:
        kept.extend(block)
    return "\n".join(kept).strip()


def reader_visible_body(text: str, skill: SkillInfo) -> str:
    text = strip_frontmatter_block(text)
    text = strip_html_comments(text)
    text = strip_generated_preamble(text, skill.name)
    text = strip_reader_hidden_code_blocks(text)
    return text.strip()


def build_reading_map(skill: SkillInfo, group_items: list[SkillInfo]) -> str:
    ordered = group_items or [skill]
    names = [item.name for item in ordered]
    try:
        index = names.index(skill.name)
    except ValueError:
        index = 0
    previous_skill = ordered[index - 1] if index > 0 else None
    next_skill = ordered[index + 1] if index + 1 < len(ordered) else None
    previous_text = f"`{previous_skill.name}`" if previous_skill else "无，当前页是本组第一篇"
    next_text = f"`{next_skill.name}`" if next_skill else "无，当前页是本组最后一篇"
    route = " → ".join(f"`{item.name}`" for item in ordered[:8])
    if len(ordered) > 8:
        route += " → ..."
    if skill.structure_status == "diagnostic" or skill.group == STRUCTURE_DIAGNOSIS_UNIT:
        return (
            f"本页属于 `{STRUCTURE_DIAGNOSIS_UNIT}`，不是普通完成阅读页。ReaderLab 目前只能确认它在材料结构中存在，"
            "但入口职责、阅读价值或上下游关系还不足以稳定归入其他阅读单元。\n\n"
            f"- 结构判断：{skill.route_reason}\n"
            f"- 判断依据：{'、'.join(skill.route_basis)}\n"
            "- 阅读路线：先把它当作结构诊断项检查，不把它当作已经整理好的正文单元。"
        )
    return (
        f"本页位于 `{skill.group}`，这个阅读单元的作用是：{reading_unit_purpose(skill.group)}\n\n"
        f"- 单元内位置：第 {index + 1}/{len(ordered)} 个。\n"
        f"- 组内前一页：{previous_text}。\n"
        f"- 组内后一页：{next_text}。\n"
        f"- 本组浏览顺序：{route}。\n"
        "- 常见进入方式：先从包入口、总控页或本组导读判断当前任务是否落在这一页；不要把组内顺序误读成业务流程。\n"
        "- 常见后续：按本页结论回到包入口或总控页选择下一步，或进入同组相邻页做专项补充。\n"
        f"- 本页职责：{reader_skill_role(skill)}"
    )


def build_skill_translation_task_page(
    skill: SkillInfo,
    files: list[FileInfo] | None = None,
    group_items: list[SkillInfo] | None = None,
) -> str:
    completed = completed_skill_translation(skill)
    files = files or []
    group_items = group_items or [skill]
    metrics = skill_coverage_metrics(skill, files)
    status = skill_status(metrics)
    if skill.structure_status == "diagnostic" or skill.group == STRUCTURE_DIAGNOSIS_UNIT:
        title = f"{skill.name}：材料结构诊断页"
    elif status == "完成":
        title = f"{skill.name}：完整中文阅读页"
    elif status == "需复核":
        title = f"{skill.name}：需复核中文阅读页"
    else:
        title = f"{skill.name}：待生成中文精读"
    tools = normalize_allowed_tools(skill.allowed_tools)
    triggers = skill.frontmatter.get("triggers", "")
    if isinstance(triggers, str):
        trigger_text = triggers.replace("\n", "、").replace("- ", "").strip() or "原文未单独声明。"
    else:
        trigger_text = "原文未单独声明。"
    zh_description = reader_skill_role(skill)
    body = (
        demote_markdown_headings(reader_visible_body(completed["body"], skill))
        if completed
        else "> [!warning] 待生成\n> 这里必须替换为完整中文译文。不得用摘要、概括、临时导读或源块状态替代原文翻译。"
    )
    intro = completed["intro"] if completed else f"这个 Skill 的初步用途：{zh_description} 正式交付前必须补齐完整中文译文和覆盖指标。"
    intro = f"{intro}\n\n{skill_terms_hint(skill, files)}"
    manual_related = completed.get("related", "") if completed else ""
    auto_related = build_auto_related_materials(skill, files)
    related = strip_reader_hidden_related_sections(
        "\n\n".join(part for part in [manual_related, auto_related] if part)
    )
    related_section = f"\n## 关联说明\n\n{related}\n" if related else ""
    return f"""# {title}

## 短导读

{intro}

## 阅读地图

{build_reading_map(skill, group_items)}

## Skill 正文

{body}
{related_section}

"""


def skill_support_stem(skill: SkillInfo, suffix: str) -> str:
    stem = Path(skill_reading_filename(skill)).with_suffix("").name
    return f"{stem}-{suffix}.md"


def skill_mechanism_page_path(skill: SkillInfo) -> str:
    return f"11_机制说明/{skill.group}/{skill_support_stem(skill, '机制说明')}"


def skill_evidence_page_path(skill: SkillInfo) -> str:
    return f"12_证据附录/{skill.group}/{skill_support_stem(skill, '证据附录')}"


def build_skill_mechanism_page(skill: SkillInfo, files: list[FileInfo]) -> str:
    completed = completed_skill_translation(skill)
    manual_related = completed.get("related", "") if completed else "没有已生成的人工关联材料说明。"
    auto_related = build_auto_related_materials(skill, files)
    related = "\n\n".join(part for part in [manual_related, auto_related] if part)
    main_page = f"../../10_中文精读/{skill.group}/{skill_reading_filename(skill)}"
    evidence_page = f"../../{skill_evidence_page_path(skill)}"
    return f"""# {skill.name}：机制说明

## 阅读边界

本页只解释支撑理解的机制材料：脚本、模板、hook、配置、迁移文件、执行流程和关联说明。第一次阅读主线回到 [{skill.name} 主阅读页]({main_page})。

## 关联材料与机制说明

{related}

## 相邻页面

- 主阅读页：[{skill.name}]({main_page})
- 证据附录：[{skill.name} 证据附录]({evidence_page})
"""


def build_skill_evidence_page(book_id: str, skill: SkillInfo, files: list[FileInfo]) -> str:
    completed = completed_skill_translation(skill)
    metrics = skill_coverage_metrics(skill, files)
    artifacts = discover_skill_artifacts(skill, files)
    main_page = f"../../10_中文精读/{skill.group}/{skill_reading_filename(skill)}"
    mechanism_page = f"../../{skill_mechanism_page_path(skill)}"
    artifact_rows = "\n".join(
        f"| `{artifact.rel}` | {artifact_category(artifact.rel)} | {artifact_role(artifact.rel)} |"
        for artifact in artifacts
    ) or "| 无 | 无额外材料 | 当前扫描未发现直接关联材料。 |"
    reading_artifact = (completed or {}).get("artifact_path", "")
    block_count = len(source_blocks_for_skill(skill))
    status = manifest_skill_status(metrics)
    human_state = human_review_state(book_id, skill.name)["human_status"]
    return f"""# {skill.name}：证据附录

## 页面关系

- 主阅读页：[{skill.name}]({main_page})
- 机制说明：[{skill.name} 机制说明]({mechanism_page})

## 源文件

- 路径：`{skill.file.rel}`
- 精读产物：`{reading_artifact or '无'}`

## 验收状态

- 机器状态：`{status}`
- 人工状态：`{human_state}`
- validate 含义：只代表机器覆盖和结构验收，不代表人工阅读质量已经通过。

## 读者可用证据

- 正文覆盖：已生成中文正文、导读、重点和机制说明。
- 标题覆盖：{metrics['translated_headings']}/{metrics['source_headings']}。
- 段落覆盖：{metrics['translated_paragraphs']}/{metrics['source_paragraphs']}。
- 代码块处理：{metrics['translated_code_blocks']}/{metrics['source_code_blocks']}。
- 机制说明：{"已发现并单独展示关联机制材料" if metrics["has_execution_mechanism"] else "当前未发现需要单独解释的脚本、模板或 hook"}。

## 关联文件清单

| 文件 | 类型 | 说明 |
|---|---|---|
{artifact_rows}

## 机器校验数据在哪里

源块 ID、行号、hash 和完整源文件是 ReaderLab 内部校验数据，不要求读者人工处理。本页只保留读者判断阅读质量需要的信息；完整机器数据保留在 `manifest.json` 和 `source.md`。

- 内部源块数量：{block_count}
"""


def build_reading_pages(book_id: str, skills: list[SkillInfo], files: list[FileInfo]) -> dict[str, str]:
    pages: dict[str, str] = {}
    for group, items in grouped_skills(skills).items():
        pages[f"{group}/00_本组导读.md"] = build_group_intro(book_id, group, items)
        for skill in items:
            if completed_skill_translation(skill):
                pages[f"{group}/{skill_reading_filename(skill)}"] = build_skill_translation_task_page(skill, files, items)
    return pages


def build_support_pages(book_id: str, skills: list[SkillInfo], files: list[FileInfo]) -> dict[str, str]:
    return {}


def build_trial_record(book_id: str, unit_path: str, skills: list[SkillInfo]) -> str:
    completed = sum(1 for s in skills if manifest_skill_status(skill_coverage_metrics(s)) == "completed")
    accepted = sum(1 for s in skills if human_review_state(book_id, s.name)["human_status"] == "accepted")
    return f"""# 试跑记录

## 本次处理状态

- 试跑入口：`{unit_path}`
- 单元类型：Skills 包
- 覆盖 Skill 数：{len(skills)}
- 输出结构：拆解手册 + 主控清单 + 技能组 + 每个 Skill 一个完整阅读页目标
- 当前机器状态：{completed}/{len(skills)} 个 Skill 已完成完整阅读页
- 当前人工验收：{accepted}/{len(skills)} 个 Skill 已人工验收

## 为什么不能算完成

ReaderLab v0.1 的验收目标不是“看起来有一组文件”，而是让读者能通过中文正文读懂每个完整 Skill。源块、标题、段落、代码块只用于后台校验，不能作为读者主入口。

机器完成只说明结构、覆盖和质量门通过；人工验收需要读者另行确认，不能由 validator 绿灯替代。

## 验收门槛

- 每个已完成 Skill 都有完整中文正文，不用摘要替代翻译。
- ReaderLab 解读和原文翻译分层清楚。
- 译文覆盖标题、段落和代码块；代码块要么保留，要么有中文用途说明。
- 页面默认不生成 `重点与亮点`；阅读辅助由导读、阅读地图和必要关联说明承担。
- `python3 scripts/readerlab.py validate <材料目录>` 返回当前进度。
- `python3 scripts/readerlab.py validate <材料目录> --require-complete` 才是整包强验收。

## 后续动作

读者在 `10_中文精读/` 中批注后，AI 再读取 Tandem Comments 线程并回复。需要长讨论时，讨论稿进入 `20_批注与讨论/`。
"""


def build_distillation_placeholders() -> dict[str, str]:
    return {
        "书中精华.md": "# 书中精华\n\n读完并完成批注讨论后再写。这里借鉴仓颉方法：先理解材料，再抽框架、原则、案例、反例和术语，不直接生成正式 Skill。\n",
        "可借鉴清单.md": "# 可借鉴清单\n\n读完后记录哪些设计可以迁移到我们的 Skills、工作流或知识库。\n",
        "方法卡草稿.md": "# 方法卡草稿\n\n把可复用方法整理成小卡片，等待验证后再升格。\n",
        "Skill草稿.md": "# Skill草稿\n\n只放草稿，不自动安装、不自动写入全局 Skill 库。\n",
    }


def status_for_ratio(ratio: float, untranslated_blocks: int = 0) -> tuple[str, list[str]]:
    flags: list[str] = []
    if untranslated_blocks:
        flags.append("source_blocks_unprocessed")
    if ratio < 0.28:
        flags.append("translation_too_short")
    elif ratio < 0.45:
        flags.append("translation_needs_review")
    return ("needs_review" if flags else "ok", flags)


def build_acceptance() -> dict[str, Any]:
    return {
        "delivery_rule": "按 Skill 完整阅读页验收；源块、标题、段落、代码块只做后台校验。",
        "gates": [
            {
                "id": "source_assignment",
                "name": "源材料分配完整",
                "pass_condition": "每个 SKILL.md 被分配到且只分配到一个技能组。",
            },
            {
                "id": "full_chinese_body",
                "name": "中文正文完整",
                "pass_condition": "每个 Skill 都有完整中文正文，不能用摘要替代翻译。",
            },
            {
                "id": "layer_separation",
                "name": "原文翻译与 ReaderLab 解读分层",
                "pass_condition": "章前导读、阅读地图和关联材料可以解释，中文正文只承载源文中文化内容。",
            },
            {
                "id": "coverage_check",
                "name": "覆盖校验通过",
                "pass_condition": "已完成 Skill 的源文长度、正文译文长度、导读长度、标题、段落和代码块覆盖指标都通过。",
            },
            {
                "id": "reader_context",
                "name": "阅读辅助清晰",
                "pass_condition": "导读、阅读地图和必要关联说明帮助读者理解位置、路线和机制关系；不生成空洞机器说明。",
            },
            {
                "id": "annotation_ready",
                "name": "可批注",
                "pass_condition": "中文精读页可以被 Tandem Comments 锚定，批注回复命令可读写。",
            },
        ],
    }


def build_manifest(
    book_id: str,
    title: str,
    source: Path,
    files: list[FileInfo],
    skills: list[SkillInfo],
    reading_pages: dict[str, str],
) -> dict[str, Any]:
    groups = grouped_skills(skills)
    source_blocks = {s.name: source_blocks_for_skill(s) for s in skills}
    block_records: list[dict[str, Any]] = []
    skill_records: list[dict[str, Any]] = []
    for skill in skills:
        metrics = skill_coverage_metrics(skill, files)
        status = manifest_skill_status(metrics)
        human_state = human_review_state(book_id, skill.name)
        reading_page = f"10_中文精读/{skill.group}/{skill_reading_filename(skill)}"
        artifacts = discover_skill_artifacts(skill, files)
        skill_record = {
            "name": skill.name,
            "source_file": skill.file.rel,
            "group": skill.group,
            "reading_page": reading_page,
            "mechanism_page": "",
            "evidence_page": "",
            "sha256": skill.file.sha256,
            "source_chars": skill.file.chars,
            "source_bytes": skill.file.bytes,
            "status": status,
            "machine_status": status,
            "human_status": human_state["human_status"],
            "route_reason": skill.route_reason,
            "route_basis": list(skill.route_basis),
            "route_confidence": skill.route_confidence,
            "structure_status": skill.structure_status,
            "reading_source": completed_skill_source(skill),
            "reading_artifact": (completed_skill_translation(skill) or {}).get("artifact_path", ""),
            "coverage": metrics,
            "codex_absorption": build_codex_absorption_record(skill, files, status),
            "related_artifacts": [
                {
                    "path": artifact.rel,
                    "kind": artifact_category(artifact.rel),
                    "role": artifact_role(artifact.rel),
                }
                for artifact in artifacts
            ],
            "source_blocks": len(source_blocks.get(skill.name, [])),
        }
        if "human_review" in human_state:
            skill_record["human_review"] = human_state["human_review"]
        skill_records.append(skill_record)
        for block in source_blocks[skill.name]:
            layer = source_block_reading_layer(block)
            block_records.append(
                {
                    "id": block["id"],
                    "skill": skill.name,
                    "source_file": skill.file.rel,
                    "source_sha256": skill.file.sha256,
                    "kind": block["kind"],
                    "type": block["type"],
                    "start_line": block["start_line"],
                    "end_line": block["end_line"],
                    "source_chars": block["chars"],
                    "sha256": block["sha256"],
                    "source_hash": block["source_hash"],
                    "title": block["title"],
                    "heading": block["heading"],
                    "content_layer": layer["content_layer"],
                    "reader_visibility": layer["reader_visibility"],
                    "absorption_status": layer["absorption_status"],
                    "status": "covered_by_completed_skill" if status == "completed" else "background_pending",
                    "machine_status": "covered_by_completed_skill" if status == "completed" else "background_pending",
                    "reading_page": reading_page,
                }
            )
    skill_records_by_group = {
        group: [record for record in skill_records if record["group"] == group] for group in groups
    }
    group_records = []
    for group, records in skill_records_by_group.items():
        completed_count = sum(1 for record in records if record["machine_status"] == "completed")
        review_count = sum(1 for record in records if record["machine_status"] == "needs_review")
        not_started_count = sum(1 for record in records if record["machine_status"] == "not_started")
        accepted_count = sum(1 for record in records if record["human_status"] == "accepted")
        human_pending_count = sum(1 for record in records if record["human_status"] == "pending")
        human_not_required_count = sum(1 for record in records if record["human_status"] == "not_required")
        group_records.append(
            {
                "id": group,
                "path": f"10_中文精读/{group}/",
                "skill_count": len(records),
                "completed_skills": completed_count,
                "needs_review_skills": review_count,
                "not_started_skills": not_started_count,
                "human_accepted_skills": accepted_count,
                "human_pending_skills": human_pending_count,
                "human_not_required_skills": human_not_required_count,
                "purpose": reading_unit_purpose(group),
                "reason": reading_unit_reason(group, [skill for skill in skills if skill.group == group]),
                "basis": reading_unit_basis([skill for skill in skills if skill.group == group]),
                "confidence": reading_unit_confidence([skill for skill in skills if skill.group == group]),
                "structure_status": reading_unit_status([skill for skill in skills if skill.group == group]),
                "skills": [record["name"] for record in records],
                "source_chars": sum(record["source_chars"] for record in records),
                "translated_body_chars": sum(record["coverage"]["translated_body_chars"] for record in records),
                "status": group_status(records),
                "pages": ["00_本组导读.md"] + [Path(record["reading_page"]).name for record in records],
                "deliverable": completed_count == len(records),
            }
        )
    delivery_status = "deliverable" if group_records and all(g["status"] == "completed" for g in group_records) else "in_progress"
    return {
        "schema": "readerlab.v0.1",
        "delivery_status": delivery_status,
        "status_semantics": {
            "delivery_status": "machine_pack_delivery_status",
            "machine_status": "per_item_machine_generation_and_coverage_status",
            "human_status": "manual_reading_acceptance_status_not_implied_by_delivery_status",
        },
        "acceptance": build_acceptance(),
        "material": {
            "id": book_id,
            "title": title,
            "type": "skills-package",
            "source_path": str(source),
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        },
        "coverage_policy": {
            "source_in_reading_page": False,
            "source_used_for_verification": True,
            "code_blocks": "preserve_or_explain_not_line_translate",
            "related_materials": "inventory_first_mechanism_explained_separately",
            "reading_route": "structure_first_then_name_keywords_as_fallback",
            "reading_page_structure": "main_reading_page_centered",
            "non_body_handling": "codex_absorption_with_trace",
            "reader_visible_evidence_pages": False,
        },
        "material_structure": structure_diagnosis(skills),
        "files": [
            {
                "path": f.rel,
                "kind": f.kind,
                "sha256": f.sha256,
                "source_chars": f.chars,
                "source_bytes": f.bytes,
            }
            for f in files
        ],
        "skills": skill_records,
        "reading_units": group_records,
        "source_blocks": block_records,
    }


def import_skills(args: argparse.Namespace) -> None:
    global AGENT_SKILL_READINGS
    source = Path(args.source).expanduser().resolve()
    if not source.exists() or not source.is_dir():
        raise SystemExit(f"source is not a directory: {source}")
    dest_root = Path(args.dest).expanduser()
    book_id = args.book_id or slugify(source.name)
    title = args.title or source.name
    book_dir = dest_root / book_id
    if book_dir.exists() and not args.force:
        raise SystemExit(f"target exists, pass --force to overwrite generated files: {book_dir}")
    old_manifest = load_existing_manifest(book_dir) if book_dir.exists() else {}
    comment_pages = scan_tandem_comment_pages(book_dir) if book_dir.exists() else []
    if book_dir.exists() and args.force and comment_pages and not args.preserve_comments:
        raise SystemExit(
            "target contains tandem-comments; refusing to overwrite. "
            "Rerun with --force --preserve-comments to migrate or preserve comments."
        )

    files = iter_files(source)
    skills = collect_skills(files, book_id)
    if not skills:
        raise SystemExit("no SKILL.md files found")
    readings_dir = Path(args.readings_dir).expanduser()
    if not readings_dir.is_absolute():
        readings_dir = Path(__file__).resolve().parents[1] / readings_dir
    AGENT_SKILL_READINGS = load_agent_skill_readings(readings_dir, book_id)
    reading_root = "10_中文精读/"
    reading_pages = build_reading_pages(book_id, skills, files)
    support_pages = build_support_pages(book_id, skills, files)
    manifest = build_manifest(book_id, title, source, files, skills, reading_pages)

    if book_dir.exists():
        shutil.rmtree(book_dir)
    (book_dir / "10_中文精读").mkdir(parents=True, exist_ok=True)
    (book_dir / "20_批注与讨论").mkdir(parents=True, exist_ok=True)
    (book_dir / "30_沉淀草稿").mkdir(parents=True, exist_ok=True)

    write_text(book_dir / "00_从这里开始.md", build_start(book_id, title, args.goal, skills))
    write_text(book_dir / "01_轻量拆解手册.md", build_decomposition(title, skills))
    write_text(book_dir / TERMS_PAGE_FILENAME, build_terms_glossary())
    write_text(book_dir / "02_试跑记录.md", build_trial_record(book_id, reading_root, skills))
    write_text(book_dir / "03_验收标准.md", build_acceptance_doc())
    write_text(book_dir / "04_主控清单.md", build_master_checklist(book_id, skills))
    for path, page in reading_pages.items():
        write_text(book_dir / reading_root / path, page)
    for path, page in support_pages.items():
        write_text(book_dir / path, page)
    write_text(book_dir / "source.md", build_source(book_id, title, source, files, skills))
    for filename, content in build_distillation_placeholders().items():
        write_text(book_dir / "30_沉淀草稿" / filename, content)

    if args.preserve_comments and comment_pages:
        manifest["comment_preservation"] = restore_tandem_comments(book_dir, comment_pages, old_manifest, manifest)
    else:
        manifest["comment_preservation"] = {
            "schema": "readerlab.comment-preservation.v1",
            "found": 0,
            "restored": 0,
            "unresolved": 0,
            "malformed_blocks": 0,
            "source_pages": [],
            "report": "",
            "unresolved_page": "",
        }
    write_text(book_dir / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    print(
        json.dumps(
            {
                "book_dir": str(book_dir),
                "files_scanned": len(files),
                "skills": len(skills),
                "reading_units": len(manifest["reading_units"]),
                "reading_root": reading_root,
                "delivery_status": manifest["delivery_status"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


READER_PAGE_FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("页面分层", re.compile(r"页面分层")),
    ("重点与亮点", re.compile(r"^##\s+重点与亮点\s*$", re.M)),
    ("Codex 吸收后的设计提炼", re.compile(r"^##\s+Codex 吸收后的设计提炼\s*$", re.M)),
    ("ReaderLab 后台验收信息", re.compile(r"ReaderLab\s+后台验收信息")),
    ("raw frontmatter", re.compile(r"(?m)^---\s*\n(?:name|description|triggers|allowed-tools|hooks)\s*:")),
    ("自动生成注释", re.compile(r"<!--[^>]*(?:自动生成|请不要直接编辑|重新生成)[^>]*-->", re.S)),
    ("source block", re.compile(r"source\s+block", re.I)),
    ("source_blocks", re.compile(r"source_blocks")),
    ("源块统计", re.compile(r"源块统计")),
    ("源块后台信息", re.compile(r"源块|内部源块")),
    ("hash", re.compile(r"\bhash\b|source_hash|sha256", re.I)),
    ("行号", re.compile(r"源块.{0,20}行号|行号.{0,20}(?:hash|覆盖|校验)|start_line|end_line", re.I)),
    ("源文/译文比例", re.compile(r"源文/译文比例|译文/源文比例|源文/正文译文/比例")),
]


def reader_page_forbidden_terms(text: str) -> list[str]:
    return [label for label, pattern in READER_PAGE_FORBIDDEN_PATTERNS if pattern.search(text)]


def nested_value(payload: dict[str, Any], dotted_path: str) -> Any:
    current: Any = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_missing_value(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def is_absent_required_value(value: Any) -> bool:
    return value is None or value == ""


def load_contract_schema(contract_schema: str) -> dict[str, Any] | None:
    if not CONTRACT_SCHEMA_DIR.exists():
        return None
    for schema_path in sorted(CONTRACT_SCHEMA_DIR.glob("*.schema.json")):
        try:
            schema = json.loads(read_text(schema_path))
        except json.JSONDecodeError:
            continue
        if schema.get("contract_schema") == contract_schema:
            return schema
    return None


def contract_artifact_path(book_dir: Path, rel_path: str) -> Path | None:
    artifact_path = Path(rel_path)
    if artifact_path.is_absolute():
        return None
    resolved = (book_dir / artifact_path).resolve()
    try:
        resolved.relative_to(book_dir.resolve())
    except ValueError:
        return None
    return resolved


def validate_contract_payload(
    contract_schema: str,
    artifact_path: Path,
    artifact: dict[str, Any],
    payload: dict[str, Any],
    schema: dict[str, Any],
    failures: list[str],
) -> None:
    label = f"{contract_schema} ({artifact_path.name})"
    if payload.get("schema") != contract_schema:
        failures.append(f"{label} schema 不匹配：{payload.get('schema')!r}")
    for field in schema.get("required_top_level") or []:
        if field not in payload or is_absent_required_value(payload.get(field)):
            failures.append(f"{label} 缺少必填字段：{field}")
    for parent, fields in (schema.get("required_fields") or {}).items():
        parent_value = nested_value(payload, parent)
        if not isinstance(parent_value, dict):
            failures.append(f"{label} 字段 {parent} 必须是对象")
            continue
        for field in fields:
            if field not in parent_value or is_absent_required_value(parent_value.get(field)):
                failures.append(f"{label} 缺少必填字段：{parent}.{field}")
    for list_path, fields in (schema.get("required_item_fields") or {}).items():
        value = nested_value(payload, list_path)
        if not isinstance(value, list):
            failures.append(f"{label} 字段 {list_path} 必须是列表")
            continue
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                failures.append(f"{label} 字段 {list_path}[{index}] 必须是对象")
                continue
            missing = [field for field in fields if is_missing_value(item.get(field))]
            if missing:
                failures.append(f"{label} 字段 {list_path}[{index}] 缺少：{', '.join(missing)}")
    for field in schema.get("non_empty") or []:
        if is_missing_value(nested_value(payload, field)):
            failures.append(f"{label} 字段不能为空：{field}")
    for field, allowed in (schema.get("allowed_values") or {}).items():
        value = nested_value(payload, field)
        if value not in allowed:
            failures.append(f"{label} 字段 {field} 取值无效：{value!r}")
    if artifact.get("machine_status") and artifact.get("machine_status") != payload.get("machine_status"):
        failures.append(f"{label} manifest.machine_status 与契约产物不一致")
    if artifact.get("human_status") and artifact.get("human_status") != payload.get("human_status"):
        failures.append(f"{label} manifest.human_status 与契约产物不一致")


def validate_contract_artifacts(
    book_dir: Path,
    manifest: dict[str, Any],
    *,
    require_contracts: bool,
    failures: list[str],
) -> list[dict[str, Any]]:
    artifacts = manifest.get("contract_artifacts") or []
    if not isinstance(artifacts, list):
        failures.append("contract_artifacts 必须是列表")
        return []

    seen_schemas = {artifact.get("schema") for artifact in artifacts if isinstance(artifact, dict)}
    if require_contracts:
        for required_schema in REQUIRED_CONTRACT_SCHEMAS:
            if required_schema not in seen_schemas:
                failures.append(f"缺少契约产物引用：{required_schema}")

    summaries: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            failures.append("contract_artifacts 项必须是对象")
            continue
        contract_schema = artifact.get("schema") or artifact.get("contract_schema")
        rel_path = artifact.get("path")
        if not contract_schema:
            failures.append("contract_artifacts 项缺少 schema")
            continue
        if not rel_path:
            failures.append(f"{contract_schema} 缺少 path")
            continue
        schema = load_contract_schema(contract_schema)
        if not schema:
            failures.append(f"{contract_schema} 没有对应的项目契约 schema")
            continue
        artifact_path = contract_artifact_path(book_dir, rel_path)
        if not artifact_path:
            failures.append(f"{contract_schema} path 必须是材料目录内的相对路径：{rel_path}")
            continue
        if not artifact_path.exists():
            failures.append(f"{contract_schema} 契约产物不存在：{rel_path}")
            continue
        try:
            payload = json.loads(read_text(artifact_path))
        except json.JSONDecodeError as exc:
            failures.append(f"{contract_schema} 契约产物不是合法 JSON：{rel_path}: {exc.msg}")
            continue
        validate_contract_payload(contract_schema, artifact_path, artifact, payload, schema, failures)
        summaries.append(
            {
                "schema": contract_schema,
                "path": rel_path,
                "machine_status": payload.get("machine_status"),
                "human_status": payload.get("human_status"),
                "source_scope": payload.get("source_scope", {}).get("coverage_status")
                if isinstance(payload.get("source_scope"), dict)
                else None,
                "confidence": payload.get("confidence", {}).get("level")
                if isinstance(payload.get("confidence"), dict)
                else None,
            }
        )
    return summaries


def validate_pack(args: argparse.Namespace) -> None:
    book_dir = Path(args.book_dir).expanduser()
    manifest_path = book_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifest not found: {manifest_path}")
    manifest = json.loads(read_text(manifest_path))
    failures: list[str] = []
    skills = manifest.get("skills", [])
    blocks = manifest.get("source_blocks", [])
    coverage_policy = manifest.get("coverage_policy") or {}
    contract_summaries = validate_contract_artifacts(
        book_dir,
        manifest,
        require_contracts=args.require_contracts,
        failures=failures,
    )
    expected_policy = {
        "reading_page_structure": "main_reading_page_centered",
        "non_body_handling": "codex_absorption_with_trace",
        "reader_visible_evidence_pages": False,
    }
    for key, expected in expected_policy.items():
        if coverage_policy.get(key) != expected:
            failures.append(f"coverage_policy.{key} 应为 {expected!r}，当前为 {coverage_policy.get(key)!r}")
    for block in blocks:
        missing = [
            key
            for key in ("content_layer", "reader_visibility", "absorption_status")
            if not block.get(key)
        ]
        if missing:
            failures.append(f"源块 {block.get('id')} 缺少分层字段：{', '.join(missing)}")
    scoped_skills = skills
    if args.skill:
        scoped_skills = [s for s in skills if s.get("name") == args.skill]
        blocks = [b for b in blocks if b.get("skill") == args.skill]
        if not scoped_skills:
            failures.append(f"没有找到 Skill：{args.skill}")
    if args.block:
        blocks = [b for b in blocks if b.get("id") == args.block]
        if not blocks:
            failures.append(f"没有找到源块：{args.block}")
    duplicate_pages: dict[str, int] = {}
    for skill in skills:
        page = skill.get("reading_page")
        duplicate_pages[page] = duplicate_pages.get(page, 0) + 1
        page_path = book_dir / page if page else None
        machine_status = skill.get("machine_status") or skill.get("status")
        if machine_status in {"completed", "needs_review"} and page_path and not page_path.exists():
            failures.append(f"{skill.get('name')} 缺少目标阅读页：{page}")
        if machine_status in {"completed", "needs_review"}:
            absorption = skill.get("codex_absorption") or {}
            if not absorption or absorption.get("status") not in {"absorbed", "pending"} or not absorption.get("source_refs"):
                failures.append(f"{skill.get('name')} 缺少可追溯 codex_absorption 记录")
            if page_path and page_path.exists():
                page_text = read_text(page_path)
                forbidden = reader_page_forbidden_terms(page_text)
                if forbidden:
                    failures.append(f"{skill.get('name')} 主阅读页暴露后台信息：{', '.join(forbidden)}")
                if skill.get("structure_status") == "diagnostic" and re.search(r"^#\s+.+：完整中文阅读页", page_text):
                    failures.append(f"{skill.get('name')} 结构诊断项不能标成完整中文阅读页")
            mechanism_page = skill.get("mechanism_page")
            evidence_page = skill.get("evidence_page")
            if mechanism_page and not (book_dir / mechanism_page).exists():
                failures.append(f"{skill.get('name')} 缺少机制说明页：{mechanism_page}")
            if evidence_page and not (book_dir / evidence_page).exists():
                failures.append(f"{skill.get('name')} 缺少证据附录页：{evidence_page}")
    repeated_pages = [page for page, count in duplicate_pages.items() if page and count > 1]
    if repeated_pages:
        failures.append(f"目标阅读页重复：{', '.join(repeated_pages[:5])}")
    if len({(s.get("source_file"), s.get("group")) for s in skills}) != len(skills):
        failures.append("存在重复的 SKILL.md 分组记录")
    if args.require_complete and manifest.get("delivery_status") != "deliverable":
        failures.append(f"材料状态不是整包完成：{manifest.get('delivery_status')}")
    for unit in manifest.get("reading_units", []):
        if not args.require_complete:
            continue
        if unit.get("not_started_skills"):
            failures.append(f"{unit.get('id')} 仍有未完成 Skill：{unit.get('not_started_skills')}")
        if unit.get("needs_review_skills"):
            failures.append(f"{unit.get('id')} 仍有需复核 Skill：{unit.get('needs_review_skills')}")
        if unit.get("status") != "completed":
            failures.append(f"{unit.get('id')} 状态仍是 {unit.get('status')}")
    if args.require_complete:
        scoped_pending = [s for s in scoped_skills if (s.get("machine_status") or s.get("status")) != "completed"]
        if scoped_pending:
            failures.append(f"检查范围内仍有 {len(scoped_pending)} 个 Skill 未完成")
    if args.require_human_accepted:
        scoped_not_cleared = [
            s for s in scoped_skills if s.get("human_status", "pending") not in HUMAN_CLEARED_STATUSES
        ]
        if scoped_not_cleared:
            failures.append(
                f"检查范围内仍有 {len(scoped_not_cleared)} 个 Skill 未人工验收或未标记无需验收"
            )
        contract_not_cleared = [
            item
            for item in contract_summaries
            if item.get("human_status", "pending") not in HUMAN_CLEARED_STATUSES
        ]
        if contract_not_cleared:
            failures.append(
                f"检查范围内仍有 {len(contract_not_cleared)} 个契约产物未人工验收或未标记无需验收"
            )
    validation_issues: list[dict[str, Any]] = []
    for skill in scoped_skills:
        coverage = skill.get("coverage") or {}
        for issue in coverage.get("block_issues") or []:
            validation_issues.append(
                {
                    "skill": skill.get("name"),
                    "kind": "block_reading",
                    "issue": issue,
                }
            )
        for flag in coverage.get("flags") or []:
            if flag in {"block_translation_incomplete", "heading_coverage_incomplete", "paragraph_coverage_low", "code_blocks_not_preserved"}:
                validation_issues.append(
                    {
                        "skill": skill.get("name"),
                        "kind": "coverage",
                        "issue": flag,
                    }
                )
    result = {
        "book_dir": str(book_dir),
        "passed": not failures,
        "require_complete": args.require_complete,
        "require_contracts": args.require_contracts,
        "require_human_accepted": args.require_human_accepted,
        "status_semantics": manifest.get(
            "status_semantics",
            {
                "delivery_status": "machine_pack_delivery_status",
                "human_status": "manual_reading_acceptance_status_not_implied_by_delivery_status",
            },
        ),
        "summary": {
            "total_skills": len(skills),
            "completed_skills": sum(1 for s in skills if (s.get("machine_status") or s.get("status")) == "completed"),
            "needs_review_skills": sum(1 for s in skills if (s.get("machine_status") or s.get("status")) == "needs_review"),
            "not_started_skills": sum(1 for s in skills if (s.get("machine_status") or s.get("status")) == "not_started"),
            "human_accepted_skills": sum(1 for s in skills if s.get("human_status", "pending") == "accepted"),
            "human_pending_skills": sum(1 for s in skills if s.get("human_status", "pending") == "pending"),
            "human_not_required_skills": sum(1 for s in skills if s.get("human_status", "pending") == "not_required"),
            "total_source_blocks": len(manifest.get("source_blocks", [])),
            "delivery_status": manifest.get("delivery_status"),
            "human_cleared_skills": sum(
                1 for s in skills if s.get("human_status", "pending") in HUMAN_CLEARED_STATUSES
            ),
        },
        "contract_artifacts": contract_summaries,
        "scoped_skills": len(scoped_skills),
        "validation_issues": validation_issues,
        "skills": [
            {
                "name": s.get("name"),
                "group": s.get("group"),
                "status": s.get("status"),
                "machine_status": s.get("machine_status") or s.get("status"),
                "human_status": s.get("human_status", "pending"),
                "human_review": s.get("human_review"),
                "reading_page": s.get("reading_page"),
                "coverage": s.get("coverage"),
            }
            for s in scoped_skills[:20]
        ]
        if args.skill
        else [],
        "scoped_blocks": len(blocks),
        "blocks": [
            {
                "id": b.get("id"),
                "skill": b.get("skill"),
                "title": b.get("title"),
                "status": b.get("status"),
                "machine_status": b.get("machine_status") or b.get("status"),
                "reading_page": b.get("reading_page"),
            }
            for b in blocks[:20]
        ]
        if args.block
        else [],
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


def contract_schema(payload: dict[str, Any]) -> str:
    return str(payload.get("schema") or payload.get("contract_schema") or "")


def contract_coverage_status(payload: dict[str, Any]) -> str:
    source_scope = payload.get("source_scope")
    if isinstance(source_scope, dict):
        return str(source_scope.get("coverage_status") or source_scope.get("status") or "")
    coverage = payload.get("coverage")
    if isinstance(coverage, dict):
        return str(coverage.get("coverage_status") or coverage.get("status") or "")
    return ""


def contract_label(path: Path, payload: dict[str, Any]) -> str:
    return f"{contract_schema(payload) or 'unknown-contract'} ({path.name})"


def iter_contract_json_paths(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(path for path in target.rglob("*.json") if path.is_file())


def iter_dict_nodes(value: Any, path: str = "$") -> list[tuple[str, dict[str, Any]]]:
    nodes: list[tuple[str, dict[str, Any]]] = []
    if isinstance(value, dict):
        nodes.append((path, value))
        for key, child in value.items():
            nodes.extend(iter_dict_nodes(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            nodes.extend(iter_dict_nodes(child, f"{path}[{index}]"))
    return nodes


def as_non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def has_contract_refs(item: dict[str, Any]) -> bool:
    for key in CONTRACT_REF_KEYS:
        if as_non_empty_list(item.get(key)):
            return True
    claim_refs = item.get("claim_refs")
    if isinstance(claim_refs, list):
        for ref in claim_refs:
            if isinstance(ref, dict) and any(as_non_empty_list(ref.get(key)) for key in CONTRACT_REF_KEYS):
                return True
    return False


def collect_contract_refs(payload: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for _path, node in iter_dict_nodes(payload):
        for key in CONTRACT_REF_KEYS:
            value = node.get(key)
            if isinstance(value, list):
                refs.update(str(item) for item in value if isinstance(item, str) and item)
    return refs


def collect_known_ref_ids(payloads: list[dict[str, Any]]) -> set[str]:
    known: set[str] = set()
    for payload in payloads:
        schema = contract_schema(payload)
        if schema == "readerlab.source-registry.v1":
            for source in payload.get("sources") or []:
                if isinstance(source, dict):
                    for key in ("source_id", "id"):
                        if source.get(key):
                            known.add(str(source[key]))
        if schema == "readerlab.location-map.v1":
            for location in payload.get("locations") or payload.get("location_refs") or []:
                if isinstance(location, dict):
                    for key in ("location_id", "id", "ref_id"):
                        if location.get(key):
                            known.add(str(location[key]))
    return known


def collect_primary_module_location_ids(payloads: list[dict[str, Any]]) -> set[str]:
    primary_source_ids: set[str] = set()
    for payload in payloads:
        if contract_schema(payload) != "readerlab.source-registry.v1":
            continue
        for source in payload.get("sources") or []:
            if not isinstance(source, dict):
                continue
            source_id = source.get("source_id") or source.get("id")
            if source_id and source.get("source_role") == "primary_module":
                primary_source_ids.add(str(source_id))
    if not primary_source_ids:
        return set()
    required_location_ids: set[str] = set()
    for payload in payloads:
        if contract_schema(payload) != "readerlab.location-map.v1":
            continue
        for location in payload.get("locations") or []:
            if not isinstance(location, dict):
                continue
            location_id = location.get("location_id") or location.get("id") or location.get("ref_id")
            source_id = location.get("source_id")
            if location_id and source_id and str(source_id) in primary_source_ids:
                required_location_ids.add(str(location_id))
    return required_location_ids


def collect_capability_domain_refs(payloads: list[dict[str, Any]]) -> set[str]:
    refs: set[str] = set()
    for payload in payloads:
        if contract_schema(payload) != "readerlab.capability-map.v1":
            continue
        domains = payload.get("capability_domains")
        if not isinstance(domains, list):
            continue
        for domain in domains:
            if isinstance(domain, dict):
                refs.update(collect_contract_refs(domain))
    return refs


def normalize_eval_key(value: Any) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", str(value or "").lower()).strip("_")
    return normalized


def validate_source_registry(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    if contract_schema(payload) != "readerlab.source-registry.v1":
        return
    label = contract_label(path, payload)
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        failures.append(f"{label} source-registry.sources 必须是非空列表")
        return
    seen: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            failures.append(f"{label} sources[{index}] 必须是对象")
            continue
        source_id = source.get("source_id") or source.get("id")
        if not source_id:
            failures.append(f"{label} sources[{index}] 缺少 source_id")
            continue
        if is_missing_value(source.get("source_path")) and is_missing_value(source.get("title")):
            failures.append(f"{label} sources[{index}] 缺少 source_path 或 title，不能作为空壳来源")
        if str(source_id) in seen:
            failures.append(f"{label} source_id 重复：{source_id}")
        seen.add(str(source_id))


def validate_location_map(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    if contract_schema(payload) != "readerlab.location-map.v1":
        return
    label = contract_label(path, payload)
    locations = payload.get("locations")
    if not isinstance(locations, list) or not locations:
        failures.append(f"{label} location-map.locations 必须是非空列表")
        return
    seen: set[str] = set()
    for index, location in enumerate(locations):
        if not isinstance(location, dict):
            failures.append(f"{label} locations[{index}] 必须是对象")
            continue
        location_id = location.get("location_id") or location.get("id") or location.get("ref_id")
        if not location_id:
            failures.append(f"{label} locations[{index}] 缺少 location_id")
            continue
        if is_missing_value(location.get("source_id")):
            failures.append(f"{label} locations[{index}] 缺少 source_id，位置必须挂回来源")
        if is_missing_value(location.get("path")) and is_missing_value(location.get("range")):
            failures.append(f"{label} locations[{index}] 缺少 path 或 range，不能作为空壳位置")
        if str(location_id) in seen:
            failures.append(f"{label} location_id 重复：{location_id}")
        seen.add(str(location_id))


def validate_contract_status_and_display(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    label = contract_label(path, payload)
    if not payload.get("machine_status"):
        failures.append(f"{label} 缺少 machine_status，机器状态不能和人工状态混用")
    if not payload.get("human_status"):
        failures.append(f"{label} 缺少 human_status，人工验收状态必须单独表达")
    display = payload.get("display")
    if not isinstance(display, dict):
        failures.append(f"{label} 缺少 display，无法证明 reader-facing 和 internal audit 分离")
        return
    relationship = display.get("relationship")
    if not relationship:
        failures.append(f"{label} 缺少 display.relationship")
    if relationship in {"mixed", "same_file", "reader_facing_is_audit"}:
        failures.append(f"{label} display.relationship 不能把 reader-facing 和 internal audit 混在一起")
    reader_paths = display.get("reader_facing") or display.get("reader_facing_paths") or []
    audit_paths = display.get("internal_audit") or display.get("internal_audit_paths") or []
    if reader_paths and not isinstance(reader_paths, list):
        failures.append(f"{label} display.reader_facing 必须是列表")
        reader_paths = []
    if audit_paths and not isinstance(audit_paths, list):
        failures.append(f"{label} display.internal_audit 必须是列表")
        audit_paths = []
    overlap = set(reader_paths) & set(audit_paths)
    if overlap:
        failures.append(f"{label} reader-facing 与 internal audit 路径重叠：{', '.join(sorted(overlap))}")


def validate_contract_claim_refs(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    label = contract_label(path, payload)
    for node_path, node in iter_dict_nodes(payload):
        for list_key in ("high_level_claims", "claims", "distillation_candidates", "technical_insights"):
            items = node.get(list_key)
            if not isinstance(items, list):
                continue
            for index, item in enumerate(items):
                if not isinstance(item, dict):
                    failures.append(f"{label} {node_path}.{list_key}[{index}] 必须是对象")
                    continue
                if item.get("claim") and not has_contract_refs(item):
                    failures.append(f"{label} {node_path}.{list_key}[{index}] high-level claim 缺少 source refs")
        if node.get("claim") and "claim_refs" not in node_path and not has_contract_refs(node):
            failures.append(f"{label} {node_path} high-level claim 缺少 source refs")


def validate_grounded_global_map(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    schema = contract_schema(payload)
    if schema != "readerlab.grounded-global-map.v1":
        return
    coverage_status = contract_coverage_status(payload)
    if coverage_status not in CONTRACT_FULL_COVERAGE_STATUSES:
        failures.append(
            f"{contract_label(path, payload)} coverage={coverage_status!r} 不足，不能生成 grounded global map"
        )


def validate_local_deepread(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    if contract_schema(payload) != "readerlab.local-deepread.v1":
        return
    label = contract_label(path, payload)
    deepread = payload.get("local_deepread")
    if isinstance(deepread, dict) and isinstance(deepread.get("cards"), list):
        cards = deepread["cards"]
    elif isinstance(deepread, dict):
        cards = [deepread]
    elif isinstance(deepread, list):
        cards = deepread
    else:
        failures.append(f"{label} local_deepread 必须是对象或列表")
        return
    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            failures.append(f"{label} local_deepread[{index}] 必须是对象")
            continue
        for field in ("reader_gain", "primary_refs", "boundary", "confidence"):
            if is_missing_value(card.get(field)):
                failures.append(f"{label} local_deepread[{index}] 缺少 {field}")


def validate_capability_map(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    if contract_schema(payload) != "readerlab.capability-map.v1":
        return
    label = contract_label(path, payload)
    domains = payload.get("capability_domains")
    if not isinstance(domains, list) or not domains:
        failures.append(f"{label} capability-map 必须包含 capability_domains，不能只是目录列表")
        return
    for index, domain in enumerate(domains):
        if not isinstance(domain, dict):
            failures.append(f"{label} capability_domains[{index}] 必须是对象")
            continue
        missing = [field for field in CAPABILITY_CORE_FIELDS if is_missing_value(domain.get(field))]
        if missing:
            failures.append(f"{label} capability_domains[{index}] 缺少核心字段：{', '.join(missing)}")
        if not has_contract_refs(domain):
            failures.append(f"{label} capability_domains[{index}] 缺少 source refs")


def validate_output_eval(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    if contract_schema(payload) != "readerlab.output-eval.v1":
        return
    label = contract_label(path, payload)
    output_eval = payload.get("output_eval")
    checks = output_eval.get("checks") if isinstance(output_eval, dict) else None
    if not isinstance(checks, list) or not checks:
        failures.append(f"{label} output-eval 必须包含检查项列表")
        return
    covered_categories: set[str] = set()
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            failures.append(f"{label} output_eval.checks[{index}] 必须是对象")
            continue
        if is_missing_value(check.get("status")):
            failures.append(f"{label} output_eval.checks[{index}] 缺少 status")
        if is_missing_value(check.get("id")) and is_missing_value(check.get("name")):
            failures.append(f"{label} output_eval.checks[{index}] 缺少 id 或 name")
        candidates = {
            normalize_eval_key(check.get("category")),
            normalize_eval_key(check.get("id")),
            normalize_eval_key(check.get("name")),
        }
        for required in OUTPUT_EVAL_REQUIRED_CATEGORIES:
            if required in candidates:
                covered_categories.add(required)
    missing_categories = sorted(OUTPUT_EVAL_REQUIRED_CATEGORIES - covered_categories)
    if missing_categories:
        failures.append(f"{label} output-eval 缺少必检项：{', '.join(missing_categories)}")


def validate_contract_payload_v1(path: Path, payload: dict[str, Any], failures: list[str]) -> None:
    schema = contract_schema(payload)
    if not schema.startswith("readerlab."):
        return
    validate_source_registry(path, payload, failures)
    validate_location_map(path, payload, failures)
    validate_contract_status_and_display(path, payload, failures)
    validate_contract_claim_refs(path, payload, failures)
    validate_grounded_global_map(path, payload, failures)
    validate_local_deepread(path, payload, failures)
    validate_capability_map(path, payload, failures)
    validate_output_eval(path, payload, failures)


def validate_contract_package_shape(target: Path, payloads: list[dict[str, Any]], failures: list[str]) -> None:
    schemas = {contract_schema(payload) for payload in payloads}
    missing = sorted(CONTRACT_PACKAGE_REQUIRED_SCHEMAS - schemas)
    if missing:
        failures.append(f"样本目录缺少必需 contract：{', '.join(missing)}")
    if not (schemas & CONTRACT_ROUTE_SCHEMAS):
        failures.append("样本目录缺少 catalog-map / capability-map / grounded-global-map 之一")
    if "readerlab.grounded-global-map.v1" in schemas:
        source_payload = next((p for p in payloads if contract_schema(p) == "readerlab.source-registry.v1"), {})
        source_coverage = contract_coverage_status(source_payload)
        if source_coverage not in CONTRACT_FULL_COVERAGE_STATUSES:
            failures.append(
                f"source-registry coverage={source_coverage!r} 不足，目录中不能包含 grounded-global-map"
            )
    reader_pages = sorted(path for path in target.rglob("*.md") if path.is_file() and "audit" not in path.parts)
    audit_json = sorted(path for path in target.rglob("*.json") if path.is_file() and "audit" in path.parts)
    if not reader_pages:
        failures.append("样本目录缺少 reader-facing markdown")
    if not audit_json:
        failures.append("样本目录缺少 internal audit JSON")
    if not any(path.name == "rejected-downgraded.md" for path in target.rglob("*.md") if path.is_file()):
        failures.append("样本目录缺少 rejected-downgraded.md")


def validate_capability_module_coverage(payloads: list[dict[str, Any]], failures: list[str]) -> None:
    schemas = {contract_schema(payload) for payload in payloads}
    if "readerlab.capability-map.v1" not in schemas:
        return
    required_location_ids = collect_primary_module_location_ids(payloads)
    if not required_location_ids:
        return
    covered_refs = collect_capability_domain_refs(payloads)
    missing = sorted(required_location_ids - covered_refs)
    if missing:
        failures.append(f"capability-map 未覆盖 primary_module location refs：{', '.join(missing)}")


def validate_contract_references(
    contract_paths: list[Path],
    payloads: list[dict[str, Any]],
    failures: list[str],
) -> None:
    known = collect_known_ref_ids(payloads)
    all_refs = [
        (path, payload, sorted(collect_contract_refs(payload)))
        for path, payload in zip(contract_paths, payloads)
    ]
    refs_present = any(refs for _path, _payload, refs in all_refs)
    if refs_present and not known:
        failures.append("contract refs 存在，但 source-registry/location-map 没有可用 known ids")
        return
    for path, payload, refs in all_refs:
        for ref in refs:
            if ref not in known:
                failures.append(f"{contract_label(path, payload)} 引用了未知 source/location ref：{ref}")


def validate_contract_target(target: Path) -> dict[str, Any]:
    if not target.exists():
        raise SystemExit(f"contract path not found: {target}")
    contract_paths = iter_contract_json_paths(target)
    failures: list[str] = []
    payloads: list[dict[str, Any]] = []
    used_paths: list[Path] = []
    for path in contract_paths:
        try:
            payload = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            failures.append(f"{path} 不是合法 JSON：{exc.msg}")
            continue
        if not isinstance(payload, dict):
            failures.append(f"{path} contract 必须是 JSON 对象")
            continue
        schema = contract_schema(payload)
        if not schema.startswith("readerlab."):
            if target.is_file():
                failures.append(f"{path} 缺少 readerlab.* schema")
            continue
        payloads.append(payload)
        used_paths.append(path)
        validate_contract_payload_v1(path, payload, failures)
    if target.is_dir():
        validate_contract_package_shape(target, payloads, failures)
        validate_capability_module_coverage(payloads, failures)
    validate_contract_references(used_paths, payloads, failures)
    return {
        "target": str(target),
        "passed": not failures,
        "contract_count": len(payloads),
        "schemas": sorted({contract_schema(payload) for payload in payloads}),
        "contracts": [
            {
                "path": str(path),
                "schema": contract_schema(payload),
                "coverage_status": contract_coverage_status(payload),
                "machine_status": payload.get("machine_status"),
                "human_status": payload.get("human_status"),
            }
            for path, payload in zip(used_paths, payloads)
        ],
        "failures": failures,
    }


def validate_contract_cmd(args: argparse.Namespace) -> None:
    target = Path(args.path).expanduser()
    result = validate_contract_target(target)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["failures"]:
        raise SystemExit(1)


def first_contract_payload(payloads: list[dict[str, Any]], schema: str) -> dict[str, Any]:
    for payload in payloads:
        if contract_schema(payload) == schema:
            return payload
    return {}


def load_contract_payloads(target: Path) -> tuple[list[Path], list[dict[str, Any]]]:
    paths: list[Path] = []
    payloads: list[dict[str, Any]] = []
    for path in iter_contract_json_paths(target):
        try:
            payload = json.loads(read_text(path))
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and contract_schema(payload).startswith("readerlab."):
            paths.append(path)
            payloads.append(payload)
    return paths, payloads


def strip_markdown_title(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def source_excerpt_records(sample_dir: Path, source_registry: dict[str, Any]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    failures: list[str] = []
    for source in source_registry.get("sources") or []:
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("source_id") or source.get("id") or "")
        source_path = str(source.get("source_path") or "")
        if not source_path:
            failures.append(f"source {source_id or '<unknown>'} 缺少 source_path，renderer 无法生成一手正文")
            continue
        path = sample_dir / source_path
        if not path.exists():
            failures.append(f"source excerpt not found: {source_path}")
            continue
        text = strip_markdown_title(read_text(path))
        if not text:
            failures.append(f"source excerpt is empty: {source_path}")
            continue
        records.append(
            {
                "source_id": source_id,
                "source_path": source_path,
                "source_role": str(source.get("source_role") or ""),
                "text": text,
            }
        )
    if failures:
        raise SystemExit("source excerpts invalid:\n- " + "\n- ".join(failures))
    if not records:
        raise SystemExit("source excerpts invalid: no renderable source excerpts")
    return records


def lines_to_markdown_list(items: Any, *, indent: str = "") -> list[str]:
    if not isinstance(items, list) or not items:
        return [f"{indent}- 未声明。"]
    return [f"{indent}- {item}" for item in items]


def markdown_quote(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        lines.append(f"> {line}" if line else ">")
    return "\n".join(lines)


def render_status_block(payloads: list[dict[str, Any]]) -> list[str]:
    machine_statuses = sorted({str(payload.get("machine_status")) for payload in payloads if payload.get("machine_status")})
    human_statuses = sorted({str(payload.get("human_status")) for payload in payloads if payload.get("human_status")})
    return [
        "## 状态边界",
        "",
        f"- machine_status：{', '.join(machine_statuses) if machine_statuses else 'unknown'}",
        f"- human_status：{', '.join(human_statuses) if human_statuses else 'unknown'}",
        "- 说明：机器状态只表示脚本和 contract 层可检查；人工阅读验收仍需单独完成。",
        "",
    ]


def render_longform_reader(sample_dir: Path, payloads: list[dict[str, Any]]) -> dict[str, str]:
    source_registry = first_contract_payload(payloads, "readerlab.source-registry.v1")
    catalog = first_contract_payload(payloads, "readerlab.catalog-map.v1")
    deepread = first_contract_payload(payloads, "readerlab.local-deepread.v1")
    excerpts = source_excerpt_records(sample_dir, source_registry)
    reading_units = ((catalog.get("catalog") or {}).get("reading_units") or []) if isinstance(catalog, dict) else []
    unit = reading_units[0] if reading_units and isinstance(reading_units[0], dict) else {}
    deepread_card = deepread.get("local_deepread") if isinstance(deepread.get("local_deepread"), dict) else {}
    title = str(unit.get("title") or deepread_card.get("title") or "局部长文阅读页")
    route_hypothesis = (catalog.get("catalog") or {}).get("route_hypothesis") if isinstance(catalog, dict) else []
    not_yet = (catalog.get("catalog") or {}).get("not_yet_covered_units") if isinstance(catalog, dict) else []
    lines = [
        f"# 局部长文样本：{title}",
        "",
        "## 这一节先看什么",
        "",
        *lines_to_markdown_list(route_hypothesis),
        "",
        "## 处理过的一手正文",
        "",
    ]
    for excerpt in excerpts:
        lines.extend(
            [
                f"### 来源：`{excerpt['source_path']}`",
                "",
                markdown_quote(excerpt["text"]),
                "",
            ]
        )
    lines.extend(
        [
            "## AI 旁批",
            "",
            str(deepread_card.get("reader_gain") or "这一页只提供局部阅读辅助，不能替代一手材料。"),
            "",
            "## 深读判断",
            "",
            f"- 主张：{deepread_card.get('claim') or '未声明'}",
            f"- 边界：{deepread_card.get('boundary') or '未声明'}",
            f"- 置信度：{deepread_card.get('confidence') or 'unknown'}",
            "",
            "## 尚未覆盖",
            "",
            *lines_to_markdown_list(not_yet),
            "",
            *render_status_block(payloads),
            "## 可批注问题",
            "",
            "- 这个局部原则在你的材料或工作流里应该怎样被验证，而不是直接照搬？",
            "",
        ]
    )
    return {"reader/01_局部长文阅读页.md": "\n".join(lines)}


def render_skill_reader(sample_dir: Path, payloads: list[dict[str, Any]]) -> dict[str, str]:
    source_registry = first_contract_payload(payloads, "readerlab.source-registry.v1")
    capability = first_contract_payload(payloads, "readerlab.capability-map.v1")
    excerpts = source_excerpt_records(sample_dir, source_registry)
    domains = capability.get("capability_domains") if isinstance(capability.get("capability_domains"), list) else []
    title = str((capability.get("material") or {}).get("title") or "工程材料阅读页")
    reader_lines = [
        f"# Skill/工程材料样本：{title}",
        "",
        "## 这一节先看什么",
        "",
        "这个渲染页按模块能力阅读材料：先看一手模块正文，再看触发、输入、输出和验收边界。",
        "",
        "## 处理过的一手正文",
        "",
    ]
    for index, excerpt in enumerate(excerpts, start=1):
        reader_lines.extend(
            [
                f"### 模块{index}：`{excerpt['source_path']}`",
                "",
                excerpt["text"],
                "",
            ]
        )
    reader_lines.extend(
        [
            "## AI 旁批",
            "",
            "这组材料的重点不是目录顺序，而是每个模块在 Agent 工作流中的职责边界。",
            "",
            "## 容易误读的地方",
            "",
            "- capability-map 不是目录列表；它必须说明触发、输入、输出、验证和不适用边界。",
            "- output-eval 只能表达机器检查结论，不能冒充人工阅读验收。",
            "",
            *render_status_block(payloads),
        ]
    )
    side_lines = [
        "# 技术合伙人旁批",
        "",
        "下面只记录可迁移的工程设计原子；它不是人工验收结论。",
        "",
    ]
    for domain in domains:
        if not isinstance(domain, dict):
            continue
        side_lines.extend(
            [
                f"## {domain.get('name') or domain.get('domain_id')}",
                "",
                f"- owned_job：{domain.get('owned_job') or '未声明'}",
                "- trigger_signals：",
                *lines_to_markdown_list(domain.get("trigger_signals"), indent="  "),
                "- required_inputs：",
                *lines_to_markdown_list(domain.get("required_inputs"), indent="  "),
                "- output_contract：",
                *lines_to_markdown_list(domain.get("output_contract"), indent="  "),
                "- verification：",
                *lines_to_markdown_list(domain.get("verification"), indent="  "),
                f"- human_status：{domain.get('human_status') or 'pending'}",
                "",
            ]
        )
    return {
        "reader/01_工程材料阅读页.md": "\n".join(reader_lines),
        "reader/02_技术合伙人旁批.md": "\n".join(side_lines),
    }


def render_contract_package_cmd(args: argparse.Namespace) -> None:
    sample_dir = Path(args.sample_dir).expanduser()
    output_dir = Path(args.output_dir).expanduser()
    if not sample_dir.exists() or not sample_dir.is_dir():
        raise SystemExit(f"sample_dir not found: {sample_dir}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise SystemExit(f"output_dir is not empty; refusing to overwrite: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    validation = validate_contract_target(sample_dir)
    if validation["failures"]:
        print(json.dumps(validation, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    _paths, payloads = load_contract_payloads(sample_dir)
    audit_src = sample_dir / "audit"
    if not audit_src.exists():
        raise SystemExit(f"sample_dir 缺少 audit 目录: {sample_dir}")
    shutil.copytree(audit_src, output_dir / "audit", dirs_exist_ok=True)

    schemas = {contract_schema(payload) for payload in payloads}
    if "readerlab.capability-map.v1" in schemas:
        rendered_pages = render_skill_reader(sample_dir, payloads)
    elif "readerlab.catalog-map.v1" in schemas:
        rendered_pages = render_longform_reader(sample_dir, payloads)
    else:
        raise SystemExit("sample_dir 缺少可渲染的 catalog-map 或 capability-map")
    for rel_path, text in rendered_pages.items():
        write_text(output_dir / rel_path, text.rstrip() + "\n")
    result = {
        "sample_dir": str(sample_dir),
        "output_dir": str(output_dir),
        "rendered_pages": sorted(rendered_pages),
        "audit_copied": True,
        "machine_status": sorted({str(payload.get("machine_status")) for payload in payloads if payload.get("machine_status")}),
        "human_status": sorted({str(payload.get("human_status")) for payload in payloads if payload.get("human_status")}),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def output_eval_categories(payloads: list[dict[str, Any]]) -> set[str]:
    output_eval = first_contract_payload(payloads, "readerlab.output-eval.v1")
    checks = ((output_eval.get("output_eval") or {}).get("checks") or []) if isinstance(output_eval, dict) else []
    categories: set[str] = set()
    for check in checks:
        if not isinstance(check, dict):
            continue
        candidates = {
            normalize_eval_key(check.get("category")),
            normalize_eval_key(check.get("id")),
            normalize_eval_key(check.get("name")),
        }
        categories.update(required for required in OUTPUT_EVAL_REQUIRED_CATEGORIES if required in candidates)
    return categories


def collect_reader_paths(payloads: list[dict[str, Any]]) -> set[str]:
    paths: set[str] = set()
    for payload in payloads:
        display = payload.get("display")
        if not isinstance(display, dict):
            continue
        reader_paths = display.get("reader_facing") or display.get("reader_facing_paths") or []
        if isinstance(reader_paths, list):
            paths.update(str(path) for path in reader_paths if path)
    return paths


def collect_declared_source_paths(payloads: list[dict[str, Any]]) -> list[str]:
    source_registry = first_contract_payload(payloads, "readerlab.source-registry.v1")
    source_paths: list[str] = []
    for source in source_registry.get("sources") or []:
        if isinstance(source, dict) and source.get("source_path"):
            source_paths.append(str(source["source_path"]))
    return source_paths


def normalize_inline_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def first_hand_body_failures(target: Path, reader_paths: set[str], source_paths: list[str]) -> list[str]:
    failures: list[str] = []
    if not source_paths:
        return ["source-registry has no source_path for first-hand body check"]
    source_snippets: list[tuple[str, str]] = []
    for source_path in source_paths:
        path = target / source_path
        if not path.is_file():
            failures.append(f"source excerpt not found for first-hand body check: {source_path}")
            continue
        source_text = normalize_inline_text(strip_markdown_title(read_text(path)))
        if not source_text:
            failures.append(f"source excerpt is empty for first-hand body check: {source_path}")
            continue
        source_snippets.append((source_path, source_text[:80]))
    if failures:
        return failures
    body_found = False
    for reader_path in sorted(reader_paths):
        path = target / reader_path
        if not path.is_file():
            continue
        text = read_text(path)
        body_match = re.search(r"^## 处理过的一手正文\s*(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not body_match:
            continue
        body = body_match.group(1)
        normalized_body = normalize_inline_text(body)
        if any(source_path in body and snippet in normalized_body for source_path, snippet in source_snippets):
            body_found = True
            break
    if not body_found:
        failures.append("reader markdown missing actual first-hand body from source excerpts")
    return failures


def render_eval_markdown_report(result: dict[str, Any]) -> str:
    lines = [
        "# ReaderLab Rendered Package Eval Report",
        "",
        f"- target: `{result['target']}`",
        f"- passed: {str(result['passed']).lower()}",
        f"- validate_contract_passed: {str(result['validate_contract_passed']).lower()}",
        f"- contract_count: {result['contract_count']}",
        f"- schemas: {', '.join(result['schemas']) if result['schemas'] else 'none'}",
        "",
        "## Gates",
        "",
    ]
    for gate in result["gates"]:
        lines.append(f"- {gate['id']}: {gate['status']}")
        failures = gate.get("failures") or []
        if failures:
            for failure in failures:
                lines.append(f"  - {failure}")
    if not result["gates"]:
        lines.append("- none")
    lines.extend(["", "## Failures", ""])
    if result["failures"]:
        lines.extend(f"- {failure}" for failure in result["failures"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Machine / Human Boundary",
            "",
            "- This report is a machine eval report, not human acceptance.",
            "- Required boundary: human_status pending until the product owner manually accepts the reader benefit and taste.",
            "- Passing gates mean ready_for_human_review at most; they do not mean product_ready.",
            "",
        ]
    )
    return "\n".join(lines)


def prepare_report_path(raw_path: str, *, overwrite: bool = False) -> Path:
    report_path = Path(raw_path).expanduser()
    resolved = report_path.resolve()
    try:
        resolved.relative_to(LIFEATLAS_ROOT)
    except ValueError:
        pass
    else:
        raise SystemExit("refusing to write eval report under LifeAtlas; use /private/tmp or repo-local path")
    if resolved.exists() and not overwrite:
        raise SystemExit(f"report path already exists; use --overwrite-report to replace: {resolved}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def eval_rendered_package_cmd(args: argparse.Namespace) -> None:
    target = Path(args.path).expanduser()
    validation = validate_contract_target(target)
    _paths, payloads = load_contract_payloads(target)
    failures: list[str] = list(validation["failures"])
    gates: list[dict[str, Any]] = []

    reader_paths = collect_reader_paths(payloads)
    missing_reader = sorted(path for path in reader_paths if not (target / path).is_file())
    audit_reader_paths = sorted(path for path in reader_paths if "audit" in Path(path).parts)
    gates.append(
        {
            "id": "reader_markdown_exists",
            "status": "fail" if missing_reader else "pass",
            "failures": [f"reader markdown missing: {path}" for path in missing_reader],
        }
    )
    gates.append(
        {
            "id": "reader_audit_path_separation",
            "status": "fail" if audit_reader_paths else "pass",
            "failures": [f"reader path must not be under audit: {path}" for path in audit_reader_paths],
        }
    )
    failures.extend(f"reader markdown missing: {path}" for path in missing_reader)
    failures.extend(f"reader path must not be under audit: {path}" for path in audit_reader_paths)

    first_hand_failures = first_hand_body_failures(target, reader_paths, collect_declared_source_paths(payloads))
    gates.append(
        {
            "id": "first_hand_body_source_present",
            "status": "fail" if first_hand_failures else "pass",
            "failures": first_hand_failures,
        }
    )
    failures.extend(first_hand_failures)

    missing_eval = sorted(OUTPUT_EVAL_REQUIRED_CATEGORIES - output_eval_categories(payloads))
    gates.append(
        {
            "id": "output_eval_9_gates_present",
            "status": "fail" if missing_eval else "pass",
            "failures": [f"output-eval missing gate: {gate}" for gate in missing_eval],
        }
    )
    failures.extend(f"output-eval missing gate: {gate}" for gate in missing_eval)

    accepted_paths = [
        contract_label(path, payload)
        for path, payload in zip(_paths, payloads)
        if str(payload.get("human_status") or "").lower() in HUMAN_CLEARED_STATUSES
    ]
    gates.append(
        {
            "id": "human_status_not_machine_accepted",
            "status": "fail" if accepted_paths else "pass",
            "failures": [f"human_status must remain pending for rendered machine package: {path}" for path in accepted_paths],
        }
    )
    failures.extend(f"human_status must remain pending for rendered machine package: {path}" for path in accepted_paths)

    result = {
        "target": str(target),
        "passed": not failures,
        "validate_contract_passed": validation["passed"],
        "contract_count": validation["contract_count"],
        "schemas": validation["schemas"],
        "gates": gates,
        "failures": failures,
    }
    if args.report_md:
        report_path = prepare_report_path(args.report_md, overwrite=args.overwrite_report)
        write_text(report_path, render_eval_markdown_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


def block_manifest_cmd(args: argparse.Namespace) -> None:
    skill_md = Path(args.skill_md).expanduser().resolve()
    if not skill_md.exists() or not skill_md.is_file():
        raise SystemExit(f"SKILL.md not found: {skill_md}")
    payload = build_skill_block_manifest(
        skill_md,
        skill_name=args.skill or skill_md.parent.name,
        source_file=args.source_file or skill_md.name,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def load_tandem(path: Path) -> tuple[str, dict]:
    text = read_text(path)
    m = SOURCE_BLOCK_RE.search(text)
    if not m:
        return text, {}
    raw = "\n".join(line for line in m.group(1).splitlines() if not line.lstrip().startswith("//"))
    json_start = raw.find("{")
    if json_start < 0:
        return text, {}
    data, _ = json.JSONDecoder().raw_decode(raw[json_start:])
    return text, data


def locate_anchor(text: str, item: dict) -> dict:
    anchor = item.get("anchor", {})
    exact = anchor.get("exact", "")
    prefix = anchor.get("prefix", "")
    suffix = anchor.get("suffix", "")
    pos = anchor.get("pos")
    found = text.find(exact) if exact else -1
    return {
        "found": found >= 0,
        "actual_pos": found,
        "stored_pos": pos,
        "pos_delta": None if found < 0 or pos is None else found - pos,
        "prefix_matches": found >= 0 and (not prefix or text[max(0, found - len(prefix)) : found] == prefix),
        "suffix_matches": found >= 0
        and (not suffix or text[found + len(exact) : found + len(exact) + len(suffix)] == suffix),
    }


def comments_list(args: argparse.Namespace) -> None:
    text, data = load_tandem(Path(args.path))
    rows = []
    for cid, item in data.items():
        thread = item.get("thread", [])
        rows.append(
            {
                "id": cid,
                "status": item.get("status"),
                "thread_count": len(thread),
                "latest": thread[-1].get("text") if thread else "",
                "anchor": locate_anchor(text, item),
            }
        )
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def dump_tandem(data: dict) -> str:
    return "```tandem-comments\n" + "\n".join(
        [
            '// Schema: { "<id>": { anchor:{exact,prefix,suffix,pos?}, status:open|resolved, thread:[{author,ts,text}] } }',
            '// Anchor = quote from the prose. To locate: search for "exact", disambiguate via prefix/suffix.',
            json.dumps(data, ensure_ascii=False, indent=2),
            "```",
        ]
    )


def comments_reply(args: argparse.Namespace) -> None:
    path = Path(args.path)
    text, data = load_tandem(path)
    if args.comment_id not in data:
        raise SystemExit(f"comment id not found: {args.comment_id}")
    item = data[args.comment_id]
    loc = locate_anchor(text, item)
    if not loc["found"]:
        raise SystemExit("anchor exact text not found; refusing to write reply")
    item.setdefault("thread", []).append(
        {
            "author": args.author,
            "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "text": args.text,
        }
    )
    new_block = dump_tandem(data)
    if SOURCE_BLOCK_RE.search(text):
        new_text = SOURCE_BLOCK_RE.sub(lambda _m: new_block, text)
    else:
        new_text = text.rstrip() + "\n\n" + new_block + "\n"
    write_text(path, new_text)
    print(json.dumps({"replied": args.comment_id, "anchor": loc}, ensure_ascii=False, indent=2))


def parse_tandem_block_from_text(text: str) -> tuple[dict[str, Any], str, str]:
    m = SOURCE_BLOCK_RE.search(text)
    if not m:
        return {}, "", ""
    raw_block = m.group(0)
    raw = "\n".join(line for line in m.group(1).splitlines() if not line.lstrip().startswith("//"))
    json_start = raw.find("{")
    if json_start < 0:
        return {}, "tandem-comments block has no JSON object", raw_block
    try:
        data, _ = json.JSONDecoder().raw_decode(raw[json_start:])
    except json.JSONDecodeError as exc:
        return {}, f"invalid tandem-comments JSON: {exc}", raw_block
    if not isinstance(data, dict):
        return {}, "tandem-comments JSON is not an object", raw_block
    return data, "", raw_block


def scan_tandem_comment_pages(book_dir: Path) -> list[TandemCommentPage]:
    if not book_dir.exists():
        return []
    pages: list[TandemCommentPage] = []
    for path in sorted(book_dir.rglob("*.md")):
        if not path.is_file():
            continue
        text = read_text(path)
        if not SOURCE_BLOCK_RE.search(text):
            continue
        data, parse_error, raw_block = parse_tandem_block_from_text(text)
        if data or parse_error:
            pages.append(
                TandemCommentPage(
                    rel_path=path.relative_to(book_dir).as_posix(),
                    comments=data,
                    parse_error=parse_error,
                    raw_block=raw_block,
                )
            )
    return pages


def comment_pages_count(pages: list[TandemCommentPage]) -> int:
    return sum(len(page.comments) for page in pages) + sum(1 for page in pages if page.parse_error)


def manifest_skill_page_map(manifest: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for skill in manifest.get("skills", []) or []:
        if not isinstance(skill, dict):
            continue
        name = str(skill.get("name") or "").strip()
        page = str(skill.get("reading_page") or "").strip()
        if name and page:
            mapping[name] = page
    return mapping


def manifest_page_skill_map(manifest: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for skill in manifest.get("skills", []) or []:
        if not isinstance(skill, dict):
            continue
        name = str(skill.get("name") or "").strip()
        page = str(skill.get("reading_page") or "").strip()
        if name and page:
            mapping[page] = name
    return mapping


def load_existing_manifest(book_dir: Path) -> dict[str, Any]:
    manifest_path = book_dir / "manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(read_text(manifest_path))
    except json.JSONDecodeError:
        return {}


def unique_comment_id(existing: dict[str, Any], preferred: str) -> str:
    if preferred not in existing:
        return preferred
    idx = 2
    while f"{preferred}-{idx}" in existing:
        idx += 1
    return f"{preferred}-{idx}"


def candidate_comment_target(
    rel_path: str,
    book_dir: Path,
    old_manifest: dict[str, Any],
    new_manifest: dict[str, Any],
) -> str | None:
    if (book_dir / rel_path).exists():
        return rel_path
    old_page_to_skill = manifest_page_skill_map(old_manifest)
    new_skill_to_page = manifest_skill_page_map(new_manifest)
    skill = old_page_to_skill.get(rel_path)
    if skill and new_skill_to_page.get(skill):
        return new_skill_to_page[skill]
    return None


def append_tandem_comments(path: Path, comments: dict[str, Any]) -> None:
    text, existing = load_tandem(path)
    merged = dict(existing)
    for cid, item in comments.items():
        merged[unique_comment_id(merged, cid)] = item
    new_block = dump_tandem(merged)
    if SOURCE_BLOCK_RE.search(text):
        new_text = SOURCE_BLOCK_RE.sub(lambda _m: new_block, text)
    else:
        new_text = text.rstrip() + "\n\n" + new_block + "\n"
    write_text(path, new_text)


def build_comment_migration_doc(unresolved: list[dict[str, Any]]) -> str:
    lines = [
        "# 批注迁移待处理",
        "",
        "这些批注在重建阅读包时未能自动定位到新正文。原始批注数据已保留，等待人工处理。",
        "",
    ]
    for idx, item in enumerate(unresolved, start=1):
        lines.extend(
            [
                f"## {idx}. {item['source_page']} / {item['comment_id']}",
                "",
                f"- 原页面：`{item['source_page']}`",
                f"- 目标页面：`{item.get('target_page') or '未找到'}`",
                f"- 原因：{item['reason']}",
                "",
                "```json",
                json.dumps(item["comment"], ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_comment_migration_log(summary: dict[str, Any], restored: list[dict[str, Any]], unresolved: list[dict[str, Any]]) -> str:
    lines = [
        "# 批注迁移记录",
        "",
        f"- 发现批注：{summary['found']}",
        f"- 已恢复：{summary['restored']}",
        f"- 待处理：{summary['unresolved']}",
        f"- 来源页面数：{len(summary['source_pages'])}",
        "",
    ]
    if restored:
        lines.extend(["## 已恢复", ""])
        for item in restored:
            lines.append(
                f"- `{item['source_page']}` / `{item['comment_id']}` -> `{item['target_page']}`，"
                f"anchor_found={item['anchor'].get('found')}"
            )
        lines.append("")
    if unresolved:
        lines.extend(["## 待处理", ""])
        for item in unresolved:
            lines.append(
                f"- `{item['source_page']}` / `{item['comment_id']}` -> "
                f"`{item.get('target_page') or '未找到'}`：{item['reason']}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def restore_tandem_comments(
    book_dir: Path,
    pages: list[TandemCommentPage],
    old_manifest: dict[str, Any],
    new_manifest: dict[str, Any],
) -> dict[str, Any]:
    restored: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    comments_by_target: dict[str, dict[str, Any]] = {}
    malformed_count = 0

    for page in pages:
        target_rel = candidate_comment_target(page.rel_path, book_dir, old_manifest, new_manifest)
        if page.parse_error:
            malformed_count += 1
            unresolved.append(
                {
                    "source_page": page.rel_path,
                    "target_page": target_rel,
                    "comment_id": "__malformed_tandem_block__",
                    "reason": page.parse_error,
                    "comment": {"raw_block": page.raw_block},
                }
            )
            continue
        if not target_rel:
            for cid, item in page.comments.items():
                unresolved.append(
                    {
                        "source_page": page.rel_path,
                        "target_page": None,
                        "comment_id": cid,
                        "reason": "target page not found after rebuild",
                        "comment": item,
                    }
                )
            continue
        target_path = book_dir / target_rel
        if not target_path.exists():
            for cid, item in page.comments.items():
                unresolved.append(
                    {
                        "source_page": page.rel_path,
                        "target_page": target_rel,
                        "comment_id": cid,
                        "reason": "target page path does not exist after rebuild",
                        "comment": item,
                    }
                )
            continue
        target_text = read_text(target_path)
        for cid, item in page.comments.items():
            loc = locate_anchor(target_text, item)
            if loc["found"]:
                restored_item = dict(item)
                restored_anchor = dict(restored_item.get("anchor") or {})
                actual_pos = loc["actual_pos"]
                exact = str(restored_anchor.get("exact") or "")
                restored_anchor["pos"] = actual_pos
                restored_anchor["prefix"] = target_text[max(0, actual_pos - 40) : actual_pos]
                restored_anchor["suffix"] = target_text[actual_pos + len(exact) : actual_pos + len(exact) + 40]
                restored_item["anchor"] = restored_anchor
                comments_by_target.setdefault(target_rel, {})[cid] = restored_item
                restored.append(
                    {
                        "source_page": page.rel_path,
                        "target_page": target_rel,
                        "comment_id": cid,
                        "anchor": loc,
                    }
                )
            else:
                unresolved.append(
                    {
                        "source_page": page.rel_path,
                        "target_page": target_rel,
                        "comment_id": cid,
                        "reason": "anchor exact text not found in target page",
                        "comment": item,
                    }
                )
    for target_rel, comments in comments_by_target.items():
        append_tandem_comments(book_dir / target_rel, comments)

    summary = {
        "schema": "readerlab.comment-preservation.v1",
        "found": comment_pages_count(pages),
        "restored": len(restored),
        "unresolved": len(unresolved),
        "malformed_blocks": malformed_count,
        "source_pages": sorted(page.rel_path for page in pages),
        "report": "20_批注与讨论/批注迁移记录.md" if pages else "",
        "unresolved_page": "20_批注与讨论/批注迁移待处理.md" if unresolved else "",
    }
    if pages:
        write_text(book_dir / "20_批注与讨论" / "批注迁移记录.md", build_comment_migration_log(summary, restored, unresolved))
    if unresolved:
        write_text(book_dir / "20_批注与讨论" / "批注迁移待处理.md", build_comment_migration_doc(unresolved))
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="readerlab")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_import = sub.add_parser("import-skills")
    p_import.add_argument("source")
    p_import.add_argument("--dest", required=True)
    p_import.add_argument("--book-id")
    p_import.add_argument("--title")
    p_import.add_argument("--goal", default="学习这份材料的结构、方法和可复用经验。")
    p_import.add_argument("--readings-dir", default=str(DEFAULT_AGENT_READINGS_DIR))
    p_import.add_argument("--force", action="store_true")
    p_import.add_argument("--preserve-comments", action="store_true")
    p_import.set_defaults(func=import_skills)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("book_dir")
    p_validate.add_argument("--require-complete", action="store_true")
    p_validate.add_argument("--require-contracts", action="store_true")
    p_validate.add_argument("--require-human-accepted", action="store_true")
    p_validate.add_argument("--skill")
    p_validate.add_argument("--block")
    p_validate.set_defaults(func=validate_pack)

    p_validate_contract = sub.add_parser("validate-contract")
    p_validate_contract.add_argument("path")
    p_validate_contract.set_defaults(func=validate_contract_cmd)

    p_render_contract = sub.add_parser("render-contract-package")
    p_render_contract.add_argument("sample_dir")
    p_render_contract.add_argument("output_dir")
    p_render_contract.set_defaults(func=render_contract_package_cmd)

    p_eval_rendered = sub.add_parser("eval-rendered-package")
    p_eval_rendered.add_argument("path")
    p_eval_rendered.add_argument("--report-md")
    p_eval_rendered.add_argument("--overwrite-report", action="store_true")
    p_eval_rendered.set_defaults(func=eval_rendered_package_cmd)

    p_blocks = sub.add_parser("block-manifest")
    p_blocks.add_argument("skill_md")
    p_blocks.add_argument("--skill")
    p_blocks.add_argument("--source-file")
    p_blocks.set_defaults(func=block_manifest_cmd)

    p_list = sub.add_parser("comments-list")
    p_list.add_argument("path")
    p_list.set_defaults(func=comments_list)

    p_reply = sub.add_parser("comments-reply")
    p_reply.add_argument("path")
    p_reply.add_argument("comment_id")
    p_reply.add_argument("--text", required=True)
    p_reply.add_argument("--author", default="Codex")
    p_reply.set_defaults(func=comments_reply)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
