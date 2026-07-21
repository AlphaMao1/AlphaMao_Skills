# 手动写回模板

当 ChatGPT 可以读取 Notion、但不能写入时，使用本页。每次只生成本讲发生变化的块，不整页覆盖。

## Runtime Snapshot

```markdown
### 手动写回｜{{session_id}}
- 当前节点：{{current_node}}
- 本讲结果：{{progress_result}}
- 下一讲入口：{{next_lesson_entry}}
- 更新时间：{{updated_at}}
```

## Course_State & Profile

```markdown
### 进度证据｜{{session_id}}
- 节点：{{node_id}}
- 观察到的能力证据：{{evidence}}
- 状态变化：{{state_change}}
- 仍待验证：{{open_check}}
```

## Sessions

```markdown
### Session {{session_id}}｜{{session_date}}
- 课程推进问题：{{progression_question}}
- 用户回答摘要：{{user_answer_summary}}
- 采用策略：{{strategy}}
- 讲解 / 纠偏摘要：{{teaching_summary}}
- 推进结果：{{progress_result}}
- 下一步：{{next_step}}
```

## Notes Inbox

```markdown
### 候选笔记｜{{knowledge_object}}
- 来源节点：{{node_id}}
- 核心问题：{{core_question}}
- 知识结构：{{knowledge_structure}}
- 用户学习证据：{{learning_evidence}}
- 下一次教学提示：{{next_teaching_hint}}
- 状态：待审核
```

粘贴完成后重新读取相关页面，确认内容位于正确课程和正确页面。
