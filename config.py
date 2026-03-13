import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOSK_MODEL_PATH = os.path.join(BASE_DIR, 'vosk-model-small-ru-0.22')
RATE = 150  # Скорость речи
VOLUME = 1.0  # Громкость
