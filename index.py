from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import tempfile
import os
import traceback

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
            'cookiefile': 'cookies.txt',  # add your YouTube cookies file
        }

        print(f"▶️ Starting download for: {url}")

        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"✅ Download completed: {output_file}")

        # Return the file as download
        return send_file(
            output_file,
            as_attachment=True,
            download_name=f"audio.{format}",
            mimetype="audio/mpeg"
        )
    except yt_dlp.utils.DownloadError as e:
        traceback.print_exc()
        return jsonify({"error": f"Download error: {str(e)}"}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    finally:
        # Clean up temporary file
        if os.path.exists(output_file):
            os.remove(output_file)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
