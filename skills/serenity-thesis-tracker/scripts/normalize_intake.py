#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from creator_tracker_lib import (
    COMPANY_ALIASES,
    assert_ingestible_collection,
    assert_qualified_x_row,
    normalize_item,
    read_jsonl,
    render_daily_report,
    require_registered_platform,
    utc_now,
    write_json,
)


def load_x_items(path: Path, args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[str], list[str], str]:
    rows = read_jsonl(path)
    items = []
    for index, row in enumerate(rows, 1):
        items.append(
            normalize_item(
                source_id=args.source_id,
                display_name=args.display_name or args.source_id,
                platform="x",
                canonical_url=str(row.get("canonical_url") or row.get("url") or ""),
                posted_at=str(row.get("posted_at") or row.get("created_at") or "unknown"),
                captured_at=str(row.get("captured_at") or utc_now()),
                text=str(row.get("text") or ""),
                raw_ref=str(row.get("raw_ref") or ""),
                source_status=str(row.get("source_status") or "creator-original"),
                title=str(row.get("summary") or ""),
                index=index,
            )
        )
    gaps: list[str] = []
    status = "ok" if items else "no-new-items"
    raw_paths = [str(path)]
    if args.collection_manifest and args.collection_manifest.exists():
        manifest = json.loads(args.collection_manifest.read_text(encoding="utf-8"))
        gaps = list(manifest.get("known_gaps") or [])
        status = str(manifest.get("collection_status") or status)
        assert_ingestible_collection(status=status, gaps=[str(x) for x in gaps], context=str(args.collection_manifest))
        raw_paths.extend(str(p) for p in manifest.get("raw_paths", []) if p)
        raw_paths.append(str(args.collection_manifest))
    for row in rows:
        assert_qualified_x_row(row, context=f"X row {path}")
    return items, raw_paths, gaps, status


