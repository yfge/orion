---
id: 2025-09-21T06-40-00Z-compose-nginx-host-port
date: 2025-09-21T06:40:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [devops, docker, nginx]
related_paths:
  - Docker/nginx.conf
summary: "Fix Nginx proxy headers to include port in Host for correct absolute URLs (avoid http://localhost without :8080)"
---

Issue

- 在 Docker Compose 下访问 8080 时，部分 307/重定向或绝对 URL 变成 `http://localhost/...`（缺少端口）。
  根因：Nginx 将 `Host` 透传 `$host`，该变量不包含端口，FastAPI 生成的 Location 等绝对 URL 用了该 Host。

Change

- `Docker/nginx.conf`：
  - `proxy_set_header Host $http_host;`（包含端口）
  - 新增 `X-Forwarded-Host $host:$server_port`（可供上游框架识别端口）
  - 前端与后端 location 均应用以上设置。

Outcome

- 上游生成绝对 URL（如重定向 Location）将包含端口 `:8080`，浏览器不再落到 `http://localhost/...`。
