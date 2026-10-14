import tkinter as tk
from tkinter import filedialog
from .estructura import crear_estructura_academica
from .organizador_modelo import organizar_con_modelo

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta de tu semestre")
    if carpeta:
        organizar_archivos(carpeta)

def seleccionar_modo():
    ventana_modo = tk.Toplevel()
    ventana_modo.title("Seleccionar Modo")
    ventana_modo.geometry("700x500")
    ventana_modo.configure(bg="#F5F5F7")
    ventana_modo.resizable(False, False)

    # Íconos
    icono_estructura = tk.PhotoImage(file="icono_estructura.png")
    icono_organizar = tk.PhotoImage(file="icono_organizar.png")

    # Título y subtítulo
    tk.Label(ventana_modo, text="¿Qué deseas hacer con ClassifyEDU?", font=("Helvetica", 18, "bold"),
             bg="#F5F5F7", fg="#000").pack(pady=(30, 0))

    tk.Label(ventana_modo, text="Selecciona la acción que deseas realizar", font=("Helvetica", 12),
             bg="#F5F5F7", fg="#888").pack(pady=(0, 30))

    def crear_opcion(master, icono, titulo, descripcion, comando):
        frame = tk.Frame(master, bg="#FFFFFF", bd=1, relief="solid", padx=15, pady=15)
        frame.pack(fill="x", padx=50, pady=10)

        tk.Label(frame, image=icono, bg="#FFFFFF").pack(side="left", padx=10)
        textos = tk.Frame(frame, bg="#FFFFFF")
        textos.pack(side="left", fill="both", expand=True)
        tk.Label(textos, text=titulo, font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#333").pack(anchor="w")
        tk.Label(textos, text=descripcion, font=("Helvetica", 10), bg="#FFFFFF", fg="#888").pack(anchor="w")

        frame.bind("<Button-1>", lambda e: (ventana_modo.destroy(), comando()))
        textos.bind("<Button-1>", lambda e: (ventana_modo.destroy(), comando()))

    # Opciones
    crear_opcion(ventana_modo, icono_estructura, "Crea una nueva estructura",
                 "Genera carpetas organizadas por semestres y materias.", crear_estructura_academica)

    crear_opcion(ventana_modo, icono_organizar, "Organiza tus archivos de forma inteligente",
                 "Clasifica automáticamente tus archivos.", organizar_con_modelo)

    # Mantener referencias de imagen
    ventana_modo.icono_estructura = icono_estructura
    ventana_modo.icono_organizar = icono_organizar