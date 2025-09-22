"use client";

import Link from "next/link";
import { ThemeToggle } from "@/components/theme-toggle";
import { useI18n } from "@/i18n/provider";
import { LangSwitch } from "@/components/lang-switch";

export function Navbar() {
  const { t } = useI18n();
  return (
    <header className="border-b bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container h-14 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-7 w-7 rounded-md bg-primary" />
          <Link href="/" className="font-semibold">
            Orion
          </Link>
          <span className="text-sm text-muted-foreground hidden sm:inline">
            {t("nav.tagline")}
          </span>
        </div>
        <div className="flex items-center gap-3">
          <LangSwitch />
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
