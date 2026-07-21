# Notion 托管区域包装模板

创建页面正文时，把下面结构写成一个独立的 Notion toggle 或 callout。标题必须是精确的 `{{managed_region_id}}`，其余页面区块不得放进这个容器。

```text
托管区域｜{{managed_region_id}}

managed_by: notion-course-pack-init
course_id: {{course_id}}
page_role: {{page_role}}
region_id: {{managed_region_id}}
update_policy: replace-managed-region-only
source_fingerprint: {{source_fingerprint}}

{{managed_content_blocks}}
```

`source_fingerprint` 是对 `{{managed_content_blocks}}` 规范化后计算的 SHA-256，不包含上面的元数据行，避免指纹自引用。更新时只替换这个容器；容器外的用户区块必须保留。
