import subprocess
import webbrowser

from ..timer import parse_duration
from ..log import logger


_APP_MAP = {
    "браузер": "web",
    "калькулятор": "calc.exe",
    "блокнот": "notepad.exe",
    "проводник": "explorer.exe",
    "диспетчер задач": "taskmgr.exe",
    "терминал": "cmd.exe",
    "командную строку": "cmd.exe",
}


class SystemCommands:
    def open_app(self, command):
        for name in _APP_MAP:
            if name in command:
                try:
                    target = _APP_MAP[name]
                    if target == "web":
                        webbrowser.open("https://google.com")
                    else:
                        subprocess.Popen([target], shell=True)
                    return f"Открываю {name}"
                except Exception as e:
                    logger.error(f"Ошибка открытия {name}: {e}")
                    return f"Не удалось открыть {name}"
        return "Что открыть? Например: открой браузер, открой калькулятор"

    def shutdown_pc(self, command):
        seconds = parse_duration(command)
        if not seconds:
            seconds = 30
        subprocess.Popen(["shutdown", "/s", "/t", str(seconds)], shell=False)
        if seconds >= 60:
            return f"Компьютер выключится через {seconds // 60} мин"
        return f"Компьютер выключится через {seconds} сек"

    def cancel_shutdown(self, command):
        try:
            subprocess.Popen(["shutdown", "/a"], shell=False)
            return "Выключение отменено"
        except Exception as e:
            logger.error(f"Ошибка отмены выключения: {e}")
            return "Не удалось отменить выключение"

    def restart_pc(self, command):
        seconds = parse_duration(command)
        if not seconds:
            seconds = 30
        subprocess.Popen(["shutdown", "/r", "/t", str(seconds)], shell=False)
        if seconds >= 60:
            return f"Компьютер перезагрузится через {seconds // 60} мин"
        return f"Компьютер перезагрузится через {seconds} сек"

    def lock_pc(self, command):
        try:
            subprocess.Popen(
                ["rundll32.exe", "user32.dll,LockWorkStation"], shell=False
            )
            return "Компьютер заблокирован"
        except Exception as e:
            logger.error(f"Ошибка блокировки: {e}")
            return "Не удалось заблокировать компьютер"
