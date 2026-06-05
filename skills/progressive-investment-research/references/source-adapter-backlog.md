# Source Adapter Backlog

This backlog keeps the data acquisition layer small. Build adapters only when they solve a recurring data defect that existing search, browser, URL extraction, or local file parsing cannot solve.

## Priority Rules

1. Prefer official, stable, structured sources over broad crawling.
2. Reuse AnySearch for discovery and quick snapshots when available; otherwise fall back to the agent runtime's search/browser/URL fetch capabilities.
3. Reuse web-access/CDP for authorized browser access when available; otherwise use a user-authorized browser flow or manual export.
4. Reuse PDF/Office parsers for raw reading when available; otherwise ask for text/CSV export and keep the item as a source lead.
5. Paid terminals and professional sites are import/authorized-intake surfaces, not scraping targets.
6. Broad social scraping, paywall circumvention and terminal screen scraping are out of scope.

## Backlog

| priority | adapter | purpose | input | output | reuse | new capability | MVP | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | Source Card Schema + Entity Master | Give every evidence object stable provenance and entity IDs | source URL/file, company name/ticker/code | Source Card, entity map | existing dossier conventions | schema, IDs, permission fields, checksum | 10 mixed sources across US/CN/HK/local files | over-modeling if schema is too large |
| P0 | Discovery Wrapper | Standardize search, batch search and vertical search output into Source Card candidates | query list, domain intent | source candidates, snapshot notes | AnySearch CLI or runtime search | wrapper prompt/runbook, result normalization | 5 public source discovery tasks + finance snapshot | treating snippets as facts |
| P0 | Filing Source Locator | Resolve issuer to native disclosure documents | issuer, ticker, exchange, date range | filing queue with native IDs | AnySearch, browser, URL fetch, runtime search | SEC/CN/HK locator logic, dedupe, deltas | 3 US issuers, 3 A-share issuers, 2 HK issuers | portal churn, alias ambiguity |
| P0 | Filing Structured Extractor | Convert filings into Number/Claim rows | filing HTML/PDF/XBRL + Source Card | Number Rows, Claim Rows, Model Patch Candidates | PDF/HTML/Office stack | XBRL-first extraction, unit/period/segment normalization | revenue split, CapEx, backlog/order rows from sample issuers | custom tags, scanned tables |
| P1 | Event Transcript Extractor | Extract management language and Q&A evidence | transcript, IR deck, replay page, event metadata | Quote Rows, Claim Rows, Number Rows | browser, YouTube transcript, local audio where allowed | speaker mapping, Q&A segmentation, transcript provenance | 2 earnings calls, 1 investor day, 2 CN activity records | missing transcripts, ASR errors |
| P1 | Local Report PDF Intake | Turn local broker/industry reports into typed evidence | file/folder path | Source Cards, page-anchored rows, source-leads | markitdown, pdf, xlsx | assumption/forecast classifier, page spans, quote policy | 3 broker PDFs + 2 industry PDFs | copyright, inconsistent layouts |
| P1 | Authorized Site Adapter | Ingest paid/professional content under user authorization | logged-in page or local export | source-lead Number/Claim/Quote Rows | web-access/CDP, AnySearch extract when allowed | permission capture, excerpt limits, lead-vs-fact classifier | 2 SemiAnalysis-like samples + 1 industry data page | terms compliance, session fragility |
| P1 | CSV/XLS Terminal Import | Normalize exports from Bloomberg/FactSet/Wind/Choice/Capital IQ | CSV/XLS/XLSM/API dump | vendor_standardized Number Rows, Conflict Rows | xlsx/Office parser | mapping templates, stale export detection, mnemonic metadata | one sample export from any available terminal | hidden formulas, entitlement drift |
| P2 | Official Alt-Data Wrappers | Track structured public proxy signals | entity/product/time window | monitor rows, source cards | HTTP/API plumbing | per-source entity matching and time-series normalization | one procurement, patent, cloud price or ATS source | methodology drift, weak entity matching |

## MVP Validation Plan

### MVP 1: Filing Extraction Benchmark

Sample:

- 3 US issuers
- 2 Mainland China issuers
- 1 HK issuer

Hypothesis:

Official filing locators and structured extraction can produce audit-grade Number Rows and at least one valid Model Patch Candidate per issuer.

Pass criteria:

- Native filing/document IDs are captured for every sample.
- At least 85% precision on benchmark Number Rows.
- Every accepted row has a citation anchor: tag, page, table, section or document URL.
- No search snippet is used as a fact.

### MVP 2: Event Speech Benchmark

Sample:

- 2 earnings calls
- 1 investor day
- 2 China investor activity records

Hypothesis:

Event materials can be segmented into speaker-attributed Quote Rows, Claim Rows and Number Rows.

Pass criteria:

- Transcript origin is explicit: official, platform_auto, local_asr, or unknown.
- Speaker attribution is correct on official transcripts or official activity records.
- Q&A is separated from prepared remarks where available.
- Management claims that conflict with model assumptions create Conflict Rows.

### MVP 3: Licensed / Local Document Benchmark

Sample:

- 3 local sell-side or industry PDFs
- 1 authorized premium-content sample or local export
- 1 CSV/XLS terminal-style export if available

Hypothesis:

Non-public or licensed materials can be ingested without losing permission boundaries or over-promoting secondary claims.

Pass criteria:

- 100% of rows carry `permission_status`.
- Paid or secondary sources default to `source-lead` or `crosscheck_required`.
- No long copyrighted excerpts are stored.
- Conflicts with existing model values create Conflict Rows instead of overwriting.

## Recommended Build Sequence

| step | build | why |
| --- | --- | --- |
| 1 | Source Card schema + entity master | all adapters depend on stable provenance |
| 2 | AnySearch discovery wrapper | immediate value, low implementation cost |
| 3 | Filing Source Locator | highest-quality public source path |
| 4 | Filing Structured Extractor | converts official facts into model rows |
| 5 | Event Transcript Extractor | captures management claims and Q&A |
| 6 | Local Report PDF Intake | turns existing user materials into source-leads |
| 7 | CSV/XLS Terminal Import | useful only when exports or licenses exist |
| 8 | Official Alt-Data Wrappers | add after entity and evidence model are stable |

## Out Of Scope

- Generic search replacement.
- Generic browser automation replacement.
- Paywall circumvention.
- Terminal screen scraping.
- LinkedIn or other prohibited automation surfaces.
- Broad marketplace/social scraping before official sources are exhausted.
- Automatic model updates from snippets, press leads, expert claims or paid reports.
