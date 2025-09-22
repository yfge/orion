% i18n 总览（Overview）

本页定义 Orion 的多语言（i18n）目标、范围、策略与流程，指导前后端与模板一致实现。

## 目标

- 提供 `zh-CN` 与 `en-US` 的一致体验，可扩展更多语言。
- 统一协商策略、键名规范、回退策略与可观测字段。
- 确保实现可审计与自动化（CI/pre-commit）。

## 范围

- 前端（Next.js）：文案、路由、日期/数字格式化、SEO（hreflang）。
- 后端（FastAPI）：错误/提示本地化，`Accept-Language` 协商，中间件注入。
- 模板（Jinja2）：通知文案与占位符插值、复数/选择规则。
- 文档与可观测：日志/指标/追踪携带语言字段。

## 语言与标签

- 采用 BCP47 标签：`zh-CN`、`en-US`。
- 默认语言：`zh-CN`。

## 协商策略（优先级）

1. `?lang=<locale>`
2. 认证用户的首选语言
3. Cookie `LANG`
4. `Accept-Language` 请求头
5. 系统默认 `zh-CN`

## 键名规范

- 形如：`<scope>.<feature>.<action>.<qualifier>`，如 `auth.login.failed.invalid_password`。
- 统一命名参数插值；避免语言硬编码拼接。

## 回退策略

- 缺失键回退到默认语言并告警；展示稳定技术码 + 可本地化文案。

## 前端实现建议

- 采用 `next-intl`；`frontend/messages/{locale}.json` 存放文案；
- `middleware.ts` 实现 locale 前缀与自动跳转；
- `useTranslations` 使用；`Intl.*` 处理日期/数字。

## 后端实现建议

- `backend/app/core/i18n.py`：中间件 + `gettext` 装载；
- 统一异常处理处使用 `_('key')` 获取文案（保留稳定 `code`）。

## 模板

- Jinja2 启用 `i18n` 扩展；支持 `{% trans %}` 与 ICU 复数规则。

## 工具链

- 提取/更新/编译：`pybabel` 脚本（`scripts/i18n/*.sh`）。
- pre-commit：缺失键检查与格式化；CI 展示翻译差异。

## 验收

- 前后端主路径可按语言切换；错误消息可本地化；模板渲染正确；日志/指标带语言标签。
