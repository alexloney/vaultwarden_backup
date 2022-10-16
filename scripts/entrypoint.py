#!python3

import os
import sys
import logging

from include import *

def validate_tz(tz):
    logging.info('Validating provided timezone')
    if not os.path.exists('/usr/share/zoneinfo/' + tz):
        logging.error('Error: Unknown timezone provided (' + tz + ')')
        sys.exit(1)

def configure_timezone(tz, localtime_file):
    logging.info('Creating timezone symlink')
    os.system('ln -sf "/usr/share/zoneinfo/' + tz + '" "' + localtime_file + '"')

def configure_cron(cron, cron_config_file):
    logging.info('Setting up cron configuration')
    if os.path.exists(cron_config_file):
        logging.info('Removing existing crontab entry')
        os.system("sed -i '/backup.py/d' '" + cron_config_file + "'")
    with open(cron_config_file, 'a') as f:
        logging.info('Adding crontab entry')
        f.write(cron + ' python3 /app/backp.py\n')

def start_crontab(cron_config_file):
    logging.info('Executing cron process')
    os.system('supercronic -passthrough-logs -quiet "' + cron_config_file + '"')
    pass

def load_github_host():
    logging.info('Loading github host')
    if not os.path.exists('/root/.ssh'):
        logging.info('Creating SSH directroy')
        os.mkdir('/root/.ssh')
    os.system('ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts')


def init():
    LOG_LEVEL = get_env('LOG_LEVEL', 'info')
    configure_logging(LOG_LEVEL)

    logging.info('Beginning initialization process')
    LOCALTIME_FILE = get_env('LOCALTIME_FILE', '/etc/localtime')
    TZ = get_env('TZ', 'UTC')
    HOME = get_env('HOME', '/root')
    CRON = get_env('CRON', '5 * * * *')

    CRON_CONFIG_FILE = HOME + '/crontabs'

    validate_tz(TZ)

    configure_timezone(TZ, LOCALTIME_FILE)
    configure_cron(CRON, CRON_CONFIG_FILE)

    load_github_host()

    start_crontab(CRON_CONFIG_FILE)

if __name__ == '__main__':
    init()
