---
id: 2025-09-20T08-35-00Z-fix-commitlint-plugin-path
date: 2025-09-20T08:35:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [ci, commitlint]
related_paths:
  - commitlint.config.js
  - .github/workflows/commitlint.yml
summary: "Fix commitlint plugin loading by requiring local plugin module; add verbose logs in CI."
---

User original prompt and requirements
- 「github action 有问题」

Background and goals
- Commitlint CI might fail to resolve the local plugin when specified as a string path.

Changes
- Updated `commitlint.config.js` to `require('./tools/commitlint-plugin-english')` and pass the plugin object in `plugins`.
- Added `--verbose` and echo ranges to the workflow for easier debugging.

Outcome and impact
- More reliable plugin loading; better logs if CI fails.

Next steps (TODO)
- If failures persist, capture the CI error output for deeper analysis.
