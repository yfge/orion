"use client"

import React from "react"
import Form, { IChangeEvent } from "@rjsf/core"
// Avoid strict type coupling to specific @rjsf versions to keep builds stable
import validator from "@rjsf/validator-ajv8"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"

type AnySchema = any

const TextWidget = ({ id, value, onChange, required, label, options, disabled, schema }: any) => {
  const widget = (options as any)?.widget || schema?.["x-ui:widget"]
  if (widget === "textarea" || schema?.format === "textarea") {
    return (
      <div className="space-y-1">
        {label && <Label htmlFor={id}>{label}{required ? " *" : ""}</Label>}
        <textarea id={id} className="border rounded-md px-3 py-2 text-sm w-full min-h-[90px]" disabled={disabled} value={value ?? ""} onChange={(e) => onChange(e.target.value)} />
      </div>
    )
  }
  return (
    <div className="space-y-1">
      {label && <Label htmlFor={id}>{label}{required ? " *" : ""}</Label>}
      <Input id={id} disabled={disabled} value={value ?? ""} onChange={(e) => onChange(e.target.value)} />
    </div>
  )
}

const NumberWidget = ({ id, value, onChange, required, label, disabled }: any) => (
  <div className="space-y-1">
    {label && <Label htmlFor={id}>{label}{required ? " *" : ""}</Label>}
    <Input id={id} type="number" disabled={disabled} value={value ?? ""} onChange={(e) => onChange(Number(e.target.value))} />
  </div>
)

const SelectWidget = ({ id, value, onChange, required, label, options, disabled }: any) => {
  const enumOptions = (options as any)?.enumOptions || []
  return (
    <div className="space-y-1">
      {label && <Label htmlFor={id}>{label}{required ? " *" : ""}</Label>}
      <select id={id} disabled={disabled} className="border rounded-md h-9 px-3 text-sm w-full" value={value ?? ""} onChange={(e) => onChange(e.target.value)}>
        <option value="">请选择</option>
        {enumOptions.map((opt: any) => (
          <option key={String(opt.value)} value={opt.value}>{opt.label}</option>
        ))}
      </select>
    </div>
  )
}

const CheckboxWidget = ({ id, value, onChange, required, label, disabled }: any) => (
  <div className="space-y-1">
    {label && <Label htmlFor={id}>{label}{required ? " *" : ""}</Label>}
    <select id={id} disabled={disabled} className="border rounded-md h-9 px-3 text-sm w-full" value={value ? "1" : "0"} onChange={(e) => onChange(e.target.value === "1")}>
      <option value="1">是</option>
      <option value="0">否</option>
    </select>
  </div>
)

const ArrayFieldTemplate = (props: any) => {
  const { items, canAdd, onAddClick, title, description } = props
  return (
    <div className="space-y-2">
      {title && <div className="font-medium">{title}</div>}
      {description && <p className="text-xs text-muted-foreground">{description as any}</p>}
      <div className="space-y-3">
        {items && items.map((el: any) => (
          <div key={el.key} className="border rounded p-3 space-y-2 bg-card/30">
            <div className="flex items-center justify-between">
              <div className="text-xs text-muted-foreground">项</div>
              <div className="space-x-2">
                {el.hasMoveUp && (
                  <Button type="button" size="sm" variant="outline" onClick={el.onReorderClick(el.index, el.index - 1)}>上移</Button>
                )}
                {el.hasMoveDown && (
                  <Button type="button" size="sm" variant="outline" onClick={el.onReorderClick(el.index, el.index + 1)}>下移</Button>
                )}
                {el.hasRemove && (
                  <Button type="button" size="sm" variant="outline" onClick={el.onDropIndexClick(el.index)}>删除</Button>
                )}
              </div>
            </div>
            <div>{el.children}</div>
          </div>
        ))}
        {canAdd && (
          <Button type="button" size="sm" variant="outline" onClick={onAddClick}>添加一项</Button>
        )}
      </div>
    </div>
  )
}

const ObjectFieldTemplate = (props: any) => {
  const { title, description, properties } = props
  return (
    <div className="space-y-2">
      {title && <div className="font-medium">{title}</div>}
      {description && <p className="text-xs text-muted-foreground">{description as any}</p>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {properties.map((p: any) => (
          <div key={p.name} className="space-y-1">{p.content}</div>
        ))}
      </div>
    </div>
  )
}

const templates: any = {
  ArrayFieldTemplate,
  ObjectFieldTemplate,
}

const widgets: any = {
  TextWidget,
  SelectWidget,
  CheckboxWidget,
  UpDownWidget: NumberWidget,
}

export function RjsfForm({ schema, formData, onChange, uiSchema, disabled }: { schema: AnySchema; formData: any; onChange: (val: any) => void; uiSchema?: any; disabled?: boolean }) {
  return (
    <Form
      schema={schema}
      formData={formData}
      validator={validator}
      templates={templates}
      widgets={widgets}
      uiSchema={uiSchema}
      disabled={disabled}
      noHtml5Validate
      onChange={(e: IChangeEvent) => onChange(e.formData)}
      onError={() => {}}
      onSubmit={(e) => onChange(e.formData)}
    >
      {/* hide default submit */}
      <div className="hidden" />
    </Form>
  )
}
