import Link from "next/link";

const items = [
  { href: "/", label: "总览" },
  { href: "/systems", label: "业务系统" },
  { href: "/apis", label: "通知 API" },
  { href: "/messages", label: "消息定义" },
  { href: "/records", label: "发送记录" },
  { href: "/users", label: "用户" },
  { href: "/api-keys", label: "API Keys" },
];

export function Sidebar() {
  return (
    <nav className="p-4 space-y-1">
      {items.map((it) => (
        <Link
          key={it.href}
          href={it.href}
          className="block px-3 py-2 rounded-md text-sm hover:bg-accent hover:text-accent-foreground text-muted-foreground"
        >
          {it.label}
        </Link>
      ))}
    </nav>
  );
}
