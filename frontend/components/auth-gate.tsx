"use client"

import { useEffect } from "react"
import { usePathname, useRouter } from "next/navigation"
import { getToken } from "@/lib/api"

export function AuthGate({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()

  useEffect(() => {
    const token = getToken()
    const isAuthPage = pathname?.startsWith("/auth")

    if (!token && !isAuthPage) {
      router.replace("/auth/login")
      return
    }

    if (token && isAuthPage) {
      router.replace("/users")
    }
  }, [pathname, router])

  return <>{children}</>
}

