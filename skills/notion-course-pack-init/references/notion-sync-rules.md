# Notion Sync Rules

Use this reference whenever `workspace-init` or `course-init` writes visible Notion pages.

## Source of Truth

After successful sync, Notion is the Course Pack fact source. Local files are minimal audit artifacts, not a parallel Course Pack copy.

Local audit structure:

```text
course-packs/<course_id>/
  manifest.json
  course_design_receipt.json
  material_read_report.md
  sync_report.md
```

Do not maintain a full local Course Pack mirror unless the user explicitly changes the architecture.

## Tool Boundary

Notion reads and writes are performed by Codex through available Notion tools at runtime. Scripts may help validate local structures, render manifests, or check audit fields, but they must not hide external Notion writes.

If Notion tools are unavailable, stop before claiming workspace or course initialization success.

## Workspace Init Sync

For `workspace-init`:

1. Confirm target top page or workspace.
2. Fetch the target page to prove Codex-side read access.
3. Create or confirm shared pages:
   - route protocol;
   - template library;
   - manual writeback templates;
   - visual standard page;
   - ChatGPT Notion plugin setup instructions;
   - read/write test prompt.
4. Keep Codex-side Notion capability separate from ChatGPT-side Notion capability.
5. If ChatGPT can read but not write, mark manual-writeback mode.
6. Do not create real courses in `workspace-init` unless the user requested an end-to-end system check.

## Course Init Sync

For `course-init`:

1. Validate material coverage before writing.
2. Validate the 8-page Course Pack structure before writing.
3. Create or update the Course Home.
4. Create or update child pages.
5. Write page bodies from `assets/templates/` output.
6. Backfill Runtime Index links after page URLs exist.
7. Read back all eight pages, including Sessions.
8. Verify every page's managed region, fingerprint, and duplicate count before updating `manifest.json` and `sync_report.md`.

## Managed Region Contract

Every generated page body has one deterministic managed region with this identity:

```text
managed_by: notion-course-pack-init
course_id: <course_id>
region_id: <course_id>:<page_role>:v1
update_policy: replace-managed-region-only
source_fingerprint: <lowercase sha256 of normalized managed payload>
```

Use `assets/templates/managed_region_wrapper.md`: a dedicated toggle/callout headed by the exact `region_id`, with metadata followed by the rendered page-template blocks. Compute the fingerprint from the normalized payload blocks only; exclude wrapper metadata so the fingerprint does not hash itself. The visible representation may be Chinese-first; stable IDs remain English for interoperability.

On update:

1. Find Course Home by exact Course ID, then resolve each page role from the stored page URL or Runtime Index.
2. If no matching page exists, create it. If more than one match exists, stop and report the duplicates.
3. Fetch the page and locate the exact managed region.
4. Replace only that region when it occurs once. Preserve all user-authored blocks outside it.
5. If the region is missing or occurs more than once, stop instead of replacing the full page.
6. Read the page back and verify title, URL, region occurrence count, region ID, and source fingerprint.

Do not use title similarity, recent-page order, or fuzzy matching as an upsert key.

### Fingerprint Normalization

Use the same deterministic projection before write and after readback:

1. Walk managed payload blocks depth-first in visible order; do not include the wrapper heading or metadata lines.
2. For each block emit `<depth>\t<block_type>\t<plain_text>\t<link_or_empty>`.
3. Normalize Unicode to NFC, line endings to `LF`, and trim trailing whitespace on every line. Preserve meaningful leading whitespace and block order.
4. Exclude Notion block/page IDs, created/edited timestamps, user identity, colors, and other volatile API metadata.
5. Join records with one `LF`, UTF-8 encode without BOM, then compute lowercase SHA-256.

If the available Notion tool cannot expose enough structure to reproduce this projection, record readback as blocked. Do not substitute a title-only or URL-only fingerprint.

## Manifest Rules

`manifest.json` records:

- Course ID;
- Notion page URLs;
- parent-child relationships, including Course Home's parent URL when known and the seven child page roles under Course Home;
- generation timestamp;
- template version;
- material coverage status;
- structured material coverage evidence;
- managed-region metadata and per-page fingerprints;
- per-page readback receipts;
- idempotency receipt;
- isolated runtime-smoke receipt;
- validation status.

