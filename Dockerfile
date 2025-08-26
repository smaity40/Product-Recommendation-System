# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose API port
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
