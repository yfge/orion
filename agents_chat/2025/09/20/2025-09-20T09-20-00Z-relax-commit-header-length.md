---
id: 2025-09-20T09-20-00Z-relax-commit-header-length
date: 2025-09-20T09:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [process, commitlint]
related_paths:
  - commitlint.config.js
summary: "Relax commit header max length from 72 to 100 to reduce CI friction while keeping clarity."
---

用户原始提示与要求
- 「你是不是考虑把长度限制放宽点？」

背景与目标
- 72 字符是传统规范，但在实际工作中会导致较多误报/回写成本。适度放宽到 100 字符，兼顾可读性与效率。

变更内容
- `commitlint.config.js` 将 `header-max-length` 从 72 放宽至 100。

结果与影响
- 更少的提交标题长度失败，仍保持简洁的提交主题。

后续
- 若仍有明显阻碍，可进一步调整或建议将细节移入 body。
