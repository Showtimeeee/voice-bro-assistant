import json
import os
import time


class Cache:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _path(self, key):
        return os.path.join(self.cache_dir, f"{key}.json")

    def get(self, key, ttl=600):
        try:
            with open(self._path(key), "r", encoding="utf-8") as f:
                entry = json.load(f)
            if time.time() - entry["timestamp"] < ttl:
                return entry["data"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass
        return None

    def set(self, key, data):
        entry = {"timestamp": time.time(), "data": data}
        with open(self._path(key), "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False)

    def clear(self, key=None):
        if key:
            try:
                os.remove(self._path(key))
            except FileNotFoundError:
                pass
        else:
            for f in os.listdir(self.cache_dir):
                if f.endswith(".json"):
                    os.remove(os.path.join(self.cache_dir, f))
