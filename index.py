from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # ✅ Added CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # ✅ Allow requests from any domain for now

@app.route("/")
def home():
    return "YT-DLP API is running!"

# ✅ GET /download for metadata
@app.route("/download", methods=["GET"])
def get_video_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forceurl': True,
        'simulate': True,
        'cookiefile': 'cookies.txt',  # ✅ Use cookies to bypass bot detection
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filtered_info = {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "formats": info.get("formats"),
            }
            return jsonify(filtered_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ POST /download for actual audio file
@app.route("/download", methods=["POST"])
def download_audio():
    data = request.get_json()
    url = data.get("url")
    format = data.get("format", "mp3")
    quality = data.get("quality", "192")

    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    output_file = f"output.{format}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'cookiefile': 'cookies.txt',  # ✅ Added cookie support
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': quality,
        }],
        'quiet': True
    }

    try:
        # Download and convert
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send file as attachment
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the file after sending
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
