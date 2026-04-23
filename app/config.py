import os
from pathlib import Path


class Settings:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_PDF_PATH = BASE_DIR / "data" / "knowledge.pdf"
    CHROMA_PATH = BASE_DIR / "chroma_db"
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_collection")
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
    TOP_K = int(os.getenv("TOP_K", "3"))
    RETRIEVAL_SCORE_THRESHOLD = float(os.getenv("RETRIEVAL_SCORE_THRESHOLD", "0.2"))
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
    ENABLE_HITL = os.getenv("ENABLE_HITL", "false").lower() == "true"


settings = Settings()
