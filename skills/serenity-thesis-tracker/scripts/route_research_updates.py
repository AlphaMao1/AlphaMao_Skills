#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_daily_report import normalize_x_rows, normalize_youtube_manifest
from creator_tracker_lib import require_registered_platform, write_json


COMPANY_REGISTRY: dict[str, dict[str, str]] = {
    "NVDA": {"slug": "nvidia", "name": "NVIDIA", "industry": "AI accelerators / AI infrastructure"},
    "NVIDIA": {"slug": "nvidia", "name": "NVIDIA", "industry": "AI accelerators / AI infrastructure"},
    "AMD": {"slug": "amd", "name": "AMD", "industry": "AI accelerators / CPUs"},
    "GOOGL": {"slug": "google", "name": "Alphabet / Google", "industry": "Hyperscale cloud / AI infrastructure / TPU"},
    "GOOG": {"slug": "google", "name": "Alphabet / Google", "industry": "Hyperscale cloud / AI infrastructure / TPU"},
    "GOOGLE": {"slug": "google", "name": "Alphabet / Google", "industry": "Hyperscale cloud / AI infrastructure / TPU"},
    "ALPHABET": {"slug": "google", "name": "Alphabet / Google", "industry": "Hyperscale cloud / AI infrastructure / TPU"},
    "META": {"slug": "meta", "name": "Meta Platforms", "industry": "Hyperscale AI infrastructure / social platforms"},
    "MSFT": {"slug": "microsoft", "name": "Microsoft", "industry": "Hyperscale cloud / enterprise AI"},
    "MICROSOFT": {"slug": "microsoft", "name": "Microsoft", "industry": "Hyperscale cloud / enterprise AI"},
    "AMZN": {"slug": "amazon", "name": "Amazon", "industry": "Hyperscale cloud / AWS / AI infrastructure"},
    "AMAZON": {"slug": "amazon", "name": "Amazon", "industry": "Hyperscale cloud / AWS / AI infrastructure"},
    "ORCL": {"slug": "oracle", "name": "Oracle", "industry": "AI cloud / data-center infrastructure"},
    "AVGO": {"slug": "broadcom", "name": "Broadcom", "industry": "AI ASIC / networking semiconductors"},
    "BROADCOM": {"slug": "broadcom", "name": "Broadcom", "industry": "AI ASIC / networking semiconductors"},
    "AAOI": {"slug": "aaoi", "name": "Applied Optoelectronics", "industry": "Optical transceivers / data-center interconnect"},
    "ORACLE": {"slug": "oracle", "name": "Oracle", "industry": "AI cloud / data-center infrastructure"},
    "MU": {"slug": "micron", "name": "Micron", "industry": "Memory / HBM / DRAM"},
    "MICRON": {"slug": "micron", "name": "Micron", "industry": "Memory / HBM / DRAM"},
    "ASML": {"slug": "asml", "name": "ASML", "industry": "Semiconductor equipment"},
    "INTC": {"slug": "intel", "name": "Intel", "industry": "Semiconductors / foundry"},
    "INTEL": {"slug": "intel", "name": "Intel", "industry": "Semiconductors / foundry"},
    "CORNING": {"slug": "corning", "name": "Corning", "industry": "Optical glass / materials"},
    "CRWV": {"slug": "coreweave", "name": "CoreWeave", "industry": "Neocloud / data centers"},
    "COREWEAVE": {"slug": "coreweave", "name": "CoreWeave", "industry": "Neocloud / data centers"},
    "SPACEX": {"slug": "spacex", "name": "SpaceX", "industry": "Private AI/cloud infrastructure candidate"},
    "XAI": {"slug": "xai", "name": "xAI", "industry": "Frontier AI lab / compute demand"},
    "SIVE": {"slug": "sive", "name": "Sivers Semiconductors", "industry": "Photonics / CPO / wireless"},
    "SIVERS": {"slug": "sive", "name": "Sivers Semiconductors", "industry": "Photonics / CPO / wireless"},
    "IFNNY": {"slug": "infineon", "name": "Infineon", "industry": "Power semiconductors"},
    "ON": {"slug": "onsemi", "name": "onsemi", "industry": "Power semiconductors"},
    "VICR": {"slug": "vicor", "name": "Vicor", "industry": "Power modules"},
    "LFUS": {"slug": "littelfuse", "name": "Littelfuse", "industry": "Power / circuit protection"},
    "VSH": {"slug": "vishay", "name": "Vishay", "industry": "Power / discretes"},
    "ENPH": {"slug": "enphase", "name": "Enphase", "industry": "Power electronics"},
    "NVTS": {"slug": "navitas", "name": "Navitas", "industry": "GaN power semiconductors"},
    "POWI": {"slug": "power-integrations", "name": "Power Integrations", "industry": "Power semiconductors / GaN"},
    "XFAB": {"slug": "xfab", "name": "X-FAB Silicon Foundries", "industry": "SiC / GaN specialty foundry"},
    "AOSL": {"slug": "alpha-omega-semiconductor", "name": "Alpha and Omega Semiconductor", "industry": "Power semiconductors"},
    "WOLF": {"slug": "wolfspeed", "name": "Wolfspeed", "industry": "SiC power semiconductors"},
    "300376": {"slug": "300376", "name": "300376", "industry": "China-listed 800V DC candidate"},
}

