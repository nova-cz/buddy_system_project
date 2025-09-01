class TreeNode:
    def __init__(self, size, is_free=True, process=None):
        self.size = size            # Tamaño del bloque de memoria
        self.is_free = is_free      # True si el bloque está libre
        self.process = process      # Nombre del proceso asignado (None si está libre)
        self.left = None            # Hijo izquierdo (otro TreeNode o None)
        self.right = None           # Hijo derecho (otro TreeNode o None)

    def preorder(self, visit):
        visit(self)  # Aplica la función 'visit' al nodo actual
        if self.left:
            self.left.preorder(visit)
        if self.right:
            self.right.preorder(visit)
            
def print_node(node):
    print(f"Tamaño: {node.size}, Libre: {node.is_free}, Proceso: {node.process}")

# Crear un árbol de ejemplo
#root = TreeNode(1024)
#root.left = TreeNode(512)
#root.right = TreeNode(9)
#root.left.left = TreeNode(256)
#root.left.right = TreeNode(36)

# Recorrer en preorden
#root.preorder(print_node)