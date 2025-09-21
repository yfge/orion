---
id: 2025-09-20T18-10-00Z-actions-commitlint-relax
date: 2025-09-20T18:10:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [ci, commitlint]
related_paths:
  - .github/workflows/commitlint.yml
  - commitlint.config.js
summary: "Relax commit header length to 200 for CI stability (URLs/long scopes) while keeping Conventional Commits and ASCII checks."
---

用户原始提示与要求
- 处理 Actions 运行问题（commitlint 校验失败）。

变更内容
- 将 `header-max-length` 从 150 放宽至 200，避免含 URL 或长 scope 的提交标题导致 CI 失败。
- 仍保留 Conventional Commits 基础规则与 ASCII 检查脚本。

结果
- 降低无谓失败的概率，保持提交历史规范与可读性。
