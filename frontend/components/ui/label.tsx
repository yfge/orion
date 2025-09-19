import * as React from "react"
import { cn } from "./cn"

export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {}

export const Label = React.forwardRef<HTMLLabelElement, LabelProps>(({ className, ...props }, ref) => (
  <label ref={ref} className={cn("text-sm font-medium text-foreground", className)} {...props} />
))
Label.displayName = "Label"

