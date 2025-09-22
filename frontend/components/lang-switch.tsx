"use client";

import { useI18n } from "@/i18n/provider";

export function LangSwitch() {
  const { locale } = useI18n();

  const onChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const v = e.target.value;
    document.cookie = `LANG=${v}; path=/; max-age=31536000`;
    location.reload();
  };

  return (
    <select
      className="border rounded-md px-2 h-8 bg-background text-sm"
      onChange={onChange}
      value={locale}
      aria-label="Language"
    >
      <option value="zh-CN">简体中文</option>
      <option value="en-US">English</option>
    </select>
  );
}
