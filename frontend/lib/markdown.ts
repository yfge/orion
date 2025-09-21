export function simpleMarkdownToHtml(md: string): string {
  // very lightweight markdown to HTML converter (headings, lists, code, inline code)
  let html = md
    // escape HTML
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // code blocks ```
  html = html.replace(
    /```([\s\S]*?)```/g,
    (_m, code) => `<pre><code>${code.replace(/\n/g, "<br/>")}</code></pre>`,
  );
  // headings
  html = html
    .replace(/^######\s+(.*)$/gm, "<h6>$1</h6>")
    .replace(/^#####\s+(.*)$/gm, "<h5>$1</h5>")
    .replace(/^####\s+(.*)$/gm, "<h4>$1</h4>")
    .replace(/^###\s+(.*)$/gm, "<h3>$1</h3>")
    .replace(/^##\s+(.*)$/gm, "<h2>$1</h2>")
    .replace(/^#\s+(.*)$/gm, "<h1>$1</h1>");
  // lists
  html = html.replace(/^\s*[-*]\s+(.*)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>.*<\/li>\n?)+/g, (m) => `<ul>${m}</ul>`);
  // inline code
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  // paragraphs
  html = html.replace(
    /^(?!<h\d>|<ul>|<li>|<pre>|<\/li>|<\/ul>|<pre>|<code>|<\/code>)(.+)$/gm,
    "<p>$1</p>",
  );
  return html;
}
