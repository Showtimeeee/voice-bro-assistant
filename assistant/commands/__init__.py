import pytz
from ..config import API_KEYS
from ..log import logger
from ..notes import NotesManager
from ..translator import OfflineTranslator
from ..reminder import ReminderService
from ..music import MusicPlayer
from .general import GeneralCommands
from .info import InfoCommands
from .storage import StorageCommands
from .tools import ToolCommands


class CommandProcessor(GeneralCommands, InfoCommands, StorageCommands, ToolCommands):
    def __init__(self, reminder_callback=None):
        self.weather_api_key = API_KEYS['weather']
        self.news_api_key = API_KEYS['news']
        self.timezone = pytz.timezone('Europe/Moscow')
        self.notes = NotesManager()
        self.reminders = ReminderService(callback=reminder_callback)
        self.translator = OfflineTranslator()
        self.music_player = MusicPlayer()

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
            'how_are_you': ['как дела', 'как поживаешь'],
            'help': ['помощь', 'что умеешь'],
        }

    def process(self, command):
        command = command.lower()

        for cmd_type, keywords in self.keywords.items():
            if any(keyword in command for keyword in keywords):
                return self.commands[cmd_type](command)

        logger.warning(f"Неизвестная команда: {command}")
        return "Не совсем поняла команду"
