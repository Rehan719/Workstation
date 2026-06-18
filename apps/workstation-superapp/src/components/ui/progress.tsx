import * as React from "react"
import { cn } from "@/lib/utils"

export interface ProgressProps extends React.HTMLAttributes<HTMLProgressElement> {
  value?: number
}

const Progress = React.forwardRef<HTMLProgressElement, ProgressProps>(
  ({ className, value = 0, ...props }, ref) => (
    <progress
      ref={ref}
      value={Math.max(0, Math.min(100, value))}
      max={100}
      className={cn(
        "h-2 w-full appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-secondary [&::-webkit-progress-value]:bg-primary [&::-webkit-progress-value]:transition-all [&::-moz-progress-bar]:bg-primary",
        className
      )}
      {...(props as React.HTMLAttributes<HTMLProgressElement>)}
    />
  )
)
Progress.displayName = "Progress"

export { Progress }
