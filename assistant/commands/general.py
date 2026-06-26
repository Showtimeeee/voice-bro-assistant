import random


class GeneralCommands:
    def handle_greeting(self, command):
        greetings = [
            "Здравствуйте!",
            "Добрый день!",
            "Рад вас слышать!",
            "Приветствую!",
            "Добрый день, чем могу помочь?"
        ]
        return random.choice(greetings)

    def handle_farewell(self, command):
        farewells = [
            "До свидания!",
            "Всего доброго!",
            "Хорошего дня!",
            "До встречи!",
            "Буду ждать вашего возвращения"
        ]
        return random.choice(farewells)

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

    def handle_repeat(self, command):
        if self._last_response:
            return self._last_response
        return "Я ещё ничего не говорила."
