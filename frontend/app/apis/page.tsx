"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listAllEndpoints, listSystems } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/i18n/provider";

export default function ApisPage() {
  const { t } = useI18n();
  const [mounted, setMounted] = useState(false);
  const [q, setQ] = useState("");
  const [items, setItems] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [limit] = useState(50);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const [systems, setSystems] = useState<any[]>([]);
  const [newSystemBid, setNewSystemBid] = useState("");

  const load = async () => {
    setLoading(true);
    try {
      const res = await listAllEndpoints({ limit, offset, q: q || undefined });
      setItems(res.items || []);
      setTotal(res.total || 0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setMounted(true);
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [offset]);

  useEffect(() => {
    (async () => {
      try {
        const s = await listSystems({ limit: 200, offset: 0 });
        setSystems(s.items || []);
      } catch {}
    })();
  }, []);

  if (!mounted) {
    return <div className="container">{t("common.loading")}</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{t("apis.title")}</h1>
        <Link
          href="/apis/new"
          className="inline-flex items-center rounded-md border px-3 h-9 text-sm border-input text-foreground hover:bg-accent"
        >
          {t("common.create")}
        </Link>
      </div>
      {items.length === 0 && (
        <div className="rounded-md border p-3 text-sm text-muted-foreground">
          {t("apis.empty.prefix")}
          <Link
            href="/systems/new"
            className="text-primary hover:underline ml-1"
          >
            {t("apis.empty.link")}
          </Link>
          {t("apis.empty.suffix")}
        </div>
      )}

      <div className="flex flex-wrap items-center gap-2">
        <Input
          placeholder={t("apis.search.placeholder")}
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
          {t("apis.search.button")}
        </Button>
        <div className="ml-auto" />
      </div>

      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-3 py-2 text-left">{t("apis.table.name")}</th>
              <th className="px-3 py-2 text-left">{t("apis.table.system")}</th>
              <th className="px-3 py-2 text-left">{t("apis.table.type")}</th>
              <th className="px-3 py-2 text-left">{t("apis.table.adapter")}</th>
              <th className="px-3 py-2 text-left">{t("apis.table.url")}</th>
              <th className="px-3 py-2 text-left">{t("apis.table.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {items.map((ep) => (
              <tr key={ep.notification_api_bid} className="border-t">
                <td className="px-3 py-2">{ep.name}</td>
                <td className="px-3 py-2 text-muted-foreground">
                  {ep.business_system_bid || "—"}
                </td>
                <td className="px-3 py-2">{ep.transport || "—"}</td>
                <td className="px-3 py-2">{ep.adapter_key || "—"}</td>
                <td className="px-3 py-2 break-all">
                  {ep.endpoint_url || "—"}
                </td>
                <td className="px-3 py-2">
                  {ep.business_system_bid ? (
                    <Link
                      href={`/systems/${ep.business_system_bid}/endpoints/${ep.notification_api_bid}`}
                      className="text-primary hover:underline"
                    >
                      {t("common.edit")}
                    </Link>
                  ) : (
                    <span className="text-muted-foreground">—</span>
                  )}
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td className="px-3 py-4 text-muted-foreground" colSpan={6}>
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
          {t("apis.pager.prev")}
        </Button>
        <span className="text-sm text-muted-foreground">
          {offset + 1}-{Math.min(offset + limit, total)} / {total}
        </span>
        <Button
          variant="outline"
          disabled={offset + limit >= total}
          onClick={() => setOffset(offset + limit)}
        >
          {t("apis.pager.next")}
        </Button>
      </div>
    </div>
  );
}
