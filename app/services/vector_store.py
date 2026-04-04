from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv


class VectorStore:
    """Clase para almacenar los vectores de los fragmentos de texto utilizando OpenAIEmbeddings."""
    def __init__(self, embeddings):
        load_dotenv() # Carga las variables de entorno desde el archivo .env
        self._embeddings = embeddings
        self.vector_store = None
        
    def create_vector_store(self, chunks):
        try:
            # Creando el vector store utilizando FAISS y los embeddings generados por OpenAIEmbeddings
            self.vector_store = FAISS.from_documents(chunks, self._embeddings)
            return self.vector_store
        except Exception as e:
            raise RuntimeError(f"Error al crear el vector store: {str(e)}")

    def get_retriever(self):
        if self.vector_store is None:
            raise ValueError("El vector store no ha sido creado. Llama a create_vector_store() primero.")
        return self.vector_store.as_retriever() # Devuelve un objeto retriever para realizar consultas de similitud en el vector store
