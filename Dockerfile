FROM python:3.9-slim-bullseye

RUN python3 -m venv /opt/venv

COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

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
CMD . /opt/venv/bin/activate && exec python /app/entrypoint.py
