"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import {
  createApiKey,
  deleteApiKey,
  listApiKeys,
  updateApiKey,
} from "@/lib/api";
import { useI18n } from "@/i18n/provider";

export default function ApiKeysPage() {
  const { t } = useI18n();
  const [mounted, setMounted] = useState(false);
  const [items, setItems] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [limit] = useState(50);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState("");
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [newToken, setNewToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const res = await listApiKeys({ limit, offset, q: q || undefined });
      setItems(res.items || []);
      setTotal(res.total || 0);
    } catch (e: any) {
      setError(e.message || t("common.failedLoad"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setMounted(true);
    load();
  }, [offset]);

  const onCreate = async () => {
    setError(null);
    try {
      const r = await createApiKey({ name, description: desc || undefined });
      setNewToken(r.token);
      setName("");
      setDesc("");
      load();
    } catch (e: any) {
      setError(e.message || t("apiKeys.create.failed"));
    }
  };

  const onDelete = async (bid: string) => {
    if (!confirm(t("apiKeys.delete.confirm"))) return;
    try {
      await deleteApiKey(bid);
      load();
    } catch (e: any) {
      alert(e.message || t("common.failedDelete"));
    }
  };

  if (!mounted) return <div className="container">{t("common.loading")}</div>;

  return (
    <div className="container max-w-2xl space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{t("apiKeys.title")}</h1>
      </div>

      <div className="rounded-lg border p-4 space-y-3">
        <h2 className="text-lg font-medium">{t("apiKeys.new.title")}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="name">{t("apiKeys.fields.name")}</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder={t("apiKeys.fields.name.placeholder")}
            />
          </div>
          <div className="space-y-1 md:col-span-2">
            <Label htmlFor="desc">{t("apiKeys.fields.desc")}</Label>
            <Input
              id="desc"
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              placeholder={t("apiKeys.fields.desc.placeholder")}
            />
          </div>
        </div>
        <Button type="button" onClick={onCreate} disabled={!name}>
          {t("apiKeys.create")}
        </Button>
        {error && <p className="text-sm text-red-600">{error}</p>}
        {newToken && (
          <div className="rounded-md border p-3 text-sm">
            <div className="font-medium mb-1">
              {t("apiKeys.newToken.title")}
            </div>
            <div className="font-mono break-all">{newToken}</div>
            <div className="text-xs text-muted-foreground mt-1">
              {t("apiKeys.newToken.hint")}
            </div>
          </div>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <Input
          placeholder={t("apiKeys.search.placeholder")}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="w-64"
        />
        <Button
          type="button"
          variant="outline"
          onClick={() => {
            setOffset(0);
            load();
          }}
          disabled={loading}
        >
          {t("apiKeys.search.button")}
        </Button>
      </div>

      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-3 py-2 text-left">{t("apiKeys.table.name")}</th>
              <th className="px-3 py-2 text-left">
                {t("apiKeys.table.prefix")}
              </th>
              <th className="px-3 py-2 text-left">
                {t("apiKeys.table.status")}
              </th>
              <th className="px-3 py-2 text-left">
                {t("apiKeys.table.actions")}
              </th>
            </tr>
          </thead>
          <tbody>
            {items.map((it: any) => (
              <tr key={it.api_key_bid} className="border-t">
                <td className="px-3 py-2">{it.name}</td>
                <td className="px-3 py-2 text-muted-foreground">
                  {it.prefix || ""}...{it.suffix || ""}
                </td>
                <td className="px-3 py-2">
                  {it.status === 1
                    ? t("apiKeys.status.enabled")
                    : t("apiKeys.status.disabled")}
                </td>
                <td className="px-3 py-2">
                  <button
                    onClick={async () => {
                      await updateApiKey(it.api_key_bid, {
                        status: it.status === 1 ? 0 : 1,
                      });
                      load();
                    }}
                    className="text-primary hover:underline mr-3"
                  >
                    {it.status === 1
                      ? t("apiKeys.actions.disable")
                      : t("apiKeys.actions.enable")}
                  </button>
                  <button
                    onClick={() => onDelete(it.api_key_bid)}
                    className="text-red-600 hover:underline"
                  >
                    {t("apiKeys.actions.delete")}
                  </button>
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td className="px-3 py-4 text-muted-foreground" colSpan={4}>
                  {t("common.noData")}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          disabled={offset === 0}
          onClick={() => setOffset(Math.max(0, offset - limit))}
        >
          {t("apiKeys.pager.prev")}
        </Button>
        <span className="text-sm text-muted-foreground">
          {offset + 1}-{Math.min(offset + limit, total)} / {total}
        </span>
        <Button
          variant="outline"
          disabled={offset + limit >= total}
          onClick={() => setOffset(offset + limit)}
        >
          {t("apiKeys.pager.next")}
        </Button>
      </div>
    </div>
  );
}
