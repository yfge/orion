import fs from "node:fs";
import path from "node:path";
import Link from "next/link";
import { Markdown } from "@/components/Markdown";
import { getLocaleServer } from "@/i18n/server";

export default function HelpArticle({ params }: { params: { slug: string } }) {
  const locale = getLocaleServer();
  let helpDir = path.join(process.cwd(), "help");
  if (!fs.existsSync(helpDir)) {
    helpDir = path.join(process.cwd(), "frontend", "help");
  }
  const localized = path.join(helpDir, locale, `${params.slug}.md`);
  const fallback = path.join(helpDir, `${params.slug}.md`);
  const file = fs.existsSync(localized) ? localized : fallback;

  function loadMessages(loc: string) {
    try {
      const file = path.join(
        process.cwd(),
        "frontend",
        "messages",
        `${loc}.json`,
      );
      const raw = fs.readFileSync(file, "utf-8");
      return JSON.parse(raw) as Record<string, string>;
    } catch {
      return {} as Record<string, string>;
    }
  }
  const messages = loadMessages(locale);
  const t = (k: string, fallback?: string) => messages[k] ?? fallback ?? k;
  if (!fs.existsSync(file)) {
    return (
      <div className="container max-w-3xl">
        <h1 className="text-2xl font-semibold mb-2">
          {t("help.article.notFound.title", "未找到该帮助文档")}
        </h1>
        <p className="text-muted-foreground">
          {t("help.article.notFound.path", "路径：")}/help/{params.slug}
        </p>
        <p className="mt-4">
          <Link href="/help" className="text-primary hover:underline">
            {t("help.article.notFound.back", "返回帮助中心")}
          </Link>
        </p>
      </div>
    );
  }
  const md = fs.readFileSync(file, "utf-8");
  return (
    <div className="container max-w-3xl prose dark:prose-invert">
      <Markdown source={md} />
    </div>
  );
}
