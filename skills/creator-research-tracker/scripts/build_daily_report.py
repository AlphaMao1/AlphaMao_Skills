#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from creator_tracker_lib import (
    COMPANY_ALIASES,
    assert_ingestible_collection,
    assert_qualified_x_row,
    compact_text,
    infer_action_and_importance,
    infer_topics,
    read_jsonl,
    require_registered_platform,
    stable_hash,
    utc_now,
    write_json,
)


CANONICAL_TICKERS = {
    "NVIDIA": "NVDA",
    "BROADCOM": "AVGO",
    "MICROSOFT": "MSFT",
    "GOOG": "GOOGL",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def materiality_score(text: str, topics: list[str]) -> tuple[int, str]:
    lower = text.lower()
    score = 5
    if any(word in lower for word in ["because", "therefore", "signal", "driven", "bottleneck", "supply", "demand", "power", "memory"]):
        score += 2
    if re.search(r"\$?[A-Z]{2,5}\b|\d+%|\$\d+|\d+\s*(billion|million|mw|gw)", text, re.I):
        score += 2
    if any(topic in topics for topic in ["data-center-power", "ai-infrastructure", "photonics-cpo", "ai-strategy", "nvidia", "sive", "broadcom", "amd"]):
        score += 2
    if any(word in lower for word in ["new", "first", "latest", "doubled", "short", "put", "call", "position", "stake"]):
        score += 1
    if "source-lead" in lower or "creator-original" in lower:
        score += 1
    score = max(5, min(score, 15))
    level = "critical" if score >= 14 else "high" if score >= 11 else "medium" if score >= 8 else "low"
    return score, level


def looks_like_800v_candidate_list(text: str) -> bool:
    lower = text.lower()
    cashtags = re.findall(r"\$[A-Z][A-Z0-9]{1,5}", text or "")
    return (
        "800v" in lower
        and any(word in lower for word in ["list", "crowd", "众包", "名单", "汇编", "compiled"])
        and (len(cashtags) >= 3 or "30+" in lower or "favorite" in lower)
    )


def content_type(text: str, action: str) -> str:
    lower = text.lower()
    if looks_like_800v_candidate_list(text):
        return "candidate_list"
    if any(word in lower for word in ["不是我的", "不是推荐", "not mine", "not recommendation", "困惑", "confused", "just a crowdsourced"]):
        return "clarification"
    if action == "archive-only":
        return "noise"
    if any(word in lower for word in ["short", "put", "bearish", "position", "portfolio", "13f"]):
        return "thesis_update"
    if any(word in lower for word in ["stake", "bought", "holding", "5%", "signal", "first"]):
        return "evidence_addition"
    if any(word in lower for word in ["list", "crowd", "众包", "名单"]):
        return "source_list"
    if action == "model-candidate":
        return "new_thesis"
    if action == "open-question":
        return "open_question"
    return "thesis_update"


def item_id(source_id: str, canonical_url: str, posted_at: str, text: str) -> str:
    return f"{source_id.upper()}-{stable_hash(canonical_url + posted_at + text[:160], 8)}"


def adjust_x_classification(summary: str, text: str, topics: list[str], action: str, importance: str) -> tuple[str, str, list[str]]:
    combined = summary + " " + text
    lower = combined.lower()
    adjusted_topics = list(dict.fromkeys(topics))
    if looks_like_800v_candidate_list(combined):
        for topic in ["data-center-power", "800v-dc-power-candidates"]:
            if topic not in adjusted_topics:
                adjusted_topics.append(topic)
        return "module-update", "P1", adjusted_topics
    if any(word in lower for word in ["不是我的", "不是推荐", "not mine", "not recommendation", "困惑", "confused", "just a crowdsourced"]):
        return "archive-only", "P2", adjusted_topics
    if "800v" in lower and any(word in lower for word in ["list", "crowd", "众包", "名单", "汇编"]):
        for topic in ["data-center-power", "800v-dc-power-candidates"]:
            if topic not in adjusted_topics:
                adjusted_topics.append(topic)
        return "module-update", "P1", adjusted_topics
    return action, importance, adjusted_topics


def extract_ticker_mentions(text: str) -> list[str]:
    found: set[str] = set()
    for token in re.findall(r"\$([A-Z][A-Z0-9]{1,5})", text or ""):
        found.add(f"${CANONICAL_TICKERS.get(token, token)}")
    for token in COMPANY_ALIASES:
        if token in {"ON"}:
            continue
        if re.search(rf"(?<![A-Za-z0-9$]){re.escape(token)}(?![A-Za-z0-9])", text or "", re.I):
            found.add(f"${CANONICAL_TICKERS.get(token, token)}")
    return sorted(found)


def display_topics(item: dict[str, Any]) -> list[str]:
    topics = list(item.get("topics") or [])
    if item.get("content_type") == "candidate_list":
        preferred = [topic for topic in ["800v-dc-power-candidates", "data-center-power"] if topic in topics]
        return preferred or ["800v-dc-power-candidates"]
    return topics


def ticker_counts(items: list[dict[str, Any]]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for item in items:
        for ticker in extract_ticker_mentions(" ".join([str(item.get("summary") or ""), str(item.get("source_text") or "")])):
            counts[ticker] = counts.get(ticker, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def evidence_quality_summary(gaps: list[str]) -> str:
    if not gaps:
        return "未记录明显抓取缺口。"
    joined = " ".join(gaps).lower()
    if "source-language" in joined and "page-ui-language" in joined:
        return "页面 UI 语言不是证据语言，但 raw evidence 已从 source-language status title/detail-expanded 捕获；正式链路未使用 UI 自动翻译文本。"
    if "no 2026-06-08 posts visible" in joined or "no-new-items" in joined:
        return "已通过注册 X 可见面检查，本日未发现可写入的新增原帖。"
    return "存在非致命抓取说明；正式写入仍以合格 raw evidence 为准。"


def verification_hint(item: dict[str, Any]) -> str:
    text = " ".join([str(item.get("summary") or ""), str(item.get("source_text") or "")]).lower()
    if "neocloud" in text or "spacex" in text:
        return "SpaceX/Google/Anthropic 原始协议、SEC/S-1/FWP、容量交付、收入确认和 90 天终止条款。"
    if "scaffolding" in text or "work iq" in text or "agent 365" in text:
        return "Microsoft 官方产品资料、Build/earnings call、Work IQ/Agent 365 文档、客户案例和 adoption/attach 指标。"
    if "msl" in text or "meta" in text or "zuck" in text:
        return "Meta IR、earnings call、CapEx 指引、MSL/Meta AI 产品指标和商业化/ROI 信号。"
    if "800v" in text:
        return "公司产品资料、客户/订单披露、800V DC 架构一手材料、数据中心电力设计资料。"
    if "13f" in text or re.search(r"\b(puts?|short|portfolio|position)\b", text):
        return "SEC 13F/13D/13G、期权披露、基金持仓原始文件；二手解读不能直接入模型。"
    return "一手来源、公司披露、监管文件、客户/订单证据或更强二手来源交叉验证。"


def normalize_x_rows(path: Path, source_id: str, display_name: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for row in read_jsonl(path):
        text = str(row.get("text") or "")
        assert_qualified_x_row(row, context=f"X row {path}")
        summary = str(row.get("summary") or compact_text(text, 160))
        topics = infer_topics(summary + " " + text)
        action, importance = infer_action_and_importance(summary + " " + text, topics)
        action, importance, topics = adjust_x_classification(summary, text, topics, action, importance)
        score, level = materiality_score(summary + " " + text, topics)
        items.append(
            {
                "item_id": item_id(source_id, str(row.get("canonical_url") or ""), str(row.get("posted_at") or ""), text),
                "source_id": source_id,
                "display_name": display_name,
                "platform": "x",
                "canonical_url": str(row.get("canonical_url") or "unknown"),
                "posted_at": str(row.get("posted_at") or "unknown"),
                "captured_at": str(row.get("captured_at") or utc_now()),
                "summary": summary,
                "topics": topics,
                "importance": importance,
                "action": action,
                "content_type": content_type(summary + " " + text, action),
                "materiality_score": score,
                "materiality_level": level,
                "source_status": str(row.get("source_status") or "creator-original-live-chrome"),
                "raw_ref": str(row.get("raw_ref") or str(path)),
                "excerpt": compact_text(text, 620),
                "source_text": text,
            }
        )
    return items


def youtube_summary(title: str, transcript: str) -> str:
    lower = (title + " " + transcript[:6000]).lower()
    if "short" in lower and "nvidia" in lower:
        return "YouTube 二手解读称某组合通过 SMH/NVIDIA 等 puts 或 short 暴露看空部分 AI 半导体 beta，同时多头线索转向数据中心、电力和内存等物理瓶颈；该说法必须回到 13F/期权披露核验，且不能自动视为被跟踪博主本人的更新。"
    if "situational awareness" in lower:
        return "视频围绕 AI situational awareness 论证，讨论 AGI、算力扩张、国家安全和 AI 产业化路径。"
    return f"YouTube 长内容补充：{title}"


def normalize_youtube_manifest(
    path: Path,
    source_id: str,
    display_name: str,
    *,
    source_status: str = "creator-original-youtube-transcript",
    force_archive: bool = False,
) -> list[dict[str, Any]]:
    data = load_json(path)
    items: list[dict[str, Any]] = []
    for idx, result in enumerate(data.get("results") or [], 1):
        url = str(result.get("url") or "")
        title = str(result.get("title") or url)
        text_paths = []
        for raw_path in result.get("text_paths") or []:
            candidate = Path(raw_path)
            if not candidate.is_absolute():
                candidate = path.parent / candidate
            text_paths.append(candidate)
        transcript = ""
        raw_ref = ""
        if text_paths:
            raw_ref = str(text_paths[0])
            transcript = text_paths[0].read_text(encoding="utf-8", errors="replace")
        summary = youtube_summary(title, transcript)
        topics = infer_topics(title + " " + transcript[:6000])
        action, importance = infer_action_and_importance(title + " " + transcript[:6000], topics)
        if "short" in (title + transcript[:2000]).lower():
            action, importance = "model-candidate", "P1"
        if force_archive:
            action, importance = "archive-only", "P2"
        score, level = materiality_score(title + " " + transcript[:6000], topics)
        items.append(
            {
                "item_id": item_id(source_id, url, str(result.get("upload_date") or ""), title),
                "source_id": source_id,
                "display_name": display_name,
                "platform": "youtube",
                "canonical_url": url,
                "posted_at": str(result.get("upload_date") or "unknown"),
                "captured_at": str(data.get("captured_at") or utc_now()),
                "summary": summary,
                "topics": topics,
                "importance": importance,
                "action": action,
                "content_type": content_type(title + " " + transcript[:6000], action),
                "materiality_score": score,
                "materiality_level": level,
                "source_status": source_status,
                "raw_ref": raw_ref or str(path),
                "excerpt": compact_text(transcript, 620),
                "source_text": transcript,
            }
        )
    return items


def load_collection_manifests(paths: list[Path]) -> tuple[list[str], list[str], list[str]]:
    statuses: list[str] = []
    gaps: list[str] = []
    raw_paths: list[str] = []
    for path in paths:
        data = load_json(path)
        if data:
            method = data.get("collection_method")
            status = data.get("collection_status")
            assert_ingestible_collection(
                status=str(status or ""),
                gaps=[str(x) for x in data.get("known_gaps", []) if x],
                context=str(path),
            )
            label = ":".join(str(x) for x in [data.get("platform", path.parent.parent.name), method, status] if x)
            statuses.append(label)
            gaps.extend(str(x) for x in data.get("known_gaps", []) if x)
            raw_paths.extend(str(x) for x in data.get("raw_paths", []) if x)
        raw_paths.append(str(path))
    return statuses, list(dict.fromkeys(gaps)), list(dict.fromkeys(raw_paths))


def render_report(
    *,
    source_id: str,
    display_name: str,
    report_date: str,
    items: list[dict[str, Any]],
    statuses: list[str],
    gaps: list[str],
    raw_paths: list[str],
) -> str:
    research_items = [x for x in items if x["importance"] != "noise" and x["action"] != "archive-only"]
    low_value = [x for x in items if x not in research_items]
    de_noise_items = [x for x in items if x.get("content_type") == "clarification" or x["action"] == "archive-only"]
    active_candidates = [x for x in research_items if x["action"] in {"company-update", "module-update", "model-candidate", "open-question"}]
    tickers = sorted({t for x in items for t in x.get("topics", []) if t not in {"creator-update", "company", "ai-infrastructure", "data-center-power", "ai-strategy", "photonics-cpo", "geopolitics"}})
    by_platform: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        by_platform.setdefault(item["platform"], []).append(item)
    for status in statuses:
        platform = status.split(":", 1)[0]
        if platform:
            by_platform.setdefault(platform, [])
    type_counts: dict[str, int] = {}
    for item in items:
        type_counts[item["content_type"]] = type_counts.get(item["content_type"], 0) + 1
    top_items = sorted(research_items or items, key=lambda x: (-x["materiality_score"], x["platform"]))
    ticker_rows = ticker_counts(items)

    lines = [
        f"# {display_name} 每日观点研究报告（{report_date}）",
        "",
        "## 执行摘要",
        "",
        f"{'本冷启动批次' if 'cold-start' in report_date else '过去24小时/本批次'}共处理 {len(items)} 条更新，其中有研究价值 {len(research_items)} 条、低价值/仅归档 {len(low_value)} 条；涉及 {', '.join(tickers) if tickers else '无明确 ticker，主要是观点系统跟踪'}。内容类型分布：{json.dumps(type_counts, ensure_ascii=False, sort_keys=True)}。",
        "",
        f"今日判断：{'有值得进入研究工作区的 source leads，但仍需验证后再改 Current Model。' if research_items else '今日没有新增可写入研究工作区的 source lead；若状态为 no-new-items，仅代表已注册平台的可见抓取面。'}",
        "",
        "## 今日综合判断",
        "",
        f"- 真正增量：{len(active_candidates)} 条。{'; '.join(x['summary'] for x in active_candidates[:3]) if active_candidates else '无。'}",
        f"- 去噪/澄清：{len(de_noise_items)} 条。{'; '.join(x['summary'] for x in de_noise_items[:3]) if de_noise_items else '无。'}",
        f"- 工作区动作：{'只写 source lead / module candidate，不改 Current Model。' if active_candidates else '不写 active research files。'}",
        f"- 证据质量：{evidence_quality_summary(gaps)}",
        "",
        "**最重要增量**：",
        "",
    ]
    if top_items:
        for idx, item in enumerate(top_items[:4], 1):
            lines.append(f"{idx}. {item['summary']}（{item['materiality_score']}/15，{item['content_type']}）。")
    else:
        lines.append("1. 无新增高优先级变化。")
    lines.extend(
        [
            "",
            "---",
            "",
            "## 覆盖与抓取状态",
            "",
            f"- 信息源覆盖：{', '.join(statuses) if statuses else '未提供 manifest'}",
            f"- known_gaps: {', '.join(gaps) if gaps else 'none'}",
            f"- raw_paths: {', '.join(raw_paths) if raw_paths else 'none'}",
            "",
            "| platform | 条目 | 状态说明 |",
            "| --- | ---: | --- |",
        ]
    )
    for platform, platform_items in sorted(by_platform.items()):
        status_text = "; ".join(s for s in statuses if s.startswith(platform)) or "ok"
        lines.append(f"| {platform} | {len(platform_items)} | {status_text} |")
    if not by_platform:
        lines.append("| none | 0 | no-new-items |")
    lines.extend(
        [
            "",
            "---",
            "",
            "## 今日核心变化",
            "",
        ]
    )
    if research_items:
        for idx, item in enumerate(top_items, 1):
            lines.extend(
                [
                    f"### {idx}) {item['summary']}",
                    "",
                    f"- Materiality：{item['materiality_score']}/15（{item['materiality_level']}）",
                    f"- 来源：{item['platform']} | {item['posted_at']} | [原文/视频]({item['canonical_url']})",
                    f"- 类型：{item['content_type']} | action: {item['action']} | importance: {item['importance']}",
                    f"- 新增变化：{item['summary']}",
                    f"- 研究含义：这是 source lead，不是已验证事实；应先作为 `{', '.join(display_topics(item) or ['creator-update'])}` 的候选线索处理。",
                    f"- 需要验证：{verification_hint(item)}",
                    f"- 下一步：{'写入 companies/modules/open-questions 的 source lead 后继续验证' if item['action'] in {'company-update', 'module-update', 'open-question', 'model-candidate'} else '仅归档观察'}。",
                    "",
                    f"**源材料摘录**：{item['excerpt']}",
                    "",
                ]
            )
    else:
        lines.append("今日没有新增高优先级变化。")
        lines.append("")

    lines.extend(["## 新增/变化的研究对象", "", "| 对象 | 来源 item | 类型 | 材料性 | 建议动作 |", "| --- | --- | --- | --- | --- |"])
    if research_items:
        for item in research_items:
            target = ", ".join(display_topics(item) or ["creator-update"])
            lines.append(f"| {target} | {item['item_id']} | {item['content_type']} | {item['materiality_score']}/15 {item['materiality_level']} | {item['action']} |")
    else:
        lines.append("| 无 | - | - | - | - |")

    lines.extend(["", "## 新增研究任务", ""])
    if research_items:
        for item in research_items:
            lines.append(f"- [ ] 验证 `{item['item_id']}`：{item['summary']}。验证路径：{verification_hint(item)} 验证前不改 Current Model。")
    else:
        lines.append("- [ ] 继续监控该来源，等待新内容。")

    lines.extend(["", "## 低价值内容", ""])
    if low_value:
        for item in low_value:
            lines.append(f"- {item['platform']} {item['posted_at']}：{item['summary']}（{item['content_type']}）")
    else:
        lines.append("- 无。")

    lines.extend(["", "## 最值得人工查看的原文链接", ""])
    for idx, item in enumerate(top_items[:6], 1):
        lines.append(f"{idx}. [{item['platform']} 原文]({item['canonical_url']}) - {item['summary']}；原因：materiality {item['materiality_score']}/15。")
    if not items:
        lines.append("无。")

    lines.extend(["", "## 已更新/建议写入工作区", ""])
    if research_items:
        for item in research_items:
            target = "companies/" if item["action"] == "company-update" else "open-questions.md" if item["action"] in {"open-question", "model-candidate"} else "modules/"
            lines.append(f"- `{target}`：{item['summary']}（{item['item_id']}）。")
    else:
        lines.append("- 无。")

    lines.extend(["", "---", "", "## 源更新摘要", ""])
    lines.extend([f"**日期**: {report_date} | **覆盖**: 本批次/过去24小时 | **总计**: {len(items)} 条", ""])
    lines.extend(["### 提及标的频次", ""])
    if ticker_rows:
        lines.extend(["| 标的 | 次数 |", "| --- | ---: |"])
        for ticker, count in ticker_rows:
            lines.append(f"| {ticker} | {count} |")
    else:
        lines.append("无明确 ticker。")
    lines.extend(["", "### 原始更新列表", ""])
    if items:
        for idx, item in enumerate(items, 1):
            mentions = sorted(set(extract_ticker_mentions(" ".join([item.get("summary", ""), item.get("source_text", "")]))))
            lines.extend(
                [
                    f"#### {idx}. {item['platform']} | {item['content_type']}",
                    "",
                    f"**标的**: {' '.join(mentions) if mentions else '无明确 ticker'}",
                    "",
                    item["summary"],
                    "",
                    f"[原文链接]({item['canonical_url']}) | raw_ref: {item.get('raw_ref') or 'none'}",
                    "",
                    f"> {compact_text(str(item.get('source_text') or item.get('excerpt') or ''), 1200)}",
                    "",
                    "---",
                    "",
                ]
            )
    else:
        lines.append("无。")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成对齐 PaiWork 日报标准的多平台博主每日研究报告。")
    parser.add_argument("--dossier", type=Path, required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--x-jsonl", type=Path, action="append", default=[])
    parser.add_argument("--youtube-manifest", type=Path, action="append", default=[])
    parser.add_argument("--allow-supporting-source", action="store_true", help="允许未注册平台作为 supporting source 进入日报；默认仅归档，不写 active。")
    parser.add_argument("--collection-manifest", type=Path, action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    items: list[dict[str, Any]] = []
    for path in args.x_jsonl:
        items.extend(normalize_x_rows(path, args.source_id, args.display_name))
    youtube_registered = True
    if args.youtube_manifest:
        youtube_registered = require_registered_platform(
            args.dossier, args.source_id, "youtube", allow_supporting_source=args.allow_supporting_source
        )
    for path in args.youtube_manifest:
        items.extend(
            normalize_youtube_manifest(
                path,
                args.source_id,
                args.display_name,
                source_status="creator-original-youtube-transcript" if youtube_registered else "supporting-secondary-transcript",
                force_archive=not youtube_registered,
            )
        )
    statuses, gaps, raw_paths = load_collection_manifests(args.collection_manifest)
    raw_paths.extend(str(path) for path in args.x_jsonl)
    raw_paths.extend(str(path) for path in args.youtube_manifest)
    raw_paths.extend(str(item["raw_ref"]) for item in items if item.get("raw_ref"))
    daily_dir = args.dossier / "archive" / "creator-daily" / args.source_id
    daily_dir.mkdir(parents=True, exist_ok=True)
    report_path = daily_dir / f"{args.date}.md"
    report = render_report(
        source_id=args.source_id,
        display_name=args.display_name,
        report_date=args.date,
        items=items,
        statuses=statuses,
        gaps=gaps,
        raw_paths=list(dict.fromkeys(raw_paths)),
    )
    report_path.write_text(report, encoding="utf-8", newline="\n")
    manifest = {
        "source_id": args.source_id,
        "date": args.date,
        "daily_report_path": str(report_path),
        "items": len(items),
        "platforms": sorted({item["platform"] for item in items}),
        "known_gaps": gaps,
        "raw_paths": list(dict.fromkeys(raw_paths)),
    }
    write_json(daily_dir / f"{args.date}-build-manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
