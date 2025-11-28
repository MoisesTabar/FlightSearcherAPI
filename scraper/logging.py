import logging
import sys


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("Flight Scraper Logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%M:%S")
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()
