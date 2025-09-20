"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { RjsfForm } from "@/components/jsonschema/RjsfForm"
import { validateSchema } from "@/lib/api"
import { createMessageDef } from "@/lib/api"

export default function NewMessagePage() {
  const router = useRouter()
  const [name, setName] = useState("")
  const [type, setType] = useState("text")
  const [schemaText, setSchemaText] = useState("{\n  \"msg_type\": \"text\",\n  \"content\": { \"text\": \"${text}\" }\n}")
  const [status, setStatus] = useState<number>(0)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [sampleDataText, setSampleDataText] = useState("{\n  \"text\": \"你好 Orion\"\n}")
  const [previewValue, setPreviewValue] = useState<any>({})
  const [validateResult, setValidateResult] = useState<string | null>(null)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const schema = schemaText ? JSON.parse(schemaText) : null
      await createMessageDef({ name, type, schema, status })
      router.push("/messages")
    } catch (e: any) {
      setError(e.message || "创建失败，检查 Schema JSON 是否有效")
    } finally {
      setLoading(false)
    }
  }

  function safeParse(text: string) {
    try { return JSON.parse(text || '{}') } catch { return {} }
  }

  return (
    <div className="container max-w-2xl">
      <h1 className="text-2xl font-semibold mb-4">新建消息定义</h1>
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
        <div className="space-y-2">
          <Label>Schema 预览表单（RJSF）</Label>
          <RjsfForm schema={safeParse(schemaText)} formData={previewValue} onChange={setPreviewValue} />
        </div>
        <div className="space-y-1">
          <Label htmlFor="sample">示例数据（用于校验）</Label>
          <Textarea id="sample" className="font-mono" value={sampleDataText} onChange={(e) => setSampleDataText(e.target.value)} />
          <div>
            <Button type="button" variant="outline" onClick={async () => {
              try {
                const res = await validateSchema({ schema: safeParse(schemaText), data: JSON.parse(sampleDataText) })
                setValidateResult(res.valid ? "校验通过" : `校验失败: ${(res.errors||[]).map((e:any)=>e.message).join('; ')}`)
              } catch (e:any) {
                setValidateResult(e.message || '校验异常')
              }
            }}>校验示例数据</Button>
            {validateResult && <p className="text-xs text-muted-foreground mt-1">{validateResult}</p>}
          </div>
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>{loading ? "创建中..." : "创建"}</Button>
          <Button type="button" variant="outline" onClick={() => router.push("/messages")}>取消</Button>
        </div>
      </form>
    </div>
  )
}
