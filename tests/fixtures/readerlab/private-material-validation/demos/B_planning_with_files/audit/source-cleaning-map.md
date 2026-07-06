# Source Cleaning Map

| Source section / category | Reader body handling | Reason | Safety-critical | Reader-facing impact |
|---|---|---|---|---|
| YAML metadata: name, version, description, tools | condensed | Identifies purpose and trigger, but field syntax is not the reading body. | no | Used to define material scope. |
| Allowed tools | moved_to_audit | Tool permissions are runtime metadata, not the main method. | yes | Not shown directly; preserved as boundary that this was not executed. |
| PreToolUse / PostToolUse / Stop hooks | condensed | Hooks show the method is enforced by execution shell, but shell branching is too noisy for reader body. | yes | Reader page says runtime shell should not become ReaderLab architecture. |
| Session catchup commands | condensed | Recovery is a core design idea; command syntax is environment-specific. | yes | Reader page promotes recovery entry as design asset. |
| File placement table | kept | Explains where persistent memory lives. | yes | Cleaned body keeps project-directory placement principle. |
| Quick Start steps | kept | Core workflow. | yes | Cleaned body converts to prose workflow. |
| Context Window = RAM / Filesystem = Disk | kept | Central explanatory metaphor. | no | Reader page uses it as high-level design frame. |
| File purposes table | kept | Defines output artifacts. | yes | Cleaned body preserves `task_plan.md`, `findings.md`, `progress.md`. |
| Critical rules | kept | Contains trigger, update, error, and decision rules. | yes | Cleaned body preserves the operational spine. |
| 3-strike error protocol | kept | Important failure handling. | yes | Reader page promotes error as strategy input. |
| Read vs Write matrix | condensed | Useful but too table-heavy for reader body. | no | Design asset notes convert it into state externalization. |
| Template references | moved_to_audit | Implementation detail. | no | Not part of reader-facing method. |
| Claude plugin directory conventions | rejected_for_reader_body | Host-specific runtime shell. | no | Explicitly rejected as ReaderLab default architecture. |
