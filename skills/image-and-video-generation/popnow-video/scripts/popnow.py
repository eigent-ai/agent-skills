#!/usr/bin/env python3
"""PopNow API helper for agent skills: quote, create, wait and download AI generations.

Dependency-free: Python 3.8+ standard library only (urllib). Works the same in
Claude Code, Codex, Claude.ai code execution or any shell.

Authentication: export POPNOW_API_KEY="sk-popnow-..." (create one at
https://popnow.ai/api/console/keys). Optional: POPNOW_BASE_URL (default
https://api.popnow.ai).

Spending rule: `create` never spends credits the user has not confirmed. It
quotes the exact request first and refuses to start when the price is above
--confirm-credits. Always run `quote`, tell the user the credit price, and only
then run `create --confirm-credits <that number>`.

Typical flow:
  popnow.py quote  --model minimax/h3/text-to-video --prompt "A paper boat on a lake"
  popnow.py create --model minimax/h3/text-to-video --prompt "A paper boat on a lake" \
      --confirm-credits 185 --download ./out
  popnow.py wait job_...          # resume waiting on an existing task
  popnow.py download job_... --out ./out

Exit codes: 0 ok, 1 API or network error, 2 bad usage, 3 needs confirmation
(price above the confirmed amount), 4 still running after --timeout,
5 the task finished but did not succeed.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import random
import sys
import time
import uuid
from urllib import error as urlerror
from urllib import parse as urlparse
from urllib import request as urlrequest

__version__ = "1.0.0"

DEFAULT_BASE_URL = "https://api.popnow.ai"
USER_AGENT = "popnow-skills/" + __version__ + " (python)"
PRICING_URL = "https://popnow.ai/pricing"
KEYS_URL = "https://popnow.ai/api/console/keys"

TERMINAL_STATES = ("succeeded", "failed", "canceled", "expired")
# Business codes that can succeed on a second attempt (see the Errors docs).
RETRYABLE_CODES = (429, 500, 503, 50301)

UPLOAD_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".safetensors": "application/octet-stream",
}

MIME_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/flac": ".flac",
    "audio/ogg": ".ogg",
}

EXIT_API, EXIT_USAGE, EXIT_CONFIRM, EXIT_TIMEOUT, EXIT_TASK_FAILED = 1, 2, 3, 4, 5


class PopNowError(Exception):
    """An error envelope ({code,msg,request_id}) or a transport failure."""

    def __init__(self, message, code=None, http_status=None, request_id=None, reason=None, retry_after=None,
                 transport=False):
        super().__init__(message)
        self.transport = transport
        self.message = message
        self.code = code
        self.http_status = http_status
        self.request_id = request_id
        self.reason = reason
        self.retry_after = retry_after

    def __str__(self):
        parts = []
        if self.code is not None:
            parts.append("code %s" % self.code)
        if self.reason:
            parts.append("reason %s" % self.reason)
        if self.request_id:
            parts.append("request_id %s" % self.request_id)
        suffix = " (" + ", ".join(parts) + ")" if parts else ""
        return self.message + suffix + hint_for(self.code)


class UsageError(Exception):
    """Bad command-line usage (exit code 2)."""


def hint_for(code):
    hints = {
        401: " Hint: set POPNOW_API_KEY to a valid sk-popnow- key from " + KEYS_URL + ".",
        40201: " Hint: not enough credits. Top up at " + PRICING_URL + ".",
        40202: " Hint: a spend cap on this API key was reached; raise it in the API console.",
        40301: " Hint: this key is not allowed to call this model; check the key's allowed models.",
        40310: " Hint: verify the account's email address first.",
        40901: " Hint: the quote expired or the price changed. Quote again and re-confirm with the user.",
        50301: " Hint: the model cannot take tasks right now; try later or pick another model.",
    }
    return hints.get(code, "")


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------


class Client:
    """Minimal client for the PopNow native API (`/api/v1/*`)."""

    def __init__(self, api_key=None, base_url=None, timeout=90, language=None):
        self.api_key = api_key if api_key is not None else os.environ.get("POPNOW_API_KEY", "")
        self.base_url = (base_url or os.environ.get("POPNOW_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.language = language

    def _headers(self, extra=None):
        if not self.api_key:
            raise UsageError("POPNOW_API_KEY is not set. Create a key at %s and export POPNOW_API_KEY." % KEYS_URL)
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if self.language:
            headers["Accept-Language"] = self.language
        if extra:
            headers.update(extra)
        return headers

    def call(self, method, path, query=None, body=None, headers=None, attempts=4, timeout=None):
        """Send one request and return (http_status, data, response_headers).

        Retries network errors and retryable business codes with backoff. Every
        POST that creates something must carry an Idempotency-Key, so a retry
        can never run (or charge) the same work twice.
        """
        url = self.base_url + path
        if query:
            pairs = [(k, v) for k, v in query.items() if v is not None and v != ""]
            if pairs:
                url += "?" + urlparse.urlencode(pairs)
        payload = None
        hdrs = self._headers(headers)
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            hdrs["Content-Type"] = "application/json"
        last = None
        for attempt in range(attempts):
            try:
                return self._once(method, url, payload, hdrs, timeout or self.timeout)
            except PopNowError as exc:
                last = exc
                if not (exc.transport or exc.code in RETRYABLE_CODES) or attempt == attempts - 1:
                    raise
                delay = exc.retry_after if exc.retry_after else (2 ** attempt) + random.random() / 2
                time.sleep(min(float(delay), 30.0))
        raise last  # pragma: no cover

    def _once(self, method, url, payload, headers, timeout):
        req = urlrequest.Request(url, data=payload, headers=headers, method=method)
        try:
            with urlrequest.urlopen(req, timeout=timeout) as res:
                return parse_envelope(res.status, res.read(), dict(res.headers.items()))
        except urlerror.HTTPError as exc:
            raw = exc.read() if hasattr(exc, "read") else b""
            return parse_envelope(exc.code, raw, dict(exc.headers.items()) if exc.headers else {})
        except (urlerror.URLError, TimeoutError, ConnectionError, OSError) as exc:
            raise PopNowError("Network error talking to %s: %s" % (url.split("?")[0], exc), transport=True)

    def get(self, path, query=None, **kw):
        return self.call("GET", path, query=query, **kw)[1]

    def post(self, path, body=None, query=None, headers=None, **kw):
        return self.call("POST", path, query=query, body=body if body is not None else {}, headers=headers, **kw)


def parse_envelope(status, raw, headers):
    """Turn a response into (status, data, headers) or raise PopNowError."""
    lower = {k.lower(): v for k, v in (headers or {}).items()}
    retry_after = None
    if lower.get("retry-after", "").strip().isdigit():
        retry_after = int(lower["retry-after"].strip())
    try:
        envelope = json.loads(raw.decode("utf-8")) if raw else None
    except (ValueError, UnicodeDecodeError):
        envelope = None
    if not isinstance(envelope, dict) or "code" not in envelope:
        snippet = raw[:200].decode("utf-8", "replace") if raw else ""
        raise PopNowError(
            "HTTP %s with a non-JSON response: %s" % (status, snippet.strip()),
            http_status=status,
            code=status if status >= 400 else None,
            retry_after=retry_after,
            # A gateway page (502/504/52x) carries no envelope; with an Idempotency-Key a retry is safe.
            transport=status in (502, 503, 504) or 520 <= status <= 524,
        )
    code = envelope.get("code")
    if code == 200 and status < 400:
        return status, envelope.get("data"), headers
    data = envelope.get("data")
    reason = data.get("reason") if isinstance(data, dict) else None
    raise PopNowError(
        str(envelope.get("msg") or "Request failed"),
        code=code,
        http_status=status,
        request_id=envelope.get("request_id") or lower.get("x-request-id"),
        reason=reason,
        retry_after=retry_after,
    )


# ---------------------------------------------------------------------------
# Models and input building
# ---------------------------------------------------------------------------


def model_path(model):
    # Model IDs contain slashes (`<maker>/<model>/<task>`); the API accepts them as is.
    return "/api/v1/models/" + urlparse.quote(model, safe="/")


def get_model(client, model):
    return client.get(model_path(model))


def schema_properties(client, model):
    """Return the model's inputSchema properties, or None if it cannot be read."""
    try:
        record = get_model(client, model)
    except PopNowError as exc:
        if exc.code == 404:
            raise UsageError("Unknown model %r. List models with: popnow.py models --search <name>" % model)
        return None
    schema = (record or {}).get("inputSchema") or {}
    props = schema.get("properties")
    return props if isinstance(props, dict) else None


