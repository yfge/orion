"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import {
  createApiKey,
  deleteApiKey,
  listApiKeys,
  updateApiKey,
} from "@/lib/api";

export default function ApiKeysPage() {
  const [mounted, setMounted] = useState(false);
  const [items, setItems] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [limit] = useState(50);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState("");
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [newToken, setNewToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const res = await listApiKeys({ limit, offset, q: q || undefined });
      setItems(res.items || []);
      setTotal(res.total || 0);
    } catch (e: any) {
      setError(e.message || "加载失败");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setMounted(true);
    load();
  }, [offset]);

  const onCreate = async () => {
    setError(null);
    try {
      const r = await createApiKey({ name, description: desc || undefined });
      setNewToken(r.token);
      setName("");
      setDesc("");
      load();
    } catch (e: any) {
      setError(e.message || "创建失败");
    }
  };

  const onDelete = async (bid: string) => {
    if (!confirm("确认删除该 API Key？删除后不可使用。")) return;
    try {
      await deleteApiKey(bid);
      load();
    } catch (e: any) {
      alert(e.message || "删除失败");
    }
  };

  if (!mounted) return <div className="container">加载中...</div>;

  return (
    <div className="container max-w-2xl space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">API Keys</h1>
      </div>

      <div className="rounded-lg border p-4 space-y-3">
        <h2 className="text-lg font-medium">新建</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label htmlFor="name">名称</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="例如：Notify 公共 Key"
            />
          </div>
          <div className="space-y-1 md:col-span-2">
            <Label htmlFor="desc">描述（可选）</Label>
            <Input
              id="desc"
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              placeholder="用途说明..."
            />
          </div>
        </div>
        <Button type="button" onClick={onCreate} disabled={!name}>
          创建
        </Button>
        {error && <p className="text-sm text-red-600">{error}</p>}
        {newToken && (
          <div className="rounded-md border p-3 text-sm">
            <div className="font-medium mb-1">新密钥（仅显示一次）</div>
            <div className="font-mono break-all">{newToken}</div>
            <div className="text-xs text-muted-foreground mt-1">
              请妥善保存。调用 Notify 推荐使用 Authorization: Bearer
              &lt;token&gt;。
            </div>
          </div>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <Input
          placeholder="按名称搜索"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="w-64"
        />
        <Button
          type="button"
          variant="outline"
          onClick={() => {
            setOffset(0);
            load();
          }}
          disabled={loading}
        >
          搜索
        </Button>
      </div>

      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-3 py-2 text-left">名称</th>
              <th className="px-3 py-2 text-left">标识</th>
              <th className="px-3 py-2 text-left">状态</th>
              <th className="px-3 py-2 text-left">操作</th>
            </tr>
          </thead>
          <tbody>
            {items.map((it: any) => (
              <tr key={it.api_key_bid} className="border-t">
                <td className="px-3 py-2">{it.name}</td>
                <td className="px-3 py-2 text-muted-foreground">
                  {it.prefix || ""}...{it.suffix || ""}
                </td>
                <td className="px-3 py-2">
                  {it.status === 1 ? "启用" : "禁用"}
                </td>
                <td className="px-3 py-2">
                  <button
                    onClick={async () => {
                      await updateApiKey(it.api_key_bid, {
                        status: it.status === 1 ? 0 : 1,
                      });
                      load();
                    }}
                    className="text-primary hover:underline mr-3"
                  >
                    {it.status === 1 ? "禁用" : "启用"}
                  </button>
                  <button
                    onClick={() => onDelete(it.api_key_bid)}
                    className="text-red-600 hover:underline"
                  >
                    删除
                  </button>
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td className="px-3 py-4 text-muted-foreground" colSpan={4}>
                  暂无数据
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          disabled={offset === 0}
          onClick={() => setOffset(Math.max(0, offset - limit))}
        >
          上一页
        </Button>
        <span className="text-sm text-muted-foreground">
          {offset + 1}-{Math.min(offset + limit, total)} / {total}
        </span>
        <Button
          variant="outline"
          disabled={offset + limit >= total}
          onClick={() => setOffset(offset + limit)}
        >
          下一页
        </Button>
      </div>
    </div>
  );
}
