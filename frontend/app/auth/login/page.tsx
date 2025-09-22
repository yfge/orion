"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { login } from "@/lib/api";
import Link from "next/link";
import { useI18n } from "@/i18n/provider";

export default function LoginPage() {
  const { t } = useI18n();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(username, password);
      router.push("/users");
    } catch (err: any) {
      setError(err.message || t("auth.login.failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container max-w-md">
      <h1 className="text-2xl font-semibold mb-4">{t("auth.login.title")}</h1>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="space-y-1">
          <Label htmlFor="username">{t("auth.login.fields.username")}</Label>
          <Input
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="space-y-1">
          <Label htmlFor="password">{t("auth.login.fields.password")}</Label>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? t("auth.login.loading") : t("auth.login.submit")}
        </Button>
      </form>
      <p className="mt-3 text-sm text-muted-foreground">
        {t("auth.login.noAccount")}
        <Link
          className="text-primary underline-offset-2 hover:underline ml-1"
          href="/auth/register"
        >
          {t("auth.login.toRegister")}
        </Link>
      </p>
    </div>
  );
}
