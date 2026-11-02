#!/usr/bin/env python3
"""Turn a finished Claude Code or Codex session into a Harbor task, and submit
it to Harbor Hub.

    capture.py sessions [--from claude|codex] [--cwd DIR]
    capture.py save [--from claude|codex] [--session ID | --transcript FILE]
                    [--cwd DIR] [--out DIR] [--exclude PATH ...] [--json]
    capture.py login | logout
    capture.py submit TASK_DIR [--json]
    capture.py status SUBMISSION_ID [--json]
    capture.py list [--json]

`save` works offline and changes nothing in the repository: the instruction is
the user's own words from the session (their workspace path becomes /app), and
the environment is the repository at the last commit before the session
started, left without build caches, system files, secrets, and binary or large
files the session never named. Each file left out is listed, with why, in
environment/omitted_files.json. The verifier and the reference solution are not
written here: Harbor Hub drafts both once the task is submitted.

`submit` uploads a saved task to Harbor Hub as the signed-in contributor (an
Eigent account; `login` opens the browser once). Nothing is uploaded otherwise.

Only the Python standard library is used. The rules for what the environment
keeps follow Eigent's own exporter (eigent backend/app/harbor_task/exporter.py).
"""

from __future__ import annotations

import argparse
import base64
import fnmatch
import hashlib
import http.server
import io
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tarfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

WORKDIR = "/app"
BASE_IMAGE = "ubuntu:24.04"
SCHEMA_VERSION = "1.4"
AGENT_TIMEOUT_SEC = 1800.0
VERIFIER_TIMEOUT_SEC = 600.0
BUILD_TIMEOUT_SEC = 600.0
MAX_FILES = 5000
MAX_TOTAL_BYTES = 200 * 1024 * 1024
MAX_UNREFERENCED_TEXT_BYTES = 1024 * 1024
GIT_DATE = "2000-01-01T00:00:00+0000"
GIT_ATTRIBUTES = "* -text -filter -ident -working-tree-encoding"
CACHE_DIRECTORIES = frozenset(
    {".cache", ".mypy_cache", ".next", ".parcel-cache", ".pytest_cache",
     ".ruff_cache", ".turbo", "__pycache__", "node_modules", ".git"}
)  # fmt: skip
SYSTEM_FILES = frozenset({".DS_Store", "Thumbs.db"})
SECRET_NAMES = (
    ".env", ".env.*", "*.pem", "*.key", "*.p12", "id_rsa*", "id_ecdsa*",
    "id_ed25519*", ".npmrc", ".netrc", "credentials", "credentials.json",
)  # fmt: skip
NOT_SECRET_NAMES = (".env.example", ".env.sample", ".env.template")
# Kinds of secret a file's text may hold; only the kind and line are reported.
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "OpenAI key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}"),
    "Anthropic key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{32,}"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghs|ghu)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{40,}"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "Harbor Hub token": re.compile(r"\bhh[a-z]?_[A-Za-z0-9_-]{30,}"),
}  # fmt: skip
PATH_TOKEN = re.compile(r"[^\s\"'`<>|;,()\[\]{}=\\]+")
SOURCES = ("claude", "codex")
DEFAULT_OUT = Path.home() / "harbor-tasks"

HUB_URL = os.environ.get("HARBOR_HUB_URL", "https://harbor-hub.eigent.ai").rstrip("/")
# The skill's public OAuth client at Harbor Hub (PKCE, no secret).
HUB_CLIENT_ID = os.environ.get("HARBOR_HUB_CLIENT_ID", "")
CREDENTIALS = Path(
    os.environ.get("HARBOR_TASK_CONFIG_DIR", Path.home() / ".config" / "harbor-task")
) / "credentials.json"


class CaptureError(Exception):
    """Something the person can fix; the message says what."""


# ── the session ──


def _jsonl(path: Path):
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except ValueError:
                    continue


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _parse_time(value) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


# What agents inject as user turns: not the person's words.
_INJECTED = re.compile(
    r"^\s*(<(environment_context|user_instructions|system-reminder|command-name|"
    r"command-message|command-args|local-command-stdout|local-command-stderr|"
    r"user-memory-input|bash-input|bash-stdout|bash-stderr|turn_aborted)[\s>]|"
    r"# AGENTS\.md instructions|Caveat: The messages below)"
)


