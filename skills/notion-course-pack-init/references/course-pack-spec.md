# Course Pack Spec

This reference defines the first-version Notion Course Pack created by `notion-course-pack-init`.

## Core Principle

The Notion Course Pack is the fact source for a course. It is not a transcript, not a local mirror, and not a generated lecture bundle. Page count can be compressed, but content responsibilities cannot disappear.

The first version uses 8 pages per course:

1. Course Home
2. Runtime Snapshot
3. Course_Map
4. Course_State & Profile
5. Sources & Coverage
6. Sessions
7. Notes Inbox
8. Codex Handoff Queue

## Page Ownership and Updates

Each page contains one Codex-managed region identified by Course ID and page role. The generated region is replaceable; all blocks outside it are user-owned and must survive re-initialization or repair.

The managed metadata records:

- `managed_by: notion-course-pack-init`;
- Course ID;
- deterministic region ID `<course_id>:<page_role>:v1`;
- `replace-managed-region-only` update policy;
- SHA-256 fingerprint of the normalized managed payload, excluding wrapper metadata.

The eight page roles and URLs must be unique. Re-running initialization performs an exact upsert, not a second parallel Course Pack. Missing or duplicate managed regions are conflicts that require repair; they never authorize whole-page replacement.

Final `verified` state requires an independent post-write evidence receipt. Planned URLs, titles, and write fingerprints may define intent, but they cannot serve as their own readback proof. Runtime smoke proof must come from the isolated course's managed-region Test ID counts and protected-page before/after fingerprints.

## Page 1: Course Home

Stable, low-frequency course entry page.

Must include:

- course title, course ID, course type, and status;
- Runtime Index with links to all required child pages;
- course goal, formal scope, and material boundaries;
- brief course orientation merged from the old Course Brief responsibility;
- ChatGPT start command, usually `用 Notion 继续《课程名》`;
- configuration notes, completeness notes, and any known constraints;
- link or embedded summary for the per-course Tutor Runtime Prompt when applicable.

Do not put volatile per-lesson state here unless it is required for navigation.

## Page 2: Runtime Snapshot

High-frequency lightweight context cache for ChatGPT. It reduces repeated reads but does not replace the Course Pack.

Must include:

- current chapter or stage;
- current node summary:
  - Node ID;
  - source chapter or material range;
  - core question;
  - minimum completion standard;
  - next node;
- next lesson entry point;
- recent 1-3 session summaries;
- content not to repeat in the current round;
- pending writebacks or unresolved maintenance items;
- Course Pack version or last-updated timestamp.

If Runtime Snapshot conflicts with Course_Map or Course_State & Profile, treat it as stale and repair it.

## Page 3: Course_Map

Stable learning route and anti-drift anchor. It is not a translated table of contents.

Course_Map contains two labeled layers. The capability architecture is derived from the fully read source. The personalized route is derived from an answered learner-calibration receipt plus the source architecture. It may tentatively compress, reorder, or add bridge candidates when that makes learning faster and clearer. A skip candidate is not a mastered node until runtime evidence confirms the completion standard.

Must include a route-calibration section with the goal, intended use, baseline summary, first entry, evidence references, and the boundary `route-calibration-only-not-mastery`. If calibration is incomplete, do not create the production Course_Map.

Each node must include:

- Node ID;
- source chapter or material range;
- core question;
- key distinction to build;
- minimum completion standard in ability terms;
- skip condition;
- bridge-needed signal;
- common misconceptions;
- suitable example types;
- what not to expand in this node;
- next node.

Do not generate full lectures or a fixed question pool for every node. ChatGPT generates progression questions live during lessons.

## Page 4: Course_State & Profile

Dynamic progress state and stable learner profile combined into one page.

Must include:

- current progress and current node;
- next lesson entry point;
- completed nodes;
- skipped or compressed nodes and reasons;
- stable learner profile evidence;
- open reviews or pending checks;
- content not to repeat;
- changed user goals.

Initialization may only write empty state or explicit placeholders for mastery, completion, stable preferences, and misconceptions. Calibration may set a provisional current node and route candidates, but must cite `course_design_receipt.json` and must not turn those candidates into completed or mastered state.

Update the profile only when there is stable evidence, such as repeated misconceptions, clear preferences, effective explanation patterns, sustained interests, confirmed mastery, or changed goals. One-off mistakes belong in Sessions or candidate notes.

## Page 5: Sources & Coverage

Material coverage audit for the course. It is not the teaching order.

Must include:

- material source list;
- formal scope for this initialization;
- source structure;
- source-to-node mapping;
- node-to-source mapping;
- coverage gaps;
- user-mandated content;
- bridge nodes added for teaching efficiency.

Daily lessons do not update this page. Codex updates it only when course scope changes or material mapping errors are found.

## Page 6: Sessions

Primary lesson writeback surface.

Each session entry should include:

- Session ID and date;
- node ID and lesson goal;
- progression question asked;
- user answer summary;
- strategy used: `skip`, `compress`, `teach`, `bridge`, or `branch`;
- explanation or correction summary;
- progress result;
- review events if any;
- candidate notes created or updated;
- writeback summary.

Learning Events are not a separate first-version page. They are session entries or session summaries.

## Page 7: Notes Inbox

Candidate theme-note hub. It is not one note per lesson and not a formal Obsidian vault.

Rules:

- split notes by stable knowledge object;
- one lesson may create multiple candidate notes;
- a candidate note must record both the knowledge structure and user learning evidence;
- do not write class transcripts;
- do not directly import into formal Obsidian notes.

Each candidate note should include:

- core question;
- key concepts;
- reasoning structure;
- examples and counterexamples;
- common misconceptions;
- user learning evidence;
- next teaching hint;
- Obsidian import suggestion.

## Page 8: Codex Handoff Queue

Queue for rare Codex follow-up work.

Write here only for:

- new major materials;
- route restructure proposals;
- structural conflicts;
- candidate notes ready for Obsidian review;
- damaged Notion pages;
- configuration, permission, or sync issues.

Ordinary side interests do not automatically enter this queue. They can become candidate notes and normal profile evidence instead.

## Merged Responsibilities

The following older pages are not separate first-version pages:

- Course Brief: merged into Course Home.
- Interaction_Profile and Reviews: merged into Course_State & Profile.
- Sources and Source_Coverage: merged into Sources & Coverage.
- Notes_Spec: shared reference/template plus course-specific summary in Notes Inbox.
- Handoff_Template: shared reference/template, not a per-course page unless needed.
- Maintenance Output: transient writeback structure, not a page.
- Learning Events: entries inside Sessions.
- Node pages: default to Course_Map and Runtime Snapshot unless a course truly needs separate node pages.
