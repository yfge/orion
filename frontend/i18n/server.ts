import { cookies, headers } from "next/headers";
import { DEFAULT_LOCALE } from "@/i18n/locales";

export function getLocaleServer(): "zh-CN" | "en-US" {
  const cookieStore = cookies();
  const cookieLang = cookieStore.get("LANG")?.value;
  if (cookieLang === "zh-CN" || cookieLang === "en-US") return cookieLang;
  const al = (headers().get("accept-language") || "").toLowerCase();
  if (al.includes("en")) return "en-US";
  return DEFAULT_LOCALE;
}
