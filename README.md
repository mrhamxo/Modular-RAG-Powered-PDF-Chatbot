# 🧠 Modular RAG-Powered PDF Chatbot

A production-ready, modular Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **Streamlit**, **ChromaDB**, and **LLaMA3 via Groq**. This AI-powered chatbot allows users to upload one or more PDF documents and ask natural language questions based on their content — ideal for querying research papers, reports, manuals, and more.

## ⚙️ Features

- 🔍 RAG-based document understanding using LLaMA3 + Groq API
- 📄 Multi-PDF upload and processing
- 🧠 Vector store powered by ChromaDB and HuggingFace embeddings
- 🖥️ Real-time web UI with Streamlit
- 🔧 Backend powered by FastAPI
- 🧩 Modular code structure for easy extension
- 🔐 Environment-secured API keys with `.env`
- 📥 Downloadable chat history
- 🌐 CORS-enabled for cross-platform integration

## 📁 Project Structure

```

Modular-RAG-Powered-PDF-Chatbot/
├── backend/
│   ├── main.py                # FastAPI app
│   ├── modules/
│   │   ├── vectorestore.py    # Embedding & ChromaDB logic
│   │   ├── llm.py             # Prompt + LLaMA3 chain
│   │   ├── query_handlers.py  # LLM execution
│   │   ├── pdf_handler.py     # Uploading docs files
│   └── logger.py              # Custom logging
├── frontend/
│   ├── app.py                 # Streamlit UI entrypoint
│   ├── components/            # UI sections
│   │   ├── chat_history.py    # show and download chat history  
│   │   ├── chat_UI.py         # user chat interface
│   │   ├── docs_upload.py     # docs uploading inputs
│   ├── utils/                 # API connector
│   │   ├── api.py            
│   ├── config.py              # API connector
├── uploaded_pdf/              # Uploaded PDFs
├── chroma_store/              # Persistent vector store
├── .env                       # API key config
└── requirements.txt           # All dependencies

````
## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Modular-RAG-Powered-PDF-Chatbot.git
cd Modular-RAG-Powered-PDF-Chatbot
````

### 2. Create Virtual Environments

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file inside the `backend/` folder:

```
GROQ_API_KEY=your_groq_api_key
```

## ▶️ Run the Application

### 1. Start FastAPI Backend

```bash
cd backend
uvicorn main:app --reload
```

### 2. Launch Streamlit Frontend

```bash
cd ../frontend
streamlit run app.py
```

## 📸 App Demo

<img width="1334" height="588" alt="Image" src="https://github.com/user-attachments/assets/8ebe6c12-f0e2-48c4-a3c5-79d1cb725063" />

## 🧠 Powered By

* [LangChain](https://python.langchain.com/)
* [ChromaDB](https://www.trychroma.com/)
* [Groq LLaMA3 API](https://console.groq.com/)
* [Streamlit](https://streamlit.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [HuggingFace Embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)

## 📄 License

This project is open-source and available under the MIT License.