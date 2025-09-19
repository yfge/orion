"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { getEndpoint, updateEndpoint, deleteEndpoint, listAuthProfiles } from "@/lib/api"

export default function EditEndpointPage() {
  const params = useParams<{ bid: string; endpointBid: string }>()
  const systemBid = params?.bid as string
  const endpointBid = params?.endpointBid as string
  const router = useRouter()

  const [name, setName] = useState("")
  const [transport, setTransport] = useState("")
  const [adapterKey, setAdapterKey] = useState("")
  const [endpointUrl, setEndpointUrl] = useState("")
  const [configText, setConfigText] = useState("{}")
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [authProfiles, setAuthProfiles] = useState<any[]>([])
  const [authProfileBid, setAuthProfileBid] = useState("")

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getEndpoint(endpointBid)
        setName(data.name || "")
        setTransport(data.transport || "")
        setAdapterKey(data.adapter_key || "")
        setEndpointUrl(data.endpoint_url || "")
        setConfigText(JSON.stringify(data.config || {}, null, 2))
        setAuthProfileBid(data.auth_profile_bid || "")
      } catch (err: any) {
        setError(err.message || "加载失败")
      } finally {
        setLoading(false)
      }
    }
    if (endpointBid) load()
    ;(async () => {
      try {
        const res = await listAuthProfiles({ limit: 100, offset: 0 })
        setAuthProfiles(res.items || [])
      } catch {}
    })()
  }, [endpointBid])

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const cfg = configText ? JSON.parse(configText) : null
      await updateEndpoint(endpointBid, {
        name,
        transport,
        adapter_key: adapterKey || null,
        endpoint_url: endpointUrl || null,
        config: cfg,
        auth_profile_bid: authProfileBid || null,
      })
      router.push(`/systems/${systemBid}`)
    } catch (err: any) {
      setError(err.message || "保存失败，检查配置 JSON 是否有效")
    } finally {
      setLoading(false)
    }
  }

  const onDelete = async () => {
    if (!confirm("确认删除该端点？")) return
    try {
      await deleteEndpoint(endpointBid)
      router.push(`/systems/${systemBid}`)
    } catch (err: any) {
      alert(err.message || "删除失败")
    }
  }

  if (loading && !name) return <div className="container">加载中...</div>

  return (
    <div className="container max-w-2xl">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">编辑端点</h1>
        <Button variant="outline" onClick={onDelete} className="text-red-600 border-red-600">删除</Button>
      </div>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Label htmlFor="name">名称</Label>
          <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="transport">类型</Label>
            <select id="transport" className="border rounded-md h-9 px-3 text-sm w-full" value={transport} onChange={(e) => setTransport(e.target.value)}>
              <option value="http">http</option>
              <option value="mq">mq</option>
            </select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="adapterKey">适配器</Label>
            <Input id="adapterKey" value={adapterKey} onChange={(e) => setAdapterKey(e.target.value)} />
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="endpointUrl">地址（HTTP 可用）</Label>
          <Input id="endpointUrl" value={endpointUrl} onChange={(e) => setEndpointUrl(e.target.value)} />
        </div>
        <div className="space-y-1">
          <Label htmlFor="config">配置 JSON</Label>
          <Textarea id="config" value={configText} onChange={(e) => setConfigText(e.target.value)} className="font-mono" />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>{loading ? "保存中..." : "保存"}</Button>
          <Button type="button" variant="outline" onClick={() => router.push(`/systems/${systemBid}`)}>取消</Button>
        </div>
      </form>
    </div>
  )
}
        <div className="space-y-1">
          <Label htmlFor="authProfile">认证配置（可选）</Label>
          <select id="authProfile" className="border rounded-md h-9 px-3 text-sm w-full" value={authProfileBid} onChange={(e) => setAuthProfileBid(e.target.value)}>
            <option value="">不使用认证</option>
            {authProfiles.map((p) => (
              <option key={p.auth_profile_bid} value={p.auth_profile_bid}>{p.name} ({p.type})</option>
            ))}
          </select>
        </div>
