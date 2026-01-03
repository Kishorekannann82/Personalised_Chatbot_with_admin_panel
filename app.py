import streamlit as st
import os
from chatbot import get_chatbot

st.set_page_config(
    page_title="Company AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Company AI Assistant")
st.caption("Answers are based only on our company profile")

INDEX_READY = (
    os.path.exists("data/faiss_index/index.faiss") and
    os.path.exists("data/faiss_index/index.pkl")
)

if not INDEX_READY:
    st.warning("Our chatbot is getting ready. Please check back soon.")
    st.stop()

qa = get_chatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about our company…")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = qa.run(user_input)
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
