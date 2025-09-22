# Orion（猎户座）通知网关

[English README](README.md)

Orion 是一个面向企业场景的统一通知网关：接收业务系统的通知请求，统一路由/编排后分发到多种外部渠道（飞书、企微、微信、邮箱、短信、消息队列等）。这是一个 ai‑coding & vibe‑coding 的工程化示范项目，强调以文档驱动、代理协作、可回溯（agents_chat）。

## 当前能力

- 消息定义（MessageDefinition）：以 JSON Schema + `${var}` 占位渲染消息体
- 端点（Endpoint）：支持 HTTP/MQ，`adapter_key` + `config` 描述第三方
- 派发映射（Dispatch）：消息 → 多端点的映射（双向管理，BID 作为关联）
- 通知 API：`POST /api/v1/notify` 传入消息名或 BID + data 即可自动派发
- 飞书闭环：端点编辑页可直接“测试发送”到飞书机器人 webhook
- 认证配置（AuthProfile）：增删改查已具备（后续与 Sender 深度集成）
- 控制台前端：系统/端点/消息/映射全流程管理

## 多语言（i18n）

- 语言：简体中文（`zh-CN`）与英文（`en-US`）。
- 文案来源：`frontend/messages/{locale}.json`；全站通过轻量 Provider 提供 `t(key)`。
- 语言检测：前端中间件按 `Accept-Language` 初次设置 `LANG` Cookie；导航栏支持语言切换（更新 `LANG` 并刷新）。
- 后端协商：FastAPI 中间件按优先级协商（`?lang` → `Cookie LANG` → `Accept-Language` → 默认 `zh-CN`），响应注入 `Content-Language` 头。
- 帮助中心：优先加载 `frontend/help/<locale>/*.md`，若缺失回退到 `frontend/help/*.md`；Markdown 标题请使用 `#`。
- 如何扩展：
  - 新增 `frontend/messages/<new-locale>.json` 并更新 `SUPPORTED_LOCALES`；
  - 在 `frontend/help/<new-locale>/` 下提供对应 Markdown 文档；
  - 后端通过 Babel/`pybabel` 在 `backend/locale/<lang>/LC_MESSAGES` 增加翻译。
- 路线：后续迁移至 `next-intl` 与 `[locale]/` 前缀路由，并完善 SEO 的 `hreflang/alternates`。

## 技术栈

- 后端：Python 3.11、FastAPI、SQLAlchemy、Alembic、httpx
- 前端：Next.js 14（app 目录）+ Tailwind
- 数据库：SQLite（开发）/ MySQL（支持）；后续可接入 Redis/MQ

## 目录结构

- `backend/`：后端服务（API、服务、仓储、ORM、测试）
- `frontend/`：管理控制台（系统、端点、消息、映射）
- `agents_chat/`：AI 协作日志

## 后端使用

- 环境（推荐）：`conda activate py311`
- 安装：仓库根执行 `pip install -e backend`（或 `cd backend && pip install -e .`）
- 运行：`uvicorn backend.app.main:app --reload`
- 数据库：`.env` 设置 `ORION_DATABASE_URL`（MySQL 示例）
  - `mysql+pymysql://root:Pa88word@127.0.0.1:13306/orion?charset=utf8mb4`
  - 迁移：`scripts/migrate.sh upgrade head`
- CORS：`.env` 配置 `ORION_CORS_ORIGINS=*` 或 JSON 数组；默认放通本地 3000/3001
- 文档：Swagger `/docs`，ReDoc `/redoc`

### 通知 API（公开）

- 鉴权：`X-API-Key` 或 HTTP Basic（`api:<key>`）
  - 在后端 `.env`/compose 环境设置 `ORION_PUBLIC_API_KEY`
  - Basic 示例：`Authorization: Basic` + base64(`api:<key>`)
- 请求：`POST /api/v1/notify`
  - 方式一（按名称）：`{"message_name":"simple-text","data":{"text":"你好"}}`
  - 方式二（按 BID）：`{"message_definition_bid":"...","data":{...}}`
- 响应：`{"results":[{"dispatch_bid","endpoint_bid","status_code","body"}]}`

- 生成随机 Key（预览）：`POST /api/v1/notify/keys/preview` 返回一个随机建议，请将其配置到后端的 `ORION_PUBLIC_API_KEY`。

### 飞书快速联调

1. 新建端点：transport=http，adapter_key=http.feishu_bot，endpoint_url=飞书机器人 webhook
2. 新建消息定义：schema `{ "msg_type":"text","content":{"text":"${text}"} }`
3. 在“消息定义”或“端点”页建立派发映射
4. 调用 `/api/v1/notify` 传入 `{text:"..."}`，或在端点编辑页用“测试发送”

### 邮件通道（Mailgun、SendGrid、SMTP）

