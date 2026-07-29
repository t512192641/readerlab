# Input contract

`init` receives four regular, non-symlink files:

| Flag | Copied run path | Meaning |
|---|---|---|
| `--source` | `inputs/source.md` | The fixed original text. Its bytes are never rewritten. |
| `--framework` | `inputs/framework.md` | The human-selected external framework identity. No discovery is performed. |
| `--source-map` | `inputs/source-map.md` | The frozen source allowlist and provenance boundary. |
| `--source-allowlist` | `inputs/source-allowlist.json` | A machine-readable allowlist with explicit `allowed`, `reference_only`, and `blocked` entries plus registered redirects. |

The command also requires `--run` to name a new directory and `--skill-version 0.1.1`. It records original path, copied path, byte count, SHA-256, and a version-local Skill fingerprint. URLs are never extracted from the source map: only `allowed` URLs and explicitly registered redirects enter task read sets. `reference_only` can be cited for audit context but cannot be opened; `blocked` cannot be cited or opened.

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
