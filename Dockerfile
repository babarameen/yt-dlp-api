FROM python:3.10-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Railway uses dynamic PORT)
EXPOSE 8080

# Run Flask directly for Railway
CMD ["python", "wsgi.py"]
