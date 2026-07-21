---
name: notion-course-pack-init
description: "Initialize or repair a Notion Course Pack workspace, or create a real course from a complete book, course, paper set, transcript set, local files, pasted materials, or authorized Notion pages. Use when Codex must bootstrap Notion access, build the shared workspace and runtime protocol, fully read course sources, calibrate the learner route, create and validate the 8-page Course Pack, or prepare ChatGPT Notion app connection guidance. User-facing artifacts must be Chinese-first."
---

# Notion Course Pack Init

Use this skill for low-frequency, high-structure initialization work around a Notion Course Pack. Codex owns connection preflight, workspace setup, material reading, Course Pack generation, Notion writeback, and validation. ChatGPT with a Notion app that has the required capabilities owns later lesson interaction, tutoring, progress updates, and light writeback.

## Language Contract

All user-facing artifacts must be Chinese-first.

Use Chinese for Notion page body text, setup instructions, reports, validation guides, smoke-test guides, manual writeback blocks, reader-facing tables, ChatGPT prompts, and explanations addressed to learners, workspace users, or future maintainers.

English may remain only for interoperability: file paths, commands, IDs, manifest keys, template variables, tool names, API names, model names, protocol names, URLs, and stable page-role names such as `Runtime Snapshot`, `Course_Map`, `Course_State & Profile`, `Sources & Coverage`, `Sessions`, `Notes Inbox`, and `Codex Handoff Queue`.

Do not ship an English-only or English-primary runtime guide to the user. If a generated template contains English-visible labels, translate those labels before delivery.

## Mode Selection

Choose exactly one mode before acting.

- `workspace-init`: use when setting up or repairing the shared Notion course workspace, route protocol, template library, visual standards, or ChatGPT Notion app connection guidance.
- `course-init`: use when creating a real new course from books, papers, course pages, transcripts, local files, pasted materials, or existing user notes.

If the user asks for a new real course, choose `course-init`. If the user asks to prepare the system, templates, protocol, Notion setup, or open-source setup instructions, choose `workspace-init`.

## Hard Boundaries

- Do not make ChatGPT responsible for full course initialization.
- Do not offer `partial-init`, `course-extend`, or any equivalent shortcut in the first version.
- Do not create a demo course by default. Only create a deletable `SYSTEM CHECK | Notion Course Pack self-check` item when the user explicitly wants end-to-end system verification.
- Never run a write smoke test against a production course. Runtime smoke writes belong only in an isolated `SYSTEM CHECK` course or disposable copy with a fixed Test ID.
- Never replace a whole Notion page during an update. Replace only the matching managed region and preserve user-authored blocks outside it.
- Do not use summaries, reviews, encyclopedia entries, course descriptions, or second-hand notes as substitutes for full reading of the declared source scope.
- Do not generate long lectures or a fixed question pool for every node.
- Do not infer the learner's goal, baseline, preferred depth, or first lesson entry from the source material or the initialization request. A source-derived capability map is not a personalized learning route.
- Do not create production Notion pages or a personalized Course_Map until the learner calibration gate is complete.
- Do not treat ChatGPT memory as course state. The Course Pack in Notion is the course fact source.
- Do not import candidate notes directly into the formal Obsidian vault during course initialization.
- Do not claim zero-setup access. Notion OAuth and workspace permission approval require the user; the Skill must automate the remaining setup around that consent boundary.
- Do not request or store Notion tokens. Prefer user-authorized Notion MCP/app connections and least-privilege page access.

## Reference Routing

Load only the references needed for the selected mode. If a required reference is missing while implementing this skill, create or restore that reference before running the mode for real work.

For `workspace-init`, read:

- `references/setup-and-capabilities.md`
- `references/workspace-init.md`
- `references/notion-visual-reference-pack.md`
- `references/notion-sync-rules.md`
- `references/validation-checklist.md`

For `course-init`, read:

- `references/course-init.md`
- `references/course-pack-spec.md`
- `references/material-coverage-rules.md`
- `references/runtime-protocol.md`
- `references/notion-sync-rules.md`
- `references/validation-checklist.md`

When creating or updating visible Notion pages in either mode, also read `references/notion-visual-reference-pack.md` before writing pages.

Use page templates from `assets/templates/` when generating bodies, then wrap each rendered body with `assets/templates/managed_region_wrapper.md`. Use scripts from `scripts/` only for local validation, manifest rendering, or audit checks; do not hide Notion writes inside scripts.

## Workspace Init Flow

1. Confirm the target Notion workspace or top page.
2. Check whether Codex-side Notion tools are available. If not, follow `references/setup-and-capabilities.md`: prepare the supported Notion MCP configuration after permission, launch or explain OAuth login, and stop until the user completes consent. Then fetch the target and record its exact title and URL.
3. Create or confirm the top workspace, route protocol, template library, manual writeback templates, and visual standard page from `assets/workspace-init/`.
4. Generate concise ChatGPT-side Notion App connection instructions. Do not add a separate capability warning or read/write test prompt unless an actual runtime write fails.
5. Validate the workspace structure and visible navigation after writing.

