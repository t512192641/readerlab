# Output and archive contract

Every run contains `inputs/`, `control/`, `raw/`, `acceptance/`, `run.json`, `run-manifest.md`, and `run-ledger.md`.

The Expert writes only:

- `raw/expert-teaching-draft.md`
- `raw/expert-teaching-source-map.md`
- `raw/expert-source-access.json`

The reviewer writes only:

- `acceptance/expert-teaching-review.md`
- `acceptance/reviewer-source-access.json`

The controller writes `control/source-boundary.json`, stage freeze files, and, after dual PASS only, `acceptance/expert-product-review.md`. Both access receipts are frozen, listed in the manifest/ledger, verified, and archived.

The product package contains a readable Markdown rendering of the frozen source, the complete Expert course, and fixed Chinese product questions. It excludes internal file paths, control titles, scoring metadata, old drafts, Writer/route control metadata, and explicit ReaderLab depth self-labels. Natural occurrences of `M1`, `M2`, `M3`, or `Writer` in the fixed source or teaching prose are allowed. Raw XHTML is rejected.

`archive` runs `verify` first, refuses an existing destination and a destination inside the run, writes a tar.gz with the run contents, and prints the archive SHA-256 and entry count. The archive hash is never written inside the archive itself.
