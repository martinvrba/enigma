import logging
import sys

logger = logging.getLogger(__name__)


def log_error_and_exit(error_message: str):
    logger.error(error_message)
    sys.exit(1)
