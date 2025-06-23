import express from "express";
import cors from "cors";
import { exec } from "child_process";

const app = express();
app.use(cors());

app.get("/download", (req, res) => {
  const url = req.query.url;
  if (!url) return res.status(400).json({ error: "Missing URL" });

  exec(`yt-dlp -f mp4 --get-url "${url}"`, (error, stdout) => {
    if (error || !stdout.trim()) {
      return res.status(500).json({ error: "Failed to extract video" });
    }
    res.json({ video_url: stdout.trim() });
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`yt-dlp API running on port ${PORT}`));
