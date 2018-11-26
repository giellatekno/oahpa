# -*- coding: utf-8 -*-
from local_conf import LLL1

import logging
import os
import sys

__all__ = [
    'MORFAS_LOG',
    'MORFAS_LOG_FILE_PATH',
    'DEV_LOG',
    'initialize_loggers',
]

global _logging_initialized
_logging_initialized = False

def initialize_loggers():

    global MORFAS_LOG
    global MORFAS_LOG_FILE_PATH
    global _logging_initialized

    if not _logging_initialized:
        MORFAS_FORMATTER = logging.Formatter('%(asctime)-15s - %(message)s')
        MORFAS_LOG_FILE_PATH = os.path.join(os.getcwd(),
                                            LLL1+'_oahpa/drill/morfas_log.txt')

        SCRATCH_LOG_PATH = os.path.join(os.getcwd(),
                                            'dev_log.txt')

        MORFAS_FILE = logging.FileHandler(MORFAS_LOG_FILE_PATH)
        MORFAS_FILE.setFormatter(MORFAS_FORMATTER)
        MORFAS_FILE.setLevel(logging.INFO)

        DEV_LOG_FILE = logging.FileHandler(SCRATCH_LOG_PATH)
        DEV_LOG_FILE.setLevel(logging.INFO)

        MORFAS_LOG = logging.getLogger('morfa-s')
        MORFAS_LOG.addHandler(MORFAS_FILE)

        DEV_LOG = logging.getLogger('dev_log')
        DEV_LOG.addHandler(DEV_LOG_FILE)

        _logging_initialized = True
        print >> sys.stderr, "Loggers initialized."
