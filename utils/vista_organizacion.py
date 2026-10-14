import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from .organizador_modelo import organizar_con_modelo

def mostrar_organizacion(root, volver_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#F5F5F7")

    def seleccionar_carpeta(entry_widget):
        carpeta = filedialog.askdirectory()
        if carpeta:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, carpeta)

    def iniciar_organizacion():
        origen = entry_origen.get().strip()
        destino = entry_destino.get().strip()

        if not origen or not destino:
            messagebox.showwarning("Faltan datos", "Selecciona ambas carpetas antes de continuar.")
            return

        organizar_con_modelo(origen, destino)

    # Título
    tk.Label(root, text="Organización inteligente", font=("Helvetica", 18, "bold"),
             bg="#F5F5F7", fg="#000").pack(pady=(50, 10))

    tk.Label(root, text="Selecciona carpeta de origen y carpeta destino (semestre)", font=("Helvetica", 12),
             bg="#F5F5F7", fg="#888").pack(pady=(0, 30))

    # Carpeta origen
    frame_origen = tk.Frame(root, bg="#F5F5F7")
    frame_origen.pack(pady=10)
    tk.Label(frame_origen, text="Carpeta de origen:", bg="#F5F5F7", font=("Helvetica", 11)).pack(side="left", padx=5)
    entry_origen = tk.Entry(frame_origen, font=("Helvetica", 11), width=50)
    entry_origen.pack(side="left", padx=5)
    tk.Button(frame_origen, text="Seleccionar", command=lambda: seleccionar_carpeta(entry_origen),
              font=("Helvetica", 10), bg="#E0E0E0").pack(side="left")

    # Carpeta destino
    frame_destino = tk.Frame(root, bg="#F5F5F7")
    frame_destino.pack(pady=10)
    tk.Label(frame_destino, text="Carpeta de destino:", bg="#F5F5F7", font=("Helvetica", 11)).pack(side="left", padx=5)
    entry_destino = tk.Entry(frame_destino, font=("Helvetica", 11), width=50)
    entry_destino.pack(side="left", padx=5)
    tk.Button(frame_destino, text="Seleccionar", command=lambda: seleccionar_carpeta(entry_destino),
              font=("Helvetica", 10), bg="#E0E0E0").pack(side="left")

    # Botón iniciar
    tk.Button(root, text="Organizar Archivos", command=iniciar_organizacion,
              font=("Helvetica", 12, "bold"), bg="#34C759", fg="black", padx=10, pady=5).pack(pady=30)

    # Botón volver
    tk.Button(root, text="Volver al menú", command=volver_callback,
              font=("Helvetica", 12, "bold"), bg="#007AFF", fg="black", padx=10, pady=5).pack()