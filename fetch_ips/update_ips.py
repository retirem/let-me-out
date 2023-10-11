import logging
import mypy
import sys

from shutil import which
from datetime import datetime

# Check if update-ipsets is installed
def tool_not_exists(name: str) -> bool:
    return which(name) is None

def logging_time() -> str:
    return datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def configure_logging() -> None:
    handlers = [logging.FileHandler(filename='fetch_ips.log'), logging.StreamHandler(stream=sys.stdout)]
    logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG, handlers=handlers)

if __name__ == "__main__":
    configure_logging()

    if tool_not_exists('update-ipsets'):
        logging.error(logging_time() + " update-ipset command is not available in the $PATH.")
        sys.exit(1)
