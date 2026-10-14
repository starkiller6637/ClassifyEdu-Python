import os
import re
import joblib
import numpy as np
from collections import defaultdict, Counter
from docx import Document
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z\s]', ' ', texto)
    return texto.strip()

def leer_archivo(path):
    texto = ""
    try:
        if path.endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
        elif path.endswith(".pdf"):
            with open(path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    texto += page.extract_text() or ""
        elif path.endswith(".docx"):
            doc = Document(path)
            texto = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"❌ Error leyendo archivo {path}: {e}")
    return texto

def cargar_datos(carpeta_datasets):
    textos, etiquetas = [], []
    video_extensiones = ('.mp4', '.mov', '.avi', '.mkv')

    for materia in os.listdir(carpeta_datasets):
        path_materia = os.path.join(carpeta_datasets, materia)
        if os.path.isdir(path_materia):
            for tipo_contenido in os.listdir(path_materia):
                path_tipo = os.path.join(path_materia, tipo_contenido)
                if os.path.isdir(path_tipo):
                    for root, _, archivos in os.walk(path_tipo):
                        for archivo in archivos:
                            path_archivo = os.path.join(root, archivo)
                            nombre_archivo = os.path.splitext(archivo)[0]

                            if archivo.endswith(('.txt', '.pdf', '.docx')):
                                contenido = leer_archivo(path_archivo)
                                if contenido:
                                    texto_completo = f"{materia} {tipo_contenido} {nombre_archivo} {contenido}"
                                    texto_limpio = limpiar_texto(texto_completo)
                                    if len(texto_limpio.split()) < 20:
                                        continue
                                    textos.append(texto_limpio)
                                    etiquetas.append(materia)

                            elif archivo.endswith(video_extensiones):
                                nombre_archivo_repetido = (nombre_archivo + " ") * 2 
                                texto_limpio = limpiar_texto(f"{materia} {tipo_contenido} {nombre_archivo_repetido}")
                                if len(texto_limpio.split()) < 3:
                                    continue
                                textos.extend([texto_limpio] * 2) 
                                etiquetas.extend([materia] * 2)
    return textos, etiquetas

def entrenar_modelo():
    carpeta_datasets = "datasets"
    textos, etiquetas = cargar_datos(carpeta_datasets)

    if not textos:
        print("⚠️ No se encontraron textos válidos para entrenar.")
        return

    print("📊 Distribución de clases:")
    conteo = Counter(etiquetas)
    for materia, cantidad in conteo.items():
        print(f"  - {materia}: {cantidad} documentos")

    textos_expandidos, etiquetas_expandidas = [], []
    for texto, etiqueta in zip(textos, etiquetas):
        repeticiones = 2 if conteo[etiqueta] < 5 else 1
        textos_expandidos.extend([texto] * repeticiones)
        etiquetas_expandidas.extend([etiqueta] * repeticiones)

    vectorizer = TfidfVectorizer(max_features=8000, ngram_range=(1, 3))
    X = vectorizer.fit_transform(textos_expandidos)
    y = etiquetas_expandidas

    materia_vectores = defaultdict(list)
    for texto, materia in zip(textos_expandidos, etiquetas_expandidas):
        v = vectorizer.transform([texto])
        materia_vectores[materia].append(v.toarray()[0])

    materia_centroides = {}
    for materia, vectores in materia_vectores.items():
        centroide = np.mean(vectores, axis=0)
        materia_centroides[materia] = centroide

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestClassifier(class_weight='balanced')
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    print("\n📊 Reporte de clasificación:")
    print(classification_report(y_test, y_pred))

    labels = sorted(list(set(y)))
    mat = confusion_matrix(y_test, y_pred, labels=labels)
    plt.figure(figsize=(8, 6))
    sns.heatmap(mat, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap="Blues")
    plt.title("Matriz de confusión")
    plt.xlabel("Predicción")
    plt.ylabel("Real")
    plt.tight_layout()
    plt.show()

    joblib.dump((modelo, vectorizer, materia_centroides), "modelo_clasificador.pkl")
    print("✅ Modelo entrenado y guardado como 'modelo_clasificador.pkl'.")

if __name__ == "__main__":
    entrenar_modelo()