import tkinter as tk
from tkinter import messagebox
from core.buddy_system import BuddySystem


class BuddySystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buddy System - UI (Arleth)")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        # ---- Variables ----
        self.buddy = None  # Aquí se guardará el sistema de memoria

        # ---- UI ----
        title = tk.Label(root, text="Buddy System Memory Manager", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Entrada de tamaño de memoria
        frame_top = tk.Frame(root, bg="#f0f0f0")
        frame_top.pack(pady=5)

        tk.Label(frame_top, text="Tamaño total (potencia de 2):", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.entry_size = tk.Entry(frame_top, width=10)
        self.entry_size.grid(row=0, column=1, padx=5)

        btn_init = tk.Button(frame_top, text="Inicializar memoria", command=self.init_memory, bg="#4CAF50", fg="white")
        btn_init.grid(row=0, column=2, padx=5)

        # Entrada para agregar proceso
        frame_process = tk.Frame(root, bg="#f0f0f0")
        frame_process.pack(pady=5)

        tk.Label(frame_process, text="Proceso:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.entry_process = tk.Entry(frame_process, width=10)
        self.entry_process.grid(row=0, column=1, padx=5)

        tk.Label(frame_process, text="Tamaño:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
        self.entry_p_size = tk.Entry(frame_process, width=10)
        self.entry_p_size.grid(row=0, column=3, padx=5)

        btn_add = tk.Button(frame_process, text="Agregar proceso", command=self.add_process, bg="#2196F3", fg="white")
        btn_add.grid(row=0, column=4, padx=5)

        # Entrada para eliminar proceso
        frame_remove = tk.Frame(root, bg="#f0f0f0")
        frame_remove.pack(pady=5)

        tk.Label(frame_remove, text="Proceso:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.entry_remove = tk.Entry(frame_remove, width=10)
        self.entry_remove.grid(row=0, column=1, padx=5)

        btn_remove = tk.Button(frame_remove, text="Eliminar proceso", command=self.remove_process, bg="#f44336", fg="white")
        btn_remove.grid(row=0, column=2, padx=5)

        # Botón limpiar memoria
        btn_clear = tk.Button(root, text="Limpiar memoria", command=self.clear_memory, bg="#9C27B0", fg="white")
        btn_clear.pack(pady=10)

        # Área para mostrar estado
        self.text_area = tk.Text(root, height=15, width=70, bg="#ffffff")
        self.text_area.pack(pady=10)

    # ---- Funciones ----
    def init_memory(self):
        try:
            size = int(self.entry_size.get())
            self.buddy = BuddySystem(size)
            self.show_tree()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")

    def add_process(self):
        if not self.buddy:
            messagebox.showerror("Error", "Primero inicialice la memoria.")
            return
        name = self.entry_process.get()
        try:
            size = int(self.entry_p_size.get())
            ok = self.buddy.allocate(name, size)
            if ok:
                self.show_tree()
            else:
                messagebox.showwarning("Aviso", "No se pudo asignar el proceso.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un tamaño válido.")

    def remove_process(self):
        if not self.buddy:
            messagebox.showerror("Error", "Primero inicialice la memoria.")
            return
        name = self.entry_remove.get()
        ok = self.buddy.deallocate(name)
        if ok:
            self.show_tree()
        else:
            messagebox.showwarning("Aviso", "No se encontró el proceso.")

    def clear_memory(self):
        if self.buddy:
            self.buddy.reset_memory()
            self.show_tree()

    def show_tree(self):
        """Muestra el árbol en el área de texto como diccionario"""
        self.text_area.delete("1.0", tk.END)
        tree = self.buddy.get_tree()
        self.text_area.insert(tk.END, str(tree))


if __name__ == "__main__":
    root = tk.Tk()
    app = BuddySystemApp(root)
    root.mainloop()
