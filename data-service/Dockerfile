FROM python:3.11-slim

WORKDIR /app

# Set up dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y postgresql-client libpq-dev gcc cron && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean

# Set up cronjob to truncate train_eta_raw every two hours
COPY clear_eta_raw_table.sh .
COPY cronjob /etc/cron.d/clear_eta_raw_table

# Set permissions, run
RUN chmod 0644 /etc/cron.d/clear_eta_raw_table && \
    crontab /etc/cron.d/clear_eta_raw_table

# Create logfile
RUN touch /var/log/cron.log

# Run cron in background
CMD cron -f

# Copy entrypoint script
COPY extract_from_raw.sh .

# Run data processing loop
ENTRYPOINT ["bash", "extract_from_raw.sh"]