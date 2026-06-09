#!/usr/bin/env python3
"""用 yt-dlp 抓取 YouTube 字幕/transcript。

脚本只负责收集 raw transcript 和 manifest。观点拆解和模型更新交给 agent workflow。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TIME_RE = re.compile(r"^\d{1,2}:\d{2}:\d{2}[,.]\d{3}\s+-->\s+\d{1,2}:\d{2}:\d{2}[,.]\d{3}")
TAG_RE = re.compile(r"<[^>]+>")


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(cmd, text=True, encoding="utf-8", errors="replace", capture_output=True)
    except FileNotFoundError as exc:
        raise SystemExit("PATH 中找不到 yt-dlp。请先安装或暴露 yt-dlp 后再运行。") from exc


def require_ytdlp() -> None:
    result = run(["yt-dlp", "--version"])
    if result.returncode != 0:
        raise SystemExit("PATH 中找不到 yt-dlp。请先安装或暴露 yt-dlp 后再运行。")


def read_urls_file(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def list_channel_videos(channel_url: str, max_videos: int, proxy: str | None) -> list[dict[str, Any]]:
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-single-json",
        "--playlist-end",
        str(max_videos),
        channel_url,
    ]
    if proxy:
        cmd[1:1] = ["--proxy", proxy]
    result = run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "Failed to list channel videos.")
    data = json.loads(result.stdout)
    entries = data.get("entries") or []
    videos = []
    for entry in entries[:max_videos]:
        video_id = entry.get("id") or entry.get("url")
        if not video_id:
            continue
        url = entry.get("url") or f"https://www.youtube.com/watch?v={video_id}"
        if not str(url).startswith("http"):
            url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append(
            {
                "id": video_id,
                "title": entry.get("title") or "",
                "url": url,
                "channel": data.get("channel") or data.get("uploader") or "",
            }
        )
    return videos


def subtitle_to_text(path: Path) -> str:
    lines: list[str] = []
    previous = ""
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.upper() == "WEBVTT":
            continue
        if line.isdigit():
            continue
        if TIME_RE.match(line):
            continue
        if line.startswith(("NOTE", "Kind:", "Language:")):
            continue
        line = TAG_RE.sub("", line)
        line = line.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        line = re.sub(r"\s+", " ", line).strip()
        if not line or line == previous:
            continue
        lines.append(line)
        previous = line
    return "\n".join(lines).strip() + "\n"


def fetch_one(url: str, raw_dir: Path, text_dir: Path, args: argparse.Namespace) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    meta_cmd = ["yt-dlp", "--skip-download", "--dump-single-json", url]
    if args.cookies_from_browser:
        meta_cmd[1:1] = ["--cookies-from-browser", args.cookies_from_browser]
    if args.proxy:
        meta_cmd[1:1] = ["--proxy", args.proxy]
    meta_result = run(meta_cmd)
    if meta_result.returncode == 0 and meta_result.stdout.strip():
        try:
            metadata = json.loads(meta_result.stdout)
        except json.JSONDecodeError:
            metadata = {}

    before = {p.resolve() for p in raw_dir.glob("*")}
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        args.lang,
        "--convert-subs",
        "srt",
        "-P",
        str(raw_dir),
        "-o",
        "%(id)s.%(ext)s",
        url,
    ]
    if args.cookies_from_browser:
        cmd[1:1] = ["--cookies-from-browser", args.cookies_from_browser]
    if args.proxy:
        cmd[1:1] = ["--proxy", args.proxy]
    result = run(cmd)
    after = {p.resolve() for p in raw_dir.glob("*")}
    new_files = [Path(p) for p in sorted(after - before)]
    subtitle_files = [p for p in new_files if p.suffix.lower() in {".srt", ".vtt"}]

    text_paths: list[str] = []
    for subtitle in subtitle_files:
        text = subtitle_to_text(subtitle)
        if not text.strip():
            continue
        out_path = text_dir / f"{subtitle.stem}.txt"
        out_path.write_text(text, encoding="utf-8")
        text_paths.append(str(out_path))

    if result.returncode == 0 and text_paths:
        collection_status = "ok"
    elif text_paths:
        collection_status = "partial"
    else:
        collection_status = "missing-transcript"

    return {
        "url": url,
        "title": metadata.get("title") or "",
        "upload_date": metadata.get("upload_date") or "",
        "channel": metadata.get("channel") or metadata.get("uploader") or "",
        "ok": result.returncode == 0 and bool(text_paths),
        "raw_subtitle_paths": [str(p) for p in subtitle_files],
        "text_paths": text_paths,
        "collection_status": collection_status,
        "stderr": result.stderr.strip()[-2000:],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="用 yt-dlp 抓取 YouTube 字幕/transcript。")
    parser.add_argument("--url", action="append", default=[], help="YouTube 视频 URL，可重复传入。")
    parser.add_argument("--urls-file", type=Path, help="UTF-8 文本文件，每行一个视频 URL。")
    parser.add_argument("--channel-url", help="YouTube channel 或 playlist URL。")
    parser.add_argument("--max-videos", type=int, default=3, help="从 --channel-url 抓取的视频数量上限。")
    parser.add_argument("--output-dir", type=Path, required=True, help="raw 字幕、文本和 manifest 输出目录。")
    parser.add_argument("--lang", default="en.*", help="yt-dlp 字幕语言选择器，如 en.*、zh-Hans。")
    parser.add_argument("--cookies-from-browser", help="给 yt-dlp 使用的浏览器 cookies，如 firefox 或 chrome。")
    parser.add_argument("--proxy", help="代理 URL，如 http://127.0.0.1:7890。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    require_ytdlp()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = args.output_dir / "raw"
    text_dir = args.output_dir / "text"
    raw_dir.mkdir(exist_ok=True)
    text_dir.mkdir(exist_ok=True)

    urls = list(args.url)
    if args.urls_file:
        urls.extend(read_urls_file(args.urls_file))

    channel_entries: list[dict[str, Any]] = []
    if args.channel_url:
        channel_entries = list_channel_videos(args.channel_url, args.max_videos, args.proxy)
        urls.extend(entry["url"] for entry in channel_entries)

    seen: set[str] = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            unique_urls.append(url)
            seen.add(url)

    results = [fetch_one(url, raw_dir, text_dir, args) for url in unique_urls]
    manifest = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "lang": args.lang,
        "channel_entries": channel_entries,
        "results": results,
    }
    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "fetched": len(results), "ok": sum(1 for r in results if r["ok"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
