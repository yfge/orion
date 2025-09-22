---
id: 2025-09-22T02-20-00Z-backend-i18n-scaffold
date: 2025-09-22T02:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, backend]
related_paths:
  - backend/app/core/i18n.py
  - backend/babel.cfg
  - backend/locale/
  - scripts/i18n/extract.sh
  - scripts/i18n/update.sh
  - scripts/i18n/compile.sh
summary: "后端 i18n 脚手架（中间件、协商、pybabel 脚本骨架）"
---

## 用户原始需求与目标

- 按最小单元推进 i18n，实现后端的基础脚手架并生成 agents_chat 记录。

## 背景与目标

- 提供最小可用的后端 i18n 能力：语言协商、上下文注入、`gettext` 装载与工具脚本，后续再接入异常处理与具体消息。

## 本次变更

- 新增 `backend/app/core/i18n.py`：
  - `detect_locale`（query/cookie/Accept-Language）与 `_parse_accept_language`；
  - `ContextVar` 存储当前语言；`gettext` 装载；
  - `I18nMiddleware` 将协商结果写入上下文与 `scope.state`；
  - `gettext_()` 获取当前语言翻译（无 PO 文件时返回原始 key）。
- 新增 `backend/babel.cfg`：声明 Python/Jinja2 提取规则与扩展。
- 新增脚本：`scripts/i18n/{extract,update,compile}.sh`；
- 新增 `backend/locale/` 占位目录与子目录结构（`zh_CN`、`en_US`）。

## 关键决策与取舍

- 不接入 `main.py`，避免影响现有行为；后续单独提交中再挂载中间件。
- 先提交脚本骨架与目录，待依赖安装后再执行。

## 结果与影响

- 代码具备基本的 i18n 能力与目录结构，后续可平滑对接。

## 下一步（TODO）

1. 在 `backend/app/main.py` 中挂载 `I18nMiddleware`（独立提交）。
2. 统一异常处理与响应中使用 `gettext_()`（独立提交）。
3. 初始化示例 PO/翻译键并补充最小测试（独立提交）。

## 关联提交/PR

- 本条目所在提交：新增后端 i18n 脚手架与脚本。
