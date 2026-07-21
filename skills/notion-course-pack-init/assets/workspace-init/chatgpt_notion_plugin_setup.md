# ChatGPT Notion App 配置说明

在 `workspace-init` 期间，把本说明作为用户可见的配置指引。

## 目标

把 ChatGPT 连接到 Notion 工作区。连接完成后，ChatGPT 才能从 Course Pack 继续上课；如果当前账号和工作区权限允许，也可以在用户确认后写回轻量课程更新。

## 操作步骤

1. 打开用于上课的 ChatGPT 账号。
2. 进入 ChatGPT 的 Apps / Connectors 设置。当前界面通常称为 Apps，旧文档可能称为 Connectors 或插件。
3. 找到当前 Notion App 并连接。
4. 只授权本课程系统需要访问的 Notion 工作区或页面。
5. 回到普通 ChatGPT 对话，输入 `用 Notion 继续《课程名》`。

## 重要边界

OAuth 授权需要用户亲自确认，Skill 不会索要 Notion token。只有实际写入报错时，才进入手动写回与权限排查流程。
