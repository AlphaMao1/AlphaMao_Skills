from __future__ import annotations

import hashlib
import json
import re
from urllib.parse import urlparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BUILTIN_SOURCE_PLATFORMS: dict[str, set[str]] = {
    "serenity": {"x"},
    "leopold": {"x", "website"},
    "rihardjarc": {"x", "newsletter"},
}

IMPORTANCE = {"P0", "P1", "P2", "noise"}
ACTIONS = {
    "archive-only",
    "open-question",
    "company-update",
    "module-update",
    "model-candidate",
    "current-model-update",
    "bridge-to-dossier",
}

FATAL_COLLECTION_STATUSES = {"blocked", "dependency-missing"}

FATAL_INGESTION_GAP_MARKERS = {
    "x-ui-auto-translated",
    "ui-auto-translated",
    "ui-translated",
    "original text was not expanded",
    "original-not-expanded",
    "raw-text-not-original",
    "summary-only",
    "search-snippet",
    "public-mirror",
    "cache-page",
    "unexpanded-text",
    "original-unavailable",
}

UNQUALIFIED_RAW_TEXT_MARKERS = {
    "翻译自",
    "显示原文",
    "Translated from",
    "Show original",
    "显示更多",
    "Show more",
}

BLOCKED_X_SOURCE_STATUS_MARKERS = {
    "secondary",
    "mirror",
    "public-mirror",
    "search-snippet",
    "summary-only",
    "cache",
    "cached",
    "translated-ui",
    "ui-translated",
    "missing-original",
}

ALLOWED_X_SOURCE_STATUS_PREFIXES = {
    "creator-original",
    "manual-copy",
    "user-export",
    "source-language",
    "api-adapter",
}

BLOCKED_X_URL_MARKERS = {
    "sotwe.com",
    "nitter.",
    "threadreaderapp.com",
    "webcache",
    "google.com/search",
    "bing.com",
    "duckduckgo.com",
    "archive.",
}

TOPIC_KEYWORDS = {
    "ai-infrastructure": ["ai infrastructure", "data center", "datacenter", "gpu", "accelerator", "h100", "b200"],
    "photonics-cpo": ["photonics", "cpo", "optical", "coherent", "aaoi", "lightmatter"],
    "data-center-power": ["power", "grid", "electricity", "cooling", "nuclear", "substation"],
    "ai-strategy": ["situational awareness", "agi", "scaling", "frontier", "lab", "national security"],
    "geopolitics": ["china", "export control", "national security", "compute governance", "policy"],
    "robotics": ["robotics", "humanoid", "optimus", "harmonic reduction", "planetary roller"],
    "company": ["nvda", "nvidia", "amd", "tsmc", "avgo", "broadcom", "msft", "meta", "googl", "goog", "aaoi", "sive"],
}

