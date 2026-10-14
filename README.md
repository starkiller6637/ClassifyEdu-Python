# ClassifyEDU - Python

**Organizador de archivos académicos para estudiantes, desarrollado en Python.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-555555)
![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-v1%20%7C%20Legacy-6B7280)

> [!NOTE]
> **Esta es la primera versión de ClassifyEDU (Python).** Se conserva como referencia del proyecto original y como parte de mi portafolio. Actualmente estoy desarrollando una nueva versión con **TypeScript**, por separado. No se planean nuevas funcionalidades para esta implementación.

## Descripción

ClassifyEDU nació para resolver un problema cotidiano: los materiales de distintas materias terminan mezclados entre descargas, tareas, documentos y recursos multimedia.

La aplicación ofrece una interfaz de escritorio para **crear una estructura de carpetas por semestre y materia** y **organizar archivos automáticamente**. Para sugerir la materia de destino utiliza procesamiento de texto, representaciones TF-IDF, similitud de coseno y reglas de coincidencia de palabras.

**El procesamiento se realiza localmente** en el equipo que ejecuta la aplicación; esta versión no implementa servicios en la nube.

## Funcionalidades

- **Crear una estructura académica:** genera carpetas por semestre, materia y tipo de archivo.
- **Organizar materiales:** clasifica archivos de una carpeta de origen y los mueve a subcarpetas de la materia identificada.
- **Analizar documentos:** extrae texto de archivos `.pdf`, `.docx` y `.txt`.
- **Clasificar otros formatos:** admite imágenes, audio y video utilizando principalmente sus nombres de archivo, no un análisis de su contenido multimedia.
- **Conservar archivos no clasificados:** si la lógica de clasificación no encuentra una materia adecuada, el archivo permanece en la carpeta de origen.

### Ejemplo de organización

```text
Semestre/
├── Bases de Datos/
│   ├── Documentos/
│   ├── PDF/
│   ├── Videos/
│   ├── Audios/
│   └── Otros/
└── Programación/
    ├── Documentos/
    ├── PDF/
    ├── Videos/
    ├── Audios/
    └── Otros/
```

Los nombres de las materias y del semestre se definen desde la aplicación.

## Tecnologías

| Tecnología | Uso |
| --- | --- |
| **Python** | Lógica de la aplicación y manejo de archivos |
| **Tkinter** | Interfaz gráfica de escritorio |
| **scikit-learn** | Vectorización TF-IDF, entrenamiento y utilidades de Machine Learning |
| **NumPy** | Cálculos del proceso de entrenamiento |
| **PyPDF2 / python-docx** | Lectura de documentos PDF y Word |
| **joblib** | Carga y almacenamiento del modelo y sus representaciones |

### ¿Cómo clasifica los archivos?

1. Obtiene texto del documento, cuando es posible, y lo combina con su nombre.
2. Transforma el texto en un vector **TF-IDF**.
3. Compara el vector con representaciones de las materias utilizando **similitud de coseno**.
4. Cuando la similitud no supera el umbral configurado, intenta una coincidencia basada en palabras.
5. Si identifica una materia, mueve el archivo a la subcarpeta correspondiente; en caso contrario, lo deja en el origen.

> **Detalle técnico:** el script de entrenamiento incluye un `RandomForestClassifier`, pero la organización ejecutada por la interfaz se basa principalmente en similitud de coseno frente a centroides por materia y reglas de coincidencia. No debe interpretarse el puntaje de similitud como una probabilidad calibrada.

## Instalación y ejecución

### Requisitos

- Python 3 instalado.
- Tkinter disponible en la instalación de Python.
- Dependencias indicadas en `requirements.txt`.

Clona el repositorio y entra en su carpeta:

```bash
git clone https://github.com/starkiller6637/ClassifyEdu-Python.git
cd ClassifyEdu-Python
```

Crea un entorno virtual:

```bash
python -m venv .venv
```

Actívalo en **Windows (PowerShell)**:

```powershell
.venv\Scripts\Activate.ps1
```

O en **Linux/macOS**:

```bash
source .venv/bin/activate
```

Instala las dependencias e inicia la aplicación desde la **raíz del repositorio**:

```bash
python -m pip install -r requirements.txt
python main.py
```

> [!IMPORTANT]
> Esta versión utiliza rutas relativas para los iconos y el modelo, por lo que debe ejecutarse desde la carpeta principal del proyecto. El uso de `.ico` puede requerir ajustes en sistemas distintos de Windows. La compatibilidad multiplataforma no está verificada.

### Uso básico

1. En **Crear una nueva estructura**, escribe un semestre y las materias separadas por comas.
2. En **Organiza tus archivos de forma inteligente**, selecciona la carpeta de origen y la carpeta del semestre que recibirá los archivos.
3. Inicia la organización y revisa las carpetas de destino.

**Importante:** la aplicación **mueve los archivos originales**; no crea una copia ni ofrece una vista previa para confirmar cada movimiento. Pruébala primero con archivos de ejemplo o una copia de respaldo, especialmente si contienen trabajos importantes.

## Estructura del repositorio

```text
ClassifyEdu-Python/
├── main.py                      # Inicio de la interfaz
├── model/
│   └── model.py                 # Entrenamiento exploratorio
├── modelo_clasificador.pkl      # Artefacto del modelo incluido
├── utils/
│   ├── vista_creacion.py        # Pantalla de creación de carpetas
│   ├── vista_organizacion.py    # Pantalla de organización
│   ├── organizador_modelo.py    # Clasificación y movimiento de archivos
│   ├── lectura_archivos.py      # Lectura y clasificación por coincidencias
│   ├── organizador.py           # Organizador basado en reglas
│   └── gui.py                   # Código auxiliar histórico
└── requirements.txt
```

## Alcance y limitaciones de esta versión

- **Proyecto académico / prototipo:** no está planteado como una solución de producción.
- **Evaluación del modelo:** el entrenamiento original es exploratorio. Su preparación de datos no permite presentar las métricas obtenidas como una validación independiente y reproducible; por ello no se anuncia un porcentaje de precisión.
- **Entrenamiento no reproducible con este repositorio únicamente:** `model/model.py` espera una carpeta local `datasets/` que no se incluye. Para ese script también se necesitan bibliotecas de análisis y gráficos, como Matplotlib y Seaborn, no listadas en el `requirements.txt` original.
- **Compatibilidad:** el acceso a imágenes e iconos depende de rutas relativas y algunas utilidades se conservaron como parte de la implementación histórica.
- **Archivos especiales:** los PDF escaneados sin texto reconocible no cuentan con OCR; las imágenes, los audios y los videos no se interpretan semánticamente por su contenido.

## Evolución del proyecto

La siguiente versión de **ClassifyEDU** se encuentra en desarrollo con **TypeScript**. Este repositorio de Python se mantiene como registro del punto de partida y de los conceptos explorados: automatización de archivos, interfaz gráfica y clasificación basada en texto.

---

Desarrollado por [@starkiller6637](https://github.com/starkiller6637).
