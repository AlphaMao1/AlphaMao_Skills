# Sources & Coverage｜{{course_title}}

## 材料范围

- Course ID：{{course_id}}
- 正式初始化范围：{{formal_scope}}
- 不在本次范围内：{{out_of_scope}}
- 材料读取报告：{{material_read_report_path}}

## 覆盖状态定义

- `fully_read`：Codex 已完整读取本次范围内材料。
- `out_of_scope`：本次初始化明确排除。
- `blocked`：需要但无法读取。
- `metadata_only`：只用于书目信息、目录或背景，不算内容覆盖。
- `bridge_node`：为教学效率新增的桥接节点，不直接对应原材料章节。

## 来源清单

| Source ID | 标题 | 类型 | 位置 / 范围 | 读取状态 | 对应节点 |
|---|---|---|---|---|---|
| {{source_id}} | {{source_title}} | {{source_type}} | {{source_location}} | {{read_status}} | {{mapped_nodes}} |

## 源材料结构

{{source_structure}}

## 来源到 Course_Map

| Source ID | 来源范围 | 支撑节点 | 覆盖说明 |
|---|---|---|---|
| {{source_id}} | {{source_range}} | {{node_ids}} | {{coverage_note}} |

## Course_Map 到来源

| Node ID | 节点主题 | 支撑来源 | 是否桥接节点 |
|---|---|---|---|
| {{node_id}} | {{node_topic}} | {{supporting_sources}} | {{is_bridge_node}} |

## 覆盖盲区

{{coverage_gaps}}

## 用户指定必须覆盖的内容

{{user_mandated_coverage}}

## 可跳读或合并处理的内容

{{skippable_or_merged_materials}}

## 使用边界

本页是覆盖审计，不是教学顺序。教学顺序由 Course_Map 决定。日常上课不更新本页；只有课程范围改变或材料映射错误时由 Codex 处理。
