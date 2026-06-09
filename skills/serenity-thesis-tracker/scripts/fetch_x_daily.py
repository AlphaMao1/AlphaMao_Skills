#!/usr/bin/env python3
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

from creator_tracker_lib import read_jsonl, write_json, write_jsonl, x_row_qualification_reason


DEFAULT_PROXY = "http://localhost:3456"
STATUS_RE = re.compile(r"/status/(\d+)")

EXTRACT_POSTS_JS = r"""
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

EXPAND_ORIGINALS_JS = r"""
(() => {
  const labels = [
    /show original/i,
    /显示原文/,
    /show more/i,
    /显示更多/
  ];
  let clicked = 0;
  const candidates = Array.from(document.querySelectorAll('article[data-testid="tweet"] [role="button"], article[data-testid="tweet"] button, article[data-testid="tweet"] a'));
  for (const node of candidates) {
    const text = (node.innerText || node.textContent || "").trim();
    if (!text || !labels.some((rx) => rx.test(text))) continue;
    const clickable = node.closest('[role="button"],button,a') || node;
    try {
      clickable.click();
      clicked += 1;
    } catch {}
  }
  return JSON.stringify({ clicked });
})()
""".strip()


class FetchError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def parse_date(value: str | None) -> dt.date:
    return dt.date.fromisoformat(value) if value else dt.date.today()


def parse_iso(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except ValueError:
        return None


def request_json(proxy_url: str, path: str, *, method: str = "GET", body: str | None = None, timeout: int = 45) -> Any:
    url = proxy_url.rstrip("/") + path
    data = body.encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if body is not None:
        req.add_header("Content-Type", "text/plain; charset=utf-8")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise FetchError(f"browser bridge unavailable at {proxy_url}: {exc}") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FetchError(f"browser bridge returned non-JSON response for {path}: {raw[:300]}") from exc


def ensure_bridge(proxy_url: str) -> None:
    payload = request_json(proxy_url, "/health", timeout=10)
    if payload.get("status") != "ok":
        raise FetchError(f"browser bridge health check failed: {payload}")


def open_timeline(proxy_url: str, locator: str) -> str:
    path = "/new?url=" + urllib.parse.quote(locator, safe="")
    payload = request_json(proxy_url, path, timeout=60)
    target_id = payload.get("targetId")
    if not target_id:
        raise FetchError(f"browser bridge did not return targetId: {payload}")
    return str(target_id)


def eval_js(proxy_url: str, target_id: str, script: str) -> Any:
    path = "/eval?target=" + urllib.parse.quote(target_id, safe="")
    payload = request_json(proxy_url, path, method="POST", body=script, timeout=45)
    if "error" in payload:
        raise FetchError(f"post extraction failed: {payload['error']}")
    return payload.get("value", "[]")


def expand_originals(proxy_url: str, target_id: str) -> int:
    value = eval_js(proxy_url, target_id, EXPAND_ORIGINALS_JS)
    try:
        payload = json.loads(value) if isinstance(value, str) else value
    except json.JSONDecodeError:
        return 0
    return int(payload.get("clicked") or 0) if isinstance(payload, dict) else 0


def eval_posts(proxy_url: str, target_id: str) -> list[dict[str, Any]]:
    value = eval_js(proxy_url, target_id, EXTRACT_POSTS_JS)
    rows = json.loads(value) if isinstance(value, str) else value
    if not isinstance(rows, list):
        raise FetchError(f"post extraction returned unexpected value: {rows!r}")
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


def normalize_post(row: dict[str, Any], source_id: str, handle: str, captured_at: str) -> dict[str, Any] | None:
    url = str(row.get("url") or "")
    text = str(row.get("text") or "").strip()
    status_id = status_id_from_url(url)
    if not status_id or not text:
        return None
    return {
        "id": status_id,
        "source_id": source_id,
        "platform": "x",
        "canonical_url": url,
        "posted_at": str(row.get("created_at") or "unknown"),
        "captured_at": captured_at,
        "author_label": str(row.get("author_label") or "").strip(),
        "author_handle": str(row.get("author_handle") or "").strip() or handle.lstrip("@"),
        "text": text,
        "reply_label": str(row.get("reply_label") or "").strip(),
        "repost_label": str(row.get("repost_label") or "").strip(),
        "like_label": str(row.get("like_label") or "").strip(),
        "source_status": "creator-original",
    }


def collect_live(args: argparse.Namespace) -> list[dict[str, Any]]:
    ensure_bridge(args.proxy_url)
    handle = args.handle.lstrip("@")
    locator = args.locator or f"https://x.com/{handle}"
    target_id = open_timeline(args.proxy_url, locator)
    seen: dict[str, dict[str, Any]] = {}
    captured_at = utc_now()
    try:
        time.sleep(max(args.pause_s, 0.0))
        for index in range(args.scrolls + 1):
            if expand_originals(args.proxy_url, target_id):
                time.sleep(max(args.pause_s, 0.0))
            for row in eval_posts(args.proxy_url, target_id):
                normalized = normalize_post(row, args.source_id, handle, captured_at)
                if normalized:
                    seen[normalized["id"]] = normalized
            if index < args.scrolls:
                scroll(args.proxy_url, target_id)
                time.sleep(max(args.pause_s, 0.0))
    finally:
        close_target(args.proxy_url, target_id)
    return sorted(seen.values(), key=lambda item: item.get("posted_at", ""), reverse=True)


def separate_qualified_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    qualified: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for row in rows:
        reason = x_row_qualification_reason(row, context=f"fetched X row {row.get('canonical_url') or row.get('url') or ''}")
        if reason:
            copy = dict(row)
            copy["qualification_failure"] = reason
            rejected.append(copy)
        else:
            qualified.append(row)
    return qualified, rejected


def filter_daily(rows: list[dict[str, Any]], report_date: dt.date, since_hours: int) -> list[dict[str, Any]]:
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=since_hours)
    selected: list[dict[str, Any]] = []
    for row in rows:
        posted = parse_iso(str(row.get("posted_at") or ""))
        if posted is None:
            selected.append(row)
            continue
        if posted.date() == report_date or posted >= cutoff:
            selected.append(row)
    return sorted(selected, key=lambda item: item.get("posted_at", ""), reverse=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="通过本地 browser bridge 抓取 X/Twitter 每日更新。")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--handle", required=True)
    parser.add_argument("--display-name", default="")
    parser.add_argument("--locator", default="")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--proxy-url", default=DEFAULT_PROXY)
    parser.add_argument("--scrolls", type=int, default=4)
    parser.add_argument("--pause-s", type=float, default=1.5)
    parser.add_argument("--date")
    parser.add_argument("--since-hours", type=int, default=24)
    parser.add_argument("--fixture-jsonl", type=Path, help="使用 fixture/export JSONL，不连接 live browser bridge。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_date = parse_date(args.date)
    out_dir = args.output_dir / "x" / args.source_id
    daily_path = out_dir / f"{report_date.isoformat()}.jsonl"
    manifest_path = out_dir / f"{report_date.isoformat()}-manifest.json"

    try:
        if args.fixture_jsonl:
            raw_rows = read_jsonl(args.fixture_jsonl)
            for row in raw_rows:
                reason = x_row_qualification_reason(row, context=f"fixture X row {args.fixture_jsonl}")
                if reason:
                    raise FetchError(reason)
            rows = raw_rows
            rows = [
                normalize_post(
                    {
                        "url": row.get("canonical_url") or row.get("url"),
                        "created_at": row.get("posted_at") or row.get("created_at"),
                        "author_label": row.get("author_label", args.display_name),
                        "author_handle": row.get("author_handle", args.handle),
                        "text": row.get("text", ""),
                    },
                    args.source_id,
                    args.handle,
                    row.get("captured_at") or utc_now(),
                )
                for row in rows
            ]
            rows = [row for row in rows if row]
            collection_status = "ok"
            known_gaps: list[str] = ["fixture-mode"]
        else:
            rows = collect_live(args)
            collection_status = "ok" if rows else "no-new-items"
            known_gaps = []
    except Exception as exc:
        manifest = {
            "source_id": args.source_id,
            "platform": "x",
            "collection_status": "blocked",
            "error": str(exc),
            "known_gaps": ["browser-bridge-unavailable-or-login-required"],
        }
        write_json(manifest_path, manifest)
        print(json.dumps(manifest, ensure_ascii=False), file=sys.stderr)
        return 2

    daily_rows = filter_daily(rows, report_date, args.since_hours)
    daily_rows, rejected_rows = separate_qualified_rows(daily_rows)
    raw_paths = [str(daily_path)]
    if rejected_rows:
        rejected_path = out_dir / f"{report_date.isoformat()}-rejected-unqualified.jsonl"
        write_jsonl(rejected_path, rejected_rows)
        raw_paths.append(str(rejected_path))
        known_gaps.append(f"x-unqualified-items-excluded:{len(rejected_rows)}")
        if not daily_rows:
            collection_status = "blocked"
        elif collection_status == "ok":
            collection_status = "partial"
    write_jsonl(daily_path, daily_rows)
    manifest = {
        "source_id": args.source_id,
        "display_name": args.display_name or args.source_id,
        "platform": "x",
        "captured_at": utc_now(),
        "collection_status": collection_status,
        "known_gaps": known_gaps,
        "items_total": len(rows),
        "items_daily": len(daily_rows),
        "output_jsonl": str(daily_path),
        "raw_paths": raw_paths,
    }
    write_json(manifest_path, manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if collection_status == "blocked":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
