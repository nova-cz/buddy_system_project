# Importa la clase TreeNode que representa cada bloque de memoria
from .tree_node import TreeNode

# Clase principal que implementa el algoritmo Buddy System
class BuddySystem:

	def get_tree(self):
		"""
		Devuelve la estructura del árbol de memoria como un diccionario anidado.
		Útil para que la UI o animaciones puedan visualizar el estado actual.
		:return: Diccionario con la información del árbol
		"""
		def node_to_dict(node):
			if node is None:
				return None
			return {
				'size': node.size,
				'is_free': node.is_free,
				'process': node.process,
				'left': node_to_dict(node.left),
				'right': node_to_dict(node.right)
			}
		return node_to_dict(self.root)

	def reset_memory(self):
		"""
		Reinicia toda la memoria, eliminando todos los procesos y divisiones.
		Deja solo el bloque raíz libre, como al inicio.
		"""
		self.root = TreeNode(self.total_size)  # Crea un nuevo nodo raíz libre

	def deallocate(self, process_name):
		"""
		Libera la memoria ocupada por el proceso dado y fusiona bloques libres si es posible.
		:param process_name: Nombre del proceso a eliminar
		:return: True si se liberó correctamente, False si no se encontró el proceso
		"""
		# Función auxiliar recursiva para buscar y liberar el proceso
		def _deallocate_recursive(node):
			if node is None:
				return False, False  # (¿Se liberó?, ¿Se fusionó?)
			# Si el nodo es hoja y contiene el proceso
			if node.process == process_name:
				node.is_free = True      # Marcar como libre
				node.process = None      # Quitar el nombre del proceso
				return True, False       # Se liberó, pero aún no se fusiona
			# Si tiene hijos, buscar recursivamente en ambos
			left_freed, left_merged = _deallocate_recursive(node.left)
			right_freed, right_merged = _deallocate_recursive(node.right)
			# Si se liberó en alguno de los hijos, intentar fusionar
			if left_freed or right_freed:
				# Ambos hijos existen, están libres y son hojas (no tienen más hijos)
				if (node.left and node.right and
					node.left.is_free and node.right.is_free and
					node.left.left is None and node.left.right is None and
					node.right.left is None and node.right.right is None):
					# Eliminar los hijos y marcar el padre como libre
					node.left = None
					node.right = None
					node.is_free = True
					return True, True  # Se liberó y se fusionó
				return True, False  # Se liberó, pero no se fusionó
			return False, False  # No se encontró el proceso aquí

		freed, merged = _deallocate_recursive(self.root)
		return freed  # True si se liberó, False si no se encontró el proceso

	def _allocate_recursive(self, node, process_name, size):
		"""
		Busca recursivamente un bloque libre adecuado y lo asigna al proceso.
		Si el bloque es más grande de lo necesario, lo divide en dos buddies.
		:param node: Nodo actual del árbol
		:param process_name: Nombre del proceso a asignar
		:param size: Tamaño solicitado
		:return: True si se asignó, False si no
		"""
		# Si el nodo tiene hijos, no es un bloque indivisible, hay que buscar en los hijos
		if node.left and node.right:
			# Intentar primero en el hijo izquierdo
			if self._allocate_recursive(node.left, process_name, size):
				return True
			# Si no se pudo en el izquierdo, intentar en el derecho
			return self._allocate_recursive(node.right, process_name, size)

		# Si el bloque está ocupado o no está libre, no se puede usar
		if not node.is_free or node.process is not None:
			return False

		# Si el tamaño del bloque es igual al solicitado y está libre, asignar aquí
		if node.size == size:
			node.is_free = False           # Marcar como ocupado
			node.process = process_name    # Asignar el nombre del proceso
			return True

		# Si el bloque es más grande que lo solicitado, hay que dividirlo
		if node.size > size:
			half = node.size // 2
			# Crear los dos buddies (hijos izquierdo y derecho)
			node.left = TreeNode(half)
			node.right = TreeNode(half)
			# Intentar asignar en el hijo izquierdo (por convención)
			return self._allocate_recursive(node.left, process_name, size)

		# Si el bloque es más pequeño que lo solicitado, no se puede asignar
		return False

	def _process_exists(self, process_name):
		"""
		Verifica si ya existe un proceso con ese nombre en el árbol.
		:param process_name: Nombre del proceso a buscar
		:return: True si existe, False si no
		"""
		found = False
		def visit(node):
			nonlocal found
			if node.process == process_name:
				found = True
		self.root.preorder(visit)
		return found


	def _is_power_of_two(self, n):
		"""
		Verifica si n es una potencia de 2 (y mayor que 0).
		:param n: Número a verificar
		:return: True si es potencia de 2, False en caso contrario
		"""
		return n > 0 and (n & (n - 1)) == 0

	def allocate(self, process_name, size):
		"""
		Intenta asignar un bloque de memoria al proceso dado.
		:param process_name: Nombre del proceso a asignar
		:param size: Tamaño solicitado (en MB)
		:return: True si se asignó correctamente, False si no hay espacio o hay error
		"""
		# Validar que el tamaño sea potencia de 2 y no mayor al total
		if not self._is_power_of_two(size) or size > self.total_size:
			# Tamaño inválido
			return False
		# Verificar que el proceso no exista ya
		if self._process_exists(process_name):
			# Ya hay un proceso con ese nombre
			return False
		# Buscar y asignar el bloque adecuado recursivamente desde la raíz
		return self._allocate_recursive(self.root, process_name, size)

	def initialize_memory(self):
		"""
		Reinicia la memoria, dejando solo un bloque libre del tamaño total.
		Útil para limpiar todo y empezar desde cero.
		"""
		self.root = TreeNode(self.total_size)  # Crea un nuevo nodo raíz libre

	def __init__(self, total_size):
		"""
		Inicializa el sistema Buddy con un bloque de memoria del tamaño total especificado.
		:param total_size: Tamaño total de la memoria a gestionar (debe ser potencia de 2)
		"""
		self.total_size = total_size  # Guarda el tamaño total de la memoria
		self.root = TreeNode(total_size)  # El árbol comienza con un solo bloque libre (la raíz)
