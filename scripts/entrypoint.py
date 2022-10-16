#!python3

import os
import sys
import logging

from include import *

# Check to see if the user-supplied timezone is a valid timezone, the valid timezones
# are obtained from the `tzdata` package. 
def validate_tz(tz):
    logging.info('Validating provided timezone')
    if not os.path.exists('/usr/share/zoneinfo/' + tz):
        logging.error('Error: Unknown timezone provided (' + tz + ')')
        sys.exit(1)

# Create a symbolic link between the timezone and our locally specified timezone file
def configure_timezone(tz, localtime_file):
    logging.info('Creating timezone symlink')
    os.symlink('/usr/share/zoneinfo/' + tz, localtime_file)

# If the file exists, check for and remove the entry to execute our `backup.py` script.
# Then add a new entry for our `backup.py` script. This is to allow the environment
# variable `CRON` to be updated and will refresh the job schedule.
def configure_cron(cron, cron_config_file):
    logging.info('Setting up cron configuration')
    if os.path.exists(cron_config_file):
        logging.info('Removing existing crontab entry')
        os.system("sed -i '/backup.py/d' '" + cron_config_file + "'")
    with open(cron_config_file, 'a') as f:
        logging.info('Adding crontab entry')
        f.write(cron + ' python3 /app/backp.py\n')

# Execute the `supercronic` command. This will allow the Docker container to remain
# open and operational, allowing it to follow the predefined cron schedule.
def start_crontab(cron_config_file):
    logging.info('Executing cron process')
    os.system('supercronic -passthrough-logs -quiet "' + cron_config_file + '"')
    pass

# When attempting to perform SSH authentication to github, the authorization would
# fail because our local system does not recognize githubs public key. This will
# pull the github public key and store it in our known_hosts file.
#
# NOTE: This will cause a new entry to be created in the `known_hosts` file each
#       run. At the moment I don't see a problem with this other than the just
#       slightly less-than-clean addition. If I ever notice an issue, I'll take
#       a look at preventing it from adding duplicates.
def load_github_host():
    logging.info('Loading github host')
    if not os.path.exists('/root/.ssh'):
        logging.info('Creating SSH directroy')
        os.mkdir('/root/.ssh')
    os.system('ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts')

# Initializetion function to allow initial setup/configuration sequence.
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
