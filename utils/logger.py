from loguru import logger
import os

def setup_logger():
    log_file = os.path.join("logs", "test_execution.log")

    logger.add(log_file,
               rotation="10 MB",
               level="INFO",
               format="{time} {level} {message}")

    return logger

test_logger = setup_logger()