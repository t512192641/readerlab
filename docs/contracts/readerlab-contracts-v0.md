# ReaderLab Contracts v0

## 状态

- 契约状态：薄骨架，可审查，尚未实现为 JSON Schema。
- 目的：在重做高质量样张前，定义最低事实层契约。
- 与既有 schema 的关系：`global-map.v1.schema.json` 和 `distillation.v1.schema.json` 仍是 v0.4/v0.5 的早期草案。本文件先拆出下一阶段需要的契约语义，再决定是否实现代码校验。

## 共享规则

每个契约都必须包含：

- `schema`：契约名称和版本。
- `material`：`id`、`title`、`type`，可用时记录 source package 或 book id、target package id。
- `source_scope`：来源范围、覆盖状态、覆盖率或说明、抽取方法、coverage note。
- `location_refs`：指向 source registry 和 location map 的引用。
- `confidence`：`level`、`basis` 和已知不确定性。
- `review_items`：具体待复核问题，带 `status`。
- `machine_status`：结构状态，如 `draft`、`ready`、`needs_review`、`blocked`。
- `human_status`：`pending`、`accepted`、`rejected`、`not_required`。
- `display`：事实层和 Markdown 展示层的关系。

允许的 coverage status：

- `toc_only`：只有目录、标题、元信息或 manifest。
- `partial`：覆盖一个或多个明确来源范围。
- `sample`：代表性样本，不足以支持总体主张。
- `full`：完整相关正文已覆盖。
- `unknown`：覆盖情况尚不可信。

任何契约都不能从 `machine_status`、validate 通过或文件存在推导出人工验收通过。

展示层必须区分两类输出：

- `reader_facing`：读者第一次阅读、批注和讨论需要的正文、路线、局部解释和必要来源提示。
- `internal_audit`：hash、coverage 明细、validator 结果、机器状态、未写入正式区、worker 执行证据等审计信息。

读者页不得把 `internal_audit` 内容当作正文段落反复展示；它可以链接到 README、report、appendix 或契约 JSON。

## `source-registry.v1`

### 负责什么

记录阅读包的来源库存和抽取溯源。

### 最小字段

```json
{
  "schema": "readerlab.source-registry.v1",
  "material": {
    "id": "",
    "title": "",
    "type": "",
    "target_package_id": ""
  },
  "sources": [
    {
      "source_id": "",
      "source_path": "",
      "source_type": "",
      "source_role": "",
      "version_or_commit": "",
      "content_hash": "",
      "extraction_method": "",
      "extraction_status": "",
      "coverage_role": "",
      "trust_notes": [],
      "review_items": []
    }
  ],
  "source_scope": {
    "coverage_status": "",
    "coverage_ratio": null,
    "coverage_note": ""
  },
  "machine_status": "draft",
  "human_status": "pending"
}
```

### 校验意图

- 每个高层地图或提炼项都必须引用一个或多个 `source_id`。
- `full` coverage 必须由 source count、source role 或 source-specific coverage note 支撑。
- 外部 parser 或 OCR 结果必须能追溯到原始来源。

### Agent / 脚本边界

- 脚本：收集路径、文件类型、hash、抽取状态、可用的 version/commit。
- Agent：判断 source role、trust notes、coverage meaning，以及覆盖率是否支持某个主张。

## `location-map.v1`

### 负责什么

记录稳定来源位置，让主张和批注能指回原文。

### 最小字段

```json
{
  "schema": "readerlab.location-map.v1",
  "material": {
    "id": "",
    "title": "",
    "type": ""
  },
  "locations": [
    {
      "location_id": "",
      "source_id": "",
      "path": "",
      "spine": "",
      "page": null,
      "heading_path": [],
      "block_id": "",
      "char_range": [0, 0],
      "text_preview": "",
      "extraction_confidence": "",
      "review_required": false
    }
  ],
  "source_scope": {
    "coverage_status": "",
    "coverage_note": ""
  },
  "machine_status": "draft",
  "human_status": "pending"
}
```

### 校验意图

- 书籍引用在没有页码时优先使用 EPUB spine / chapter / char range。
- PDF 引用在可用时包含 page / block。
- Markdown 或 Skill 包引用包含 path、heading path、char range 或 block ID。
- 当存在更窄位置时，不允许只引用模糊包级来源。

### Agent / 脚本边界

- 脚本：抽取 heading、spine、block、char range、text preview、confidence。
- Agent：选择哪个位置支撑主张，并标记需要复核的位置。

## `catalog-map.v1`

### 负责什么

基于 TOC、元信息、前言、标题、manifest 或有限结构扫描生成阅读路线假设。它不是 grounded full-material understanding。

### 最小字段

