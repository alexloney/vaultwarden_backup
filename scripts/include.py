#!python3

import os
import sys
import logging

# Given an environment variable and default value, fetch the variable from the environment
# if it exists. If it does not exist, return the default value. If no default value is
# define, then return an error. This allows us to have a default value when possible, or if
# not possible, give an error.
def get_env(name, default=None):
    logging.info('Fetching ENV: ' + name)
    if name in os.environ:
        return os.environ[name]

    if default is not None:
        return default

    logging.error('Error: Missing required environment variable ' + name)
    sys.exit(1)

# Set the logging level to be used based on a user input, allowing for consistent logging
# from any of the scripts utilized.
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

