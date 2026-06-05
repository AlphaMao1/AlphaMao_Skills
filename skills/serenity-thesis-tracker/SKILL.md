---
name: serenity-thesis-tracker
description: "PaiWork-first Serenity (@aleabitoreddit) investment thesis tracking system. Use when working inside PaiWork to process Serenity/X tweets into structured investment theses, verifiable claims, supply-chain relationship maps, company research files, daily reports, weekly reviews, or research backlogs. Trigger on Serenity, aleabitoreddit, Serenity daily report, Serenity weekly review, thesis tracker, tweet research, supply-chain thesis tracking, ticker research updates, or PaiWork research monitoring. This version assumes PaiWork tools and data sources are available; a generic-agent version is planned later."
---

# Serenity Thesis Tracker

## Positioning

Use this skill to convert Serenity's X posts into a cumulative PaiWork research system:

- company files as the single source of truth
- supply-chain maps as the relationship navigation layer
- thesis and claim ledgers as verifiable research state
- daily and weekly reports as incremental change logs
- research backlog items as follow-up tasks

The core method is to reason backward from end demand to supply-chain bottlenecks, then turn each investable statement into a claim that can be tracked, verified, weakened, or closed.

This is not a generic summarizer. In this release, assume PaiWork is the runtime and that PaiWork-specific tools, analyst report generation, market data, Paipai search, and workspace conventions may be required.

## PaiWork Dependency Boundary

Treat this version as PaiWork-first.

- Use PaiWork workspace paths and PaiWork tool names when they exist.
- Prefer PaiWork `analyst_report` for polished daily, weekly, and company-file reports.
- Use PaiWork research/data tools for independent verification when available.
- Do not claim the skill is fully portable outside PaiWork.
- If running outside PaiWork, only the local file templates and `scripts/fetch_daily.py` are expected to work directly.

Do not add runtime package dependencies to this skill without an explicit user request. The bundled fetch script uses only Python standard-library modules and an existing PaiWork/CDP-compatible browser bridge.

## Expected Workspace Layout

```text
tree/Serenity/
├── raw/
│   ├── serenity_statuses.jsonl
│   └── serenity_status_ids.txt
├── daily/
│   └── serenity_YYYY-MM-DD.md
├── supply_chain_map/
│   ├── master_map.md
│   └── {theme}.md
├── companies/
│   └── {TICKER}.md
├── reports/
│   ├── YYYY-MM-DD_daily.md
│   └── YYYY-WNN_weekly.md
├── research_backlog.md
└── state/
    ├── thesis_registry.jsonl
    └── claim_ledger.jsonl
```

## Modes

### Daily Processing

Use for: "执行 Serenity 每日观点处理", "处理今天 Serenity 推文", "生成 Serenity 日报".

1. Ensure tweets have been fetched into `tree/Serenity/raw/` and `tree/Serenity/daily/`.
2. Read `daily/serenity_YYYY-MM-DD.md` first; fall back to filtering `raw/serenity_statuses.jsonl`.
3. Classify each post as `new_thesis`, `thesis_update`, `evidence_addition`, `catalyst`, `risk_warning`, `rebuttal`, `price_action_comment`, `noise`, or `meta`.
4. Ignore `noise` and `meta` except for a compact low-value list in the daily report.
5. Identify tickers, industry keywords, company-to-company relationships, and materiality.
6. Extract thesis only when the post contains a real causal chain.
7. Break each thesis into verifiable claims and relationships.
8. Update company files, supply-chain maps, research backlog, and the daily report.

Use `references/schemas.md` for thesis/claim fields and `references/templates.md` for file structures.

### Single-Ticker Update

Use for: "更新 SIVE 研究文件", "深挖 AAOI", "整理某 ticker 的 Serenity 观点".

1. Read the existing `companies/{TICKER}.md` if present.
2. Read relevant raw/daily tweet entries and related supply-chain maps.
3. Preserve history; append new thesis, claims, relationships, and timeline rows.
4. Mark what is Serenity's view, what is verified fact, and what is independent research.
5. Keep relationship details linked to the map rather than duplicated in the company file.

Use `references/company_one_pager_prompt.md` when generating or refreshing a full company file.

### Independent Verification

Use for: "验证 SIVE 客户关系", "查 XFAB 的 SiC 财务数据".

1. Start from `research_backlog.md` or unverified claims in the company file.
2. Use PaiWork financial, web, Paipai, and market-data tools when available.
3. Append findings to the company file's independent research section.
4. Update claim and relationship verification status.
5. Keep source URLs and evidence notes traceable.

### Weekly Review

Use for: "Serenity 本周复盘", "生成 Serenity 周报".

1. Read the week's daily reports, updated company files, supply-chain maps, and backlog.
2. Focus on relationship verification progress, thesis upgrades/downgrades, contradicted views, map changes, and tickers entering or leaving the formal research pool.
3. Generate `reports/YYYY-WNN_weekly.md`.

## Fetching Serenity Tweets

If tweets have not been fetched yet, run the bundled no-dependency script from the skill root:

```powershell
python scripts/fetch_daily.py --out-dir tree/Serenity --handle aleabitoreddit
```

The script expects an existing PaiWork/CDP-compatible browser bridge at `http://localhost:3456` with these endpoints: `/health`, `/new`, `/eval`, `/scroll`, and `/close`. It does not install packages, launch Chrome, or bypass login. Chrome/X login and browser automation belong to the PaiWork/front-end environment.

Outputs:

- `raw/serenity_statuses.jsonl`
- `raw/serenity_status_ids.txt`
- `daily/serenity_YYYY-MM-DD.md`

## Materiality Scoring

Score each research-relevant post from 5 to 15 across five dimensions:

| Dimension | 1 | 2 | 3 |
|---|---|---|---|
| View clarity | vague sentiment | direction without causal chain | explicit causal chain |
| Verifiability | pure opinion | partly verifiable | quantitatively verifiable |
| Scarcity | public information | industry insight | scarce supply-chain information |
| Time sensitivity | no window | quarterly window | near-term catalyst |
| Repetition | first mention | repeated mention | persistent focus |

Levels:

- `low` 5-7: daily report only
- `medium` 8-10: daily report plus company timeline
- `high` 11-13: update company thesis/claims/relationships
- `critical` 14-15: update company file, supply-chain map, and research backlog

## Non-Negotiables

- Do not duplicate the same information across files. Company files are the truth source; maps are the relationship layer; reports are incremental logs.
- Treat company-to-company relationships as first-class claims.
- Preserve original English tweet text and source URLs.
- Do not manufacture a thesis from sentiment-only posts.
- Keep verified facts, Serenity judgments, and independent research separate.
- Every thesis, claim, and relationship needs source URLs.
- Use incremental updates instead of rewriting history.

## References

- `references/schemas.md`: thesis, claim, and ticker schemas.
- `references/templates.md`: company file, supply-chain map, and daily report templates.
- `references/company_one_pager_prompt.md`: PaiWork analyst prompt for company files.
- `references/daily_report_prompt.md`: PaiWork analyst prompt for daily reports.
- `assets/sample-deep-research-report.md`: sample research report material for style/context inspection only.
