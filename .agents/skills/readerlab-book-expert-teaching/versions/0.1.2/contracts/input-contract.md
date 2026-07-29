# Input contract

`init` receives four regular, non-symlink files:

| Flag | Copied run path | Meaning |
|---|---|---|
| `--source` | `inputs/source.md` | The fixed original text. Its bytes are never rewritten. |
| `--framework` | `inputs/framework.md` | The human-selected external framework identity. No discovery is performed. |
| `--source-map` | `inputs/source-map.md` | The frozen source attribution/evidence boundary: the human-readable claims-to-source record. |
| `--source-allowlist` | `inputs/source-allowlist.json` | The machine-readable network-permission boundary with explicit `allowed`, `reference_only`, and `blocked` entries plus exact registered redirects. |

The command also requires `--run` to name a new directory and `--skill-version 0.1.2`. It records original path, copied path, byte count, SHA-256, and a version-local Skill fingerprint. `init` extracts URLs from the source map only to prove closure: every canonical allowlist URL must occur in the map, every map URL must be registered, and only explicitly registered redirects may be extra. Only `allowed` URLs and explicitly registered redirects enter task read sets. `reference_only` can be cited for audit context but cannot be opened; `blocked` cannot be cited or opened.

The access receipt schema is `readerlab-book-expert-teaching/source-access/v1`:

```json
{
  "schema": "readerlab-book-expert-teaching/source-access/v1",
  "opened_urls": [],
  "cited_only_urls": [],
  "provenance": "agent_declared",
  "audit_scope": "agent-declared; not a browser or OS-level network audit"
}
```

The receipt records the agent's declaration, not browser or OS-level network telemetry. `opened_urls` is limited to `allowed` URLs and explicit redirects; `cited_only_urls` accepts `allowed` or `reference_only` URLs. Arrays must be disjoint and exact.

The allowlist schema is `readerlab-book-expert-teaching/source-allowlist/v1`:

```json
{
  "schema": "readerlab-book-expert-teaching/source-allowlist/v1",
  "sources": [
    {"id": "primary", "url": "https://example.test/primary", "status": "allowed", "redirects": []},
    {"id": "context", "url": "https://example.test/context", "status": "reference_only", "redirects": []},
    {"id": "failed", "url": "https://example.test/blocked", "status": "blocked", "redirects": []}
  ]
}
```

The Expert and reviewer tasks receive closed local read sets. A file outside those sets is `unknown`; the Skill does not claim an OS sandbox.
