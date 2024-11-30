FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data
RUN mkdir -p /var/log

# Set the entrypoint to execute scrape.py directly
CMD ["python", "/app/scrape.py"]