```json
{
  "schema": "readerlab.catalog-map.v1",
  "material": {
    "id": "",
    "title": "",
    "type": ""
  },
  "source_scope": {
    "coverage_status": "toc_only",
    "coverage_ratio": null,
    "coverage_note": ""
  },
  "catalog": {
    "top_level_structure": [],
    "route_hypothesis": [],
    "likely_core_questions": [],
    "known_covered_units": [],
    "not_yet_covered_units": []
  },
  "location_refs": [],
  "confidence": {
    "level": "low",
    "basis": []
  },
  "review_items": [],
  "machine_status": "draft",
  "human_status": "pending",
  "display": {
    "markdown_path": "",
    "relationship": "renders_from_contract"
  }
}
```

### 校验意图

- 可以在完整阅读前为整本书存在。
- 不能声称 full-body understanding。
- 必须标出已覆盖和未覆盖单元。
- 除非来源证据支持，否则 confidence 只能低或中。

### Agent / 脚本边界

- 脚本：抽取 TOC / headings 和已知覆盖来源单元。
- Agent：写 route hypothesis、likely questions 和 review items。

## `grounded-global-map.v1`

### 负责什么

当来源覆盖足以支撑全局主张时，为书籍、长文或混合材料生成 source-grounded 全局理解。

### 最小字段

```json
{
  "schema": "readerlab.grounded-global-map.v1",
  "material": {
    "id": "",
    "title": "",
    "type": ""
  },
  "source_scope": {
    "coverage_status": "full",
    "coverage_ratio": 1.0,
    "coverage_note": ""
  },
  "global_map": {
    "core_questions": [],
    "structure_mainline": [],
    "unit_relationships": [],
    "concept_method_case_relationships": [],
    "counterexamples_or_limits": [],
    "reading_routes": []
  },
  "location_refs": [],
  "claim_refs": [],
  "confidence": {
    "level": "",
    "basis": []
  },
  "review_items": [],
  "machine_status": "draft",
  "human_status": "pending",
  "display": {
    "markdown_path": "",
    "relationship": "renders_from_contract"
  }
}
```

### 校验意图

- `coverage_status=full` 必须有 registry evidence。
- 每个主要判断都应有 `claim_refs`。
- 反例、边界和未解决问题是必填，不是润色项。
- 不能从 TOC-only 或一个局部章节生成。

### Agent / 脚本边界

- 脚本：校验 registry coverage、claim ref 语法和必填字段。
- Agent：产出核心问题、主线、关系、边界和读者路线。

## `local-deepread.v1`

### 负责什么

在明确的局部来源范围内，为一个章节、部件、文章片段、课程单元或 Skill 子集生成可复核的局部深读。它只能回答“这一段材料里能读出什么”，不能冒充全书地图、整包能力地图或完整材料理解。

### 最小字段

```json
{
  "schema": "readerlab.local-deepread.v1",
  "material": {
    "id": "",
    "title": "",
    "type": "",
    "parent_material_id": ""
  },
  "source_scope": {
    "coverage_status": "partial",
    "coverage_ratio": null,
    "coverage_note": "",
    "location_precision_required": "heading_or_block_or_char",
    "precision_exception_note": ""
  },
  "local_deepread": {
    "covered_unit": "",
    "covered_source_files": [],
    "reading_thesis": "",
    "reader_gain": "",
    "mechanism_chain": [],
    "reading_route": [],
    "deepread_cards": [
      {
        "card_id": "",
        "card_type": "framework",
        "title": "",
        "reader_takeaway": "",
        "source_refs": [],
        "primary_location_refs": [],
        "case_refs": [],
        "counterexample_refs": [],
        "term_refs": [],
        "applicability_boundary": "",
        "verification": {
          "v1_cross_context": {
            "status": "pending",
            "evidence_contexts": []
          },
          "v2_predictive_power": {
            "status": "pending",
            "novel_question": "",
            "derived_answer": ""
          },
          "v3_distinctiveness": {
            "status": "pending",
            "why_not_common": ""
          }
        },
        "review_status": "open"
      }
    ],
    "distillation_candidates": [],
    "misread_guards": []
  },
  "location_refs": [],
  "claim_refs": [
    {
      "claim_id": "",
      "claim": "",
      "primary_location_refs": [],
      "derived_location_refs": [],
      "applicability_boundary": "",
      "confidence": "",
      "review_status": "open"
    }
  ],
  "confidence": {
    "level": "",
    "basis": [],
    "known_uncertainties": []
  },
  "review_items": [],
  "machine_status": "draft",
  "human_status": "pending",
  "display": {
    "reader_markdown_path": "",
    "audit_markdown_path": "",
    "relationship": "renders_from_contract",
    "reader_audit_policy": "reader page links audit, audit details stay out of main reading body"
  }
}
```

### 校验意图

