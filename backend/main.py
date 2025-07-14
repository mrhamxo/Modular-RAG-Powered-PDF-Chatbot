from typing import List
from pathlib import Path
import os

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


from modules.vectorestore import load_vectorstore, PERSIST_DIR
from modules.llm import build_qa_chain
from modules.query_handlers import query_chain

from logger import logger

# FastAPI App & CORS                                                           #
app = FastAPI(title="Modular RAG‑Powered PDF Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception catcher (so you always get JSON)                            
@app.middleware("http")
async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500, content={"error": str(exc)})

# PDF Upload Endpoint                                                          
@app.post("/upload_pdfs/")
async def upload_pdf(files: List[UploadFile] = File(...)):
    """
    Save uploaded PDFs and update / create the Chroma vector store.
    """
    try:
        logger.info(f"Received {len(files)} file(s) to upload.")
        load_vectorstore(files)
        logger.info("Documents added to Chroma successfully.")
        return {"message": "Files processed and vector store updated."}
    except Exception as exc:
        logger.exception("Error during PDF upload.")
        return JSONResponse(status_code=500, content={"error": str(exc)})

# Question‑Answer Endpoint                                                     
@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    """
    Run Retrieval‑QA over the persisted vector store.

    Request must be form‑encoded:
        POST body: question=<your question>
    """
    try:
        logger.info(f"User query: {question}")

        # 1. Reload vector store from disk
        vectorstore = Chroma(
            persist_directory=str(PERSIST_DIR),
            embedding_function=HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L12-v2"
            ),
        )

        # 2. Build QA chain and run
        chain = build_qa_chain(vectorstore)
        result = query_chain(chain, question)

        logger.info("Query processed successfully.")
        return result

    except Exception as exc:
        logger.exception("Error processing question.")
        return JSONResponse(status_code=500, content={"error": str(exc)})

# Health‑check                                                                 #
@app.get("/")
async def home():
    return {"message": "Welcome to home"}
