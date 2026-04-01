# 📋 Roadmap: Document Intelligence API

Proyecto de RAG (Retrieval-Augmented Generation) con memoria conversacional para análisis de documentos PDF.

---

## 🛠 Fase 1: Backend & Ingestión (Día 1)
*Objetivo: Procesar el documento y preparar el motor de búsqueda.*

- [x] **Configuración del Entorno**
    - [x] Inicializar repositorio y `.gitignore`.
    - [x] Configurar variables de entorno (`.env`) para las API Keys.
    - [x] Instalar dependencias: `fastapi`, `langchain`, `faiss-cpu`, `pypdf`, `anthropic`.
- [x] **Pipeline de Procesamiento**
    - [x] Crear script de carga de PDF con `PyPDFLoader`.
    - [x] Implementar `RecursiveCharacterTextSplitter` para el chunking (probar 1000 tokens con 200 de overlap).
- [x] **Vector Store**
    - [x] Configurar `FAISS` localmente.
    - [x] Generar embeddings de los chunks y guardarlos en el vector store.
- [ ] **API Inicial (FastAPI)**
    - [ ] Endpoint `POST /upload`: Recibir archivo, procesar y confirmar indexación.

---

## 💬 Fase 2: Lógica del Chat & RAG (Día 2)
*Objetivo: Conectar el conocimiento extraído con el modelo de lenguaje.*

- [ ] **Integración de LLM**
    - [ ] Configurar el cliente de Claude (Anthropic) mediante LangChain.
- [ ] **Cadena de Recuperación (Retrieval Chain)**
    - [ ] Crear el prompt template (System Message + Contexto + Pregunta).
    - [ ] Implementar `RetrievalQA` o `create_retrieval_chain`.
- [ ] **Memoria Conversacional**
    - [ ] Integrar `ConversationBufferMemory`.
    - [ ] Asegurar que el historial se mantenga durante la sesión del chat.
- [ ] **Endpoint de Inferencia**
    - [ ] Endpoint `POST /chat`: Recibir la pregunta del usuario y devolver la respuesta contextualizada.

---

## ✨ Fase 3: Interfaz & Documentación (Día 3)
*Objetivo: Hacer el proyecto presentable y funcional para terceros.*

- [ ] **Interfaz de Usuario (Opcional)**
    - [ ] Crear un cliente simple en Streamlit para subir archivos y chatear.
- [ ] **Refactorización y Testing**
    - [ ] Manejo de errores (PDFs corruptos, límites de API).
    - [ ] Validar respuestas consistentes con el contenido del PDF.
- [ ] **Documentación Final**
    - [ ] Pulir los esquemas de Pydantic para que el Swagger (`/docs`) sea auto-explicativo.
    - [ ] Redactar el `README.md` con:
        - [ ] Arquitectura del sistema.
        - [ ] Guía de instalación rápida.
        - [ ] Screenshots o ejemplos de uso (cURL/UI).

---

## 🚀 Notas Adicionales / Ideas Pro
- [ ] ¿Añadir soporte para múltiples archivos simultáneos?
- [ ] ¿Implementar persistencia de FAISS en disco para no re-indexar cada vez?