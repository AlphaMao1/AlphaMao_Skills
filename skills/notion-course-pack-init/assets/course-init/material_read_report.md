# 材料读取报告｜{{course_title}}

## 摘要

- Course ID：{{course_id}}
- 正式范围：{{formal_scope}}
- 创建时间：{{created_at}}
- 状态：{{status}}

## 用户提供的材料

| Source ID | 标题 | 角色 | 类型 | 位置 | 用户声明范围 |
|---|---|---|---|---|---|
| {{source_id}} | {{title}} | {{role}} | {{type}} | {{location}} | {{declared_scope}} |

## Codex 已完整读取的材料

| Source ID | 读取状态 | 已读范围 | SHA-256 来源指纹 | 方法 / 工具 | 证据备注 |
|---|---|---|---|---|---|
| {{source_id}} | {{read_status}} | {{read_range}} | {{source_fingerprint}} | {{method}} | {{evidence_note}} |

## 不在本次范围内

{{out_of_scope_materials}}

## 读取失败 / 阻塞材料

{{blocked_materials}}

## Course_Map 来源证据

| Node ID | 节点标题 | Material ID | 支撑来源范围 | 备注 |
|---|---|---|---|---|
| {{node_id}} | {{node_title}} | {{material_ids}} | {{source_ranges}} | {{notes}} |

## 补桥节点

| Node ID | 增加原因 | 相关来源 |
|---|---|---|
| {{node_id}} | {{why_added}} | {{related_sources}} |

## 覆盖声明

只有列在“Codex 已完整读取的材料”里的来源，才能被视为已覆盖。只读取元数据、目录或索引，不算内容覆盖。

同一份证据必须同步写入 `manifest.json.material_coverage`：材料清单、声明范围、读取状态、读取范围、来源指纹、节点映射缺一不可。正文报告与 manifest 不一致时，初始化失败。