- Mailgun
  - 新建端点：transport=http，adapter_key=http.mailgun
  - 配置：`url=https://api.mailgun.net/v3/<domain>/messages`，`api_key=<key>`，可选 `from`/`to`
  - 端点编辑页“测试发送”：默认主题为“Orion Test”，正文取输入文本
- SendGrid
  - 新建端点：transport=http，adapter_key=http.sendgrid
  - 配置：`url=https://api.sendgrid.com/v3/mail/send`，`api_key=<key>`，可选 `from`/`to`
  - 测试发送将按 SendGrid JSON 结构构造 from/to/subject/content
- SMTP
  - 新建端点：transport=smtp，adapter_key=smtp.generic
  - 配置：`host`，可选 `port`、`use_tls`/`use_ssl`、`username`/`password`、默认 `from`/`to`
  - 测试发送会发送一封主题为“Orion Test”的邮件，正文为输入文本；mapping 也支持 `subject`、`text`、`html`、`from`、`to`

## 前端使用

- 安装：`cd frontend && npm i`（或 pnpm/yarn）
- 启动：`npm run dev`，浏览器访问 http://localhost:3000
- 说明：浏览器侧走同源的 `/api`；若本地未使用 Docker/Nginx，需要在 Next.js 开发环境配置一个将 `/api` 代理到 `http://127.0.0.1:8000` 的重写（rewrites）；或直接使用下方 Docker Compose（已由 Nginx 代理到后端）。
- 操作：系统/端点/消息管理；在消息或端点页面配置映射

### 前端 i18n 提示

- 通过导航栏选择语言；当前语言保存在 `LANG` Cookie。
- 页面文案改造：使用 `t('...')` 替换硬编码，并在 `frontend/messages/{locale}.json` 添加键值。
- 帮助文档：在 `frontend/help/en-US/*`（或其他语言目录）放置本地化 Markdown；首行用 `#` 标题。

## 使用 Docker 一键启动

- 预置要求：已安装 Docker Desktop（含 Compose）。
- 启动（首次建议构建镜像）：
  - 构建镜像：`docker compose build`
  - 后台运行：`docker compose up -d`
  - 查看状态：`docker compose ps`
  - 查看日志：`docker compose logs -f --tail=200 backend`（或 `frontend`/`mysql`/`nginx`）

### 访问地址

- 控制台（Nginx 统一入口）：http://localhost:8080
- 后端 API 入口（经 Nginx 反代）：http://localhost:8080/api/
- 健康检查：`/healthz` 或 `/api/v1/ping`

### Compose 服务说明（简要）

- `mysql`：MySQL 8（账号 `orion`/`orionpass`，库 `orion`，root 密码 `orionroot`），数据挂载到卷 `mysql_data`。
- `backend`：FastAPI 应用，自动执行 Alembic 迁移（`alembic upgrade head`），再启动 Uvicorn。
  - 关键环境：`ORION_DATABASE_URL=mysql+pymysql://orion:orionpass@mysql:3306/orion?charset=utf8mb4`、`ORION_PUBLIC_API_KEY` 等。
- `frontend`：Next.js 控制台；浏览器请求命中同源 `/api`，由 Nginx 反代至后端。
- `nginx`：反向代理 `/` 到前端，`/api/` 到后端。

### 常见问题

- 初次启动 MySQL 需要时间初始化，若后端迁移时数据库尚未就绪可重试：`docker compose restart backend`。
- Compose 关于 `version` 的提示为警告，可忽略；计划后续清理。
- 若需覆盖前端 API 基础地址：在 `docker-compose.yml` 的 `frontend.build.args` 与 `frontend.environment` 同步修改 `NEXT_PUBLIC_API_BASE_URL`。

## 本地开发：pre-commit 钩子

- 安装：`pip install pre-commit`，并保证有 Node.js（用于 commitlint）。
- 安装钩子：`pre-commit install` 与 `pre-commit install --hook-type commit-msg`。
- 本地验证：`pre-commit run -a`。
- 正常提交时不要使用 `--no-verify`；CI 会校验 Conventional Commits 与 agents_chat 绑定。

## 测试

- 安装：`pip install -e backend[test]`
- 运行（在 backend/）：`pytest`

## Agents 与文档

- 智能体说明文件均链接到 `AGENTS.md`（单一事实来源）
- 协作日志：`agents_chat/YYYY/MM/DD/<timestamp>-<topic>.md`。凡修改代码的提交，需在同一次提交中包含相应 agents_chat（CI 强制）；必要时可在提交正文加入 `skip agents-chat` 作为例外。
- 架构文档：`docs/architecture/overview.md`

## 规划

- API Key 多租户管理、调用统计与配额、签名/防重放
- 模板与映射表单化（JSON Schema 驱动）
- 发送记录落库、异步重试、限流与熔断
- 更多适配器（企微、微信、邮件、MQ 等）

## 许可

暂未设置，后续补充。
