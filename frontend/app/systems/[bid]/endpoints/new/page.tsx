"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { createEndpoint, listAuthProfiles } from "@/lib/api"

export default function NewEndpointPage() {
  const params = useParams<{ bid: string }>()
  const systemBid = params?.bid as string
  const router = useRouter()

  const [name, setName] = useState("")
  const [transport, setTransport] = useState("http")
  const [adapterKey, setAdapterKey] = useState("")
  const [endpointUrl, setEndpointUrl] = useState("")
  const [configText, setConfigText] = useState("{\n  \"method\": \"POST\",\n  \"headers\": {\n    \"Content-Type\": \"application/json\"\n  }\n}")
  const [authProfiles, setAuthProfiles] = useState<any[]>([])
  const [authProfileBid, setAuthProfileBid] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const cfg = configText ? JSON.parse(configText) : null
      await createEndpoint(systemBid, {
        name,
        transport,
        adapter_key: adapterKey || null,
        endpoint_url: endpointUrl || null,
        config: cfg,
        auth_profile_bid: authProfileBid || null,
        status: 0,
      })
      router.push(`/systems/${systemBid}`)
    } catch (err: any) {
      setError(err.message || "创建失败，检查配置 JSON 是否有效")
    } finally {
      setLoading(false)
    }
  }

  const adapterOptions: Record<string, string[]> = {
    http: ["http.generic", "http.feishu_bot"],
    mq: ["mq.kafka", "mq.rabbit"],
  }

  // load auth profiles
  useEffect(() => {
    (async () => {
      try {
        const data = await listAuthProfiles({ limit: 100, offset: 0 })
        setAuthProfiles(data.items || [])
      } catch (e) {
        // ignore
      }
    })()
  }, [])

  return (
    <div className="container max-w-2xl">
      <h1 className="text-2xl font-semibold mb-4">新建端点</h1>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Label htmlFor="name">名称</Label>
          <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="transport">类型</Label>
            <select id="transport" className="border rounded-md h-9 px-3 text-sm w-full" value={transport} onChange={(e) => { setTransport(e.target.value); setAdapterKey("") }}>
              <option value="http">http</option>
              <option value="mq">mq</option>
            </select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="adapterKey">适配器</Label>
            <select id="adapterKey" className="border rounded-md h-9 px-3 text-sm w-full" value={adapterKey} onChange={(e) => setAdapterKey(e.target.value)}>
              <option value="">选择适配器</option>
              {(adapterOptions[transport] || []).map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="endpointUrl">地址（HTTP 可用）</Label>
          <Input id="endpointUrl" value={endpointUrl} onChange={(e) => setEndpointUrl(e.target.value)} placeholder="https://..." />
        </div>
        <div className="space-y-1">
          <Label htmlFor="authProfile">认证配置（可选）</Label>
          <select id="authProfile" className="border rounded-md h-9 px-3 text-sm w-full" value={authProfileBid} onChange={(e) => setAuthProfileBid(e.target.value)}>
            <option value="">不使用认证</option>
            {authProfiles.map((p) => (
              <option key={p.auth_profile_bid} value={p.auth_profile_bid}>{p.name} ({p.type})</option>
            ))}
          </select>
        </div>
        <div className="space-y-1">
          <Label htmlFor="config">配置 JSON</Label>
          <Textarea id="config" value={configText} onChange={(e) => setConfigText(e.target.value)} className="font-mono" />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>{loading ? "创建中..." : "创建"}</Button>
          <Button type="button" variant="outline" onClick={() => router.push(`/systems/${systemBid}`)}>取消</Button>
        </div>
      </form>
    </div>
  )
}
