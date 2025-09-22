"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listSendRecords, listMessageDefs, listAllEndpoints } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useI18n } from "@/i18n/provider";

export default function RecordsPage() {
  const { t } = useI18n();
  const [items, setItems] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [limit] = useState(50);
  const [offset, setOffset] = useState(0);
  const [messageBid, setMessageBid] = useState("");
  const [endpointBid, setEndpointBid] = useState("");
  const [status, setStatus] = useState<string>("");
  const [messages, setMessages] = useState<any[]>([]);
  const [endpoints, setEndpoints] = useState<any[]>([]);

  const load = async () => {
    const res = await listSendRecords({
      limit,
      offset,
      message_definition_bid: messageBid || undefined,
      notification_api_bid: endpointBid || undefined,
      status: status === "" ? undefined : Number(status),
    });
    setItems(res.items || []);
    setTotal(res.total || 0);
  };

  useEffect(() => {
    (async () => {
      const [msgs, eps] = await Promise.all([
        listMessageDefs({ limit: 500, offset: 0 }),
        listAllEndpoints({ limit: 500, offset: 0 }),
      ]);
      setMessages(msgs.items || []);
      setEndpoints(eps.items || []);
    })();
  }, []);

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [offset]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">{t("records.title")}</h1>
      <div className="flex flex-wrap gap-2 items-center">
        <select
          className="border rounded px-2 py-1"
          value={messageBid}
          onChange={(e) => setMessageBid(e.target.value)}
        >
          <option value="">{t("records.filters.allMessages")}</option>
          {messages.map((m) => (
            <option
              key={m.message_definition_bid}
              value={m.message_definition_bid}
            >
              {m.name}
            </option>
          ))}
        </select>
        <select
          className="border rounded px-2 py-1"
          value={endpointBid}
          onChange={(e) => setEndpointBid(e.target.value)}
        >
          <option value="">{t("records.filters.allEndpoints")}</option>
          {endpoints.map((ep) => (
            <option
              key={ep.notification_api_bid}
              value={ep.notification_api_bid}
            >
              {ep.name}
            </option>
          ))}
        </select>
        <select
          className="border rounded px-2 py-1"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          <option value="">{t("records.filters.allStatus")}</option>
          <option value="1">{t("common.success")}</option>
          <option value="0">{t("common.pending")}</option>
          <option value="-1">{t("common.failed")}</option>
        </select>
        <Button
          type="button"
          variant="outline"
          onClick={() => {
            setOffset(0);
            load();
          }}
        >
          {t("records.filters.apply")}
        </Button>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full border text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="p-2 border">{t("records.table.time")}</th>
              <th className="p-2 border">{t("records.table.message")}</th>
              <th className="p-2 border">{t("records.table.endpoint")}</th>
              <th className="p-2 border">{t("records.table.status")}</th>
              <th className="p-2 border">{t("records.table.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {items.map((it) => (
              <tr key={it.send_record_bid} className="hover:bg-accent/30">
                <td className="p-2 border whitespace-nowrap">
                  {it.send_time ? new Date(it.send_time).toLocaleString() : "-"}
                </td>
                <td className="p-2 border">
                  {it.message_name || it.message_definition_bid}
                </td>
                <td className="p-2 border">
                  {it.endpoint_name || it.notification_api_bid}
                </td>
                <td className="p-2 border">
                  {it.status === 1
                    ? t("common.success")
                    : it.status === -1
                      ? t("common.failed")
                      : t("common.pending")}
                </td>
                <td className="p-2 border">
                  <Link
                    href={`/records/${it.send_record_bid}`}
                    className="text-primary hover:underline"
                  >
                    {t("records.actions.detail")}
                  </Link>
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td
                  colSpan={5}
                  className="p-4 text-center text-muted-foreground"
                >
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
          {t("records.pager.prev")}
        </Button>
        <span className="text-sm text-muted-foreground">
          {offset + 1}-{Math.min(offset + limit, total)} / {total}
        </span>
        <Button
          variant="outline"
          disabled={offset + limit >= total}
          onClick={() => setOffset(offset + limit)}
        >
          {t("records.pager.next")}
        </Button>
      </div>
    </div>
  );
}
