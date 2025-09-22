"use client";

import Link from "next/link";
import { useI18n } from "@/i18n/provider";

const items: { href: string; key: string }[] = [
  { href: "/", key: "nav.overview" },
  { href: "/systems", key: "nav.systems" },
  { href: "/apis", key: "nav.apis" },
  { href: "/messages", key: "nav.messages" },
  { href: "/records", key: "nav.records" },
  { href: "/users", key: "nav.users" },
  { href: "/api-keys", key: "nav.apiKeys" },
  { href: "/help", key: "nav.help" },
];

export function Sidebar() {
  const { t } = useI18n();
  return (
    <nav className="p-4 space-y-1">
      {items.map((it) => (
        <Link
          key={it.href}
          href={it.href}
          className="block px-3 py-2 rounded-md text-sm hover:bg-accent hover:text-accent-foreground text-muted-foreground"
        >
          {t(it.key)}
        </Link>
      ))}
    </nav>
  );
}
