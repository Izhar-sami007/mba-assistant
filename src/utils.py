import time
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
logger = logging.getLogger("mba-bot")

@contextmanager
def timer(name: str):
    t0 = time.time()
    yield
    logging.info(f"{name} took {time.time()-t0:.2f}s")
