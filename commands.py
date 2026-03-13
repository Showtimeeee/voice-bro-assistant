import datetime


class CommandProcessor:
    def process(self, command):
        command = command.lower()
        
        if "привет" in command:
            return "Здравствуйте!"
        elif "как дела" in command:
            return "У меня всё хорошо, спасибо!"
        elif "время" in command:
            return "Сейчас " + datetime.now().strftime("%H:%M")
        else:
            return "Не совсем поняла команду"
