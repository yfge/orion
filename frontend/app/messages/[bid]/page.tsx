"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { getMessageDef, updateMessageDef, deleteMessageDef, listAllEndpoints, listDispatches, createDispatch, updateDispatch, deleteDispatch } from "@/lib/api"

export default function EditMessagePage() {
  const params = useParams<{ bid: string }>()
  const bid = params?.bid as string
  const router = useRouter()

  const [name, setName] = useState("")
  const [type, setType] = useState("text")
  const [schemaText, setSchemaText] = useState("{}")
  const [status, setStatus] = useState<number>(0)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [endpoints, setEndpoints] = useState<any[]>([])
  const [dispatches, setDispatches] = useState<any[]>([])
  const [newEndpointBid, setNewEndpointBid] = useState("")
  const [newMappingText, setNewMappingText] = useState("{}")
  const [newEnabled, setNewEnabled] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getMessageDef(bid)
        setName(data.name || "")
        setType(data.type || "text")
        setSchemaText(JSON.stringify(data.schema || {}, null, 2))
        setStatus(typeof data.status === "number" ? data.status : 0)
        const eps = await listAllEndpoints({ limit: 500, offset: 0 })
        setEndpoints(eps.items || [])
        const dps = await listDispatches(bid)
        setDispatches(dps.items || [])
      } catch (e: any) {
        setError(e.message || "加载失败")
      } finally {
        setLoading(false)
      }
    }
    if (bid) load()
  }, [bid])

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const schema = schemaText ? JSON.parse(schemaText) : null
      await updateMessageDef(bid, { name, type, schema, status })
      router.push("/messages")
    } catch (e: any) {
      setError(e.message || "保存失败，检查 Schema JSON 是否有效")
    } finally {
      setLoading(false)
    }
  }

  const onDelete = async () => {
    if (!confirm("确认删除该消息定义？")) return
    try {
      await deleteMessageDef(bid)
      router.push("/messages")
    } catch (e: any) {
      alert(e.message || "删除失败")
    }
  }

  const onAddDispatch = async () => {
    try {
      const mapping = newMappingText ? JSON.parse(newMappingText) : null
      await createDispatch(bid, { endpoint_bid: newEndpointBid, mapping, enabled: newEnabled })
      const dps = await listDispatches(bid)
      setDispatches(dps.items || [])
      setNewMappingText("{}")
      setNewEndpointBid("")
      setNewEnabled(true)
    } catch (e: any) {
      alert(e.message || "新增映射失败")
    }
  }

  const onDeleteDispatch = async (dispatchBid: string) => {
    if (!confirm("确认删除映射？")) return
    try {
      await deleteDispatch(dispatchBid)
      const dps = await listDispatches(bid)
      setDispatches(dps.items || [])
    } catch (e: any) {
      alert(e.message || "删除失败")
    }
  }

  if (loading && !name) return <div className="container">加载中...</div>

  return (
    <div className="container max-w-2xl">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">编辑消息定义</h1>
        <Button variant="outline" onClick={onDelete} className="text-red-600 border-red-600">删除</Button>
      </div>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Label htmlFor="name">名称</Label>
          <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="type">类型</Label>
            <select id="type" className="border rounded-md h-9 px-3 text-sm w-full" value={type} onChange={(e) => setType(e.target.value)}>
              <option value="text">text</option>
              <option value="markdown">markdown</option>
              <option value="template">template</option>
              <option value="custom">custom</option>
            </select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="status">状态</Label>
            <Input id="status" type="number" value={status} onChange={(e) => setStatus(Number(e.target.value))} />
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="schema">Schema JSON</Label>
          <Textarea id="schema" className="font-mono" value={schemaText} onChange={(e) => setSchemaText(e.target.value)} />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>{loading ? "保存中..." : "保存"}</Button>
          <Button type="button" variant="outline" onClick={() => router.push("/messages")}>取消</Button>
        </div>
      </form>
      <div className="space-y-3 mt-6">
        <h2 className="text-xl font-semibold">派发映射（Message → Endpoints）</h2>
        <div className="rounded-lg border p-3 space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <Label htmlFor="endpoint">选择端点</Label>
              <select id="endpoint" className="border rounded-md h-9 px-3 text-sm w-full" value={newEndpointBid} onChange={(e) => setNewEndpointBid(e.target.value)}>
                <option value="">选择一个端点</option>
                {endpoints.map((ep) => (
                  <option key={ep.notification_api_bid} value={ep.notification_api_bid}>
                    {ep.name} ({ep.business_system_bid})
                  </option>
                ))}
              </select>
            </div>
            <div className="space-y-1">
              <Label htmlFor="enabled">启用</Label>
              <select id="enabled" className="border rounded-md h-9 px-3 text-sm w-full" value={newEnabled ? "1" : "0"} onChange={(e) => setNewEnabled(e.target.value === "1") }>
                <option value="1">是</option>
                <option value="0">否</option>
              </select>
            </div>
          </div>
          <div className="space-y-1">
            <Label htmlFor="mapping">Mapping JSON（可选）</Label>
            <Textarea id="mapping" className="font-mono" value={newMappingText} onChange={(e) => setNewMappingText(e.target.value)} />
          </div>
          <div>
            <Button type="button" onClick={onAddDispatch} disabled={!newEndpointBid}>新增映射</Button>
          </div>
        </div>

        <div className="overflow-x-auto rounded-lg border">
          <table className="min-w-full text-sm">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-3 py-2 text-left">端点</th>
                <th className="px-3 py-2 text-left">系统</th>
                <th className="px-3 py-2 text-left">启用</th>
                <th className="px-3 py-2 text-left">操作</th>
              </tr>
            </thead>
            <tbody>
              {dispatches.map((d) => (
                <tr key={d.message_dispatch_bid} className="border-t">
                  <td className="px-3 py-2">{d.endpoint_name || d.endpoint_bid}</td>
                  <td className="px-3 py-2 text-muted-foreground">{d.business_system_bid || "—"}</td>
                  <td className="px-3 py-2">{d.enabled ? "是" : "否"}</td>
                  <td className="px-3 py-2">
                    <button onClick={() => onDeleteDispatch(d.message_dispatch_bid)} className="text-red-600 hover:underline">删除</button>
                  </td>
                </tr>
              ))}
              {dispatches.length === 0 && (
                <tr>
                  <td className="px-3 py-4 text-muted-foreground" colSpan={4}>暂无映射</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
