import "./globals.css"
import { Inter } from "next/font/google"
import { ThemeProvider } from "@/components/theme-provider"
import { Navbar } from "@/components/navbar"
import { Sidebar } from "@/components/sidebar"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "Orion Console",
  description: "Notification gateway control center",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <div className="min-h-screen grid grid-rows-[auto,1fr]">
            <Navbar />
            <div className="grid grid-cols-1 lg:grid-cols-[240px_1fr]">
              <aside className="hidden lg:block border-r bg-card/50">
                <Sidebar />
              </aside>
              <main className="p-4 md:p-6 lg:p-8">{children}</main>
            </div>
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}

