# Validation Checklist

Use this checklist before reporting success.

## Skill Structure

- `SKILL.md` exists and passes `quick_validate.py`.
- `agents/openai.yaml` exists.
- `references/`, `assets/templates/`, and `scripts/` exist.
- Required reference files for the selected mode exist.
- `references/setup-and-capabilities.md` records both Codex-side and ChatGPT-side setup boundaries.
- Required templates for generated pages exist before real `course-init`.
- `assets/templates/managed_region_wrapper.md` exists and is used around every rendered page body.

## Language

Pass only when all are true:

- user-facing reports, Notion page bodies, setup instructions, smoke-test guides, manual writeback blocks, and ChatGPT prompts are Chinese-first;
- English is limited to paths, commands, IDs, template variables, page-role names, tool/API/model/protocol names, and URLs;
- no delivered runtime guide or setup guide is English-primary.

## Workspace Init

Pass only when all are true:

- target Notion workspace or top page is known;
- Codex-side Notion connection is authenticated through user-authorized access; no token was requested or stored;
- Codex-side Notion fetch works;
- shared route protocol exists or was created;
- shared template library exists or was created;
- visual standard page exists or was created;
- ChatGPT Notion App connection instructions exist or were created;
- no real demo course was created unless explicitly requested as a system check.
- workspace home, route protocol, template library, manual writeback templates, and visual standard were rendered from the bundled workspace assets.

## Course Init: Material Gate

Pass only when all are true:

- course name, goal, intended use, formal scope, learner baseline, preferred depth, and first entry point are explicitly answered or supported by existing evidence;
- `course_design_receipt.json` exists, contains one to three answered calibration items, and records `route-calibration-only-not-mastery`;
- at least one calibration item contains a concrete mechanism, boundary, example, or transfer signal unless the learner explicitly chose a zero-baseline route;
- every in-scope core material was fully read;
- blocked or excluded materials are explicitly recorded;
- no summary-only or index-only source is counted as covered;
- material read report exists;
- every material has a stable ID, exact declared/read ranges, role, status, and SHA-256 source fingerprint;
- Course_Map node-to-source mapping is documented in both directions;
- `manifest.json.material_coverage` agrees with the human-readable report.

Hard fail:

- any required core material cannot be read;
- the declared scope is larger than the actually read scope;
- source coverage is inferred from secondary material.

## Course Init: Local Structure

Pass only when all are true:

- 8 required pages are generated;
- every page has one deterministic managed region keyed by Course ID and page role;
- Course Home includes Runtime Index;
- Runtime Snapshot includes the calibrated current node summary, next lesson entry, and course-design receipt reference;
- Course_Map is not a table-of-contents copy and visibly separates capability architecture from personalized route;
- Course_Map nodes include boundaries, ability standards, skip conditions, bridge signals, misconceptions, and next nodes;
- Course_State & Profile is empty or placeholder-only for mastery and stable profile fields; calibration may set route state but not completion or mastery;
- Sources & Coverage maps source ranges to Course_Map nodes;
- Sessions page is ready for lesson entries;
- Notes Inbox defines candidate theme-note rules;
- Codex Handoff Queue exists and is limited to Codex-worthy issues.

## Notion Sync

Pass only when all are true:

- required pages were created or updated in Notion;
- all eight pages were fetched after writing;
- Runtime Index links resolve;
- manifest contains actual Notion URLs and Course Home child-page relationships;
- each readback receipt has the actual title/URL, exactly one managed region, and a matching source fingerprint;
- `render_manifest.py` consumed a separate evidence receipt captured from Notion readback, not values copied from the render declarations;
- each readback receipt records `write_mode`, both managed write/readback fingerprints, the required outside-region preservation fields, and an actual verification timestamp;
- Course Home lookup returns exactly one match and duplicate page roles are empty;
- updated pages have equal non-placeholder outside-region before/after fingerprints; created pages explicitly mark the comparison not applicable;
- sync report records created, updated, skipped, and failed items;
- material read report and sync report exist and are not empty;
- no failed write is described as successful.

## Runtime Smoke Test

Do not run a positive write smoke against a production course. If the user has not explicitly authorized an isolated `SYSTEM CHECK` course, report `Course Pack initialized; runtime smoke pending` and do not claim full readiness.

Pass only when all are true:

- the smoke target is a separate `SYSTEM CHECK` course or disposable copy with a different Course ID and Course Home URL from production;
- the user authorized that isolated write test;
- Codex chose a fixed Test ID before rendering the prompt;
- delivered smoke prompt and guide contain the concrete isolated title, isolated Course Home URL, and fixed Test ID, with no `{{...}}` placeholders;
- the prompt refuses missing/placeholder targets and never chooses the most recent or most similar course;
- ChatGPT read the route protocol, Runtime Snapshot, and current Course_Map node;
- ChatGPT generated one live progression question rather than an initialization diagnosis question;
- the fixed Test ID appears exactly once in Runtime Snapshot, Course_State & Profile, Sessions, and Notes Inbox;
- those writes are marked as smoke records, not real progress, mastery, or formal candidate notes;
- Course_Map and Sources & Coverage retain their pre-test fingerprints and do not contain the Test ID;
- the evidence receipt records managed-region Test ID counts, protected-page before/after fingerprints, authorization, verification, and cleanup timestamps;
- Codex performed the readback itself rather than trusting only ChatGPT's report;
- the isolated course was deleted and deletion verified, or the user explicitly chose retention and that choice is recorded;
- `render_manifest.py` received real material, page, readback, idempotency, and smoke evidence;
- `validate_course_pack.py` passes against the final audit directory.

## Lesson Writeback Criteria

A successful lesson writeback includes:

- Course_State & Profile progress update;
- Sessions entry;
- Notes Inbox candidate note creation or update when needed;
- Runtime Snapshot refresh;
- short next-conversation prompt for the user.

Sources & Coverage is not updated during normal lessons.

## Failure Report Format

When blocked, report:

- failed stage;
- exact blocker;
- evidence gathered;
- what was not done;
- smallest safe next action;
- whether any Notion state changed.

Never hide uncertainty behind a polished completion summary.
