from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# TODO: Realizar la correción de la clase VectorStore para que no tenga problemas con FastAPI

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY"))

class VectorStore:
    """Clase para almacenar los vectores de los fragmentos de texto utilizando OpenAIEmbeddings."""
    
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.vector_store = None
        
    def create_vector_store(self, chunks):
        # Creando el vector store utilizando FAISS y los embeddings generados por OpenAIEmbeddings
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        return self.vector_store
    
    def get_retriever(self):
        if self.vector_store is None:
            raise ValueError("El vector store no ha sido creado. Llama a create_vector_store() primero.")
        return self.vector_store.as_retriever() # Devuelve un objeto retriever para realizar consultas de similitud en el vector store
