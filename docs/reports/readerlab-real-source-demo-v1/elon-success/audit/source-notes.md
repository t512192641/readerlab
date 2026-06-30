# elon-success source notes

## Source registry

- source_id: elon-success-v101-14
- material_type: book / longform chapter
- source_path: `/Users/tianqiang/LifeAtlas/200_原始资料/270_电子书与书籍资料/2026-06-20_埃隆之书_中文版.epub`
- epub_entry: `OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-14.xhtml`
- toc_title: 成功之道
- xhtml_internal_title: 成功要素
- source_role: complete primary chapter source
- coverage: full chapter
- chapter_sha256: `2d23768d77b3ebc724ae2aba7076fc1449c04d27bb8e9a81ce96a99e58fcecc9`

## TOC boundary

- `OEBPS/toc.xhtml` contains TOC title “成功之道”.
- `OEBPS/toc.ncx` contains `navPoint24` text “成功之道”.
- `navPoint24` points to `Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-14.xhtml#_idParaDest-24`.
- The same XHTML chapter contains child headings for the chapter body: “承担责任”, “掌握深度理解”, “睡在工厂车间”, “前线领导力”, “逆境锻造力量”, “吞玻璃与凝视深渊”.
- TOC/body title mismatch is preserved as a fact: TOC says “成功之道”; body heading says “成功要素”.

## Extraction method

- Read the EPUB with Python `zipfile` from the local source path.
- Parsed `OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-14.xhtml` as XHTML with `xml.etree.ElementTree`.
- Extracted all direct chapter body blocks before the `_idFootnotes` div.
- Extracted `_idFootnotes` as原书注释 and placed them before AI explanation in the reader.
- Converted XHTML headings, paragraphs, callout paragraphs, strong text, and footnote references into Markdown.

## Cleaning scope

- Decoded HTML entities.
- Normalized whitespace, line breaks, and footnote references.
- Preserved chapter order, headings, paragraph order, emphasized text, and note numbers.
- Did not summarize, compress, rewrite, or reorder the chapter body.
- Did not expose EPUB paths, source refs, location map, claim trace, or machine/human status in the reader page.

## Location refs

- raw_xhtml_chars: 73911
- body_blocks_before_notes: 67
- footnotes: 52
- extracted_headings:
- _idParaDest-24: 成功要素
- _idParaDest-25: 承担责任
- _idParaDest-26: 掌握深度理解
- _idParaDest-27: 睡在工厂车间
- _idParaDest-28: 前线领导力
- _idParaDest-29: 逆境锻造力量
- _idParaDest-30: 吞玻璃与凝视深渊

## Claim trace

| Reader claim | Source basis | Status |
|---|---|---|
| The chapter links responsibility, depth of understanding, factory-floor presence, frontline leadership, adversity and startup pain. | Extracted chapter headings and paragraph sequence. | source-supported |
| Extreme work intensity is contextual rather than a universal management rule. | Chapter body says hundred-hour weeks apply to emergency states and are not recommended as normal. | source-supported plus AI interpretation |
| Leadership is framed as shortening responsibility and cognition chains. | Paragraphs about CEO handling hardest problems, integrating engineering and spending decisions, and staying at the front line. | AI interpretation, source-grounded |
| Design asset cards are not required for this reader. | ReaderLab product spec requires design asset cards for Skill/engineering materials; this is a book chapter. | project-rule-supported |

## Human / machine status

- machine_status: epub_exists; toc_checked; chapter_entry_read; full_body_extracted; footnotes_extracted; reader_written; audit_written
- human_status: pending_reader_review

## Downgrade / refusal notes

- No claim is made that this is product ready.
- No claim is made that this is a full-book ReaderLab package.
- No claim is made that ReaderLab can automatically generate this page yet.
- No LifeAtlas formal 300/600/800 material was written.
