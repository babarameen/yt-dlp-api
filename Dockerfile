FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy requirements first (to cache dependencies)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port (Railway will bind dynamically)
EXPOSE 8080

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "index:app"]
