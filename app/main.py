from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import OpenAIEmbeddings
from app.services.vector_store import VectorStore
from app.routers import upload, query, index
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al arrancar el servidor
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    app.state.vector_store = VectorStore(embeddings)
    
    yield # El servidor está corriendo y atendiendo solicitudes
    
    # Cierre - cleanup
    app.state.vector_store.reset()

app = FastAPI(lifespan=lifespan)

app.include_router(upload.router)
app.include_router(query.router)
app.include_router(index.router)

