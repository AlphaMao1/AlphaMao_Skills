# Setup and Capability Contract

Use this reference in every `workspace-init`, and whenever Notion access is missing or ambiguous.

Last verified: 2026-07-21.

## Product Boundary

The Skill does not grant Notion access by itself. Two execution surfaces need independent access:

1. Codex initializes and repairs the workspace and Course Packs.
2. ChatGPT runs lessons and writes lightweight progress updates.

Both surfaces should use user-authorized Notion access. Never request, print, store, or commit a Notion token.

## Codex-Side Connection

Prefer Notion's hosted MCP server:

```toml
[mcp_servers.notion]
url = "https://mcp.notion.com/mcp"
```

For Codex CLI, authentication is normally started with:

```text
codex mcp login notion
```

The user must complete the browser OAuth consent. The Skill may detect the missing connection, prepare the exact project-local or user-level configuration after receiving permission, and launch the login command when available. It must not claim that OAuth can be completed without the user.

After authentication, fetch the chosen top page and verify the title and URL before any write.

## ChatGPT-Side Connection

Tell the user once to connect the current Notion App in ChatGPT and authorize the course workspace. Treat that app as the normal read/write runtime surface. Do not add a separate capability warning, classification table, or setup smoke prompt. If a real lesson write fails, report the exact error and use the existing manual-writeback failure path.

## What Can Be Automated

After the two OAuth connections and target-page choice, the Skill owns:

- shared workspace page creation;
- source reading and coverage audit;
- learner calibration;
- Course_Map design;
- 8-page Course Pack generation;
- Notion upsert and readback validation;
- local audit receipts;
- isolated runtime smoke preparation and verification when explicitly authorized.

The user still owns actions that cannot be delegated safely:

- approving OAuth and workspace permissions;
- choosing the target Notion page or workspace;
- providing the full source material and answering calibration questions;
- confirming lesson writeback and optional destructive cleanup.

## Fail-Closed Rules

Stop and report the smallest recovery action when:

- Codex has no Notion read tool after configuration;
- OAuth is incomplete or the target page is outside the authorized scope;
- a real ChatGPT lesson write returns an error.

Do not downgrade these failures into a claim of full readiness.

## Primary Sources

- Notion MCP overview: https://developers.notion.com/guides/mcp/overview
- Notion MCP connection guide: https://developers.notion.com/guides/mcp/get-started-with-mcp
- OpenAI apps guidance: https://help.openai.com/en/articles/11487775-connectors-in-chatgpt
