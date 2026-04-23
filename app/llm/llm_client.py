from langchain_community.chat_models import ChatOllama
from app.config import settings

def get_llm():
    return ChatOllama(
        model=settings.OLLAMA_MODEL,
        temperature=0
    )