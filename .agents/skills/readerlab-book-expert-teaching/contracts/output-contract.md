# Output and archive contract

Every run contains `inputs/`, `control/`, `raw/`, `acceptance/`, `run.json`, `run-manifest.md`, and `run-ledger.md`.

The Expert writes only:

- `raw/expert-teaching-draft.md`
- `raw/expert-teaching-source-map.md`

The reviewer writes only `acceptance/expert-teaching-review.md`. The controller writes stage freeze files and, after dual PASS only, `acceptance/expert-product-review.md`.

The product package contains a readable Markdown rendering of the frozen source, the complete Expert course, and fixed product questions. It excludes the source map, technical scores, old drafts, Writer/route material, and M1/M2/M3 labels. Raw XHTML is rejected.

`archive` runs `verify` first, refuses an existing destination and a destination inside the run, writes a tar.gz with the run contents, and prints the archive SHA-256 and entry count. The archive hash is never written inside the archive itself.
