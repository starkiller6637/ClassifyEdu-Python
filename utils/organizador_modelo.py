import os
import shutil
import re
import joblib
import unicodedata
from tkinter import messagebox
from docx import Document
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity

EXTENSIONES_VIDEO = ('.mp4', '.mov', '.avi', '.mkv')
EXTENSIONES_IMAGEN = ('.jpg', '.jpeg', '.png', '.gif')
EXTENSIONES_AUDIOS = ('.mp3', '.wav', '.ogg', '.flac')

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z\s]', ' ', texto)
    return texto.strip()

def limpiar_texto_match(texto):
    texto = texto.upper()
    texto = re.sub(r'[^A-Z\s]', '', texto)
    palabras = [p for p in texto.split() if len(p) > 4]
    return palabras

def leer_archivo(path):
    texto = ""
    try:
        if path.endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
        elif path.endswith(".pdf"):
            with open(path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages[:2]:
                    texto += page.extract_text() or ""
        elif path.endswith(".docx"):
            doc = Document(path)
            texto = "\n".join([p.text for p in doc.paragraphs[:10]])
    except Exception as e:
        print(f"❌ Error leyendo archivo {path}: {e}")
    return texto

def clasificar_por_match(texto_original, materias_existentes):
    palabras_doc = set(limpiar_texto_match(texto_original))
    mejor_materia = None
    mejor_score = 0

    for materia in materias_existentes:
        materia_normalizada = re.sub(r'[^A-Z\s]', '', normalizar(materia).upper())
        palabras_materia = set(materia_normalizada.split())
        interseccion = palabras_materia & palabras_doc

        print(f"🧩 Match con '{materia}': {len(interseccion)} palabras comunes → {sorted(interseccion)}")

        if len(interseccion) > mejor_score:
            mejor_score = len(interseccion)
            mejor_materia = materia

    if mejor_materia:
        print(f"✅ Clasificación por palabras: {mejor_materia} (coincidencias: {mejor_score})")
    else:
        print(f"❌ Sin coincidencias con materias: {materias_existentes}")
    
    return mejor_materia if mejor_score >= 1 else None


def organizar_con_modelo(carpeta_origen=None, carpeta_semestre=None):
    modelo_path = "modelo_clasificador.pkl"
    if not os.path.exists(modelo_path):
        messagebox.showerror("Error", "El modelo clasificador no se encontró.")
        return

    modelo, vectorizer, materia_centroides = joblib.load(modelo_path)

    if not carpeta_origen or not os.path.exists(carpeta_origen):
        messagebox.showerror("Error", "Debes seleccionar una carpeta de origen válida.")
        return

    if not carpeta_semestre or not os.path.exists(carpeta_semestre):
        messagebox.showerror("Error", "Debes seleccionar una carpeta de destino válida.")
        return

    materias_existentes = [
        carpeta for carpeta in os.listdir(carpeta_semestre)
        if os.path.isdir(os.path.join(carpeta_semestre, carpeta)) and carpeta.upper() not in ["DOCUMENTOS", "PDF", "VIDEOS", "AUDIOS", "OTROS"]
    ]

    if not materias_existentes:
        materias_existentes = list(materia_centroides.keys())
        print(f"⚠️ No se encontraron carpetas físicas, usando materias del modelo: {materias_existentes}")
    else:
        print(f"📚 Materias detectadas: {materias_existentes}")

    archivos = [a for a in os.listdir(carpeta_origen) if not a.startswith(".")]

    if not archivos:
        messagebox.showwarning("Aviso", "No se encontraron archivos compatibles.")
        return

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_origen, archivo)
        extension = os.path.splitext(archivo)[1].lower()
        nombre_archivo = os.path.splitext(archivo)[0]

        if extension == ".pdf":
            tipo_contenido = "PDF"
        elif extension in EXTENSIONES_VIDEO:
            tipo_contenido = "Videos"
        elif extension in EXTENSIONES_IMAGEN:
            tipo_contenido = "Imagenes"
        elif extension in EXTENSIONES_AUDIOS:
            tipo_contenido = "Audios"
        elif extension in ('.docx', '.txt'):
            tipo_contenido = "Documentos"
        else:
            tipo_contenido = "Otros"

        contenido = leer_archivo(ruta_archivo) if extension in ('.pdf', '.docx', '.txt') else ""

        if "individual" in nombre_archivo.lower():
            contenido += " temas selectos de optimizacion optimizacion heuristicas metaheuristicas seleccion"

        combinado = f"{tipo_contenido} {nombre_archivo} {contenido}"
        texto_limpio = limpiar_texto(combinado)

        if len(texto_limpio.split()) < 5 and extension in ('.pdf', '.docx', '.txt'):
            print(f"⚠️ {archivo} omitido: texto insuficiente")
            continue

        print(f"\n📂 Clasificando archivo: {archivo}")
        print(f"🔎 Texto limpio:\n{texto_limpio[:300]}...\n")

        vector = vectorizer.transform([texto_limpio]).toarray()[0]
        similitudes = {materia: cosine_similarity([vector], [centroide])[0][0] for materia, centroide in materia_centroides.items()}
        mejor_materia = max(similitudes, key=similitudes.get)
        mejor_similitud = similitudes[mejor_materia]

        if mejor_similitud < 0.58:
            print(f"⚠️ Similitud ({mejor_similitud:.2f}) insuficiente. Buscando por coincidencias de palabras...")
            mejor_materia_match = clasificar_por_match(combinado, materias_existentes)
            if mejor_materia_match:
                mejor_materia = mejor_materia_match
                print(f"📌 {archivo} → Clasificado por coincidencia → {mejor_materia}")
            else:
                mejor_materia = "No_Clasificados"
                print(f"❌ {archivo} → No clasificado")
        else:
            print(f"📌 {archivo} → {mejor_materia} (similitud: {mejor_similitud:.2f})")

        if mejor_materia == "No_Clasificados":
            print(f"📎 {archivo} se queda en la carpeta de origen (no clasificado).")
            continue

        mejor_materia_normalizada = normalizar(mejor_materia)
        carpeta_materia = os.path.join(carpeta_semestre, mejor_materia_normalizada)

        if not os.path.exists(carpeta_materia):
            print(f"⚠️ Carpeta '{mejor_materia}' no existe físicamente. Creando...")
            os.makedirs(carpeta_materia, exist_ok=True)

        destino = os.path.join(carpeta_materia, tipo_contenido)
        os.makedirs(destino, exist_ok=True)
        shutil.move(ruta_archivo, os.path.join(destino, archivo))

    print("\n✅ Clasificación terminada.")
    messagebox.showinfo("Completado", "Los archivos fueron organizados correctamente.")
