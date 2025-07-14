import requests
import streamlit as st
from components.docs_upload import render_uploader
from components.chat_history import render_history_download
from components.chat_UI import render_chat
from config import API_URL


# Page Configuration
st.set_page_config(
    page_title="RAG-Powered PDF Chatbot 1.0",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App Title
st.title("🧠 RAG-Powered PDF Chatbot")
st.markdown("Chat with your PDFs using retrieval-augmented generation (RAG) powered by LLaMA 3 + Groq.")


# UI Components
render_uploader()           # PDF upload section
render_chat()               # Chat interface (input + response)
render_history_download()   # Chat history download/export section

try:
    requests.get(API_URL)
    st.success("✅ Backend online")
except:
    st.error("❌ Backend unavailable")
