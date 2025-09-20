---
id: 2025-09-20T07-00-00Z-agents-chat-rename-convention
date: 2025-09-20T07:00:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [流程, 记录, 规范]
related_paths:
  - agents_chat/
summary: "统一 agents_chat 命名：采用 YYYY-MM-DDTHH-MM-SSZ-<topic>.md 格式，保持年/月/日目录。"
---

内容
- 将非规范命名条目重命名为标准格式：`YYYY-MM-DDTHH-MM-SSZ-<topic>.md`。
- 仍按目录组织：`agents_chat/YYYY/MM/DD/`。
- 已重命名示例：
  - 2025/09/19/1700-send-records-ui.md → 2025/09/19/2025-09-19T17-00-00Z-send-records-ui.md
  - 2025/09/19/1720-jsonschema-form-enhance.md → 2025/09/19/2025-09-19T17-20-00Z-jsonschema-form-enhance.md
  - 2025/09/20/0650-rjsf-integration.md → 2025/09/20/2025-09-20T06-50-00Z-rjsf-integration.md
  - 2025/09/20/0655-rjsf-integration-zh.md → 2025/09/20/2025-09-20T06-55-00Z-rjsf-integration-zh.md

原因
- 与既有记录保持一致，便于时间序排序与检索。

结果
- agents_chat 下所有条目现已遵循统一命名规范。

后续
- 严格执行“每次提交必须有 agents_chat 记录”的流程，使用上述命名格式。