def parse_value(text):
    """`--set key=value` values: JSON when they parse (numbers, booleans, lists), otherwise strings."""
    try:
        return json.loads(text)
    except ValueError:
        return text


def is_remote_ref(value):
    return value.startswith(("https://", "http://", "popnow://", "data:"))


def resolve_media(client, value):
    """A public URL, popnow:// URI or data URI passes through; a local file is uploaded first."""
    if is_remote_ref(value):
        return value
    path = os.path.expanduser(value)
    if os.path.isfile(path):
        return upload_file(client, path)["uri"]
    raise UsageError("%r is neither a URL (https://, popnow://, data:) nor an existing local file." % value)


def place_media(inp, props, single, plural, values, label):
    """Put media values in the field the model declares: `<x>_url` or `<x>_urls`."""
    if not values:
        return
    has_single = props is None or single in props
    has_plural = props is not None and plural in props
    if props is None and len(values) > 1:
        has_single, has_plural = False, True
    if len(values) == 1 and has_single:
        inp[single] = values[0]
    elif has_plural:
        inp[plural] = list(values)
    elif has_single:
        raise UsageError("This model takes one %s in %r; got %d. Use --set for other fields." % (label, single, len(values)))
    else:
        fields = ", ".join(sorted(props or {})) or "none"
        raise UsageError("This model has no %s input (%s/%s). Its input fields: %s" % (label, single, plural, fields))