def load_youtube_manifest(path: Path, args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[str], list[str], str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries_by_url = {entry.get("url"): entry for entry in data.get("channel_entries") or []}
    items = []
    raw_paths = [str(path)]
    gaps = []
    for index, result in enumerate(data.get("results") or [], 1):
        url = str(result.get("url") or "")
        entry = entries_by_url.get(url, {})
        text_paths = []
        for raw_path in result.get("text_paths") or []:
            candidate = Path(raw_path)
            if not candidate.is_absolute():
                candidate = path.parent / candidate
            text_paths.append(candidate)
        text = ""
        raw_ref = ""
        if text_paths:
            raw_ref = str(text_paths[0])
            raw_paths.append(raw_ref)
            text = text_paths[0].read_text(encoding="utf-8", errors="replace")
        else:
            gaps.append(f"missing-transcript:{url}")
        if result.get("collection_status") and result.get("collection_status") != "ok":
            gaps.append(f"{result.get('collection_status')}:{url}")
        if result.get("stderr"):
            stderr = str(result.get("stderr"))
            if "429" in stderr or "Too Many Requests" in stderr:
                gaps.append(f"rate-limited-subtitle-fetch:{url}")
        title = str(entry.get("title") or result.get("title") or url)
        items.append(
            normalize_item(
                source_id=args.source_id,
                display_name=args.display_name or args.source_id,
                platform="youtube",
                canonical_url=url,
                posted_at=str(entry.get("timestamp") or entry.get("upload_date") or "unknown"),
                captured_at=str(data.get("captured_at") or utc_now()),
                text=text,
                raw_ref=raw_ref,
                title=title,
                source_status="secondary-transcript" if text else "missing-transcript",
                index=index,
            )
        )
    status = "partial" if gaps and items else "ok" if items else "no-new-items"
    return items, raw_paths, gaps, status


def apply_research_actions(dossier: Path, report_date: str, items: list[dict[str, Any]], daily_path: Path) -> list[str]:
    changed: list[str] = []
    oq_path = dossier / "open-questions.md"
    if not oq_path.exists():
        return changed

    questions = []
    for item in items:
        if item["importance"] == "noise" or item["action"] == "archive-only":
            continue
        if item["action"] in {"open-question", "model-candidate", "bridge-to-dossier"}:
            questions.append(
                "\n".join(
                    [
                        f"## Q: Verify creator source lead {item['item_id']}",
                        f"Priority: {item['importance']}",
                        f"Impact: {', '.join(item.get('topics') or [])}",
                        f"- [ ] c1: 用一手来源或更强二手来源验证该 claim (source-lead: {item['source_id']} {item['item_id']})",
                        f"- [ ] c2: 复核每日报告：{daily_path}",
                        "",
                    ]
                )
            )
    if questions:
        with oq_path.open("a", encoding="utf-8", newline="\n") as f:
            f.write("\n" + "\n".join(questions))
        changed.append(str(oq_path))

    known_companies = set(COMPANY_ALIASES.values())
    company_items = [item for item in items if item["action"] == "company-update" and item["importance"] != "noise"]
    for item in company_items:
        target = next((topic for topic in item.get("topics") or [] if topic in known_companies), "")
        if not target:
            continue
        path = dossier / "companies" / f"{target}.md"
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "# 公司 Source Leads\n\n## 博主 Source Leads\n\n| 日期 | 来源 | item | claim | 验证状态 | 下一步 |\n| --- | --- | --- | --- | --- | --- |\n",
                encoding="utf-8",
                newline="\n",
            )
        with path.open("a", encoding="utf-8", newline="\n") as f:
            summary = str(item["summary"]).replace("|", "\\|")
            f.write(f"| {report_date} | {item['source_id']} | {item['item_id']} | {summary} | source-lead | 一手/更强二手来源验证 |\n")
        changed.append(str(path))

    module_items = [
        item
        for item in items
        if item["importance"] != "noise"
        and (
            item["action"] == "module-update"
            or (item["action"] == "company-update" and not any(topic in known_companies for topic in item.get("topics") or []))
        )
    ]
    for item in module_items:
        target = next((topic for topic in item.get("topics") or [] if topic != "creator-update"), "creator-viewpoint-system")
        path = dossier / "modules" / f"{target}.md"
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"# {target}\n\n## 博主 Source Leads\n\n| 日期 | 来源 | item | mechanism | 模型相关性 | 下一步 |\n| --- | --- | --- | --- | --- | --- |\n",
                encoding="utf-8",
                newline="\n",
            )
        with path.open("a", encoding="utf-8", newline="\n") as f:
            summary = str(item["summary"]).replace("|", "\\|")
            f.write(f"| {report_date} | {item['source_id']} | {item['item_id']} | {summary} | source-lead | 一手/更强二手来源验证 |\n")
        changed.append(str(path))

    if changed:
        log_path = dossier / "update-log.md"
        if log_path.exists():
            with log_path.open("a", encoding="utf-8", newline="\n") as f:
                f.write(f"| {report_date} | source-lead-routing | 博主日报产生候选写入 | 通过写入门禁后更新 active files | {daily_path} |\n")
            changed.append(str(log_path))
    return sorted(set(changed))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="把博主 intake 归一成每日报告，并可生成研究写入草案。")
    parser.add_argument("--dossier", type=Path, required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--display-name", default="")
    parser.add_argument("--platform", choices=["x", "youtube"], required=True)
    parser.add_argument("--input-jsonl", type=Path)
    parser.add_argument("--collection-manifest", type=Path)
    parser.add_argument("--youtube-manifest", type=Path)
    parser.add_argument("--date", required=True)
    parser.add_argument("--allow-supporting-source", action="store_true", help="允许未注册平台作为 supporting source 调试归一化；输出仍只写 debug 路径。")
    parser.add_argument("--apply-research-actions", action="store_true", help="为非归档 item 追加 source-lead 写入草案。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.apply_research_actions:
        raise SystemExit(
            "--apply-research-actions 已废弃：normalize_intake 只能生成单平台归一化日报/调试产物；"
            "active 写入必须走 build_daily_report.py -> route_research_updates.py。"
        )
    if args.platform == "x":
        if not args.input_jsonl:
            if not args.collection_manifest:
                raise SystemExit("--input-jsonl or --collection-manifest is required for --platform x")
            empty_path = args.collection_manifest.with_suffix(".empty.jsonl")
            if not empty_path.exists():
                empty_path.write_text("", encoding="utf-8")
            args.input_jsonl = empty_path
        items, raw_paths, gaps, status = load_x_items(args.input_jsonl, args)
    else:
        if not args.youtube_manifest:
            raise SystemExit("--youtube-manifest is required for --platform youtube")
        require_registered_platform(args.dossier, args.source_id, "youtube", allow_supporting_source=args.allow_supporting_source)
        items, raw_paths, gaps, status = load_youtube_manifest(args.youtube_manifest, args)

    display_name = args.display_name or args.source_id
    captured_at = utc_now()
    daily_dir = args.dossier / "archive" / "creator-normalized-debug" / args.source_id / args.platform
    daily_path = daily_dir / f"{args.date}.md"
    daily_dir.mkdir(parents=True, exist_ok=True)
    report = render_daily_report(
        source_id=args.source_id,
        display_name=display_name,
        platform=args.platform,
        report_date=args.date,
        captured_at=captured_at,
        collection_status=status,
        known_gaps=gaps,
        raw_paths=raw_paths,
        items=items,
    )
    daily_path.write_text(report, encoding="utf-8", newline="\n")

    changed_files = apply_research_actions(args.dossier, args.date, items, daily_path) if args.apply_research_actions else []
    manifest = {
        "source_id": args.source_id,
        "platform": args.platform,
        "date": args.date,
        "daily_report_path": str(daily_path),
        "items": len(items),
        "collection_status": status,
        "known_gaps": gaps,
        "changed_files": changed_files,
    }
    manifest_path = daily_dir / f"{args.date}-normalize-manifest.json"
    write_json(manifest_path, manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
