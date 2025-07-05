from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
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

    output_file = f"output.{format}"  # temporary file

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,  # write to file
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': quality,
        }],
        'quiet': True,
        'cookiefile': 'cookies.txt',  # pass cookies for YouTube login
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # download audio

        # Send file as attachment
        return send_file(
            output_file,
            as_attachment=True,
            download_name=f"audio.{format}",
            mimetype="audio/mpeg"
        )

    except Exception as e:
        traceback.print_exc()  # log full error
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up downloaded file
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
