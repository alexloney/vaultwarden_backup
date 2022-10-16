# Vaultwarden Backup
This is a simple script to autoamte the process defined in the [Vaultwarden wiki](https://github.com/dani-garcia/vaultwarden/wiki), specifically the (somewhat hidden) [Backing up your vault](https://github.com/dani-garcia/vaultwarden/wiki/Backing-up-your-vault) wiki page. The main reason I wanted this was to provide an external backup through a git repository, which would allow version control of backups.

This is a pretty simple Docker container, it provides a way to spin up a container that will run on a cron schedule, and on the specified schedule it will export the Vaultwarden data and send the backup to the specified git repository. You must specify your SSH key for use with the container.

## Usage
```bash
docker pull ghcr.io/alexloney/vaultwarden_backup:latest
docker run -d --name vaultwarden_backup \
    -v /vw-data/:/data/ \
    -v /path/to/id_rsa:/root/.ssh/id_rsa \
    -e CRON='5 * * * *' \
    -e GIT_REPOSITORY_URL='GIT_REPO' \
    alexloney/vaultwarden_backup:latest
```
