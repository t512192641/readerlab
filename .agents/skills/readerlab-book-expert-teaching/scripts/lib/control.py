"""Narrow control primitives for the ReaderLab Expert Teaching Skill.

The generic repository run tool owns the stable hashing and exclusive-publication
primitives.  This module adds only the stage-specific identity, state, and
read-set checks needed by this Skill.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = SKILL_DIR.parents[2]
SKILL_VERSION = (SKILL_DIR / "VERSION").read_text(encoding="utf-8").strip()
SCHEMA = "readerlab-book-expert-teaching/v0.1"
STATUSES = {
    "EXPERT_OPEN",
    "REVIEW_OPEN",
    "REVIEW_TERMINAL",
    "PRODUCT_READY",
}
FIDELITY_STATES = {
    "SOURCE_FIDELITY_PASS",
    "RETURN_EXPERT_SOURCE",
    "SOURCE_BLOCKED",
}
TEACHING_STATES = {
    "TEACHING_PASS",
    "TEACHING_PARTIAL",
    "TEACHING_FAIL",
}
URL_RE = re.compile(r"https?://[^\s<>)\]}`\"']+")
FORBIDDEN_PRODUCT_RE = re.compile(
    r"(?:\bM[123]\b|expert-teaching-source-map|技术评分|Writer|旧稿|路线信息)",
    re.IGNORECASE,
)
XHTML_RE = re.compile(
    r"<\s*(?:html|body|head|h[1-6]|p|div|section|article|blockquote|span|br|a|img|ul|ol|li)\b",
    re.IGNORECASE,
)
HTML_TAG_RE = re.compile(r"<\s*/?\s*[A-Za-z][^>]*>")


class SkillError(RuntimeError):
    """A deterministic Skill-contract failure."""


def core_run_tool() -> Any:
    """Load the repository's stable run/hash primitives without copying them."""

    if os.fspath(REPO_ROOT) not in sys.path:
        sys.path.insert(0, os.fspath(REPO_ROOT))
    return importlib.import_module("tools.run")


def require_file(path: Path, label: str) -> Path:
    if path.is_symlink() or not path.is_file():
        raise SkillError(f"{label} must be a regular file: {path}")
    return path


def require_dir(path: Path, label: str) -> Path:
    if path.is_symlink() or not path.is_dir():
        raise SkillError(f"{label} must be a real directory: {path}")
    return path


def stable_bytes(path: Path, label: str) -> bytes:
    return core_run_tool()._stable_bytes(path, label)


def sha256_size(path: Path) -> tuple[str, int]:
    return core_run_tool()._sha256_and_size(path)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def publish_exclusive(path: Path, payload: bytes) -> None:
    """Publish a new file without replacing an existing artifact."""

    if path.exists() or path.is_symlink():
        raise SkillError(f"refusing to overwrite existing file: {path}")
    require_dir(path.parent, "file parent")
    core_run_tool()._publish_exclusive(path, payload)


def write_text_exclusive(path: Path, text: str) -> None:
    publish_exclusive(path, text.encode("utf-8"))


def read_json(path: Path, label: str) -> dict[str, Any]:
    require_file(path, label)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SkillError(f"{label} is not valid UTF-8 JSON: {path}") from error
    if not isinstance(value, dict):
        raise SkillError(f"{label} must be a JSON object: {path}")
    return value


def write_json_exclusive(path: Path, value: dict[str, Any]) -> None:
    payload = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    publish_exclusive(path, payload)


