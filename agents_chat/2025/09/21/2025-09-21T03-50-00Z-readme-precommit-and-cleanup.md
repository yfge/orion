---
id: 2025-09-21T03-50-00Z-readme-precommit-and-cleanup
date: 2025-09-21T03:50:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [docs, readme, pre-commit]
related_paths:
  - README.md
  - README.zh-CN.md
summary: "Update READMEs with local pre-commit guide, same-origin API note, and remove single-image section"
---

User original prompt and requirements

- “可以，更新中英readme 同时把那个为什么不用单一镜像没有的话去掉”—— 增加本地 pre-commit 校验说明，并移除“为什么不做单镜像”段落。

Background and goals

- 代码已切换前端浏览器调用为同源 `/api`；本地开发不经 Nginx 时需要开发代理。需在 README 中明确。
- 团队流程上要求提交启用 pre-commit，文档需提供快速指引。

Changes

- README.md：
  - 前端章节添加同源 `/api` 说明与本地代理建议。
  - 服务说明更新前端行为（Nginx 代理 `/api`）。
  - 新增 “Local Dev: pre-commit hooks” 小节。
  - Agents 小节补充 agents_chat 与代码变更同提交（CI 约束）。
  - 删除 “Why not a single image” 段落。
- README.zh-CN.md：
  - 同步上述改动（中文）。

Outcome and impact

- 文档与现有实现对齐；开发者更易按流程在本地启用 pre-commit；避免关于单镜像的跑题信息。

Next steps (TODO)

- 若团队需要，附上 Next.js `rewrites` 样例以便快速配置本地 `/api` 代理。
