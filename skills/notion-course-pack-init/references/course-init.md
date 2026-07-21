# Course Init

Use this reference for `course-init`.

## Required Reads

Before running real course initialization, read:

- `references/course-pack-spec.md`
- `references/material-coverage-rules.md`
- `references/runtime-protocol.md`
- `references/notion-sync-rules.md`
- `references/validation-checklist.md`

Before creating visible Notion pages, also read:

- `references/notion-visual-reference-pack.md`

Use page templates from `assets/templates/`, then wrap every rendered body with `assets/templates/managed_region_wrapper.md` before Notion writeback.

Use output assets:

- `assets/course-init/material_read_report.md`
- `assets/course-init/sync_report.md`
- `assets/course-init/course_init_report.md`
- `assets/course-init/manual_notion_writeback_block.md`
- `assets/course-init/chatgpt_runtime_smoke_prompt.md`
- `assets/course-init/runtime_smoke_test_guide.md`

Use scripts:

- `scripts/render_manifest.py`
- `scripts/validate_course_pack.py`

Scripts are local-only and must not write Notion.

## Flow

### 1. Intake

Confirm or mark unresolved:

- course title;
- course goal;
- formal material scope;
- source files or authorized source pages;
- intended use;
- learner baseline and preferred depth;
- desired first lesson entry point if known.

Do not silently choose defaults for unresolved fields. Read the declared source before asking source-specific diagnostic questions.

If the user only provides a book title, course title, table of contents, or general topic, stop and request readable core material. Metadata is not enough for `course-init`.

### 2. Material Read Gate

Fully read every in-scope core material.

Hard fail when:

- any core material cannot be opened or parsed;
- only summaries, reviews, descriptions, or indexes are available;
- the declared scope is larger than the actually readable scope;
- the user asks to initialize a whole book/course but only provides part of it.

When failing, report the blocked material and do not create a half Course Pack.

If the material is too large, propose a smaller formal scope. Once accepted, fully read that smaller scope.

### 3. Learner Calibration Gate

After the material read gate and before Course_Map design, ask one to three adaptive, voice-friendly questions in one batch. Together they must:

- establish the learning goal and intended use;
- obtain at least one concrete mechanism, boundary, example, or transfer signal instead of relying only on self-rating;
- establish the desired or evidence-supported first lesson entry.

Existing reliable evidence in a prior Course_State may replace a question. An explicit answer such as “按零基础开始” is valid. Unanswered questions are not valid calibration.

Calibration answers are route-design evidence, not mastery evidence. They may select a start node, mark skip candidates for later live verification, or identify bridge candidates. They must not mark a node completed, mastered, or permanently skipped.

If calibration is incomplete, stop after material reading. Report the answered and unanswered fields and do not create production Notion pages or Course_Map.

Create `course_design_receipt.json` from `assets/course-init/course_design_receipt.json`. The receipt must contain the exact questions and answers, their source, the evidence boundary `route-calibration-only-not-mastery`, and a personalized-route summary.

### 4. Material Read Report

Create `course-packs/<course_id>/material_read_report.md` from `assets/course-init/material_read_report.md`.

It must record:

- materials provided;
- materials fully read;
- stable Material IDs, roles, declared ranges, exact read ranges, and SHA-256 source fingerprints;
- formal scope;
- out-of-scope material;
- blocked material;
- source-to-node evidence after Course_Map design;
- reciprocal node-to-source evidence using the same Material IDs;
- bridge nodes added for learning efficiency.

This report is local-only.

### 5. Course Model

Design the course model only after the calibration gate passes:

- course ID;
- stages;
- Course_Map nodes;
- prerequisites;
- ability-based completion standards;
- skip conditions;
- bridge signals;
- common misconceptions;
- source mappings;
- candidate note themes.

Separate two layers:

- `capability architecture`: source-derived concepts, dependencies, boundaries, and ability standards;
- `personalized route`: evidence-calibrated start node, tentative compression or skip candidates, and bridge candidates.

Never label the capability architecture as the learner's fixed schedule. Skip candidates remain unverified until a live progression question confirms the node standard.

Do not generate long lectures. Do not pre-generate a fixed question pool. Only record node boundaries, standards, and progression-question direction.

### 6. Generate 8 Page Bodies

Use `assets/templates/` to generate:

1. Course Home
2. Runtime Snapshot
3. Course_Map
4. Course_State & Profile
5. Sources & Coverage
6. Sessions
7. Notes Inbox
8. Codex Handoff Queue

Initialization state must be empty or placeholder-only where there is no real lesson evidence. Calibration may establish a route start but never mastery, completion, stable preference, or misconception state.

Wrap each generated body in one deterministic managed region. Its identity is `<course_id>:<page_role>:v1`, and its metadata records `managed_by`, Course ID, update policy, and the SHA-256 fingerprint of the normalized managed payload. Compute the fingerprint over the page-template content only, excluding wrapper metadata. Blocks outside that region belong to the user and are never replacement targets.

### 7. Local Preflight

Before Notion write:

