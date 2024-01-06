# Specifically using v3.18.5 as when I update to 3.19 the below breaks on the 
# "python3 -m ensurepip" command as it appears to now be executed from a venv.
# I tried upgrading this to using the python Docker container, however that
# has a problem of not being hable to obtain some of the required programs
# outside of Python to execute. So for now, using v3.18.5 until I get back
# around to updating this and determining a solution for the issue with ensurepip

FROM alpine:3.18.5

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
# RUN apk add --update supercronic
RUN apk add --update curl

# Latest releases available at https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.29/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=cd48d45c4b10f3f0bfdd3a57d054cd05ac96812b

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

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
