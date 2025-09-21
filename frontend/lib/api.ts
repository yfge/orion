const isBrowser = typeof window !== "undefined";
// In browser, prefer same-origin '/api'. If NEXT_PUBLIC_API_BASE_URL is set, use it as a fallback for local dev without proxy.
const API_BASE = isBrowser
  ? process.env.NEXT_PUBLIC_API_BASE_URL || ""
  : process.env.INTERNAL_API_BASE_URL ||
    process.env.NEXT_PUBLIC_API_BASE_URL ||
    "http://backend:8000";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("orion_token");
}

export function setToken(token: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem("orion_token", token);
}

export function clearToken() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("orion_token");
}

export async function apiFetch(path: string, opts: RequestInit = {}) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(opts.headers as Record<string, string> | undefined),
  };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers });
  if (!res.ok) {
    let detail: any;
    try {
      detail = await res.json();
    } catch {
      detail = await res.text();
    }
    throw new Error(
      typeof detail === "string" ? detail : detail?.detail || "Request failed",
    );
  }
  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) return res.json();
  return res.text();
}

export async function login(username: string, password: string) {
  const data = await apiFetch("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  if (data?.access_token) setToken(data.access_token);
  return data;
}

export async function registerUser(
  username: string,
  password: string,
  email?: string,
) {
  return apiFetch("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, password, email: email || null }),
  });
}

export async function fetchUsers() {
  return apiFetch("/api/v1/users/");
}

// Business systems
export interface BusinessSystemPayload {
  name: string;
  base_url?: string | null;
  auth_method?: string | null;
  app_id?: string | null;
  app_secret?: string | null;
  status?: number | null;
}

export async function listSystems(params?: {
  limit?: number;
  offset?: number;
  q?: string;
}) {
  const qs = new URLSearchParams();
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  if (params?.q) qs.set("q", params.q);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiFetch(`/api/v1/systems/${suffix}`);
}

