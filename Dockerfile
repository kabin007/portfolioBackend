FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Install system dependencies for building psycopg and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
