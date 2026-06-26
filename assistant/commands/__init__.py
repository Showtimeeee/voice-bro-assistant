import os
import pytz
from ..config import API_KEYS, FILE_PATHS
from ..log import logger
from ..notes import NotesManager
from ..translator import OfflineTranslator
from ..reminder import ReminderService
from ..music import MusicPlayer
from ..cache import Cache
from .general import GeneralCommands
from .info import InfoCommands
from .storage import StorageCommands
from .tools import ToolCommands
from .settings import SettingsCommands, _load_speed, _load_voice, _load_volume


class CommandProcessor(GeneralCommands, InfoCommands, StorageCommands, ToolCommands, SettingsCommands):
    def __init__(self, reminder_callback=None, tts=None):
        self.tts = tts
        self.weather_api_key = API_KEYS['weather']
        self.news_api_key = API_KEYS['news']
        self.timezone = pytz.timezone('Europe/Moscow')
        self.notes = NotesManager()
        self.reminders = ReminderService(callback=reminder_callback)
        self.translator = OfflineTranslator()
        self.music_player = MusicPlayer()
        self.cache = Cache(FILE_PATHS['cache_dir'])
        self._last_response = ""

        if self.tts:
            self.tts.set_rate(_load_speed())
            self.tts.set_volume(_load_volume())
            voice_idx = _load_voice()
            if voice_idx is not None:
                self.tts.set_voice(voice_idx)

        self.commands = {
            'greeting': self.handle_greeting,
            'farewell': self.handle_farewell,
            'weather': self.get_weather,
            'news': self.get_news,
            'time': self.get_time,
            'reminder': self.set_reminder,
            'note': self.add_note,
            'show_notes': self.show_notes,
            'calculate': self.calculate,
            'joke': self.tell_joke,
            'translate': self.translate,
            'music': self.play_music,
            'stop_music': self.stop_music,
            'search': self.search,
            'speed': self.set_speed,
            'voice': self.set_voice,
            'volume': self.set_volume,
            'repeat': self.handle_repeat,
            'how_are_you': self.handle_how_are_you,
            'help': self.show_help,
        }

        self.keywords = {
            'greeting': ['привет', 'добрый день', 'здравствуйте'],
            'farewell': ['пока', 'до свидания'],
            'weather': ['погода', 'какая погода'],
            'news': ['новости', 'что нового'],
            'time': ['время', 'который час'],
            'reminder': ['напомни'],
            'note': ['заметка', 'запиши'],
            'show_notes': ['покажи заметки', 'мои заметки'],
            'calculate': ['калькулятор', 'посчитай', 'посчитать'],
            'joke': ['шутка', 'анекдот'],
            'translate': ['перевод', 'переведи'],
            'music': ['включи', 'воспроизведи'],
            'stop_music': ['выключи музыку', 'останови музыку'],
            'search': ['поиск', 'найди'],
            'speed': ['говори быстрее', 'говори медленнее', 'нормальная скорость', 'увеличь скорость', 'уменьши скорость', 'скорость речи'],
            'voice': ['голос мужской', 'голос женский'],
            'volume': ['громче', 'тише', 'громкость'],
            'repeat': ['повтори', 'что ты сказала', 'ещё раз'],
            'how_are_you': ['как дела', 'как поживаешь'],
            'help': ['помощь', 'что умеешь'],
        }

    def process(self, command):
        command = command.lower()

        for cmd_type, keywords in self.keywords.items():
            if any(keyword in command for keyword in keywords):
                result = self.commands[cmd_type](command)
                if cmd_type != "repeat":
                    self._last_response = result
                return result

        logger.warning(f"Неизвестная команда: {command}")
        self._last_response = "Не совсем поняла команду"
        return self._last_response
