import fs from "node:fs";
import path from "node:path";
import Link from "next/link";

export default function HelpIndex() {
  // Determine help directory for both `npm run dev` in frontend/ and repo-root executions
  let helpDir = path.join(process.cwd(), "help");
  if (!fs.existsSync(helpDir)) {
    helpDir = path.join(process.cwd(), "frontend", "help");
  }
  let items: { slug: string; title: string }[] = [];
  try {
    const files = fs.readdirSync(helpDir).filter((f) => f.endsWith(".md"));
    items = files.map((f) => {
      const slug = f.replace(/\.md$/, "");
      const content = fs.readFileSync(path.join(helpDir, f), "utf-8");
      const m = content.match(/^#\s+(.+)$/m);
      const title = m ? m[1].trim() : slug;
      return { slug, title };
    });
  } catch (e) {
    items = [];
  }

  return (
    <div className="container max-w-3xl space-y-3">
      <h1 className="text-2xl font-semibold">帮助中心</h1>
      <p className="text-muted-foreground">Orion 使用指南与最佳实践</p>
      <div className="grid grid-cols-1 divide-y">
        {items.map((it) => (
          <Link
            key={it.slug}
            href={`/help/${it.slug}`}
            className="py-3 hover:underline"
          >
            {it.title}
          </Link>
        ))}
        {items.length === 0 && (
          <p className="text-muted-foreground py-6">暂无文档</p>
        )}
      </div>
    </div>
  );
}
