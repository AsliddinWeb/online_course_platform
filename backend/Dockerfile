FROM python:3.12-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Work directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements/base.txt requirements/base.txt
COPY requirements/prod.txt requirements/prod.txt
RUN pip install --no-cache-dir -r requirements/prod.txt

# Copy project
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application"]