"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  getEndpoint,
  updateEndpoint,
  deleteEndpoint,
  listAuthProfiles,
  sendTestToEndpoint,
  listDispatchesByEndpoint,
  listMessageDefs,
  createDispatchForEndpoint,
  deleteDispatch,
} from "@/lib/api";
import { endpointConfigSchemaFor } from "@/lib/schemas";
import { RjsfForm } from "@/components/jsonschema/RjsfForm";

export default function EditEndpointPage() {
  const params = useParams<{ bid: string; endpointBid: string }>();
  const systemBid = params?.bid as string;
  const endpointBid = params?.endpointBid as string;
  const router = useRouter();

  const [name, setName] = useState("");
  const [transport, setTransport] = useState("");
  const [adapterKey, setAdapterKey] = useState("");
  const [endpointUrl, setEndpointUrl] = useState("");
  const [configText, setConfigText] = useState("{}");
  const [configObj, setConfigObj] = useState<any>({});
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [authProfiles, setAuthProfiles] = useState<any[]>([]);
  const [authProfileBid, setAuthProfileBid] = useState("");
  const [testText, setTestText] = useState("");
  const [testResult, setTestResult] = useState<string | null>(null);
  const [messageDefs, setMessageDefs] = useState<any[]>([]);
  const [endpointDispatches, setEndpointDispatches] = useState<any[]>([]);
  const [newMsgBid, setNewMsgBid] = useState("");
  const [newMappingText, setNewMappingText] = useState("{}");
  const [newEnabled, setNewEnabled] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getEndpoint(endpointBid);
        setName(data.name || "");
        setTransport(data.transport || "");
        setAdapterKey(data.adapter_key || "");
        setEndpointUrl(data.endpoint_url || "");
        const cfgObj = data.config || {};
        setConfigText(JSON.stringify(cfgObj, null, 2));
        setConfigObj(cfgObj);
        setAuthProfileBid(data.auth_profile_bid || "");
      } catch (err: any) {
        setError(err.message || "加载失败");
      } finally {
        setLoading(false);
      }
    };
    if (endpointBid) load();
    (async () => {
      try {
        const res = await listAuthProfiles({ limit: 100, offset: 0 });
        setAuthProfiles(res.items || []);
      } catch {}
    })();
    (async () => {
      try {
        const msgs = await listMessageDefs({ limit: 500, offset: 0 });
        setMessageDefs(msgs.items || []);
      } catch {}
    })();
    (async () => {
      try {
        const dps = await listDispatchesByEndpoint(endpointBid);
        setEndpointDispatches(dps.items || []);
      } catch {}
    })();
  }, [endpointBid]);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const cfg = configObj ?? (configText ? JSON.parse(configText) : null);
      await updateEndpoint(endpointBid, {
        name,
        transport,
        adapter_key: adapterKey || null,
        endpoint_url: endpointUrl || null,
        config: cfg,
        auth_profile_bid: authProfileBid || null,
      });
      router.push(`/systems/${systemBid}`);
    } catch (err: any) {
      setError(err.message || "保存失败，检查配置 JSON 是否有效");
    } finally {
      setLoading(false);
    }
  };

  const onDelete = async () => {
    if (!confirm("确认删除该端点？")) return;
    try {
      await deleteEndpoint(endpointBid);
      router.push(`/systems/${systemBid}`);
    } catch (err: any) {
      alert(err.message || "删除失败");
    }
  };

  const onSendTest = async () => {
    setTestResult(null);
    try {
      const res = await sendTestToEndpoint(
        endpointBid,
        testText || "Hello from Orion",
      );
      setTestResult(
        `HTTP ${res.status_code} ${
          typeof res.body === "string" ? res.body : JSON.stringify(res.body)
        }`,
      );
    } catch (e: any) {
      setTestResult(e.message || "发送失败");
    }
  };

  const onAddDispatch = async () => {
    try {
      const mapping = newMappingText ? JSON.parse(newMappingText) : null;
      await createDispatchForEndpoint(endpointBid, {
        message_definition_bid: newMsgBid,
        mapping,
        enabled: newEnabled,
      });
      const dps = await listDispatchesByEndpoint(endpointBid);
      setEndpointDispatches(dps.items || []);
      setNewMsgBid("");
      setNewMappingText("{}");
      setNewEnabled(true);
    } catch (e: any) {
      alert(e.message || "新增映射失败");
    }
  };

  if (loading && !name) return <div className="container">加载中...</div>;

  return (
    <div className="container max-w-2xl">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">编辑端点</h1>
        <Button
          variant="outline"
          onClick={onDelete}
          className="text-red-600 border-red-600"
        >
          删除
        </Button>
      </div>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Label htmlFor="name">名称</Label>
          <Input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="transport">类型</Label>
            <select
              id="transport"
              className="border rounded-md h-9 px-3 text-sm w-full"
              value={transport}
              onChange={(e) => setTransport(e.target.value)}
            >
              <option value="http">http</option>
              <option value="mq">mq</option>
            </select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="adapterKey">适配器</Label>
            <Input
              id="adapterKey"
              value={adapterKey}
              onChange={(e) => setAdapterKey(e.target.value)}
            />
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="endpointUrl">地址（HTTP 可用）</Label>
          <Input
            id="endpointUrl"
            value={endpointUrl}
            onChange={(e) => setEndpointUrl(e.target.value)}
          />
        </div>
        <div className="space-y-1">
          <Label htmlFor="authProfile">认证配置（可选）</Label>
          <select
            id="authProfile"
            className="border rounded-md h-9 px-3 text-sm w-full"
            value={authProfileBid}
            onChange={(e) => setAuthProfileBid(e.target.value)}
          >
            <option value="">不使用认证</option>
            {authProfiles.map((p) => (
              <option key={p.auth_profile_bid} value={p.auth_profile_bid}>
                {p.name} ({p.type})
              </option>
            ))}
          </select>
        </div>
        <div className="space-y-1">
          <Label>配置（基于适配器 Schema）</Label>
          <RjsfForm
            schema={endpointConfigSchemaFor(adapterKey)}
            formData={configObj}
            onChange={(val) => {
              setConfigObj(val);
              setConfigText(JSON.stringify(val ?? {}, null, 2));
            }}
          />
          {adapterKey === "http.mailgun" && (
            <p className="text-xs text-muted-foreground">
              Mailgun 提示：API URL 如
              https://api.mailgun.net/v3/&lt;domain&gt;/messages；设置
              api_key；可在 config 里预设 from/to 方便测试。
            </p>
          )}
          {adapterKey === "http.sendgrid" && (
            <p className="text-xs text-muted-foreground">
              SendGrid 提示：API URL 通常为
              https://api.sendgrid.com/v3/mail/send；设置 api_key；建议在 config
              里预设 from/to 以便测试。
            </p>
          )}
          {(adapterKey?.startsWith("smtp.") || transport === "smtp") && (
            <p className="text-xs text-muted-foreground">
              SMTP 提示：配置 host、端口、TLS/SSL、用户名/密码（如需）、默认
              from/to。支持 text 与 html。
            </p>
          )}
          <div className="space-y-1 mt-2">
            <Label htmlFor="config">高级模式：配置 JSON</Label>
            <Textarea
              id="config"
              value={configText}
              onChange={(e) => {
                setConfigText(e.target.value);
                try {
                  setConfigObj(JSON.parse(e.target.value || "{}"));
                } catch {}
              }}
              className="font-mono"
            />
          </div>
        </div>
        <div className="space-y-3">
          <h2 className="text-lg font-medium">
            派发映射（Endpoint ← Message）
          </h2>
          <div className="rounded-lg border p-3 space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="msg">选择消息定义</Label>
                <select
                  id="msg"
                  className="border rounded-md h-9 px-3 text-sm w-full"
                  value={newMsgBid}
                  onChange={(e) => setNewMsgBid(e.target.value)}
                >
                  <option value="">选择消息定义</option>
                  {messageDefs.map((m) => (
                    <option
                      key={m.message_definition_bid}
                      value={m.message_definition_bid}
                    >
                      {m.name} ({m.type || "custom"})
                    </option>
                  ))}
                </select>
              </div>
              <div className="space-y-1">
                <Label htmlFor="enabled2">启用</Label>
                <select
                  id="enabled2"
                  className="border rounded-md h-9 px-3 text-sm w-full"
                  value={newEnabled ? "1" : "0"}
                  onChange={(e) => setNewEnabled(e.target.value === "1")}
                >
                  <option value="1">是</option>
                  <option value="0">否</option>
                </select>
              </div>
            </div>
            <div className="space-y-1">
              <Label htmlFor="mapping2">Mapping JSON（可选）</Label>
              <Textarea
                id="mapping2"
                className="font-mono"
                value={newMappingText}
                onChange={(e) => setNewMappingText(e.target.value)}
              />
            </div>
            <div>
              <Button
                type="button"
                onClick={onAddDispatch}
                disabled={!newMsgBid}
              >
                新增映射
              </Button>
            </div>
          </div>

          <div className="overflow-x-auto rounded-lg border">
            <table className="min-w-full text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-3 py-2 text-left">消息定义</th>
                  <th className="px-3 py-2 text-left">启用</th>
                  <th className="px-3 py-2 text-left">操作</th>
                </tr>
              </thead>
              <tbody>
                {endpointDispatches.map((d) => (
                  <tr key={d.message_dispatch_bid} className="border-t">
                    <td className="px-3 py-2">{d.message_definition_bid}</td>
                    <td className="px-3 py-2">{d.enabled ? "是" : "否"}</td>
                    <td className="px-3 py-2">
                      <button
                        onClick={async () => {
                          await deleteDispatch(d.message_dispatch_bid);
                          const dd =
                            await listDispatchesByEndpoint(endpointBid);
                          setEndpointDispatches(dd.items || []);
                        }}
                        className="text-red-600 hover:underline"
                      >
                        删除
                      </button>
                    </td>
                  </tr>
                ))}
                {endpointDispatches.length === 0 && (
                  <tr>
                    <td className="px-3 py-4 text-muted-foreground" colSpan={3}>
                      暂无映射
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="test">测试发送（按适配器自动构造消息）</Label>
          <div className="flex gap-2">
            <Input
              id="test"
              value={testText}
              onChange={(e) => setTestText(e.target.value)}
              placeholder="测试消息文本"
            />
            <Button type="button" variant="outline" onClick={onSendTest}>
              发送
            </Button>
          </div>
          {testResult && (
            <p className="text-xs text-muted-foreground break-all">
              {testResult}
            </p>
          )}
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>
            {loading ? "保存中..." : "保存"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => router.push(`/systems/${systemBid}`)}
          >
            取消
          </Button>
        </div>
      </form>
    </div>
  );
}
