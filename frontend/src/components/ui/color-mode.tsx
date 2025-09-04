"use client"

import { IconButton, IconButtonProps, Skeleton, Box } from "@chakra-ui/react"
import { ThemeProvider, useTheme } from "next-themes"
import * as React from "react"
import { MoonIcon, SunIcon } from "@chakra-ui/icons"

export interface ColorModeProviderProps extends React.ComponentProps<typeof ThemeProvider> {}

export function ColorModeProvider(props: ColorModeProviderProps) {
  return (
    <ThemeProvider attribute="class" disableTransitionOnChange {...props} />
  )
}

export type ColorMode = "light" | "dark"

export interface UseColorModeReturn {
  colorMode: ColorMode
  setColorMode: (colorMode: ColorMode) => void
  toggleColorMode: () => void
}

export function useColorMode(): UseColorModeReturn {
  const { resolvedTheme, setTheme, forcedTheme } = useTheme()
  const colorMode = forcedTheme || resolvedTheme
  const toggleColorMode = () => {
    setTheme(resolvedTheme === "dark" ? "light" : "dark")
  }
  return {
    colorMode: colorMode as ColorMode,
    setColorMode: setTheme,
    toggleColorMode,
  }
}

export function useColorModeValue<T>(light: T, dark: T) {
  const { colorMode } = useColorMode()
  return colorMode === "dark" ? dark : light
}


export function ColorModeIcon() {
  const { colorMode } = useColorMode();
  return colorMode === "dark" ? <MoonIcon /> : <SunIcon />;
}

interface ColorModeButtonProps extends Omit<IconButtonProps, "aria-label"> {}

export const ColorModeButton = React.forwardRef<HTMLButtonElement, ColorModeButtonProps>(
  function ColorModeButton(props, ref) {
    const { toggleColorMode } = useColorMode()
    return (
      <React.Suspense fallback={<Skeleton boxSize="8" />}>
        <IconButton
          onClick={toggleColorMode}
          variant="ghost"
          aria-label="Toggle color mode"
          size="sm"
          ref={ref}
          {...props}
          icon={<ColorModeIcon />}
        />
      </React.Suspense>
    )
  }
)

// Componente LightMode/DarkMode usando Box en lugar de Span
export const LightMode = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof Box>>(
  function LightMode(props, ref) {
    return (
      <Box
        ref={ref}
        className="chakra-theme light"
        display="contents"
        {...props}
      />
    )
  }
)

export const DarkMode = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof Box>>(
  function DarkMode(props, ref) {
    return (
      <Box
        ref={ref}
        className="chakra-theme dark"
        display="contents"
        {...props}
      />
    )
  }
)
