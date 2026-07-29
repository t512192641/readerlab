# Input contract

`init` receives exactly three regular, non-symlink files:

| Flag | Copied run path | Meaning |
|---|---|---|
| `--source` | `inputs/source.md` | The fixed original text. Its bytes are never rewritten. |
| `--framework` | `inputs/framework.md` | The human-selected external framework identity. No discovery is performed. |
| `--source-map` | `inputs/source-map.md` | The frozen source allowlist and provenance boundary. |

The command also requires `--run` to name a new directory and `--skill-version 0.1.0`. It records original path, copied path, byte count, SHA-256, and a Skill fingerprint. A source map URL is an allowlist entry, not permission to search for alternatives.

The Expert and reviewer tasks receive closed local read sets. A file outside those sets is `unknown`; the Skill does not claim an OS sandbox.
