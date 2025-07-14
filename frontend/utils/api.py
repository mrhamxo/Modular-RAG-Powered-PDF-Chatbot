import requests
from config import API_URL


def upload_pdfs_api(files):
    """
    Send one or more PDF files to the FastAPI backend for processing.
    
    Parameters:
        files (list): List of file-like objects from Streamlit or other input
    
    Returns:
        requests.Response: The HTTP response from the backend
    """
    # Prepare multipart/form-data payload
    files_payload = [
        ("files", (f.name, f.read(), "application/pdf")) for f in files
    ]
    # <- fixed endpoint
    return requests.post(f"{API_URL}/upload_pdfs/", files=files_payload)


def ask_question(question: str):
    """
    Send a user's question to the backend and receive an answer.

    Parameters:
        question (str): The natural language query from the user

    Returns:
        requests.Response: The HTTP response from the backend
    """
    payload = {"question": question}
    response = requests.post(f"{API_URL}/ask/", data=payload)
    return response
