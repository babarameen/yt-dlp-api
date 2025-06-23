from flask import Flask, request, jsonify
import yt_dlp
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "YT-DLP API is running!"

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forceurl': True,
        'simulate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Filter relevant info
            filtered_info = {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "formats": info.get("formats")
            }

            return app.response_class(
                response=json.dumps(filtered_info, indent=2),
                status=200,
                mimetype='application/json'
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
