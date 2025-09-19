"use client"

import { useMemo } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

type Schema = any

export function JsonSchemaForm({
  schema,
  value,
  onChange,
  disabled,
}: {
  schema: Schema
  value: any
  onChange: (val: any) => void
  disabled?: boolean
}) {
  const properties = useMemo(() => (schema?.properties || {}) as Record<string, any>, [schema])
  const required: string[] = useMemo(() => (schema?.required || []) as string[], [schema])

  const handleChange = (key: string, v: any) => {
    const next = { ...(value || {}) }
    next[key] = v
    onChange(next)
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {Object.entries(properties).map(([key, prop]) => {
        const title = prop.title || key
        const type = prop.type || "string"
        const isReq = required.includes(key)
        const val = value?.[key] ?? (type === "boolean" ? false : "")
        if (prop.enum && Array.isArray(prop.enum)) {
          return (
            <div key={key} className="space-y-1">
              <Label htmlFor={key}>{title}{isReq ? " *" : ""}</Label>
              <select id={key} disabled={disabled} className="border rounded-md h-9 px-3 text-sm w-full" value={val} onChange={(e) => handleChange(key, e.target.value)}>
                <option value="">请选择</option>
                {prop.enum.map((opt: any) => (<option key={String(opt)} value={opt}>{String(opt)}</option>))}
              </select>
            </div>
          )
        }
        if (type === "boolean") {
          return (
            <div key={key} className="space-y-1">
              <Label htmlFor={key}>{title}{isReq ? " *" : ""}</Label>
              <select id={key} disabled={disabled} className="border rounded-md h-9 px-3 text-sm w-full" value={val ? "1" : "0"} onChange={(e) => handleChange(key, e.target.value === "1") }>
                <option value="1">是</option>
                <option value="0">否</option>
              </select>
            </div>
          )
        }
        let inputType = "text"
        if (type === "number" || type === "integer") inputType = "number"
        return (
          <div key={key} className="space-y-1">
            <Label htmlFor={key}>{title}{isReq ? " *" : ""}</Label>
            <Input id={key} disabled={disabled} type={inputType} value={val} onChange={(e) => handleChange(key, inputType === "number" ? Number(e.target.value) : e.target.value)} />
          </div>
        )
      })}
    </div>
  )
}

