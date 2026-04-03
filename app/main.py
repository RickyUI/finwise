from fastapi import FastAPI, HTTPException, UploadFile, File
from app.services.processor import PDFProcessor
from app.services.vector_store import VectorStore
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True) # Garantiza que el directorio exista

# POST Endpoint que realiza la siguiente logica: UPLOAD -> CHUNKING -> INDEXING -> VECTOR STORE
@app.post("/upload/", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    # 1. Verificando que unicamente acepte .pdf
    if not file.content_type or file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Solo se permiten archivos PDF (application/pdf)"
        )
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # 2. Guardar el archivo de forma segura con manejo de errores
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read() # Leer el contenido del archivo de forma asíncrona
            buffer.write(content) # Escribir el contenido en el archivo
    except OSError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar el archivo: {str(e)}"
        )
    
    # 3. Procesar el PDF: Cargar y dividir en fragmentos
    try:
        processor = PDFProcessor(file_path=file_path)
        chunks = processor.load_and_split()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el PDF: {str(e)}"
        )
    
    # 4. Crear el vector store utilizando los fragmentos y los embeddings
    try:
        vector_store = VectorStore()
        vector_store.create_vector_store(chunks=chunks)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear el vector store: {str(e)}"
        )
        
    # 5. Retornar respuesta serializable JSON con el mensaje de éxito y el número de fragmentos procesados
    return {
        "message": "Archivo PDF procesado y vector store creado exitosamente.",
        "filename": file.filename,
        "num_chunks": len(chunks)
    }