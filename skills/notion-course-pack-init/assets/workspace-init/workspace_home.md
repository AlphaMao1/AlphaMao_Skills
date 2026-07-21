# 学习工作区｜{{workspace_title}}

> 状态：{{workspace_status}}
> 最近检查：{{updated_at}}

这里是课程系统的总入口。新课程由 Codex 初始化；ChatGPT 只在课程建好后负责日常上课与轻量写回。

## 现在要做什么

- 新建课程：在 Codex 中调用 `notion-course-pack-init`，提供课程名称、完整材料与本页 URL。
- 继续上课：在 ChatGPT 中输入 `用 Notion 继续《课程名》`。
- 修复结构或权限：把问题写入 Codex Handoff Queue，交给 Codex 处理。

## 工作区导航

- [课程路由协议]({{route_protocol_url}})
- [Course Pack 模板库]({{template_library_url}})
- [手动写回模板]({{manual_writeback_templates_url}})
- [Notion 页面视觉标准]({{visual_standard_url}})
- [ChatGPT Notion 配置说明]({{chatgpt_setup_url}})

## 正式课程

{{course_index_or_empty_state}}

## 系统检查与归档

{{system_checks_and_archive}}

## 能力状态

- Codex 读取：{{codex_read_status}}
- Codex 写入：{{codex_write_status}}
- ChatGPT Notion App：{{chatgpt_connection_status}}
