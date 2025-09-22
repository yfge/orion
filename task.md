% 多语言（i18n）支持实施任务

> 目标：为 Orion 建立端到端的多语言能力（前端/后端/模板/文档/运维），确保可观测、可运维、可审计与高可用；初始语言包含 `zh-CN`、`en-US`，后续可扩展 `zh-TW`、`ja-JP` 等。

## 背景与范围

- 网关对外与对内均需稳定的多语言体验：
  - 前端（Next.js）界面与路由本地化、日期/数字/货币格式化、SEO hreflang。
  - 后端（FastAPI）错误与提示消息本地化、`Accept-Language` 协商、审计事件的语言标注与非破坏性记录。
  - 通知模板（Email/SMS/IM）本地化与占位符插值、复数/性别/选择规则（ICU MessageFormat）。
  - 文档与运维：可观测（语言标签、度量指标）、日志与追踪中携带语言上下文。

## 技术选型与原则

- 前端：Next.js App Router + `next-intl`（建议）或 `next-i18next`；统一使用 ICU MessageFormat；静态与动态消息分离。
- 后端：`Babel` + `gettext` 工作流（`.po/.mo`）或 `babel + jinja2` 的 `i18n` 扩展；Starlette/FastAPI 中间件进行语言协商与上下文注入。
- 模板：Jinja2 + `i18n` 扩展；每个渠道保留 locale 版本（或在同一模板中使用 `{% trans %}`）。
- 数据：业务数据保持“原文 + locale 标注”；不可变审计事件使用“原始技术码 + 可选展示文案/locale”。
- 约束：
  - 默认语言 `zh-CN`，统一 BCP47 语言标签（如 `en-US`）。
  - 支持 `Accept-Language`、`?lang=`、用户配置、Cookie 多策略协商，明确优先级。
  - 不在日志中强制翻译技术细节，面向用户的提示才翻译。

## 目录与代码布局（不立即实现，仅约定）

- 前端（Next.js）
  - `frontend/i18n/` 配置与工具；`frontend/messages/{locale}.json` 文案。
  - 路由国际化：`middleware.ts` + `[locale]/` 路由段，默认重定向至 `zh-CN`。
  - 组件使用 `useTranslations`；日期/数字使用 `Intl.*` 或 `@formatjs/intl`。
- 后端（FastAPI）
  - `backend/app/core/i18n.py`：语言协商、中间件、`gettext` 装载与 `_()` 包装。
  - `backend/locale/<lang>/LC_MESSAGES/orion.po|mo`：消息目录。
  - 错误/响应消息统一走消息表，API 始终返回稳定 `code`，`message` 可本地化。
- 模板（渠道）
  - `backend/app/services/templates/`：每渠道模板按 `/<channel>/<template_key>/<locale>.jinja2` 或单模板+`{% trans %}`。

## 分阶段实施计划（里程碑）

1. 基座与规范（M1）

- 定语言清单与默认、协商优先级、文件组织结构与命名规范。
- 选型落定（Next.js: `next-intl`；FastAPI: `Babel/gettext`）。
- 加入基础依赖、脚手架与示例；建立占位样例文案与提取流程。

2. 前端路由与文案（M2）

- 引入 `next-intl`，实现 locale 前缀路由与中间件自动跳转。
- 抽取公共 UI 文案（导航、表单、表格、状态）至 `messages/*.json`。
- 日期/数字格式化封装（`lib/format.ts`），RTL 准备（样式策略）。
- SEO：`hreflang`、`canonical`、`robots` 校验。

3. 后端错误与响应本地化（M3）

- `Accept-Language` 中间件与上下文（支持 `?lang`/Cookie/用户设置覆盖）。
- 错误与响应消息统一走 `_('key')`；保留稳定 `code` 与 `details`。
- `pybabel` 提取/编译流程：`scripts/i18n/*.sh`（提取→更新→翻译→编译）。

4. 通知模板与渠道适配（M4）

- Jinja2 启用 `i18n` 扩展，支持 ICU/复数；模板按语言版本管理。
- 渠道适配器传入语言与时区；回退策略与占位符校验。

5. 文档与可观测（M5）

- 使用指南与开发手册：新增 `docs/i18n/`。
- 监控：在日志/metrics/traces 中附带 `lang` 标签；SLA 报表支持按语言维度。

6. 测试与验收（M6）

- 单测：语言协商、中间件、缺失键回退、模板渲染与复数。
- 端到端：前端路由与 SEO、后端响应消息、渠道发送路径。

## 详细任务清单（可拆分为 Issue/PR）

- 规范与文档
  - 写 `docs/i18n/overview.md`（目标、范围、协商策略、文件组织、翻译流程）。
  - 在 `AGENTS.md` 追加与 i18n 相关的工程约束与 commit 示例（如需）。
