import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "agno-cookcook", log_dir: str = "logs") -> logging.Logger:
    Path(log_dir).mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    file_handler = logging.FileHandler(
        os.path.join(log_dir, f"{today}.log"),
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    
    error_handler = logging.FileHandler(
        os.path.join(log_dir, f"{today}_error.log"),
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = "agno-cookcook") -> logging.Logger:
    return logging.getLogger(name)
