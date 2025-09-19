---
id: 2025-09-19T00-00-00Z-jsonschema-support
date: 2025-09-19T09:37:06Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [jsonschema, ui, validate]
related_paths:
  - backend/app/api/v1/schema.py
  - backend/app/api/v1/router.py
  - frontend/components/jsonschema/Form.tsx
  - frontend/app/messages/new/page.tsx
  - frontend/app/messages/[bid]/page.tsx
  - frontend/lib/api.ts
summary: "前后端增加 JSON Schema 支持：后端提供 /schema/validate；前端新增基础 JSON Schema 表单与示例数据校验，提升易用性。"
---

内容
- 后端：POST /api/v1/schema/validate（若安装 jsonschema 则严格校验，否则放行），用于前端示例数据校验。
- 前端：JsonSchemaForm（基础渲染 string/number/boolean/enum），在消息定义新建/编辑页集成预览与校验按钮。
- 交互：编辑 schema 时可立即预览生成的表单；输入示例数据后点击“校验”调用后端校验 API，展示结果。
