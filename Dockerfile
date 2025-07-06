FROM python:3.10-slim

# Install ffmpeg and certificates
RUN apt-get update && apt-get install -y ffmpeg ca-certificates && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (for Railway, dynamic port will be set by $PORT)
EXPOSE 8080

# Use Gunicorn with wsgi entry point
CMD exec gunicorn --bind :$PORT --timeout 120 wsgi:app
