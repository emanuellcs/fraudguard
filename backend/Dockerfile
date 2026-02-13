FROM python:3.11-slim

# Install system dependencies (OpenMP for XGBoost)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (Caching layer)
# We copy ONLY requirements.txt first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
# Since this file is inside 'backend/', COPY . . puts 'app', 'Dockerfile', etc. into /app
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]