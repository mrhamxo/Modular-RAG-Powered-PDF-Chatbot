import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(
    name: str = "RAG-POWERED-PDF-CHATBOT",
    level: int | str = logging.INFO,
    logfile: str | Path | None = None,
    max_bytes: int = 1_048_576,        # 1 MB
    backup_count: int = 3,
) -> logging.Logger:
    """
    Create (or retrieve) a logger with a sensible default format.
    
    Parameters
    ----------
    name : str
        Logger name.
    level : int | str
        Logging level (e.g. logging.DEBUG or "DEBUG").
    logfile : str | Path | None
        If provided, adds a rotating file handler.
    max_bytes : int
        Max size for each log file before rotation.
    backup_count : int
        Number of rotated log files to keep.
    """
    logger = logging.getLogger(name)

    # Convert string levels like "DEBUG" → numeric constant
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())
    logger.setLevel(level)

    # Ensure we don’t duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    fmt = "[%(asctime)s] [%(levelname)s] %(name)s ─ %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Optional rotating file handler
    if logfile:
        logfile = Path(logfile).expanduser().resolve()
        logfile.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            logfile, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Example usage
logger = setup_logger(level="DEBUG", logfile="logs/RAG-LOG.log")
logger.debug("Logger initialised")
