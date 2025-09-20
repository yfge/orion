"use client"

import { useEffect, useMemo, useState } from "react"
import { fetchUsers, clearToken, getToken } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"

interface User {
  user_bid: string
  username: string
  email?: string | null
  status: number
}

export default function UsersPage() {
  const [mounted, setMounted] = useState(false)
  const [users, setUsers] = useState<User[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [q, setQ] = useState("")
  const router = useRouter()

  const load = async () => {
    setLoading(true)
    try {
      const data = await fetchUsers()
      setUsers(data)
    } catch (err: any) {
      const msg = err?.message || "加载失败"
      setError(msg)
      if (msg.toLowerCase().includes("invalid") || msg.includes("401")) {
        // 令牌失效或未登录
        clearToken()
        router.push("/auth/login")
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!getToken()) {
      router.push("/auth/login")
      return
    }
    setMounted(true)
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const filtered = useMemo(() => {
    const kw = (q || "").toLowerCase()
    if (!kw) return users
    return users.filter(u => (u.username || "").toLowerCase().includes(kw) || (u.email || "").toLowerCase().includes(kw) || (u.user_bid || "").toLowerCase().includes(kw))
  }, [q, users])

  if (!mounted) return <div className="container">加载中...</div>

  return (
    <div className="container space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">用户列表</h1>
        <div className="flex items-center gap-2">
          <input className="border rounded-md h-9 px-3 text-sm" placeholder="搜索用户名/邮箱/BID" value={q} onChange={(e)=>setQ(e.target.value)} />
          <Button variant="outline" onClick={load} disabled={loading}>{loading ? "刷新中..." : "刷新"}</Button>
          <Button variant="outline" onClick={() => router.push("/auth/register")}>注册新用户</Button>
          <Button variant="outline" onClick={() => { clearToken(); router.push("/auth/login") }}>退出登录</Button>
        </div>
      </div>
      <div className="text-sm text-muted-foreground">共 {filtered.length} 人</div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-3 py-2 text-left">用户名</th>
              <th className="px-3 py-2 text-left">邮箱</th>
              <th className="px-3 py-2 text-left">状态</th>
              <th className="px-3 py-2 text-left">BID</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((u) => (
              <tr key={u.user_bid} className="border-t">
                <td className="px-3 py-2">{u.username}</td>
                <td className="px-3 py-2 text-muted-foreground">{u.email || "—"}</td>
                <td className="px-3 py-2">{u.status}</td>
                <td className="px-3 py-2 text-muted-foreground">
                  <span>{u.user_bid}</span>
                  <Button
                    type="button"
                    variant="outline"
                    className="ml-2 h-7 px-2 text-xs"
                    onClick={() => navigator.clipboard.writeText(u.user_bid)}
                  >复制</Button>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td className="px-3 py-4 text-muted-foreground" colSpan={4}>暂无数据</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
