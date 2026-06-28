import threading
import time
import re

from .log import logger


class TimerService:
    def __init__(self, callback=None):
        self.timers = []
        self.callback = callback
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def add_timer(self, seconds, label=None):
        timer = {
            "id": len(self.timers) + 1,
            "end_time": time.time() + seconds,
            "duration": seconds,
            "label": label or TimerService._fmt(seconds),
            "fired": False,
        }
        with self._lock:
            self.timers.append(timer)
        logger.info(f"Таймер {timer['id']} запущен на {seconds} сек")
        return timer["id"]

    def get_remaining(self, timer_id=None):
        now = time.time()
        with self._lock:
            if timer_id is not None:
                for t in self.timers:
                    if t["id"] == timer_id and not t["fired"]:
                        return max(0, t["end_time"] - now)
                return None
            result = []
            for t in self.timers:
                if not t["fired"]:
                    remaining = max(0, t["end_time"] - now)
                    result.append((t["id"], remaining, t["label"]))
            return result

    def active_count(self):
        with self._lock:
            return sum(1 for t in self.timers if not t["fired"])

    def _run(self):
        while self._running:
            now = time.time()
            fired = []
            with self._lock:
                for t in self.timers:
                    if not t["fired"] and now >= t["end_time"]:
                        t["fired"] = True
                        fired.append(t)
            for t in fired:
                if self.callback:
                    self.callback(t["label"])
            time.sleep(0.1)

    @staticmethod
    def _fmt(seconds):
        m = int(seconds // 60)
        s = int(seconds % 60)
        if m and s:
            return f"{m} мин {s} сек"
        if m:
            return f"{m} мин"
        return f"{s} сек"


def parse_duration(text):
    total = 0
    patterns = [
        (r"(\d+)\s*час(?:а|ов|)", 3600),
        (r"(\d+)\s*мин", 60),
        (r"(\d+)\s*секунд", 1),
    ]
    for pattern, multiplier in patterns:
        m = re.search(pattern, text)
        if m:
            total += int(m.group(1)) * multiplier
    return total if total > 0 else None
