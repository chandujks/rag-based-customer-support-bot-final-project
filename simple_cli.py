from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama

print("🚀 Simple RAG CLI Starting...")

# 1. Load PDF
loader = PyPDFLoader("data/knowledge.pdf")
docs = loader.load()

# 2. Split
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)

print("Chunks:", len(chunks))

# 3. Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Vector DB (in-memory, no bugs)
db = Chroma.from_documents(chunks, embeddings)

# 5. Retriever
retriever = db.as_retriever(search_kwargs={"k": 3})

# 6. LLM (Ollama)
llm = ChatOllama(
    model="phi3",
    base_url="http://127.0.0.1:11434",
    temperature=0
)

print("✅ Ready! Type 'exit' to quit\n")

# 7. Chat loop
while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    docs = retriever.invoke(query)

    if not docs:
        print("Bot: I don't know\n")
        continue

    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
Answer using the context only.

Context:
{context}

Question:
{query}
"""

    try:
        response = llm.invoke(prompt)
        print("\nBot:", response.content, "\n")
    except Exception as e:
        print("LLM Error:", e)