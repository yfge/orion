---
id: 2025-09-21T04-20-00Z-email-mapping-form
date: 2025-09-21T04:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, email, mapping, rjsf]
related_paths:
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
  - frontend/lib/schemas.ts
summary: "Add RJSF-based mapping form for email adapters on endpoint edit page"
---

User original prompt and requirements

- 做映射表单化：将端点映射（mapping）从纯 JSON 文本改为表单（RJSF），尤其是邮件类适配器（Mailgun/SendGrid/SMTP）。

Background and goals

- 已有 `mappingSchemaFor()`（Mailgun/SendGrid/SMTP 包含 from/to/subject/text/html）。需在端点编辑页对“新增映射”集成 RJSF 表单，同时保留 JSON 高级编辑。

Changes

- frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx：
  - 引入 `mappingSchemaFor` 并新增 `newMappingObj` 状态。
  - “新增映射”区域加入 `RjsfForm`，根据当前适配器与所选消息类型生成 Schema。
  - 双向同步：表单变化写入 JSON 文本；JSON 文本修改尝试反解析回表单。
  - `onAddDispatch` 优先使用对象映射（无则回退解析 JSON）。
  - 提示：邮件适配器可设置 from/to/subject/text/html。

Outcome and impact

- 配置映射体验更友好，避免 JSON 手写错误；邮件类常见字段有表单提示。

Next steps (TODO)

- 未来可在“已有映射”列表提供编辑功能（目前仅删除）。
