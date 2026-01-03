import streamlit as st
import os
from chatbot import get_chatbot

st.set_page_config(page_title="Company AI Assistant", page_icon="🤖")
st.title("🤖 Company AI Assistant")
st.caption("Answers are based only on our company profile")

INDEX_OK = (
    os.path.exists("data/faiss_index/index.faiss")
    and os.path.exists("data/faiss_index/index.pkl")
)

if not INDEX_OK:
    st.warning("Our chatbot is getting ready. Please check back soon.")
    st.stop()

qa = get_chatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

q = st.chat_input("Ask about our company…")
if q:
    st.session_state.messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.markdown(q)

    with st.chat_message("assistant"):
        ans = qa.run(q)
        st.markdown(ans)

    st.session_state.messages.append({"role": "assistant", "content": ans})
