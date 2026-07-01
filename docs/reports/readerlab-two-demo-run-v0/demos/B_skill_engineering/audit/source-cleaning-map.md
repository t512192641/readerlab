# Demo B Source Cleaning Map

This file is audit-only. It records how the selected `gstack/spec/SKILL.md` source was cleaned into `10_一手正文/001_净化正文.md`. The original source remains a local read-only source path; this map lets reviewers inspect the cleaning decisions without treating runtime shell as reader body.

| Source section / category | Reader body treatment | Audit / design treatment | Safety-critical | Reason |
|---|---|---|---|---|
| Frontmatter name, description, triggers | kept | also recorded in source registry and body anchors | yes | Defines when the Skill owns a task; without this, `spec` could swallow unrelated workflows. |
| When to invoke this skill | kept | linked to `B-BODY-001`, claim `C1` | yes | Preserves purpose, trigger, and user intent. |
| Preamble runtime checks | condensed | moved to runtime shell category in `B-BODY-003` and this map | partial | Branch, session, telemetry, routing, vendoring, and model checks matter for execution, but not as the main reading body. |
| Upgrade, telemetry, proactive routing, vendoring prompts | condensed / moved out of reader body | design pattern "environment aware but not main line"; rejected as ReaderLab default by `C8` / `K4` | partial | These are foreign runtime maintenance flows. They should not become ReaderLab defaults, but their opt-in and boundary design are useful. |
| AskUserQuestion format and fallback rules | kept / condensed | design asset "decision questions"; claims `C2`, `C5` | yes | This is a core reusable method: decisions must expose stakes, recommendation, options, and fallback behavior. |
| Plan mode and spawned session handling | condensed | body anchor `B-BODY-003`, design asset "automation boundaries" | yes | Relevant to multi-agent safety, but too host-specific for full reader body. |
| /spec process phases 1-5 | kept | body anchor `B-BODY-002`; claims `C2`, `C6`, `C7`; candidates `K1`, `K7` | yes | This is the operational spine: why, scope, evidence, draft review, gate, file/archive/handoff. |
| Redaction and quality gates | kept / condensed | body lines 21 and 37; trace `B-READ-003` | yes | Prevents specs from moving unsafe or unreviewed content downstream. |
| Issue filing, archive, optional spawned execution | kept / condensed | claim `C7`; body lines 23 and 41 | yes | Defines output requirements and handoff boundary. |
| Telemetry implementation commands, shell snippets, local paths, analytics files | moved to audit only / rejected from reader body | source registry plus this map; not in reader-facing | no for reading, partial for execution | These are machine protocol and host-local maintenance details; including them would pollute the reader body. |
| Issue quality standards and templates | condensed | body line 41 and design asset "handoff spec" | yes | Keeps output requirements without copying the full template wall into the reader body. |
| Voice, context recovery, completion footer | condensed | design asset "environment aware" and "handoff" | partial | Useful as product design evidence, but not the main method for ReaderLab readers. |

## Cleaning Decision

The cleaned body is not a summary of the source's topic. It preserves the operational spine that a reader needs to understand the Skill as a demand-specification workflow:

1. trigger boundary;
2. user intent;
3. why-first interrogation;
4. scope and boundary lock;
5. evidence-before-technical-questions;
6. draft review and user confirmation;
7. quality and redaction gates;
8. issue / archive / handoff outputs;
9. runtime shell separation;
10. automation boundaries and failure risks.

Runtime shell details were not deleted from the evidence model; they were moved out of the reader body so they can be inspected without becoming the main reading experience.
