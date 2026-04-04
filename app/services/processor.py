from http.client import HTTPException

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFProcessor:
    '''Clase para procesar archivos PDF, cargarlos y dividirlos en fragmentos utilizando PyPDFLoader y RecursiveCharacterTextSplitter.'''
    def __init__(self, file_path):
        self.file_path = file_path
    def load_and_split(self, chunk_size=1000, chunk_overlap=200):
        try:
            loader = PyPDFLoader(self.file_path)
            # Cargando el documento PDF
            documents = loader.load()
            # Dividiendo el documento en fragmentos utilizando RecursiveCharacterTextSplitter
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunks = text_splitter.split_documents(documents)
        except ValueError as ve:
            raise ValueError(f"Error al cargar o dividir el PDF: {str(ve)}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo no encontrado: {self.file_path}")
        except Exception as e:
            raise RuntimeError(f"Error al procesar el archivo PDF: {str(e)}")

        # Devolviendo los fragmentos resultantes -> chunks
        return chunks
