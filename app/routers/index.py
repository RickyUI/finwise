from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from app.services.vector_store import VectorStore
from app.services.processor import PDFProcessor

router = APIRouter(prefix="/index", tags=["index"])

load_dotenv() # Carga las variables de entorno desde el archivo .env

UPLOAD_DIR = "uploads"

@router.post("/index/", status_code=201)
async def index_files():
    # Verificamos que exista el directorio de uploads antes de intentar listar los archivos
    if not (os.path.exists(UPLOAD_DIR) and os.path.isdir(UPLOAD_DIR)):
        raise HTTPException(status_code=400, detail="El directorio de uploads no existe o no es un directorio válido.")
    
    # Inicializamos los embeddings y el vector store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY"))
    vector_store = VectorStore(embeddings)
    
    # Cargamos file.name de cada archivo en el directorio de uploads
    files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
    
    if not files:
        raise HTTPException(status_code=400, detail="No se encontraron archivos para indexar en el directorio de uploads.")
    
    try:
        for f in files:
            # 1. Verificar que el archivo no esté vacío antes de procesarlo
            with open(os.path.join(UPLOAD_DIR, f), "rb") as file:
                content = file.read() # Lee el contenido del archivo sin bloquearl el servidor, permitiendo que otros usuarios sean atentidos durante la espera
                if not content:
                    raise ValueError(f"El archivo '{f}' está vacío o no se pudo leer correctamente.")
                
            # 2. Procesar cada archivo PDF utilizando PDFProcessor para cargarlo y dividirlo en fragmentos
            processor = PDFProcessor(os.path.join(UPLOAD_DIR, f))
            chunks = processor.load_and_split(chunk_size=1000, chunk_overlap=200)
    
            # 3. Crear el vector store utilizando VectorStore y los fragmentos obtenidos del PDF
            vector_store.create_vector_store(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar los archivos: {str(e)}")
    
    return {
        "message": f"{len(files)} archivo(s) indexado(s) exitosamente.",
        "files": files
    }