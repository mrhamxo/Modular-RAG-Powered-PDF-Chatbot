from fastapi import UploadFile
from pathlib import Path
from datetime import datetime
import shutil

# Folder where PDFs will live
UPLOAD_DIR = Path("uploaded_pdf")
UPLOAD_DIR.mkdir(exist_ok=True)  # create once at import time


def save_uploaded_files(files: list[UploadFile]) -> list[str]:
    
    """
    Persist uploaded files to disk.

    Parameters
    ----------
    files : list[UploadFile]
        Files received from FastAPI endpoint.

    Returns
    -------
    list[str]
        Absolute paths to the saved files (as strings, for easy JSON).
    """
    
    saved_paths: list[Path] = []

    for uf in files:
        # Create a safe, timestamped filename to avoid collisions
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        safe_name = f"{timestamp}_{Path(uf.filename).name}"
        dest = UPLOAD_DIR / safe_name

        # Stream copy to disk
        with dest.open("wb") as out_file:
            shutil.copyfileobj(uf.file, out_file)

        saved_paths.append(dest.resolve())

    # Return as str for easier downstream JSON usage
    return [str(p) for p in saved_paths]
