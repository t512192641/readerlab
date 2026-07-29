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
from urllib.parse import urlparse


SKILL_DIR = Path(__file__).resolve().parents[2]


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "tools" / "run.py").is_file():
            return candidate
    raise RuntimeError(f"cannot locate ReaderLab repository root from {start}")


REPO_ROOT = _find_repo_root(SKILL_DIR)
SKILL_VERSION = (SKILL_DIR / "VERSION").read_text(encoding="utf-8").strip()
SCHEMA = "readerlab-book-expert-teaching/v0.1"
ALLOWLIST_SCHEMA = "readerlab-book-expert-teaching/source-allowlist/v1"
SOURCE_ACCESS_SCHEMA = "readerlab-book-expert-teaching/source-access/v1"
SOURCE_BOUNDARY_SCHEMA = "readerlab-book-expert-teaching/source-boundary/v1"
SOURCE_ACCESS_PROVENANCE = "agent_declared"
SOURCE_ACCESS_AUDIT_SCOPE = "agent-declared; not a browser or OS-level network audit"
ALLOWLIST_STATUSES = {"allowed", "reference_only", "blocked"}
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
URL_RE = re.compile(r"https?://[^\s<>)\]}`\"'，。；：、（）【】《》！？…“”‘’]+")
DEPTH_SELF_LABEL_RE = re.compile(
    r"(?:\b(?:ReaderLab|readerlab)[-_ ]+(?:M1|M2|M3)\b|"
    r"(?:depth|深度)[-_ ]?(?:label|self|自证|等级)\s*[:：=]|"
    r"(?:M1|M2|M3)\s*[:：=]\s*(?:depth|深度))",
    re.IGNORECASE,
)
FORBIDDEN_PRODUCT_RE = re.compile(
    r"(?:\.agents/skills/readerlab-book-expert-teaching(?:/[A-Za-z0-9._/-]+)?|"
    r"(?:^|[\s`])(?:runs|control|raw|acceptance)/[A-Za-z0-9._/-]+|"
    r"SOURCE_FIDELITY_FINAL|TEACHING_FINAL|EXPERT_OPEN|REVIEW_OPEN|"
    r"REVIEW_TERMINAL|PRODUCT_READY|stage-[0-9]+\.sha256|prompt-freeze(?:\.sha256)?|"
    r"input-freeze\.json|(?:expert-teaching-(?:draft|source-map|review)\.md)|source-allowlist\.json|"
    r"run-(?:manifest|ledger)\.md|metadata_provenance|技术评分|technical[-_ ]score|"
    r"internal[-_ ](?:score|rating)|score[_ -]column|"
    r"(?:Writer|writer)[-_ ]?(?:route|stage|control|metadata)|"
    r"(?:route|路线)[-_ ]?(?:key|metadata|control)|"
    r"(?:ReaderLab|readerlab)[-_ ]+(?:M1|M2|M3)\b|"
    r"(?:depth|深度)[-_ ]?(?:label|self|自证|等级)\s*[:：=])",
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


def _validate_url(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SkillError(f"{label} must be a non-empty URL")
    url = value.strip()
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or url != value:
        raise SkillError(f"{label} must be an absolute http(s) URL: {value!r}")
    if URL_RE.fullmatch(url) is None:
        raise SkillError(f"{label} contains unsupported URL characters: {value!r}")
    return url


def read_source_allowlist(path: Path) -> list[dict[str, Any]]:
    value = read_json(path, "source allowlist")
    if value.get("schema") != ALLOWLIST_SCHEMA:
        raise SkillError(f"source allowlist schema must be {ALLOWLIST_SCHEMA}")
    if set(value) - {"schema", "sources"}:
        raise SkillError("source allowlist contains unknown top-level fields")
    entries = value.get("sources")
    if not isinstance(entries, list):
        raise SkillError("source allowlist sources must be a list")
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise SkillError(f"source allowlist entry {index} must be an object")
        if set(entry) - {"id", "url", "status", "redirects"}:
            raise SkillError(f"source allowlist entry {index} contains unknown fields")
        source_id = entry.get("id")
        if not isinstance(source_id, str) or not source_id.strip() or source_id in seen_ids:
            raise SkillError(f"source allowlist entry {index} has duplicate or empty id")
        status = entry.get("status")
        if not isinstance(status, str) or status not in ALLOWLIST_STATUSES:
            raise SkillError(f"source allowlist entry {source_id} has invalid status")
        url = _validate_url(entry.get("url"), f"source allowlist {source_id}.url")
        redirects = entry.get("redirects", [])
        if not isinstance(redirects, list):
            raise SkillError(f"source allowlist {source_id}.redirects must be a list")
        normalized_redirects = [_validate_url(item, f"source allowlist {source_id}.redirects") for item in redirects]
        for candidate in [url, *normalized_redirects]:
            if candidate in seen_urls:
                raise SkillError(f"source allowlist URL appears more than once: {candidate}")
            seen_urls.add(candidate)
        seen_ids.add(source_id)
        normalized.append(
            {
                "id": source_id,
                "url": url,
                "status": status,
                "redirects": normalized_redirects,
            }
        )
    return normalized


def allowlist_urls(entries: list[dict[str, Any]], statuses: set[str]) -> list[str]:
    urls: list[str] = []
    for entry in entries:
        if entry["status"] in statuses:
            urls.extend([entry["url"], *entry["redirects"]])
    return urls


def allowlist_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": ALLOWLIST_SCHEMA,
        "entries": entries,
        "status_counts": {
            status: sum(1 for entry in entries if entry["status"] == status)
            for status in sorted(ALLOWLIST_STATUSES)
        },
        "allowed_urls": allowlist_urls(entries, {"allowed"}),
        "reviewable_urls": allowlist_urls(entries, {"allowed", "reference_only"}),
    }


def urls_in_text(text: str) -> list[str]:
    return sorted({match.rstrip(".,;:)\uFF09\u3002\uFF1B\uFF1A\u3001\"'") for match in URL_RE.findall(text)})


def assert_output_urls_allowed(text: str, entries: list[dict[str, Any]], label: str) -> None:
    allowed = set(allowlist_urls(entries, {"allowed", "reference_only"}))
    blocked = set(allowlist_urls(entries, {"blocked"}))
    for url in urls_in_text(text):
        if url in blocked:
            raise SkillError(f"{label} cites blocked source URL: {url}")
        if url not in allowed:
            raise SkillError(f"{label} cites unregistered source URL: {url}")


def source_boundary_summary(source_map_text: str, entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Return and validate the closed relation between source map and allowlist.

    Canonical allowlist URLs are source identities and therefore must occur in
    the frozen source map.  Explicit redirects may be registered in advance
    without being present in the map; they never imply domain or query-string
    expansion.
    """

    source_urls = urls_in_text(source_map_text)
    registered: dict[str, dict[str, str]] = {}
    redirect_urls: set[str] = set()
    for entry in entries:
        canonical = entry["url"]
        registered[canonical] = {"id": entry["id"], "status": entry["status"], "kind": "canonical"}
        for redirect in entry["redirects"]:
            redirect_urls.add(redirect)
            registered[redirect] = {"id": entry["id"], "status": entry["status"], "kind": "redirect"}

    source_set = set(source_urls)
    unregistered_urls = sorted(source_set - set(registered))
    unreferenced_primary_urls = sorted(
        entry["url"] for entry in entries if entry["url"] not in source_set
    )
    if unregistered_urls:
        raise SkillError(
            "source map contains URLs not registered in source allowlist: "
            + ", ".join(unregistered_urls)
        )
    if unreferenced_primary_urls:
        raise SkillError(
            "source allowlist canonical URLs missing from source map: "
            + ", ".join(unreferenced_primary_urls)
        )

    return {
        "schema": SOURCE_BOUNDARY_SCHEMA,
        "source_map_urls": source_urls,
        "registered_urls": [
            {"url": url, **registered[url]} for url in sorted(registered)
        ],
        "unreferenced_redirects": sorted(redirect_urls - source_set),
        "unregistered_urls": [],
        "unreferenced_primary_urls": [],
        "policy": "every canonical allowlist URL must occur in source-map; explicitly registered redirects may be extra",
    }


def read_source_access(
    path: Path, entries: list[dict[str, Any]], label: str
) -> dict[str, Any]:
    """Read the agent-declared URL access receipt under exact allowlist rules."""

    value = read_json(path, label)
    expected_fields = {"schema", "opened_urls", "cited_only_urls", "provenance", "audit_scope"}
    if set(value) != expected_fields:
        raise SkillError(f"{label} must contain exactly: {', '.join(sorted(expected_fields))}")
    if value.get("schema") != SOURCE_ACCESS_SCHEMA:
        raise SkillError(f"{label} schema must be {SOURCE_ACCESS_SCHEMA}")
    if value.get("provenance") != SOURCE_ACCESS_PROVENANCE:
        raise SkillError(f"{label} provenance must be {SOURCE_ACCESS_PROVENANCE}")
    if value.get("audit_scope") != SOURCE_ACCESS_AUDIT_SCOPE:
        raise SkillError(f"{label} audit_scope must state agent-declared scope")

    opened = value.get("opened_urls")
    cited_only = value.get("cited_only_urls")
    if not isinstance(opened, list) or not isinstance(cited_only, list):
        raise SkillError(f"{label} opened_urls and cited_only_urls must be lists")

    def normalize_urls(values: list[Any], field: str) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for index, item in enumerate(values):
            url = _validate_url(item, f"{label}.{field}[{index}]")
            if url in seen:
                raise SkillError(f"{label}.{field} contains duplicate URL: {url}")
            seen.add(url)
            normalized.append(url)
        return normalized

    opened_urls = normalize_urls(opened, "opened_urls")
    cited_only_urls = normalize_urls(cited_only, "cited_only_urls")
    overlap = sorted(set(opened_urls) & set(cited_only_urls))
    if overlap:
        raise SkillError(f"{label} URL appears in both access arrays: {', '.join(overlap)}")

    allowed = set(allowlist_urls(entries, {"allowed"}))
    reviewable = set(allowlist_urls(entries, {"allowed", "reference_only"}))
    for url in opened_urls:
        if url not in allowed:
            if url in set(allowlist_urls(entries, {"blocked"})):
                raise SkillError(f"{label} opened_urls contains blocked URL: {url}")
            if url in reviewable:
                raise SkillError(f"{label} opened_urls may contain only allowed URLs: {url}")
            raise SkillError(f"{label} opened_urls contains unregistered URL: {url}")
    for url in cited_only_urls:
        if url not in reviewable:
            if url in set(allowlist_urls(entries, {"blocked"})):
                raise SkillError(f"{label} cited_only_urls contains blocked URL: {url}")
            raise SkillError(f"{label} cited_only_urls contains unregistered URL: {url}")
    return {
        "schema": value["schema"],
        "opened_urls": opened_urls,
        "cited_only_urls": cited_only_urls,
        "provenance": value["provenance"],
        "audit_scope": value["audit_scope"],
    }


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
        "- semantic calls invoked by this Skill: `none`",
        "- external semantic contexts: `controller_declared`",
        "- production integration: `not_integrated`",
        "",
        "## Fixed inputs",
        "",
    ]
    for name in ("source", "framework", "source_map", "source_allowlist"):
        record = fixed[name]
        suffix = ".json" if name == "source_allowlist" else ".md"
        lines.append(f"- `inputs/{name.replace('_', '-')}{suffix}`: {record['bytes']} bytes, SHA-256 `{record['sha256']}`")
    allowlist = state.get("source_allowlist", {})
    lines.append(f"- source allowlist schema: `{allowlist.get('schema', ALLOWLIST_SCHEMA)}`; SHA-256 `{allowlist.get('sha256', 'unknown')}`")
    boundary = state.get("source_boundary", {})
    lines.append(
        f"- source boundary schema: `{boundary.get('schema', SOURCE_BOUNDARY_SCHEMA)}`; "
        f"SHA-256 `{boundary.get('sha256', 'unknown')}`; policy: canonical URLs closed to source map, redirects explicit"
    )
    lines.extend(["", "## Stage outcomes", ""])
    lines.append(f"- Expert: `{state.get('expert', {}).get('status', 'pending')}`")
    lines.append(
        f"- Expert source access: `{state.get('expert', {}).get('source_access', {}).get('sha256', 'pending')}`; "
        f"provenance: `{state.get('expert', {}).get('source_access_provenance', 'pending')}`; "
        f"audit scope: `{state.get('expert', {}).get('source_access_audit_scope', SOURCE_ACCESS_AUDIT_SCOPE)}`"
    )
    lines.append(f"- Review: `{state.get('review', {}).get('status', 'pending')}`")
    lines.append(
        f"- Reviewer source access: `{state.get('review', {}).get('source_access', {}).get('sha256', 'pending')}`; "
        f"provenance: `{state.get('review', {}).get('source_access_provenance', 'pending')}`; "
        f"audit scope: `{state.get('review', {}).get('source_access_audit_scope', SOURCE_ACCESS_AUDIT_SCOPE)}`"
    )
    lines.append(f"- Product pack: `{state.get('product', {}).get('status', 'not_created')}`")
    lines.extend([
        "",
        "## Freeze files",
        "",
        "- `control/input-freeze.json`",
        "- `control/source-boundary.json`",
        "- `control/prompt-freeze.sha256`",
        "- `control/stage-freezes/` (includes both source access receipts)",
    ])
    replace_text(run / "run-manifest.md", "\n".join(lines) + "\n")

    ledger = [
        f"# {run.name} · run ledger",
        "",
        "> This ledger records deterministic control actions only; it is not a semantic judgment.",
        "",
        f"- current status: `{state['status']}`",
        f"- Expert Agent ID: `{state.get('expert', {}).get('agent_id', 'pending')}`",
        f"- Reviewer Agent ID: `{state.get('review', {}).get('agent_id', 'pending')}`",
        f"- model: Expert `{state.get('expert', {}).get('model', 'pending')}`, review `{state.get('review', {}).get('model', 'pending')}`; provenance: `controller_declared`",
        f"- reasoning: Expert `{state.get('expert', {}).get('reasoning', 'pending')}`, review `{state.get('review', {}).get('reasoning', 'pending')}`; provenance: `controller_declared`",
        f"- network: Expert `{state.get('expert', {}).get('network', 'pending')}`, review `{state.get('review', {}).get('network', 'pending')}`; provenance: `controller_declared`",
        f"- retries: Expert `{state.get('expert', {}).get('retries', 'pending')}`, review `{state.get('review', {}).get('retries', 'pending')}`; provenance: `controller_declared`",
        f"- Prompt modified: Expert `{state.get('expert', {}).get('prompt_modified', 'pending')}`, review `{state.get('review', {}).get('prompt_modified', 'pending')}`; provenance: `controller_declared`",
        "- semantic calls invoked by this Skill: `none`",
        "- external semantic contexts: `controller_declared`",
        f"- source access receipts: Expert `{state.get('expert', {}).get('source_access', {}).get('path', 'pending')}` (SHA-256 `{state.get('expert', {}).get('source_access', {}).get('sha256', 'pending')}`), reviewer `{state.get('review', {}).get('source_access', {}).get('path', 'pending')}` (SHA-256 `{state.get('review', {}).get('source_access', {}).get('sha256', 'pending')}`); provenance: `{SOURCE_ACCESS_PROVENANCE}`; audit scope: `{SOURCE_ACCESS_AUDIT_SCOPE}`",
        f"- source boundary: `{state.get('source_boundary', {}).get('path', 'control/source-boundary.json')}`; schema: `{state.get('source_boundary', {}).get('schema', SOURCE_BOUNDARY_SCHEMA)}`",
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
