import datetime
import requests
import pytz
import random
from .config import API_KEYS
from .notes import NotesManager, ReminderManager
from duckduckgo_search import DDGS


class CommandProcessor:
    def __init__(self):
        self.weather_api_key = API_KEYS['weather']
        self.news_api_key = API_KEYS['news']
        self.timezone = pytz.timezone('Europe/Moscow')
        self.notes = NotesManager()
        self.reminders = ReminderManager()
        
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
            'calculate': ['калькулятор', 'посчитать'],
            'joke': ['шутка', 'анекдот'],
            'translate': ['перевод', 'переведи'],
            'music': ['включи музыку', 'воспроизведи'],
            'search': ['поиск', 'найди'],
            'how_are_you': ['как дела', 'как поживаешь'],
            'help': ['помощь', 'что умеешь'],
        }

    def process(self, command):
        command = command.lower()
        
        for cmd_type, keywords in self.keywords.items():
            if any(keyword in command for keyword in keywords):
                return self.commands[cmd_type](command)
                
        return "Не совсем поняла команду"

    # Обработка приветствий
    def handle_greeting(self, command):
        greetings = [
            "Здравствуйте!",
            "Добрый день!",
            "Рад вас слышать!",
            "Приветствую!",
            "Добрый день, чем могу помочь?"
        ]
        return random.choice(greetings)

    # Обработка прощаний
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


    # Калькулятор
    def calculate(self, command):
        expr = command.replace("посчитай", "").replace("калькулятор", "").strip()
        try:
            result = self._safe_eval(expr)
            return f"Результат: {result}"
        except Exception:
            return "Некорректное математическое выражение"

    def _safe_eval(self, expr):
        pos = 0

        def skip_ws():
            nonlocal pos
            while pos < len(expr) and expr[pos] == " ":
                pos += 1

        def parse_number():
            nonlocal pos
            skip_ws()
            if pos >= len(expr):
                raise ValueError
            start = pos
            if expr[pos] in ("+", "-"):
                pos += 1
            while pos < len(expr) and (expr[pos].isdigit() or expr[pos] == "."):
                pos += 1
            if pos == start or (pos == start + 1 and expr[start] in ("+", "-")):
                raise ValueError
            return float(expr[start:pos])

        def parse_factor():
            nonlocal pos
            skip_ws()
            if pos < len(expr) and expr[pos] == "(":
                pos += 1
                val = parse_expr()
                skip_ws()
                if pos >= len(expr) or expr[pos] != ")":
                    raise ValueError
                pos += 1
                return val
            return parse_number()

        def parse_term():
            nonlocal pos
            val = parse_factor()
            while True:
                skip_ws()
                if pos >= len(expr):
                    break
                op = expr[pos]
                if op in ("*", "/"):
                    pos += 1
                    right = parse_factor()
                    val = val * right if op == "*" else val / right
                else:
                    break
            return val

        def parse_expr():
            nonlocal pos
            val = parse_term()
            while True:
                skip_ws()
                if pos >= len(expr):
                    break
                op = expr[pos]
                if op in ("+", "-"):
                    pos += 1
                    right = parse_term()
                    val = val + right if op == "+" else val - right
                else:
                    break
            return val

        result = parse_expr()
        skip_ws()
        if pos != len(expr):
            raise ValueError
        return int(result) if result == int(result) else result

    # Анекдоты (моки)
    def tell_joke(self, command):
        jokes = [
            "Почему программист не пошел на вечеринку? Потому что он не смог найти подходящий URL!",
            "Почему компьютер пошел к врачу? У него был вирус!",
            "Как программист назвал свою кошку? Ctrl+Alt+Meow!"
        ]
        return random.choice(jokes)

    # Перевод (моки)
    def translate(self, command):
        try:
            text_to_translate = command.replace("переведи", "").strip()
            return f"Перевод: {text_to_translate}"
        except Exception:
            return "Ошибка при переводе"

    # Музыка (моки)
    def play_music(self, command):
        return "Функция воспроизведения музыки 1"

    # Поиск
    def search(self, command):
        try:
            query = command.replace("найди", "").strip()
            if not query:
                return "Что вы хотите найти?"

            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=2))

            if not results:
                return f"Ничего не нашёл по запросу '{query}'."

            parts = [f"Вот что нашёл по запросу '{query}'."]
            for r in results:
                title = r.get("title", "")
                body = r.get("body", "")
                snippet = body[:300] if body else ""
                if title and snippet:
                    parts.append(f"{title}: {snippet}")
                elif title:
                    parts.append(title)

            return " ".join(parts)
        except ImportError:
            return "Модуль поиска не установлен. Выполните: pip install duckduckgo-search"
        except Exception as e:
            return f"Не удалось выполнить поиск: {str(e)}"

    # Помощь
    def show_help(self, command):
        help_text = (
            "Я могу помочь с:\n"
            "- Погодной информацией\n"
            "- Новыми новостями\n"
            "- Временем\n"
            "- Напоминаниями\n"
            "- Записками\n"
            "- Математическими вычислениями\n"
            "- Анекдоты\n"
            "- Переводами\n"
            "- Воспроизведением музыки\n"
            "- Поиском информации\n"
            "Просто скажите команду, и я постараюсь помочь!"
        )
        return help_text

    def handle_how_are_you(self, command):
        replies = ["Всё отлично!", "Работаю в штатном режиме", "Лучше всех, спасибо!"]
        return random.choice(replies)

    # Заметки 
    def add_note(self, command):
        try:
            text = command.replace("запиши", "").replace("заметка", "").strip()
            if not text:
                return "Пожалуйста, укажите текст заметки"
            self.notes.add_note(text)
            return f"Заметка успешно добавлена: {text}"
        except Exception as e:
            return f"Произошла ошибка при добавлении заметки: {str(e)}"

            
    # Показать заметки
    def show_notes(self, command):
        try:
            return self.notes.show_notes()
        except Exception as e:
            return f"Произошла ошибка при отображении заметок: {str(e)}"

            
    # Удалить заметку
    def delete_note(self, command):
        try:
            # Извлекаем номер заметки из команды
            words = command.split()
            if 'удалить' in words:
                try:
                    note_number = int(words[-1])
                    return self.notes.delete_note(note_number)
                except:
                    pass
            return "Не указан номер заметки для удаления"
        except Exception as e:
            return f"Произошла ошибка при удалении заметки: {str(e)}"

    
    # Напоминания
    def set_reminder(self, command):
        try:
            text = command.replace("напомни", "").strip()
            if not text:
                return "Пожалуйста, укажите текст напоминания"
            self.reminders.add_reminder(text)
            return f"Напоминание установлено: {text}"
        except Exception as e:
            return f"Произошла ошибка при установке напоминания: {str(e)}"

    
    # Показать напоминания
    def show_reminders(self, command):
        try:
            return self.reminders.show_reminders()
        except Exception as e:
            return f"Произошла ошибка при отображении напоминаний: {str(e)}"

    # Удалить напоминание
    def delete_reminder(self, command):
        try:
            # Извлекаем номер напоминания из команды
            words = command.split()
            if 'удалить' in words:
                try:
                    reminder_number = int(words[-1])
                    return self.reminders.delete_reminder(reminder_number)
                except:
                    pass
            return "Не указан номер напоминания для удаления"
        except Exception as e:
            return f"Произошла ошибка при удалении напоминания: {str(e)}"
