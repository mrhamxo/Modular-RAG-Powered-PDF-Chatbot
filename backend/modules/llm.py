import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Environment                                                                 #
load_dotenv()                                   # Load variables from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")        # Expect your Groq key here
if not GROQ_API_KEY:                            # Fail fast if missing
    raise EnvironmentError(
        "GROQ_API_KEY not found—add it to your .env file."
    )

# Prompt template                                                              #
PROMPT_TEMPLATE = """
                    You are **ChatBot**, an AI‑powered assistant trained to help users understand
                    information in **any documents**—research papers, reports, manuals, medical
                    records, and more—and to answer related health‑ or general‑knowledge questions.

                    Your job is to provide clear, accurate, and helpful responses based **only on
                    the provided context**.

                    ---

                    🔍 **Context**:
                    {context}

                    🙋‍♂️ **User Question**:
                    {question}

                    ---

                    💬 **Answer**:
                    - Respond in a calm, factual, and respectful tone.
                    - Use simple explanations where helpful.
                    - If the context does not contain the answer, say:
                    "I'm sorry, but I couldn't find relevant information in the provided documents."
                    - **Do NOT** invent facts.
                    - **Do NOT** give medical advice or diagnoses.
                    """

# Factory function                                                             #
def build_qa_chain(vectorstore):
    """
    Build and return a Retrieval‑Augmented‑Generation QA chain.

    Parameters
    ----------
    vectorstore : langchain.vectorstores.base.VectorStore
        Your pre‑populated VectorStore (e.g., Chroma).

    Returns
    -------
    RetrievalQA
        Chain ready to answer questions:
        result = chain({"query": "your question"})["result"]
    """

    # 1. Large Language Model (Groq‑hosted LLaMA‑3)
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama3-70b-8192",      # Change if you prefer a smaller model
        temperature=0.7,              # Adjust creativity / determinism
    )

    # 2. Prompt wrapper
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    # 3. Retriever from the provided VectorStore
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # 4. Assemble RetrievalQA chain (LangChain helper)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",           # Basic “stuff” chain (prompt + context)
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True, # Include doc chunks in output for traceability
    )
