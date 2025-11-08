# Base Layer
FROM python:3.14.0-slim

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project

COPY . .

# Export  port
EXPOSE 8000


# Running Command
CMD ["sh", "-c", "python manage.py migrate && python manage.py spectacular --file schema.yml && daphne -b 0.0.0.0 -p 8000 config.asgi:application"]