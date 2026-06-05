# Data Acquisition Layer

数据获取层服务于 progressive research 的模型更新。它不负责多抓资料，而负责把来源转换成可审计、可复核、可拒绝的证据对象。

## 目标

- 明确现有抓取能力已经能解决什么，避免重复造搜索、浏览器、PDF 或字幕工具。
- 对每个数据缺口判断：可自动化、需授权导入、只能 source-lead、或不应构建。
- 把外部材料转换为 `Source Card`、`Number Row`、`Claim Row`、`Quote Row`、`Conflict Row` 和 `Model Patch Candidate`。
- 让模型更新只发生在证据对象通过来源分层、口径归一和写入门禁之后。

## Public Fallback Rule

The public version has no hard dependency on AnySearch, web-access, browser CDP, markitdown, PDF/Office skills, RSS pipelines, or paid data terminals.

Use the best available capability in the current agent runtime:

- If a dedicated discovery tool exists, use it for source discovery.
- If it does not, use ordinary web search, browser navigation, official pages, URL fetch, or user-provided files.
- If a parser is unavailable, ask for a text/CSV export or capture a source lead instead of pretending the source was parsed.
- Always record `acquisition_method`, `permission_status`, and source limitations.
- Never let snippets, search summaries, or paid/licensed secondary material update the model directly.

## 已有能力边界

| capability | existing tool | use for | do not rebuild |
| --- | --- | --- | --- |
| 通用发现 | AnySearch / web search / Tavily / runtime search | 找来源入口、官方页面、新闻线索、大数 | 不再做新通用搜索器 |
| 登录态和动态页面 | web-access / browser CDP / user-authorized browser | 用户授权登录态、动态渲染、交互页面 | 不再做通用浏览器抓取层 |
| 已知 URL 正文 | AnySearch `extract` / Jina / WebFetch / curl / runtime URL fetch | HTML 正文化、网页正文 | 不把正文抽取当事实核验 |
| 本地文件读取 | markitdown / pdf / docx / xlsx / pptx / runtime file readers / user export | PDF、Office、OCR、表格读取 | 不再做通用文件读取器 |
| YouTube 字幕 | youtube-digest / yt-dlp / platform transcript / user export | YouTube transcript | 不再做 YouTube 字幕下载器 |
| 信息流增量 | RSS / daily-digest-hub / user-provided feed export | 普通 RSS、YouTube、日常信息流 | 不把 digest 当研究事实源 |
| 大类免费 API | AkShare / FRED / World Bank 等 | 宏观、市场规模、行情快照 | 不替代公司披露和模型底稿 |

剩余缺口是 source-specific locator、结构化抽取、权限状态、来源分层、冲突检测和模型补丁生成。

## AnySearch 使用规则

AnySearch 是可选发现/初筛工具。若当前环境没有 AnySearch，使用 runtime search/browser/URL fetch 继续推进，并把缺失能力写入 Source Card 或 open question。AnySearch 适合：

- `search`：实时通用搜索、找官方来源、找最新公开线索。
- `batch_search`：2-5 个独立查询并行，适合多公司、多来源、多假设初筛。
- `extract`：已知 HTML URL 正文抽取，输出 Markdown；长文可能截断，不适合 PDF 或复杂数据面板。
- `list_domains`：垂直域目录。涉及 finance、academic、legal、code 等结构化查询时先调用。

垂直域规则：

- 先调用 `list_domains`，缓存本轮结果。
- 严格按返回的 query constraints 构造 query，不把自然语言句子塞进要求 ticker/code 的域。
- `region = CN` 时才使用 `--zone cn`；US/ALL 域不要加 CN zone。
- `finance.us_stock` 和 `finance.cn_stock` 输出可作为行情、估值、财务摘要 snapshot，必须标 snapshot 日期和来源，不直接作为一手财务事实。

推荐命令形态：

```powershell
python <anysearch>/scripts/anysearch_cli.py list_domains --domain finance
python <anysearch>/scripts/anysearch_cli.py search "AAPL" --domain finance --sub_domain finance.us_stock --max_results 5
python <anysearch>/scripts/anysearch_cli.py search "600519" --domain finance --sub_domain finance.cn_stock --zone cn --max_results 5
python <anysearch>/scripts/anysearch_cli.py batch_search --queries '[{"query":"SEC EDGAR companyfacts API","max_results":3},{"query":"HKEX annual report search","max_results":3}]'
python <anysearch>/scripts/anysearch_cli.py extract "https://example.com/article"
```

AnySearch 输出的默认状态：

| output type | default status | can patch model directly? |
| --- | --- | --- |
| Search result snippet | source-lead | no |
| Search result URL | source locator candidate | no |
| Extracted HTML text | parsed source text | no |
| Finance vertical snapshot | vendor/aggregated snapshot | only after field policy allows |
| News result | press source-lead | no |

## Source Tiers

