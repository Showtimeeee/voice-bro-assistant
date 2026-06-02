import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, '.env'))
VOSK_MODEL_PATH = os.path.join(
    BASE_DIR, 
    os.getenv('VOSK_MODEL_DIR', 'vosk-model-small-ru-0.22'))
RATE = int(os.getenv('SPEECH_RATE', 150))  # Скорость речи
VOLUME = float(os.getenv('VOLUME_LEVEL', 1.0))  # Громкость

# API ключи из .env
API_KEYS = {
    'weather': os.getenv('OPENWEATHERMAP_KEY'),
    'news': os.getenv('NEWSAPI_KEY')
}

# Основные настройки приложения
SETTINGS = {
    'language': os.getenv('APP_LANGUAGE', 'ru'),
    'timezone': os.getenv('TIMEZONE', 'Europe/Moscow'),
    'default_city': os.getenv('DEFAULT_CITY', 'Москва'),
    'speech_rate': RATE,
    'volume_level': VOLUME
}

# Пути к файлам
FILE_PATHS = {
    'notes': os.path.join(BASE_DIR, os.getenv('NOTES_FILE', 'notes.txt')),
    'reminders': os.path.join(BASE_DIR, os.getenv('REMINDERS_FILE', 'reminders.txt')),
    'vosk_model': VOSK_MODEL_PATH,
    'cache_dir': os.path.join(BASE_DIR, os.getenv('CACHE_DIR', 'cache_data')),
}
