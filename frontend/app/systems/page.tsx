"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { listSystems, deleteSystem } from "@/lib/api";
import { useI18n } from "@/i18n/provider";

interface SystemItem {
  business_system_bid: string;
  name: string;
  base_url?: string | null;
  auth_method?: string | null;
  app_id?: string | null;
  app_secret?: string | null;
  status: number;
}

export default function SystemsPage() {
  const { t } = useI18n();
  const [items, setItems] = useState<SystemItem[]>([]);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async (query?: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await listSystems({ q: query, limit: 50, offset: 0 });
      setItems(data.items || []);
    } catch (err: any) {
      setError(err.message || t("common.failedLoad"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const onSearch = (e: React.FormEvent) => {
    e.preventDefault();
    load(q);
  };

  const onDelete = async (bid: string) => {
    if (!confirm(t("systems.delete.confirm"))) return;
    try {
      await deleteSystem(bid);
      await load(q);
    } catch (err: any) {
      alert(err.message || t("common.failedDelete"));
    }
  };

  return (
    <div className="container space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 className="text-2xl font-semibold">{t("systems.title")}</h1>
        <div className="flex items-center gap-2">
          <form onSubmit={onSearch} className="flex items-center gap-2">
            <Input
              placeholder={t("systems.search.placeholder")}
              value={q}
              onChange={(e) => setQ(e.target.value)}
            />
            <Button type="submit" variant="outline">
              {t("systems.search.button")}
            </Button>
          </form>
          <Link href="/systems/new">
            <Button>{t("common.create")}</Button>
          </Link>
        </div>
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-3 py-2 text-left">{t("systems.table.name")}</th>
              <th className="px-3 py-2 text-left">
                {t("systems.table.baseUrl")}
              </th>
              <th className="px-3 py-2 text-left">{t("systems.table.auth")}</th>
              <th className="px-3 py-2 text-left">
                {t("systems.table.status")}
              </th>
              <th className="px-3 py-2 text-left">
                {t("systems.table.actions")}
              </th>
            </tr>
          </thead>
          <tbody>
            {items.map((it) => (
              <tr key={it.business_system_bid} className="border-t">
                <td className="px-3 py-2">{it.name}</td>
                <td className="px-3 py-2 text-muted-foreground">
                  {it.base_url || "—"}
                </td>
                <td className="px-3 py-2">{it.auth_method || "—"}</td>
                <td className="px-3 py-2">{it.status}</td>
                <td className="px-3 py-2 flex gap-2">
                  <Link
                    href={`/systems/${it.business_system_bid}`}
                    className="text-primary hover:underline"
                  >
                    {t("common.edit")}
                  </Link>
                  <button
                    onClick={() => onDelete(it.business_system_bid)}
                    className="text-red-600 hover:underline"
                  >
                    {t("common.delete")}
                  </button>
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td className="px-3 py-4 text-muted-foreground" colSpan={5}>
                  {t("common.noData")}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
