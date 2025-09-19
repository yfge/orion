"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { getSystem, updateSystem, deleteSystem, listEndpoints } from "@/lib/api"
import Link from "next/link"

export default function EditSystemPage() {
  const params = useParams<{ bid: string }>()
  const bid = params?.bid as string
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [name, setName] = useState("")
  const [baseUrl, setBaseUrl] = useState("")
  const [authMethod, setAuthMethod] = useState("")
  const [appId, setAppId] = useState("")
  const [appSecret, setAppSecret] = useState("")
  const [status, setStatus] = useState<number>(0)
  const router = useRouter()
  const [endpoints, setEndpoints] = useState<any[]>([])

  const load = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getSystem(bid)
      setName(data.name || "")
      setBaseUrl(data.base_url || "")
      setAuthMethod(data.auth_method || "")
      setAppId(data.app_id || "")
      setAppSecret(data.app_secret || "")
      setStatus(typeof data.status === "number" ? data.status : 0)
      // load endpoints
      const eps = await listEndpoints({ systemBid: bid, limit: 50, offset: 0 })
      setEndpoints(eps.items || [])
    } catch (err: any) {
      setError(err.message || "加载失败")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (bid) load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bid])

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await updateSystem(bid, { name, base_url: baseUrl || null, auth_method: authMethod || null, app_id: appId || null, app_secret: appSecret || null, status })
      router.push("/systems")
    } catch (err: any) {
      setError(err.message || "保存失败")
    } finally {
      setLoading(false)
    }
  }

  const onDelete = async () => {
    if (!confirm("确认删除该业务系统？")) return
    try {
      await deleteSystem(bid)
      router.push("/systems")
    } catch (err: any) {
      alert(err.message || "删除失败")
    }
  }

  if (loading && !name) return <div className="container">加载中...</div>

  return (
    <div className="container max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">编辑业务系统</h1>
        <Button variant="outline" onClick={onDelete} className="text-red-600 border-red-600">删除</Button>
      </div>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Label htmlFor="name">名称</Label>
          <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div className="space-y-1">
          <Label htmlFor="baseUrl">地址</Label>
          <Input id="baseUrl" value={baseUrl} onChange={(e) => setBaseUrl(e.target.value)} placeholder="https://..." />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="authMethod">鉴权方式</Label>
            <Input id="authMethod" value={authMethod} onChange={(e) => setAuthMethod(e.target.value)} placeholder="token/basic/..." />
          </div>
          <div className="space-y-1">
            <Label htmlFor="status">状态</Label>
            <Input id="status" type="number" value={status} onChange={(e) => setStatus(Number(e.target.value))} />
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="appId">app_id</Label>
            <Input id="appId" value={appId} onChange={(e) => setAppId(e.target.value)} />
          </div>
          <div className="space-y-1">
            <Label htmlFor="appSecret">app_secret</Label>
            <Input id="appSecret" value={appSecret} onChange={(e) => setAppSecret(e.target.value)} />
          </div>
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>{loading ? "保存中..." : "保存"}</Button>
          <Button type="button" variant="outline" onClick={() => router.push("/systems")}>取消</Button>
        </div>
      </form>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">端点（Endpoints）</h2>
          <Link href={`/systems/${bid}/endpoints/new`} className="text-primary hover:underline">新建端点</Link>
        </div>
        <div className="overflow-x-auto rounded-lg border">
          <table className="min-w-full text-sm">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-3 py-2 text-left">名称</th>
                <th className="px-3 py-2 text-left">类型</th>
                <th className="px-3 py-2 text-left">适配器</th>
                <th className="px-3 py-2 text-left">地址</th>
                <th className="px-3 py-2 text-left">操作</th>
              </tr>
            </thead>
            <tbody>
              {endpoints.map((ep) => (
                <tr key={ep.notification_api_bid} className="border-t">
                  <td className="px-3 py-2">{ep.name}</td>
                  <td className="px-3 py-2">{ep.transport || "http"}</td>
                  <td className="px-3 py-2">{ep.adapter_key || "—"}</td>
                  <td className="px-3 py-2 text-muted-foreground">{ep.endpoint_url || ep.config?.url || "—"}</td>
                  <td className="px-3 py-2">
                    <Link href={`/systems/${bid}/endpoints/${ep.notification_api_bid}`} className="text-primary hover:underline">编辑</Link>
                  </td>
                </tr>
              ))}
              {endpoints.length === 0 && (
                <tr>
                  <td className="px-3 py-4 text-muted-foreground" colSpan={5}>暂无端点</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
