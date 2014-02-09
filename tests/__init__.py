import logging

logger = logging.getLogger("fondz")
handler = logging.FileHandler(filename="test.log")
formatter = logging.Formatter('%(asctime)-15s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

