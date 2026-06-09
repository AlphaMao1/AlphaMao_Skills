#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def collection_method_for(platform: str) -> str:
    return {
        "x": "chrome-plugin-first",
        "youtube": "yt-dlp",
        "website": "manual-or-web",
        "manual": "manual-or-web",
        "newsletter": "manual-or-web",
        "podcast": "podcast-feed-or-manual",
    }.get(platform, "manual-or-web")


def scaffold(args: argparse.Namespace) -> dict[str, object]:
    dossier = args.dossier.resolve()
    title = args.title or f"{args.display_name} 博主观点跟踪"
    today = date.today().isoformat()
    created: list[str] = []

    context = f"""# {title} 接续说明

这个 dossier 跟踪 {args.display_name} 的公开观点系统，目标是把博主更新转成研究输入，而不是把博主观点当事实。

默认恢复面：
- context.md
- current-synthesis.md
- model-map.md
- source-leads-index.md
- open-questions.md
- update-log.md
- modules/
- companies/

`source-leads-index.md` 是 active source lead 索引。每日报告在 `archive/creator-daily/{args.source_id}/`，主要给人查看和审计。除非追溯来源，agent 默认不要读 archive。

写入规则：
- 博主材料是 `creator_source_lead`，兼容映射到 `expert_interview`。
- 博主观点不能直接更新 Current Model。
- 只有有研究价值且有 verification path 的 item 才写 active research files。
"""
    current = f"""# Current Model

## 一句话判断

这个 dossier 已创建，但尚未形成稳定研究判断。

## 已知

- 跟踪来源：{args.display_name}
- 观点范围：{args.viewpoint_scope or '首次 intake 后再细化'}

## 未知

- 哪些博主 claim 能通过一手或更强二手来源验证。
- 哪些模块或公司值得持续跟踪。

## 当前冲突

- 冷启动阶段的主要冲突是：博主观点可能提供研究线索，但尚未被一手材料或更强二手材料验证。
- 第一次 daily intake 后，需要把可研究 item 拆成公司、行业模块、验证路径和 open questions。

## 最近变化

- {today}: 创建 dossier 骨架。

## 下一步

1. 跑第一次 daily intake。
2. 把 item 分成 P0/P1/P2/noise。
3. 只把有价值的 source lead 写入 source-leads-index、open questions、modules 或 companies。
"""
    model_map = f"""# Model Map

## 范围

跟踪 {args.display_name} 的公开更新，把它们作为研究线索，而不是已验证事实或投资建议。

## 分析轴

- 博主观点系统变化
- 需要验证的 claim
- 公司相关 source leads
- 主题模块 source leads
- 模型补丁候选

## Modules

- `modules/creator-viewpoint-system.md`

## Companies

重复出现的公司线索写入 `companies/<slug>.md`。

## Source Lead Index

- `source-leads-index.md`

## Related Dossiers

- 复核后在这里记录 bridge candidates。
"""
    open_questions = """# Open Questions

> 只记录从具体 source lead 拆出来、且需要继续验证后才可能改变研究模型的问题。不要放泛化占位问题。
"""
    update_log = """# Model Change Log

| 日期 | 类型 | 变化 | 影响 | 来源 |
| --- | --- | --- | --- | --- |
"""
    source_leads_index = """# Source Leads Index

该文件是 active 恢复面，用于索引已从博主日报拆出的 source leads。它不是事实源，也不是模型变化日志。

## Source Lead Index

| 日期 | 来源 | item | 类型 | action | target | source status | 证据边界 | 状态 | 日报 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
"""
    module = f"""# 博主观点系统

## 用途

跟踪 {args.display_name} 公开论证系统中的稳定模式。

## 博主 Source Leads

| 日期 | 来源 | item | mechanism | 模型相关性 | 下一步 |
| --- | --- | --- | --- | --- | --- |
"""

    files = {
        dossier / "context.md": context,
        dossier / "current-synthesis.md": current,
        dossier / "model-map.md": model_map,
        dossier / "source-leads-index.md": source_leads_index,
        dossier / "open-questions.md": open_questions,
        dossier / "update-log.md": update_log,
        dossier / "modules" / "creator-viewpoint-system.md": module,
        dossier / "companies" / ".gitkeep": "",
        dossier / "archive" / "creator-daily" / args.source_id / ".gitkeep": "",
        dossier / "archive" / "creator-raw" / args.platform / args.source_id / ".gitkeep": "",
    }
    for path, content in files.items():
        if write_if_missing(path, content):
            created.append(str(path))

    registry_path = dossier / "archive" / "creator-sources.json"
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    else:
        registry = {"sources": []}
    if not any(src.get("source_id") == args.source_id for src in registry.get("sources", [])):
        registry.setdefault("sources", []).append(
            {
                "source_id": args.source_id,
                "display_name": args.display_name,
                "viewpoint_scope": args.viewpoint_scope,
                "platforms": [
                    {
                        "platform": args.platform,
                        "locator": args.locator,
                        "handle_or_channel": args.handle_or_channel,
                        "collection_method": collection_method_for(args.platform),
                    }
                ],
                "source_tier": "creator_source_lead",
                "research_tier_fallback": "expert_interview",
                "raw_material_policy": "links-plus-structured-summary",
                "caution_labels": ["source-lead-not-fact", "requires-primary-check", "not-investment-advice"],
            }
        )
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created.append(str(registry_path))

    return {"dossier": str(dossier), "created": created, "created_count": len(created)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按 progressive research active surface 创建博主跟踪 dossier。")
    parser.add_argument("dossier", type=Path)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--title")
    parser.add_argument("--viewpoint-scope", default="")
    parser.add_argument("--platform", choices=["x", "youtube", "website", "podcast", "newsletter", "manual"], default="x")
    parser.add_argument("--locator", default="")
    parser.add_argument("--handle-or-channel", default="")
    return parser.parse_args()


def main() -> int:
    result = scaffold(parse_args())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
