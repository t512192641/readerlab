import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const toolPath = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(toolPath), "..");

const paths = {
  b1: path.join(root, "inputs/chapter-readable.md"),
  expert: path.join(root, "inputs/D3-expert.md"),
  writer: path.join(root, "inputs/writer-v2-accepted.md"),
  readerOut: path.join(root, "candidates/reader-unit-assembly-v1.md"),
  chapterOut: path.join(root, "candidates/chapter-with-reader-v1.md"),
  receiptOut: path.join(root, "evidence/mechanical-receipt.json"),
};

const expected = {
  b1: "c936cde2923eb1ea1beb199414026cefd70ada16467aa8f73aece8b9bfa6242b",
  expert: "22e8226fc131c74bb522e3f6a292b0e799dd3bac77116318455f24dd67f6b8c6",
  writer: "6207fbe799221edc1c7d7c25d090f12e6eb70dc2def5ef56d342860705c95325",
};

function read(file) {
  return fs.readFileSync(file, "utf8");
}

function sha256(value) {
  return crypto.createHash("sha256").update(value, "utf8").digest("hex");
}

function count(haystack, needle) {
  if (!needle) throw new Error("Empty needle");
  return haystack.split(needle).length - 1;
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const b1 = read(paths.b1);
const expert = read(paths.expert);
const writer = read(paths.writer);

assert(sha256(b1) === expected.b1, "B1 hash mismatch");
assert(sha256(expert) === expected.expert, "Expert hash mismatch");
assert(sha256(writer) === expected.writer, "Writer v2 hash mismatch");

const anchorHeading = "### 实际触发本课的完整段落（逐字）\n\n> ";
assert(count(expert, anchorHeading) === 1, "Expert actual-trigger heading is not unique");
const quotedStart = expert.indexOf(anchorHeading) + anchorHeading.length;
const quotedEnd = expert.indexOf("\n\n", quotedStart);
assert(quotedEnd > quotedStart, "Expert actual-trigger paragraph end not found");
const anchor = expert.slice(quotedStart, quotedEnd);
assert(!anchor.includes("\n"), "Expected one-line frozen anchor paragraph");
assert(count(b1, anchor) === 1, "Frozen anchor is not unique in complete B1");

const definitionNeedle =
  "普通交易里，增加收益会提高接受方案的理由。禁忌交换里，物质加码还会使";
const definitionReplacement =
  "普通交易里，增加收益会提高接受方案的理由。所谓“禁忌交换”，就是拿金钱、便利等世俗利益去交换被视为身份义务的东西。禁忌交换里，物质加码还会使";
const symbolicNeedle = "象征性承认降低了部分极端反应";
const symbolicReplacement = "象征性承认降低了部分愤怒和暴力反对指标";

assert(count(writer, definitionNeedle) === 1, "Definition insertion point is not unique");
assert(count(writer, symbolicNeedle) === 1, "Symbolic-evidence replacement point is not unique");
assert(count(writer, definitionReplacement) === 0, "Definition is already present in source");
assert(count(writer, symbolicReplacement) === 0, "Symbolic replacement is already present in source");

const reader = writer
  .replace(definitionNeedle, definitionReplacement)
  .replace(symbolicNeedle, symbolicReplacement);

assert(count(reader, definitionReplacement) === 1, "Definition patch failed");
assert(count(reader, symbolicReplacement) === 1, "Symbolic patch failed");
assert(
  reader
    .replace(definitionReplacement, definitionNeedle)
    .replace(symbolicReplacement, symbolicNeedle) === writer,
  "Reader contains changes outside the two authorized replacements",
);

const readerId = "T235-D3-READER-V2-A1";
const startMarker =
  `<!-- readerlab-candidate-only:reader-unit-start id="${readerId}" -->`;
const endMarker =
  `<!-- readerlab-candidate-only:reader-unit-end id="${readerId}" -->`;
assert(reader.endsWith("\n"), "Reader candidate must end with one frozen newline");
const insertBlock = `\n\n${startMarker}\n\n${reader}${endMarker}`;
const insertionOffset = b1.indexOf(anchor) + anchor.length;
const assembled =
  b1.slice(0, insertionOffset) + insertBlock + b1.slice(insertionOffset);

assert(count(assembled, startMarker) === 1, "Start marker is not unique");
assert(count(assembled, endMarker) === 1, "End marker is not unique");
assert(count(assembled, anchor) === 1, "Anchor drifted after assembly");
const recoveredB1 =
  assembled.slice(0, insertionOffset) +
  assembled.slice(insertionOffset + insertBlock.length);
assert(recoveredB1 === b1, "Removing insertion does not recover exact B1");

const readerStart = assembled.indexOf(startMarker) + startMarker.length + 2;
const readerEnd = assembled.indexOf(endMarker);
const recoveredReader = assembled.slice(readerStart, readerEnd);
assert(recoveredReader === reader, "Assembled Reader bytes drifted");

fs.writeFileSync(paths.readerOut, reader, "utf8");
fs.writeFileSync(paths.chapterOut, assembled, "utf8");

const receipt = {
  schema: "readerlab-writer-assembly-mechanical-receipt/v1",
  reader_id: readerId,
  start_head: "90c94450e5d4550da78d775111d364167542f5cd",
  source: {
    b1_sha256: sha256(b1),
    b1_bytes: Buffer.byteLength(b1, "utf8"),
    expert_sha256: sha256(expert),
    writer_v2_sha256: sha256(writer),
  },
  anchor: {
    owner: "inputs/D3-expert.md#实际触发本课的完整段落（逐字）",
    sha256: sha256(anchor),
    bytes: Buffer.byteLength(anchor, "utf8"),
    b1_occurrences: count(b1, anchor),
    insertion_offset_utf8_bytes: Buffer.byteLength(
      b1.slice(0, insertionOffset),
      "utf8",
    ),
    relation: "insert_after_exact_paragraph",
  },
  patches: [
    {
      id: "DEFINE_TABOO_TRADEOFF",
      old_occurrences: count(writer, definitionNeedle),
      new_occurrences: count(reader, definitionReplacement),
    },
    {
      id: "NARROW_SYMBOLIC_METRICS",
      old_occurrences: count(writer, symbolicNeedle),
      new_occurrences: count(reader, symbolicReplacement),
    },
  ],
  output: {
    reader_sha256: sha256(reader),
    reader_bytes: Buffer.byteLength(reader, "utf8"),
    chapter_sha256: sha256(assembled),
    chapter_bytes: Buffer.byteLength(assembled, "utf8"),
    recovered_b1_sha256: sha256(recoveredB1),
    recovered_reader_sha256: sha256(recoveredReader),
    exact_b1_recovery: recoveredB1 === b1,
    exact_reader_recovery: recoveredReader === reader,
    start_marker: startMarker,
    end_marker: endMarker,
  },
  boundary: {
    candidate_only: true,
    tandem_comments_compatibility_claimed: false,
    production_promotion: false,
    p3_product_verdict: "NOT_CLAIMED",
  },
};

fs.writeFileSync(paths.receiptOut, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
