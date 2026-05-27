import subprocess
import shutil

import yt_dlp


class MusicPlayer:
    def __init__(self):
        self._process = None
        self._check_ffplay()

    def _check_ffplay(self):
        self.ffplay_available = shutil.which("ffplay") is not None

    def play(self, query):
        if not self.ffplay_available:
            return "ffplay не найден. Установите ffmpeg."
        try:
            url, title = self._search_youtube(query)
            if not url:
                return "Ничего не найдено по запросу."
            self.stop()
            self._process = subprocess.Popen(
                [
                    "ffplay", "-nodisp", "-autoexit",
                    "-hide_banner", "-loglevel", "quiet", url,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return f"Воспроизвожу: {title}"
        except Exception as e:
            return f"Ошибка при воспроизведении: {str(e)}"

    def stop(self):
        if self._process and self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None

    def is_playing(self):
        return self._process is not None and self._process.poll() is None

    def _search_youtube(self, query):
        opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "default_search": "ytsearch",
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if not info or "entries" not in info or not info["entries"]:
                return None, None
            entry = info["entries"][0]
            return entry["url"], entry.get("title", "Неизвестно")
