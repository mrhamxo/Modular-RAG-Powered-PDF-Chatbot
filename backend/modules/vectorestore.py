import os
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
#from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Configuration                                                               
PERSIST_DIR = Path("chroma_store")
UPLOAD_DIR  = Path("uploaded_pdf")
UPLOAD_DIR.mkdir(exist_ok=True)           # Ensure folder exists

# Main helper                                                                  #
def load_vectorstore(uploaded_files: List):
    
    """
    Save uploaded PDF(s) → create/update Chroma vector store → return store.

    Parameters
    ----------
    uploaded_files : list of st.uploaded_file (or any .file/.filename objects)

    Returns
    -------
    Chroma
        Ready-for‑RAG VectorStore.
    """
    
    # 1. Persist uploads to disk and collect their paths
    pdf_paths = []
    for file in uploaded_files:
        save_path = UPLOAD_DIR / file.filename
        save_path.write_bytes(file.file.read())
        pdf_paths.append(save_path)

    # 2. Load & split PDFs into text chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = []
    for path in pdf_paths:
        docs.extend(PyPDFLoader(str(path)).load())
    chunks = splitter.split_documents(docs)

    # 3. Embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

    # 4. Create or update persistent Chroma store
    if PERSIST_DIR.exists() and any(PERSIST_DIR.iterdir()):
        # Store already exists → append
        vectorstore = Chroma(persist_directory=str(PERSIST_DIR), embedding_function=embeddings)
        vectorstore.add_documents(chunks)
    else:
        # First‑time build
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(PERSIST_DIR),
        )

    vectorstore.persist()  # flush to disk
    return vectorstore