export async function createSystem(payload: BusinessSystemPayload) {
  return apiFetch("/api/v1/systems/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getSystem(bid: string) {
  return apiFetch(`/api/v1/systems/${bid}`);
}

export async function updateSystem(
  bid: string,
  payload: Partial<BusinessSystemPayload>,
) {
  return apiFetch(`/api/v1/systems/${bid}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteSystem(bid: string) {
  return apiFetch(`/api/v1/systems/${bid}`, { method: "DELETE" });
}

// Endpoints (Notification APIs)
export async function listEndpoints(params: {
  systemBid: string;
  limit?: number;
  offset?: number;
  q?: string;
}) {
  const qs = new URLSearchParams();
  if (params.limit) qs.set("limit", String(params.limit));
  if (params.offset) qs.set("offset", String(params.offset));
  if (params.q) qs.set("q", params.q);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiFetch(`/api/v1/systems/${params.systemBid}/endpoints${suffix}`);
}

export async function createEndpoint(systemBid: string, payload: any) {
  return apiFetch(`/api/v1/systems/${systemBid}/endpoints`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getEndpoint(endpointBid: string) {
  return apiFetch(`/api/v1/endpoints/${endpointBid}`);
}

export async function updateEndpoint(endpointBid: string, payload: any) {
  return apiFetch(`/api/v1/endpoints/${endpointBid}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteEndpoint(endpointBid: string) {
  return apiFetch(`/api/v1/endpoints/${endpointBid}`, { method: "DELETE" });
}

// Auth profiles
export async function listAuthProfiles(params?: {
  limit?: number;
  offset?: number;
  q?: string;
}) {
  const qs = new URLSearchParams();
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  if (params?.q) qs.set("q", params.q);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiFetch(`/api/v1/auth-profiles/${suffix}`);
}

export async function sendTestToEndpoint(endpointBid: string, text: string) {
  return apiFetch(`/api/v1/endpoints/${endpointBid}/send-test`, {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}

// Message definitions
export async function listMessageDefs(params?: {
  limit?: number;
  offset?: number;
  q?: string;
}) {
  const qs = new URLSearchParams();
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  if (params?.q) qs.set("q", params.q);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiFetch(`/api/v1/message-definitions/${suffix}`);
}

export async function createMessageDef(payload: {
  name: string;
  type?: string | null;
  schema?: any;
  status?: number | null;
}) {
  return apiFetch(`/api/v1/message-definitions/`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getMessageDef(bid: string) {
  return apiFetch(`/api/v1/message-definitions/${bid}`);
}

export async function updateMessageDef(
  bid: string,
  payload: Partial<{
    name: string;
    type: string | null;
    schema: any;
    status: number | null;
  }>,
) {
  return apiFetch(`/api/v1/message-definitions/${bid}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteMessageDef(bid: string) {
  return apiFetch(`/api/v1/message-definitions/${bid}`, { method: "DELETE" });
}

// Dispatches
export async function listAllEndpoints(params?: {
  limit?: number;
  offset?: number;
  q?: string;
}) {
  const qs = new URLSearchParams();
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  if (params?.q) qs.set("q", params.q);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiFetch(`/api/v1/endpoints${suffix}`);
}

export async function listDispatches(messageBid: string) {
  return apiFetch(`/api/v1/message-definitions/${messageBid}/dispatches`);
}

export async function createDispatch(
  messageBid: string,
  payload: { endpoint_bid: string; mapping?: any; enabled?: boolean },
) {
  return apiFetch(`/api/v1/message-definitions/${messageBid}/dispatches`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateDispatch(
  dispatchBid: string,
  payload: Partial<{ endpoint_bid: string; mapping: any; enabled: boolean }>,
) {
  return apiFetch(`/api/v1/dispatches/${dispatchBid}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteDispatch(dispatchBid: string) {
  return apiFetch(`/api/v1/dispatches/${dispatchBid}`, { method: "DELETE" });
}

export async function listDispatchesByEndpoint(endpointBid: string) {
  return apiFetch(`/api/v1/endpoints/${endpointBid}/dispatches`);
}

export async function createDispatchForEndpoint(
  endpointBid: string,
  payload: { message_definition_bid: string; mapping?: any; enabled?: boolean },
) {
  return apiFetch(`/api/v1/endpoints/${endpointBid}/dispatches`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function validateSchema(payload: { schema: any; data: any }) {
  return apiFetch(`/api/v1/schema/validate`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// Send records
export async function listSendRecords(params?: {
  limit?: number;
  offset?: number;
  message_definition_bid?: string;
  notification_api_bid?: string;
  status?: number;
  start_time?: string;
  end_time?: string;
}) {
  const qs = new URLSearchParams();
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  if (params?.message_definition_bid)
    qs.set("message_definition_bid", params.message_definition_bid);
  if (params?.notification_api_bid)
    qs.set("notification_api_bid", params.notification_api_bid);
  if (typeof params?.status === "number")
    qs.set("status", String(params.status));
  if (params?.start_time) qs.set("start_time", params.start_time);
  if (params?.end_time) qs.set("end_time", params.end_time);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiFetch(`/api/v1/send-records/${suffix}`);
}

export async function getSendRecord(bid: string) {
  return apiFetch(`/api/v1/send-records/${bid}`);
}

export async function listSendDetails(
  bid: string,
  params?: { limit?: number; offset?: number },
) {
  const qs = new URLSearchParams();
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiFetch(`/api/v1/send-records/${bid}/details${suffix}`);
}

// API Keys
export async function listApiKeys(params?: {
  limit?: number;
  offset?: number;
}) {
  const qs = new URLSearchParams();
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiFetch(`/api/v1/api-keys/${suffix}`);
}

export async function createApiKey(payload: {
  name: string;
  description?: string | null;
}) {
  return apiFetch(`/api/v1/api-keys/`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function deleteApiKey(bid: string) {
  return apiFetch(`/api/v1/api-keys/${bid}`, { method: "DELETE" });
}
