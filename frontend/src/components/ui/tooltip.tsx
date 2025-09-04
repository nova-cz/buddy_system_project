import { Tooltip as ChakraTooltip } from "@chakra-ui/react"
import * as React from "react"

export interface TooltipProps {
  label: React.ReactNode
  children: React.ReactNode
  showArrow?: boolean
  disabled?: boolean
  placement?: "top" | "bottom" | "left" | "right" | "auto"
}

export const Tooltip = React.forwardRef<HTMLDivElement, TooltipProps>(
  function Tooltip(
    { label, children, showArrow = true, disabled = false, placement = "top" },
    ref
  ) {
    if (disabled) return <>{children}</>

    return (
      <ChakraTooltip
        label={label}
        hasArrow={showArrow}
        placement={placement}
        ref={ref}
      >
        {children}
      </ChakraTooltip>
    )
  }
)
