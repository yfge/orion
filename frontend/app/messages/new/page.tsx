"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { RjsfForm } from "@/components/jsonschema/RjsfForm";
import { validateSchema } from "@/lib/api";
import { createMessageDef } from "@/lib/api";
import { useI18n } from "@/i18n/provider";

export default function NewMessagePage() {
  const { t } = useI18n();
  const router = useRouter();
  const [name, setName] = useState("");
  const [type, setType] = useState("text");
  const [schemaText, setSchemaText] = useState(
    '{\n  "msg_type": "text",\n  "content": { "text": "${text}" }\n}',
  );
  const [status, setStatus] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [sampleDataText, setSampleDataText] = useState(
    '{\n  "text": "你好 Orion"\n}',
  );
  const [previewValue, setPreviewValue] = useState<any>({});
  const [validateResult, setValidateResult] = useState<string | null>(null);
  const [schemaError, setSchemaError] = useState<string | null>(null);
  const [sampleError, setSampleError] = useState<string | null>(null);
  const [parsedSchema, setParsedSchema] = useState<any>({});
  const [parsedSample, setParsedSample] = useState<any>({});
  const [missingRequired, setMissingRequired] = useState<string[]>([]);

  const quickPresets = [
    {
      key: "wechat_template",
      label: "WeChat 模板-URL",
      type: "template",
      schema: `{
  "channel": "wechat_official_account",
  "touser": "\${openid}",
  "template_id": "\${template_id}",
  "data": {
    "first": { "value": "\${title}" },
    "remark": { "value": "\${remark}" }
  },
  "link": {
    "type": "url",
    "url": "\${link_url}"
  },
  "language": "zh_CN"
}`,
      sample: `{
  "openid": "openid-123",
  "template_id": "TM00015",
  "title": "支付成功",
  "remark": "感谢使用 Orion",
  "link_url": "https://example.com/order/123"
}`,
    },
    {
      key: "wechat_template_miniprogram",
      label: "WeChat 模板-小程序跳转",
      type: "template",
      schema: `{
  "channel": "wechat_official_account",
  "touser": "\${openid}",
  "template_id": "\${template_id}",
  "data": {
    "first": { "value": "\${title}" },
    "remark": { "value": "\${remark}" }
  },
  "link": {
    "type": "miniprogram",
    "appid": "\${mini_appid}",
    "pagepath": "\${mini_path}"
  },
  "language": "zh_CN"
}`,
      sample: `{
  "openid": "openid-123",
  "template_id": "TM00042",
  "title": "订单发货",
  "remark": "点击查看物流",
  "mini_appid": "wx1234567890",
  "mini_path": "/pages/order/detail?id=123"
}`,
    },
    {
      key: "wechat_custom_text",
      label: "WeChat 客服文本",
      type: "custom",
      schema: `{
  "channel": "wechat_official_account",
  "touser": "\${openid}",
  "msgtype": "text",
  "payload": {
    "text": { "content": "\${content}" }
  }
}`,
      sample: `{
  "openid": "openid-123",
  "content": "您好，这是客服消息"
}`,
    },
    {
      key: "wechat_custom_image",
      label: "WeChat 客服图片",
      type: "custom",
      schema: `{
  "channel": "wechat_official_account",
  "touser": "\${openid}",
  "msgtype": "image",
  "payload": {
    "image": { "media_id": "\${media_id}" }
  }
}`,
      sample: `{
  "openid": "openid-123",
  "media_id": "MEDIA_ID_FROM_WECHAT"
}`,
    },
  ];

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const schema = schemaText ? JSON.parse(schemaText) : null;
      await createMessageDef({ name, type, schema, status });
      router.push("/messages");
    } catch (e: any) {
      setError(e.message || t("messages.create.failed"));
    } finally {
      setLoading(false);
    }
  };

  function computeMissingRequired(schemaObj: any, sampleObj: any) {
    const required = Array.isArray(schemaObj?.required)
      ? schemaObj.required
      : [];
    if (required.length === 0) return [];
    if (typeof sampleObj !== "object" || sampleObj === null) return required;
    return required.filter((k: string) => sampleObj[k] === undefined);
  }

  useEffect(() => {
    try {
      const parsed = schemaText ? JSON.parse(schemaText) : {};
      setParsedSchema(parsed);
      setSchemaError(null);
    } catch (e: any) {
      setParsedSchema({});
      setSchemaError(e.message || "Schema JSON 解析失败");
    }
  }, [schemaText]);

  useEffect(() => {
    try {
      const parsed = sampleDataText ? JSON.parse(sampleDataText) : {};
      setParsedSample(parsed);
      setSampleError(null);
    } catch (e: any) {
      setParsedSample({});
      setSampleError(e.message || "示例数据解析失败");
    }
  }, [sampleDataText]);

  useEffect(() => {
    setMissingRequired(computeMissingRequired(parsedSchema, parsedSample));
  }, [parsedSchema, parsedSample]);

  const validationHints = useMemo(() => {
    const hints: string[] = [];
    if (schemaError) hints.push(`Schema错误: ${schemaError}`);
    if (sampleError) hints.push(`示例数据错误: ${sampleError}`);
    if (!schemaError && missingRequired.length > 0) {
      hints.push(`缺少必填字段: ${missingRequired.join(", ")}`);
    }
    return hints;
  }, [schemaError, sampleError, missingRequired]);

  return (
    <div className="container max-w-2xl">
      <h1 className="text-2xl font-semibold mb-4">{t("messages.new.title")}</h1>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Label htmlFor="name">{t("messages.fields.name")}</Label>
          <Input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="type">{t("messages.fields.type")}</Label>
            <select
              id="type"
              className="border rounded-md h-9 px-3 text-sm w-full"
              value={type}
              onChange={(e) => setType(e.target.value)}
            >
              <option value="text">text</option>
              <option value="markdown">markdown</option>
              <option value="template">template</option>
              <option value="custom">custom</option>
            </select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="status">{t("messages.fields.status")}</Label>
            <Input
              id="status"
              type="number"
              value={status}
              onChange={(e) => setStatus(Number(e.target.value))}
            />
          </div>
        </div>
        {quickPresets.length > 0 && (
          <div className="space-y-1">
            <Label>{t("messages.fields.schemaJson")}{` - 快速模板`}</Label>
            <div className="flex flex-wrap gap-2">
              {quickPresets.map((p) => (
                <Button
                  key={p.key}
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setType(p.type);
                    setSchemaText(p.schema);
                    setSampleDataText(p.sample);
                    setPreviewValue({});
                  }}
                >
                  {p.label}
                </Button>
              ))}
            </div>
          </div>
        )}
        <div className="space-y-1">
          <Label htmlFor="schema">{t("messages.fields.schemaJson")}</Label>
          <Textarea
            id="schema"
            className="font-mono"
            value={schemaText}
            onChange={(e) => setSchemaText(e.target.value)}
          />
          {schemaError && (
            <p className="text-xs text-red-600">Schema 解析错误: {schemaError}</p>
          )}
        </div>
        <div className="space-y-2">
          <Label>{t("messages.fields.schemaPreview")}</Label>
          <RjsfForm
            schema={parsedSchema}
            formData={previewValue}
            onChange={setPreviewValue}
          />
        </div>
        <div className="space-y-1">
          <Label htmlFor="sample">{t("messages.fields.sampleData")}</Label>
          <Textarea
            id="sample"
            className="font-mono"
            value={sampleDataText}
            onChange={(e) => setSampleDataText(e.target.value)}
          />
          {validationHints.length > 0 && (
            <p className="text-xs text-muted-foreground">
              {validationHints.join("；")}
            </p>
          )}
          <div>
            <Button
              type="button"
              variant="outline"
              onClick={async () => {
                try {
                  const res = await validateSchema({
                    schema: parsedSchema,
                    data: JSON.parse(sampleDataText),
                  });
                  setValidateResult(
                    res.valid
                      ? t("messages.validate.valid")
                      : `${t("messages.validate.invalidPrefix")} ${(
                          res.errors || []
                        )
                          .map((e: any) => e.message)
                          .join("; ")}`,
                  );
                } catch (e: any) {
                  setValidateResult(
                    e.message || t("messages.validate.exception"),
                  );
                }
              }}
            >
              {t("messages.validate.button")}
            </Button>
            {validateResult && (
              <p className="text-xs text-muted-foreground mt-1">
                {validateResult}
              </p>
            )}
          </div>
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>
            {loading ? t("common.creating") : t("common.create")}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => router.push("/messages")}
          >
            {t("common.cancel")}
          </Button>
        </div>
      </form>
    </div>
  );
}
