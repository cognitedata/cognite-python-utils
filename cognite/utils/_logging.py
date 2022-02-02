import logging

# Define default logger
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
