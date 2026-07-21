# Sessions｜{{course_title}}

## 使用规则

- 每讲结束并经用户确认后写入一条 session。
- Session 记录摘要、判断和推进结果，不写课堂逐字稿。
- Learning Events 不单独建页；需要记录时写入本页对应 session。

## 当前上课记录

{{sessions_index_or_empty_state}}

## 上课记录模板

### Session {{session_id}}｜{{session_date}}

- Course ID：{{course_id}}
- Node ID：{{node_id}}
- 本讲目标：{{session_goal}}
- 课程推进问题：{{progression_question}}
- 用户回答摘要：{{user_answer_summary}}
- 判断结果：{{judgment}}
- 错误类型：{{error_type}}
- 采用策略：{{strategy}}
- 本讲讲解 / 纠偏摘要：{{teaching_summary}}
- 推进结果：{{progress_result}}
- 是否完成当前节点：{{node_completion_status}}
- 新增或更新的复习事项：{{review_events}}
- 新增或更新的候选主题笔记：{{candidate_notes}}
- 下一步：{{next_step}}
- 写回摘要：{{writeback_summary}}
- 状态证据：{{evidence}}

## 策略说明

- `skip`：用户已达到节点标准，跳过或压缩。
- `compress`：短解释后推进。
- `teach`：正常讲解当前知识点。
- `bridge`：补最小必要前置，再回主线。
- `branch`：回答支线问题，不改变 Course_Map。
