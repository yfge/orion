---
id: 2025-09-21T06-20-00Z-help-markdown-renderer
date: 2025-09-21T06:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, docs, markdown]
related_paths:
  - frontend/components/Markdown.tsx
  - frontend/app/help/[slug]/page.tsx
  - frontend/tailwind.config.ts
  - frontend/app/globals.css
  - frontend/package.json
summary: "Switch Help pages to ReactMarkdown + remark/rehype + Prism code highlighting; enable Tailwind Typography"
---

Goal

- 让帮助文档渲染更美观、人性化，支持 GFM/标题锚点/外链与代码高亮。

Changes

- 依赖（package.json）：react-markdown、remark-gfm、rehype-slug、rehype-autolink-headings、rehype-external-links、rehype-prism-plus；dev: @tailwindcss/typography。
- Tailwind：开启 Typography 插件，帮助页容器使用 `prose` 与暗色 `dark:prose-invert`。
- 组件：`components/Markdown.tsx` 封装 ReactMarkdown + 插件（GFM/slug/auto-link/external/prism）。
- 页面：`/help/[slug]` 改用 <Markdown source={md}/>；删除旧的 simpleMarkdownToHtml。
- 样式：在 globals.css 增加 prose 内代码块与行内 code 的美化样式。

Notes

- 需要在前端项目安装新增依赖（`npm i` 或 `pnpm i`）。
- 若需目录（TOC）、自定义提示块，后续可加 remark-toc 或改用 MDX。
