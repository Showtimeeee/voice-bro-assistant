import datetime
import requests
from duckduckgo_search import DDGS


class InfoCommands:
    def get_time(self, command):
        now = datetime.datetime.now(self.timezone)
        return f"Сейчас {now.strftime('%H:%M')}"

    def get_weather(self, command):
        try:
            response = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q=Москва&appid={self.weather_api_key}&units=metric&lang=ru"
            )
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"Сейчас в Москве {temp}°C, {description}"
        except Exception:
            return "Не удалось получить данные о погоде"

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

            articles = data['articles'][:5]
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
