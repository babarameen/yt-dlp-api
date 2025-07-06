FROM python:3.10-slim

# Install ffmpeg and certificates
RUN apt-get update && apt-get install -y ffmpeg ca-certificates

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port
EXPOSE 8080

# Run with Gunicorn (increased timeout for long downloads)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "120", "index:app"]