class Session:
    """What a session recorded: who asked what, what the tools were asked to
    do (their inputs, never their output), where and when it ran."""

    def __init__(self, source: str, transcript: Path) -> None:
        self.source = source
        self.transcript = transcript
        self.id = transcript.stem
        self.cwd: str | None = None
        self.started: datetime | None = None
        self.commit: str | None = None
        self.messages: list[str] = []
        self.tool_inputs: list[str] = []
        (self._claude if source == "claude" else self._codex)()
        if not self.cwd:
            raise CaptureError(f"{transcript} records no working directory")

    def _claude(self) -> None:
        for d in _jsonl(self.transcript):
            self.cwd = self.cwd or d.get("cwd")
            self.id = d.get("sessionId") or self.id
            self.started = self.started or _parse_time(d.get("timestamp"))
            message = d.get("message") or {}
            content = message.get("content")
            if d.get("type") == "user" and not d.get("isMeta") and not d.get("isSidechain"):
                if isinstance(content, str):
                    texts = [content]
                elif isinstance(content, list):
                    texts = [b.get("text", "") for b in content
                             if isinstance(b, dict) and b.get("type") == "text"]  # fmt: skip
                else:
                    texts = []
                for text in texts:
                    if text.strip() and not _INJECTED.match(text):
                        self.messages.append(text.strip())
            elif d.get("type") == "assistant" and isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        self.tool_inputs.extend(_strings(block.get("input")))

    def _codex(self) -> None:
        for d in _jsonl(self.transcript):
            kind, p = d.get("type"), d.get("payload") or {}
            self.started = self.started or _parse_time(d.get("timestamp"))
            if kind == "session_meta":
                self.id = p.get("id") or self.id
                self.cwd = p.get("cwd") or self.cwd
                self.started = _parse_time(p.get("timestamp")) or self.started
                self.commit = (p.get("git") or {}).get("commit_hash") or self.commit
            elif kind == "turn_context":
                self.cwd = self.cwd or p.get("cwd")
            elif kind == "response_item" and p.get("type") == "message" and p.get("role") == "user":
                for block in p.get("content") or []:
                    text = block.get("text", "") if isinstance(block, dict) else ""
                    if text.strip() and not _INJECTED.match(text):
                        self.messages.append(text.strip())
            elif kind == "response_item" and p.get("type") in ("function_call", "custom_tool_call", "local_shell_call"):
                for key in ("arguments", "input", "action"):
                    self.tool_inputs.extend(_strings(p.get(key)))


def _claude_dir() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude").expanduser() / "projects"


def _codex_dir() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser() / "sessions"


def _transcripts(source: str) -> list[Path]:
    if source == "claude":
        found = _claude_dir().glob("*/*.jsonl")
    else:
        found = _codex_dir().glob("*/*/*/rollout-*.jsonl")
    return sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)


def _same_dir(a: str | None, b: Path) -> bool:
    try:
        return a is not None and Path(a).resolve() == b.resolve()
    except OSError:
        return False


def find_session(source: str, session_id: str | None, cwd: Path) -> Session:
    """The session named, else the newest one that ran in ``cwd``."""
    for transcript in _transcripts(source):
        if session_id:
            if session_id in transcript.name:
                return Session(source, transcript)
            continue
        try:
            session = Session(source, transcript)
        except CaptureError:
            continue
        if _same_dir(session.cwd, cwd):
            return session
    what = f"session {session_id}" if session_id else f"a {source} session in {cwd}"
    raise CaptureError(f"found no {what}")


# ── the repository before the session ──


def _git(repo: Path, *args: str, data: bytes | None = None) -> bytes:
    done = subprocess.run(
        ["git", "-C", str(repo), *args], input=data, capture_output=True, check=False
    )
    if done.returncode != 0:
        raise CaptureError(f"git {args[0]} failed: {done.stderr.decode(errors='replace').strip()[:300]}")
    return done.stdout


