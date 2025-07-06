from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
import yt_dlp
import tempfile
import os
import mimetypes
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


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
        if not url:
            return jsonify({"error": "Missing 'url' parameter"}), 400

        format = "mp3"
        quality = "192"

        # Create a temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
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
            'quiet': True
        }

        print(f"▶️ Downloading: {url}")

        # Download and convert
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"✅ Download completed: {output_file}")

        @after_this_request
        def cleanup(response):
            try:
                os.remove(output_file)
                print(f"🗑 Deleted temp file: {output_file}")
            except Exception as e:
                print(f"⚠️ Cleanup failed: {e}")
            return response

        # Set MIME type
        mime_type, _ = mimetypes.guess_type(output_file)
        if not mime_type:
            mime_type = "application/octet-stream"

        return send_file(
            output_file,
            as_attachment=True,
            download_name="audio.mp3",
            mimetype=mime_type
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500
