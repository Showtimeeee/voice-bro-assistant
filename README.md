# voice-bro-assistant

![assbro](https://github.com/user-attachments/assets/4d1c24aa-4943-4b60-a855-6781c88fdf17)

Голосовой ассистент на Python с русским языком. Офлайн-распознавание (Vosk) и синтез речи (pyttsx3), пробуждение по wake word.

## Возможности

- **Wake word** — активация по слову "Бро"
- **Погода** — текущая погода через OpenWeatherMap
- **Новости** — топ-5 новостей через NewsAPI
- **Заметки и напоминания** — создание, просмотр, удаление (сохраняются в файлы)
- **Поиск в интернете** — через DuckDuckGo
- **Время и дата** — текущее время
- **Калькулятор** — вычисление выражений
- **Шутки** — случайный анекдот
- **Помощь** — список команд

## Установка

```bash
pip install -r requirements.txt
```

Скачать Vosk-модель: https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
Распаковать в корень проекта.

Создать `.env`:
```
OPENWEATHERMAP_KEY=your_key
NEWSAPI_KEY=your_key
```

## Запуск

```bash
python main.py
```

Скажите "Бро" для активации, затем команду.

