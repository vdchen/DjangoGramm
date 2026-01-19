FROM ubuntu:latest
LABEL authors="vladi"

ENTRYPOINT ["top", "-b"]

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (needed for Postgres & Pillow)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files (CSS/JS) so Whitenoise can serve them
# We set dummy env vars because settings.py might crash without them
RUN SECRET_KEY=dummy DATABASE_URL=postgres://dummy:dummy@dummy:5432/dummy python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "DjangoGramm.wsgi:application"]