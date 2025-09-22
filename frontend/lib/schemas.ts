export function endpointConfigSchemaFor(
  adapterKey?: string | null,
  t?: (k: string) => string,
) {
  const T = (k: string, fallback: string) => (t ? t(k) : fallback);
  const baseHttp = {
    type: "object",
    properties: {
      method: {
        type: "string",
        enum: ["POST", "GET", "PUT", "DELETE"],
        title: "HTTP 方法",
      },
      url: { type: "string", title: "URL" },
      timeout: {
        type: "number",
        title: T("schemas.common.timeout", "超时(秒)"),
      },
      headers: {
        type: "object",
        title: T("schemas.http.headers", "请求头(键值)"),
      },
    },
    required: ["url"],
  };
  if (!adapterKey) return baseHttp;
  if (adapterKey.startsWith("http.feishu")) {
    return {
      type: "object",
      properties: {
        url: {
          type: "string",
          title: T("schemas.http.webhookUrl", "Webhook URL"),
        },
        timeout: {
          type: "number",
          title: T("schemas.common.timeout", "超时(秒)"),
        },
        headers: {
          type: "object",
          title: T("schemas.http.headersOptional", "请求头(可选)"),
        },
      },
      required: ["url"],
    };
  }
  if (adapterKey === "http.mailgun") {
    return {
      type: "object",
      properties: {
        url: {
          type: "string",
          title: "API URL",
          description: "如 https://api.mailgun.net/v3/<domain>/messages",
        },
        api_key: { type: "string", title: "API Key" },
        from: {
          type: "string",
          title: T("schemas.email.defaultFrom", "默认发件人(可选)"),
        },
        to: {
          type: "string",
          title: T("schemas.email.defaultTo", "默认收件人(逗号分隔，可选)"),
        },
        timeout: {
          type: "number",
          title: T("schemas.common.timeout", "超时(秒)"),
        },
        headers: {
          type: "object",
          title: T("schemas.http.extraHeadersOptional", "额外请求头(可选)"),
        },
        body_format: {
          type: "string",
          enum: ["form", "json"],
          title: T("schemas.http.bodyFormat", "Body 格式"),
          default: "form",
        },
      },
      required: ["url", "api_key"],
    };
  }
  if (adapterKey === "http.sendgrid") {
    return {
      type: "object",
      properties: {
        url: {
          type: "string",
          title: "API URL",
          description: "通常为 https://api.sendgrid.com/v3/mail/send",
        },
        api_key: { type: "string", title: "API Key" },
        from: {
          type: "string",
          title: T("schemas.email.defaultFrom", "默认发件人(可选)"),
        },
        to: {
          type: "string",
          title: T("schemas.email.defaultToSimple", "默认收件人(可选)"),
        },
        timeout: {
          type: "number",
          title: T("schemas.common.timeout", "超时(秒)"),
        },
        headers: {
          type: "object",
          title: T("schemas.http.extraHeadersOptional", "额外请求头(可选)"),
        },
        body_format: {
          type: "string",
          enum: ["json"],
          title: T("schemas.http.bodyFormat", "Body 格式"),
          default: "json",
        },
      },
      required: ["url", "api_key"],
    };
  }
  if (adapterKey.startsWith("smtp.")) {
    return {
      type: "object",
      properties: {
        host: { type: "string", title: T("schemas.smtp.host", "SMTP 主机") },
        port: {
          type: "number",
          title: T("schemas.smtp.portOptional", "端口(可选)"),
        },
        use_tls: {
          type: "boolean",
          title: T("schemas.smtp.useTLS", "使用 STARTTLS"),
        },
        use_ssl: {
          type: "boolean",
          title: T("schemas.smtp.useSSL", "使用 SSL"),
        },
        username: {
          type: "string",
          title: T("schemas.smtp.usernameOptional", "用户名(可选)"),
        },
        password: {
          type: "string",
          title: T("schemas.smtp.passwordOptional", "密码(可选)"),
        },
        from: {
          type: "string",
          title: T("schemas.email.defaultFrom", "默认发件人(可选)"),
        },
        to: {
          type: "string",
          title: T("schemas.email.defaultTo", "默认收件人(逗号分隔，可选)"),
        },
        timeout: {
          type: "number",
          title: T("schemas.common.timeout", "超时(秒)"),
        },
      },
      required: ["host"],
    };
  }
  return baseHttp;
}

export function mappingSchemaFor(
  adapterKey?: string | null,
  messageType?: string | null,
  t?: (k: string) => string,
) {
  const T = (k: string, fallback: string) => (t ? t(k) : fallback);
  if (
    adapterKey?.startsWith("http.feishu") &&
    (messageType === "text" || !messageType)
  ) {
    return {
      type: "object",
      properties: {
        text: {
          type: "string",
          title: T("schemas.feishu.textOverride", "文本内容覆盖(可选)"),
        },
      },
    };
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
    };
  }
  if (adapterKey === "http.sendgrid" || adapterKey?.startsWith("smtp.")) {
    return {
      type: "object",
      properties: {
        from: {
          type: "string",
          title: T("schemas.email.fromOptional", "发件人(可选)"),
        },
        to: {
          type: "string",
          title: T(
            "schemas.email.toOptionalDelimited",
            "收件人(逗号分隔，可选)",
          ),
        },
        subject: {
          type: "string",
          title: T("schemas.email.subjectOptional", "主题(可选)"),
        },
        text: {
          type: "string",
          title: T("schemas.email.textOptional", "纯文本正文(可选)"),
        },
        html: {
          type: "string",
          title: T("schemas.email.htmlOptional", "HTML 正文(可选)"),
          format: "textarea",
        },
      },
    };
  }
  return { type: "object", properties: {} };
}