def build_input(client, args):
    """Combine --input/--input-file, the shortcut flags and --set into one `input` object."""
    inp = {}
    if getattr(args, "input_file", None):
        with open(os.path.expanduser(args.input_file), "r", encoding="utf-8") as fh:
            inp.update(json.load(fh))
    if getattr(args, "input", None):
        try:
            extra = json.loads(args.input)
        except ValueError as exc:
            raise UsageError("--input is not valid JSON: %s" % exc)
        if not isinstance(extra, dict):
            raise UsageError("--input must be a JSON object")
        inp.update(extra)

    simple = (
        ("prompt", "prompt"),
        ("text", "text"),
        ("negative_prompt", "negative_prompt"),
        ("lyrics", "lyrics"),
        ("title", "title"),
        ("voice", "voice_id"),
        ("aspect_ratio", "aspect_ratio"),
        ("resolution", "resolution"),
        ("output_format", "output_format"),
    )
    for attr, field in simple:
        value = getattr(args, attr, None)
        if value is not None:
            inp[field] = value
    if getattr(args, "duration", None) is not None:
        inp["duration_seconds"] = args.duration
    if getattr(args, "seed", None) is not None:
        inp["seed"] = args.seed

    images = getattr(args, "image", None) or []
    videos = getattr(args, "video", None) or []
    audios = getattr(args, "audio", None) or []
    last_image = getattr(args, "last_image", None)
    if images or videos or audios or last_image:
        props = schema_properties(client, args.model)
        place_media(inp, props, "image_url", "image_urls", [resolve_media(client, v) for v in images], "image")
        place_media(inp, props, "video_url", "video_urls", [resolve_media(client, v) for v in videos], "video")
        place_media(inp, props, "audio_url", "audio_urls", [resolve_media(client, v) for v in audios], "audio")
        if last_image:
            if props is not None and "last_image_url" not in props:
                raise UsageError("This model has no last_image_url input.")
            inp["last_image_url"] = resolve_media(client, last_image)

    for item in getattr(args, "set", None) or []:
        if "=" not in item:
            raise UsageError("--set expects key=value, got %r" % item)
        key, value = item.split("=", 1)
        inp[key.strip()] = parse_value(value)
    return inp


def task_body(model, inp, callback=None):
    body = {"model": model, "input": inp}
    if callback:
        body["callBackUrl"] = callback
    return body


# ---------------------------------------------------------------------------
# Quote, create, wait, download
# ---------------------------------------------------------------------------


def quote(client, body):
    """POST /api/v1/jobs/quote: price of this exact request. Creates nothing, holds nothing."""
    return client.post("/api/v1/jobs/quote", body)[1]


def balance(client):
    return client.get("/api/v1/chat/credit")


def credits_text(n):
    return "1 credit" if n == 1 else "%s credits" % n


def describe_quote(q, bal=None):
    max_c, exp_c = q.get("maxCredits"), q.get("expectedCredits")
    lines = [
        "Model:      %s" % q.get("model"),
        "Price:      %s max (usually %s), $%s USD"
        % (credits_text(max_c), credits_text(exp_c), q.get("maxCharge") or q.get("estimatedCost")),
        "Billed:     %s (%s)" % (q.get("quantity"), q.get("unit")),
        "Quote:      %s (valid until %s)" % (q.get("quoteId"), q.get("expiresAt")),
    ]
    if bal is not None:
        lines.append("Balance:    %s available" % credits_text(bal.get("availableCredits")))
        if isinstance(max_c, int) and isinstance(bal.get("availableCredits"), int) and bal["availableCredits"] < max_c:
            lines.append("WARNING:    not enough credits for this request. Top up at %s" % PRICING_URL)
    lines.append("Next:       tell the user the price; after they agree, run create with --confirm-credits %s" % max_c)
    lines.append("            (failed or expired tasks are refunded automatically)")
    return "\n".join(lines)


