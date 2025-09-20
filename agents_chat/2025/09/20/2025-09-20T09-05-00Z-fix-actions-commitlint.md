---
id: 2025-09-20T09-05-00Z-fix-actions-commitlint
date: 2025-09-20T09:05:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [ci, commitlint]
related_paths:
  - .github/workflows/commitlint.yml
  - commitlint.config.js
  - tools/ci/check-commit-ascii.js
summary: "Stabilize CI by removing custom commitlint plugin and adding a standalone ASCII check script; keep conventional rules."
---

用户原始提示与要求
- 「先修复 GitHub Action 运行失败」

背景与目标
- 避免自定义插件在 CI 环境加载异常，保证 Conventional Commits 与英文（ASCII）标题的校验稳定可用。

变更内容
- 移除自定义 commitlint 插件；保留 Conventional Commits 规则集。
- 新增 `tools/ci/check-commit-ascii.js`：独立校验提交标题 ASCII。
- workflow 中增加对应 Node 步骤，在 PR/Push 两种触发下分别校验范围。

结果与影响
- 提高 CI 稳定性；规则等价但更易排错。

后续事项
- 如需更复杂的英文检测（不仅 ASCII），可升级为词典/语言规则；现阶段 ASCII 足够达标。
