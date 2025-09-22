---
id: 2025-09-22T03-35-00Z-frontend-i18n-extract-systems
date: 2025-09-22T03:35:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/systems/page.tsx
  - frontend/app/systems/new/page.tsx
  - frontend/app/systems/[bid]/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "抽取 Systems 模块（列表/新建/编辑）文案至 i18n，并统一采用 useI18n 渲染"
---

## 变更内容

- Systems 列表与新建/编辑页全部用户可见文本抽取到 messages：
  - 列表：标题、搜索、按钮、表头与空态、操作文案；
  - 新建/编辑：表单字段、按钮文案、加载/错误提示、端点列表区块；
- 通用 common 键补充：搜索、创建/保存/删除/取消、加载与错误信息；
- 页面组件接入 `useI18n` 并替换硬编码文案。

## 影响

- Systems 模块完全支持中英文切换；字符串集中管理，便于翻译与审计。

## 下一步

- 继续抽取 Messages/Records/Auth 模块文案，逐步覆盖整个前端；
- 后续切换到 next-intl 与 [locale] 路由以完善 SEO 与访问路径本地化。
