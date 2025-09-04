"use client"

import { useToast, ToastId, Box, Button } from "@chakra-ui/react"
import * as React from "react"

export type ToastOptions = {
  title?: string
  description?: string
  status?: "info" | "warning" | "success" | "error"
  duration?: number
  isClosable?: boolean
}

export const useToaster = () => {
  const toast = useToast()

  const showToast = (options: ToastOptions) => {
    toast({
      title: options.title,
      description: options.description,
      status: options.status || "info",
      duration: options.duration ?? 5000,
      isClosable: options.isClosable ?? true,
      position: "bottom-right",
    })
  }

  return { showToast }
}

// Ejemplo de componente Toaster
export const ToasterExample = () => {
  const { showToast } = useToaster()

  return (
    <Box>
      <Button onClick={() => showToast({ title: "Hola!", description: "Esto es un toast." })}>
        Mostrar Toast
      </Button>
    </Box>
  )
}
