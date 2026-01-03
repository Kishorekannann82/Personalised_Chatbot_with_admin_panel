import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
PDF_PATH = "data/company.pdf"
VECTOR_PATH = "data/faiss_index"

st.set_page_config(page_title="Admin • Company Chatbot", page_icon="🔐")
st.title("🔐 Admin Panel")

# -------- Auth --------
if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False

if not st.session_state.admin_auth:
    pwd = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.success("Logged in")
        else:
            st.error("Invalid password")
    st.stop()

# -------- Upload --------
st.subheader("📄 Upload / Replace Company PDF")
uploaded = st.file_uploader("Upload company profile (PDF)", type=["pdf"])

def build_index(pdf_path: str):
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    os.makedirs(VECTOR_PATH, exist_ok=True)

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vs = FAISS.from_documents(docs, embeddings)
    vs.save_local(VECTOR_PATH)

if uploaded:
    with open(PDF_PATH, "wb") as f:
        f.write(uploaded.read())
    st.info("PDF saved. Building index…")

    with st.spinner("Building FAISS index…"):
        build_index(PDF_PATH)

    st.success("Index built successfully!")

# -------- Status --------
st.subheader("📊 Status")
idx_faiss = os.path.exists(os.path.join(VECTOR_PATH, "index.faiss"))
idx_pkl = os.path.exists(os.path.join(VECTOR_PATH, "index.pkl"))

st.write("FAISS index:", "✅ Ready" if idx_faiss and idx_pkl else "❌ Not built yet")
