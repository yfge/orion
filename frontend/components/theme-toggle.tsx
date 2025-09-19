"use client"

import { Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useTheme } from "next-themes"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  const next = theme === "dark" ? "light" : "dark"
  const Icon = theme === "dark" ? Sun : Moon

  return (
    <Button variant="outline" size="icon" aria-label="Toggle theme" onClick={() => setTheme(next)}>
      <Icon className="h-4 w-4" />
    </Button>
  )
}

