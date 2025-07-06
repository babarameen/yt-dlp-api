# Use Python slim base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Expose port (for Railway dynamic port binding)
EXPOSE 8080

# Use Gunicorn with dynamic port binding and 2 workers
CMD exec gunicorn index:app --bind 0.0.0.0:$PORT --workers=2
