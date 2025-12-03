"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { RjsfForm } from "@/components/jsonschema/RjsfForm";
import {
  getMessageDef,
  updateMessageDef,
  deleteMessageDef,
  listAllEndpoints,
  listDispatches,
  createDispatch,
  updateDispatch,
  deleteDispatch,
  validateSchema,
} from "@/lib/api";
import { useI18n } from "@/i18n/provider";

export default function EditMessagePage() {
  const { t } = useI18n();
  const params = useParams<{ bid: string }>();
  const bid = params?.bid as string;
  const router = useRouter();

  const [name, setName] = useState("");
  const [type, setType] = useState("text");
  const [schemaText, setSchemaText] = useState("{}");
  const [status, setStatus] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [endpoints, setEndpoints] = useState<any[]>([]);
  const [dispatches, setDispatches] = useState<any[]>([]);
  const [newEndpointBid, setNewEndpointBid] = useState("");
  const [newMappingText, setNewMappingText] = useState("{}");
  const [newEnabled, setNewEnabled] = useState(true);
  const [previewValue, setPreviewValue] = useState<any>({});
  const [sampleDataText, setSampleDataText] = useState(
    '{\n  "text": "你好 Orion"\n}',
  );
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

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getMessageDef(bid);
        setName(data.name || "");
        setType(data.type || "text");
        setSchemaText(JSON.stringify(data.schema || {}, null, 2));
        setStatus(typeof data.status === "number" ? data.status : 0);
        const eps = await listAllEndpoints({ limit: 500, offset: 0 });
        setEndpoints(eps.items || []);
        const dps = await listDispatches(bid);
        setDispatches(dps.items || []);
      } catch (e: any) {
        setError(e.message || t("common.failedLoad"));
      } finally {
        setLoading(false);
      }
    };
    if (bid) load();
  }, [bid]);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const schema = schemaText ? JSON.parse(schemaText) : null;
      await updateMessageDef(bid, { name, type, schema, status });
      router.push("/messages");
    } catch (e: any) {
      setError(e.message || t("messages.save.failed"));
    } finally {
      setLoading(false);
    }
  };

  const onDelete = async () => {
    if (!confirm(t("messages.delete.confirm"))) return;
    try {
      await deleteMessageDef(bid);
      router.push("/messages");
    } catch (e: any) {
      alert(e.message || t("common.failedDelete"));
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

  const onAddDispatch = async () => {
    try {
      const mapping = newMappingText ? JSON.parse(newMappingText) : null;
      await createDispatch(bid, {
        endpoint_bid: newEndpointBid,
        mapping,
        enabled: newEnabled,
      });
      const dps = await listDispatches(bid);
      setDispatches(dps.items || []);
      setNewMappingText("{}");
      setNewEndpointBid("");
      setNewEnabled(true);
    } catch (e: any) {
      alert(e.message || "新增映射失败");
    }
  };

  const onDeleteDispatch = async (dispatchBid: string) => {
    if (!confirm("确认删除映射？")) return;
    try {
      await deleteDispatch(dispatchBid);
      const dps = await listDispatches(bid);
      setDispatches(dps.items || []);
    } catch (e: any) {
      alert(e.message || "删除失败");
    }
  };

  if (loading && !name)
    return <div className="container">{t("common.loading")}</div>;

  return (
    <div className="container max-w-2xl">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">{t("messages.edit.title")}</h1>
        <Button
          variant="outline"
          onClick={onDelete}
          className="text-red-600 border-red-600"
        >
          {t("common.delete")}
        </Button>
      </div>
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
            {loading ? t("common.saving") : t("common.save")}
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
      <div className="space-y-3 mt-6">
        <h2 className="text-xl font-semibold">
          {t("messages.dispatch.title")}
        </h2>
        <div className="rounded-lg border p-3 space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <Label htmlFor="endpoint">
                {t("messages.dispatch.selectEndpoint")}
              </Label>
              <select
                id="endpoint"
                className="border rounded-md h-9 px-3 text-sm w-full"
                value={newEndpointBid}
                onChange={(e) => setNewEndpointBid(e.target.value)}
              >
                <option value="">
                  {t("messages.dispatch.selectEndpointPlaceholder")}
                </option>
                {endpoints.map((ep) => (
                  <option
                    key={ep.notification_api_bid}
                    value={ep.notification_api_bid}
                  >
                    {ep.name} ({ep.business_system_bid})
                  </option>
                ))}
              </select>
            </div>
            <div className="space-y-1">
              <Label htmlFor="enabled">{t("messages.dispatch.enabled")}</Label>
              <select
                id="enabled"
                className="border rounded-md h-9 px-3 text-sm w-full"
                value={newEnabled ? "1" : "0"}
                onChange={(e) => setNewEnabled(e.target.value === "1")}
              >
                <option value="1">{t("common.yes")}</option>
                <option value="0">{t("common.no")}</option>
              </select>
            </div>
          </div>
          <div className="space-y-1">
            <Label htmlFor="mapping">
              {t("messages.dispatch.mappingJsonOptional")}
            </Label>
            <Textarea
              id="mapping"
              className="font-mono"
              value={newMappingText}
              onChange={(e) => setNewMappingText(e.target.value)}
            />
          </div>
          <div>
            <Button
              type="button"
              onClick={onAddDispatch}
              disabled={!newEndpointBid}
            >
              {t("messages.dispatch.addMapping")}
            </Button>
          </div>
        </div>

        <div className="overflow-x-auto rounded-lg border">
          <table className="min-w-full text-sm">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-3 py-2 text-left">
                  {t("messages.dispatch.table.endpoint")}
                </th>
                <th className="px-3 py-2 text-left">
                  {t("messages.dispatch.table.system")}
                </th>
                <th className="px-3 py-2 text-left">
                  {t("messages.dispatch.table.enabled")}
                </th>
                <th className="px-3 py-2 text-left">
                  {t("messages.dispatch.table.actions")}
                </th>
              </tr>
            </thead>
            <tbody>
              {dispatches.map((d) => (
                <tr key={d.message_dispatch_bid} className="border-t">
                  <td className="px-3 py-2">
                    {d.endpoint_name || d.endpoint_bid}
                  </td>
                  <td className="px-3 py-2 text-muted-foreground">
                    {d.business_system_bid || "—"}
                  </td>
                  <td className="px-3 py-2">
                    {d.enabled ? t("common.yes") : t("common.no")}
                  </td>
                  <td className="px-3 py-2">
                    <button
                      onClick={() => onDeleteDispatch(d.message_dispatch_bid)}
                      className="text-red-600 hover:underline"
                    >
                      {t("common.delete")}
                    </button>
                  </td>
                </tr>
              ))}
              {dispatches.length === 0 && (
                <tr>
                  <td className="px-3 py-4 text-muted-foreground" colSpan={4}>
                    {t("messages.dispatch.none")}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
