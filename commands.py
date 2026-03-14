import datetime
import requests
import pytz
import random
from config import API_KEYS
from notes import NotesManager
from reminders import ReminderManager
import os
from PIL import Image
import urllib.request


class CommandProcessor:
    def __init__(self):
        self.weather_api_key = API_KEYS['weather']
        self.news_api_key = API_KEYS['news']
        self.timezone = pytz.timezone('Europe/Moscow')
        self.notes = NotesManager()
        self.reminders = ReminderManager()
        
        # Словарь команд
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
            'search': self.search,
            'how_are_you': self.handle_how_are_you,
            'help': self.show_help,
            'meme': self.show_meme
        }
        
        # Ключевые слова
        self.keywords = {
            'greeting': ['привет', 'добрый день', 'здравствуйте'],
            'farewell': ['пока', 'до свидания'],
            'weather': ['погода', 'какая погода'],
            'news': ['новости', 'что нового'],
            'time': ['время', 'который час'],
            'reminder': ['напомни'],
            'note': ['заметка', 'запиши'],
            'show_notes': ['покажи заметки', 'мои заметки'],
            'calculate': ['калькулятор', 'посчитать'],
            'joke': ['шутка', 'анекдот'],
            'translate': ['перевод', 'переведи'],
            'music': ['включи музыку', 'воспроизведи'],
            'search': ['поиск', 'найди'],
            'how_are_you': ['как дела', 'как поживаешь'],
            'help': ['помощь', 'что умеешь'],
            'meme': ['пришли мем', 'покажи мем', 'мем']
        }

    def process(self, command):
        command = command.lower()
        
        for cmd_type, keywords in self.keywords.items():
            if any(keyword in command for keyword in keywords):
                return self.commands[cmd_type](command)
                
        return "Не совсем поняла команду"

    # Обработка приветствий (моки)
    def handle_greeting(self, command):
        greetings = [
            "Здравствуйте!",
            "Добрый день!",
            "Рад вас слышать!",
            "Приветствую!",
            "Добрый день, чем могу помочь?"
        ]
        return random.choice(greetings)

    # Обработка прощаний (моки)
    def handle_farewell(self, command):
        farewells = [
            "До свидания!",
            "Всего доброго!",
            "Хорошего дня!",
            "До встречи!",
            "Буду ждать вашего возвращения"
        ]
        return random.choice(farewells)

    # Время
    def get_time(self, command):
        now = datetime.datetime.now(self.timezone)
        return f"Сейчас {now.strftime('%H:%M')}"

    # Погода
    def get_weather(self, command):
        try:
            response = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q=Москва&appid={self.weather_api_key}&units=metric&lang=ru"
            )
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"Сейчас в Москве {temp}°C, {description}"
        except Exception as e:
            return "Не удалось получить данные о погоде"
        
        
        
     # Новости
    def get_news(self, command):
        try:
            response = requests.get(
                f"https://newsapi.org/v2/top-headlines?"
                f"country=ru&"
                f"apiKey={self.news_api_key}&"
                f"language=ru"
            )
            
            if response.status_code != 200:
                return "Ошибка при получении новостей"
                
            data = response.json()
            
            if not data.get('articles'):
                return "Новости не найдены"
                
            articles = data['articles'][:5]  # Берем топ-5 новостей
            news_list = "Последние новости:\n"
            
            for index, article in enumerate(articles, start=1):
                title = article.get('title', 'Без заголовка')
                description = article.get('description', 'Нет описания')
                news_list += f"{index}. {title}\n{description}\n\n"
                
            return news_list
            
        except requests.exceptions.RequestException:
            return "Произошла ошибка при загрузке новостей"
        except Exception as e:
            return f"Не удалось получить новости: {str(e)}"
