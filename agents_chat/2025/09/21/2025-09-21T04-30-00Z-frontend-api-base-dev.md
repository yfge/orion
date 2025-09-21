---
id: 2025-09-21T04-30-00Z-frontend-api-base-dev
date: 2025-09-21T04:30:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, dev, proxy]
related_paths:
  - frontend/lib/api.ts
  - frontend/next.config.js
summary: "Restore NEXT_PUBLIC_API_BASE_URL fallback and add Next.js /api rewrite for local dev"
---

User original prompt and requirements

- 前端 npm run dev 时，API 基地址设置不好用，需要修复。

Background and goals

- 之前浏览器端通过 `NEXT_PUBLIC_API_BASE_URL` 直连后端；近期改为同源 `/api`，需 Nginx 或 dev 代理。
- 目标：同时兼容两种开发方式。

Changes

- frontend/lib/api.ts：浏览器端 API_BASE 增加 `NEXT_PUBLIC_API_BASE_URL` 回退（若设置则使用，否则同源 `/api`）。
- frontend/next.config.js：新增 `rewrites()`；若设置 `DEV_API_PROXY` 或 `INTERNAL_API_BASE_URL`，将 `/api/:path*` 代理到后端（例如 `http://127.0.0.1:8000/api/:path*`）。

Outcome and impact

- `npm run dev` 下两种方式均可工作：
  1. 设置 `DEV_API_PROXY=http://127.0.0.1:8000`（推荐），浏览器访问同源 `/api`，由 Next dev server 代理。
  2. 不使用代理时，设置 `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`，浏览器直连。
- SSR 继续使用 `INTERNAL_API_BASE_URL`，如未设置回退到 `NEXT_PUBLIC_API_BASE_URL`。

Usage note

- 建议在 `frontend/.env.local` 配置：
  - `DEV_API_PROXY=http://127.0.0.1:8000`
  - `INTERNAL_API_BASE_URL=http://127.0.0.1:8000`
  - 可选：`NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`（若不启用代理）
