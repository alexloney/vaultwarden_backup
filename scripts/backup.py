#!python3

import os
import sys
import git
import logging
import tempfile
import shutil
from git import Repo
from git import Git
from datetime import datetime

from include import *

# Check to see if the repository is set up, this is done by first ensuring that the
# required backup path folder exists, and if not creating it. Then it checks to see
# if the backup folder contains a git repository and returns either True or False
# based on if a repository exists
def is_repo_setup(backup_path):
    logging.info("Checking to see if " + backup_path + " exists")
    if not os.path.exists(backup_path):
        logging.info("The path " + backup_path + " does not exist, creating it.")
        os.mkdir(backup_path)

    try:
        _ = git.Repo(backup_path).git_dir
        logging.info("The backup directory contains a GIT repository")
        return True
    except git.exc.InvalidGitRepositoryError:
        logging.info("The backup directory does not contain a GIT repository")
        return False

# Clone the specified repository into the backup path
def setup_repo(git_repository_url, backup_path):
    logging.info("Checking out " + git_repository_url + " into " + backup_path)
    Repo.clone_from(git_repository_url, backup_path)

# Remove all file contents except for the ".git" folder in a given directory. This
# is done to allow us to have a fresh commit each time, removing/adding any files
# that need to be removed/added. Since the git repo inheritly records each commit,
# there's not a reason to maintain a history within the file structure, instead we
# can just use the inherit property of a git repo to keep track of the history.
#
# To keep it a valid .git repository and avoiding having to checkout the repo every
# time we run, this will ignore the .git folder.
def cleanup_repo_contents(backup_path):
    logging.info("Cleaning " + backup_path)

    tmpdir = tempfile.mkdtemp()
    logging.info("Created temporary directory: " + tmpdir)

    logging.info("Removing all contents from " + backup_path)
    for filename in os.listdir(backup_path):
        file_path = os.path.join(backup_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path) and file_path != backup_path + '/.git':
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error('Failed to delete %s. Reason: %s' % (file_path, e))
            sys.exit(1)

# Backup the SQLite database by using the `.backup` command
def backup_sqlite(backup_path):
    logging.info("Backing up SQLite database")
    os.system("sqlite3 /data/db.sqlite3 \".backup '" + backup_path + "/db.sqlite3'\"")

# Backup the "Attachments" directory contents
def backup_attachments(backup_path):
    logging.info("Backing up /data/attachments")
    if os.path.exists('/data/attachments'):
        shutil.copytree('/data/attachments', backup_path + '/attachments')

# Backup the "Sends" directory contents
def backup_sends(backup_path):
    logging.info("Backing up /data/sends")
    if os.path.exists('/data/sends'):
        shutil.copytree('/data/sends', backup_path + '/sends')

# Backup the "config.json" file
def backup_config(backup_path):
    logging.info('Backing up /data/config.json')
    if os.path.exists('/data/config.json'):
        shutil.copyfile('/data/config.json', backup_path + '/config.json')

# Backup the RSA keys
def backup_rsa_keys(backup_path):
    if os.path.exists('/data/rsa_key.pem'):
        logging.info('Backing up /data/rsa_key.pem')
        shutil.copyfile('/data/rsa_key.pem', backup_path + '/rsa_key.pem')
    if os.path.exists('/data/rsa_key.pub.pem'):
        logging.info('Backing up /data/rsa_key.pub.pem')
        shutil.copyfile('/data/rsa_key.pub.pem', backup_path + '/rsa_key.pub.pem')

# Add all changes to the repository, add a comment indicating the time, and
# commit/push these changes.
def add_commit_and_push(backup_path):
    logging.info('Adding commit and pushing repo')
    today = datetime.now()
    datestr = today.strftime("%Y/%m/%d - %H:%M")

    repo = Repo(backup_path)
    repo.git.add(all=True)
    if repo.index.diff("HEAD"):
        repo.index.commit('Automated backup on ' + datestr)
        origin = repo.remote(name='origin')
        origin.push()
        logging.info('Changes pushed')
    else:
        logging.info('No changes detected')

if __name__ == '__main__':
    LOG_LEVEL = get_env('LOG_LEVEL', 'info')
    configure_logging(LOG_LEVEL)

    logging.info("Obtaining environment variables")

    GIT_REPOSITORY_URL = get_env('GIT_REPOSITORY_URL')
    logging.info("GIT_REPOSITORY_URL=" + GIT_REPOSITORY_URL)

    BACKUP_PATH = get_env('BACKUP_PATH', '/bitwarden_backup')
    logging.info("BACKUP_PATH=" + BACKUP_PATH)

    if not is_repo_setup(BACKUP_PATH):
        setup_repo(GIT_REPOSITORY_URL, BACKUP_PATH)

    cleanup_repo_contents(BACKUP_PATH)

    backup_sqlite(BACKUP_PATH)
    backup_attachments(BACKUP_PATH)
    backup_sends(BACKUP_PATH)
    backup_config(BACKUP_PATH)
    backup_rsa_keys(BACKUP_PATH)

    add_commit_and_push(BACKUP_PATH)
