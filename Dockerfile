# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-production.txt requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Create directories for static files and logs
RUN mkdir -p staticfiles media logs

# Collect static files
RUN python manage.py collectstatic --noinput || echo "Static files collection failed, continuing..."

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/admin/').read()" || exit 1

# Create startup script that runs migrations before starting server
RUN echo '#!/bin/bash\n\
    set -e\n\
    echo "Running database migrations..."\n\
    python manage.py migrate --noinput\n\
    echo "Migrations complete!"\n\
    echo "Starting Gunicorn..."\n\
    exec gunicorn config.wsgi:application \\\n\
    --bind 0.0.0.0:8080 \\\n\
    --workers 3 \\\n\
    --threads 4 \\\n\
    --timeout 120 \\\n\
    --access-logfile - \\\n\
    --error-logfile - \\\n\
    --log-level info\n\
    ' > /app/start.sh && chmod +x /app/start.sh

# Run startup script
CMD ["/app/start.sh"]