def create(client, body, confirm_credits, idempotency_key=None, wait_seconds=None, retention=None):
    """Quote, check the price against what the user confirmed, then createTask.

    Returns (quote, http_status, data, idempotency_key). `data` is the task
    record when `wait_seconds` was given and the task finished in time (HTTP
    200), otherwise the accepted task (HTTP 202). Raises ConfirmationNeeded when the price
    is above `confirm_credits`; nothing is created or held in that case.
    """
    if confirm_credits is None or confirm_credits < 0:
        raise UsageError("--confirm-credits is required: quote first and pass the credit price the user agreed to.")
    q = quote(client, body)
    max_c = q.get("maxCredits")
    if not isinstance(max_c, int) or max_c > confirm_credits:
        raise ConfirmationNeeded(q, confirm_credits)
    full = dict(body)
    full["quoteId"] = q.get("quoteId")
    full["expectedCredits"] = max_c
    headers = {"Idempotency-Key": idempotency_key or new_idempotency_key()}
    if retention is not None:
        headers["X-PopNow-Retention"] = str(retention)
    query = {"wait": int(wait_seconds)} if wait_seconds else None
    timeout = client.timeout + (int(wait_seconds) if wait_seconds else 0)
    status, data, _ = client.call("POST", "/api/v1/jobs/createTask", query=query, body=full, headers=headers, timeout=timeout)
    return q, status, data, headers["Idempotency-Key"]


class ConfirmationNeeded(Exception):
    def __init__(self, q, confirmed):
        super().__init__("price above confirmed amount")
        self.quote = q
        self.confirmed = confirmed

    def __str__(self):
        return (
            "Not started, nothing was charged: this request costs up to %s, more than the %s the user confirmed. "
            "Tell the user the new price and, if they agree, run again with --confirm-credits %s."
            % (credits_text(self.quote.get("maxCredits")), credits_text(self.confirmed), self.quote.get("maxCredits"))
        )


def new_idempotency_key():
    return "skill-" + uuid.uuid4().hex


def record(client, task_id):
    return client.get("/api/v1/jobs/recordInfo", {"taskId": task_id})


def poll_interval(elapsed):
    # Gentle polling: every 3 s at first (images), then 10-15 s (video).
    if elapsed < 30:
        return 3
    if elapsed < 120:
        return 10
    return 15


def wait_task(client, task_id, timeout=1200, quiet=False):
    """Poll recordInfo until the task is final or `timeout` seconds pass."""
    start = time.time()
    last_state = None
    while True:
        task = record(client, task_id)
        state = task.get("state")
        if not quiet and state != last_state:
            log("[%s] %s" % (task_id, state))
            last_state = state
        if state in TERMINAL_STATES:
            return task
        elapsed = time.time() - start
        if elapsed >= timeout:
            raise WaitTimeout(task)
        time.sleep(min(poll_interval(elapsed), max(1, timeout - elapsed)))


class WaitTimeout(Exception):
    def __init__(self, task):
        super().__init__("timeout")
        self.task = task


def extension_for(mime, url):
    if mime and mime.split(";")[0].strip() in MIME_EXTENSIONS:
        return MIME_EXTENSIONS[mime.split(";")[0].strip()]
    path_ext = os.path.splitext(urlparse.urlparse(url).path)[1]
    if path_ext and len(path_ext) <= 6:
        return path_ext
    return mimetypes.guess_extension(mime or "") or ".bin"


def fetch_to_file(url, dest):
    # Signed output links are bearer links: never attach the API key to them.
    req = urlrequest.Request(url, headers={"User-Agent": USER_AGENT})
    tmp = dest + ".part"
    try:
        with urlrequest.urlopen(req, timeout=300) as res, open(tmp, "wb") as fh:
            while True:
                chunk = res.read(1 << 16)
                if not chunk:
                    break
                fh.write(chunk)
    except (urlerror.URLError, OSError) as exc:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise PopNowError("Download failed for %s: %s" % (dest, exc))
    os.replace(tmp, dest)
    return dest


