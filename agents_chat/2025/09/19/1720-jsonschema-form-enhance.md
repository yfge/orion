---
id: 2025-09-19T17-20-00Z-orion-jsonschema-enhance
date: 2025-09-19T17:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, json-schema, ui]
related_paths:
  - frontend/components/jsonschema/Form.tsx
summary: "Enhance in-house JsonSchemaForm with object/array/oneOf/anyOf and propose adoption paths for full JSON Schema support."
---

What
- Upgraded the internal `JsonSchemaForm` to support:
  - object: nested properties、required 标识
  - array: 添加/删除项，子项渲染
  - oneOf/anyOf: 通过下拉切换变体
  - enum/boolean/number/integer/string/textarea（通过 format 或 x-ui:widget）
  - 展示 title/description，保留禁用态
- 与后端 `/api/v1/schema/validate` 保持兼容。

Why
- 当前端点配置/消息定义需要更复杂的 JSON Schema 表单时，增强的通用渲染器能覆盖更多场景，减少手写表单成本。

Options
- 若需要完整 JSON Schema 能力与本地校验：
  - 方案 A: 采用 @rjsf/core + @rjsf/validator-ajv8，定制 ShadCN 模板与 widgets。
  - 方案 B: 采用 JSON Forms（@jsonforms/core + @jsonforms/react），编写 ShadCN 风格渲染器。

Outcome
- 前端配置表单可直接渲染更复杂的 schema；为后续引入专业库打好过渡基础。

Next
- 可增加 uiSchema 支持（字段顺序/占位符/隐藏/组件映射），x-enumNames，format(date/datetime/url/email) 组件，和后端校验错误联动显示。