- `source_scope.coverage_status` 通常应为 `partial`；只允许指向明确命名的局部范围。
- `covered_unit` 和 `covered_source_files` 必须足够具体，能和 source registry / location map 对齐。
- 每个 `reading_route` 步骤、`deepread_cards` 和提炼候选都应有 source refs；提炼候选还应有 item-level `claim_refs`、适用边界和 confidence。
- `deepread_cards.card_type` 至少支持 `framework`、`principle`、`case`、`counterexample`、`term`、`transfer_insight`；没有对应内容时不强行凑数，但必须记录为什么为空或降级。
- 高价值卡片必须记录 V1/V2/V3 验证状态；未验证只能是 `pending` 或 `failed`，不能写成可迁移结论。
- `claim_refs.primary_location_refs` 优先指向一手来源或读者正文中的原文 span；派生提炼页只能作为 `derived_location_refs` 或辅助证据，不能当主要证据。
- 局部深读不能被后续展示层改名成全书理解、完整能力地图或 accepted 人工结论。
- 读者 Markdown 不展示完整机器审计；审计信息进入 `display.audit_markdown_path` 或契约 JSON。

### Agent / 脚本边界

- 脚本：抽取局部来源文件、章节位置、block/line/char refs，并校验 claim refs 指向已登记 location。
- Agent：判断 reading thesis、局部路线、提炼候选、适用边界、误读防线和仍需人工复核的问题。

## `capability-map.v1`

### 负责什么

理解 Skill/package 的能力结构。它回答：遇到什么问题用哪个能力，为什么用，产出什么，怎么验收。

### 最小字段

```json
{
  "schema": "readerlab.capability-map.v1",
  "material": {
    "id": "",
    "title": "",
    "type": "skill_package",
    "version_or_commit": ""
  },
  "source_scope": {
    "coverage_status": "",
    "coverage_ratio": null,
    "coverage_note": ""
  },
  "suite_overview": {
    "job_family": "",
    "primary_users": [],
    "not_for": [],
    "route_summary": [],
    "coverage_plan": {
      "inventory_status": "sample",
      "known_total_units": null,
      "covered_units": [],
      "not_yet_covered_units": []
    }
  },
  "capability_domains": [
    {
      "domain_id": "",
      "name": "",
      "owned_job": "",
      "trigger_signals": [],
      "near_neighbor_exclusions": [],
      "method_atoms": [],
      "required_inputs": [],
      "output_contract": [],
      "verification": [],
      "route_decisions": [
        {
          "when_to_use": [],
          "when_not_to_use": [],
          "handoff_to": [],
          "route_conflicts": [],
          "decision_evidence_refs": []
        }
      ],
      "source_refs": [],
      "confidence": {
        "level": "",
        "basis": []
      },
      "review_items": []
    }
  ],
  "cross_skill_routes": [],
  "reader_routes": [
    {
      "route_id": "",
      "reader_goal": "",
      "steps": [],
      "expected_output": "",
      "verification_checkpoint": ""
    }
  ],
  "location_refs": [],
  "machine_status": "draft",
  "human_status": "pending",
  "display": {
    "reader_markdown_path": "",
    "audit_markdown_path": "",
    "relationship": "renders_from_contract",
    "reader_audit_policy": "reader page explains capability choices; inventory and validation details live in audit output"
  }
}
```

### 校验意图

- 能力域不能只是文件名、文件夹名或目录项。
- 至少需要 trigger signals、method atoms、output contract、verification、source refs 和 confidence。
- `route_decisions` 必须说明何时用、何时不用、冲突时交给哪个能力或标记 review item。
- `reader_routes` 必须解释人如何理解这个包，而不是只列 source order。
- sample coverage 不能伪装成 24 Skills full coverage；`coverage_plan` 必须暴露未覆盖单元。
- 跨 Skill 路由不确定性必须变成 review items。

### Agent / 脚本边界

- 脚本：扫描 `SKILL.md`、package metadata、references、scripts、tests 和路径；校验 source refs。
- Agent：分组能力、解释触发、抽取方法原子、定义输出契约和读者路线。

## 最小 validate 设计

后续如果要改代码，第一步应只做契约校验 helper，不做地图生成。

有用检查：

- 必填顶层字段存在。
- `schema` 属于 v1 契约名之一。
- `source_scope.coverage_status` 合法。
- `human_status` 和 `machine_status` 同时存在且分离。
- `catalog-map.v1` 不能使用 `coverage_status=full`。
- `grounded-global-map.v1` 不能使用 `toc_only`、`sample`、`partial` 或 `unknown`。
- `local-deepread.v1` 必须绑定明确局部来源范围，不能使用 `coverage_status=full` 支撑全书级主张。
- `local-deepread.v1` 的高价值深读卡必须有 primary location refs、适用边界和 V1/V2/V3 状态。
- `capability-map.v1` 至少有一个能力域，且包含 trigger signals、method atoms、output contract、verification、source refs、route decisions。
- `capability-map.v1` 如为 sample coverage，必须有 `coverage_plan.not_yet_covered_units` 或 review item，不得暗示全量。
- 展示层如果有读者 Markdown 和 audit Markdown，二者必须分开；读者正文不得把 validator 通过、hash、pending 说明当阅读主线。
- 每个 source ref 指向 `source-registry.v1`，可能时也指向 `location-map.v1`。

本契约步骤不实现生成逻辑，也不把生成逻辑塞进 `scripts/readerlab.py`。只有样张契约稳定后，才讨论最小 validate 代码。
