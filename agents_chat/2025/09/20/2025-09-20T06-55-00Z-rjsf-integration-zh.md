---
id: 2025-09-20T06-55-00Z-orion-rjsf-integration-zh
date: 2025-09-20T06:55:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [前端, JSON Schema, RJSF, UI]
related_paths:
  - frontend/components/jsonschema/RjsfForm.tsx
  - frontend/app/messages/new/page.tsx
  - frontend/app/messages/[bid]/page.tsx
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
  - frontend/package.json
  - frontend/pnpm-lock.yaml
summary: "集成 @rjsf/core + ajv8，提供 ShadCN 风格表单渲染，替换消息与端点配置处的 Schema 表单。"
---

内容
- 新增 `RjsfForm` 封装，基于 `@rjsf/core` + `@rjsf/validator-ajv8`，提供 ShadCN 风格的 widgets（文本/数字/选择/布尔）与 templates（对象/数组）。
- 消息定义页面（新建与编辑）的 Schema 预览切换为 RJSF，支持 Ajv 校验。
- 端点编辑页增加“基于适配器 Schema 的配置表单”（RJSF 渲染），并保留“高级模式：配置 JSON”文本框，二者双向同步。
- 更新 `package.json` 依赖并提交了 pnpm lockfile 变更。

原因
- 需要更完整的 JSON Schema 表单能力与本地校验，同时统一 UI 风格，降低后续复杂表单开发成本。

结果
- 控制台可通过 Schema 渲染更复杂的配置与预览表单，具备 Ajv 校验能力。
- 为后续接入 uiSchema、更多组件（date/datetime/url/email、x-enumNames、密码框、KV 编辑器等）打好基础。

注意
- 请在 `frontend/` 目录安装依赖：`npm install --legacy-peer-deps`（如遇到 peer 冲突）。
- 如遇 SSR 相关问题，可将 RJSF 组件以 `ssr: false` 的动态导入方式使用。

后续
- 增加 uiSchema 支持（顺序、隐藏、占位符、组件映射、帮助文本、分组）。
- 丰富 widgets，并与后端 `/api/v1/schema/validate` 的错误结果联动到具体字段上。
