import React from 'react';
import { initMemory, addProcess, removeProcess, getTree } from './buddySystem';
import MemoryTree, { MemoryNode } from './MemoryTree';
import {
  Box,
  Button,
  Input,
  Select,
  Stack,
  Heading,
  Text,
  useToast,
  Card,
  CardBody,
  CardHeader,
  CardFooter,
  Divider,
  Flex,
  Spacer
} from '@chakra-ui/react';

function App() {
  // Utilidad para potencia de 2
  function isPowerOfTwo(n: number) {
    return n > 0 && (n & (n - 1)) === 0;
  }
  // Historial de procesos
  const [history, setHistory] = React.useState<{ action: string; name: string; size?: number; unit?: string }[]>([]);
  const [tree, setTree] = React.useState<MemoryNode | null>(null);
  const [totalSize, setTotalSize] = React.useState<string>("");
  const [totalUnit, setTotalUnit] = React.useState<'MB' | 'KB'>('MB');
  const [processId, setProcessId] = React.useState("");
  const [processSize, setProcessSize] = React.useState<string>("");
  const [processUnit, setProcessUnit] = React.useState<'MB' | 'KB'>('MB');
  const [removeId, setRemoveId] = React.useState("");
  const toast = useToast();

  // Devuelve el valor numérico y la unidad para el backend
  const getTotalSize = () => {
    const n = Number(totalSize);
    return { value: n > 0 ? n : 0, unit: totalUnit };
  };
  const getProcessSize = () => {
    const n = Number(processSize);
    return { value: n > 0 ? n : 0, unit: processUnit };
  };

  const fetchTree = async () => {
    try {
      const result = await getTree();
      setTree(result);
    } catch {
      setTree(null);
    }
  };

  const handleInit = async () => {
    const { value, unit } = getTotalSize();
    if (!isPowerOfTwo(value)) {
      toast({ title: "El tamaño total de memoria debe ser potencia de 2", status: "error", duration: 2500 });
      return;
    }
    try {
      await initMemory(value, unit);
      setHistory([]); // Limpiar historial al inicializar memoria
      toast({ title: "Memoria inicializada", status: "success", duration: 2000 });
      await fetchTree();
    } catch (e) {
      toast({ title: "Error al inicializar memoria", status: "error", duration: 2000 });
    }
  };

  const handleAdd = async () => {
    const total = getTotalSize();
    const proc = getProcessSize();
    if (!processId || Number(processSize) < 1) {
      toast({ title: "Ingresa un nombre y tamaño válido para el proceso", status: "warning", duration: 2000 });
      return;
    }
  // Ya no se requiere que el proceso sea potencia de 2, el backend lo redondea
    // Validación: solo comparar si las unidades son iguales
    if (proc.unit === total.unit && proc.value > total.value) {
      toast({ title: "El proceso excede la memoria total disponible", status: "error", duration: 2500 });
      return;
    }
    // Si las unidades son diferentes, convierte ambas a KB para comparar
    const procKB = proc.unit === 'MB' ? proc.value * 1024 : proc.value;
    const totalKB = total.unit === 'MB' ? total.value * 1024 : total.value;
    if (procKB > totalKB) {
      toast({ title: "El proceso excede la memoria total disponible", status: "error", duration: 2500 });
      return;
    }
    try {
      const result = await addProcess(processId, proc.value, proc.unit);
      if (result && result.status === "allocated") {
        toast({ title: "Proceso agregado", status: "success", duration: 2000 });
        setHistory(h => [{ action: "Agregado", name: processId, size: proc.value, unit: proc.unit }, ...h]);
        await fetchTree();
      } else {
        // Si el backend responde pero no es "allocated", muestra error y NO agrega al historial
        toast({ title: result.detail || "No se pudo agregar el proceso", status: "error", duration: 2000 });
      }
    } catch (e: any) {
      // El backend lanza excepción HTTP con el mensaje de error
      let msg = "No se pudo agregar el proceso";
      if (e && e.message) {
        msg = e.message;
      }
      toast({ title: msg, status: "error", duration: 2000 });
    }
  };

  const handleRemove = async () => {
    if (!removeId) {
      toast({ title: "Ingresa el nombre del proceso a eliminar", status: "warning", duration: 2000 });
      return;
    }
    try {
      const result = await removeProcess(removeId);
      if (result.status === "deallocated") {
        toast({ title: "Proceso eliminado", status: "success", duration: 2000 });
        setHistory(h => [{ action: "Eliminado", name: removeId }, ...h]);
        await fetchTree();
      } else {
        toast({ title: result.detail || "No se pudo eliminar el proceso", status: "error", duration: 2000 });
      }
    } catch (e) {
      toast({ title: "No se pudo eliminar el proceso", status: "error", duration: 2000 });
    }
  };

  // No cargar el árbol ni historial al refrescar, solo cuando el usuario inicialice memoria

  return (
    <Flex minH="100vh" align="flex-start" justify="center" bg="gray.50" p={6}>
      <Box w="100%" maxW="1100px">
        <Flex direction={{ base: "column", lg: "row" }} gap={8}>
          <Box flex={2}>
            <Card boxShadow="xl" borderRadius="2xl" p={6}>
              <CardHeader>
                <Heading size="xl" textAlign="center" mb={2} color="teal.600">Buddy System Visualizer</Heading>
                <Text textAlign="center" color="gray.500" fontSize="md">Simula la gestión de memoria con animaciones y una interfaz moderna</Text>
              </CardHeader>
              <Divider my={4} />
              <CardBody>
                <Stack spacing={5}>
                  {/* ...inputs y controles... */}
                  <Stack direction={{ base: "column", md: "row" }} spacing={4} align="center">
                    <Input
                      type="number"
                      min={1}
                      value={totalSize}
                      onChange={e => setTotalSize(e.target.value)}
                      placeholder="Tamaño total"
                      w="32"
                      bg="white"
                      inputMode="numeric"
                    />
                    <Select
                      value={totalUnit}
                      onChange={e => setTotalUnit(e.target.value as 'MB' | 'KB')}
                      w="24"
                      bg="white"
                    >
                      <option value="MB">MB</option>
                      <option value="KB">KB</option>
                    </Select>
                    <Button colorScheme="blue" onClick={handleInit} w="40">Inicializar Memoria</Button>
                  </Stack>
                  <Stack direction={{ base: "column", md: "row" }} spacing={4} align="center">
                    <Input
                      type="text"
                      value={processId}
                      onChange={e => setProcessId(e.target.value)}
                      placeholder="Nombre del proceso"
                      w="32"
                      bg="white"
                    />
                    <Input
                      type="number"
                      min={1}
                      value={processSize}
                      onChange={e => setProcessSize(e.target.value)}
                      placeholder="Tamaño"
                      w="24"
                      bg="white"
                      inputMode="numeric"
                    />
                    <Select
                      value={processUnit}
                      onChange={e => setProcessUnit(e.target.value as 'MB' | 'KB')}
                      w="24"
                      bg="white"
                    >
                      <option value="MB">MB</option>
                      <option value="KB">KB</option>
                    </Select>
                    <Button colorScheme="green" onClick={handleAdd} w="40">Agregar Proceso</Button>
                  </Stack>
                  <Stack direction={{ base: "column", md: "row" }} spacing={4} align="center">
                    <Input
                      type="text"
                      value={removeId}
                      onChange={e => setRemoveId(e.target.value)}
                      placeholder="Nombre del proceso a eliminar"
                      w="56"
                      bg="white"
                    />
                    <Button colorScheme="red" onClick={handleRemove} w="40">Eliminar Proceso</Button>
                  </Stack>
                </Stack>
              </CardBody>
              <CardFooter>
                <Box w="100%">
                  {/* Mostrar el árbol si la memoria ya fue inicializada (tree no nulo) */}
                  {tree && <MemoryTree node={tree} key={history.map(h=>h.name+h.action).join('-')} />}
                </Box>
              </CardFooter>
            </Card>
          </Box>
          <Box flex={1} minW="260px">
            <Card boxShadow="md" borderRadius="xl" p={4} h="100%" bg="white">
              <CardHeader pb={2}>
                <Heading size="md" color="teal.700">Historial de procesos</Heading>
              </CardHeader>
              <Divider my={2} />
              <CardBody>
                <Stack spacing={2} maxH="600px" overflowY="auto">
                  {history.length === 0 && <Text color="gray.400">Sin movimientos aún</Text>}
                  {/* Solo mostrar historial si hay movimientos */}
                  {history.length > 0 && history.map((h, i) => (
                    <Box key={i} bg={h.action === "Agregado" ? "green.50" : "red.50"} borderRadius="md" px={3} py={2} boxShadow="sm">
                      <Text fontWeight="bold" color={h.action === "Agregado" ? "green.700" : "red.700"}>{h.action}</Text>
                      <Text fontSize="sm">{h.name}{h.size ? ` (${h.size} ${h.unit || 'MB'})` : ""}</Text>
                    </Box>
                  ))}
                </Stack>
              </CardBody>
            </Card>
          </Box>
        </Flex>
      </Box>
    </Flex>
  );
}

export default App;