## Course Init Flow

1. Confirm the course name and formal material scope. Record missing goal, intended use, learner baseline, preferred depth, and first-lesson entry as unresolved; never fill them with defaults.
2. Fully read every in-scope core material. If any core material cannot be fully read, stop and report the blocker instead of creating a half Course Pack.
3. Run the learner calibration gate before Course_Map design. Ask one to three adaptive, voice-friendly questions in one batch: establish the learning goal and intended use, obtain a concrete baseline signal with at least one transfer or mechanism probe, and determine the desired or evidence-supported first entry. Existing reliable course-state evidence may replace a question. An explicit learner choice to start from zero is valid calibration. If the user has not answered, stop after the material read and do not create production Notion pages.
4. Create `course_design_receipt.json`. Record the exact user answers or existing evidence, the evidence boundary `route-calibration-only-not-mastery`, and the calibrated start, skip candidates, and bridge candidates. Calibration can shape the route but cannot mark nodes mastered or completed.
5. Produce the local audit files under `course-packs/<course_id>/`: `manifest.json`, `course_design_receipt.json`, `material_read_report.md`, and `sync_report.md`. Record the exact material inventory, declared ranges, read ranges, SHA-256 source fingerprints, and reciprocal source-to-node mapping.
6. Design Course_Map as two explicit layers: a source-derived capability architecture and an evidence-calibrated personalized route. Do not present the capability architecture as a fixed lesson schedule.
7. Generate the 8-page Course Pack from templates: Course Home, Runtime Snapshot, Course_Map, Course_State & Profile, Sources & Coverage, Sessions, Notes Inbox, and Codex Handoff Queue. Give each page a deterministic managed region keyed by Course ID and page role.
8. Run the pre-write structural checks. Keep intended page URLs, titles, and write fingerprints as declarations; they are not readback evidence.
9. Upsert by Course ID and page role. Create only when no matching page exists; stop on duplicates. On update, replace only the matching managed region. Read back all eight pages and capture an independent evidence receipt containing `write_mode`, managed write/readback fingerprints, outside-managed-region before/after fingerprints for updates, region counts, actual verification timestamps, and idempotency results.
10. If the user explicitly authorizes end-to-end verification, create or confirm an isolated `SYSTEM CHECK` Course Pack, choose a fixed Test ID, and render the smoke prompt and guide with that isolated title, URL, and Test ID. Do not point them at the production course.
11. After ChatGPT returns the smoke result, read back the isolated course. Add the managed-region Test ID counts for the four allowed pages, before/after fingerprints for the two protected pages, and cleanup/retention verification to the evidence receipt. Then run `scripts/render_manifest.py --course-design-json <course_design_receipt.json> --evidence-receipt-json <receipt.json> ...`; missing or inconsistent evidence must fail closed.

## Validation Principles

Before Notion writeback, verify:

- all declared in-scope materials were fully read;
- `course_design_receipt.json` contains one to three answered calibration items, an explicit goal and intended use, a first entry, and a personalized-route receipt;
- the calibration answers are route-design evidence only and no node is marked mastered or completed from them;
- the structured material inventory records exact ranges, fingerprints, and reciprocal node mapping;
- the 8 required pages are present;
- Runtime Index links are planned;
- Course_Map separates the source-derived capability architecture from the calibrated personalized route and includes node boundaries, completion standards, skip conditions, bridge-needed signals, common misconceptions, and next nodes;
- Sources & Coverage maps source material ranges to Course_Map nodes;
- Notes Inbox remains a candidate-note area, not formal Obsidian notes.

After Notion writeback, verify:

- all eight created or updated pages can be fetched;
- each page contains exactly one matching managed region and the readback fingerprint matches the written fingerprint;
- the Course Home lookup returns exactly one course and no page role has duplicates;
- updated pages have matching non-placeholder outside-managed-region before/after fingerprints; created pages record that this comparison is not applicable;
- Runtime Index links resolve to the intended pages;
- Runtime Snapshot contains the current node summary and next lesson entry;
- `manifest.json` and `sync_report.md` match the actual Notion URLs and readback receipts;
- failures are reported as explicit manual writeback or repair steps, never as success.

## Output Contract

For successful `workspace-init`, report the workspace pages checked or created, Codex-side connection status, and the single remaining user action of connecting the Notion App in ChatGPT when needed.

For successful `course-init`, report the production course URL, calibration receipt, local audit paths, material coverage result, Notion readback/idempotency result, and readiness status. If isolated runtime smoke has not been explicitly authorized and verified, say `Course Pack initialized; runtime smoke pending` instead of claiming full system readiness.

If blocked, report the blocking material, missing tool, Notion permission issue, or failed validation step, plus the smallest safe next action.
