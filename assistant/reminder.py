import os
import json
import threading
import time
from datetime import datetime
from dateparser.search import search_dates
from .log import logger
from . import config


class ReminderService:
    def __init__(self, callback=None):
        self._lock = threading.Lock()
        self._reminders = []
        self._thread = None
        self._running = False
        self._callback = callback
        self._path = config.FILE_PATHS['reminders']

    def parse(self, command):
        text = command.replace("напомни", "").strip()
        if not text:
            return None, None

        try:
            results = search_dates(text, languages=['ru'])
        except Exception:
            return None, text

        if not results:
            return None, text

        time_text, dt = results[0]
        if dt < datetime.now():
            return None, text

        reminder_text = text.replace(time_text, "").strip()
        if not reminder_text:
            reminder_text = time_text

        return dt, reminder_text

    def add(self, text, dt=None):
        with self._lock:
            self._reminders.append({
                'time': dt.isoformat() if dt else None,
                'text': text,
                'fired': False,
                'created': datetime.now().isoformat(),
            })
            self._save()
            idx = len(self._reminders)
        if dt:
            logger.info(f"Напоминание на {dt}: {text}")
        return idx

    def show_all(self):
        with self._lock:
            if not self._reminders:
                return "Напоминаний нет"
            lines = []
            for i, r in enumerate(self._reminders, 1):
                if r['fired']:
                    prefix = "[✓]"
                elif r['time']:
                    dt = datetime.fromisoformat(r['time'])
                    prefix = dt.strftime('%d.%m %H:%M')
                else:
                    prefix = "[ ]"
                lines.append(f"{i}. {prefix} {r['text']}")
            return "Ваши напоминания:\n" + "\n".join(lines)

    def delete(self, index):
        with self._lock:
            try:
                idx = int(index) - 1
                if 0 <= idx < len(self._reminders):
                    r = self._reminders.pop(idx)
                    self._save()
                    return f"Напоминание удалено: {r['text']}"
                return "Неверный номер напоминания"
            except (ValueError, IndexError):
                return "Ошибка при удалении напоминания"

    def timed_count(self):
        with self._lock:
            return sum(1 for r in self._reminders if r['time'] and not r['fired'])

    def start(self):
        self._load()
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        active = self.timed_count()
        logger.info(f"Сервис напоминаний запущен. Активных: {active}")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)

    def _run(self):
        while self._running:
            now = datetime.now()
            to_fire = []
            with self._lock:
                for r in self._reminders:
                    if r['time'] and not r['fired']:
                        dt = datetime.fromisoformat(r['time'])
                        if dt <= now:
                            r['fired'] = True
                            to_fire.append(r['text'])
                if to_fire:
                    self._save()
            for text in to_fire:
                logger.info(f"Сработало напоминание: {text}")
                if self._callback:
                    self._callback(text)
            time.sleep(10)

    def _save(self):
        try:
            with open(self._path, 'w', encoding='utf-8') as f:
                json.dump(self._reminders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Ошибка сохранения напоминаний: {e}")

    def _load(self):
        try:
            if os.path.exists(self._path):
                with open(self._path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._reminders = data
        except Exception:
            logger.info("Файл напоминаний не найден или имеет старый формат")
