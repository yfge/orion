"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { listMessageDefs, deleteMessageDef } from "@/lib/api";
import { useI18n } from "@/i18n/provider";

interface MsgDef {
  message_definition_bid: string;
  name: string;
  type?: string | null;
  status: number;
}

export default function MessagesPage() {
  const { t } = useI18n();
  const [items, setItems] = useState<MsgDef[]>([]);
  const [q, setQ] = useState("");
  const [error, setError] = useState<string | null>(null);

  const load = async (query?: string) => {
    setError(null);
    try {
      const res = await listMessageDefs({ q: query, limit: 50, offset: 0 });
      setItems(res.items || []);
    } catch (e: any) {
      setError(e.message || t("common.failedLoad"));
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
    if (!confirm(t("messages.delete.confirm"))) return;
    try {
      await deleteMessageDef(bid);
      await load(q);
    } catch (e: any) {
      alert(e.message || t("common.failedDelete"));
    }
  };

  return (
    <div className="container space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 className="text-2xl font-semibold">{t("messages.title")}</h1>
        <div className="flex items-center gap-2">
          <form onSubmit={onSearch} className="flex items-center gap-2">
            <Input
              placeholder={t("messages.search.placeholder")}
              value={q}
              onChange={(e) => setQ(e.target.value)}
            />
            <Button type="submit" variant="outline">
              {t("messages.search.button")}
            </Button>
          </form>
          <Link href="/messages/new">
            <Button>{t("common.create")}</Button>
          </Link>
        </div>
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-3 py-2 text-left">
                {t("messages.table.name")}
              </th>
              <th className="px-3 py-2 text-left">
                {t("messages.table.type")}
              </th>
              <th className="px-3 py-2 text-left">
                {t("messages.table.status")}
              </th>
              <th className="px-3 py-2 text-left">
                {t("messages.table.actions")}
              </th>
            </tr>
          </thead>
          <tbody>
            {items.map((it) => (
              <tr key={it.message_definition_bid} className="border-t">
                <td className="px-3 py-2">{it.name}</td>
                <td className="px-3 py-2">{it.type || "—"}</td>
                <td className="px-3 py-2">{it.status}</td>
                <td className="px-3 py-2 flex gap-2">
                  <Link
                    href={`/messages/${it.message_definition_bid}`}
                    className="text-primary hover:underline"
                  >
                    {t("common.edit")}
                  </Link>
                  <button
                    onClick={() => onDelete(it.message_definition_bid)}
                    className="text-red-600 hover:underline"
                  >
                    {t("common.delete")}
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
    </div>
  );
}
