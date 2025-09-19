"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { createMessageDef } from "@/lib/api"

export default function NewMessagePage() {
  const router = useRouter()
  const [name, setName] = useState("")
  const [type, setType] = useState("text")
  const [schemaText, setSchemaText] = useState("{\n  \"msg_type\": \"text\",\n  \"content\": { \"text\": \"${text}\" }\n}")
  const [status, setStatus] = useState<number>(0)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

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
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>{loading ? "创建中..." : "创建"}</Button>
          <Button type="button" variant="outline" onClick={() => router.push("/messages")}>取消</Button>
        </div>
      </form>
    </div>
  )
}

