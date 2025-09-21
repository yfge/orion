---
id: 2025-09-21T03-40-00Z-pre-commit-local-setup
date: 2025-09-21T03:40:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [pre-commit, tooling, process]
related_paths:
  - .pre-commit-config.yaml
summary: "Relax Python pin for pre-commit and steps to validate locally; future commits re-enable pre-commit"
---

User original prompt and requirements

- 中文：本地配置验证 pre-commit，以后提交要启用 pre-commit（不再使用 --no-verify）。

Background and goals

- 之前在本机缺少 Python 3.11 导致 pre-commit 安装 hook 环境失败。为降低门槛，将 Python 版本从固定 3.11 放宽为系统 `python3`，以适配 3.11/3.12/3.13。

Changes

- `.pre-commit-config.yaml`：
  - `default_language_version.python` 从 `python3.11` 改为 `python3`。
  - Black hook 的 `language_version` 从 `python3.11` 改为 `python3`。

Outcome and impact

- 开发者无需特定安装 3.11 即可运行 pre-commit。Ruff/Black/Isort/基础钩子在 3.11+ 均可用。

Local verification steps

1. 安装依赖：`pip install pre-commit`，并确保本机有 Node.js（用于 commitlint）。
2. 安装钩子：`pre-commit install` 和 `pre-commit install --hook-type commit-msg`。
3. 手动校验：`pre-commit run -a`（首次运行会安装环境，可能较慢）。
4. 之后正常 `git commit`，不要使用 `--no-verify`。

Notes

- CI 仍会执行 commitlint 和 agents_chat 耦合检查；本地失败建议先运行 `pre-commit run -a` 修复后再提交。
