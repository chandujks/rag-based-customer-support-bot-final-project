from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

def load_pdf(path: str):
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"Knowledge PDF not found at {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    return loader.load()
