import { Card } from "@/components/ui/card"

export default function HomePage() {
  return (
    <div className="container space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">欢迎来到 Orion 控制台</h1>
        <p className="text-muted-foreground mt-1">
          统一的通知网关：配置渠道、管理模板、查看发送记录与状态。
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card title="业务系统" value="—" hint="接入系统数量" />
        <Card title="通知 API" value="—" hint="已配置的 API" />
        <Card title="今日发送" value="—" hint="成功/失败" />
        <Card title="待重试" value="—" hint="失败待重试消息" />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border bg-card p-4">
          <h2 className="font-medium mb-2">最近发送</h2>
          <p className="text-sm text-muted-foreground">数据接入后展示最近发送记录。</p>
        </div>
        <div className="rounded-lg border bg-card p-4">
          <h2 className="font-medium mb-2">渠道健康</h2>
          <p className="text-sm text-muted-foreground">展示渠道可用性与限流情况。</p>
        </div>
      </div>
    </div>
  )
}

