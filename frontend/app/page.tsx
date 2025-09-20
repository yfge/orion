"use client"

import { useEffect, useMemo, useState } from "react"
import { Card } from "@/components/ui/card"
import { listSystems, listAllEndpoints, listSendRecords } from "@/lib/api"

function toIso(dt: Date) {
  return dt.toISOString()
}

export default function HomePage() {
  const [systemsTotal, setSystemsTotal] = useState<number | null>(null)
  const [endpointsTotal, setEndpointsTotal] = useState<number | null>(null)
  const [todaySuccess, setTodaySuccess] = useState<number | null>(null)
  const [todayFailed, setTodayFailed] = useState<number | null>(null)
  const [recent, setRecent] = useState<any[]>([])

  useEffect(() => {
    ;(async () => {
      try {
        const sys = await listSystems({ limit: 1, offset: 0 })
        setSystemsTotal(sys.total || 0)
      } catch {}
      try {
        const eps = await listAllEndpoints({ limit: 1, offset: 0 })
        setEndpointsTotal(eps.total || 0)
      } catch {}
      try {
        const now = new Date()
        const start = new Date(now)
        start.setHours(0, 0, 0, 0)
        const end = new Date(now)
        end.setHours(23, 59, 59, 999)
        const [succ, fail, rec] = await Promise.all([
          listSendRecords({ limit: 1, offset: 0, status: 1, start_time: toIso(start), end_time: toIso(end) }),
          listSendRecords({ limit: 1, offset: 0, status: -1, start_time: toIso(start), end_time: toIso(end) }),
          listSendRecords({ limit: 10, offset: 0 }),
        ])
        setTodaySuccess(succ.total || 0)
        setTodayFailed(fail.total || 0)
        setRecent(rec.items || [])
      } catch {}
    })()
  }, [])

  return (
    <div className="container space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">欢迎来到 Orion 控制台</h1>
        <p className="text-muted-foreground mt-1">
          统一的通知网关：配置渠道、管理模板、查看发送记录与状态。
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card title="业务系统" value={systemsTotal === null ? "…" : String(systemsTotal)} hint="接入系统数量" />
        <Card title="通知 API" value={endpointsTotal === null ? "…" : String(endpointsTotal)} hint="已配置的 API" />
        <Card title="今日发送" value={todaySuccess === null || todayFailed === null ? "…" : `${todaySuccess}/${todayFailed}`} hint="成功/失败" />
        <Card title="待重试" value={todayFailed === null ? "…" : String(todayFailed)} hint="失败待重试消息" />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border bg-card p-4">
          <h2 className="font-medium mb-2">最近发送</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-3 py-2 text-left">时间</th>
                  <th className="px-3 py-2 text-left">消息</th>
                  <th className="px-3 py-2 text-left">端点</th>
                  <th className="px-3 py-2 text-left">状态</th>
                </tr>
              </thead>
              <tbody>
                {recent.map((it) => (
                  <tr key={it.send_record_bid} className="border-t">
                    <td className="px-3 py-2 whitespace-nowrap">{it.send_time ? new Date(it.send_time).toLocaleString() : "-"}</td>
                    <td className="px-3 py-2">{it.message_name || it.message_definition_bid}</td>
                    <td className="px-3 py-2">{it.endpoint_name || it.notification_api_bid}</td>
                    <td className="px-3 py-2">{it.status === 1 ? "成功" : it.status === -1 ? "失败" : "待定"}</td>
                  </tr>
                ))}
                {recent.length === 0 && (
                  <tr>
                    <td colSpan={4} className="px-3 py-4 text-muted-foreground">暂无数据</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
        <div className="rounded-lg border bg-card p-4">
          <h2 className="font-medium mb-2">渠道健康</h2>
          <p className="text-sm text-muted-foreground">展示渠道可用性与限流情况（后续接入）。</p>
        </div>
      </div>
    </div>
  )
}
