import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
    'notes': os.getenv('NOTES_FILE', 'notes.txt'),
    'reminders': os.getenv('REMINDERS_FILE', 'reminders.txt'),
    'vosk_model': VOSK_MODEL_PATH
}

# Настройки БД
DATABASE = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'your_user'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'database': os.getenv('DB_NAME', 'your_database')
}

# Логирование
LOGGING = {
    'log_file': os.getenv('LOG_FILE', 'app.log'),
    'level': os.getenv('LOG_LEVEL', 'INFO')
}

# Уведомления
NOTIFICATIONS = {
    'enabled': os.getenv('NOTIFICATIONS_ENABLED', 'True').lower() in ['true', '1', 'yes'],
    'method': os.getenv('NOTIFICATION_METHOD', 'email'),
    'email': os.getenv('NOTIFICATION_EMAIL', 'your@email.com')
}
