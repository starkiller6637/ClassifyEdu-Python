import tkinter as tk
from tkinter import messagebox
import os

def mostrar_creacion(root, volver_callback):
    def crear_estructura():
        semestre = entry_semestre.get().strip()
        materias_texto = entry_materias.get().strip()

        if not semestre or not materias_texto:
            messagebox.showwarning("Faltan datos", "Por favor ingresa el semestre y al menos una materia.")
            return

        carpeta_semestre = os.path.join(os.getcwd(), semestre)
        os.makedirs(carpeta_semestre, exist_ok=True)

        materias = [m.strip() for m in materias_texto.split(",") if m.strip()]
        if not materias:
            messagebox.showwarning("Error", "No se detectaron materias válidas.")
            return

        for materia in materias:
            materia_path = os.path.join(carpeta_semestre, materia)
            os.makedirs(materia_path, exist_ok=True)

            for categoria in ["Documentos", "PDF", "Videos", "Audios", "Otros"]:
                os.makedirs(os.path.join(materia_path, categoria), exist_ok=True)

        messagebox.showinfo("Estructura creada", f"Se creó la estructura para el semestre: {semestre}")

        # Limpiar inputs
        entry_semestre.delete(0, tk.END)
        entry_materias.delete(0, tk.END)

    # Limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#F5F5F7")

    # Título
    tk.Label(root, text="Creación de nueva estructura", font=("Helvetica", 18, "bold"),
             bg="#F5F5F7", fg="#000000").pack(pady=(50, 10))

    # Instrucciones
    tk.Label(root, text="Ingresa tu semestre y las materias separadas por comas", font=("Helvetica", 12),
             bg="#F5F5F7", fg="#888").pack(pady=(0, 20))

    # Campo semestre
    tk.Label(root, text="Semestre:", bg="#F5F5F7", font=("Helvetica", 11)).pack()
    entry_semestre = tk.Entry(root, font=("Helvetica", 12), width=40)
    entry_semestre.pack(pady=(0, 15))

    # Campo materias
    tk.Label(root, text="Materias (separadas por coma):", bg="#F5F5F7", font=("Helvetica", 11)).pack()
    entry_materias = tk.Entry(root, font=("Helvetica", 12), width=60)
    entry_materias.pack(pady=(0, 30))

    # Botón crear estructura
    tk.Button(root, text="Crear estructura", command=crear_estructura,
              font=("Helvetica", 12, "bold"), bg="#34C759", fg="black", padx=10, pady=5).pack(pady=(0, 20))

    # Botón volver
    tk.Button(root, text="Volver al menú", command=volver_callback,
              font=("Helvetica", 12, "bold"), bg="#007AFF", fg="black", padx=10, pady=5).pack()