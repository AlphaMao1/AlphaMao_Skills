# Material Coverage Rules

Use this reference in every `course-init`.

## Hard Gate

Formal course initialization must be based on full reading of every in-scope core material. If Codex cannot fully read a core material, stop the initialization and report the blocker.

Never create a formal Course Pack from:

- partial reading;
- index-only reading;
- summaries only;
- reviews or encyclopedia entries;
- course descriptions;
- second-hand notes or interpretations;
- a declared full book or full course when only part of it was read.

## Scope Declaration

Before reading, declare the formal scope:

- course title and goal;
- material list;
- exact ranges included, such as chapters, papers, lectures, pages, or files;
- explicit exclusions;
- first-lesson entry point if known.

Assign every material a stable `material_id` and one role: `core`, `supplemental`, or `metadata-only`. Record the exact source reference and declared range before reading. Do not silently widen or narrow that range.

If materials are too large, ask the user to shrink the formal scope or propose a smaller formal scope. Once a scope is declared, every core material inside it must be fully read.

## Learner Calibration

After fully reading the declared source scope, ask one to three adaptive calibration questions as defined in `references/course-init.md`.

These answers are route-design evidence only. They must not be used to claim mastery, misconceptions, completion, or stable preferences.

## Allowed Material Sources

Core materials may come from:

- local files;
- pasted text;
- PDFs, EPUBs, Markdown, Word documents, spreadsheets, slides, or transcripts readable by available tools;
- Notion pages the user authorizes;
- legal full-text web sources;
- user notes that are explicitly included in scope.

Use appropriate parsing tools for structured files. Do not rely on ad hoc string extraction when a better parser is available.

## Web Use

Web search may be used to:

- verify bibliographic metadata;
- find a table of contents;
- find publication or course information;
- find background context;
- locate legal full text.

Web search must not be used to replace full reading with summaries, reviews, Wikipedia-style pages, or other people's notes.

For unstable or current facts, verify with current primary sources and record the source date or retrieval date in the material read report.

## Failure Rules

Stop `course-init` when:

- a core source cannot be opened, parsed, or read completely;
- source scope is ambiguous and the ambiguity changes Course_Map design;
- the only available source is a summary or secondary account;
- a file is corrupted, encrypted, truncated, or inaccessible;
- a required Notion page cannot be fetched and no local source copy exists.

When stopped, report:

- which material blocked initialization;
- what was attempted;
- why the material is required;
- what the user can provide next;
- whether a smaller formal scope would be valid.

## Material Read Report

Create `course-packs/<course_id>/material_read_report.md` for every `course-init`.

It must record:

- user-provided materials;
- materials actually fully read by Codex;
- formal initialization scope;
- excluded or deferred materials;
- blocked materials and failure reasons, if any;
- Course_Map node to source mapping;
- bridge nodes added for teaching efficiency;
- source ranges used for each node.
- a SHA-256 fingerprint for every source object actually used;
- the read status and exact read ranges for every material;
- stable Material IDs used by `manifest.json`;
- reciprocal mapping: every material-to-node edge must also appear in node-to-material evidence.

Do not write this full audit report into Notion. It is a local audit artifact.

## Coverage Language

Use precise coverage language:

- `fully read`: Codex read the complete in-scope source.
- `out of scope`: intentionally excluded from this initialization.
- `blocked`: required but could not be read.
- `metadata only`: used for bibliographic or structural context, not content coverage.
- `bridge node`: added for learning efficiency and not a direct source chapter.

Never describe a source as covered unless it was fully read within the declared scope.

## Manifest Receipt

`manifest.json.material_coverage` is the machine-checkable receipt for this gate. It must contain:

- `status: fully_read`;
- the declared course scope;
- a non-empty material inventory with Material ID, title, source reference, role, declared scope, read status, read ranges, source fingerprint, and mapped node IDs;
- a non-empty node-to-source map with exact source ranges.

Every core material must be `fully_read`, have at least one read range, and map to at least one Course_Map node. The human-readable report and manifest receipt must agree. A missing field, partial core source, invalid fingerprint, unknown Material ID, or one-way mapping is a hard failure.
