"use client"

import { ChakraProvider, extendTheme, ColorModeScript } from "@chakra-ui/react"
import { ColorModeProvider, type ColorModeProviderProps } from "./color-mode"

const theme = extendTheme({
  config: {
    initialColorMode: "light",
    useSystemColorMode: true,
  },
})

export function Provider(props: ColorModeProviderProps) {
  return (
    <ChakraProvider theme={theme}>
      {/* Este script asegura que el color mode se inicialice correctamente en SSR */}
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      <ColorModeProvider {...props} />
    </ChakraProvider>
  )
}
