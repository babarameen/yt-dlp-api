from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
import yt_dlp
import tempfile
import os
import traceback
import mimetypes

app = Flask(__name__)
CORS(app)  # Allow requests from frontend


@app.route("/")
def home():
    return "✅ YT-DLP API is running!"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/download", methods=["POST"])
def download_audio():
    try:
        data = request.get_json()
        url = data.get("url")
        format = data.get("format", "mp3")
        quality = data.get("quality", "192")

        if not url:
            return jsonify({"error": "Missing URL parameter"}), 400

        # Create a temporary file for output
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}")
        output_file = temp_file.name
        temp_file.close()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_file,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': quality,
            }],
            'quiet': True,
            'cookiefile': 'cookies.txt',  # optional: for restricted videos
        }

        print(f"▶️ Starting download for: {url}")

        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"✅ Download completed: {output_file}")

        # Automatically delete temp file after response is sent
        @after_this_request
        def cleanup(response):
            try:
                os.remove(output_file)
                print(f"🗑 Temporary file deleted: {output_file}")
            except Exception as cleanup_error:
                print(f"⚠️ Cleanup failed: {cleanup_error}")
