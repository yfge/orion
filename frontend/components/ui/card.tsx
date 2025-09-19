import { cn } from "./cn"

export function Card(
  { title, value, hint, className }: { title: string; value: string; hint?: string; className?: string }
) {
  return (
    <div className={cn("rounded-lg border bg-card p-4", className)}>
      <div className="text-sm text-muted-foreground">{title}</div>
      <div className="mt-1 text-2xl font-semibold tracking-tight">{value}</div>
      {hint ? <div className="text-xs text-muted-foreground mt-1">{hint}</div> : null}
    </div>
  )
}

