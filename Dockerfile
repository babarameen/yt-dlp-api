FROM python:3.11-slim

WORKDIR /app

# Install yt-dlp
RUN pip install yt-dlp flask

# Copy project files
COPY . .

# Expose port (for Railway)
EXPOSE 8000

# Run the app
CMD ["python", "index.py"]

