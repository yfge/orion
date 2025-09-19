"use client"

import { useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { createEndpoint } from "@/lib/api"

export default function NewEndpointPage() {
  const params = useParams<{ bid: string }>()
  const systemBid = params?.bid as string
  const router = useRouter()

  const [name, setName] = useState("")
  const [transport, setTransport] = useState("http")
  const [adapterKey, setAdapterKey] = useState("")
  const [endpointUrl, setEndpointUrl] = useState("")
  const [configText, setConfigText] = useState("{\n  \"method\": \"POST\",\n  \"headers\": {\n    \"Content-Type\": \"application/json\"\n  }\n}")
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
        status: 0,
      })
      router.push(`/systems/${systemBid}`)
    } catch (err: any) {
      setError(err.message || "创建失败，检查配置 JSON 是否有效")
    } finally {
      setLoading(false)
    }
  }

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
            <Input id="transport" value={transport} onChange={(e) => setTransport(e.target.value)} placeholder="http 或 mq" />
          </div>
          <div className="space-y-1">
            <Label htmlFor="adapterKey">适配器</Label>
            <Input id="adapterKey" value={adapterKey} onChange={(e) => setAdapterKey(e.target.value)} placeholder="http.generic / http.feishu_bot / mq.kafka / mq.rabbit" />
          </div>
        </div>
        <div className="space-y-1">
          <Label htmlFor="endpointUrl">地址（HTTP 可用）</Label>
          <Input id="endpointUrl" value={endpointUrl} onChange={(e) => setEndpointUrl(e.target.value)} placeholder="https://..." />
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