def replace_json(path: Path, value: dict[str, Any]) -> None:
    """Update the mutable state projection atomically.

    Semantic outputs are exclusive-only.  `run.json` is explicitly a mutable
    control projection, so replacing it is allowed and recorded in transitions.
    """

    require_file(path, "mutable state projection")
    payload = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    fd, name = tempfile.mkstemp(prefix=".state-", dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass


def replace_text(path: Path, text: str) -> None:
    require_file(path, "mutable control document")
    payload = text.encode("utf-8")
    fd, name = tempfile.mkstemp(prefix=".document-", dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def resolve_run(path_value: str | Path, *, must_exist: bool = True) -> Path:
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve(strict=False)
    if must_exist:
        require_dir(path, "run directory")
    return path


def resolve_input(path_value: str | Path, label: str) -> Path:
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve(strict=True)
    return require_file(path, label)


def relative_path(run: Path, path: Path) -> str:
    try:
        relative = path.resolve(strict=False).relative_to(run.resolve(strict=False))
    except ValueError as error:
        raise SkillError(f"path escapes run directory: {path}") from error
    posix = PurePosixPath(relative.as_posix())
    if posix.is_absolute() or any(part in {"", ".", ".."} for part in posix.parts):
        raise SkillError(f"non-canonical run-relative path: {path}")
    return posix.as_posix()


def path_from_run(run: Path, relative: str) -> Path:
    posix = PurePosixPath(relative)
    if (
        posix.is_absolute()
        or posix.as_posix() != relative
        or not posix.parts
        or any(part in {"", ".", ".."} for part in posix.parts)
    ):
        raise SkillError(f"invalid run-relative path: {relative!r}")
    path = run.joinpath(*posix.parts)
    relative_path(run, path)
    return path


def file_record(path: Path, run: Path | None = None) -> dict[str, Any]:
    digest, size = sha256_size(path)
    record: dict[str, Any] = {"sha256": digest, "bytes": size}
    if run is not None:
        record["path"] = relative_path(run, path)
    return record


def copy_exclusive(source: Path, target: Path, label: str) -> dict[str, Any]:
    payload = stable_bytes(source, label)
    target.parent.mkdir(parents=True, exist_ok=True)
    require_dir(target.parent, "copy target parent")
    publish_exclusive(target, payload)
    return {"sha256": sha256_bytes(payload), "bytes": len(payload)}


def template(name: str) -> str:
    path = SKILL_DIR / "templates" / name
    return stable_bytes(path, f"template {name}").decode("utf-8")


def skill_fingerprint() -> dict[str, Any]:
    files = [SKILL_DIR / "SKILL.md", SKILL_DIR / "VERSION"]
    files.extend(sorted((SKILL_DIR / "agents").glob("*.yaml")))
    files.extend(sorted((SKILL_DIR / "contracts").glob("*.md")))
    files.extend(sorted((SKILL_DIR / "templates").glob("*.md")))
    files.extend(sorted((SKILL_DIR / "scripts").glob("*.py")))
    files.extend(sorted((SKILL_DIR / "scripts/lib").glob("*.py")))
    records = []
    for path in files:
        digest, size = sha256_size(path)
        records.append({"path": path.relative_to(SKILL_DIR).as_posix(), "sha256": digest, "bytes": size})
    aggregate = sha256_bytes(
        "".join(f"{item['path']}\0{item['sha256']}\0{item['bytes']}\n" for item in records).encode(
            "utf-8"
        )
    )
    return {"version": SKILL_VERSION, "aggregate_sha256": aggregate, "files": records}


def urls_from_source_map(path: Path) -> list[str]:
    text = stable_bytes(path, "source map").decode("utf-8")
    urls = {match.rstrip(".,;:)") for match in URL_RE.findall(text)}
    return sorted(urls)


def render(template_text: str, values: dict[str, str]) -> str:
    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    unresolved = re.findall(r"\{\{[^}]+\}\}", rendered)
    if unresolved:
        raise SkillError(f"unresolved template placeholders: {unresolved}")
    return rendered


def read_text(path: Path, label: str) -> str:
    try:
        payload = stable_bytes(path, label)
        return payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise SkillError(f"{label} is not valid UTF-8: {path}") from error


def record_lines(records: list[tuple[str, Path]], run: Path) -> str:
    lines = []
    for relative, path in records:
        digest, size = sha256_size(path)
        lines.append(f"{digest}  {relative}  # {size} bytes")
    return "\n".join(lines) + "\n"


class _ReadableHTML(HTMLParser):
    """Small dependency-free XHTML-to-readable-Markdown adapter."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.block_depth = 0

    def _newline(self, count: int = 1) -> None:
        current = "".join(self.parts)
        suffix = "\n" * count
        if not current.endswith(suffix):
            self.parts.append(suffix)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._newline(2)
            self.parts.append("#" * int(tag[1]) + " ")
            self.block_depth += 1
        elif tag in {"p", "div", "section", "article", "blockquote"}:
            self._newline(2)
            self.block_depth += 1
        elif tag == "br":
            self._newline(1)
        elif tag == "li":
            self._newline(1)
            self.parts.append("- ")
        elif tag in {"ul", "ol"}:
            self._newline(1)
        elif tag == "img":
            return

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "section", "article", "blockquote"}:
            self._newline(2)
            self.block_depth = max(0, self.block_depth - 1)
        elif tag == "li":
            self._newline(1)

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def readable_markdown(path: Path) -> str:
    source = read_text(path, "frozen source")
    if not XHTML_RE.search(source):
        return source.strip() + "\n"
    parser = _ReadableHTML()
    parser.feed(source)
    parser.close()
    return parser.markdown()


def load_state(run: Path) -> dict[str, Any]:
    state = read_json(run / "run.json", "run state")
    if state.get("schema") != SCHEMA:
        raise SkillError(f"unsupported Skill run schema: {state.get('schema')!r}")
    if state.get("skill_version") != SKILL_VERSION:
        raise SkillError("run Skill version does not match installed VERSION")
    return state


def transition(run: Path, expected: str, new_status: str, **event: Any) -> dict[str, Any]:
    state = load_state(run)
    current = state.get("status")
    if current != expected:
        raise SkillError(f"illegal state transition: {current!r} -> {new_status!r}; expected {expected!r}")
    if new_status not in STATUSES:
        raise SkillError(f"unknown state: {new_status}")
    transitions = state.setdefault("transitions", [])
    if not isinstance(transitions, list):
        raise SkillError("run transitions are malformed")
    transitions.append({"from": current, "to": new_status, "at": now(), **event})
    state["status"] = new_status
    state["updated_at"] = now()
    replace_json(run / "run.json", state)
    return state


def transition_with_fields(
    run: Path,
    expected: str,
    new_status: str,
    fields: dict[str, Any],
    **event: Any,
) -> dict[str, Any]:
    """Commit a state transition and its stage projection in one replacement."""

    state = load_state(run)
    current = state.get("status")
    if current != expected:
        raise SkillError(
            f"illegal state transition: {current!r} -> {new_status!r}; expected {expected!r}"
        )
    if new_status not in STATUSES:
        raise SkillError(f"unknown state: {new_status}")
    transitions = state.setdefault("transitions", [])
    if not isinstance(transitions, list):
        raise SkillError("run transitions are malformed")
    transitions.append({"from": current, "to": new_status, "at": now(), **event})
    state.update(fields)
    state["status"] = new_status
    state["updated_at"] = now()
    replace_json(run / "run.json", state)
    return state


def stage_freeze(run: Path, name: str, relatives: list[str]) -> Path:
    path = run / "control" / "stage-freezes" / name
    if path.exists() or path.is_symlink():
        raise SkillError(f"stage freeze already exists: {path}")
    records: list[tuple[str, Path]] = []
    for relative in relatives:
        candidate = path_from_run(run, relative)
        require_file(candidate, f"stage input {relative}")
        records.append((relative, candidate))
    write_text_exclusive(path, record_lines(records, run))
    return path


def verify_stage_freeze(run: Path, name: str) -> None:
    path = run / "control" / "stage-freezes" / name
    text = read_text(path, f"stage freeze {name}")
    for line in text.splitlines():
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) < 2 or not re.fullmatch(r"[0-9a-f]{64}", fields[0]):
            raise SkillError(f"malformed stage freeze line: {line}")
        relative = fields[1]
        candidate = path_from_run(run, relative)
        observed, _ = sha256_size(candidate)
        if observed != fields[0]:
            raise SkillError(f"freeze hash drift for {relative}")


def verify_prompt_freeze(run: Path) -> None:
    text = read_text(run / "control" / "prompt-freeze.sha256", "Prompt freeze")
    for line in text.splitlines():
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) < 2 or not re.fullmatch(r"[0-9a-f]{64}", fields[0]):
            raise SkillError(f"malformed Prompt freeze line: {line}")
        observed, _ = sha256_size(path_from_run(run, fields[1]))
        if observed != fields[0]:
            raise SkillError(f"Prompt/template hash drift for {fields[1]}")


def update_documents(run: Path, state: dict[str, Any]) -> None:
    fixed = state["inputs"]
    lines = [
        f"# {run.name} · run manifest",
        "",
        f"- schema: `{state['schema']}`",
        f"- skill-version: `{state['skill_version']}`",
        f"- status: `{state['status']}`",
        f"- created-at: `{state['created_at']}`",
        f"- updated-at: `{state.get('updated_at', state['created_at'])}`",
        "- semantic calls: `not performed by this Skill`",
        "- production integration: `not_applicable`",
        "",
        "## Fixed inputs",
        "",
    ]
    for name in ("source", "framework", "source_map"):
        record = fixed[name]
        lines.append(f"- `inputs/{name.replace('_', '-')}.md`: {record['bytes']} bytes, SHA-256 `{record['sha256']}`")
    lines.extend(["", "## Stage outcomes", ""])
    lines.append(f"- Expert: `{state.get('expert', {}).get('status', 'pending')}`")
    lines.append(f"- Review: `{state.get('review', {}).get('status', 'pending')}`")
    lines.append(f"- Product pack: `{state.get('product', {}).get('status', 'not_created')}`")
    lines.extend(["", "## Freeze files", "", "- `control/input-freeze.json`", "- `control/prompt-freeze.sha256`", "- `control/stage-freezes/`"])
    replace_text(run / "run-manifest.md", "\n".join(lines) + "\n")

    ledger = [
        f"# {run.name} · run ledger",
        "",
        "> This ledger records deterministic control actions only; it is not a semantic judgment.",
        "",
        f"- current status: `{state['status']}`",
        f"- Expert Agent ID: `{state.get('expert', {}).get('agent_id', 'pending')}`",
        f"- Reviewer Agent ID: `{state.get('review', {}).get('agent_id', 'pending')}`",
        f"- network: Expert `{state.get('expert', {}).get('network', 'pending')}`, review `{state.get('review', {}).get('network', 'pending')}`",
        f"- retries: Expert `{state.get('expert', {}).get('retries', 'pending')}`, review `{state.get('review', {}).get('retries', 'pending')}`",
        f"- Prompt modified: Expert `{state.get('expert', {}).get('prompt_modified', 'pending')}`, review `{state.get('review', {}).get('prompt_modified', 'pending')}`",
        "- semantic model calls: `none`",
        "- archive hash: recorded outside the archive to avoid self-reference",
        "",
        "## State transitions",
        "",
    ]
    for event in state.get("transitions", []):
        ledger.append(f"- `{event.get('from')}` → `{event.get('to')}` at `{event.get('at')}`")
    replace_text(run / "run-ledger.md", "\n".join(ledger) + "\n")


def assert_output_file(run: Path, relative: str, label: str) -> Path:
    path = path_from_run(run, relative)
    require_file(path, label)
    text = read_text(path, label)
    if not text.strip():
        raise SkillError(f"{label} is empty: {path}")
    return path


def assert_no_forbidden_product_content(text: str) -> None:
    if FORBIDDEN_PRODUCT_RE.search(text):
        raise SkillError("product package contains forbidden source-map, technical, route, Writer, or M-label text")
    if HTML_TAG_RE.search(text):
        raise SkillError("product package contains raw XHTML markup")
