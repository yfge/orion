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
import { endpointConfigSchemaFor, mappingSchemaFor } from "@/lib/schemas";
import { RjsfForm } from "@/components/jsonschema/RjsfForm";
import { useI18n } from "@/i18n/provider";

export default function EditEndpointPage() {
  const { t } = useI18n();
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
  const [newMappingObj, setNewMappingObj] = useState<any>({});
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
        setError(err.message || t("common.failedLoad"));
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
      setError(err.message || t("endpoints.save.failed"));
    } finally {
      setLoading(false);
    }
  };

  const onDelete = async () => {
    if (!confirm(t("endpoints.delete.confirm"))) return;
    try {
      await deleteEndpoint(endpointBid);
      router.push(`/systems/${systemBid}`);
    } catch (err: any) {
      alert(err.message || t("common.failedDelete"));
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
      const mapping =
        newMappingObj ?? (newMappingText ? JSON.parse(newMappingText) : null);
      await createDispatchForEndpoint(endpointBid, {
        message_definition_bid: newMsgBid,
        mapping,
        enabled: newEnabled,
      });
      const dps = await listDispatchesByEndpoint(endpointBid);
      setEndpointDispatches(dps.items || []);
      setNewMsgBid("");
      setNewMappingText("{}");
      setNewMappingObj({});
      setNewEnabled(true);
    } catch (e: any) {
      alert(e.message || "新增映射失败");
    }
  };

  if (loading && !name)
    return <div className="container">{t("common.loading")}</div>;

  return (
    <div className="container max-w-2xl">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">{t("endpoints.edit.title")}</h1>
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
          <Label htmlFor="name">{t("endpoints.fields.name")}</Label>
          <Input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="transport">{t("endpoints.fields.transport")}</Label>
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
            <Label htmlFor="adapterKey">{t("endpoints.fields.adapter")}</Label>
            <Input
              id="adapterKey"
              value={adapterKey}
              onChange={(e) => setAdapterKey(e.target.value)}
            />
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="endpointUrl">{t("endpoints.fields.httpUrl")}</Label>
          <Input
            id="endpointUrl"
            value={endpointUrl}
            onChange={(e) => setEndpointUrl(e.target.value)}
          />
        </div>
        <div className="space-y-1">
          <Label htmlFor="authProfile">{t("endpoints.fields.auth")}</Label>
          <select
            id="authProfile"
            className="border rounded-md h-9 px-3 text-sm w-full"
            value={authProfileBid}
            onChange={(e) => setAuthProfileBid(e.target.value)}
          >
            <option value="">{t("endpoints.fields.auth.none")}</option>
            {authProfiles.map((p) => (
              <option key={p.auth_profile_bid} value={p.auth_profile_bid}>
                {p.name} ({p.type})
              </option>
            ))}
          </select>
        </div>
        <div className="space-y-1">
          <Label>{t("endpoints.fields.configSchemaForm")}</Label>
          <RjsfForm
            schema={endpointConfigSchemaFor(adapterKey, t)}
            formData={configObj}
            onChange={(val) => {
              setConfigObj(val);
              setConfigText(JSON.stringify(val ?? {}, null, 2));
            }}
          />
          {adapterKey === "http.mailgun" && (
            <p className="text-xs text-muted-foreground">
              {t("endpoints.hints.mailgun")}
            </p>
          )}
          {adapterKey === "http.sendgrid" && (
            <p className="text-xs text-muted-foreground">
              {t("endpoints.hints.sendgrid")}
            </p>
          )}
          {(adapterKey?.startsWith("smtp.") || transport === "smtp") && (
            <p className="text-xs text-muted-foreground">
              {t("endpoints.hints.smtp")}
            </p>
          )}
          <div className="space-y-1 mt-2">
            <Label htmlFor="config">
              {t("apis.fields.configJsonAdvanced")}
            </Label>
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
            {t("endpoints.dispatch.title")}
          </h2>
          <div className="rounded-lg border p-3 space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="msg">
                  {t("endpoints.dispatch.selectMessage")}
                </Label>
                <select
                  id="msg"
                  className="border rounded-md h-9 px-3 text-sm w-full"
                  value={newMsgBid}
                  onChange={(e) => setNewMsgBid(e.target.value)}
                >
                  <option value="">
                    {t("endpoints.dispatch.selectMessagePlaceholder")}
                  </option>
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
                <Label htmlFor="enabled2">
                  {t("endpoints.dispatch.enabled")}
                </Label>
                <select
                  id="enabled2"
                  className="border rounded-md h-9 px-3 text-sm w-full"
                  value={newEnabled ? "1" : "0"}
                  onChange={(e) => setNewEnabled(e.target.value === "1")}
                >
                  <option value="1">{t("common.yes")}</option>
                  <option value="0">{t("common.no")}</option>
                </select>
              </div>
            </div>
            <div className="space-y-2">
              <Label>{t("endpoints.dispatch.mappingSchema")}</Label>
              <RjsfForm
                schema={mappingSchemaFor(
                  adapterKey,
                  messageDefs.find(
                    (m: any) => m.message_definition_bid === newMsgBid,
                  )?.type || null,
                )}
                formData={newMappingObj}
                onChange={(val) => {
                  setNewMappingObj(val);
                  setNewMappingText(JSON.stringify(val ?? {}, null, 2));
                }}
              />
              {(adapterKey === "http.mailgun" ||
                adapterKey === "http.sendgrid" ||
                (typeof adapterKey === "string" &&
                  adapterKey.startsWith("smtp."))) && (
                <p className="text-xs text-muted-foreground">
                  {t("endpoints.dispatch.mailMappingHint")}
                </p>
              )}
              <div className="space-y-1">
                <Label htmlFor="mapping2">
                  {t("endpoints.dispatch.mappingJsonAdvanced")}
                </Label>
                <Textarea
                  id="mapping2"
                  className="font-mono"
                  value={newMappingText}
                  onChange={(e) => {
                    setNewMappingText(e.target.value);
                    try {
                      setNewMappingObj(JSON.parse(e.target.value || "{}"));
                    } catch {}
                  }}
                />
              </div>
            </div>
            <div>
              <Button
                type="button"
                onClick={onAddDispatch}
                disabled={!newMsgBid}
              >
                {t("endpoints.dispatch.addMapping")}
              </Button>
            </div>
          </div>

          <div className="overflow-x-auto rounded-lg border">
            <table className="min-w-full text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-3 py-2 text-left">
                    {t("endpoints.dispatch.table.message")}
                  </th>
                  <th className="px-3 py-2 text-left">
                    {t("endpoints.dispatch.table.enabled")}
                  </th>
                  <th className="px-3 py-2 text-left">
                    {t("endpoints.dispatch.table.actions")}
                  </th>
                </tr>
              </thead>
              <tbody>
                {endpointDispatches.map((d) => (
                  <tr key={d.message_dispatch_bid} className="border-t">
                    <td className="px-3 py-2">{d.message_definition_bid}</td>
                    <td className="px-3 py-2">
                      {d.enabled ? t("common.yes") : t("common.no")}
                    </td>
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
                        {t("common.delete")}
                      </button>
                    </td>
                  </tr>
                ))}
                {endpointDispatches.length === 0 && (
                  <tr>
                    <td className="px-3 py-4 text-muted-foreground" colSpan={3}>
                      {t("endpoints.dispatch.none")}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="test">{t("endpoints.test.title")}</Label>
          <div className="flex gap-2">
            <Input
              id="test"
              value={testText}
              onChange={(e) => setTestText(e.target.value)}
              placeholder={t("endpoints.test.placeholder")}
            />
            <Button type="button" variant="outline" onClick={onSendTest}>
              {t("endpoints.test.send")}
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
            {loading ? t("common.saving") : t("common.save")}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => router.push(`/systems/${systemBid}`)}
          >
            {t("common.cancel")}
          </Button>
        </div>
      </form>
    </div>
  );
}
