import tkinter as tk
from pathlib import Path
from ui.vista_creacion import mostrar_creacion
from ui.vista_organizacion import mostrar_organizacion

ASSETS_DIR = Path(__file__).resolve().parent / "assets" / "icons"

def mostrar_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    # Íconos
    icono_estructura = tk.PhotoImage(file=str(ASSETS_DIR / "icono_puzzle.png"))
    icono_organizar = tk.PhotoImage(file=str(ASSETS_DIR / "icono_inteligente.png"))

    tk.Label(root, text="¿Qué deseas hacer con ClassifyEDU?", font=("Helvetica", 18, "bold"),
             bg="#F5F5F7", fg="#000").pack(pady=(50, 0))

    tk.Label(root, text="Selecciona la acción que deseas realizar", font=("Helvetica", 12),
             bg="#F5F5F7", fg="#888").pack(pady=(0, 30))

    def crear_opcion(master, icono, titulo, descripcion, comando):
        frame = tk.Frame(master, bg="#FFFFFF", bd=1, relief="solid", padx=15, pady=15)
        frame.pack(fill="x", padx=100, pady=10)

        tk.Label(frame, image=icono, bg="#FFFFFF").pack(side="left", padx=10)
        textos = tk.Frame(frame, bg="#FFFFFF")
        textos.pack(side="left", fill="both", expand=True)
        tk.Label(textos, text=titulo, font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#333").pack(anchor="w")
        tk.Label(textos, text=descripcion, font=("Helvetica", 10), bg="#FFFFFF", fg="#888").pack(anchor="w")

        frame.bind("<Button-1>", lambda e: comando())
        textos.bind("<Button-1>", lambda e: comando())

    crear_opcion(root, icono_estructura, "Crea una nueva estructura",
                 "Genera carpetas organizadas por semestres y materias.",
                 lambda: mostrar_creacion(root, lambda: mostrar_menu(root)))

    crear_opcion(root, icono_organizar, "Organiza tus archivos de forma inteligente",
                 "Clasifica automáticamente tus archivos.",
                 lambda: mostrar_organizacion(root, lambda: mostrar_menu(root)))

    # Guardar referencias
    root.icono_estructura = icono_estructura
    root.icono_organizar = icono_organizar

def main():
    root = tk.Tk()
    root.iconbitmap(str(ASSETS_DIR / "logoc.ico"))
    root.title("ClassifyEDU")
    root.geometry("800x600")
    root.configure(bg="#F5F5F7")
    root.resizable(False, False)

    mostrar_menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()