- check all 8 page bodies exist;
- check Course Home contains Runtime Index placeholders;
- check Runtime Snapshot contains current node summary;
- check Course_Map has complete node fields;
- check Notes Inbox contains candidate-note rules and Notes_Spec summary;
- check Sources & Coverage maps all fully read materials to nodes;
- check no page claims unread material was covered.

### 8. Notion Write

Upsert the Course Home and 7 child pages by exact Course ID and page role.

- Search for the exact Course ID before creating Course Home. Create only when there are zero matches; update only when there is one; stop when there are multiple matches.
- Resolve child pages from stored URLs/Runtime Index and exact page role. Never use title similarity or recent-page order.
- When updating, replace only the single matching managed region. If it is missing or duplicated, stop; do not replace the whole page.
- Preserve user-authored blocks outside the managed region. For every updated page, fingerprint the normalized outside-region projection before and after the write and require equality; for a newly created page, record `write_mode: created` and `not_applicable_created` for both outside-region fields.

After URLs exist:

- backfill Runtime Index links;
- write a provisional `sync_report.md` with actual external write results;
- retain the intended page titles, URLs, and normalized managed-region write fingerprints as render declarations;
- do not write the full manifest into Notion.

### 9. Readback Validation

Fetch all eight pages:

- Course Home;
- Runtime Snapshot;
- Course_Map;
- Course_State & Profile;
- Sources & Coverage;
- Sessions;
- Notes Inbox;
- Codex Handoff Queue.

For each page, record the actual title and URL, confirm the exact region ID occurs once, and compare the readback fingerprint with the intended fingerprint. Re-run the exact Course ID/page-role lookup and record `course_home_matches` plus any duplicate page roles. Capture these observations in an independent evidence receipt JSON; do not generate it by copying the render declarations or a provisional manifest. Update the sync report from the same observations. Any mismatch is a failed sync and must be repaired before runtime smoke.

### 10. Runtime Smoke Prompt

Only after explicit user authorization, create or confirm a disposable `SYSTEM CHECK` Course Pack or isolated copy. Its Course ID and Course Home URL must differ from production. Choose one fixed Test ID before rendering any prompt.

Generate a ChatGPT runtime functional smoke prompt from `assets/course-init/chatgpt_runtime_smoke_prompt.md`.

Also generate a runtime functional smoke test guide from `assets/course-init/runtime_smoke_test_guide.md`. The guide must include one complete ChatGPT prompt that tests the functional points in one run: route protocol read, Course Home location, required page reads, current-node location, progression-question generation, smoke-marked writes to Runtime Snapshot / Course_State & Profile / Sessions / Notes Inbox, no write to Course_Map, no write to Sources & Coverage, and a return report template for Codex.

Before handing the smoke prompt or guide to the user, render every template variable. The delivered artifacts must contain the concrete `SYSTEM CHECK` title, isolated Course Home URL, fixed Test ID, and local audit directory. If any `{{...}}` placeholder remains, stop and regenerate. The prompt must refuse an empty/non-specific target and must not choose the most recent or most similar course.

The guide is a user-facing artifact and must be Chinese-first. Keep only stable page-role names, paths, commands, IDs, and URLs in English.

After ChatGPT returns its report, Codex must read back the isolated Runtime Snapshot, Course_State & Profile, Sessions, Notes Inbox, Course_Map, and Sources & Coverage. Record the fixed Test ID occurrence inside each managed region on the four allowed pages, and record before/after fingerprints plus zero Test ID occurrences on the two protected pages. Then delete the isolated course and verify deletion, or record the user's explicit decision to retain it. Add the actual verification and cleanup timestamps to the evidence receipt.

Render the final evidence-bearing manifest with `scripts/render_manifest.py`. Supply `--course-design-json <course_design_receipt.json>`, the structured material receipt, intended page declarations, and `--evidence-receipt-json <receipt.json>`. The renderer cross-checks these sources and rejects missing calibration, unanswered calibration items, placeholder URLs/hashes, readback mismatches, incomplete Test ID receipts, changed protected pages, or unverified cleanup. Then run:

```text
python scripts/validate_course_pack.py course-packs/<course_id>
```

Final local validation must fail when material evidence is partial, a managed region is missing/duplicated, readback fingerprints disagree, page roles are duplicated, the smoke target is production, the prompt/guide is unrendered, protected pages changed, or cleanup/retention is unverified.

If the user does not authorize the isolated smoke, stop after the Notion readback receipt and report `Course Pack initialized; runtime smoke pending`. Do not claim full system readiness and do not manufacture a passing manifest.

## Failure Output

### Material Failure

Report:

- blocked source;
- why it is required;
- what was actually readable;
- what user should provide;
- whether a smaller formal scope is possible.

Do not generate a Course_Map.

### Notion Failure

Use `assets/course-init/manual_notion_writeback_block.md`.

Report:

- which page failed;
- whether local audit files exist;
- which manual blocks to paste;
- whether ChatGPT runtime can start;
- what must be fixed before the next step.

## Success Output

Use `assets/course-init/course_init_report.md`.

Report:

- course page URL;
- local audit directory;
- material coverage status;
- Notion validation result;
- isolated ChatGPT runtime smoke result, or the explicit `runtime smoke pending` status;
- remaining risks.
