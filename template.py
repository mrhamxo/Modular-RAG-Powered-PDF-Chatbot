import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_of_files = [
    "frontend/components/chat_UI.py",
    "frontend/components/chat_history.py",
    "frontend/components/docs_upload.py",
    "frontend/utils/api.py",
    "frontend/app.py",
    "frontend/config.py",
    "backend/modules/vectorestore.py",
    "backend/modules/llm.py",
    "backend/modules/pdf_handler.py",
    "backend/modules/query_handlers.py",
    "backend/logger.py",
    "backend/main.py",
    "pdf_documents/"
    ".env",
    "requirements.txt",
    "setup.py", 
    "research/trials.ipynb"
]

for file_path in list_of_files:
    file_path = Path(file_path)
    
    file_dir = file_path.parent
    if not file_dir.exists():
        logging.info(f"Creating directory: {file_dir}")
        os.makedirs(file_dir, exist_ok=True)
    
    if not file_path.exists():
        logging.info(f"Creating file: {file_path}")
        with open(file_path, 'w') as f:
            pass  # Create an empty file
    else:
        logging.info(f"File already exists: {file_path}")