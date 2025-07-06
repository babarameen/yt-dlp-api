FROM python:3.10-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Railway provides dynamic PORT)
EXPOSE 8080

# Start Gunicorn with Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "index:app"]
