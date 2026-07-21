# 课程｜{{course_title}}

## 就绪状态

{{ready_status}}

> 初始化状态只能写事实：已初始化 / 待补材料 / Notion 同步待验证 / 手动写回模式。不要写用户已经掌握什么，除非已有真实 session 证据。

## 下一讲入口

```text
用 Notion 继续《{{course_title}}》。
```

## Runtime Index

- Runtime Snapshot：{{runtime_snapshot_url}}
- Course_Map：{{course_map_url}}
- Course_State & Profile：{{course_state_profile_url}}
- Sources & Coverage：{{sources_coverage_url}}
- Sessions：{{sessions_url}}
- Notes Inbox：{{notes_inbox_url}}
- Codex Handoff Queue：{{codex_handoff_queue_url}}
- 课程路由协议：{{route_protocol_url}}
- 视觉 / 模板标准：{{template_or_visual_standard_url}}

## 当前定位

- Course ID：{{course_id}}
- 课程类型：{{course_type}}
- 当前阶段：{{current_stage_placeholder}}
- 当前节点：{{current_node_placeholder}}
- 下一讲目标：{{next_lesson_goal_placeholder}}
- 初始化时间：{{initialized_at}}
- Course Pack 版本：{{course_pack_version}}

## 课程设计校准

- 校准状态：{{calibration_status}}
- 学习目标：{{calibrated_learning_goal}}
- 预期用途：{{calibrated_intended_use}}
- 基础与深度摘要：{{calibrated_baseline_summary}}
- 第一讲入口：{{calibrated_first_entry}}
- 校准证据：{{course_design_receipt_path}}
- 证据边界：route-calibration-only-not-mastery

## 课程目标

{{course_goal}}

## 正式材料范围

{{formal_material_scope}}

## 不在本次范围内

{{out_of_scope_materials}}

## 课程设计原则

- Course_Map 按核心问题、前置依赖、概念边界、机制链条、能力目标和误区诊断组织，不机械照搬原材料目录。
- 用户能力足够时允许跳过或压缩；能力不足时补最小必要基础。
- 课程推进问题由 ChatGPT 在上课现场生成，不预生成固定问题池。
- 候选笔记进入 Notes Inbox，后续复核后再进入 Obsidian。

## Tutor_Runtime_Prompt

你是《{{course_title}}》的互动导师。每次上课必须基于本 Course Pack，而不是普通聊天记忆。

运行规则：

1. 先读 Runtime Snapshot，必要时再读 Course_Map 和 Course_State & Profile。
2. 定位当前节点后，现场生成一个适合用户水平的课程推进问题。
3. 根据用户回答选择 `skip` / `compress` / `teach` / `bridge` / `branch`。
4. 必须推进，不在同一概念上原地打转。
5. 支线问题正常回答，但不改 Course_Map；必要时写入候选主题笔记。
6. 一讲结束并经用户确认后，写回 Course_State & Profile、Sessions、Notes Inbox、Runtime Snapshot。
7. 不更新 Sources & Coverage，除非 Codex 后续介入处理范围或映射错误。

## 完整性备注

- 材料读取状态：{{material_read_status}}
- Notion 同步状态：{{notion_sync_status}}
- ChatGPT Notion App：{{chatgpt_connection_status}}
- 待用户确认：{{pending_user_confirmation}}
- 其他风险：{{known_risks}}