COMPANY_ALIASES = {
    "NVDA": "nvidia",
    "NVIDIA": "nvidia",
    "AMD": "amd",
    "TSMC": "tsmc",
    "AVGO": "broadcom",
    "BROADCOM": "broadcom",
    "MSFT": "microsoft",
    "MICROSOFT": "microsoft",
    "META": "meta",
    "GOOGL": "google",
    "GOOG": "google",
    "AAOI": "aaoi",
    "SIVE": "sive",
    "COHERENT": "coherent",
    "LEADERDRIVE": "leaderdrive",
    "688017": "leaderdrive",
    "SIVERS": "sive",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_hash(text: str, size: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:size]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def disqualifying_gap_reason(gap: str) -> str:
    lower = str(gap or "").lower()
    for marker in sorted(FATAL_INGESTION_GAP_MARKERS):
        if marker in lower:
            return f"不合格抓取缺口: {gap}"
    return ""


def unqualified_raw_text_reason(text: str) -> str:
    raw = str(text or "")
    for marker in sorted(UNQUALIFIED_RAW_TEXT_MARKERS, key=len, reverse=True):
        if marker in raw:
            return f"原始文本包含 UI 翻译/未展开标记: {marker}"
    return ""


def assert_qualified_raw_text(text: str, *, context: str) -> None:
    reason = unqualified_raw_text_reason(text)
    if reason:
        raise SystemExit(
            f"{context} 的 raw 文本不合格，拒绝进入正式日报/active route。{reason}。"
            "请先在 X 页面展开原文，或使用能返回 source-language full text 的 API/导出。"
        )


def x_row_qualification_reason(row: dict[str, Any], *, context: str = "X row") -> str:
    text = str(row.get("text") or "")
    reason = unqualified_raw_text_reason(text)
    if reason:
        return f"{context} 的 raw 文本不合格：{reason}"

    canonical_url = str(row.get("canonical_url") or row.get("url") or "").strip()
    parsed = urlparse(canonical_url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if any(marker in canonical_url.lower() for marker in BLOCKED_X_URL_MARKERS):
        return f"{context} 的 canonical_url 指向非 X 原帖来源：{canonical_url}"
    if not host.endswith(("x.com", "twitter.com")):
        return f"{context} 的 canonical_url 不是 X/Twitter 原帖：{canonical_url or 'missing'}"
    if "/status/" not in path:
        return f"{context} 的 canonical_url 不是具体 status：{canonical_url}"

    raw_ref = str(row.get("raw_ref") or "")
    raw_ref_lower = raw_ref.lower()
    if "creator-rejected" in raw_ref_lower or any(marker in raw_ref_lower for marker in BLOCKED_X_URL_MARKERS):
        return f"{context} 的 raw_ref 指向 rejected/镜像来源：{raw_ref}"

    source_status = str(row.get("source_status") or "creator-original").strip().lower()
    if any(marker in source_status for marker in BLOCKED_X_SOURCE_STATUS_MARKERS):
        return f"{context} 的 source_status 不合格：{source_status}"
    if not any(source_status.startswith(prefix) for prefix in ALLOWED_X_SOURCE_STATUS_PREFIXES):
        return f"{context} 的 source_status 不在允许列表：{source_status or 'missing'}"

    return ""


def assert_qualified_x_row(row: dict[str, Any], *, context: str = "X row") -> None:
    reason = x_row_qualification_reason(row, context=context)
    if reason:
        raise SystemExit(
            f"{reason}。拒绝进入正式日报/active route。"
            "X 材料必须来自 source-language X/Twitter 原帖、完整人工导出、Chrome 插件原文面或明确的 API adapter。"
        )


def assert_ingestible_collection(*, status: str = "", gaps: list[str] | None = None, context: str = "collection") -> None:
    normalized_status = str(status or "").strip().lower()
    if normalized_status in FATAL_COLLECTION_STATUSES:
        raise SystemExit(
            f"{context} 抓取状态为 {status}，拒绝生成正式日报/active route。"
            "这只能作为归档中的失败状态，不能伪装成无新增。"
        )
    for gap in gaps or []:
        reason = disqualifying_gap_reason(str(gap))
        if reason:
            raise SystemExit(
                f"{context} 存在不合格证据：{reason}。"
                "UI 翻译、搜索片段、公开镜像、summary-only 或未展开原文不得进入正式日报/active route。"
            )


def registered_platforms(dossier: Path, source_id: str) -> set[str]:
    source_id = source_id.lower()
    platforms = set(BUILTIN_SOURCE_PLATFORMS.get(source_id, set()))
    registry_path = dossier / "archive" / "creator-sources.json"
    data = load_json(registry_path)
    for source in data.get("sources") or []:
        if str(source.get("source_id") or "").lower() != source_id:
            continue
        for platform in source.get("platforms") or []:
            name = str(platform.get("platform") or "").strip().lower()
            if name:
                platforms.add(name)
    return platforms


def platform_is_registered(dossier: Path, source_id: str, platform: str) -> bool:
    return platform.lower() in registered_platforms(dossier, source_id)


def require_registered_platform(dossier: Path, source_id: str, platform: str, *, allow_supporting_source: bool = False) -> bool:
    if platform_is_registered(dossier, source_id, platform):
        return True
    if allow_supporting_source:
        return False
    allowed = ", ".join(sorted(registered_platforms(dossier, source_id))) or "none"
    raise SystemExit(
        f"{source_id} 未注册 {platform} 平台，拒绝把该材料纳入主日报/active route。"
        f"已注册平台：{allowed}。如这是用户显式给出的二手/supporting source，请加 --allow-supporting-source；"
        "该模式默认只归档，不写 active research files。"
    )


def slugify(value: str, fallback: str = "item") -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def compact_text(text: str, limit: int = 320) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def extract_tickers(text: str) -> list[str]:
    candidates = set(re.findall(r"\$?([A-Z]{2,5})(?=\b)", text or ""))
    tickers = []
    for token in sorted(candidates):
        if token in COMPANY_ALIASES:
            tickers.append(token)
    return tickers


def infer_topics(text: str) -> list[str]:
    lower = (text or "").lower()
    topics = []
    for topic, needles in TOPIC_KEYWORDS.items():
        if any(needle in lower for needle in needles):
            topics.append(topic)
    tickers = extract_tickers(text)
    for ticker in tickers:
        company = COMPANY_ALIASES.get(ticker)
        if company and company not in topics:
            topics.append(company)
    for alias, company in COMPANY_ALIASES.items():
        alias_pattern = rf"(?<![a-zA-Z0-9]){re.escape(alias.lower())}(?![a-zA-Z0-9])"
        if re.search(alias_pattern, lower, re.I) and company not in topics:
            topics.append(company)
    return topics or ["creator-update"]


def infer_action_and_importance(text: str, topics: list[str]) -> tuple[str, str]:
    lower = (text or "").lower()
    if not lower.strip() or len(lower.strip()) < 35:
        return "archive-only", "noise"
    if any(word in lower for word in ["contradict", "breaks thesis", "thesis change", "urgent", "wrong model"]):
        return "current-model-update", "P0"
    if any(word in lower for word in ["model", "estimate", "forecast", "sensitivity", "tam", "unit economics", "10x"]):
        return "model-candidate", "P1"
    if any(topic in COMPANY_ALIASES.values() for topic in topics) or "company" in topics:
        return "company-update", "P1"
    if "?" in text or any(word in lower for word in ["need to know", "watch", "verify", "check whether"]):
        return "open-question", "P1"
    if any(topic in topics for topic in ["ai-infrastructure", "photonics-cpo", "data-center-power", "ai-strategy", "geopolitics"]):
        return "module-update", "P1"
    if any(word in lower for word in ["lol", "meme", "gm ", "good morning"]):
        return "archive-only", "noise"
    return "archive-only", "P2"


def normalize_item(
    *,
    source_id: str,
    display_name: str,
    platform: str,
    canonical_url: str,
    posted_at: str,
    captured_at: str,
    text: str,
    raw_ref: str = "",
    title: str = "",
    source_status: str = "creator-original",
    index: int = 1,
) -> dict[str, Any]:
    basis = f"{canonical_url}-{posted_at}-{title}-{text[:160]}" if canonical_url else f"{source_id}-{platform}-{posted_at}-{title}-{text[:160]}"
    item_id = f"{source_id.upper()}-{stable_hash(basis, 8)}"
    topics = infer_topics(" ".join([title, text]))
    action, importance = infer_action_and_importance(" ".join([title, text]), topics)
    summary_source = title if title else text
    if not summary_source:
        summary_source = f"{display_name} {platform} update {index}"
    return {
        "item_id": item_id,
        "source_id": source_id,
        "display_name": display_name,
        "platform": platform,
        "canonical_url": canonical_url or "unknown",
        "posted_at": posted_at or "unknown",
        "captured_at": captured_at or utc_now(),
        "summary": compact_text(summary_source, 220),
        "topics": topics,
        "importance": importance,
        "action": action,
        "source_status": source_status,
        "raw_ref": raw_ref,
        "excerpt": compact_text(text, 420) if text else "",
    }


def render_daily_report(
    *,
    source_id: str,
    display_name: str,
    platform: str,
    report_date: str,
    captured_at: str,
    collection_status: str,
    known_gaps: list[str],
    raw_paths: list[str],
    items: list[dict[str, Any]],
) -> str:
    counts: dict[str, int] = {}
    action_counts: dict[str, int] = {}
    for item in items:
        counts[item["importance"]] = counts.get(item["importance"], 0) + 1
        action_counts[item["action"]] = action_counts.get(item["action"], 0) + 1
    raw_paths = list(dict.fromkeys(raw_paths))

    lines = [
        f"# {display_name} 博主每日报告 - {report_date}",
        "",
        "## 来源范围",
        f"- source_id: {source_id}",
        f"- platform: {platform}",
        f"- captured_at: {captured_at}",
        f"- collection_status: {collection_status}",
        f"- items: {len(items)}",
        f"- importance_counts: {json.dumps(counts, ensure_ascii=False, sort_keys=True)}",
        f"- action_counts: {json.dumps(action_counts, ensure_ascii=False, sort_keys=True)}",
        f"- raw_paths: {', '.join(raw_paths) if raw_paths else 'none'}",
        f"- known_gaps: {', '.join(known_gaps) if known_gaps else 'none'}",
        "",
        "## 今日条目",
        "",
        "| item_id | 时间 | 链接 | 主题 | 重要性 | 动作 | 摘要 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        link = item["canonical_url"]
        link_text = link if link == "unknown" else f"[link]({link})"
        topics = ", ".join(item.get("topics") or [])
        summary = str(item.get("summary") or "").replace("|", "\\|")
        lines.append(
            f"| {item['item_id']} | {item['posted_at']} | {link_text} | {topics} | {item['importance']} | {item['action']} | {summary} |"
        )
    if not items:
        lines.extend(["", "今日未抓取到符合本日报窗口的新条目。"])

    lines.extend(["", "## 证据草案", ""])
    for item in items:
        lines.extend(
            [
                f"### {item['item_id']}",
                f"- source_status: {item['source_status']}",
                f"- canonical_url: {item['canonical_url']}",
                f"- raw_ref: {item.get('raw_ref') or 'none'}",
                f"- proposed_source_tier: creator_source_lead",
                f"- research_tier_fallback: expert_interview",
                f"- write_policy: {'auto_blocked' if item['action'] == 'archive-only' else 'review_required'}",
                f"- verification_path: 写入模型前，需要一手来源、公司来源、监管来源或更强二手来源交叉验证",
                f"- excerpt: {item.get('excerpt') or 'none'}",
                "",
            ]
        )
    if not items:
        lines.append("无。")
        lines.append("")

    lines.extend(
        [
            "## 候选工作区动作",
            "",
            "| action | item | 目标提示 | 现在写入？ |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in items:
        write_now = "no" if item["action"] in {"archive-only", "bridge-to-dossier"} or item["importance"] == "noise" else "agent-review"
        target_hint = ", ".join(item.get("topics") or ["unknown"])
        lines.append(f"| {item['action']} | {item['item_id']} | {target_hint} | {write_now} |")

    return "\n".join(lines).rstrip() + "\n"