| source_tier | examples | default use | model write policy |
| --- | --- | --- | --- |
| `primary_regulatory` | SEC, exchange filings, regulator databases | factual anchor | eligible after normalization |
| `primary_company` | IR pages, annual reports, investor decks, official activity records | company facts and management claims | review required |
| `vendor_standardized` | Bloomberg, FactSet, Wind, Choice, Capital IQ exports | standardized data and cross-check | field-level policy required |
| `licensed_secondary` | sell-side reports, paid industry databases, professional newsletters | source-lead, estimates, assumptions | crosscheck required |
| `press_source_lead` | Reuters, Bloomberg News, WSJ, The Information | private-company lead, conflict signal | auto blocked until corroborated |
| `expert_interview` | podcast, conference, expert call transcript | user/expert prior, source-lead | open question or assumption first |
| `user_local_file` | local PDF, spreadsheet, exported deck | depends on origin | permission and source tier required |
| `altdata_public` | procurement, patent, trade, cloud pricing, ATS jobs | monitoring and proxy signals | review required |

## Evidence Objects

Every object must point back to a `Source Card`. Nothing updates the model directly except a `Model Patch Candidate`.

| object | minimum fields | behavior |
| --- | --- | --- |
| Source Card | `source_card_id`, `source_tier`, `title`, `entity_ids`, `author_org`, `publish_date`, `url_or_file`, `permission_status`, `acquisition_method`, `document_id`, `checksum`, `source_boundary_note` | provenance anchor |
| Number Row | `number_row_id`, `source_card_id`, `metric_name`, `value`, `unit`, `period`, `entity_scope`, `segment`, `citation_anchor`, `normalization_rule`, `confidence`, `review_status`, `candidate_model_fields` | bridge into Calculation Sheet |
| Claim Row | `claim_row_id`, `source_card_id`, `claim_type`, `subject`, `claim_text`, `time_horizon`, `supporting_anchors`, `confidence`, `review_status` | supports synthesis, assumptions, open questions |
| Quote Row | `quote_row_id`, `source_card_id`, `speaker_name`, `speaker_role`, `event_name`, `quote_text`, `citation_anchor`, `quote_policy`, `confidence` | supports management language and citeable context |
| Conflict Row | `conflict_row_id`, `new_object_id`, `existing_model_ref`, `conflict_type`, `old_value_or_claim`, `new_value_or_claim`, `definition_gap`, `resolution_status` | routes contradictions into review |
| Model Patch Candidate | `patch_id`, `target_artifact`, `target_row_id`, `patch_type`, `supporting_object_ids`, `suggested_value_or_text`, `write_policy`, `required_checks`, `final_status` | only object that may update model after review |

Suggested enums:

- `permission_status`: `public`, `login_session`, `paid_license`, `user_local_file`, `manual_export_only`, `prohibited`
- `review_status`: `raw`, `parsed_ok`, `cross_checked`, `human_verified`, `rejected`
- `write_policy`: `auto_blocked`, `review_required`, `crosscheck_required`, `eligible_after_validation`
- `claim_type`: `fact`, `management_claim`, `estimate`, `forecast`, `judgment`, `assumption`, `rumor_or_anonymous_lead`

## Write Rules

1. Search results never update `current-synthesis.md`, modules, or models directly.
2. Primary regulatory/company numbers may become `Model Patch Candidate` after exact source anchoring, unit/period normalization, and definition check.
3. Vendor standardized data may update only fields explicitly allowed by a field-level policy; otherwise use for cross-check.
4. Licensed secondary research, journalism, paid newsletters and expert interviews default to `source-lead` or `crosscheck_required`.
5. If new evidence conflicts with existing model rows, create `Conflict Row`; do not silently overwrite.
6. If a number is high-drift market data, include snapshot date and `needs refresh before trade`.
7. Paid/authorized sources must carry `permission_status` and `quote_policy`; do not store long copyrighted excerpts.

## Common Source Routes

| route | recommended first step | output target |
| --- | --- | --- |
| Unknown public source | AnySearch `search` / `batch_search` | Source Card candidate |
| Known HTML page | AnySearch `extract` or Jina/WebFetch | Source Card + Claim/Quote candidates |
| SEC filing | native SEC locator / XBRL first | Number Rows + Model Patch Candidates |
| CN/HK filing | exchange/native locator then PDF/HTML parse | Number Rows + Claim Rows |
| Earnings call / investor day | official IR/event page first | Quote Rows + Claim Rows + Number Rows |
| Local broker report | local report intake over PDF parser | licensed_secondary/user_local_file rows |
| SemiAnalysis/professional site | authorized browser/local export only | source-lead rows |
| Bloomberg/Wind/FactSet/Choice | API/Excel/CSV/XLS import only | vendor_standardized Number Rows |
| Alternative data | official API only | monitor rows |

## Minimal Completion Standard

A data acquisition run is complete only when it reports:

- what source was attempted and through which route;
- whether access was public, authorized, local, licensed, or blocked;
- what evidence objects were produced;
- which objects are eligible for model patch, which are source-leads only;
- what conflicts or missing fields remain;
- whether any model artifact was updated, or why no update was allowed.
