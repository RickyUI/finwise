from fastapi import APIRouter, Request
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

router = APIRouter(prefix="/query", tags=["query"])


@router.get("/query/")
async def query(question: str, request: Request):
    """Endpoint para realizar consultas sobre los archivos indexados."""
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Eres un asistente financiero especializado en el análisis de documentos corporativos.
        Responde únicamente basándote en el contexto proporcionado.
        Si la información no está en el contexto, indícalo explícitamente en lugar de inventar una respuesta.
        Cita siempre la fuente (nombre del documento y página) de donde obtuviste la información.

        Contexto:
        {context}

        Pregunta:
        {question}

        Respuesta:
        """,
    )

    # Obtiene el retriever del vector store para realizar consultas de similitud
    vector_store = request.app.state.vector_store
    retriever = vector_store.get_retriever()
    
    # Recuperar los documents
    docs = retriever.invoke(question)

    # Construir la cadena de RAG utilizando el prompt template, el LLM y un output parser para obtener una respuesta formateada
    rag_chain = prompt_template | llm | StrOutputParser()
    response = rag_chain.invoke({
        "context": docs,
        "question": question
    })
    
    # Extraer las fuentes de los documentos utilizados para generar la respuesta
    src = []
    for doc in docs:
        source = doc.metadata.get("source", "desconocida")
        page = doc.metadata.get("page", "desconocida")
        src.append(f"{source} (página {page})")
    
    return {
        "response": response,
        "sources": src
    }
    
