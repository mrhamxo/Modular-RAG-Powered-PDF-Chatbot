from logger import logger


def query_chain(chain, user_input: str) -> dict:
    """
    Run a LangChain RetrievalQA chain with the user's input query.

    Parameters
    ----------
    chain : RetrievalQA
        A chain object created by build_qa_chain().
    user_input : str
        The user's question/query.

    Returns
    -------
    dict
        A dictionary with:
        - "response": the generated answer from the LLM
        - "sources": list of document sources that supported the answer
    """
    try:
        logger.debug(f"Running chain for input: {user_input}")

        # Run the chain on the user query
        result = chain.invoke({"query": user_input})
        
        # Extract answer and source documents with page numbers
        sources = [
            f"{doc.metadata.get('source', '')} Page={doc.metadata.get('page', 0) + 1}"
            for doc in result.get("source_documents", [])
        ]

        # Extract answer and source document metadata
        response = {
            "response": result["result"],
            "sources": list(set(sources)),  # remove duplicates
        }

        logger.debug(f"Chain response: {response}")
        return response

    except Exception as e:
        logger.exception("Error in query_chain")
        raise  # re-raise the error for FastAPI or Streamlit to handle
