"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { listSystems, listAuthProfiles, createEndpoint, validateSchema } from "@/lib/api"
import { endpointConfigSchemaFor } from "@/lib/schemas"
import { RjsfForm } from "@/components/jsonschema/RjsfForm"

export default function NewApiPage() {
  const router = useRouter()
  const [mounted, setMounted] = useState(false)
  const [systems, setSystems] = useState<any[]>([])
  const [systemBid, setSystemBid] = useState("")
  const [name, setName] = useState("")
  const [transport, setTransport] = useState("http")
  const [adapterKey, setAdapterKey] = useState("http.generic")
  const [endpointUrl, setEndpointUrl] = useState("")
  const [authProfiles, setAuthProfiles] = useState<any[]>([])
  const [authProfileBid, setAuthProfileBid] = useState("")
  const [configObj, setConfigObj] = useState<any>({})
  const [configText, setConfigText] = useState("{}")
  const [validateMsg, setValidateMsg] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setMounted(true)
    ;(async () => {
      try {
        const s = await listSystems({ limit: 200, offset: 0 })
        setSystems(s.items || [])
      } catch {}
      try {
        const ap = await listAuthProfiles({ limit: 200, offset: 0 })
        setAuthProfiles(ap.items || [])
      } catch {}
    })()
  }, [])

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!systemBid) { setError("请选择业务系统"); return }
    setLoading(true)
    setError(null)
    try {
      const cfg = configObj ?? (configText ? JSON.parse(configText) : null)
      await createEndpoint(systemBid, {
        name,
        transport,
        adapter_key: adapterKey || null,
        endpoint_url: endpointUrl || null,
        config: cfg,
        auth_profile_bid: authProfileBid || null,
        status: 0,
      })
      router.push("/apis")
    } catch (err: any) {
      setError(err.message || "创建失败，请检查表单与配置")
    } finally {
      setLoading(false)
    }
  }

  const configSchema = endpointConfigSchemaFor(adapterKey)

  if (!mounted) {
    return <div className="container max-w-2xl">加载中...</div>
  }

  return (
    <div className="container max-w-2xl space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">新建通知 API</h1>
      </div>
      {systems.length === 0 && (
        <div className="rounded-md border p-3 text-sm text-muted-foreground">
          未找到业务系统，请先
          <Link href="/systems/new" className="text-primary hover:underline ml-1">新建业务系统</Link>
          ，再回来创建通知 API。
        </div>
      )}
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="system">业务系统</Label>
            <select id="system" className="border rounded-md h-9 px-3 text-sm w-full" value={systemBid} onChange={(e) => setSystemBid(e.target.value)} required>
              <option value="">选择业务系统</option>
              {systems.map((s) => (
                <option key={s.business_system_bid} value={s.business_system_bid}>{s.name}</option>
              ))}
            </select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="name">名称</Label>
            <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="transport">类型</Label>
            <select id="transport" className="border rounded-md h-9 px-3 text-sm w-full" value={transport} onChange={(e) => { const v = e.target.value; setTransport(v); if (v === 'http') setAdapterKey('http.generic'); if (v === 'smtp') setAdapterKey('smtp.generic') }}>
              <option value="http">http</option>
              <option value="smtp">smtp</option>
              <option value="mq">mq</option>
            </select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="adapter">适配器</Label>
            <select id="adapter" className="border rounded-md h-9 px-3 text-sm w-full" value={adapterKey} onChange={(e) => setAdapterKey(e.target.value)}>
            {transport === 'http' ? (
              <>
                <option value="http.generic">http.generic</option>
                <option value="http.feishu_bot">http.feishu_bot</option>
                <option value="http.mailgun">http.mailgun</option>
                <option value="http.sendgrid">http.sendgrid</option>
              </>
            ) : transport === 'smtp' ? (
                <>
                  <option value="smtp.generic">smtp.generic</option>
                </>
              ) : (
                <>
                  <option value="mq.kafka">mq.kafka</option>
                  <option value="mq.rabbit">mq.rabbit</option>
                </>
              )}
            </select>
          </div>
        </div>

        {transport === 'http' && (
          <div className="space-y-1">
            <Label htmlFor="url">地址（HTTP 可用）</Label>
            <Input id="url" value={endpointUrl} onChange={(e) => setEndpointUrl(e.target.value)} placeholder="https://..." />
          </div>
        )}

        <div className="space-y-1">
          <Label htmlFor="auth">认证配置（可选）</Label>
          <select id="auth" className="border rounded-md h-9 px-3 text-sm w-full" value={authProfileBid} onChange={(e) => setAuthProfileBid(e.target.value)}>
            <option value="">不使用认证</option>
            {authProfiles.map((p) => (
              <option key={p.auth_profile_bid} value={p.auth_profile_bid}>{p.name} ({p.type})</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label>配置（Schema 表单）</Label>
          <RjsfForm schema={configSchema} formData={configObj} onChange={(v) => { setConfigObj(v); setConfigText(JSON.stringify(v ?? {}, null, 2)) }} />
          <div className="flex items-center gap-2">
            <Button type="button" variant="outline" onClick={async () => {
              try {
                const res = await validateSchema({ schema: configSchema, data: configObj })
                setValidateMsg(res.valid ? "配置校验通过" : `校验失败: ${(res.errors||[]).map((e:any)=>e.message).join('; ')}`)
              } catch (e:any) { setValidateMsg(e.message || '校验异常') }
            }}>校验配置</Button>
            {validateMsg && <p className="text-xs text-muted-foreground">{validateMsg}</p>}
          </div>
        </div>

        <div className="space-y-1">
          <Label htmlFor="config">配置 JSON（高级）</Label>
          <Textarea id="config" value={configText} onChange={(e) => { setConfigText(e.target.value); try { setConfigObj(JSON.parse(e.target.value || '{}')) } catch {} }} className="font-mono" />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex items-center gap-2">
          <Button type="submit" disabled={loading || !systemBid}>{loading ? "创建中..." : "创建"}</Button>
          <Button type="button" variant="outline" onClick={() => router.push("/apis")}>取消</Button>
        </div>
      </form>
    </div>
  )
}