- 前端
  - 安装与配置 `next-intl`；新增 `middleware.ts` 实现 locale prefix。
  - 规划 `frontend/messages/`；抽取现有中文文案到 `zh-CN.json`；生成 `en-US.json` 草稿。
  - `lib/i18n.ts` 封装；组件改造使用 `useTranslations`；日期/数字工具。
  - SEO：`generateMetadata` 中注入 `alternates.languages`。
  - 检查路由/链接/导航在多语言下的稳定性与回退。
- 后端
  - 新增 `core/i18n.py`：
    - `detect_locale(request)`：解析 `Accept-Language`、`?lang`、Cookie、用户设定。
    - `I18nMiddleware`：把 `locale` 存入 `request.state/ContextVar`；
    - `gettext` 初始化：`translations = gettext.translation('orion', localedir, languages=[...], fallback=True)`；
    - `_ = translations.gettext` 封装；公共 `translate(key, **kwargs)`。
  - 在统一异常处理与响应构造处接入 `_()`。
  - `scripts/i18n/extract.sh`、`update.sh`、`compile.sh`：`pybabel extract/update/compile`。
- 模板/渠道
  - 启用 Jinja2 `i18n` 扩展；模板支持 `{% trans %}` 与参数插值。
  - 规范模板命名与语言文件；适配器传递 `locale` 与 `tz`。
  - 验证 Feishu/WeCom/Email/SMS 的语言切换与回退策略。
- 工具与 CI
  - pre-commit：检测缺失 key、未使用 key（前端可用 `i18next-parser` 或自建脚本）。
  - CI：在 PR 中展示翻译差异报告与缺失清单（后续接入 Crowdin/Weblate）。
- 测试
  - 单测覆盖：协商优先级、缺失键回退、复数/选择规则、模板渲染。
  - 前端 e2e：路由/SEO/hreflang；后端 e2e：按不同 `Accept-Language` 返回本地化消息。

## 协商优先级（建议顺序，高到低）

1. `?lang=<locale>` 显式参数
2. 认证用户的首选语言（用户配置）
3. Cookie `LANG`
4. `Accept-Language` 请求头
5. 系统默认 `zh-CN`

## 文案/键名规范

- 键名：`<scope>.<feature>.<action>.<qualifier>`，如 `auth.login.failed.invalid_password`。
- 插值：统一使用命名参数；前后端保持一致。
- 复数：使用 ICU 复数规则；避免在英文中硬编码拼接。

## 回退与缺失策略

- 缺失键：回退到默认语言，并在日志发出 `warning` 带 `lang` 与 `key`。
- 运行时切换：允许用户在 UI 改变语言，持久化到 Cookie/用户配置。
- 版本变更：新增/更名键需在 PR 描述与 `agents_chat` 中明确说明。

## 可观测与审计

- 日志字段：`lang`、`user_locale`、`template_locale`、`negotiated_by`（参数/头/Cookie/默认）。
- 指标：每语言的错误率/延迟/模板渲染失败计数。
- 审计：保留技术码与参数；展示层按请求语言渲染。

## 验收标准（Definition of Done）

- 前端：
  - 主要页面支持 `zh-CN` 与 `en-US` 切换；路由与 SEO 正确；日期/数字随语言变化。
  - 缺失键回退与告警可见；RTL 开关基础验证通过。
- 后端：
  - 通过 `Accept-Language`/`?lang` 能返回本地化错误与提示；
  - `.po/.mo` 构建链路通过；单测覆盖协商逻辑与回退；
  - 渠道模板能按语言渲染并正确插值；
- 文档：`docs/i18n/*` 完整说明流程，开发者可据此新增语言。
- 可观测：日志/指标包含语言标签；在看板可按语言筛选。

## 风险与缓解

- 键膨胀与漂移：通过 pre-commit 与 CI 生成缺失报告；约束命名规范。
- 模板变体爆炸：优先使用 `{% trans %}`；确需分支时最小化差异。
- 性能：编译缓存 `.mo` 与模板；避免运行时频繁装载；中间件轻量。
- 一致性：前后端共享术语表与键名；在 `agents_chat` 中记录关键变更。

## 时间与产出（建议）

- M1：1–2 天 → 基座与样例、文档初稿
- M2：2–3 天 → 前端路由与主要文案抽取
- M3：2 天 → 后端错误/响应本地化与脚本
- M4：2–3 天 → 模板/渠道适配与校验
- M5：1 天 → 文档与可观测
- M6：1–2 天 → 测试与验收

## 相关路径（计划落位，不代表已存在）

- 前端：`frontend/i18n/*`、`frontend/messages/*.json`、`frontend/middleware.ts`
- 后端：`backend/app/core/i18n.py`、`backend/locale/*`、`scripts/i18n/*`
- 模板：`backend/app/services/templates/*`
- 文档：`docs/i18n/*`

---

下一步建议：

- 我来补充 `docs/i18n/overview.md` 与最小代码脚手架（前后端各 1 个示例），并在后续 PR 中分阶段完成上述里程碑。
