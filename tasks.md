# 微信公众号消息发送集成任务清单

## 0. 需求梳理与方案确认
- 明确通知网关中公众号场景（事务通知、模板消息、自定义消息）的业务需求与成功判定标准。
- 调研现有渠道（如飞书/企业微信）集成模式，澄清可复用的抽象与需要新增的领域模型。
- 产出架构与设计文档初稿，冻结依赖、接口、认证策略。

## 1. 平台准备与凭证管理
- 在微信公众平台创建/确认服务号，开通模板消息或客服消息能力。
- 获取 AppID、AppSecret、消息模板 ID、消息体示例等，并录入到安全配置（vault/env）。
- 设计凭证滚动策略与运维手册（密钥更新、账号权限、风控限制）。

## 2. 配置与基础设施支持
- 在 `backend/app/core/config.py` 增加公众号渠道配置项（凭证、token 缓存 TTL、API 域名）。
- 追加速率限制、重试、断路器策略的默认参数，区分 4XX/5XX。
- 更新 secrets 模板与基础设施文档（K8s Secret / Docker `.env`）。

## 3. 域模型与存储设计
- 在 `backend/app/domain/notifications` 扩展微信公众号消息实体（模板 ID、数据字段、跳转链接）。
- 设计并迁移存储：凭证缓存（Access Token）、消息发送记录、回执事件；更新 Alembic migration。
- 定义领域事件：发送请求、供应商回执、失败重试、放弃策略。

## 4. 适配器与外部 API 集成
- 在 `backend/app/adapters/wechat_official_account/` 实现请求签名、Access Token 获取与缓存。
- 封装模板消息发送 API、客服消息发送 API，处理错误码与异常映射。
- 集成微信推送回调处理（服务器配置 URL、Token 验证、消息解密）。

## 5. 服务编排与业务流程
- 在 `backend/app/services/gateway` 中注册公众号渠道，支持路由与渠道能力声明。
- 实现消息体模板渲染器（字段校验、默认值、富文本/小程序跳转）。
- 支持重试/补发/撤回场景，结合任务队列（`backend/tasks/`）更新调度策略。

## 6. API 与 Schemas 扩展
- 在 `backend/app/schemas/` 新增公众号消息请求/响应模型，校验 message data。
- 在 `backend/app/api/v1/notifications` 暴露创建、查询、重试接口参数。
- 更新 API 文档（OpenAPI、docs/architecture）的示例与调用说明。

## 7. 可观测性与运营支持
- 增加渠道级别 metrics（发送成功率、失败原因、延迟），暴露 Prometheus 指标。
- 建立结构化日志与追踪标记（trace_id、msg_id、vendor_msgid）。
- 配置报警：凭证过期、连续失败、QPS 告警、回调异常。

## 8. 测试与验证
- 编写单元测试：适配器（API 调用、token 缓存）、服务层（重试策略、模板填充）。
- 编写集成测试：Mock 微信 API / 使用 sandbox 账号验证流程。
- 创建端到端校验脚本或 manual checklist（从 API 调用到公众号消息送达）。

## 9. 文档与交付
- 在 `docs/architecture/channels/wechat-official-account.md` 输出完整设计与运维指南。
- 补充 runbook：常见故障、排查步骤、回滚策略。
- 更新 `agents_chat/` 日志，沉淀实现过程与决策记录。

## 10. 发布与后续保障
- 配置 CI/CD 覆盖新测试，确保 agents_chat 钩子通过。
- 和运营对接灰度策略，确认配额、限流阈值，执行灰度发布。
- 监控首轮发送数据，建立事后回顾机制与下一步优化计划。

## 11. 微信易用性提升（前端）
- [x] 消息定义：补充快捷模板按钮（客服文本/图片、模板+小程序跳转等），自动填充 schema 与示例。
- [x] 消息定义：添加实时预览与必填校验，标注缺失字段/变量。
- [x] 映射向导：在 dispatch 配置页提供微信字段映射示例，一键填充后再微调。
- [x] 发送测试：在端点或消息页提供微信发送测试入口（OpenID + 简单文本），展示 errcode/返回体。
