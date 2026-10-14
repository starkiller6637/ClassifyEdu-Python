import os
import shutil
from tkinter import messagebox

def organizar_archivos(carpeta):
    categorias = {
        "Documentos": ['docx', 'txt'],
        "PDF": ['pdf'],
        "Videos": ['mp4', 'avi', 'mkv'],
        "Audios": ['mp3', 'wav']
    }

    if not os.path.exists(carpeta):
        messagebox.showerror("Error", "La carpeta seleccionada no existe.")
        return

    materia_dict = {}
    for materia in os.listdir(carpeta):
        materia_path = os.path.join(carpeta, materia)
        if os.path.isdir(materia_path):
            materia_dict[materia] = materia

    archivos_encontrados = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    if not archivos_encontrados:
        messagebox.showwarning("Aviso", "No se encontraron archivos en la carpeta seleccionada.")
        return

    for archivo in archivos_encontrados:
        ruta_archivo = os.path.join(carpeta, archivo)
        _, extension = os.path.splitext(archivo)
        extension = extension[1:].lower()

        destino_materia = None
        for materia, siglas in materia_dict.items():
            if siglas in archivo.upper() or any(word in archivo.upper() for word in materia.upper().split()):
                destino_materia = os.path.join(carpeta, siglas)
                break

        if destino_materia:
            destino_categoria = os.path.join(destino_materia, "Otros")
            for categoria, ext_list in categorias.items():
                if extension in ext_list:
                    destino_categoria = os.path.join(destino_materia, categoria)
                    break

            os.makedirs(destino_categoria, exist_ok=True)
            shutil.move(ruta_archivo, os.path.join(destino_categoria, archivo))

    messagebox.showinfo("Completado", "¡Los archivos han sido organizados correctamente!")