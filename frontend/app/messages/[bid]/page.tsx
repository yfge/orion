"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { getMessageDef, updateMessageDef, deleteMessageDef } from "@/lib/api"

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

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getMessageDef(bid)
        setName(data.name || "")
        setType(data.type || "text")
        setSchemaText(JSON.stringify(data.schema || {}, null, 2))
        setStatus(typeof data.status === "number" ? data.status : 0)
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
    </div>
  )
}

