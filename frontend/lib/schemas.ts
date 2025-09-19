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
  return { type: "object", properties: {} }
}

