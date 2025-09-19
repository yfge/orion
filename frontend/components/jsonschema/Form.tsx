"use client"

import { useMemo, useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"

type Schema = any

type RendererProps = {
  schema: Schema
  value: any
  onChange: (val: any) => void
  disabled?: boolean
  path?: string
}

function FieldRenderer({ schema, value, onChange, disabled, path = "" }: RendererProps) {
  const t = schema?.type
  const title = schema?.title
  const description = schema?.description

  // oneOf/anyOf support via a simple selector
  const variants: any[] | undefined = schema?.oneOf || schema?.anyOf
  const [variantIdx, setVariantIdx] = useState(0)
  if (variants && variants.length > 0) {
    const active = variants[variantIdx] || variants[0]
    return (
      <div className="space-y-2">
        {title && <div className="font-medium">{title}</div>}
        <div className="flex items-center gap-2">
          <Label className="text-xs text-muted-foreground">类型</Label>
          <select
            className="border rounded-md h-8 px-2 text-xs"
            value={variantIdx}
            onChange={(e) => {
              const idx = Number(e.target.value)
              setVariantIdx(idx)
              onChange(undefined)
            }}
          >
            {variants.map((v, i) => (
              <option key={i} value={i}>
                {v.title || v.type || `方案 ${i + 1}`}
              </option>
            ))}
          </select>
        </div>
        <FieldRenderer schema={active} value={value} onChange={onChange} disabled={disabled} path={path} />
      </div>
    )
  }

  // enum
  if (Array.isArray(schema?.enum)) {
    const val = value ?? ""
    return (
      <div className="space-y-1">
        {title && <Label>{title}</Label>}
        <select
          disabled={disabled}
          className="border rounded-md h-9 px-3 text-sm w-full"
          value={val}
          onChange={(e) => onChange(e.target.value)}
        >
          <option value="">请选择</option>
          {schema.enum.map((opt: any) => (
            <option key={String(opt)} value={opt}>
              {String(opt)}
            </option>
          ))}
        </select>
        {description && <p className="text-xs text-muted-foreground">{description}</p>}
      </div>
    )
  }

  // boolean
  if (t === "boolean") {
    const val = !!value
    return (
      <div className="space-y-1">
        {title && <Label>{title}</Label>}
        <select
          disabled={disabled}
          className="border rounded-md h-9 px-3 text-sm w-full"
          value={val ? "1" : "0"}
          onChange={(e) => onChange(e.target.value === "1")}
        >
          <option value="1">是</option>
          <option value="0">否</option>
        </select>
        {description && <p className="text-xs text-muted-foreground">{description}</p>}
      </div>
    )
  }

  // object
  if (t === "object" || schema?.properties) {
    const properties = (schema?.properties || {}) as Record<string, any>
    const required: string[] = (schema?.required || []) as string[]
    const obj = value && typeof value === "object" ? value : {}
    const handleChild = (key: string, v: any) => {
      const next = { ...(obj || {}) }
      if (v === undefined) delete next[key]
      else next[key] = v
      onChange(next)
    }
    return (
      <div className="space-y-2">
        {title && <div className="font-medium">{title}</div>}
        {description && <p className="text-xs text-muted-foreground">{description}</p>}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(properties).map(([key, prop]) => {
            const isReq = required.includes(key)
            return (
              <div key={`${path}/${key}`} className="space-y-1">
                {prop.type !== "object" && prop.type !== "array" && (
                  <Label>
                    {prop.title || key}
                    {isReq ? " *" : ""}
                  </Label>
                )}
                <FieldRenderer
                  schema={prop}
                  value={obj?.[key] ?? prop.default}
                  onChange={(v) => handleChild(key, v)}
                  disabled={disabled}
                  path={`${path}/${key}`}
                />
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  // array
  if (t === "array") {
    const itemsSchema = schema.items || { type: "string" }
    const arr: any[] = Array.isArray(value) ? value : []
    const addDefault = () => {
      let defVal: any = itemsSchema.default
      if (defVal === undefined) {
        if (itemsSchema.type === "number" || itemsSchema.type === "integer") defVal = 0
        else if (itemsSchema.type === "boolean") defVal = false
        else if (itemsSchema.type === "object") defVal = {}
        else defVal = ""
      }
      onChange([...(arr || []), defVal])
    }
    const removeAt = (i: number) => {
      const next = [...arr]
      next.splice(i, 1)
      onChange(next)
    }
    return (
      <div className="space-y-2">
        {title && <div className="font-medium">{title}</div>}
        {description && <p className="text-xs text-muted-foreground">{description}</p>}
        <div className="space-y-3">
          {arr.map((item, i) => (
            <div key={`${path}/${i}`} className="border rounded p-3 space-y-2 bg-card/30">
              <div className="flex items-center justify-between">
                <div className="text-xs text-muted-foreground">项 #{i + 1}</div>
                <Button type="button" size="sm" variant="outline" disabled={disabled} onClick={() => removeAt(i)}>
                  删除
                </Button>
              </div>
              <FieldRenderer
                schema={itemsSchema}
                value={item}
                onChange={(v) => {
                  const next = [...arr]
                  next[i] = v
                  onChange(next)
                }}
                disabled={disabled}
                path={`${path}/${i}`}
              />
            </div>
          ))}
          <Button type="button" size="sm" variant="outline" disabled={disabled} onClick={addDefault}>
            添加一项
          </Button>
        </div>
      </div>
    )
  }

  // string/number/integer and default widgets
  const inputType = schema?.format === "textarea" || schema?.["x-ui:widget"] === "textarea"
    ? "textarea"
    : (t === "number" || t === "integer")
      ? "number"
      : "text"

  const primitiveVal = value ?? (t === "boolean" ? false : "")

  if (inputType === "textarea") {
    return (
      <div className="space-y-1">
        {title && <Label>{title}</Label>}
        <textarea
          className="border rounded-md px-3 py-2 text-sm w-full min-h-[90px]"
          disabled={disabled}
          value={primitiveVal}
          onChange={(e) => onChange(e.target.value)}
        />
        {description && <p className="text-xs text-muted-foreground">{description}</p>}
      </div>
    )
  }

  return (
    <div className="space-y-1">
      {title && <Label>{title}</Label>}
      <Input
        type={inputType}
        disabled={disabled}
        value={primitiveVal}
        onChange={(e) => onChange(inputType === "number" ? Number(e.target.value) : e.target.value)}
      />
      {description && <p className="text-xs text-muted-foreground">{description}</p>}
    </div>
  )
}

export function JsonSchemaForm({ schema, value, onChange, disabled }: { schema: Schema; value: any; onChange: (val: any) => void; disabled?: boolean }) {
  // Default root to object if not specified
  const rootSchema = useMemo(() => {
    if (!schema) return { type: "object", properties: {} }
    if (!schema.type && schema.properties) return { type: "object", ...schema }
    return schema
  }, [schema])

  return (
    <div className="space-y-2">
      <FieldRenderer schema={rootSchema} value={value} onChange={onChange} disabled={disabled} path="root" />
    </div>
  )
}
