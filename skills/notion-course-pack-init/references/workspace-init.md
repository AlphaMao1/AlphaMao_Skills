# Workspace Init

Use this reference for `workspace-init`.

## Current Product Assumptions

Product names and capabilities change. Last verified: 2026-07-21.

- Notion's hosted MCP server supports user-authorized read/write access and documents Codex configuration through `https://mcp.notion.com/mcp`: https://developers.notion.com/guides/mcp/get-started-with-mcp
- OpenAI calls integrations "apps": https://help.openai.com/en/articles/11487775-connectors-in-chatgpt

`workspace-init` verifies Codex-side Notion access. For ChatGPT, it provides one concise Notion App connection instruction and treats the current app as the normal read/write runtime surface. Only an actual lesson write error triggers permission troubleshooting.

## Required Reads

Before writing visible Notion pages, read:

- `references/setup-and-capabilities.md`
- `references/notion-visual-reference-pack.md`
- `references/notion-sync-rules.md`
- `references/validation-checklist.md`

Use output assets:

- `assets/workspace-init/workspace_home.md`
- `assets/workspace-init/route_protocol.md`
- `assets/workspace-init/template_library.md`
- `assets/workspace-init/manual_writeback_templates.md`
- `assets/workspace-init/visual_standard.md`
- `assets/workspace-init/chatgpt_notion_plugin_setup.md`
- `assets/workspace-init/workspace_init_report.md`
- `assets/workspace-init/system_check_page.md` only if the user explicitly requests an end-to-end system check.

## Flow

### 1. Confirm Target

Confirm or infer:

- target top workspace page;
- whether this is a new workspace or migration of an existing one;
- whether Codex may write to Notion now;
- whether the user wants an optional deletable system check page.

Do not create a demo course by default.

### 2. Check Codex-Side Notion Access

If Notion tools are missing, follow `references/setup-and-capabilities.md`. The Skill may prepare configuration and start the supported login flow after permission, but the user must complete OAuth consent. Resume only after the connection is available.

Use available Notion tools to:

- fetch the target page;
- confirm title and URL;
- record read access;
- perform a small write only when the user has authorized workspace initialization and the write target is clear.

If Codex cannot fetch the target, stop. Do not claim workspace initialization succeeded.

### 3. Create or Confirm Shared Workspace Pages

Create or confirm:

- top workspace page;
- route protocol page;
- template library page;
- manual writeback templates page;
- visual standard page;
- ChatGPT Notion plugin setup instructions;

Render these pages from the matching files under `assets/workspace-init/`. Do not invent a new route protocol or page system on every run.

Apply visual standards from `notion-visual-reference-pack.md`.

### 4. Generate ChatGPT Setup Instructions

Use `assets/workspace-init/chatgpt_notion_plugin_setup.md`.

The instruction must tell the user to:

- connect or enable the Notion app/connector in ChatGPT's current Apps or Connectors UI;
- authorize the relevant Notion workspace or pages;
- check admin/workspace app-action settings if using Business, Enterprise, or Edu;
- run the read/write test prompt;
- paste the test result back to Codex.

These setup instructions are user-facing and must be Chinese-first. Keep only product names, paths, IDs, and URLs in English.

### 5. Optional System Check Page

Only create `SYSTEM CHECK | Notion Course Pack self-check` when the user explicitly asks for end-to-end verification.

Rules:

- mark it as deletable or archivable;
- do not call it a demo course;
- do not use it as a template for real courses;
- do not store real learning evidence inside it.

### 6. Report

Use `assets/workspace-init/workspace_init_report.md`.

The report must say:

- what Codex checked or wrote;
- which workspace pages exist;
- Codex-side Notion capability;
- whether the ChatGPT Notion App connection instruction was provided;
- whether the workspace is ready, partially ready, or blocked;
- exact next action for the user.

## Stop Conditions

Stop and report blocked when:

- Codex-side Notion tools are unavailable;
- target workspace cannot be fetched;
- the user has not authorized Notion writes required for workspace setup;
- required shared pages cannot be created or confirmed;
- an actual ChatGPT write error remains unresolved.
