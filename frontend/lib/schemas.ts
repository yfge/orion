export function endpointConfigSchemaFor(adapterKey?: string | null) {
  const baseHttp = {
    type: "object",
    properties: {
      method: { type: "string", enum: ["POST", "GET", "PUT", "DELETE"], title: "HTTP 方法" },
      url: { type: "string", title: "URL" },
      timeout: { type: "number", title: "超时(秒)" },
      headers: { type: "object", title: "请求头(键值)" },
    },
    required: ["url"],
  }
  if (!adapterKey) return baseHttp
  if (adapterKey.startsWith("http.feishu")) {
    return {
      type: "object",
      properties: {
        url: { type: "string", title: "Webhook URL" },
        timeout: { type: "number", title: "超时(秒)" },
        headers: { type: "object", title: "请求头(可选)" },
      },
      required: ["url"],
    }
  }
  if (adapterKey === "http.mailgun") {
    return {
      type: "object",
      properties: {
        url: { type: "string", title: "API URL", description: "如 https://api.mailgun.net/v3/<domain>/messages" },
        api_key: { type: "string", title: "API Key" },
        timeout: { type: "number", title: "超时(秒)" },
        headers: { type: "object", title: "额外请求头(可选)" },
        body_format: { type: "string", enum: ["form", "json"], title: "Body 格式", default: "form" },
      },
      required: ["url", "api_key"],
    }
  }
  return baseHttp
}

export function mappingSchemaFor(adapterKey?: string | null, messageType?: string | null) {
  if (adapterKey?.startsWith("http.feishu") && (messageType === "text" || !messageType)) {
    return {
      type: "object",
      properties: {
        text: { type: "string", title: "文本内容覆盖(可选)" },
      },
    }
  }
  if (adapterKey === "http.mailgun") {
    return {
      type: "object",
      properties: {
        from: { type: "string", title: "发件人(可选)" },
        to: { type: "string", title: "收件人(逗号分隔，可选)" },
        subject: { type: "string", title: "主题(可选)" },
        text: { type: "string", title: "纯文本正文(可选)" },
        html: { type: "string", title: "HTML 正文(可选)", format: "textarea" },
      },
    }
  }
  return { type: "object", properties: {} }
}
