---
id: 2025-09-22T02-40-00Z-backend-i18n-tests-and-header
date: 2025-09-22T02:40:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, backend, test]
related_paths:
  - backend/app/core/i18n.py
  - backend/tests/test_i18n.py
summary: "为后端 i18n 增加 Content-Language 响应头，并补充语言协商测试"
---

## 用户原始需求与目标

- 按规范继续提交，并补全测试，确保最小可验证单元。

## 本次变更

- 中间件改造：在响应起始时注入 `Content-Language` 头，值为协商后的 locale。
- 新增测试 `backend/tests/test_i18n.py`，覆盖：
  - 默认回退 `zh-CN`；
  - `Accept-Language: en-US`；
  - 权重选择 `en;q=0.9, zh-CN;q=0.8`（语言级回退到 `en-US`）；
  - `?lang` 覆盖请求头；
  - Cookie `LANG` 覆盖请求头；
  - 不支持语言回退默认。

## 结果与影响

- 无需新增测试专用接口即可验证协商结果；生产也从 `Content-Language` 获益。

## 下一步（TODO）

1. 初始化最小 PO/键值，验证 `gettext_()` 渲染；
2. 统一异常处理处接入本地化消息与稳定 `code`。

## 关联提交/PR

- 本条目所在提交：中间件 header 注入 + 测试用例。
