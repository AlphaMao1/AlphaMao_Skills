# Notion Visual Reference Pack

Last checked: 2026-07-09

Use this reference before creating or updating visible Notion pages. The goal is not to invent a pretty style from scratch. The goal is to extract stable patterns from official Notion guidance and mature marketplace templates, then apply them conservatively to Course Pack pages.

## Reference Sources

Do not copy paid templates, full pages, screenshots, names, copy, or proprietary layouts. Use these only as pattern references.

Official Notion references:

- [Notion for education](https://www.notion.com/help/notion-for-education): education workspace setup, templates, student/teacher workspace assumptions.
- [Setting up Notion for school](https://www.notion.com/help/guides/setting-up-notion-for-school): school workspace, notes, reading lists, planning, collaboration.
- [Start with a template](https://www.notion.com/help/guides/start-with-a-template): templates as starting structure, not as content to copy blindly.
- [Page icons & covers](https://www.notion.com/help/guides/page-icons-and-covers): icons and covers help page recognition and digestibility.
- [Using database views](https://www.notion.com/help/guides/using-database-views): table, list, board, gallery, calendar, and timeline views.
- [When to use each type of database view](https://www.notion.com/help/guides/when-to-use-each-type-of-database-view): choose views based on task, not decoration.
- [Board view databases](https://www.notion.com/help/guides/board-view-databases): boards work for status-based task and process management.
- [Getting started with projects and tasks](https://www.notion.com/help/guides/getting-started-with-projects-and-tasks): simple task systems, projects/tasks relation, avoid over-heavy process.
- [Give your to-dos a home with task databases](https://www.notion.com/help/guides/give-your-to-dos-a-home-with-task-databases): central task surfaces and filtered views.
- [Dashboards view](https://www.notion.com/help/dashboards): useful as an information-architecture reference, but do not require it because it is Business/Enterprise plan functionality.

Marketplace pattern references:

- [Student dashboards category](https://www.notion.com/templates/category/student-dashboards): home base for courses, assignments, exams, deadlines, progress.
- [Free course site templates category](https://www.notion.com/templates/category/free-course-site-templates): course sites, class hubs, syllabi, course delivery pages.
- [Course Delivery Hub / Course Portal](https://www.notion.com/templates/course-delivery-hub-course-portal): course overview plus module/course delivery navigation.
- [Knowledge Hub Template](https://www.notion.com/templates/simple-knowledge-hub): notes, references, and insights in one hub.
- [Top free Knowledge Hub templates](https://www.notion.com/templates/collections/top-10-free-knowledge-hub-templates-in-notion): searchability, taxonomy, and avoiding over-complex structures.
- [Minimalist Student Dashboard](https://www.notion.com/templates/minimalist-student-dashboard): simple course, assignment, exam, and note arrangement.
- [Janice Studies' student dashboard](https://www.notion.com/templates/student-dashboard): tasks, to-dos, courses, notes, and assignment awareness in one place.

## Extracted Layout Modes

### 1. Workspace Dashboard / Course Hub

Use for the top-level shared workspace.

First screen should show:

- current courses;
- shared route protocol;
- template library;
- ChatGPT setup and read/write test;
- Codex Handoff Queue or pending system issues;
- clear create-new-course entry for Codex, not ChatGPT autonomous initialization.

Pattern:

```text
Title
Status callout
Quick links
Current courses
Setup / protocol
Pending queue
Archive
```

Do not make the workspace look like a marketing landing page. It is an operations hub.

### 2. Course Portal

Use for Course Home.

First screen should show:

- current course status;
- Runtime Snapshot link;
- current node and next lesson prompt;
- Course_Map link;
- Course_State & Profile link;
- Notes Inbox link;
- Sources & Coverage link;
- ChatGPT start command.

Pattern:

```text
Course title
One-line current status
Next lesson command
Runtime Index
Current node summary
Course navigation
Completeness / warnings
```

Do not bury the start command or Runtime Index below long course descriptions.

### 3. Notes / Knowledge Hub

Use for Notes Inbox.

First screen should show:

- candidate-note rules;
- filter or section by status;
- filter or section by Course_Map node;
- candidate notes grouped by stable knowledge object;
- Obsidian review status.

Pattern:

```text
Notes Inbox title
Candidate-note rules
Status views: draft / needs review / ready for Obsidian / archived
Topic clusters
Recent notes
Review instructions
```

Do not create one note per lesson by default. Do not make candidate notes look like already-approved Obsidian notes.

### 4. Inbox / Task Queue

Use for Codex Handoff Queue.

First screen should show:

- open Codex-worthy items;
- status;
- priority;
- reason Codex is needed;
- source page or session;
- smallest next action.

Pattern:

```text
Queue title
Open items
Status groups: open / waiting user / in progress / done / archived
Priority or blocker
Source link
Next action
```

Use board-style status grouping only if it remains readable. A simple table or list is acceptable and often better.

## Page-Specific Standards

### Top Workspace

- Must show shared protocol and template entry points in the first screen.
- Must distinguish real courses from system checks and archives.
- Must not say users can close Codex for initialization.
- Must include setup instructions for both Codex skill and ChatGPT Notion plugin.

### Course Home

- Must act as a course portal, not a long essay.
- Runtime Index must be near the top.
- The next lesson command must be obvious and copyable.
- Material scope and completeness warnings must be visible.

### Runtime Snapshot

- Must be short, scannable, and high-frequency.
- Current node summary must fit near the top.
- Recent session summaries should be capped at 1-3 items.
- Do not turn it into a Course_Map duplicate.

### Course_Map

- Use clear node headings and repeated fields.
- Avoid dense nested toggles for fields ChatGPT must read.
- Keep node IDs stable and visible.
- Do not rely on visual indentation alone to show dependencies.

### Course_State & Profile

- Separate current progress from stable learner profile.
- Show evidence state: empty, placeholder, observed, stable.
- Do not color-code mastery without textual evidence.

### Sources & Coverage

- Prefer tables for source-to-node and node-to-source mappings.
- Use explicit status labels: fully read, out of scope, blocked, metadata only.
- Do not hide coverage gaps in toggles.

### Sessions

- One session entry should be easy to scan.
- Use consistent fields for progression question, user answer summary, strategy, result, notes, and next action.
- Long transcripts do not belong here.

### Notes Inbox

- Group by knowledge object, status, and source node.
- Candidate-note warnings must be visible.
- Use status colors sparingly.
- Keep Obsidian import suggestions explicit but not automatic.

### Codex Handoff Queue

- This is a work queue, not a showcase.
- Every item needs a reason Codex is needed.
- Ordinary side questions must not appear here unless they became a structural issue or Obsidian review item.

## Visual System

### Icons

Use a consistent, small icon system to help recognition:

- Workspace: hub / compass / school-like icon.
- Course Home: book or graduation-related icon.
- Runtime Snapshot: radar / compass / lightning-like icon.
- Course_Map: map icon.
- Course_State & Profile: status / user icon.
- Sources & Coverage: archive / source icon.
- Sessions: calendar / log icon.
- Notes Inbox: note / inbox icon.
- Codex Handoff Queue: tool / queue icon.

Do not use icons as decoration piles. One page icon and a small number of section markers are enough.

### Color

Use color only for state and hierarchy:

- green: ready / active / complete;
- yellow: needs attention / pending;
- red: blocked / failed validation;
- blue: information / protocol;
- gray: archived / inactive / unknown.

Do not create random multi-color aesthetic pages. Do not make color the only carrier of meaning; always include text status.

### Covers and Images

Covers are optional. If used, they should not push Runtime Index, current node, or next command below the useful first screen.

Avoid stock-like decorative covers for course operations pages. For specific courses, a restrained course-relevant cover is acceptable only if it does not harm readability.

### Layout

- Keep critical navigation in plain text links.
- Avoid critical information inside images, decorative callouts, or deeply nested toggles.
- Use columns only for light navigation or short summaries.
- Do not depend on complex multi-column layouts for mobile.
- Prefer repeated, predictable section structure over aesthetic variety.

### Database Views

Use the simplest view that fits the task:

- table: coverage mapping, queue details, source lists;
- list: recent sessions, quick links, notes index;
- board: status-based queue or candidate note review, only if readable;
- calendar: scheduled reviews if needed;
- gallery: avoid for critical runtime surfaces unless visual inspection is the main goal.

Do not require Notion Dashboard view because it may require Business/Enterprise plan. A normal Notion page can still behave like a dashboard through headings, links, callouts, simple tables, and linked databases.

## ChatGPT Fetchability

ChatGPT must be able to fetch and understand the page without seeing the visual design.

Therefore:

- every critical page must have explicit headings;
- every critical link must use descriptive text;
- statuses must be written as text, not only color;
- Runtime Index must not rely on visual cards only;
- table columns must have clear names;
- long decorative introductions must not precede operational context.

## Visual / Structural Validation

After workspace or course initialization, check:

- first screen shows the next useful action;
- page role is obvious from title, icon, and first section;
- required links are visible and fetchable;
- warnings and blocked states are visible;
- mobile reading does not depend on columns;
- status colors are consistent;
- no paid template content or copied full-page design is present;
- Course Pack pages still satisfy the structural validation checklist.

If visual polish conflicts with runtime clarity, runtime clarity wins.
