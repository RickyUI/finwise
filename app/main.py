from fastapi import FastAPI, HTTPException, UploadFile, File
from app.services.processor import PDFProcessor
from app.services.vector_store import VectorStore
import os
