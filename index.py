from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import io
import traceback

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route("/")
def home():
    return "✅ YT-DLP API is running!"

@app.route("/download", methods=["POST"])
def download_audio():
    data = request.get_json()
    url = data.get("url")
    format = data.get("format", "mp3")
    quality = data.get("quality", "192")

    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    try:
        # Use in-memory buffer to store audio
        buffer = io.BytesIO()
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '-',  # output to stdout
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': quality,
            }],
            'quiet': True,
            'cookiefile': 'cookies.txt',  # pass cookies
            'logger': yt_dlp.Logger(),    # enable yt-dlp logging
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download audio into buffer
            result = ydl.download([url])
            print("yt-dlp result:", result)  # log for debug

        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"audio.{format}",
            mimetype="audio/mpeg"
        )

    except Exception as e:
        traceback.print_exc()  # print full error to Railway logs
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
