# Notion 手动写回块

当 Notion 写入或回读校验失败时使用本模板。

## 失败位置

- 阶段：{{failure_stage}}
- 失败页面职责：{{failed_page_role}}
- 目标 URL：{{target_url}}
- 错误 / 限制：{{error_detail}}

## 已完成内容

{{completed_work}}

## 尚未写入内容

{{unwritten_work}}

## 手动粘贴目标

- 页面职责：{{page_role}}
- 页面标题：{{page_title}}
- 父页面：{{parent_page_url}}

## 需要粘贴的 Markdown

```markdown
{{page_markdown}}
```

## ChatGPT 运行端是否还能继续

{{runtime_can_continue}}

## 继续前必须修复

{{must_fix_before_continuing}}

## 风险

手动粘贴完成并通过回读校验前，不要把这个 Course Pack 视为已同步成功。
