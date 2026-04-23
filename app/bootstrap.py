from app.config import settings
from app.ingestion.chunker import chunk_docs
from app.ingestion.embedder import get_embeddings
from app.ingestion.loader import load_pdf
from app.retrieval.retriever import get_retriever
from app.vectorstore.chroma_store import create_vector_store, load_vector_store
from app.workflow.graph import build_graph


def initialize_graph():
    embedding = get_embeddings()

    if settings.CHROMA_PATH.exists():
        vector_store = load_vector_store(embedding)
    else:
        docs = load_pdf(str(settings.DATA_PDF_PATH))
        chunks = chunk_docs(docs)
        vector_store = create_vector_store(chunks, embedding)

    retriever = get_retriever(vector_store)
    return build_graph(retriever)
