from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

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
    
    def save_vector_store(self, file_path):
        # Guardando el vector store en un archivo utilizando FAISS
        if self.vector_store:
            self.vector_store.save_local(file_path)
        else:
            raise ValueError("El vector store no ha sido creado. Por favor, cree el vector store antes de guardarlo.")
        
    def load_vector_store(self, file_path):
        # Cargando el vector store desde un archivo utilizando FAISS
        self.vector_store = FAISS.load_local(file_path, self.embeddings, allow_dangerous_deserialization=True)
        return self.vector_store
    
    def query_vector_store(self, query):
        # Realizando una consulta al vector store utilizando FAISS
        if self.vector_store:
            results = self.vector_store.similarity_search(query)
            return results
        else:
            raise ValueError("El vector store no ha sido creado. Por favor, cree el vector store antes de realizar una consulta.")
