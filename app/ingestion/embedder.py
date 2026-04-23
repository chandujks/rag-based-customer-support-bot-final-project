from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )
