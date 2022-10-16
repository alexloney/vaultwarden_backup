#!python3

import os
import sys
import logging

def get_env(name, default=None):
    logging.info('Fetching ENV: ' + name)
    if name in os.environ:
        return os.environ[name]

    if default is not None:
        return default

    logging.error('Error: Missing required environment variable ' + name)
    sys.exit(1)


def configure_logging(log_level):
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    if log_level == 'debug':
        root.setLevel(level=logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    elif log_level == 'info':
        root.setLevel(level=logging.INFO)
        handler.setLevel(logging.INFO)
    elif log_level == 'warning':
        root.setLevel(level=logging.WARNING)
        handler.setLevel(logging.WARNING)
    elif log_level == 'error':
        root.setLevel(level=logging.ERROR)
        handler.setLevel(logging.ERROR)
    elif log_level == 'critical':
        root.setLevel(level=logging.CRITICAL)
        handler.setLevel(logging.CRITICAL)
    else:
        print('Unknown log level, defaulting to INFO')
        root.setLevel(level=logging.INFO)
        handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


