import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# ---------------- CONFIG ----------------
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

PDF_PATH = "data/company.pdf"
VECTOR_PATH = "data/faiss_index"

st.set_page_config(
    page_title="Admin Panel • Company AI",
    page_icon="🔐"
)

st.title("🔐 Admin Panel")

# ---------------- AUTH ----------------
if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False

if not st.session_state.admin_auth:
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.success("Login successful")
        else:
            st.error("Invalid password")
    st.stop()

# ---------------- PDF UPLOAD ----------------
st.subheader("📄 Upload Company PDF")

uploaded = st.file_uploader(
    "Upload company profile (PDF only)",
    type=["pdf"]
)

def build_faiss_index(pdf_path: str):
    # Ensure directories exist (CRITICAL FOR STREAMLIT CLOUD)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    os.makedirs(VECTOR_PATH, exist_ok=True)

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(VECTOR_PATH)

if uploaded:
    # Ensure data folder exists before saving PDF
    os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)

    with open(PDF_PATH, "wb") as f:
        f.write(uploaded.read())

    st.info("PDF uploaded. Building FAISS index…")

    with st.spinner("Processing document…"):
        build_faiss_index(PDF_PATH)

    st.success("✅ FAISS index built successfully!")

# ---------------- STATUS ----------------
st.subheader("📊 System Status")

faiss_ready = (
    os.path.exists(os.path.join(VECTOR_PATH, "index.faiss")) and
    os.path.exists(os.path.join(VECTOR_PATH, "index.pkl"))
)

st.write("FAISS Index:", "✅ Ready" if faiss_ready else "❌ Not available")
