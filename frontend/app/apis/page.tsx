"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { listAllEndpoints, listSystems } from "@/lib/api"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function ApisPage() {
  const [q, setQ] = useState("")
  const [items, setItems] = useState<any[]>([])
  const [total, setTotal] = useState(0)
  const [limit] = useState(50)
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(false)
  const [systems, setSystems] = useState<any[]>([])
  const [newSystemBid, setNewSystemBid] = useState("")

  const load = async () => {
    setLoading(true)
    try {
      const res = await listAllEndpoints({ limit, offset, q: q || undefined })
      setItems(res.items || [])
      setTotal(res.total || 0)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [offset])

  useEffect(() => {
    ;(async () => {
      try {
        const s = await listSystems({ limit: 500, offset: 0 })
        setSystems(s.items || [])
      } catch {}
    })()
  }, [])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">通知 API</h1>
        <Link href="/apis/new" className="inline-flex items-center rounded-md border px-3 h-9 text-sm border-input text-foreground hover:bg-accent">新建</Link>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <Input placeholder="按名称搜索" value={q} onChange={(e) => setQ(e.target.value)} className="w-64" />
        <Button type="button" variant="outline" onClick={() => { setOffset(0); load() }} disabled={loading}>搜索</Button>
        <div className="ml-auto" />
      </div>

      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-3 py-2 text-left">名称</th>
              <th className="px-3 py-2 text-left">系统</th>
              <th className="px-3 py-2 text-left">类型</th>
              <th className="px-3 py-2 text-left">适配器</th>
              <th className="px-3 py-2 text-left">地址</th>
              <th className="px-3 py-2 text-left">操作</th>
            </tr>
          </thead>
          <tbody>
            {items.map((ep) => (
              <tr key={ep.notification_api_bid} className="border-t">
                <td className="px-3 py-2">{ep.name}</td>
                <td className="px-3 py-2 text-muted-foreground">{ep.business_system_bid || "—"}</td>
                <td className="px-3 py-2">{ep.transport || "—"}</td>
                <td className="px-3 py-2">{ep.adapter_key || "—"}</td>
                <td className="px-3 py-2 break-all">{ep.endpoint_url || "—"}</td>
                <td className="px-3 py-2">
                  {ep.business_system_bid ? (
                    <Link href={`/systems/${ep.business_system_bid}/endpoints/${ep.notification_api_bid}`} className="text-primary hover:underline">编辑</Link>
                  ) : (
                    <span className="text-muted-foreground">—</span>
                  )}
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td className="px-3 py-4 text-muted-foreground" colSpan={6}>暂无数据</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="outline" disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - limit))}>上一页</Button>
        <span className="text-sm text-muted-foreground">{offset + 1}-{Math.min(offset + limit, total)} / {total}</span>
        <Button variant="outline" disabled={offset + limit >= total} onClick={() => setOffset(offset + limit)}>下一页</Button>
      </div>
    </div>
  )
}
