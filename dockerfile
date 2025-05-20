FROM python:3.11-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create staticfiles directory with proper permissions
RUN mkdir -p /code/staticfiles && chmod 755 /code/staticfiles

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Start command with proper order, logging, and health checks
CMD python -c 'import time; time.sleep(3)' && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput --clear && \
    gunicorn core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --log-level debug \
    --error-logfile - \
    --access-logfile - \
    --timeout 120