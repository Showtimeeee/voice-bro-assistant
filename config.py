import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOSK_MODEL_PATH = os.path.join(BASE_DIR, 'vosk-model-small-ru-0.22')
RATE = 150  # Скорость речи
VOLUME = 1.0  # Громкость

# Настройки API ключей
API_KEYS = {
    'weather': 'ВАШ_КЛЮЧ_ОТ_OPENWEATHERMAP',  # Замените на ваш реальный ключ
    'news': 'ВАШ_КЛЮЧ_ОТ_NEWSAPI',            # Замените на ваш реальный ключ
}

# Основные настройки приложения
SETTINGS = {
    'language': 'ru',                         # Язык интерфейса
    'timezone': 'Europe/Moscow',              # Часовой пояс
    'default_city': 'Москва',                 # Город по умолчанию для погоды
    'speech_rate': 150,                       # Скорость речи
    'volume_level': 1.0                       # Уровень громкости
}

# Пути к файлам и директориям
FILE_PATHS = {
    'notes': 'notes.txt',                     # Файл для хранения заметок
    'reminders': 'reminders.txt',             # Файл для напоминаний
    'vosk_model': 'vosk-model-small-ru-0.22'  # Модель для распознавания речи
}

# Настройки подключения к базе данных (если используется)
DATABASE = {
    'host': 'localhost',
    'port': 5432,
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database'
}

# Настройки логирования (опционально)
LOGGING = {
    'log_file': 'app.log',
    'level': 'INFO'
}

# Настройки уведомлений (опционально)
NOTIFICATIONS = {
    'enabled': True,
    'method': 'email',  # или 'push', 'sms'
    'email': 'your@email.com'
}
