FROM python:3.11-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code  # Align with fly.toml static guest_path

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files and migrate database before starting server
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn core.wsgi:application --bind 0.0.0.0:$PORT

