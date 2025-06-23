from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'Missing URL'}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({'video_url': info['url'], 'title': info['title']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