def _start(session: Session) -> tuple[Path, str, str]:
    """(the repository, the commit before the session, the session's folder
    within it as a posix path, '' for the top)."""
    cwd = Path(session.cwd).resolve()
    try:
        top = Path(_git(cwd, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    except (CaptureError, FileNotFoundError):
        raise CaptureError(
            f"{cwd} is not in a git repository: only sessions in a git repository can be saved"
        ) from None
    commit = session.commit
    if commit:
        try:
            commit = _git(top, "rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip()
        except CaptureError:
            commit = None
    if not commit and session.started:
        before = session.started.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        commit = _git(top, "rev-list", "-1", f"--before={before}", "HEAD").decode().strip() or None
    if not commit:
        raise CaptureError("the repository has no commit from before the session")
    sub = cwd.relative_to(top).as_posix()
    return top, commit, "" if sub == "." else sub


def _tree(repo: Path, commit: str, sub: str) -> list[tuple[str, str, str, int]]:
    """(path relative to the session's folder, mode, blob id, size) of each
    regular file at ``commit`` under ``sub``."""
    args = ["ls-tree", "-r", "-z", "-l", "--full-tree", commit]
    if sub:
        args += ["--", sub]
    out = []
    for record in _git(repo, *args).split(b"\0"):
        if not record:
            continue
        meta, _, path = record.decode("utf-8", errors="surrogateescape").partition("\t")
        mode, kind, oid, size = meta.split()
        if kind != "blob" or mode not in ("100644", "100755"):
            continue
        rel = path[len(sub) + 1 :] if sub else path
        out.append((rel, mode, oid, int(size)))
    return out


def _blobs(repo: Path, oids: list[str]) -> dict[str, bytes]:
    if not oids:
        return {}
    raw = _git(repo, "cat-file", "--batch", data=("\n".join(oids) + "\n").encode())
    out, i = {}, 0
    for oid in oids:
        end = raw.index(b"\n", i)
        header = raw[i:end].split()
        size = int(header[2])
        out[oid] = raw[end + 1 : end + 1 + size]
        i = end + 1 + size + 1
    return out


def _is_text(data: bytes) -> bool:
    if b"\0" in data[:8192]:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def _looks_like_secret(path: str) -> bool:
    name = PurePosixPath(path).name
    return name not in NOT_SECRET_NAMES and any(fnmatch.fnmatchcase(name, p) for p in SECRET_NAMES)


def _secret_hits(text: str) -> list[dict]:
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for kind, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                hits.append({"line": n, "kind": kind})
    return hits


def _referenced(paths: list[str], text: str, cwd: str) -> set[str]:
    """Paths of the session's folder its record names: whole (relative or
    absolute, or as path:line), or by a file name no other file has."""
    prefix = cwd.rstrip("/") + "/"
    mentioned = set()
    for token in PATH_TOKEN.findall(text):
        token = re.sub(r"(:\d+)+$", "", token.rstrip(".,:"))
        token = token[len(prefix) :] if token.startswith(prefix) else token
        token = token.removeprefix("./")
        if token:
            mentioned.add(token)
    names = {PurePosixPath(t).name for t in mentioned}
    counts: dict[str, int] = {}
    for path in paths:
        counts[PurePosixPath(path).name] = counts.get(PurePosixPath(path).name, 0) + 1
    return {
        path for path in paths
        if path in mentioned or (counts[PurePosixPath(path).name] == 1 and PurePosixPath(path).name in names)
    }  # fmt: skip


def _localize(text: str, cwd: str) -> str:
    return re.sub(re.escape(cwd.rstrip("/")) + r"(?![\w-]|\.[\w-])", WORKDIR, text)


# ── the task ──


def _dockerfile(has_files: bool) -> str:
    copy = f"COPY workspace/ {WORKDIR}/\n" if has_files else ""
    return f"""FROM {BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8

RUN apt-get update \\
    && apt-get install -y --no-install-recommends \\
        asciinema bash ca-certificates curl git nodejs npm procps python3 ripgrep tmux \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR {WORKDIR}
{copy}
# The repository as one commit holding every file byte for byte.
RUN git init -q -b main \\
    && echo '{GIT_ATTRIBUTES}' > .git/info/attributes \\
    && git add -A --force \\
    && GIT_AUTHOR_DATE='{GIT_DATE}' GIT_COMMITTER_DATE='{GIT_DATE}' \\
       git -c user.name=workspace -c user.email=workspace@localhost commit -q --allow-empty -m 'Initial workspace'
"""


PLACEHOLDER = """#!/bin/bash
# Placeholder: Harbor Hub writes the {what} once the task is submitted.
echo "No {what} is defined for this task yet." >&2
exit 1
"""


def _toml_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{k} = {_toml_value(v)}" for k, v in value.items()) + " }"
    return json.dumps(str(value), ensure_ascii=False)


def _task_toml(name: str, description: str, session: Session, commit: str, omitted: int) -> str:
    lines = [
        f'schema_version = "{SCHEMA_VERSION}"',
        f"artifacts = {_toml_value([{'source': WORKDIR, 'destination': 'workspace', 'exclude': ['.git', 'node_modules']}])}",
        "",
        "[task]",
        f"name = {_toml_value(name)}",
        'version = "1.0.0"',
        f"description = {_toml_value(description)}",
        f"keywords = {_toml_value([session.source, 'user-query'])}",
        "",
        "[metadata.capture]",
        f"source = {_toml_value(session.source)}",
        f"session_id = {_toml_value(session.id)}",
        f"start_commit = {_toml_value(commit)}",
        f"omitted_files = {omitted}",
        'omitted_list = "environment/omitted_files.json"',
        'verifier = "none"',
        "",
        "[verifier]",
        f"timeout_sec = {VERIFIER_TIMEOUT_SEC}",
        'environment_mode = "separate"',
        "",
        "[agent]",
        f"timeout_sec = {AGENT_TIMEOUT_SEC}",
        "",
        "[environment]",
        f"build_timeout_sec = {BUILD_TIMEOUT_SEC}",
        'os = "linux"',
        'network_mode = "public"',
    ]
    return "\n".join(lines) + "\n"


def save(session: Session, out_root: Path, exclude: list[str]) -> dict:
    """Write the task folder and its archive; a summary of what is in them."""
    if not session.messages:
        raise CaptureError("the session has no message from you to make a task of")
    repo, commit, sub = _start(session)
    instruction = _localize("\n\n".join(session.messages), session.cwd) + "\n"
    instruction_hits = _secret_hits(instruction)
    if instruction_hits:
        kinds = sorted({h["kind"] for h in instruction_hits})
        raise CaptureError(
            "your messages in the session hold what looks like a secret "
            f"({', '.join(kinds)}); this session cannot be saved as it is"
        )
    files = _tree(repo, commit, sub)
    request_text = "\n".join(session.messages + session.tool_inputs)
    referenced = _referenced([f[0] for f in files], request_text, session.cwd)
    excluded = {e.strip("/") for e in exclude}

    kept, omitted, candidates = {}, [], []
    for rel, mode, oid, size in files:
        parts = PurePosixPath(rel).parts
        reason = None
        if any(p in CACHE_DIRECTORIES for p in parts[:-1]):
            reason = "build_cache"
        elif parts[-1] in SYSTEM_FILES:
            reason = "system_file"
        elif rel in excluded or any(rel.startswith(e + "/") for e in excluded):
            reason = "excluded"
        elif _looks_like_secret(rel):
            reason = "secret_name"
        elif rel not in referenced and size > MAX_UNREFERENCED_TEXT_BYTES:
            reason = "large_unreferenced"
        if reason:
            omitted.append({"path": rel, "reason": reason, "size_bytes": size, "git_oid": oid})
        else:
            candidates.append((rel, mode, oid, size))
    if len(candidates) > MAX_FILES or sum(c[3] for c in candidates) > MAX_TOTAL_BYTES:
        raise CaptureError(
            f"the repository is too large to save: over {MAX_FILES} files or "
            f"{MAX_TOTAL_BYTES // 2**20} MB; leave folders out with --exclude"
        )
    blobs = _blobs(repo, [c[2] for c in candidates])
    secret_files = []
    for rel, mode, oid, size in candidates:
        data = blobs[oid]
        if rel not in referenced and not _is_text(data):
            omitted.append({"path": rel, "reason": "binary_unreferenced", "size_bytes": size, "git_oid": oid})
            continue
        hits = _secret_hits(data.decode("utf-8", errors="replace")) if _is_text(data) else []
        if hits:
            omitted.append({"path": rel, "reason": "secret_content", "size_bytes": size, "git_oid": oid})
            secret_files.append({"path": rel, "hits": hits})
            continue
        kept[rel] = (data, mode == "100755")
    omitted.sort(key=lambda o: o["path"])

    name = f"{session.source}-{re.sub(r'[^A-Za-z0-9]', '', session.id)[:12] or 'session'}"
    task = out_root / name
    if task.exists():
        shutil.rmtree(task)
    workspace = task / "environment" / "workspace"
    for rel, (data, executable) in kept.items():
        target = workspace.joinpath(*PurePosixPath(rel).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if executable:
            target.chmod(0o755)
    (task / "environment").mkdir(parents=True, exist_ok=True)
    (task / "environment" / "Dockerfile").write_text(_dockerfile(bool(kept)))
    (task / "environment" / "omitted_files.json").write_text(
        json.dumps({"start_commit": commit, "files": omitted}, indent=2) + "\n"
    )
    (task / "instruction.md").write_text(instruction)
    for folder, what in (("solution", "reference solution"), ("tests", "verifier")):
        script = task / folder / ("solve.sh" if folder == "solution" else "test.sh")
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text(PLACEHOLDER.format(what=what))
        script.chmod(0o755)
    description = " ".join(instruction.split())[:200]
    # Harbor names a task "<org>/<name>"
    (task / "task.toml").write_text(
        _task_toml(f"{session.source}/{name}", description, session, commit, len(omitted))
    )
    (task / "README.md").write_text(
        f"# {name}\n\nSaved from {session.source} session `{session.id}`: `{WORKDIR}` "
        f"starts as the repository at commit `{commit[:12]}`, before the session. "
        "The verifier and reference solution are written by Harbor Hub.\n"
    )
    archive = pack(task)
    return {
        "task": str(task),
        "archive": str(archive),
        "archive_bytes": archive.stat().st_size,
        "source": session.source,
        "session_id": session.id,
        "start_commit": commit,
        "instruction": instruction if len(instruction) <= 600 else instruction[:600] + "…",
        "files_kept": len(kept),
        "files_omitted": {
            reason: sum(1 for o in omitted if o["reason"] == reason)
            for reason in sorted({o["reason"] for o in omitted})
        },
        "secrets_left_out": secret_files,
    }


def pack(task: Path) -> Path:
    archive = task.parent / f"{task.name}.tar.gz"
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for path in [task, *sorted(task.rglob("*"))]:
            rel = path.relative_to(task).as_posix()
            info = tar.gettarinfo(str(path), arcname=task.name if rel == "." else f"{task.name}/{rel}")
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            if path.is_file():
                with path.open("rb") as f:
                    tar.addfile(info, f)
            else:
                tar.addfile(info)
    archive.write_bytes(buf.getvalue())
    return archive


# ── Harbor Hub ──


def _client_id() -> str:
    if not HUB_CLIENT_ID:
        raise CaptureError("HARBOR_HUB_CLIENT_ID is not set: submitting is not set up yet")
    return HUB_CLIENT_ID


def _http(method: str, url: str, *, form=None, body=None, token=None, headers=None, data=None):
    req_headers = {"Accept": "application/json", **(headers or {})}
    payload = data
    if form is not None:
        payload = urllib.parse.urlencode(form).encode()
        req_headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif body is not None:
        payload = json.dumps(body).encode()
        req_headers["Content-Type"] = "application/json"
    if token:
        req_headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=payload, method=method, headers=req_headers)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            text = response.read().decode()
            return response.status, (json.loads(text) if text.strip() else {})
    except urllib.error.HTTPError as exc:
        text = exc.read().decode(errors="replace")
        try:
            return exc.code, json.loads(text)
        except ValueError:
            return exc.code, {"detail": text[:300]}


def _load_credentials() -> dict | None:
    try:
        data = json.loads(CREDENTIALS.read_text())
    except (OSError, ValueError):
        return None
    return data if data.get("hub") == HUB_URL else None


def _save_credentials(tokens: dict) -> None:
    CREDENTIALS.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "hub": HUB_URL,
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "expires_at": time.time() + float(tokens.get("expires_in", 3600)),
    }
    fd = os.open(CREDENTIALS, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)


def login() -> dict:
    """Authorize in the browser (OAuth 2.0 with PKCE, back to a one-off
    listener on 127.0.0.1)."""
    client_id = _client_id()
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(24)
    result: dict = {}

    class Callback(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
            ok = query.get("state", [""])[0] == state and "code" in query
            result.update(code=query.get("code", [""])[0] if ok else "", error=query.get("error", [""])[0])
            self.send_response(200 if ok else 400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            words = "Harbor Hub is connected." if ok else "Harbor Hub was not connected."
            self.wfile.write(f"<p>{words} You can close this tab.</p>".encode())

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Callback)
    redirect_uri = f"http://127.0.0.1:{server.server_port}/callback"
    query = urllib.parse.urlencode({
        "response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri,
        "scope": "tasks:submit tasks:read", "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256",
    })  # fmt: skip
    url = f"{HUB_URL}/oauth/authorize?{query}"
    print(f"Opening your browser to sign in to Harbor Hub:\n  {url}", file=sys.stderr)
    webbrowser.open(url)
    thread = threading.Thread(target=server.handle_request, daemon=True)
    server.timeout = 600
    thread.start()
    thread.join(610)
    server.server_close()
    if not result.get("code"):
        raise CaptureError(f"Harbor Hub was not connected ({result.get('error') or 'no answer'})")
    status, tokens = _http("POST", f"{HUB_URL}/oauth/token", form={
        "grant_type": "authorization_code", "code": result["code"], "redirect_uri": redirect_uri,
        "client_id": client_id, "code_verifier": verifier,
    })  # fmt: skip
    if status != 200:
        raise CaptureError(f"Harbor Hub refused the sign-in: {tokens.get('error_description') or tokens}")
    _save_credentials(tokens)
    return _hub("GET", "/api/contrib/me")


def logout() -> None:
    creds = _load_credentials()
    if creds and HUB_CLIENT_ID:
        _http("POST", f"{HUB_URL}/oauth/revoke", form={"token": creds["refresh_token"], "client_id": HUB_CLIENT_ID})
    CREDENTIALS.unlink(missing_ok=True)


def _token() -> str:
    creds = _load_credentials()
    if creds is None:
        raise CaptureError("not signed in to Harbor Hub: run `capture.py login`")
    if creds["expires_at"] - 60 > time.time():
        return creds["access_token"]
    status, tokens = _http("POST", f"{HUB_URL}/oauth/token", form={
        "grant_type": "refresh_token", "refresh_token": creds["refresh_token"], "client_id": _client_id(),
    })  # fmt: skip
    if status != 200:
        CREDENTIALS.unlink(missing_ok=True)
        raise CaptureError("your Harbor Hub sign-in ended: run `capture.py login`")
    _save_credentials(tokens)
    return tokens["access_token"]


def _hub(method: str, path: str, body=None) -> dict:
    status, payload = _http(method, f"{HUB_URL}{path}", body=body, token=_token())
    if status >= 400:
        detail = payload.get("detail")
        message = detail if isinstance(detail, str) else (detail or {}).get("message") or f"HTTP {status}"
        if status == 403 and isinstance(detail, dict) and detail.get("error") == "agreement":
            message += " — run `capture.py login` to read and accept it"
        raise CaptureError(f"Harbor Hub: {message}")
    return payload


def submit(target: Path) -> dict:
    """Upload a saved task (its folder, or the archive ``save`` wrote beside
    it) and submit it; the submission as Harbor Hub reports it."""
    if target.is_dir():
        folder, archive = target, pack(target)
    elif target.is_file() and target.name.endswith(".tar.gz"):
        folder, archive = target.with_name(target.name[: -len(".tar.gz")]), target
    else:
        raise CaptureError(f"no saved task at {target}")
    source = "other"
    toml = folder / "task.toml"
    if toml.is_file():
        found = re.search(r'^source = "(\w+)"', toml.read_text(), re.M)
        source = found.group(1) if found and found.group(1) in SOURCES else "other"
    data = archive.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    slot = _hub("POST", "/api/contrib/uploads", {"size": len(data), "sha256": sha256})
    status, _ = _http("PUT", slot["upload_url"], data=data, headers={
        "Content-Range": f"bytes 0-{len(data) - 1}/{len(data)}", "Content-Type": "application/gzip",
    })  # fmt: skip
    if status >= 300:
        raise CaptureError(f"the upload failed (HTTP {status})")
    return _hub("POST", "/api/contrib/submissions", {"sha256": sha256, "source": source})


# ── the command line ──


def _print(data, as_json: bool, lines) -> None:
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for line in lines(data):
            print(line)


def _summary_lines(s: dict):
    yield f"Saved {s['task']}"
    yield f"  archive: {s['archive']} ({s['archive_bytes'] / 1024:.0f} KB)"
    yield f"  workspace: {s['files_kept']} files, from commit {s['start_commit'][:12]}"
    for reason, n in s["files_omitted"].items():
        yield f"  left out: {n} ({reason})"
    for f in s["secrets_left_out"]:
        kinds = ", ".join(sorted({h["kind"] for h in f["hits"]}))
        yield f"  left out, looks like a secret: {f['path']} ({kinds})"
    yield "Instruction:"
    yield from ("  " + line for line in s["instruction"].splitlines())


def _submission_lines(s: dict):
    yield f"{s['id']}: {s['stage']}" + (f" ({s['task']} rev {s['revision']})" if s.get("task") else "")
    for e in s.get("errors") or []:
        yield f"  {e}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("sessions", help="recent sessions in this folder")
    p.add_argument("--from", dest="source", choices=SOURCES, default="claude")
    p.add_argument("--cwd", type=Path, default=Path.cwd())
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("save", help="save a session as a Harbor task")
    p.add_argument("--from", dest="source", choices=SOURCES, default="claude")
    p.add_argument("--session", help="the session id (default: the newest in --cwd)")
    p.add_argument("--transcript", type=Path, help="the session's transcript file")
    p.add_argument("--cwd", type=Path, default=Path.cwd())
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--exclude", action="append", default=[], help="a path to leave out (repeatable)")
    p.add_argument("--json", action="store_true")
    sub.add_parser("login", help="sign in to Harbor Hub in the browser")
    sub.add_parser("logout", help="sign out of Harbor Hub")
    p = sub.add_parser("submit", help="submit a saved task to Harbor Hub")
    p.add_argument("task", type=Path)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("status", help="how a submission is going")
    p.add_argument("id")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("list", help="your submissions")
    p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "sessions":
            rows = []
            for transcript in _transcripts(args.source)[:200]:
                try:
                    s = Session(args.source, transcript)
                except CaptureError:
                    continue
                if _same_dir(s.cwd, args.cwd) and s.messages:
                    rows.append({"id": s.id, "started": s.started and s.started.isoformat(),
                                 "first_message": s.messages[0][:120]})  # fmt: skip
                if len(rows) >= 15:
                    break
            _print(rows, args.json, lambda r: (f"{x['id']}  {x['started']}  {x['first_message']}" for x in r))
        elif args.command == "save":
            session = (
                Session(args.source, args.transcript)
                if args.transcript
                else find_session(args.source, args.session, args.cwd.resolve())
            )
            args.out.mkdir(parents=True, exist_ok=True)
            _print(save(session, args.out, args.exclude), args.json, _summary_lines)
        elif args.command == "login":
            me = login()
            print(f"Signed in to Harbor Hub as {me.get('name') or me.get('email')}.")
        elif args.command == "logout":
            logout()
            print("Signed out of Harbor Hub.")
        elif args.command == "submit":
            _print(submit(args.task), args.json, _submission_lines)
        elif args.command == "status":
            _print(_hub("GET", f"/api/contrib/submissions/{urllib.parse.quote(args.id)}"), args.json, _submission_lines)
        elif args.command == "list":
            rows = _hub("GET", "/api/contrib/submissions")
            _print(rows, args.json, lambda r: (line for s in r for line in _submission_lines(s)))
    except CaptureError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
