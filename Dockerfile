FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data

RUN echo "0 * * * * cd /app && /usr/local/bin/python /app/scrape.py >> /var/log/cron.log 2>&1" | crontab -

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]