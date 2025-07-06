from index import app

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))  # Railway provides PORT env
    print(f"🚀 Running on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
