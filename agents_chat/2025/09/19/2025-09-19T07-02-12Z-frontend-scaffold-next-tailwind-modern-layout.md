---
id: 2025-09-19T07-02-12Z-frontend-scaffold
date: 2025-09-19T07:02:12Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, nextjs, tailwind, ui, scaffold]
related_paths:
  - frontend/
summary: "搭建前端脚手架：Next.js + Tailwind + 主题切换，现代美观的基础布局（导航栏 + 侧边栏 + 卡片总览）。"
---

内容
- 配置：`package.json`、`next.config.mjs`、`tsconfig.json`、`postcss.config.mjs`、`tailwind.config.ts`、`app/globals.css`。
- 布局：`app/layout.tsx`（Navbar + Sidebar + 内容区），`app/page.tsx`（总览卡片）。
- 组件：`components/theme-provider.tsx`、`components/theme-toggle.tsx`、`components/navbar.tsx`、`components/sidebar.tsx`、`components/ui/{button,card,cn}.ts(x)`。
- 风格：CSS 变量 + Tailwind 扩展，支持深浅色切换（next-themes）。

使用
- `cd frontend`
- 安装依赖：`pnpm i` 或 `npm i` 或 `yarn`
- 开发：`pnpm dev`（默认 3000 端口）

备注
- 当前环境无网络未安装依赖；在本机联网后执行安装即可。
- 后续可通过 shadcn/ui 增量引入组件（已具备基础样式与工具）。
