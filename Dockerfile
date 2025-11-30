# Use Python 3.11 slim image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-production.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p staticfiles media logs

# Collect static files
RUN python manage.py collectstatic --noinput || echo "Static failed"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen(\"http://localhost:8000/admin/\").read()" || exit 1


CMD rm -f /app/db.sqlite3 && \
    find /app -path "*/migrations/*.py" ! -name "__init__.py" -delete && \
    find /app -path "*/migrations/*.pyc" -delete && \
    echo "Creating fresh migrations..." && \
    python manage.py makemigrations && \
    echo "Applying migrations..." && \
    python manage.py migrate --noinput && \
    echo "Starting Gunicorn..." && \
    gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 3
