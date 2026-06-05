#!/usr/bin/env python3
"""Fetch Serenity posts from X through an existing CDP-compatible browser bridge.

This script intentionally uses only Python standard-library modules. It assumes
the PaiWork/front-end environment already provides a logged-in browser and an
HTTP CDP bridge compatible with:
  /health, /new, /eval, /scroll, /close
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_PROXY = "http://localhost:3456"
DEFAULT_HANDLE = "aleabitoreddit"
STATUS_RE = re.compile(r"/status/(\d+)")


EXTRACT_TWEETS_JS = r"""
(() => {
  const articles = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
  const normalizeUrl = (href) => {
    if (!href) return "";
    try {
      const url = new URL(href, location.origin);
      url.search = "";
      url.hash = "";
      return url.href;
    } catch {
      return "";
    }
  };
  const getMetric = (article, testid) => {
    const node = article.querySelector(`[data-testid="${testid}"]`);
    return node ? (node.getAttribute("aria-label") || node.textContent || "").trim() : "";
  };
  return JSON.stringify(articles.map((article) => {
    const time = article.querySelector("time");
    const statusLink = time ? time.closest("a") : null;
    const statusUrl = normalizeUrl(statusLink ? statusLink.getAttribute("href") : "");
    const textNode = article.querySelector('[data-testid="tweetText"]');
    const userNode = article.querySelector('[data-testid="User-Name"]');
    const handleLinks = Array.from(article.querySelectorAll('a[role="link"]'))
      .map((a) => a.getAttribute("href") || "")
      .filter((href) => /^\/[A-Za-z0-9_]{1,20}$/.test(href));
    const handle = handleLinks.length ? handleLinks[0].slice(1) : "";
    return {
      url: statusUrl,
      created_at: time ? time.getAttribute("datetime") || "" : "",
      author_label: userNode ? userNode.textContent.trim() : "",
      author_handle: handle,
      text: textNode ? textNode.textContent.trim() : "",
      reply_label: getMetric(article, "reply"),
      repost_label: getMetric(article, "retweet"),
      like_label: getMetric(article, "like")
    };
  }));
})()
""".strip()


class FetchError(RuntimeError):
    pass


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_iso(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = dt.datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except ValueError:
        return None


def request_json(
    proxy_url: str,
    path: str,
    *,
    method: str = "GET",
    body: str | None = None,
    timeout: int = 45,
) -> Any:
    url = proxy_url.rstrip("/") + path
    data = body.encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if body is not None:
        req.add_header("Content-Type", "text/plain; charset=utf-8")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise FetchError(f"Cannot reach CDP bridge at {proxy_url}: {exc}") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FetchError(f"CDP bridge returned non-JSON response from {path}: {raw[:300]}") from exc


def ensure_bridge(proxy_url: str) -> None:
    payload = request_json(proxy_url, "/health", timeout=10)
    if payload.get("status") != "ok":
        raise FetchError(f"CDP bridge health check failed: {payload}")


def open_timeline(proxy_url: str, handle: str) -> str:
    url = "https://x.com/" + handle.lstrip("@")
    path = "/new?url=" + urllib.parse.quote(url, safe="")
    payload = request_json(proxy_url, path, timeout=60)
    target_id = payload.get("targetId")
    if not target_id:
        raise FetchError(f"CDP bridge did not return targetId: {payload}")
    return str(target_id)


def eval_tweets(proxy_url: str, target_id: str) -> list[dict[str, Any]]:
    path = "/eval?target=" + urllib.parse.quote(target_id, safe="")
    payload = request_json(proxy_url, path, method="POST", body=EXTRACT_TWEETS_JS, timeout=45)
    if "error" in payload:
        raise FetchError(f"Tweet extraction failed: {payload['error']}")
    value = payload.get("value", "[]")
    if isinstance(value, str):
        rows = json.loads(value)
    else:
        rows = value
    if not isinstance(rows, list):
        raise FetchError(f"Tweet extraction returned unexpected value: {rows!r}")
    return [row for row in rows if isinstance(row, dict)]


def scroll(proxy_url: str, target_id: str) -> None:
    path = "/scroll?target=" + urllib.parse.quote(target_id, safe="") + "&y=2400&direction=down"
    request_json(proxy_url, path, timeout=45)


def close_target(proxy_url: str, target_id: str) -> None:
    path = "/close?target=" + urllib.parse.quote(target_id, safe="")
    try:
        request_json(proxy_url, path, timeout=15)
    except FetchError:
        pass


def status_id_from_url(url: str) -> str:
    match = STATUS_RE.search(url or "")
    return match.group(1) if match else ""


def normalize_tweet(row: dict[str, Any], source_handle: str, fetched_at: str) -> dict[str, Any] | None:
    url = str(row.get("url") or "")
    text = str(row.get("text") or "").strip()
    created_at = str(row.get("created_at") or "")
    status_id = status_id_from_url(url)
    if not status_id or not text:
        return None
    return {
        "id": status_id,
        "url": url,
        "created_at": created_at,
        "author_label": str(row.get("author_label") or "").strip(),
        "author_handle": str(row.get("author_handle") or "").strip() or source_handle.lstrip("@"),
        "text": text,
        "reply_label": str(row.get("reply_label") or "").strip(),
        "repost_label": str(row.get("repost_label") or "").strip(),
        "like_label": str(row.get("like_label") or "").strip(),
        "source_handle": source_handle.lstrip("@"),
        "fetched_at": fetched_at,
    }


def collect_tweets(proxy_url: str, handle: str, scrolls: int, pause_s: float) -> list[dict[str, Any]]:
    ensure_bridge(proxy_url)
    target_id = open_timeline(proxy_url, handle)
    seen: dict[str, dict[str, Any]] = {}
    fetched_at = utc_now().isoformat()
    try:
        time.sleep(max(pause_s, 0.0))
        for index in range(scrolls + 1):
            for row in eval_tweets(proxy_url, target_id):
                normalized = normalize_tweet(row, handle, fetched_at)
                if normalized:
                    seen[normalized["id"]] = normalized
            if index < scrolls:
                scroll(proxy_url, target_id)
                time.sleep(max(pause_s, 0.0))
    finally:
        close_target(proxy_url, target_id)
    return sorted(seen.values(), key=lambda item: item.get("created_at", ""), reverse=True)


def read_existing(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    rows: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            status_id = str(item.get("id") or "")
            if status_id:
                rows[status_id] = item
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_ids(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(row["id"] for row in rows) + "\n", encoding="utf-8")


def filter_daily(rows: list[dict[str, Any]], report_date: dt.date, since_hours: int) -> list[dict[str, Any]]:
    cutoff = utc_now() - dt.timedelta(hours=since_hours)
    selected: list[dict[str, Any]] = []
    for row in rows:
        created = parse_iso(str(row.get("created_at") or ""))
        if created is None:
            continue
        if created.date() == report_date or created >= cutoff:
            selected.append(row)
    return sorted(selected, key=lambda item: item.get("created_at", ""), reverse=True)


def render_daily(rows: list[dict[str, Any]], report_date: dt.date, handle: str) -> str:
    lines = [
        f"# Serenity Daily Intake - {report_date.isoformat()}",
        "",
        f"- source: https://x.com/{handle.lstrip('@')}",
        f"- fetched_at_utc: {utc_now().isoformat()}",
        f"- tweet_count: {len(rows)}",
        "",
        "This file is raw intake for PaiWork/Codex analysis. It preserves original text and URLs; classification, translation, thesis extraction, and claim updates happen in the skill workflow.",
        "",
    ]
    for index, row in enumerate(rows, 1):
        lines.extend(
            [
                f"## {index}. {row.get('created_at', '')}",
                "",
                f"- id: {row.get('id', '')}",
                f"- url: {row.get('url', '')}",
                f"- author: @{row.get('author_handle', handle.lstrip('@'))}",
                f"- engagement: reply={row.get('reply_label', '')} repost={row.get('repost_label', '')} like={row.get('like_label', '')}",
                "",
                "```text",
                str(row.get("text", "")).strip(),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_date(value: str | None) -> dt.date:
    if not value:
        return dt.date.today()
    return dt.date.fromisoformat(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch Serenity X posts through a PaiWork/CDP-compatible bridge.")
    parser.add_argument("--handle", default=DEFAULT_HANDLE, help="X handle without @.")
    parser.add_argument("--out-dir", default="tree/Serenity", help="Output Serenity workspace directory.")
    parser.add_argument("--proxy-url", default=DEFAULT_PROXY, help="CDP bridge URL.")
    parser.add_argument("--scrolls", type=int, default=4, help="Number of timeline scrolls.")
    parser.add_argument("--pause-s", type=float, default=1.5, help="Delay between extraction/scroll operations.")
    parser.add_argument("--date", help="Report date in YYYY-MM-DD. Defaults to local today.")
    parser.add_argument("--since-hours", type=int, default=24, help="Also include tweets newer than this UTC cutoff.")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing files.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = Path(args.out_dir)
    raw_dir = out_dir / "raw"
    daily_dir = out_dir / "daily"
    statuses_path = raw_dir / "serenity_statuses.jsonl"
    ids_path = raw_dir / "serenity_status_ids.txt"
    report_date = parse_date(args.date)

    try:
        fetched = collect_tweets(args.proxy_url, args.handle, args.scrolls, args.pause_s)
    except Exception as exc:
        print(f"[fetch_daily] ERROR: {exc}", file=sys.stderr)
        print(
            "[fetch_daily] Ensure PaiWork/front-end CDP bridge is running and Chrome is logged into X.",
            file=sys.stderr,
        )
        return 1

    existing = read_existing(statuses_path)
    for row in fetched:
        existing[row["id"]] = row
    all_rows = sorted(existing.values(), key=lambda item: item.get("created_at", ""), reverse=True)
    daily_rows = filter_daily(all_rows, report_date, args.since_hours)

    if args.dry_run:
        print(json.dumps({"fetched": len(fetched), "total": len(all_rows), "daily": len(daily_rows)}, ensure_ascii=False))
        return 0

    raw_dir.mkdir(parents=True, exist_ok=True)
    daily_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(statuses_path, all_rows)
    write_ids(ids_path, all_rows)
    daily_path = daily_dir / f"serenity_{report_date.isoformat()}.md"
    daily_path.write_text(render_daily(daily_rows, report_date, args.handle), encoding="utf-8", newline="\n")

    print(json.dumps({
        "fetched": len(fetched),
        "total": len(all_rows),
        "daily": len(daily_rows),
        "statuses_path": str(statuses_path),
        "daily_path": str(daily_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
