from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException

import os

router = APIRouter(prefix="/files", tags=["files"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_CONTENT_TYPES = {"application/pdf"}


@router.post("/upload/", status_code=201)
async def upload_file(files: List[UploadFile] = File(...)):
    
    # 1. Validar todos los archivos antes de guardar
    for f in files:
        if not f.content_type or f.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=415, detail=f"Archivo '{f.filename}' no es un PDF válido.")
        
    # 2. Guardar los archivos válidos
    saved_files = []
    for f in files:
        file_path = os.path.join(UPLOAD_DIR, f.filename)
        try:
            with open(file_path, "wb") as buffer:
                content = await f.read() # Lee el contenido del archivo sin bloquearl el servidor, permitiendo que otros usuarios sean atentidos durante la espera
                buffer.write(content)
            saved_files.append(f.filename)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar el archivo '{f.filename}': {str(e)}")
        
    return {
        "message": f"{len(saved_files)} archivo(s) subido(s) exitosamente.",
        "files": saved_files
    }
    
