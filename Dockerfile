FROM python:3.10-slim

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all app files
COPY . .

EXPOSE 8080

# Start the server with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "index:app"]