The full manifest is local only. Course Home may include a lightweight Runtime Index but should not expose technical manifest fields ChatGPT does not need.

### Independent Evidence Receipt

`render_manifest.py` accepts intended write declarations and one separate `--evidence-receipt-json` file. The receipt must be captured from actual post-write Notion fetches and the isolated smoke readback; never derive it from the same CLI page values, a provisional manifest, or ChatGPT's self-report.

Use receipt schema `notion-course-pack-init.evidence-receipt.v1` with:

- root `evidence_source: codex-notion-readback`, Course ID, and `captured_at`;
- `notion_readback.status: verified`, `verified_at`, and all eight page receipts;
- each page receipt's actual URL/title, region ID/count, `write_mode`, `prewrite_fingerprint`, `readback_fingerprint`, and `verified_at`;
- updated pages' `outside_managed_region_before_fingerprint` and `outside_managed_region_after_fingerprint` must be non-placeholder and equal; created pages mark both as `not_applicable_created`;
- verified idempotency receipt with timestamp, one Course Home match, and no duplicate page roles;
- verified isolated smoke receipt with authorization record and timestamp;
- four write-page receipts with `managed_region_test_id_occurrences: 1`;
- two protected-page receipts with matching `before_fingerprint` / `after_fingerprint` and `managed_region_test_id_occurrences: 0`;
- verified cleanup or explicit retention status and timestamp.

The renderer must reject a missing receipt, missing role, inconsistent timestamp, `.invalid` URL, all-zero fingerprint, write/readback mismatch, changed protected page, or unsupported smoke/cleanup status. It may emit `verified` only after this cross-check passes. Keep the receipt as an audit input; its SHA-256 is recorded in the manifest.

## Sync Report Rules

`sync_report.md` records:

- created pages;
- updated pages;
- skipped pages and reasons;
- readback validation results;
- managed-region occurrence and fingerprint checks;
- Course Home match count and duplicate page roles;
- isolated runtime-smoke and cleanup/retention receipt when performed;
- failures;
- manual repair instructions.

Every external write attempt should be reflected in the sync report.

## Readback Validation

After writing, fetch key pages and verify:

- page exists and is reachable;
- title matches expected role;
- Runtime Index links point to the intended pages;
- required sections are present;
- Runtime Snapshot current node summary exists;
- Course_Map has node boundaries and next-node links;
- Sources & Coverage maps sources to nodes;
- Notes Inbox states candidate-note rules;
- Codex Handoff Queue is present and not used for ordinary side interests.

The final readback receipt must cover all eight pages. Each receipt records page role, actual URL, actual title, region ID, `region_occurrences: 1`, `write_mode`, the managed fingerprint observed after write, and the outside-region preservation evidence required by that write mode. The idempotency receipt must record `course_home_matches: 1` and an empty `duplicate_page_roles` list.

## Runtime Smoke Isolation

A positive write smoke test requires separate user authorization and must target an isolated `SYSTEM CHECK` Course Pack or disposable copy. Use a fixed Test ID chosen before the prompt is rendered. Only Runtime Snapshot, Course_State & Profile, Sessions, and Notes Inbox may receive it. Course_Map and Sources & Coverage are protected and must be fingerprinted before and after the test.

After ChatGPT returns, Codex reads back all six relevant pages, verifies the fixed Test ID and protected fingerprints, then deletes the isolated course and confirms deletion or records the user's explicit retention choice. A production-course write test is never a valid receipt.

## Failure Handling

If Notion writeback fails:

- do not say the Course Pack was created in Notion;
- preserve local audit files if already created;
- record failed pages in `sync_report.md`;
- output manual writeback blocks when useful;
- tell the user the smallest safe recovery step.

If local generation succeeds but Notion sync fails, the course is not ready for ChatGPT runtime until required pages exist in Notion or manual writeback is completed.

## Visual Structure

Before creating or updating visible pages, read `references/notion-visual-reference-pack.md` when it exists. The goal is reference-driven Notion structure, not ad hoc page decoration.

After writing, check that:

- the first screen has clear navigation;
- key links use explicit text;
- page roles are visually distinguishable;
- status colors carry meaning;
- mobile reading does not depend on complex columns;
- decorative choices do not damage ChatGPT fetchability.
