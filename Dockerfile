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

# Expose port (for Railway dynamic port)
EXPOSE 8080

# Start the app with Gunicorn
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:$PORT", "--worker-class", "gevent", "--timeout", "120", "--access-logfile", "-"]
