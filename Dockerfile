# Dockerfile for SportsMole Scraper API

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY scraper.py .
COPY api.py .
COPY config.py .

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
# Disable debug mode in Docker for security
ENV DEBUG_MODE=false

# Run the API
CMD ["python", "api.py"]
