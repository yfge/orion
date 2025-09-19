"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { createSystem } from "@/lib/api"

export default function NewSystemPage() {
  const [name, setName] = useState("")
  const [baseUrl, setBaseUrl] = useState("")
  const [authMethod, setAuthMethod] = useState("")
  const [appId, setAppId] = useState("")
  const [appSecret, setAppSecret] = useState("")
  const [status, setStatus] = useState<number>(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await createSystem({ name, base_url: baseUrl || null, auth_method: authMethod || null, app_id: appId || null, app_secret: appSecret || null, status })
      router.push("/systems")
    } catch (err: any) {
      setError(err.message || "创建失败")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container max-w-2xl">
      <h1 className="text-2xl font-semibold mb-4">新建业务系统</h1>
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
          <Button type="submit" disabled={loading}>{loading ? "创建中..." : "创建"}</Button>
          <Button type="button" variant="outline" onClick={() => router.push("/systems")}>取消</Button>
        </div>
      </form>
    </div>
  )
}

