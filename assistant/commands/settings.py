import json
import re
import os


_SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "settings.json",
)


def _load_settings():
    try:
        with open(_SETTINGS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_setting(key, value):
    data = _load_settings()
    data[key] = value
    with open(_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _load_speed():
    return _load_settings().get("speech_rate", 150)


def _load_voice():
    return _load_settings().get("voice_index", None)


def _load_volume():
    return _load_settings().get("volume", 1.0)


class SettingsCommands:
    def set_speed(self, command):
        if not self.tts:
            return "Ошибка: голосовой движок не инициализирован."
        if "быстрее" in command or "увеличь" in command:
            rate = min(400, self.tts.get_rate() + 10)
        elif "медленнее" in command or "уменьши" in command:
            rate = max(50, self.tts.get_rate() - 10)
        elif "нормальн" in command:
            rate = 150
        else:
            match = re.search(r"(\d+)", command)
            if match:
                rate = max(50, min(400, int(match.group(1))))
            else:
                return "Не поняла, какую скорость установить."
        self.tts.set_rate(rate)
        _save_setting("speech_rate", rate)
        return f"Скорость речи: {rate}"

    def set_voice(self, command):
        if not self.tts:
            return "Ошибка: голосовой движок не инициализирован."
        voices = self.tts.get_voices()
        if "мужск" in command:
            target = 0
        elif "женск" in command:
            target = 1 if len(voices) > 1 else 0
        else:
            return "Скажите «голос мужской» или «голос женский»."
        if target < len(voices):
            self.tts.set_voice(target)
            _save_setting("voice_index", target)
            return "Голос изменён."
        return "Доступен только один голос."

    def set_volume(self, command):
        if not self.tts:
            return "Ошибка: голосовой движок не инициализирован."
        if "громче" in command:
            vol = min(1.0, self.tts.get_volume() + 0.1)
        elif "тише" in command:
            vol = max(0.0, self.tts.get_volume() - 0.1)
        else:
            match = re.search(r"(\d+)", command)
            if match:
                vol = max(0.0, min(1.0, int(match.group(1)) / 100))
            else:
                return "Не поняла, какую громкость установить."
        self.tts.set_volume(vol)
        _save_setting("volume", vol)
        return f"Громкость: {int(vol * 100)}%"