def download_task(client, task_id, out_dir, task=None):
    """Download every ready output of a succeeded task. Returns the saved paths."""
    task = task or record(client, task_id)
    if task.get("state") != "succeeded":
        raise PopNowError("Task %s is %s; only succeeded tasks have files." % (task_id, task.get("state")))
    os.makedirs(out_dir, exist_ok=True)
    assets = ((task.get("output") or {}).get("assets")) or []
    saved = []
    for index, asset in enumerate(assets):
        if asset.get("unavailable") or asset.get("deleted") or asset.get("pending"):
            continue
        url = asset.get("url")
        if not url and asset.get("key"):
            url = client.post("/api/v1/common/download-url", {"taskId": task_id, "key": asset["key"]})[1].get("url")
        if not url:
            continue
        role = asset.get("role")
        suffix = "-%s" % role if role and role not in ("video", "image", "audio") else ""
        name = "%s-%d%s%s" % (task_id, index, suffix, extension_for(asset.get("mime"), url))
        saved.append(fetch_to_file(url, os.path.join(out_dir, name)))
    text = (task.get("output") or {}).get("text")
    if text:
        path = os.path.join(out_dir, "%s.txt" % task_id)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        saved.append(path)
    return saved


def upload_file(client, path):
    """Upload a local file (ticket, PUT, commit) and return the commit record with its popnow:// `uri`."""
    ext = os.path.splitext(path)[1].lower()
    content_type = UPLOAD_TYPES.get(ext)
    if not content_type:
        raise UsageError("Unsupported file type %r. Supported: %s" % (ext or path, ", ".join(sorted(UPLOAD_TYPES))))
    size = os.path.getsize(path)
    ticket = client.post("/api/v1/common/upload-url", {"contentType": content_type, "bytes": size})[1]
    headers = dict(ticket.get("headers") or {})
    headers.setdefault("Content-Type", content_type)
    headers.setdefault("Content-Length", str(size))
    headers["User-Agent"] = USER_AGENT
    with open(path, "rb") as fh:
        req = urlrequest.Request(ticket["uploadUrl"], data=fh, headers=headers, method=ticket.get("method") or "PUT")
        try:
            with urlrequest.urlopen(req, timeout=600) as res:
                res.read()
        except urlerror.HTTPError as exc:
            raise PopNowError("Upload PUT failed with HTTP %s" % exc.code, http_status=exc.code)
        except (urlerror.URLError, OSError) as exc:
            raise PopNowError("Upload PUT failed: %s" % exc)
    return client.post("/api/v1/files/%s/commit" % urlparse.quote(ticket["fileId"]), {})[1]


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def log(message):
    print(message, file=sys.stderr)


