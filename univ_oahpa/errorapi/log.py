import logging
import os

__all__ = [
    'ERROR_FST_LOG',
]

# Logging globals

ERROR_FST_FORMATTER = logging.Formatter('%(asctime)-15s - %(message)s')
ERROR_FST_LOG_FILE_PATH = os.path.join(os.getcwd(),
                                       'error_api_log.txt')

ERROR_FST_FILE = logging.FileHandler(ERROR_FST_LOG_FILE_PATH)
ERROR_FST_FILE.setFormatter(ERROR_FST_FORMATTER)
ERROR_FST_FILE.setLevel(logging.INFO)

ERROR_FST_LOG = logging.getLogger('morfa-s')
ERROR_FST_LOG.addHandler(ERROR_FST_FILE)


