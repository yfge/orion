# Orion（猎户座）通知网关

Orion 是一个面向企业场景的统一通知网关：接收业务系统的通知请求，统一路由/编排后分发到多种外部渠道（飞书、企微、微信、邮箱、短信等）。名称取自“猎户座”，寓意方向与联络，具有中控与聚合的意味。

这是一个 ai-coding & vibe coding 的工程化示范项目，强调以文档驱动、代理协作、可回溯的工程流程。

## 目标与特性（规划）
- 多渠道通知分发：飞书、企业微信、微信公众平台、邮件、短信等可插拔适配器。
- 解耦的集成方式：通过依赖注入与接口约束，做到系统无关、组件化可替换。
- 可观测与可追踪：通知全量落库、状态机管理、查询与追踪。
- 稳定性保障：重试与补偿机制（轮询任务/消息队列）、限流与熔断。
- 运维友好：配置化管理、环境隔离、灰度与演练。
- 可选前端控制台：用于渠道配置、发送策略、模板与审计。

## 技术栈（规划）
- 后端：Python 3.11 + FastAPI，Alembic 进行数据库迁移，计划接入任务系统（如 Celery/RQ/APScheduler）实现重试与定时轮询。
- 前端：Next.js + Tailwind CSS + ShadCN UI（用于管理控制台）。
- 持久化：PostgreSQL/MySQL（二选一，后续在 `backend` 中提供适配），Redis 用于队列/限流（可选）。
- 部署：Docker 容器化。

## 目录结构（当前）
- `backend/`：后端服务代码（待实现）
- `frontend/`：前端管理控制台（待实现）
- `Docker/`：容器化与部署相关（待实现）
- `agents_chat/`：AI 对话与协作日志（见“AI 协作与会话记录”）

后续将逐步完善：
- 后端项目脚手架（FastAPI 应用、配置、路由、依赖注入、适配器接口、ORM 模型、Alembic）。
- 前端项目脚手架（Next.js + Tailwind + ShadCN 基础页）。
- 文档与流程：整体架构设计文档 -> 模块设计文档 -> 以模块文档为约束实现功能。

## 本地准备（建议）
- Python 3.11
- Node.js 18+ / pnpm 或 yarn（任选其一）
- Docker（可选，用于本地或部署）
- pre-commit（可选，启用提交检查）

## 开发约定（摘要）
- 提交信息遵循 Conventional Commits（例如：`feat: add feishu adapter`）。
- 启用 pre-commit 钩子进行基础质量控制（见 `.pre-commit-config.yaml`）。
- 文档放置建议：整体架构在 `docs/architecture/`，模块文档在各模块目录下 `README.md`。
- 与 AI 对话过程落库至 `agents_chat/`，便于审计与回溯（见下）。

## 后端依赖与运行
- 建议使用 conda 环境：`conda activate py311`
- 安装后端依赖（任选其一）：
  - 仓库根目录执行：`pip install -e backend`
  - 或进入后端目录：`cd backend && pip install -e .`
- 启动后端：`uvicorn backend.app.main:app --reload`

### 代理说明文件（统一链接）
- 所有智能体说明文件统一链接（symlink）到根目录的 `AGENTS.md`：
  - `.CLAUDE.md`
  - `GEMINI.md`
  - `.cursorrules`
  - `.github/instructions/agents.instructions.md`
- 不在这些文件中重复规则，请仅在 `AGENTS.md` 维护详细约束（英文）。

## AI 协作与会话记录
- 根目录：`agents_chat/`；按日期归档：`agents_chat/YYYY/MM/DD/<timestamp>-<short-topic>.md`。
- 建议包含 YAML Frontmatter：
  - `id`、`date`、`participants`、`models`、`tags`、`related_paths`、`summary`。
- 内容侧重结论与决策点，并链回相关 PR/commit。
- 数据合规：不可写入密钥/令牌等敏感信息；如需展示，使用占位符。
- 详细约定参见 `AGENTS.md` 的“会话记录保存约定”。

## 许可
尚未设置开源许可证。如需开源将另行添加。
