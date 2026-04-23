from langchain_community.vectorstores import Chroma
from app.config import settings

def create_vector_store(docs, embedding):
    return Chroma.from_documents(
        docs,
        embedding,
        persist_directory=str(settings.CHROMA_PATH),
        collection_name=settings.COLLECTION_NAME
    )

def load_vector_store(embedding):
    return Chroma(
        persist_directory=str(settings.CHROMA_PATH),
        embedding_function=embedding,
        collection_name=settings.COLLECTION_NAME
    )
