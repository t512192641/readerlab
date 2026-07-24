#!/usr/bin/env python3
"""Deterministically select and byte-extract the T2.26 v07 chapter scope."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree


SOURCE_RELATIVE = Path("materials/T2.4-IDEA-PILOT-01/source.epub")
SOURCE_SHA256 = "3baf9932c92412f0e7d0ccae993182f55f62e2fab5ec46a3882d675476288664"
EXCLUDED_CHAPTERS = frozenset({7, 13, 14, 15, 16, 19})
EXPECTED_ELIGIBLE_COUNT = 15
EXPECTED_PAYLOAD_BYTES = 250
EXPECTED_PAYLOAD_SHA256 = (
    "16b480aa130a24d8fa1e3e925fb0eaa32740c732271691afd3cf87bdb27e70c3"
)
EXPECTED_SELECTION_INDEX = 1
EXPECTED_ELIGIBLE_ID = "eligible-02"
EXPECTED_CHAPTER = 2
EXPECTED_MEMBER = "text/part0006.html"
EXPECTED_MEMBER_SIZE = 82261
EXPECTED_COMPRESSED_MEMBER_SHA256 = (
    "5807933d06163a3aebe54d0882987fe2a35d7ea75e417ba05a3113403bac0585"
)
EXPECTED_MEMBER_CONTENT_SHA256 = (
    "ba0c9aa2a7413d6792cf1b57b821dc38bd3d6777d5a16cb0dcd69c4dd9442e82"
)
SCOPE_END = b"</html>"
EXPECTED_SCOPE_BYTES = 82260
EXPECTED_SCOPE_SHA256 = (
    "934624eacafabf192b930519ff19a0c004fb12d8fc477c04922e5835cdaf69c6"
)
EXPECTED_SUFFIX = b"\n"


class MaterialError(RuntimeError):
    """A deterministic T2.26 material failure."""


@dataclass(frozen=True)
class Eligible:
    eligible_id: str
    chapter: int
    member: str
    size: int
    compressed_sha256: str


@dataclass(frozen=True)
class Selection:
    source_sha256: str
    payload: bytes
    payload_sha256: str
    index: int
    eligible: tuple[Eligible, ...]
    selected: Eligible


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exclusive_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _toc_member(archive: zipfile.ZipFile) -> str:
    matches = sorted(name for name in archive.namelist() if name.endswith("toc.ncx"))
    if len(matches) != 1:
        raise MaterialError(f"expected one toc.ncx member, found {len(matches)}")
    return matches[0]


def _chapter_number(label: str) -> int | None:
    match = re.match(r"^\s*第\s*(\d+)\s*章\b", label)
    return int(match.group(1)) if match else None


def _toc_chapters(archive: zipfile.ZipFile) -> dict[int, str]:
    toc_member = _toc_member(archive)
    root = ElementTree.fromstring(archive.read(toc_member))
    toc_parent = PurePosixPath(toc_member).parent
    result: dict[int, str] = {}
    for nav_point in root.findall(".//{*}navPoint"):
        label_node = nav_point.find("./{*}navLabel/{*}text")
        content_node = nav_point.find("./{*}content")
        if label_node is None or content_node is None or label_node.text is None:
            continue
        chapter = _chapter_number(label_node.text)
        source = content_node.attrib.get("src", "").split("#", 1)[0]
        if chapter is None or not source:
            continue
        member = (toc_parent / PurePosixPath(source)).as_posix()
        if chapter in result:
            raise MaterialError(f"duplicate TOC chapter: {chapter}")
        result[chapter] = member
    expected = set(range(1, 22))
    if set(result) != expected:
        raise MaterialError(
            f"TOC chapter set mismatch; missing={sorted(expected - set(result))}; "
            f"extra={sorted(set(result) - expected)}"
        )
    return result


def compressed_member_sha256(source: Path, info: zipfile.ZipInfo) -> str:
    with source.open("rb") as handle:
        handle.seek(info.header_offset)
        header = handle.read(30)
        if len(header) != 30:
            raise MaterialError(f"short local ZIP header: {info.filename}")
        fields = struct.unpack("<IHHHHHIIIHH", header)
        signature = fields[0]
        filename_length = fields[-2]
        extra_length = fields[-1]
        if signature != 0x04034B50:
            raise MaterialError(f"invalid local ZIP header: {info.filename}")
        handle.seek(filename_length + extra_length, os.SEEK_CUR)
        compressed = handle.read(info.compress_size)
    if len(compressed) != info.compress_size:
        raise MaterialError(f"short compressed member: {info.filename}")
    return sha256_bytes(compressed)


def build_selection(source: Path) -> Selection:
    source_sha = sha256_file(source)
    if source_sha != SOURCE_SHA256:
        raise MaterialError(f"source SHA mismatch: {source_sha}")
    with zipfile.ZipFile(source) as archive:
        chapter_members = _toc_chapters(archive)
        candidates = sorted(
            (
                (chapter, member)
                for chapter, member in chapter_members.items()
                if chapter not in EXCLUDED_CHAPTERS
            ),
            key=lambda item: item[1],
        )
        items = []
        for index, (chapter, member) in enumerate(candidates, 1):
            info = archive.getinfo(member)
            items.append(
                Eligible(
                    eligible_id=f"eligible-{index:02d}",
                    chapter=chapter,
                    member=member,
                    size=info.file_size,
                    compressed_sha256=compressed_member_sha256(source, info),
                )
            )
        eligible = tuple(items)
    if len(eligible) != EXPECTED_ELIGIBLE_COUNT:
        raise MaterialError(f"eligible count mismatch: {len(eligible)}")
    payload = (
        f"T2.26|{source_sha}|" + "\n".join(item.eligible_id for item in eligible)
    ).encode("ascii")
    payload_sha = sha256_bytes(payload)
    if len(payload) != EXPECTED_PAYLOAD_BYTES or payload_sha != EXPECTED_PAYLOAD_SHA256:
        raise MaterialError(
            f"payload mismatch: bytes={len(payload)}, sha256={payload_sha}"
        )
    index = int(payload_sha[:16], 16) % len(eligible)
    selected = eligible[index]
    expected_identity = (
        EXPECTED_SELECTION_INDEX,
        EXPECTED_ELIGIBLE_ID,
        EXPECTED_CHAPTER,
        EXPECTED_MEMBER,
        EXPECTED_MEMBER_SIZE,
        EXPECTED_COMPRESSED_MEMBER_SHA256,
    )
    actual_identity = (
        index,
        selected.eligible_id,
        selected.chapter,
        selected.member,
        selected.size,
        selected.compressed_sha256,
    )
    if actual_identity != expected_identity:
        raise MaterialError(
            f"selected identity mismatch: actual={actual_identity}, "
            f"expected={expected_identity}"
        )
    return Selection(source_sha, payload, payload_sha, index, eligible, selected)


def manifest_bytes(selection: Selection) -> bytes:
    lines = [
        "# T2.26 v07 material selection manifest",
        "",
        f"source_sha256: `{selection.source_sha256}`",
        f"eligible_count: {len(selection.eligible)}",
        f"payload_bytes: {len(selection.payload)}",
        f"payload_sha256: `{selection.payload_sha256}`",
        f"selection_index_zero_based: {selection.index}",
        f"selected_eligible_id: `{selection.selected.eligible_id}`",
        f"selected_chapter: {selection.selected.chapter}",
        f"selected_member: `{selection.selected.member}`",
        f"selected_member_size: {selection.selected.size}",
        f"selected_member_compressed_sha256: `{selection.selected.compressed_sha256}`",
        "",
        "The two independent control-layer selections matched exactly.",
        "",
        "## Eligible mapping",
    ]
    lines.extend(
        f"- `{item.eligible_id}`: chapter {item.chapter}, `{item.member}`, "
        f"size {item.size}, compressed SHA-256 `{item.compressed_sha256}`"
        for item in selection.eligible
    )
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def extract_scope(member_bytes: bytes) -> bytes:
    if member_bytes.count(SCOPE_END) != 1:
        raise MaterialError(
            f"scope end marker count mismatch: {member_bytes.count(SCOPE_END)}"
        )
    end = member_bytes.index(SCOPE_END) + len(SCOPE_END)
    scope = member_bytes[:end]
    suffix = member_bytes[end:]
    scope_sha = sha256_bytes(scope)
    if suffix != EXPECTED_SUFFIX:
        raise MaterialError(f"selected member suffix mismatch: {suffix.hex()}")
    if len(scope) != EXPECTED_SCOPE_BYTES or scope_sha != EXPECTED_SCOPE_SHA256:
        raise MaterialError(
            f"scope mismatch: bytes={len(scope)}, sha256={scope_sha}"
        )
    return scope


def materialize(workspace: Path, run_root: Path) -> dict[str, object]:
    source = workspace / SOURCE_RELATIVE
    first = build_selection(source)
    second = build_selection(source)
    if first != second:
        raise MaterialError("two independent selections differ")

    manifest = manifest_bytes(first)
    manifest_path = run_root / "control" / "material-selection-manifest.md"
    scope_path = run_root / "inputs" / "chapter-scope.xhtml"
    if manifest_path.exists() or scope_path.exists():
        raise MaterialError("material target already exists")
    exclusive_write(manifest_path, manifest)
    if manifest_path.read_bytes() != manifest:
        raise MaterialError("manifest first-write readback mismatch")

    if sha256_file(source) != first.source_sha256:
        raise MaterialError("source SHA changed after manifest freeze")
    with zipfile.ZipFile(source) as archive:
        selected_info = archive.getinfo(first.selected.member)
        if selected_info.file_size != first.selected.size:
            raise MaterialError("selected member size changed after manifest freeze")
        if (
            compressed_member_sha256(source, selected_info)
            != first.selected.compressed_sha256
        ):
            raise MaterialError(
                "selected compressed member SHA changed after manifest freeze"
            )
        member_bytes = archive.read(first.selected.member)
    if len(member_bytes) != first.selected.size:
        raise MaterialError("selected member size changed after manifest freeze")
    member_content_sha = sha256_bytes(member_bytes)
    if member_content_sha != EXPECTED_MEMBER_CONTENT_SHA256:
        raise MaterialError(
            f"selected member content SHA mismatch: {member_content_sha}"
        )
    scope = extract_scope(member_bytes)
    exclusive_write(scope_path, scope)
    readback = scope_path.read_bytes()
    if readback != scope:
        raise MaterialError("scope first-write readback bytes mismatch")
    if len(readback) != EXPECTED_SCOPE_BYTES:
        raise MaterialError("scope first-write readback length mismatch")
    if sha256_bytes(readback) != EXPECTED_SCOPE_SHA256:
        raise MaterialError("scope first-write readback SHA mismatch")
    return {
        "status": "PASS",
        "source_sha256": first.source_sha256,
        "eligible_count": len(first.eligible),
        "payload_bytes": len(first.payload),
        "payload_sha256": first.payload_sha256,
        "selection_index_zero_based": first.index,
        "selected_eligible_id": first.selected.eligible_id,
        "selected_chapter": first.selected.chapter,
        "selected_member": first.selected.member,
        "selected_member_size": first.selected.size,
        "selected_member_compressed_sha256": first.selected.compressed_sha256,
        "selected_member_content_sha256": member_content_sha,
        "scope_expected_bytes": EXPECTED_SCOPE_BYTES,
        "scope_actual_bytes": len(readback),
        "scope_expected_sha256": EXPECTED_SCOPE_SHA256,
        "scope_actual_sha256": sha256_bytes(readback),
        "scope_suffix_excluded_hex": EXPECTED_SUFFIX.hex(),
        "manifest_sha256": sha256_bytes(manifest),
        "chapter_body_semantic_reads": 0,
        "semantic_model_calls": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = materialize(args.workspace.resolve(), args.run_root.resolve())
    except (OSError, ValueError, zipfile.BadZipFile, ElementTree.ParseError, MaterialError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
