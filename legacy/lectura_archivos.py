import os
import shutil
import difflib
import re
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
from docx import Document

def limpiar_texto(texto):
    texto = texto.upper()
    texto = re.sub(r'[^A-Z\s]', '', texto)
    palabras = [p for p in texto.split() if len(p) > 4]
    return palabras

def clasificar_archivos_por_materia(archivos, carpeta_origen, materias_existentes, carpeta_semestre):
    omitidos = []
    clasificados = []

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_origen, archivo)
        extension = os.path.splitext(archivo)[1].lower()
        contenido = ""

        try:
            if extension == ".pdf":
                reader = PdfReader(ruta_archivo)
                for page in reader.pages[:2]:
                    contenido += page.extract_text() or ""
            elif extension == ".docx":
                doc = Document(ruta_archivo)
                for para in doc.paragraphs[:10]:
                    contenido += para.text + " "
        except Exception as e:
            print(f"No se pudo leer {archivo}: {e}")
            omitidos.append((archivo, "Error de lectura"))
            continue

        palabras = limpiar_texto(contenido)
        mejor_materia = None
        coincidencias_materia = {}

        for materia in materias_existentes:
            materia_path = os.path.join(carpeta_semestre, materia)
            materia_nombre = os.path.basename(materia_path)
            materia_palabras = limpiar_texto(materia_nombre)

            coincidencias = 0
            for palabra_materia in materia_palabras:
                similares = difflib.get_close_matches(palabra_materia, palabras, n=1, cutoff=0.85)
                if similares:
                    coincidencias += 1
            if coincidencias >= 1:
                coincidencias_materia[materia] = coincidencias

        if coincidencias_materia:
            mejor_materia = max(coincidencias_materia, key=coincidencias_materia.get)
            clasificados.append((archivo, mejor_materia, extension))
        else:
            print(f"Omitido: {archivo} (sin coincidencias suficientes)")
            omitidos.append((archivo, "Sin coincidencias fuertes"))

    return clasificados, omitidos

def mover_archivos(clasificados, carpeta_origen, carpeta_semestre):
    for archivo, mejor_materia, extension in clasificados:
        ruta_archivo = os.path.join(carpeta_origen, archivo)
        subcarpeta = "PDF" if extension == ".pdf" else "Documentos"
        destino = os.path.join(carpeta_semestre, mejor_materia, subcarpeta)
        os.makedirs(destino, exist_ok=True)
        shutil.move(ruta_archivo, os.path.join(destino, archivo))
        print(f"Movido: {archivo} → {destino} (match: {mejor_materia})")

def mover_archivos_por_materia():
    carpeta_origen = filedialog.askdirectory(title="Selecciona la carpeta con los archivos PDF y Word")
    if not carpeta_origen:
        return

    carpeta_semestre = os.path.join(os.getcwd(), "7mo Semestre")

    materias_existentes = [
        carpeta for carpeta in os.listdir(carpeta_semestre)
        if os.path.isdir(os.path.join(carpeta_semestre, carpeta)) and carpeta.upper() not in ["DOCUMENTOS", "PDF", "VIDEOS", "AUDIOS", "OTROS"]
    ]

    if not materias_existentes:
        messagebox.showerror("Error", "No se encontraron carpetas de materias.")
        return

    archivos = [archivo for archivo in os.listdir(carpeta_origen) if archivo.lower().endswith((".pdf", ".docx"))]
    if not archivos:
        messagebox.showwarning("Aviso", "No se encontraron archivos PDF ni Word en la carpeta seleccionada.")
        return

    clasificados, omitidos = clasificar_archivos_por_materia(archivos, carpeta_origen, materias_existentes, carpeta_semestre)
    mover_archivos(clasificados, carpeta_origen, carpeta_semestre)

    messagebox.showinfo("Completado", "Todos los archivos fueron organizados con éxito.")