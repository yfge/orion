import fs from "node:fs";
import path from "node:path";
import Link from "next/link";
import { simpleMarkdownToHtml } from "@/lib/markdown";

export default function HelpArticle({ params }: { params: { slug: string } }) {
  const helpDir = path.join(process.cwd(), "frontend", "help");
  const file = path.join(helpDir, `${params.slug}.md`);
  if (!fs.existsSync(file)) {
    return (
      <div className="container max-w-3xl">
        <h1 className="text-2xl font-semibold mb-2">未找到该帮助文档</h1>
        <p className="text-muted-foreground">路径：/help/{params.slug}</p>
        <p className="mt-4">
          <Link href="/help" className="text-primary hover:underline">
            返回帮助中心
          </Link>
        </p>
      </div>
    );
  }
  const md = fs.readFileSync(file, "utf-8");
  const html = simpleMarkdownToHtml(md);
  return (
    <div className="container max-w-3xl prose dark:prose-invert">
      {/* eslint-disable-next-line react/no-danger */}
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}
