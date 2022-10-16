# Vaultwarden Backup
This is a simple script to autoamte the process defined in the [Vaultwarden wiki](https://github.com/dani-garcia/vaultwarden/wiki), specifically the (somewhat hidden) [Backing up your vault](https://github.com/dani-garcia/vaultwarden/wiki/Backing-up-your-vault) wiki page. The main reason I wanted this was to provide an external backup through a git repository, which would allow version control of backups.

This is a pretty simple Docker container, it provides a way to spin up a container that will run on a cron schedule, and on the specified schedule it will export the Vaultwarden data and send the backup to the specified git repository. You must specify your SSH key for use with the container.

## Usage
Here are some example snippets to help you get started creating a container.

### docker cli
```bash
docker pull ghcr.io/alexloney/vaultwarden_backup:latest
docker run -d --name vaultwarden_backup \
    -v /vw-data/:/data/ \
    -v /path/to/id_rsa:/root/.ssh/id_rsa \
    -e CRON='5 * * * *' \
    -e GIT_REPOSITORY_URL='GIT_REPO' \
    -e TZ='America/Los_Angeles' \
    -e LOG_LEVEL=info \
    ghcr.io/alexloney/vaultwarden_backup:latest
```

## Parameters
Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-v /vw-data/:/data/` would map the folder `/vw-data/` on the host machine into the directory `/data/` in the Docker image.
| Parameter | Function |
| --------- | -------- |
| `-v /data/` | Location of the Vaultwarden data directory |
| `-v /root/.ssh/id_rsa` | The RSA key used for SSH authentication to git |
| `-e CRON='5 * * * *'` | The cron schedule to run backups on |
| `-e GIT_REPOSITORY_URL='<GIT_REPO>'` | The git repository to use, in the form `git@...` |
| `-e TZ=UTC` | The timezone to utilize, important for the cron schedule to be accurate. [See here for valid values](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). |
| `-e LOG_LEVEL=info` | Indicates the level of log verbosity to use. Values are: debug, info, warning, error, and critical |

