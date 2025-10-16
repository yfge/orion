# 微信公众号渠道可观测性与报警手册

## 指标总览
- `orion_wechat_send_attempts_total{result,app_id}`：发送尝试次数，`result`=success/error/retry。
- `orion_wechat_send_latency_seconds{app_id}`：发送耗时直方图（秒）。
- `orion_wechat_callback_events_total{event_type,status}`：回调事件量，`status`=success/failure.

## 日志规范
- 发送成功日志 `wechat.template.send.success`，包含 `message_bid`, `vendor_msg_id`, `app_id`, `latency_ms`。
- 发送失败日志 `wechat.template.send.failure`，包含 `errcode`, `errmsg`, `retry_scheduled`。
- 回调日志 `wechat.callback.received`，包含 `event_type`, `vendor_msg_id`, `status_text`, `error_code`。
- 所有日志附带 `trace_id`（若有）、`request_id`（API 侧）、`environment`。

## Alert 规则
- **Access Token 失败**：`orion_wechat_send_attempts_total{result="error",errcode="40001"}` 在 5 分钟内 >= 3 次 → P1。
- **发送失败率**：5 分钟窗口失败率 > 5% → P1；>2% → P2。
- **回调缺失**：连续 10 分钟无 `status=success` 的回调 → P2。
- **延迟异常**：`orion_wechat_send_latency_seconds` 95 分位 > 3 秒持续 15 分钟 → P2。

## 监控面板建议
- 总览：发送成功率、失败率、平均/95th 延迟。
- 错误明细：按 `errcode` TopN、按模板 ID 分布。
- 回调流水：最近 100 条事件及状态。

## 运维操作
1. 新功能上线前验证指标是否注册；Prometheus scrape 存在 `orion_wechat_send_attempts_total`。
2. 如遇报警：
   - 检查 Access Token 有效性（Vault、配置中心）。
   - 查看发送日志与回调日志中的 trace_id，定位请求闭环。
   - 若属供应商限流（45009 等），协调业务降流并调整重试策略。
3. 事故复盘：将指标截图、日志示例附加至事件工单，并更新本手册。

## 参考
- Prometheus 报警模板位于 `infra/alerts/wechat-official-account.yml`（待补充）。
- 日志字段定义在 `backend/app/observability/README.md`（待补充）。
