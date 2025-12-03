"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { createEndpoint, listAuthProfiles, validateSchema } from "@/lib/api";
import { JsonSchemaForm } from "@/components/jsonschema/Form";
import { endpointConfigSchemaFor } from "@/lib/schemas";
import { useI18n } from "@/i18n/provider";

export default function NewEndpointPage() {
  const { t } = useI18n();
  const params = useParams<{ bid: string }>();
  const systemBid = params?.bid as string;
  const router = useRouter();

  const [name, setName] = useState("");
  const [transport, setTransport] = useState("http");
  const [adapterKey, setAdapterKey] = useState("");
  const [endpointUrl, setEndpointUrl] = useState("");
  const [configText, setConfigText] = useState(
    '{\n  "method": "POST",\n  "headers": {\n    "Content-Type": "application/json"\n  }\n}',
  );
  const [configObj, setConfigObj] = useState<any>({});
  const [validateResult, setValidateResult] = useState<string | null>(null);
  const [authProfiles, setAuthProfiles] = useState<any[]>([]);
  const [authProfileBid, setAuthProfileBid] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const cfg = configText ? JSON.parse(configText) : null;
      await createEndpoint(systemBid, {
        name,
        transport,
        adapter_key: adapterKey || null,
        endpoint_url: endpointUrl || null,
        config: cfg,
        auth_profile_bid: authProfileBid || null,
        status: 0,
      });
      router.push(`/systems/${systemBid}`);
    } catch (err: any) {
      setError(err.message || t("endpoints.create.failed"));
    } finally {
      setLoading(false);
    }
  };

  // load auth profiles
  useEffect(() => {
    (async () => {
      try {
        const data = await listAuthProfiles({ limit: 100, offset: 0 });
        setAuthProfiles(data.items || []);
      } catch (e) {
        // ignore
      }
    })();
  }, []);

  const adapterOptions: Record<string, string[]> = {
    http: ["http.generic", "http.feishu_bot", "http.mailgun", "http.sendgrid"],
    mq: ["mq.kafka", "mq.rabbit"],
    channel: ["channel.wechat_official_account"],
  };
  const optionsForSelect = Array.from(
    new Set([
      ...(adapterOptions[transport] || []),
      ...(transport !== "channel" ? adapterOptions.channel : []),
    ]),
  );

  return (
    <div className="container max-w-2xl">
      <h1 className="text-2xl font-semibold mb-4">
        {t("endpoints.new.title")}
      </h1>
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
              onChange={(e) => {
                const nextTransport = e.target.value;
                const presets = adapterOptions[nextTransport] || [];
                setTransport(nextTransport);
                if (!adapterKey || !presets.includes(adapterKey)) {
                  setAdapterKey(presets[0] || "");
                }
              }}
            >
              <option value="http">http</option>
              <option value="mq">mq</option>
              <option value="channel">channel</option>
            </select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="adapterKey">{t("endpoints.fields.adapter")}</Label>
            <select
              id="adapterKey"
              className="border rounded-md h-9 px-3 text-sm w-full"
              value={adapterKey}
              onChange={(e) => {
                const nextAdapter = e.target.value;
                setAdapterKey(nextAdapter);
                if (nextAdapter.startsWith("channel.")) {
                  setTransport("channel");
                }
              }}
            >
              <option value="">
                {t("endpoints.fields.adapter.placeholder")}
              </option>
              {optionsForSelect.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="endpointUrl">
            {transport === "channel"
              ? t("apis.fields.apiUrl")
              : t("endpoints.fields.httpUrl")}
          </Label>
          <Input
            id="endpointUrl"
            value={endpointUrl}
            onChange={(e) => setEndpointUrl(e.target.value)}
            placeholder={
              transport === "channel" ? "https://api.weixin.qq.com" : "https://..."
            }
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
        <div className="space-y-2">
          <Label>{t("endpoints.fields.configSchemaForm")}</Label>
          <JsonSchemaForm
            schema={endpointConfigSchemaFor(adapterKey, t)}
            value={configObj}
            onChange={(v) => {
              setConfigObj(v);
              setConfigText(JSON.stringify(v, null, 2));
            }}
          />
          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={async () => {
                try {
                  const res = await validateSchema({
                    schema: endpointConfigSchemaFor(adapterKey),
                    data: configObj,
                  });
                  setValidateResult(
                    res.valid
                      ? t("apis.validate.valid")
                      : `${t("apis.validate.invalidPrefix")} ${(
                          res.errors || []
                        )
                          .map((e: any) => e.message)
                          .join("; ")}`,
                  );
                } catch (e: any) {
                  setValidateResult(e.message || t("apis.validate.exception"));
                }
              }}
            >
              {t("apis.validate.button")}
            </Button>
            {validateResult && (
              <p className="text-xs text-muted-foreground">{validateResult}</p>
            )}
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="config">{t("apis.fields.configJsonAdvanced")}</Label>
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
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>
            {loading ? t("common.creating") : t("common.create")}
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
