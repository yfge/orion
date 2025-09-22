import "./globals.css";
import { Inter } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider";
import { Navbar } from "@/components/navbar";
import { AuthGate } from "@/components/auth-gate";
import { Sidebar } from "@/components/sidebar";
import { cookies, headers } from "next/headers";
import { I18nProvider } from "@/i18n/provider";
import { DEFAULT_LOCALE } from "@/i18n/locales";
import zhCN from "../messages/zh-CN.json";
import enUS from "../messages/en-US.json";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Orion Console",
  description: "Notification gateway control center",
};

function pickLocale(): "zh-CN" | "en-US" {
  const cookieStore = cookies();
  const cookieLang = cookieStore.get("LANG")?.value;
  if (cookieLang === "zh-CN" || cookieLang === "en-US") return cookieLang;
  // Fallback to Accept-Language
  const al = headers().get("accept-language") || "";
  const lower = al.toLowerCase();
  if (lower.includes("en")) return "en-US";
  return DEFAULT_LOCALE;
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const locale = pickLocale();
  const messages =
    locale === "en-US"
      ? (enUS as Record<string, string>)
      : (zhCN as Record<string, string>);
  return (
    <html lang={locale} suppressHydrationWarning>
      <body className={inter.className}>
        <I18nProvider locale={locale} messages={messages}>
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            <div className="min-h-screen grid grid-rows-[auto,1fr]">
              <Navbar />
              <div className="grid grid-cols-1 lg:grid-cols-[240px_1fr]">
                <aside className="hidden lg:block border-r bg-card/50">
                  <Sidebar />
                </aside>
                <main className="p-4 md:p-6 lg:p-8">
                  <AuthGate>{children}</AuthGate>
                </main>
              </div>
            </div>
          </ThemeProvider>
        </I18nProvider>
      </body>
    </html>
  );
}
