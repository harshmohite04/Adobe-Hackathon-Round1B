# Use official Python 3.9 image
FROM --platform=linux/amd64 python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy all project files
COPY . /app/

# Copy the pre-downloaded model into the image
COPY all-MiniLM-L6-v2 /app/model/all-MiniLM-L6-v2

# Install system dependencies (for faiss, PyTorch, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r req.txt

# Default command
CMD ["python", "app.py"] 