COMPANY_TICKERS: dict[str, str] = {
    "nvidia": "NVDA",
    "amd": "AMD",
    "google": "GOOGL",
    "meta": "META",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "broadcom": "AVGO",
    "aaoi": "AAOI",
    "oracle": "ORCL",
    "micron": "MU",
    "asml": "ASML",
    "intel": "INTC",
    "corning": "GLW",
    "coreweave": "CRWV",
    "spacex": "SpaceX",
    "xai": "xAI",
    "sive": "SIVE",
    "infineon": "IFNNY",
    "onsemi": "ON",
    "vicor": "VICR",
    "littelfuse": "LFUS",
    "vishay": "VSH",
    "enphase": "ENPH",
    "navitas": "NVTS",
    "power-integrations": "POWI",
    "xfab": "XFAB",
    "alpha-omega-semiconductor": "AOSL",
    "wolfspeed": "WOLF",
    "300376": "300376",
}

NAME_PATTERNS = {
    "NVIDIA": r"\bNVDA\b|\bNVIDIA\b",
    "AMD": r"\bAMD\b",
    "GOOGL": r"\bGOOGL\b|\bGOOG\b|\bGoogle\b|\bAlphabet\b",
    "META": r"\bMETA\b|\bMeta\b",
    "MSFT": r"\bMSFT\b|\bMicrosoft\b",
    "AMZN": r"\bAMZN\b|\bAmazon\b|\bAWS\b",
    "BROADCOM": r"\bAVGO\b|\bBroadcom\b",
    "AAOI": r"\bAAOI\b|\bApplied Optoelectronics\b",
    "ORACLE": r"\bORCL\b|\bOracle\b",
    "SPACEX": r"\bSpaceX\b",
    "XAI": r"\bxAI\b",
    "MICRON": r"\bMicron\b",
    "ASML": r"\bASML\b",
    "INTEL": r"\bIntel\b",
    "CORNING": r"\bCorning\b",
    "COREWEAVE": r"\bCoreWeave\b",
    "SIVERS": r"\bSivers?\b|\$SIVE\b",
    "NVTS": r"\bNVTS\b|\bNavitas\b",
    "POWI": r"\bPOWI\b|\bPower Integrations\b",
    "XFAB": r"\bXFAB\b|\bX-FAB\b",
    "AOSL": r"\bAOSL\b|\bAlpha and Omega Semiconductor\b",
}

CANDIDATE_LIST_COMPANY_SLUGS = {
    "navitas",
    "onsemi",
    "power-integrations",
    "xfab",
    "alpha-omega-semiconductor",
}

LEOPOLD_SHORT_SIDE_SLUGS = {
    "nvidia",
    "amd",
    "broadcom",
    "oracle",
    "asml",
    "intel",
    "corning",
}

LEOPOLD_LONG_SIDE_SLUGS = {
    "coreweave",
}

LEOPOLD_AMBIGUOUS_SIDE_SLUGS = {
    "micron",
}


