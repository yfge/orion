---
id: 2025-12-03T04-55-48Z-wechat-mapping-schema
date: 2025-12-03T04:55:48Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, wechat, mapping]
related_paths:
- frontend/lib/schemas.ts
- frontend/messages/en-US.json
- frontend/messages/zh-CN.json
- frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
summary: "完善微信模板映射 schema，表单自动展示必填字段"
---

## User original prompt and requirements
- 反馈：在发送测试时，选择对应模板后没有加载对应字段，映射表单是写死的，JSON Schema 没生效。

## Background and goals
- 原先 mappingSchemaFor 对微信只提供 link 配置，缺少 touser/template_id/data 等字段，导致 RJSF 无法展示可填项。
- 目标：为微信模板映射提供完整 schema，包含必填项和模板数据结构描述。

## Changes
- frontend/lib/schemas.ts：微信映射 schema 增加 touser、template_id、data（支持任意模板字段 value/color），并保留 link 配置。
- frontend/messages/en-US.json / zh-CN.json：补充对应文案键。
- frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx：派发映射的 RJSF 表单改为直接使用所选消息定义的 schema，避免出现无关字段。
- 映射表单若消息定义存的是模板（非标准 JSON Schema），前端会自动推导为 JSON Schema，再渲染字段。

## Outcome and impact
- 选择微信渠道时，映射表单将展示 OpenID、模板ID、模板数据等字段，用户可直接填写或映射变量，减少空白/写死问题。
- 派发映射表单随消息定义变化而变化，不再出现多余字段。

## Next steps (TODO)
- 若需要按消息定义动态生成具体模板字段，可在后端/前端传入 message schema 再细化 data 的键约束；当前为通用键值模式。

## Linked commits/PRs
- 未提交 commit
