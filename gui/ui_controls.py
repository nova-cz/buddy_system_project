from tkinter import messagebox


class UIControls:
    def __init__(self, app):
        """
        Recibe la referencia a la ventana principal (BuddySystemApp)
        para poder acceder a sus entradas, área de texto y al BuddySystem.
        """
        self.app = app

    def init_memory(self):
        try:
            size = int(self.app.entry_size.get())
            self.app.buddy = self.app.BuddySystem(size)
            self.show_tree()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")

    def add_process(self):
        if not self.app.buddy:
            messagebox.showerror("Error", "Primero inicialice la memoria.")
            return
        name = self.app.entry_process.get()
        try:
            size = int(self.app.entry_p_size.get())
            ok = self.app.buddy.allocate(name, size)
            if ok:
                self.show_tree()
            else:
                messagebox.showwarning("Aviso", "No se pudo asignar el proceso.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un tamaño válido.")

    def remove_process(self):
        if not self.app.buddy:
            messagebox.showerror("Error", "Primero inicialice la memoria.")
            return
        name = self.app.entry_remove.get()
        ok = self.app.buddy.deallocate(name)
        if ok:
            self.show_tree()
        else:
            messagebox.showwarning("Aviso", "No se encontró el proceso.")

    def clear_memory(self):
        if self.app.buddy:
            self.app.buddy.reset_memory()
            self.show_tree()

    def show_tree(self):
        """Muestra el árbol en el área de texto como diccionario"""
        self.app.text_area.delete("1.0", "end")
        tree = self.app.buddy.get_tree()
        self.app.text_area.insert("end", str(tree))
