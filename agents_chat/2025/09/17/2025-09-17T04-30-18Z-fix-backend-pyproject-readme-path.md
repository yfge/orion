---
id: 2025-09-17T04-30-18Z-fix-readme-path
date: 2025-09-17T04:30:18Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, packaging, bugfix]
related_paths:
  - backend/pyproject.toml
  - backend/README.md
summary: "修复 pip editable 安装失败：pyproject.readme 指向仓库外部文件导致 setuptools 拒绝访问。"
---

问题
- 在 `backend` 目录执行 `pip install -e .` 报错：`Cannot access '../README.md' (or anything outside 'backend')`。
- 原因：`backend/pyproject.toml` 的 `project.readme` 指向 `../README.md`，setuptools 在后端子包构建时禁止读取包目录之外的文件。

修复
- 将 `readme = "../README.md"` 改为 `readme = "README.md"`，使用后端内的 `backend/README.md`。

结果
- 重新执行 `pip install -e .` 应可正常解析并安装依赖与可编辑包。

备注
- 保持后端独立打包策略：依赖声明与包查找仅在 `backend/` 下进行，避免根目录外部引用。
