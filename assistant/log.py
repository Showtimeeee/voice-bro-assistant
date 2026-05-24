import os
import logging
from .config import BASE_DIR
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, '.env'))

_LOG_FILE = os.path.join(BASE_DIR, os.getenv('LOG_FILE', 'app.log'))
_LOG_LEVEL = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper(), logging.INFO)


def setup_logging():
    logging.basicConfig(
        level=_LOG_LEVEL,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(_LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


logger = logging.getLogger('assistant')
