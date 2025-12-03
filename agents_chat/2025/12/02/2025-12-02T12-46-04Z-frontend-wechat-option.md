---
id: 2025-12-02T12-46-04Z-frontend-wechat-option
date: 2025-12-02T12:46:04Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, endpoints, wechat]
related_paths:
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
  - frontend/app/systems/[bid]/endpoints/new/page.tsx
  - frontend/app/messages/new/page.tsx
summary: "为系统端点配置界面补充微信渠道选项并优化适配器选择"
---

## User original prompt and requirements
- 现在界面配置上没有微信的选项

## Background and goals
- 系统端点配置页缺少微信渠道可选项，用户无法在 UI 里直接选择微信（公众号）适配器。
- 目标：在编辑/配置界面暴露微信渠道选项，并提供提示默认值。

## Changes
- 在 frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx 增加 channel 作为 transport 选项，预设 `channel.wechat_official_account` 适配器。
- 为适配器输入增加按传输类型过滤的 datalist，包含 http/邮件/飞书/微信等候选，切换传输类型时若当前适配器不匹配则默认设为首个候选。
- 渠道类型时 URL 标签改用 API 地址文案，并给出微信 API 的 placeholder。
- 在 frontend/app/systems/[bid]/endpoints/new/page.tsx 同步 adapter 预设列表（含 mailgun/sendgrid/微信）及 channel 的 API 地址占位符，切换 transport 时自动选择合适的默认适配器。
- 新建端点页的适配器下拉允许在任意 transport 下看到微信适配器，选择微信时自动切换到 channel，避免漏选。
- 在 frontend/app/messages/new/page.tsx 增加 WeChat 模板消息的「快速模板」按钮，一键填充 schema 与示例数据，便于创建微信消息定义。

## Outcome and impact
- 端点编辑页现在可以直接选择微信渠道，减少手动输入错误。
- 现有端点仍可保留原有适配器值；新切换到 channel 时会自动填入微信默认值。
- 新建端点时也能直接选择微信渠道并获得正确的占位提示。
- 消息定义页可直接套用微信模板消息示例，降低手动配置成本。

## Next steps (TODO)
- 增加端到端校验，确保 channel 类型配置完整后再保存。

## Linked commits/PRs
- 尚未提交 commit
