"use client"

import { useEffect, useState } from "react"
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
  const [users, setUsers] = useState<User[]>([])
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const load = async () => {
    try {
      const data = await fetchUsers()
      setUsers(data)
    } catch (err: any) {
      setError(err.message || "加载失败")
    }
  }

  useEffect(() => {
    if (!getToken()) {
      router.push("/auth/login")
      return
    }
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className="container space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">用户列表</h1>
        <Button variant="outline" onClick={() => { clearToken(); router.push("/auth/login") }}>退出登录</Button>
      </div>
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
            {users.map((u) => (
              <tr key={u.user_bid} className="border-t">
                <td className="px-3 py-2">{u.username}</td>
                <td className="px-3 py-2 text-muted-foreground">{u.email || "—"}</td>
                <td className="px-3 py-2">{u.status}</td>
                <td className="px-3 py-2 text-muted-foreground">{u.user_bid}</td>
              </tr>
            ))}
            {users.length === 0 && (
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

