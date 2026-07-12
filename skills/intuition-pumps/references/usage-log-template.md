# Usage Log Template

本文件属于 `ISSUE-007`。它定义推荐记录模板和轻量日志规则，不记录完整推理过程。

## 默认规则

- 默认不写日志。
- 用户明确说“记录、复盘、沉淀、写下来”时才记录。
- 只记录推荐表面和用户可见反馈。
- 不记录隐私信息、完整推理链、凭据、未脱敏日志或无关上下文。

## 记录字段

```json
{
  "timestamp": "",
  "mode": "menu | progress | point | self_rescue | learn",
  "problem_summary": "",
  "recommended_tools": [
    {
      "slot": "most_relevant",
      "tool_id": "",
      "short_command": "",
      "family": "",
      "reason": "",
      "card_status": "complete | missing | incomplete"
    }
  ],
  "final_used_tool": "",
  "user_feedback": "useful | mixed | not_useful | no_feedback",
  "notes": ""
}
```

## 可复制记录块

当运行环境不适合写入日志文件时，输出：

```text
推荐记录
- 时间：
- 模式：
- 问题简述：
- 推荐工具：
- 最终使用：
- 用户反馈：
- 备注：
```

## 后续升级用途

这些记录只用于观察路由是否塌缩，例如：

- 高频工具是否长期霸榜。
- `low_frequency_explorer` 是否真的带来不同工具。
- 用户最终是否总是放弃某类推荐。
- 哪些问题类型需要更强的路由规则。

如果发现塌缩，开后续升级 issue；不要在当前工具卡 issue 中顺手改路由器。
