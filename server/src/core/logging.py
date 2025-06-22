import os
from loguru import logger

from src.core.config import settings

log_file = os.path.join(settings.LOG_DIR_PATH, 'app.log')

logger.add(
    sink=log_file,
    level=settings.LOG_LEVEL,
    enqueue=True,
    colorize=True,
    rotation='500 MB'
)
