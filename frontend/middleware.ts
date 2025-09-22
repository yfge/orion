import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const SUPPORTED = ["zh-CN", "en-US"];
const DEFAULT = "zh-CN";

export function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const cookie = req.cookies.get("LANG")?.value;
  if (cookie && SUPPORTED.includes(cookie)) {
    return res;
  }
  // derive from Accept-Language
  const al = req.headers.get("accept-language")?.toLowerCase() || "";
  const lang = al.includes("en") ? "en-US" : DEFAULT;
  res.cookies.set({
    name: "LANG",
    value: lang,
    path: "/",
    maxAge: 60 * 60 * 24 * 365,
  });
  return res;
}

export const config = {
  // Run on all HTML pages
  matcher: "/((?!api|_next|.*..*).*)",
};
