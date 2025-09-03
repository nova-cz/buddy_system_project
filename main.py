import tkinter as tk
from gui.main_window import BuddySystemApp


def main():
    root = tk.Tk()
    app = BuddySystemApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