def emit(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def summarize_task(task):
    lines = ["Task:       %s" % task.get("taskId"), "Model:      %s" % task.get("model"), "State:      %s" % task.get("state")]
    if "credits" in task:
        settled = task.get("settled")
        lines.append("Credits:    %s (%s)" % (task.get("credits"), "final charge" if settled else "held, not charged yet"))
    if task.get("errorCode"):
        lines.append("Error:      %s: %s" % (task.get("errorCode"), task.get("errorMessage", "")))
        lines.append("            the hold was released, nothing was charged")
    for i, asset in enumerate(((task.get("output") or {}).get("assets")) or []):
        bits = [asset.get("mime") or "file"]
        if asset.get("width") and asset.get("height"):
            bits.append("%sx%s" % (asset["width"], asset["height"]))
        if asset.get("durationSeconds"):
            bits.append("%ss" % asset["durationSeconds"])
        lines.append("Output %d:   %s %s" % (i, " ".join(bits), asset.get("url") or "(no link yet)"))
    text = (task.get("output") or {}).get("text")
    if text:
        lines.append("Text:       %s" % (text if len(text) < 400 else text[:400] + "..."))
    return "\n".join(lines)


def price_text(credits):
    if not isinstance(credits, dict):
        return "-"
    per = credits.get("perUnit")
    unit = (credits.get("unit") or "").replace("per_", "/")
    if isinstance(per, (int, float)):
        per = ("%.2f" % per).rstrip("0").rstrip(".")
    return "from %s cr%s" % (per, unit)


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def add_input_flags(p):
    g = p.add_argument_group("model input (combined into the request's `input` object)")
    g.add_argument("--model", required=True, help="Model ID, e.g. minimax/h3/image-to-video (see `models`)")
    g.add_argument("--prompt", help="Text prompt (`prompt`)")
    g.add_argument("--text", help="Text to speak, for text-to-speech models (`text`)")
    g.add_argument("--negative-prompt", dest="negative_prompt", help="`negative_prompt`")
    g.add_argument("--image", action="append", help="Image URL, popnow:// URI or local file (repeatable); goes to image_url or image_urls")
    g.add_argument("--last-image", dest="last_image", help="Closing frame for models with `last_image_url`")
    g.add_argument("--video", action="append", help="Video URL, popnow:// URI or local file; goes to video_url(s)")
    g.add_argument("--audio", action="append", help="Audio URL, popnow:// URI or local file; goes to audio_url(s)")
    g.add_argument("--duration", type=int, help="`duration_seconds`")
    g.add_argument("--resolution", help="`resolution`, e.g. 768p, 720p, 1k, 2k")
    g.add_argument("--aspect-ratio", dest="aspect_ratio", help="`aspect_ratio`, e.g. 16:9, 9:16, 1:1")
    g.add_argument("--seed", type=int, help="`seed`")
    g.add_argument("--lyrics", help="`lyrics` (music models)")
    g.add_argument("--title", help="`title` (music models)")
    g.add_argument("--voice", help="`voice_id` (speech models)")
    g.add_argument("--output-format", dest="output_format", help="`output_format`, e.g. png, jpeg")
    g.add_argument("--set", action="append", metavar="KEY=VALUE", help="Any other input field; VALUE is parsed as JSON when possible (repeatable)")
    g.add_argument("--input", help="Full or partial `input` as a JSON object")
    g.add_argument("--input-file", dest="input_file", help="Read `input` from a JSON file")
    g.add_argument("--callback", help="Public HTTPS callBackUrl that receives the finished task (webhook)")


def add_create_flags(p):
    p.add_argument("--confirm-credits", dest="confirm_credits", type=int, required=True,
                   help="The credit price the user agreed to (maxCredits from `quote`). The task is not started if the price is higher.")
    p.add_argument("--idempotency-key", dest="idempotency_key",
                   help="Reuse the same key when retrying the same request so it never runs twice (default: a new random key)")
    p.add_argument("--retention", type=int, help="X-PopNow-Retention: keep outputs at most this many seconds")
    p.add_argument("--wait", action="store_true", help="Wait until the task is final and print the result")
    p.add_argument("--download", metavar="DIR", help="Wait, then download every output into DIR")
    p.add_argument("--timeout", type=int, default=1200, help="Seconds to wait with --wait/--download (default 1200)")


def finish_task(client, task, args):
    """Shared tail of create/wait: print, optionally download, pick the exit code."""
    if args.json:
        emit(task)
    else:
        print(summarize_task(task))
    if task.get("state") != "succeeded":
        return EXIT_TASK_FAILED
    out_dir = getattr(args, "download", None) or getattr(args, "out", None)
    if out_dir:
        for path in download_task(client, task["taskId"], out_dir, task=task):
            print("Saved:      %s" % path)
    return 0


def run_create(client, body, args):
    """Create (after the price check), then optionally wait and download."""
    want_wait = bool(args.wait or args.download)
    q, status, data, key = create(
        client, body, args.confirm_credits, idempotency_key=args.idempotency_key,
        wait_seconds=60 if want_wait else None, retention=args.retention,
    )
    task_id = data.get("taskId")
    if not args.json:
        print("Started:    %s (up to %s held; Idempotency-Key %s)" % (task_id, credits_text(data.get("estimatedCredits", data.get("credits"))), key))
    if not want_wait:
        if args.json:
            emit(data)
        else:
            print("State:      %s" % data.get("state"))
            print("Next:       popnow.py wait %s [--download DIR]" % task_id)
        return 0
    # HTTP 200 means `wait` saw the task finish: `data` is already the full record.
    task = data if status == 200 and data.get("state") in TERMINAL_STATES else None
    if task is None:
        try:
            task = wait_task(client, task_id, timeout=args.timeout, quiet=args.json)
        except WaitTimeout as exc:
            print("Still %s after %ss. Resume with: popnow.py wait %s" % (exc.task.get("state"), args.timeout, task_id))
            return EXIT_TIMEOUT
    return finish_task(client, task, args)


def cmd_balance(client, args):
    bal = balance(client)
    if args.json:
        return emit(bal)
    print("Available:  %s" % credits_text(bal.get("availableCredits")))
    print("Held:       %s (reserved by running tasks)" % credits_text(bal.get("heldCredits")))
    print("Total:      %s ($%s USD)" % (credits_text(bal.get("totalCredits")), bal.get("total")))
    print("Top up:     %s" % PRICING_URL)


def cmd_models(client, args):
    query = {"modality": args.modality, "task": args.task, "provider": args.provider, "search": args.search}
    if args.schema:
        query["includeSchema"] = "1"
    data = client.get("/api/v1/models", query)
    items = data.get("items") or []
    if args.json:
        return emit(data)
    for m in items:
        flag = "" if m.get("available", True) else "  [unavailable now]"
        print("%-52s %-26s %-6s %s%s" % (m.get("model"), (m.get("displayName") or "")[:26], m.get("modality"), price_text(m.get("credits")), flag))
    print("%d models. Exact price of one request: popnow.py quote --model <id> ..." % len(items))


def cmd_model(client, args):
    rec = get_model(client, args.model)
    if args.json:
        return emit(rec)
    print("Model:      %s (%s by %s)" % (rec.get("model"), rec.get("displayName"), rec.get("provider")))
    print("Price:      %s" % price_text(rec.get("credits")))
    for rule in (rec.get("credits") or {}).get("rules") or []:
        print("            %s when %s" % (price_text(dict(rule, unit=rule.get("unit") or rec["credits"].get("unit"))), json.dumps(rule.get("when"))))
    print("Available:  %s" % rec.get("available"))
    schema = rec.get("inputSchema") or {}
    required = set(schema.get("required") or [])
    print("Input fields:")
    for name, prop in sorted((schema.get("properties") or {}).items()):
        if not isinstance(prop, dict):
            continue
        bits = [prop.get("type") or "any"]
        if "enum" in prop:
            bits.append("one of " + ", ".join(str(v) for v in prop["enum"]))
        if "default" in prop:
            bits.append("default %s" % json.dumps(prop["default"]))
        for key in ("minimum", "maximum", "maxLength", "maxItems"):
            if key in prop:
                bits.append("%s %s" % (key, prop[key]))
        print("  %s%-22s %s" % ("*" if name in required else " ", name, "; ".join(bits)))
    print("(* = required. Full JSON: popnow.py model %s --json)" % rec.get("model"))


def cmd_quote(client, args):
    body = task_body(args.model, build_input(client, args), args.callback)
    q = quote(client, body)
    bal = None
    try:
        bal = balance(client)
    except PopNowError:
        pass
    if args.json:
        return emit({"quote": q, "balance": bal, "request": body})
    print(describe_quote(q, bal))


def cmd_create(client, args):
    body = task_body(args.model, build_input(client, args), args.callback)
    return run_create(client, body, args)


def cmd_status(client, args):
    task = record(client, args.task_id)
    if args.json:
        return emit(task)
    print(summarize_task(task))


def cmd_wait(client, args):
    try:
        task = wait_task(client, args.task_id, timeout=args.timeout, quiet=args.json)
    except WaitTimeout as exc:
        print("Still %s after %ss. Run `popnow.py wait %s` again." % (exc.task.get("state"), args.timeout, args.task_id))
        return EXIT_TIMEOUT
    return finish_task(client, task, args)


def cmd_download(client, args):
    paths = download_task(client, args.task_id, args.out)
    if args.json:
        return emit({"saved": paths})
    for path in paths:
        print("Saved:      %s" % path)
    if not paths:
        print("No downloadable outputs (they may have expired or been purged).")


def cmd_upload(client, args):
    rec = upload_file(client, os.path.expanduser(args.file))
    if args.json:
        return emit(rec)
    print("URI:        %s" % rec.get("uri"))
    print("Expires:    %s (uploads are temporary; use the URI in a task soon)" % rec.get("expiresAt"))


def cmd_jobs(client, args):
    query = {"state": args.state, "model": args.model, "from": args.date_from, "to": args.date_to, "limit": args.limit, "cursor": args.cursor}
    data = client.get("/api/v1/jobs", query)
    if args.json:
        return emit(data)
    items = data.get("items") or []
    for t in items:
        print("%-32s %-10s %-48s %s cr  %s" % (t.get("taskId"), t.get("state"), t.get("model"), t.get("credits"), t.get("createdAt")))
    print("%d tasks%s" % (len(items), "; more with --cursor %s" % data.get("nextCursor") if data.get("hasMore") else ""))


def cmd_usage(client, args):
    emit(client.get("/api/v1/usage", {"from": args.date_from, "to": args.date_to}))


def cmd_retry(client, args):
    if not args.yes:
        raise UsageError(
            "retry creates a new, billed task at today's price (it cannot be quoted first). "
            "Check the original price with `status`, confirm with the user, then pass --yes."
        )
    headers = {"Idempotency-Key": args.idempotency_key or new_idempotency_key()}
    data = client.post("/api/v1/jobs/retry", {"taskId": args.task_id}, headers=headers)[1]
    if args.json:
        return emit(data)
    print("Started:    %s (retry of %s, up to %s held)" % (data.get("taskId"), data.get("sourceTaskId"), credits_text(data.get("estimatedCredits"))))


def cmd_purge(client, args):
    if not args.yes:
        raise UsageError("purge permanently deletes the task's files and prompt (billing records stay). Pass --yes to confirm.")
    data = client.post("/api/v1/jobs/purge", {"taskId": args.task_id})[1]
    emit(data)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="popnow.py",
        description="PopNow API helper: quote, create, wait and download AI video, image and audio generations. "
        "Needs POPNOW_API_KEY. Always quote first and get the user's OK on the credit price before `create`.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Docs: https://popnow.ai/docs  API reference: https://popnow.ai/docs/openapi.yaml",
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="Print raw JSON instead of a summary")
    common.add_argument("--language", help="Accept-Language for error messages, e.g. en, de, ja")
    sub = parser.add_subparsers(dest="command", metavar="command")

    def add(name, func, help_text):
        p = sub.add_parser(name, parents=[common], help=help_text, description=help_text)
        p.set_defaults(func=func)
        return p

    add("balance", cmd_balance, "Show available and held credits")

    p = add("models", cmd_models, "List callable models with starting prices")
    p.add_argument("--modality", choices=("image", "video", "audio"))
    p.add_argument("--task", help="e.g. text-to-video, image-to-video, text-to-image, edit, text-to-audio, text-to-speech")
    p.add_argument("--provider", help="Exact model maker, e.g. google, kling")
    p.add_argument("--search", help="Free-text search")
    p.add_argument("--schema", action="store_true", help="Include input schemas (use with --json)")

    p = add("model", cmd_model, "Show one model: price tiers and input fields")
    p.add_argument("model")

    p = add("quote", cmd_quote, "Price one request exactly (creates nothing, charges nothing)")
    add_input_flags(p)

    p = add("create", cmd_create, "Quote, check against --confirm-credits, then start the task")
    add_input_flags(p)
    add_create_flags(p)

    p = add("status", cmd_status, "Read a task once")
    p.add_argument("task_id")

    p = add("wait", cmd_wait, "Poll a task until it is final")
    p.add_argument("task_id")
    p.add_argument("--timeout", type=int, default=1200, help="Seconds to wait (default 1200)")
    p.add_argument("--out", metavar="DIR", help="Download the outputs into DIR when it succeeds")

    p = add("download", cmd_download, "Download the outputs of a succeeded task")
    p.add_argument("task_id")
    p.add_argument("--out", default=".", metavar="DIR", help="Directory to save into (default: current)")

    p = add("upload", cmd_upload, "Upload a local image, video or audio file and print its popnow:// URI")
    p.add_argument("file")

    p = add("jobs", cmd_jobs, "List tasks created by this API key")
    p.add_argument("--state", choices=TERMINAL_STATES + ("queued", "running"))
    p.add_argument("--model")
    p.add_argument("--from", dest="date_from", help="UTC date YYYY-MM-DD (inclusive)")
    p.add_argument("--to", dest="date_to", help="UTC date YYYY-MM-DD (exclusive)")
    p.add_argument("--limit", type=int)
    p.add_argument("--cursor")

    p = add("usage", cmd_usage, "Usage and spend for this API key")
    p.add_argument("--from", dest="date_from")
    p.add_argument("--to", dest="date_to")

    p = add("retry", cmd_retry, "Create a new task from a failed or expired one (billed; needs --yes)")
    p.add_argument("task_id")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--idempotency-key", dest="idempotency_key")

    p = add("purge", cmd_purge, "Delete a finished task's files and prompt (needs --yes)")
    p.add_argument("task_id")
    p.add_argument("--yes", action="store_true")
    return parser


def main(argv=None, parser=None):
    parser = parser or build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return EXIT_USAGE
    client = Client(language=getattr(args, "language", None))
    try:
        result = args.func(client, args)
        return result if isinstance(result, int) else 0
    except UsageError as exc:
        log("Error: %s" % exc)
        return EXIT_USAGE
    except ConfirmationNeeded as exc:
        log(str(exc))
        return EXIT_CONFIRM
    except PopNowError as exc:
        log("PopNow error: %s" % exc)
        return EXIT_API
    except KeyboardInterrupt:
        log("Interrupted. A task that was already accepted keeps running; check it with `status`.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
