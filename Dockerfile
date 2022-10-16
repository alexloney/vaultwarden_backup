FROM alpine:latest

# Add Python/pip
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN pip3 install gitpython

# Add SQLite for exporting from the BitWarden SQLite database
RUN apk add --update sqlite

# Add git for communication with git repository
RUN apk add --update git

# Add SSH for git authentication
RUN apk add --update openssh

RUN apk add --update tzdata
RUN apk add --update supercronic

ENV LOCALTIME_FILE="/tmp/localtime"

RUN mkdir /app
COPY scripts/entrypoint.py app/entrypoint.py
COPY scripts/backup.py /app/backup.py
COPY scripts/include.py /app/include.py

RUN mkdir -m 777 /bitwarden_backup
RUN mkdir /root/.ssh
RUN ln -sf "${LOCALTIME_FILE}" /etc/localtime

# ENTRYPOINT ["python3", "/app/entrypoint.py"]
