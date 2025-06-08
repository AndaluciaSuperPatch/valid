import logging
from typing import Optional
import sys

def setup_logger(name: str, log_level: str = 'INFO', 
                log_file: Optional[str] = None) -> logging.Logger:
    """Configura un logger con salida a consola y archivo opcional"""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo si se especifica
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
