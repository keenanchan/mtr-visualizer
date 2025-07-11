FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y postgresql-client libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean

COPY extract_from_raw.sh .

ENTRYPOINT ["bash", "extract_from_raw.sh"]