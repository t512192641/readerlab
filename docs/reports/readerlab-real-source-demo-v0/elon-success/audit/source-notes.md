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

## Source confirmation

- TOC confirms `navPoint24` text is “成功之道”.
- TOC confirms `navPoint24` points to `Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-14.xhtml#_idParaDest-24`.
- TOC child nodes under the same XHTML include “担当责任 / 深入理解 / 睡在工厂车间 / 前线领导 / 逆境淬炼力量 / 直面深渊”.
- Programmatic extraction read exactly `OEBPS/Eric-Jorgenson_The-Book-of-Elon_PRODUCTION_v101-14.xhtml` from the local EPUB.
- TOC match observed: True.

## Location refs

- XHTML raw chars: 73911
- Extracted body blocks before notes: 67
- Extracted note blocks: 52
- Headings extracted from chapter body:
  - 成功要素
- 承担责任
- 掌握深度理解
- 睡在工厂车间
- 前线领导力
- 逆境锻造力量
- 吞玻璃与凝视深渊

## Processing notes

- The local EPUB chapter was checked as a complete chapter unit.
- The repo reader page no longer stores the full copyrighted chapter body.
- The reader page keeps only chapter structure, a few very short locating excerpts, and the post-reading explanation shape.
- Full original text should remain in the local private EPUB or a private LifeAtlas reading package, not in a portable repo report.
- No claim is made that this repo preview alone satisfies the full book/longform original-text track.

## Claim trace

| Reader claim | Source basis |
|---|---|
| The chapter connects responsibility, deep understanding, factory-floor presence and frontline leadership. | Chapter headings and paragraph sequence in `v101-14.xhtml`. |
| The explanation treats extreme work as conditional, not universal management advice. | AI interpretation based on the chapter’s repeated emphasis on hard problems, factory presence, failure, adversity, and limits of delegation. |
| No design asset card is included as a required track. | Product spec says design asset cards are mandatory for Skill/engineering materials, not book chapters. |
| Repo preview does not include full original chapter body. | Copyright and portability boundary; full text remains local/private. |

## Status

- machine_status: epub_exists; toc_checked; chapter_entry_read; full_chapter_body_extracted; demo_written
- human_status: pending_reader_review

## Downgrade / refusal notes

- This is not product ready.
- This is not a full-book ReaderLab package.
- This repo preview is not a full original-text reader page; it is a copyright-safe chapter-level preview.
- The chapter title has a TOC/body mismatch: TOC says “成功之道”, XHTML heading says “成功要素”. Reader title follows the requested TOC title; audit records the mismatch.
- No design asset card was generated for the book demo because this scene is not Skill/engineering material.
