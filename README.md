# FinWise

FinWise es una aplicacion para analizar documentos financieros en PDF con un flujo RAG. El proyecto combina un backend en FastAPI con un frontend en Gradio para subir archivos, cargarlos al sistema, consultarlos en lenguaje natural y obtener respuestas con sus fuentes.

## Estado actual del proyecto

- Backend API en FastAPI funcional.
- Frontend en Gradio operativo en `app/app.py`.
- Carga de multiples PDFs al directorio `uploads/`.
- Procesamiento de PDFs con `PyPDFLoader` y fragmentacion con `RecursiveCharacterTextSplitter`.
- Indexacion semantica en memoria con FAISS y embeddings de OpenAI.
- Consulta de documentos con un flujo RAG y devolucion de fuentes.
- Preguntas sugeridas y botones de analisis rapido en la interfaz.
- Formato fijo de respuesta para todo el chat con secciones de resumen, hallazgos, riesgos y fuentes.
- Reinicio del estado documental mediante eliminacion de archivos y limpieza del vector store.

## Stack tecnologico

- FastAPI
- Gradio
- LangChain
- OpenAI
- FAISS
- PyPDF
- Python dotenv

## Estructura del proyecto

```text
app/
|-- app.py                  # Frontend en Gradio
|-- main.py                 # App FastAPI y ciclo de vida del backend
|-- core/
|   |-- config.py
|   `-- constants.py
|-- models/
|   `-- schemas.py          # Modelos de request y response
|-- routers/
|   |-- upload.py           # Endpoints de carga, listado y limpieza de archivos
|   |-- index.py            # POST /index/
|   `-- query.py            # POST /query/
`-- services/
    |-- processor.py        # Carga y fragmentacion de PDFs
    `-- vector_store.py     # Gestion del indice FAISS
```

## Flujo de la aplicacion

1. El usuario sube uno o varios PDF a `/upload/`.
2. El backend guarda los archivos en `uploads/`.
3. Se llama `/index/` para cargar, dividir e indexar los documentos.
4. El usuario consulta `/query/` con una pregunta libre o dispara un analisis rapido desde la interfaz.
5. El sistema recupera contexto relevante y genera una respuesta en formato fijo con sus fuentes.
6. Si hace falta reiniciar la sesion documental, se pueden listar o eliminar archivos desde los endpoints de `upload`.

## Experiencia en la interfaz

Una vez que los archivos han sido cargados al chat, la interfaz de Gradio permite:

- Hacer preguntas libres en lenguaje natural.
- Lanzar analisis rapidos desde botones predefinidos.
- Usar preguntas sugeridas como punto de partida para explorar el contenido.
- Recibir respuestas con una estructura fija para facilitar la lectura.

Los analisis rapidos incluidos actualmente son:

- `Resumen ejecutivo`
- `Hallazgos clave`
- `Riesgos y alertas`
- `Metricas financieras`
- `Guidance y outlook`

El formato de respuesta del asistente sigue esta estructura:

- `Resumen ejecutivo`
- `Hallazgos clave`
- `Riesgos o alertas`
- `Fuentes`

## Endpoints disponibles

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| POST | `/upload/` | Recibe y guarda uno o varios archivos PDF |
| GET | `/upload/files` | Devuelve la lista de archivos subidos actualmente |
| DELETE | `/upload/delete` | Elimina todos los archivos subidos y reinicia el vector store |
| POST | `/index/` | Procesa los PDFs guardados y construye el indice FAISS |
| POST | `/query/` | Responde preguntas usando los documentos cargados |

## Variables de entorno

Crea un archivo `.env` a partir de `.env.example`:

```env
OPENAI_API_KEY=sk-...
```

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecucion del backend

```bash
uvicorn app.main:app --reload
```

Documentacion interactiva:

```text
http://localhost:8000/docs
```

## Ejecucion del frontend

Con el backend corriendo, abre otra terminal y ejecuta:

```bash
python app/app.py
```

La interfaz de Gradio te permite:

- Subir archivos PDF.
- Cargar los archivos al chat.
- Hacer preguntas libres sobre el contenido.
- Usar preguntas sugeridas y botones de analisis rapido.
- Ver respuestas en formato fijo con fuentes.
- Limpiar la conversacion sin tocar los archivos ya cargados.

## Notas tecnicas

- El indice FAISS vive en memoria y se reinicia cuando el servidor se apaga.
- `app.state.vector_store` comparte la instancia del vector store entre los routers.
- La logica de consulta al LLM esta actualmente dentro de `app/routers/query.py`.
- El formato fijo de las respuestas se controla desde el prompt del endpoint `POST /query/`.
- El endpoint `DELETE /upload/delete` tambien reinicia el vector store para dejar la sesion limpia.
