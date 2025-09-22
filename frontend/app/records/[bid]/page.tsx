"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getSendRecord, listSendDetails } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/i18n/provider";

export default function RecordDetailPage() {
  const { t } = useI18n();
  const params = useParams<{ bid: string }>();
  const router = useRouter();
  const bid = params?.bid;
  const [record, setRecord] = useState<any>(null);
  const [details, setDetails] = useState<any[]>([]);

  useEffect(() => {
    if (!bid) return;
    (async () => {
      const rec = await getSendRecord(bid);
      setRecord(rec);
      const det = await listSendDetails(bid, { limit: 100, offset: 0 });
      setDetails(det.items || []);
    })();
  }, [bid]);

  if (!bid) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{t("records.detail.title")}</h1>
        <Button variant="outline" onClick={() => router.push("/records")}>
          {t("records.detail.back")}
        </Button>
      </div>
      {record && (
        <div className="space-y-1 text-sm">
          <div>
            <span className="text-muted-foreground">
              {t("records.detail.fields.recordBid")}：
            </span>
            {record.send_record_bid}
          </div>
          <div>
            <span className="text-muted-foreground">
              {t("records.detail.fields.time")}：
            </span>
            {record.send_time
              ? new Date(record.send_time).toLocaleString()
              : "-"}
          </div>
          <div>
            <span className="text-muted-foreground">
              {t("records.detail.fields.message")}：
            </span>
            {record.message_name || record.message_definition_bid}
          </div>
          <div>
            <span className="text-muted-foreground">
              {t("records.detail.fields.endpoint")}：
            </span>
            {record.endpoint_name || record.notification_api_bid}
          </div>
          <div>
            <span className="text-muted-foreground">
              {t("records.detail.fields.status")}：
            </span>
            {record.status === 1
              ? t("common.success")
              : record.status === -1
                ? t("common.failed")
                : t("common.pending")}
          </div>
          {record.result && (
            <div className="mt-2">
              <div className="text-muted-foreground">
                {t("records.detail.response")}：
              </div>
              <pre className="mt-1 p-2 bg-muted rounded max-h-80 overflow-auto text-xs">
                {JSON.stringify(record.result, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}

      <div>
        <h2 className="text-xl font-semibold mb-2">
          {t("records.detail.attempts.title")}
        </h2>
        <div className="overflow-x-auto">
          <table className="min-w-full border text-sm">
            <thead className="bg-muted/50">
              <tr>
                <th className="p-2 border">
                  {t("records.detail.attempts.table.try")}
                </th>
                <th className="p-2 border">
                  {t("records.detail.attempts.table.time")}
                </th>
                <th className="p-2 border">
                  {t("records.detail.attempts.table.endpoint")}
                </th>
                <th className="p-2 border">
                  {t("records.detail.attempts.table.status")}
                </th>
                <th className="p-2 border">
                  {t("records.detail.attempts.table.request")}
                </th>
                <th className="p-2 border">
                  {t("records.detail.attempts.table.response")}
                </th>
                <th className="p-2 border">
                  {t("records.detail.attempts.table.error")}
                </th>
              </tr>
            </thead>
            <tbody>
              {details.map((d) => (
                <tr key={d.send_detail_bid} className="align-top">
                  <td className="p-2 border whitespace-nowrap">
                    #{d.attempt_no}
                  </td>
                  <td className="p-2 border whitespace-nowrap">
                    {d.sent_at ? new Date(d.sent_at).toLocaleString() : "-"}
                  </td>
                  <td className="p-2 border whitespace-nowrap">
                    {d.endpoint_name || d.notification_api_bid}
                  </td>
                  <td className="p-2 border whitespace-nowrap">
                    {d.status === 1
                      ? t("common.success")
                      : d.status === -1
                        ? t("common.failed")
                        : t("common.pending")}
                  </td>
                  <td className="p-2 border">
                    <pre className="max-h-48 overflow-auto text-xs">
                      {d.request_payload
                        ? JSON.stringify(d.request_payload, null, 2)
                        : "-"}
                    </pre>
                  </td>
                  <td className="p-2 border">
                    <pre className="max-h-48 overflow-auto text-xs">
                      {d.response_payload
                        ? JSON.stringify(d.response_payload, null, 2)
                        : "-"}
                    </pre>
                  </td>
                  <td className="p-2 border text-red-600 whitespace-pre-wrap">
                    {d.error || "-"}
                  </td>
                </tr>
              ))}
              {details.length === 0 && (
                <tr>
                  <td
                    colSpan={7}
                    className="p-4 text-center text-muted-foreground"
                  >
                    {t("common.noData")}
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
