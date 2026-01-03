# 🤖 Company AI Chatbot (RAG-Based)

An **AI-powered personalized chatbot** built using **Python, Streamlit, LangChain, FAISS, and Groq LLM**, designed to answer questions **only from a company’s internal PDF documents**.

This system allows:
- 🔐 **Admin-only document upload**
- 🤖 **Public users to chat via website**
- 📄 **Accurate, hallucination-free answers using RAG**
- 🌐 **Easy embedding into any website**

---

## 🚀 Features

### 🔹 Public Chatbot
- Answers questions based **only on company profile PDF**
- Clean chat UI
- No login required
- Website-embeddable (iframe)

### 🔹 Admin Panel (Private)
- Password-protected admin access
- Upload / replace company PDF
- Automatically rebuilds FAISS vector index
- No manual scripts needed

### 🔹 AI Capabilities
- Retrieval-Augmented Generation (RAG)
- Semantic search using embeddings
- Fast inference using Groq LLM
- No hallucinations

---

## 🧠 Architecture Overview

Admin Uploads PDF
↓
Text Splitting
↓
Embeddings (Sentence-Transformers)
↓
FAISS Vector Store
↓
Retriever
↓
Groq LLM
↓
User Answer

yaml
Copy code

---

## 🧰 Tech Stack

| Layer | Technology |
|-----|-----------|
| Frontend | Streamlit |
| Backend | Python |
| LLM | Groq (Free) |
| RAG Framework | LangChain |
| Vector DB | FAISS |
| Embeddings | Sentence-Transformers |
| Hosting | Streamlit Cloud |
| Auth | Environment-based Admin Password |

---

## 📂 Project Structure

Chat/
├── app.py # Public chatbot
├── admin.py # Admin panel
├── chatbot.py # RAG logic
├── ingest.py # PDF ingestion (used internally)
├── requirements.txt
├── README.md
├── .env # Local only (not pushed)
└── data/
├── company.pdf
└── faiss_index/

yaml
Copy code

---

## 🔐 Environment Variables

Create a `.env` file locally:

```env
GROQ_API_KEY=your_groq_api_key
ADMIN_PASSWORD=your_admin_password
⚠️ Never push .env to GitHub.

▶️ How to Run Locally
1️⃣ Create & Activate Environment
bash
Copy code
conda create -n chat python=3.11 -y
conda activate chat
2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Run Public Chatbot
bash
Copy code
streamlit run app.py
4️⃣ Run Admin Panel
bash
Copy code
streamlit run admin.py
🌐 Deploy on Streamlit Cloud (Free)
Push this repo to GitHub

Go to https://streamlit.io/cloud

Create new app → select app.py

Add secrets:

toml
Copy code
GROQ_API_KEY = "your_groq_api_key"
ADMIN_PASSWORD = "your_admin_password"
🌍 Website Integration
Embed the chatbot into any website:

html
Copy code
<iframe
  src="https://your-app-name.streamlit.app"
  width="100%"
  height="600"
  style="border:none;border-radius:12px;">
</iframe>
🔒 Security Notes
Admin panel is private

No document access for users

API keys stored securely

RAG prevents hallucinations

🧪 Use Cases
Company profile chatbot

HR policy assistant

College / institution chatbot

Product documentation assistant

Internal knowledge base

📈 Future Enhancements
Multiple document support

Role-based access

Analytics dashboard

Chat history export

Multi-language support

👤 Author
Kishore Kannan N
AI / ML Engineer
🎥 YouTube: Kishorelytics
💻 GitHub: https://github.com/Kishorekannann82