def append_once(path: Path, block: str, marker: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker in existing:
        return False
    if existing and not existing.endswith("\n"):
        existing += "\n"
    path.write_text(existing + block.rstrip() + "\n", encoding="utf-8", newline="\n")
    return True


def append_question_once(path: Path, block: str, marker: str, question: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker in existing or f"## Q: {question}" in existing:
        return False
    if existing and not existing.endswith("\n"):
        existing += "\n"
    path.write_text(existing + block.rstrip() + "\n", encoding="utf-8", newline="\n")
    return True


def md_cell(value: str) -> str:
    return " ".join(str(value).replace("|", "\\|").split())


def append_table_row_once(path: Path, section: str, header: str, row: str, marker: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker in existing:
        return False
    if section not in existing:
        if existing and not existing.endswith("\n"):
            existing += "\n"
        existing += f"\n{section}\n\n{header}\n"
    if existing and not existing.endswith("\n"):
        existing += "\n"
    path.write_text(existing + row.rstrip() + "\n", encoding="utf-8", newline="\n")
    return True


def replace_or_append_section(path: Path, heading: str, body: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    section = f"{heading}\n\n{body.rstrip()}\n"
    pattern = re.compile(rf"^{re.escape(heading)}\n\n.*?(?=^## |\Z)", re.M | re.S)
    if pattern.search(existing):
        new_text = pattern.sub(lambda _match: section, existing)
    else:
        if existing and not existing.endswith("\n"):
            existing += "\n"
        new_text = existing + "\n" + section
    if new_text == existing:
        return False
    path.write_text(new_text, encoding="utf-8", newline="\n")
    return True


def replace_numbered_section(path: Path, heading: str, items: list[str]) -> bool:
    body = "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, 1))
    return replace_or_append_section(path, heading, body)


def append_source_index_row(dossier: Path, report_date: str, item: dict[str, Any], targets: list[str], daily_path: Path) -> str | None:
    path = dossier / "source-leads-index.md"
    marker = f"source-index:{item['item_id']}"
    header = (
        "| 日期 | 来源 | item | 类型 | action | target | source status | 证据边界 | 状态 | 日报 |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    )
    row = (
        f"| {report_date} | {md_cell(item['display_name'] + ' / ' + item['platform'])} | "
        f"[{item['item_id']}]({item['canonical_url']}) <!-- {marker} --> | "
        f"{md_cell(item['content_type'])} | {md_cell(item['action'])} | {md_cell(', '.join(targets) or 'archive-only')} | "
        f"{md_cell(item.get('source_status') or '')} | source lead, not fact | no model change | [{daily_path.name}]({daily_path}) |"
    )
    if append_table_row_once(path, "## Source Lead Index", header, row, marker):
        return str(path)
    return None


def company_page_template(company: dict[str, str], report_date: str) -> str:
    ticker = company.get("ticker") or COMPANY_TICKERS.get(company["slug"], company["name"])
    return (
        "---\n"
        "type: company\n"
        "status: source-lead-only\n"
        f"company: {company['name']}\n"
        f"ticker: {ticker}\n"
        f"created: {report_date}\n"
        f"updated: {report_date}\n"
        "source: serenity-thesis-tracker\n"
        "---\n\n"
        f"# {company['name']} ({ticker})\n\n"
        "## Company Card\n\n"
        "| field | current read |\n"
        "| --- | --- |\n"
        f"| 公司 | {company['name']} |\n"
        f"| 代码 | {ticker} |\n"
        f"| 所属研究模块 | {company['industry']} |\n"
        "| 当前状态 | source-lead-only / monitor |\n"
        "| 持仓状态 | 未确认 |\n"
        "| 核心问题 | 这家公司是否真实暴露于对应 creator source lead 指向的产业链机制？ |\n"
        "| 规范事实源 | 待一手资料验证后再指向 modules/models rows |\n\n"
        "## Why We Care\n\n"
        "该页由博主 source lead 自动生成，只说明它被提及或可能相关；不说明公司 thesis 已成立，也不构成交易建议。\n\n"
        "## What We Know\n\n"
        "| row_id | item | current value | source / row |\n"
        "| --- | --- | --- | --- |\n"
        f"| INIT-001 | 初始状态 | 仅由 {report_date} creator source lead 创建，尚未完成一手验证 | source-leads-index.md |\n\n"
        "## Current Valuation Snapshot\n\n"
        "> 未刷新行情；交易前必须重新获取价格、市值和估值口径。\n\n"
        "| row_id | metric | value | source status | note |\n"
        "| --- | --- | --- | --- | --- |\n\n"
        "## Current Judgment\n\n"
        "一句话判断：该公司已进入 creator lead 验证队列；研究重点是确认业务暴露、收入相关性、客户/订单证据和估值影响，而不是直接形成买入结论。\n\n"
        "## Core Hypotheses\n\n"
        "| hypothesis_id | hypothesis | current status | what would validate it | what would break it |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"| HYP-001 | {company['name']} 是否真实暴露于该 source lead 指向的机制 | source-lead-only | 一手披露、公司公告、监管文件或客户/订单证据 | 一手材料显示无相关产品/客户/收入暴露，或 source lead 关键事实被证伪 |\n\n"
        "## Entry Discipline\n\n"
        "不适用；当前未形成买入评估。\n\n"
        "## Monitoring Checklist\n\n"
        "| item | why it matters | frequency |\n"
        "| --- | --- | --- |\n"
        "| 一手披露/公司公告 | 验证 source lead 是否成立 | 事件驱动 |\n\n"
        "## Current Action\n\n"
        "| action | condition |\n"
        "| --- | --- |\n"
        "| monitor | 只在验证路径出现一手证据后升级为正式 company thesis |\n\n"
    )


def module_page_template(module: dict[str, str], report_date: str) -> str:
    return (
        "---\n"
        "type: module\n"
        "status: source-lead-ledger\n"
        f"module: {module['name']}\n"
        f"created: {report_date}\n"
        f"updated: {report_date}\n"
        "source: serenity-thesis-tracker\n"
        "---\n\n"
        f"# {module['name']}\n\n"
        "## 核心逻辑\n\n"
        "本模块把 creator daily item 转成可验证的行业研究对象：先识别机制、涉及公司/环节、可证伪证据和后续研究动作，再由 progressive research 流程决定是否升级为 Current Model。\n\n"
        "## 供应链层级与公司定位\n\n"
        "| 层级 | 公司/对象 | 当前定位 | 验证状态 |\n"
        "| --- | --- | --- | --- |\n"
        "| creator lead | 每日更新中出现的公司、产业环节或资本开支机制 | 已进入研究队列；需要补充一手披露、财报/电话会、客户/订单或产业链证据 | research-candidate |\n\n"
        "## 关键关系\n\n"
        "| 关系 | 内容 | 验证状态 | 来源 |\n"
        "| --- | --- | --- | --- |\n"
        "| creator item -> research object | 每条有效更新被拆成机制、对象、验证路径和下一步动作 | needs-verification | source-leads-index.md |\n\n"
        "## 瓶颈分析\n\n"
        "| 瓶颈 | 层级 | 关键公司 | 状态 |\n"
        "| --- | --- | --- | --- |\n"
        "| 待验证机制 | 由 source lead 指向 | 见下方博主 Source Leads | 需要一手/强二手验证 |\n\n"
        "## 待验证的关键问题\n\n"
        "- 哪些一手材料可以验证该机制已经影响收入、利润率、资本开支或竞争格局？\n"
        "- 若验证成立，应更新哪一条 company thesis、行业模块判断或估值假设？\n"
        "- 若验证失败，应把该 lead 降级为噪音、观察项还是反证材料？\n\n"
    )


def extract_companies(item: dict[str, Any]) -> list[dict[str, str]]:
    text = " ".join([str(item.get("summary") or ""), str(item.get("source_text") or ""), str(item.get("excerpt") or "")])
    keys: set[str] = set()
    for token in re.findall(r"\$([A-Z][A-Z0-9]{1,5})\b", text):
        if token in COMPANY_REGISTRY:
            keys.add(token)
    for token in re.findall(r"\b(300376)\b", text):
        keys.add(token)
    for key, pattern in NAME_PATTERNS.items():
        if re.search(pattern, text, re.I):
            keys.add(key)
    companies = []
    seen_slugs = set()
    for key in sorted(keys):
        company = COMPANY_REGISTRY[key]
        if company["slug"] not in seen_slugs:
            companies.append(company)
            seen_slugs.add(company["slug"])
    return companies


def industry_modules(item: dict[str, Any], companies: list[dict[str, str]]) -> list[dict[str, str]]:
    text = " ".join([str(item.get("summary") or ""), str(item.get("source_text") or "")]).lower()
    modules: list[dict[str, str]] = []
    if any(word in text for word in ["800v", "power", "电力", "memory"]):
        modules.append({"slug": "data-center-power-and-memory", "name": "数据中心电力与内存瓶颈"})
    semi_pattern = r"(?<![a-zA-Z0-9])(semiconductor|nvidia|amd|broadcom|asml|micron|intel|smh|tpu|gpu|asic|nvda|intc)(?![a-zA-Z0-9])"
    if re.search(semi_pattern, text, re.I):
        modules.append({"slug": "ai-semiconductor-positioning", "name": "AI 半导体链条仓位与拥挤度"})
    if any(word in text for word in ["hyperscaler", "cloud", "capex", "spacex", "xai", "oracle", "google", "meta", "microsoft", "aws", "scaffolding"]):
        modules.append({"slug": "hyperscaler-ai-infrastructure", "name": "Hyperscaler AI 基础设施与 CapEx"})
    if (
        any(word in text for word in ["photonics", "cpo", "silicon photonics", "optical"])
        or re.search(r"(?<![a-zA-Z0-9])sive(?![a-zA-Z0-9])", text, re.I)
    ):
        modules.append({"slug": "photonics-cpo", "name": "光子学 / CPO"})
    if any("Power" in company.get("industry", "") or "power" in company.get("industry", "").lower() for company in companies):
        modules.append({"slug": "800v-dc-power-candidates", "name": "800V DC 供电候选公司"})
    deduped = []
    seen = set()
    for module in modules:
        if module["slug"] not in seen:
            deduped.append(module)
            seen.add(module["slug"])
    return deduped or [{"slug": "creator-viewpoint-system", "name": "博主观点系统"}]


def normalize_route_action(item: dict[str, Any]) -> dict[str, Any]:
    item = dict(item)
    if item.get("action") == "current-model-update":
        item["action"] = "model-candidate"
        item["manual_review_required"] = True
    if item.get("source_status") in {"secondary-transcript", "supporting-secondary-transcript"}:
        item["action"] = "archive-only"
        item["importance"] = "P2"
        item["manual_review_required"] = True
    return item


def logic_for_item(item: dict[str, Any], company: dict[str, str] | None = None) -> str:
    text = " ".join([str(item.get("summary") or ""), str(item.get("source_text") or "")]).lower()
    name = company["name"] if company else "该主题"
    slug = company.get("slug") if company else ""
    if "neocloud" in text or "spacex" in text:
        return (
            "Rihard Jarc 将 SpaceX/xAI 相关计算租赁解读为 AI compute 供给侧的新信号："
            "SpaceX 可能从模型公司扩展为 neocloud，或在 IPO 前通过可取消租赁抬升收入。"
            "关键变量不是单纯收入数字，而是 90 天可取消条款、算力是否回流自用、以及这类 private AI infra 是否改变 hyperscaler/neocloud 竞争格局。"
        )
    if "scaffolding" in text or "agent 365" in text or "work iq" in text:
        return (
            "Rihard Jarc 的 MSFT 线索强调 AI 价值可能从基础模型层迁移到企业 scaffolding 层："
            "数据上下文、权限安全、token 成本可观测性和跨 SaaS 编排决定企业 AI 落地价值。"
            "研究含义是把 Microsoft 的 AI thesis 从单纯模型/算力暴露拆到 enterprise orchestration layer。"
        )
    if "msl" in text or "zuck" in text:
        return (
            "Rihard Jarc 对 Meta 继续加大 AI 支出保持审慎，核心不是否定 AI 投入，而是要求 Meta 先证明 MSL 或相关 AI 产品线的实质回报。"
            "该线索应归入 hyperscaler CapEx discipline：市场是否开始区分“有效 AI capex”和“情绪驱动 capex”。"
        )
    if re.search(r"\b(13f|short|puts?|bearish|position|portfolio)\b", text):
        if slug in LEOPOLD_LONG_SIDE_SLUGS:
            return (
                f"二手视频声称 Leopold 相关组合仍保留或强化 {name} 这类 neocloud / data-center 暴露。"
                "它不是“被做空”的对象，而是“芯片估值拥挤、瓶颈转向电力/数据中心/内存”这条轮动逻辑里的多头表达。"
                "关键含义是：若一手披露验证成立，研究应拆分为半导体 beta 降温与物理基础设施瓶颈受益两条线。"
            )
        if slug in LEOPOLD_AMBIGUOUS_SIDE_SLUGS:
            return (
                f"二手视频同时把 {name} 放进期权/对冲讨论，又把内存列为 Leopold 继续看重的物理瓶颈之一。"
                "因此它不能被简单归类为纯空头或纯多头，必须回到 13F/期权披露区分股票、put/call、名义敞口和实际方向。"
            )
        if slug in LEOPOLD_SHORT_SIDE_SLUGS:
            return (
                f"二手视频声称 Leopold 相关组合对 {name} 或其所在 AI 半导体链条出现 put/short/看跌敞口。"
                "逻辑含义不是否定 AI 长期需求，而是认为泛半导体 beta/估值可能过度拥挤，资金更值得转向电力、数据中心和内存等物理瓶颈。"
                "该说法必须先核验一手 13F/期权披露。"
            )
        return (
            "二手视频声称 Leopold 的组合从单边 AI 半导体 beta 转向双向表达：一边用 put/short 管理半导体拥挤交易，"
            "另一边保留或增加数据中心、电力和内存等物理瓶颈敞口。研究含义是先拆清头寸方向和标的归属，再判断是否更新模型。"
        )
    if "5%" in text and ("sive" in text or "sivers" in text):
        return (
            "Serenity 将 JPMorgan 持有 Sivers 超过 5% 解读为小流通盘首次出现大型机构买入信号；"
            "它支持的是 CPO/光子学供应链关注度上升这一 source lead，而不是已经验证的基本面结论。"
        )
    if "800v" in text or "300376" in text:
        if company is None:
            return (
                "Serenity 的 800V DC 相关讨论提供了一组候选公司清单。核心机制是：如果 AI 数据中心供电架构向 800V DC 迁移，"
                "功率半导体、功率模块、保护器件和相关电力电子公司可能成为后续筛选对象；但这仍是 source list，不是推荐，也不是已验证受益链。"
            )
        return (
            f"{name} 出现在 Serenity 800V DC 相关众包名单或讨论中。逻辑含义是：NVDA/AI 数据中心向 800V DC 供电架构迁移可能带来电力半导体、功率模块和保护器件候选公司清单；"
            "但这是 source list，不是推荐，也不是已验证受益链。"
        )
    return str(item.get("summary") or "待拆解 source lead")


def verification_for_item(item: dict[str, Any]) -> str:
    text = " ".join([str(item.get("summary") or ""), str(item.get("source_text") or "")]).lower()
    if "neocloud" in text or "spacex" in text:
        return "SpaceX/Google/Anthropic 相关原始协议或 S-1/招股文件、交易条款披露、客户/供应关系确认；重点验证 90 天可取消条款和收入确认边界。"
    if "scaffolding" in text or "agent 365" in text or "work iq" in text:
        return "Microsoft 官方产品资料、Build/earnings call、客户案例、Work IQ/Agent 365 文档，以及企业 AI 部署成本/可观测性数据。"
    if "msl" in text or "zuck" in text:
        return "Meta earnings call、CapEx 指引、MSL/Meta Superintelligence Labs 产品与收入指标、市场对 hyperscaler CapEx 的反应。"
    if re.search(r"\b(13f|short|puts?|bearish|position|portfolio)\b", text):
        return "SEC 13F/13D/13G、期权披露、基金持仓原始文件；节目二次解读不能直接入模型。"
    if "5%" in text and ("sive" in text or "sivers" in text):
        return "Sivers 股东名册、监管持股披露、JPMorgan 持仓变动原始文件。"
    if "800v" in text or "300376" in text:
        return "公司产品资料、客户/订单披露、800V DC 架构一手材料、数据中心电力设计资料。"
    return "一手来源或更强二手来源交叉验证。"


def route_item(dossier: Path, report_date: str, item: dict[str, Any], daily_path: Path) -> list[str]:
    changed: list[str] = []
    companies = extract_companies(item)
    modules = industry_modules(item, companies)
    verification = verification_for_item(item)
    marker = f"source-lead:{item['item_id']}"
    routed_targets: list[str] = []

    should_write_companies = item["action"] in {"company-update", "model-candidate"}
    if item.get("content_type") == "candidate_list":
        companies_to_write = [company for company in companies if company["slug"] in CANDIDATE_LIST_COMPANY_SLUGS]
    else:
        companies_to_write = companies if should_write_companies else []
    for company in companies_to_write:
        path = dossier / "companies" / f"{company['slug']}.md"
        if not path.exists():
            path.write_text(company_page_template(company, report_date), encoding="utf-8", newline="\n")
        row = (
            f"| {report_date} | {md_cell(item['display_name'] + ' / ' + item['platform'])} | "
            f"[{item['item_id']}]({item['canonical_url']}) <!-- {marker} company:{company['slug']} --> | "
            f"{md_cell(item['summary'])} | {md_cell(logic_for_item(item, company))} | "
            f"{md_cell(verification)} | 验证前只作为 source lead；若成立再更新 company thesis 或模块模型 |"
        )
        header = (
            "| 日期 | 来源 | item | claim | mechanism | 验证状态/路径 | 下一步 |\n"
            "| --- | --- | --- | --- | --- | --- | --- |"
        )
        if append_table_row_once(path, "## 博主 Source Leads", header, row, f"{marker} company:{company['slug']}"):
            changed.append(str(path))
            routed_targets.append(f"companies/{company['slug']}.md")

    for module in modules:
        path = dossier / "modules" / f"{module['slug']}.md"
        if not path.exists():
            path.write_text(module_page_template(module, report_date), encoding="utf-8", newline="\n")
        next_step = "形成模型候选并核验关键变量" if item["action"] == "model-candidate" else "归入模块线索池，等待一手验证"
        row = (
            f"| {report_date} | {md_cell(item['display_name'] + ' / ' + item['platform'])} | "
            f"[{item['item_id']}]({item['canonical_url']}) <!-- {marker} module:{module['slug']} --> | "
            f"{md_cell(', '.join(c['name'] for c in companies) if companies else '无明确公司')} | "
            f"{md_cell(logic_for_item(item))} | {md_cell(verification)} | {md_cell(next_step)} |"
        )
        header = (
            "| 日期 | 来源 | item | 涉及公司 | mechanism | 验证状态/路径 | 下一步 |\n"
            "| --- | --- | --- | --- | --- | --- | --- |"
        )
        if append_table_row_once(path, "## 博主 Source Leads", header, row, f"{marker} module:{module['slug']}"):
            changed.append(str(path))
            routed_targets.append(f"modules/{module['slug']}.md")

    needs_open_question = item["action"] in {"model-candidate", "open-question"} or item.get("content_type") == "candidate_list"
    if needs_open_question:
        path = dossier / "open-questions.md"
        question = "这个 source lead 是否足以改变当前研究模型？"
        item_text = " ".join([str(item.get("summary") or ""), str(item.get("source_text") or "")]).lower()
        if "13f" in verification.lower():
            question = "Leopold 相关组合变化是否真的代表 AI 半导体 beta 向电力/内存/数据中心瓶颈轮动？"
        elif "neocloud" in item_text or "spacex" in item_text:
            question = "SpaceX/xAI compute lease 是否代表可持续的 neocloud 供给侧变化？"
        elif "scaffolding" in item_text or "agent 365" in item_text or "work iq" in item_text:
            question = "MSFT enterprise AI scaffolding 是否足以改变 Microsoft AI thesis？"
        elif "800V" in logic_for_item(item):
            question = "800V DC 候选名单里哪些公司有真实数据中心供电暴露？"
        block = "\n".join(
            [
                f"\n## Q: {question}",
                f"<!-- {marker} open-question -->",
                "Priority: P1",
                f"Impact: {', '.join(m['name'] for m in modules)}",
                f"- [ ] c1: {verification}",
                f"- [ ] c2: 复核日报：{daily_path}",
                f"- [ ] c3: 若验证成立，再更新 companies/modules/current model；验证前不改 Current Model。",
            ]
        )
        if append_question_once(path, block, f"{marker} open-question", question):
            changed.append(str(path))
            routed_targets.append("open-questions.md")

    source_index = append_source_index_row(dossier, report_date, item, routed_targets, daily_path)
    if source_index:
        changed.append(source_index)

    return changed


def load_items(args: argparse.Namespace) -> list[dict[str, Any]]:
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
    return items


def update_recovery_surface(dossier: Path, report_date: str, changed: list[str], daily_report: Path) -> list[str]:
    extra: list[str] = []
    company_files = sorted(p for p in (dossier / "companies").glob("*.md") if p.name != ".gitkeep")
    module_files = sorted(p for p in (dossier / "modules").glob("*.md") if p.name != ".gitkeep")

    model_map = dossier / "model-map.md"
    if model_map.exists():
        modules_body = "\n".join(f"- `{p.relative_to(dossier).as_posix()}`" for p in module_files) or "- 本次 intake 未产生新的主题模块；先以 `source-leads-index.md` 作为恢复入口。"
        companies_body = "\n".join(f"- `{p.relative_to(dossier).as_posix()}`" for p in company_files) or "- 本次 intake 未达到公司页写入条件；公司对象仍可在相关模块页和 `source-leads-index.md` 中追踪。"
        source_index_line = "- `source-leads-index.md`：自动路由后的 active source lead 索引；只记录线索，不代表模型变化。"
        changed_any = False
        changed_any |= replace_or_append_section(model_map, "## Modules", modules_body)
        changed_any |= replace_or_append_section(model_map, "## Companies", companies_body)
        changed_any |= replace_or_append_section(model_map, "## Source Lead Index", source_index_line)
        if changed_any:
            extra.append(str(model_map))

    current = dossier / "current-synthesis.md"
    if current.exists():
        body = (
            f"- {report_date}: 已完成 creator daily intake 路由；日报为 `{daily_report}`。\n"
            "- 模型状态：no model change。当前写入均为 source leads / module candidates，验证前不得当作事实或 Current Model。\n"
            "- 接续入口：先读 `source-leads-index.md`、`model-map.md`，再进入相关 companies/modules。\n"
            "- 下一步：优先验证 open questions 中的 P1 条件；若一手证据成立，再由 progressive research agent 升级 thesis。"
        )
        if replace_or_append_section(current, "## Source Lead Intake Status", body):
            extra.append(str(current))
        conflict_body = (
            "- 已形成研究线索，但验证证据尚未闭环；不能把 creator lead 直接升级为事实判断。\n"
            "- 下一步冲突在于：哪些线索值得投入一手验证，哪些应停留在观察/归档层。"
        )
        if replace_or_append_section(current, "## 当前冲突", conflict_body):
            extra.append(str(current))
        next_steps = [
            "验证 `source-leads-index.md` 中 P1 source leads 的一手或更强二手来源。",
            "若验证成立，再更新对应 companies/modules 的 thesis、Claim Ledger 或 Current Judgment。",
            "验证前不要把博主观点写成 Current Model，也不要把 source lead 路由写入 update-log.md。",
        ]
        if replace_numbered_section(current, "## 下一步", next_steps):
            extra.append(str(current))

    context = dossier / "context.md"
    if context.exists():
        body = (
            "- `source-leads-index.md` 是 active source lead 索引，默认可读。\n"
            "- `archive/creator-daily/` 是给人看的日报归档；需要追溯来源时再读。\n"
            "- `archive/creator-parsed/` 是机器解析和路由 manifest，不是默认恢复入口。\n"
            "- 未验证博主观点不得直接更新 Current Model。"
        )
        if replace_or_append_section(context, "## Creator Tracker Recovery Surface", body):
            extra.append(str(context))

    return extra


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="把博主日报自动拆到 companies/modules/open-questions。")
    parser.add_argument("--dossier", type=Path, required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--daily-report", type=Path, required=True)
    parser.add_argument("--x-jsonl", type=Path, action="append", default=[])
    parser.add_argument("--youtube-manifest", type=Path, action="append", default=[])
    parser.add_argument("--allow-supporting-source", action="store_true", help="允许未注册平台作为 supporting source 进入 parsed archive；默认不写 active。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    items = load_items(args)
    parsed_dir = args.dossier / "archive" / "creator-parsed" / args.source_id
    parsed_dir.mkdir(parents=True, exist_ok=True)
    parsed_path = parsed_dir / f"{args.date}-parsed-items.json"
    parsed_payload = {
        "source_id": args.source_id,
        "date": args.date,
        "daily_report": str(args.daily_report),
        "items": items,
    }
    write_json(parsed_path, parsed_payload)

    changed: list[str] = []
    active_items = 0
    for item in items:
        item = normalize_route_action(item)
        if item["importance"] == "noise" or item["action"] == "archive-only":
            continue
        active_items += 1
        changed.extend(route_item(args.dossier, args.date, item, args.daily_report))

    if changed or active_items:
        changed.extend(update_recovery_surface(args.dossier, args.date, changed, args.daily_report))

    manifest = {
        "source_id": args.source_id,
        "date": args.date,
        "daily_report": str(args.daily_report),
        "parsed_items": str(parsed_path),
        "items": len(items),
        "changed_files": sorted(set(changed)),
        "model_change": False,
        "active_index": str(args.dossier / "source-leads-index.md") if active_items else "",
    }
    write_json(parsed_dir / f"{args.date}-route-manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
