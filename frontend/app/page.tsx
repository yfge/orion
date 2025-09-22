"use client";

import { useEffect, useMemo, useState } from "react";
import { Card } from "@/components/ui/card";
import { listSystems, listAllEndpoints, listSendRecords } from "@/lib/api";
import { useI18n } from "@/i18n/provider";

function toIso(dt: Date) {
  return dt.toISOString();
}

export default function HomePage() {
  const { t } = useI18n();
  const [systemsTotal, setSystemsTotal] = useState<number | null>(null);
  const [endpointsTotal, setEndpointsTotal] = useState<number | null>(null);
  const [todaySuccess, setTodaySuccess] = useState<number | null>(null);
  const [todayFailed, setTodayFailed] = useState<number | null>(null);
  const [recent, setRecent] = useState<any[]>([]);

  useEffect(() => {
    (async () => {
      try {
        const sys = await listSystems({ limit: 1, offset: 0 });
        setSystemsTotal(sys.total || 0);
      } catch {}
      try {
        const eps = await listAllEndpoints({ limit: 1, offset: 0 });
        setEndpointsTotal(eps.total || 0);
      } catch {}
      try {
        const now = new Date();
        const start = new Date(now);
        start.setHours(0, 0, 0, 0);
        const end = new Date(now);
        end.setHours(23, 59, 59, 999);
        const [succ, fail, rec] = await Promise.all([
          listSendRecords({
            limit: 1,
            offset: 0,
            status: 1,
            start_time: toIso(start),
            end_time: toIso(end),
          }),
          listSendRecords({
            limit: 1,
            offset: 0,
            status: -1,
            start_time: toIso(start),
            end_time: toIso(end),
          }),
          listSendRecords({ limit: 10, offset: 0 }),
        ]);
        setTodaySuccess(succ.total || 0);
        setTodayFailed(fail.total || 0);
        setRecent(rec.items || []);
      } catch {}
    })();
  }, []);

  return (
    <div className="container space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">
          {t("home.title")}
        </h1>
        <p className="text-muted-foreground mt-1">{t("home.subtitle")}</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card
          title={t("home.cards.systems.title")}
          value={systemsTotal === null ? "…" : String(systemsTotal)}
          hint={t("home.cards.systems.hint")}
        />
        <Card
          title={t("home.cards.apis.title")}
          value={endpointsTotal === null ? "…" : String(endpointsTotal)}
          hint={t("home.cards.apis.hint")}
        />
        <Card
          title={t("home.cards.today.title")}
          value={
            todaySuccess === null || todayFailed === null
              ? "…"
              : `${todaySuccess}/${todayFailed}`
          }
          hint={t("home.cards.today.hint")}
        />
        <Card
          title={t("home.cards.toRetry.title")}
          value={todayFailed === null ? "…" : String(todayFailed)}
          hint={t("home.cards.toRetry.hint")}
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border bg-card p-4">
          <h2 className="font-medium mb-2">{t("home.recent.title")}</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-3 py-2 text-left">
                    {t("home.recent.time")}
                  </th>
                  <th className="px-3 py-2 text-left">
                    {t("home.recent.message")}
                  </th>
                  <th className="px-3 py-2 text-left">
                    {t("home.recent.endpoint")}
                  </th>
                  <th className="px-3 py-2 text-left">
                    {t("home.recent.status")}
                  </th>
                </tr>
              </thead>
              <tbody>
                {recent.map((it) => (
                  <tr key={it.send_record_bid} className="border-t">
                    <td className="px-3 py-2 whitespace-nowrap">
                      {it.send_time
                        ? new Date(it.send_time).toLocaleString()
                        : "-"}
                    </td>
                    <td className="px-3 py-2">
                      {it.message_name || it.message_definition_bid}
                    </td>
                    <td className="px-3 py-2">
                      {it.endpoint_name || it.notification_api_bid}
                    </td>
                    <td className="px-3 py-2">
                      {it.status === 1
                        ? t("common.success")
                        : it.status === -1
                          ? t("common.failed")
                          : t("common.pending")}
                    </td>
                  </tr>
                ))}
                {recent.length === 0 && (
                  <tr>
                    <td colSpan={4} className="px-3 py-4 text-muted-foreground">
                      {t("common.noData")}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
        <div className="rounded-lg border bg-card p-4">
          <h2 className="font-medium mb-2">{t("home.health.title")}</h2>
          <p className="text-sm text-muted-foreground">
            {t("home.health.note")}
          </p>
        </div>
      </div>
    </div>
  );
}
