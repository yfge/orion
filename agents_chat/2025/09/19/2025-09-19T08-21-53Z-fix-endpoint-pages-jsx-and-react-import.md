---
id: 2025-09-19T00-00-00Z-fix-endpoint-pages
date: 2025-09-19T08:21:53Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, fix]
related_paths:
  - frontend/app/systems/[bid]/endpoints/new/page.tsx
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
summary: "修复端点新建/编辑页：将“认证配置”选择块移入 JSX 返回体；修正 React.useEffect 导致的 React 未定义错误。"
---

问题
- 编译报 Expression expected/Expected ';'：因为“认证配置”块不在组件 return 内，JSX 语法错误。
- 运行时报 React is not defined：文件未导入 React/useEffect 却使用 React.useEffect。

修复
- 将“认证配置（可选）”块放置在表单中（配置 JSON 前）。
- 从 react 导入 useEffect，并使用 useEffect(...) 替代 React.useEffect(...)。

结果
- 端点新建/编辑页编译并运行通过，页面渲染正常。
