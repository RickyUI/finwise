import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.models.schemas import QueryRequest, QueryResponse

# Carga las variables de entorno desde el archivo .env
load_dotenv()

router = APIRouter(prefix="/query", tags=["query"])


def _format_context(docs) -> str:
    formatted_docs = []
    for idx, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "desconocida")
        page = doc.metadata.get("page", "desconocida")
        formatted_docs.append(
            f"[Documento {idx}] {source} - pagina {page}\n{doc.page_content}"
        )
    return "\n\n".join(formatted_docs)


@router.post("/", response_model=QueryResponse)
async def query(request: Request, body: QueryRequest):
    """Endpoint para realizar consultas sobre los archivos indexados."""
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Eres un asistente financiero especializado en el analisis de documentos corporativos.
        Responde unicamente basandote en el contexto proporcionado.
        No inventes informacion ni completes huecos con suposiciones.
        Si la informacion no esta en el contexto, indicalo explicitamente dentro de la seccion correspondiente.
        Responde siempre en Markdown y usa exactamente esta estructura:

        ## Resumen ejecutivo
        Un parrafo breve con la conclusion principal.

        ## Hallazgos clave
        - Bullet 1
        - Bullet 2
        - Bullet 3

        ## Riesgos o alertas
        - Bullet 1
        - Bullet 2

        ## Fuentes
        - nombre_del_documento (pagina X)

        Reglas adicionales:
        - Usa bullets en Hallazgos clave y Riesgos o alertas.
        - Si no hay suficientes datos para una seccion, dilo explicitamente dentro de esa seccion.
        - En Fuentes cita solo documentos y paginas presentes en el contexto recuperado.
        - No agregues secciones extra.

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
    docs = retriever.invoke(body.question)

    # Construir la cadena de RAG utilizando el prompt template, el LLM y un output parser para obtener una respuesta formateada
    rag_chain = prompt_template | llm | StrOutputParser()
    response = rag_chain.invoke(
        {
            "context": _format_context(docs),
            "question": body.question,
        }
    )

    # Extraer las fuentes de los documentos utilizados para generar la respuesta
    src = []
    for doc in docs:
        source = doc.metadata.get("source", "desconocida")
        page = doc.metadata.get("page", "desconocida")
        src.append(f"{source} (pagina {page})")

    return QueryResponse(response=response, sources=src)
