from index import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway provides PORT env
    print(f"🚀 Starting Flask on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
