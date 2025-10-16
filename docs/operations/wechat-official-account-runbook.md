# 微信公众号渠道运行手册

## 场景
- 适用于 Orion 通过 FastAPI 接入的微信公众号模板消息发送、回调处理。
- 涵盖发送前检查、验证步骤、故障处理、回滚策略。

## 上线前检查
1. 确认 Vault/K8s Secret 中的 `APP_ID`、`APP_SECRET`、`TOKEN` 已同步，并与公众平台配置一致。
2. 在 `docs/architecture/channels/wechat-official-account.md` 对照功能范围和限制，确保配置项齐全。
3. 运行 `pytest tests/test_wechat_channel.py`，保证单元测试通过。
4. 手动调用 `POST /api/v1/notifications/wechat/template`（使用 sandbox OpenID）验证返回 `success`。

## 发送流程验证
1. 触发实际发送（小流量），观察 API 返回值及 `send_records` 表写入。
2. 通过 Prometheus 查看 `orion_wechat_send_attempts_total` 与 `orion_wechat_send_latency_seconds` 是否有数据。
3. 在公众平台后台确认消息是否送达；如未送达，检查回调日志 `wechat.callback.received`。

## 常见故障与处理
| 现象 | 排查步骤 | 处理建议 |
| --- | --- | --- |
| API 返回 401 | 检查 `X-API-Key` 是否正确，或 `PUBLIC_API_KEY` 未配置 | 更新 API Key 或将 `PUBLIC_API_KEY=None` 仅用于测试 |
| 返回 `WechatAPIError(errcode=40001)` | Access Token 失效 | 在 Vault 轮换凭证，调用 `invalidate` 后重试 |
| `errcode=45009` 频繁 | 供应商限流 | 调低发送速率，查看 `_schedule_retry` 策略并手工重试 |
| 无回调 | 公众平台未命中回调域名或签名失败 | 检查公网地址、Token/EncodingAESKey，一次性验证 `GET` 请求 |

## 回滚策略
1. 若版本上线后失败率飙升，立刻切换至前一版本镜像/容器，并恢复旧配置。
2. 通过 `repo.mark_token_deleted` 清空缓存，防止旧 token 残留。
3. 记录事故于 agents_chat，更新 runbook 注意事项。

## 附录
- 指标/报警：参见 `docs/operations/wechat-official-account-observability.md`。
- 凭证管理：参见 `docs/operations/wechat-official-account-credentials.md`。
- 架构说明：`docs/architecture/channels/wechat-official-account.md`。
