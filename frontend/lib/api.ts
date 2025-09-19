const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000"

export function getToken(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem("orion_token")
}

export function setToken(token: string) {
  if (typeof window === "undefined") return
  localStorage.setItem("orion_token", token)
}

export function clearToken() {
  if (typeof window === "undefined") return
  localStorage.removeItem("orion_token")
}

export async function apiFetch(path: string, opts: RequestInit = {}) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(opts.headers as Record<string, string> | undefined),
  }
  const token = getToken()
  if (token) headers["Authorization"] = `Bearer ${token}`
  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers })
  if (!res.ok) {
    let detail: any
    try {
      detail = await res.json()
    } catch {
      detail = await res.text()
    }
    throw new Error(typeof detail === "string" ? detail : detail?.detail || "Request failed")
  }
  const ct = res.headers.get("content-type") || ""
  if (ct.includes("application/json")) return res.json()
  return res.text()
}

export async function login(username: string, password: string) {
  const data = await apiFetch("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  })
  if (data?.access_token) setToken(data.access_token)
  return data
}

export async function registerUser(username: string, password: string, email?: string) {
  return apiFetch("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, password, email: email || null }),
  })
}

export async function fetchUsers() {
  return apiFetch("/api/v1/users/")
}

// Business systems
export interface BusinessSystemPayload {
  name: string
  base_url?: string | null
  auth_method?: string | null
  app_id?: string | null
  app_secret?: string | null
  status?: number | null
}

export async function listSystems(params?: { limit?: number; offset?: number; q?: string }) {
  const qs = new URLSearchParams()
  if (params?.limit) qs.set("limit", String(params.limit))
  if (params?.offset) qs.set("offset", String(params.offset))
  if (params?.q) qs.set("q", params.q)
  const suffix = qs.toString() ? `?${qs.toString()}` : ""
  return apiFetch(`/api/v1/systems/${suffix}`)
}

export async function createSystem(payload: BusinessSystemPayload) {
  return apiFetch("/api/v1/systems/", { method: "POST", body: JSON.stringify(payload) })
}

export async function getSystem(bid: string) {
  return apiFetch(`/api/v1/systems/${bid}`)
}

export async function updateSystem(bid: string, payload: Partial<BusinessSystemPayload>) {
  return apiFetch(`/api/v1/systems/${bid}`, { method: "PATCH", body: JSON.stringify(payload) })
}

export async function deleteSystem(bid: string) {
  return apiFetch(`/api/v1/systems/${bid}`, { method: "DELETE" })
}
