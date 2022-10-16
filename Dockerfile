FROM alpine:latest

# Add Python and Pip, then use pip to install required Python packages
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install gitpython

# Add all required packages, this includes SQLite for extracting the
# database backups and git/OpenSSH for connecting authentication to
# the git repo. Additionally supercronic for scheduling cron jobs.
RUN apk add --update sqlite
RUN apk add --update git
RUN apk add --update openssh
RUN apk add --update tzdata
RUN apk add --update supercronic

# Local file for specifying the local timezone
ENV LOCALTIME_FILE="/tmp/localtime"

# Copy all of our local data for the application
RUN mkdir /app
COPY scripts/entrypoint.py app/entrypoint.py
COPY scripts/backup.py /app/backup.py
COPY scripts/include.py /app/include.py

# Create the required folders and a symlink for localtime to operate
RUN mkdir -m 777 /bitwarden_backup
RUN mkdir /root/.ssh
RUN ln -sf "${LOCALTIME_FILE}" /etc/localtime

# Execute our entrypoint script to begin the setup and cron monitoring
ENTRYPOINT ["python3", "/app/entrypoint.py"]
