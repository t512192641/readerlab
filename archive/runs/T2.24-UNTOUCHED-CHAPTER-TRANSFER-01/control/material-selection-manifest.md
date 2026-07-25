# T2.24 材料选择与冻结清单

status: PASS
started-at-utc: `2026-07-22T19:03:28.797776+00:00`
ended-at-utc: `2026-07-22T19:03:28.799341+00:00`
duration-ms: `1`
model-calls: `0`
provider-token-usage: `not-applicable`

## 冻结来源

- EPUB：`materials/T2.4-IDEA-PILOT-01/source.epub`
- size-bytes: `672638`
- sha256: `3baf9932c92412f0e7d0ccae993182f55f62e2fab5ec46a3882d675476288664`
- structural-inputs: `toc.ncx`, ZIP member names/sizes/hashes
- excluded-chapters: `13,14,15,19`

## 匿名 eligible IDs

- `text/part0005.html`
- `text/part0006.html`
- `text/part0007.html`
- `text/part0008.html`
- `text/part0010.html`
- `text/part0011.html`
- `text/part0012.html`
- `text/part0013.html`
- `text/part0014.html`
- `text/part0016.html`
- `text/part0017.html`
- `text/part0018.html`
- `text/part0023.html`
- `text/part0024.html`
- `text/part0025.html`
- `text/part0028.html`
- `text/part0029.html`

## 确定性选择

- payload-sha256: `1a7e1f339454295372eae9664b96e57be3b0a487b42a76d5974edb3843d1d4e5`
- selector: `uint64(payload_sha256[0:16], hex) mod 17`
- selected-index-zero-based: `12`
- selected-member: `text/part0023.html`
- selected-title-from-toc: `第16章 正义：人类的道德困境`

## 冻结正文

- member-size-bytes: `20734`
- member-sha256: `7c6ed38328d12491245bf1ad1cb325b0bcf43e4e2e245933860813f296e0d025`
- scope: `first <h2 class="calibre15" through byte before <ol class="duokan-footnote-content1">`
- scope-size-bytes: `16368`
- scope-sha256: `1c7973468c9d2716aee142de2d985a8f64d26ee673ae4a83c7e9d74d55c8804c`
- output: `runs/T2.24-UNTOUCHED-CHAPTER-TRANSFER-01/inputs/chapter-scope.xhtml`

选择前未读取任何 eligible member 正文；只有选择结果冻结后才读取并提取 `selected-member`。
