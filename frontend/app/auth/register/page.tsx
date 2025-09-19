"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { registerUser, login } from "@/lib/api"
import Link from "next/link"

export default function RegisterPage() {
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await registerUser(username, password, email || undefined)
      // Auto login
      await login(username, password)
      router.push("/users")
    } catch (err: any) {
      setError(err.message || "注册失败")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container max-w-md">
      <h1 className="text-2xl font-semibold mb-4">注册</h1>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Label htmlFor="username">用户名</Label>
          <Input id="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div className="space-y-1">
          <Label htmlFor="email">邮箱（可选）</Label>
          <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div className="space-y-1">
          <Label htmlFor="password">密码</Label>
          <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? "注册中..." : "注册并登录"}
        </Button>
      </form>
      <p className="mt-3 text-sm text-muted-foreground">
        已有账号？
        <Link className="text-primary underline-offset-2 hover:underline ml-1" href="/auth/login">
          去登录
        </Link>
      </p>
    </div>
  )
}
