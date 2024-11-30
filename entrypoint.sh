#!/bin/bash

# Run an initial scrape
python /app/scrape.py

# Start cron in the foreground
cron -f