import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

PDF_PATH = "data/company.pdf"
VECTOR_PATH = "data/faiss_index"

def ingest_pdf():
    print("🔍 Checking PDF path:", PDF_PATH)

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found at {PDF_PATH}")

    os.makedirs(VECTOR_PATH, exist_ok=True)

    print("📄 Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} pages")

    print("✂️ Splitting text...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.split_documents(documents)
    print(f"✅ Created {len(docs)} chunks")

    print("🧠 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("💾 Building FAISS index...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(VECTOR_PATH)

    print("🎉 FAISS index saved at:", VECTOR_PATH)

if __name__ == "__main__":
    ingest_pdf()
