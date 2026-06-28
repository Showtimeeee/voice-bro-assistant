from ..timer import TimerService, parse_duration


class TimerCommands:
    def start_timer(self, command):
        seconds = parse_duration(command)
        if not seconds:
            return "Не поняла, на сколько установить таймер. Скажите, например: таймер на 10 минут."
        tid = self.timer_service.add_timer(seconds)
        return f"Таймер {tid} на {TimerService._fmt(seconds)} запущен."

    def check_timer(self, command):
        timers = self.timer_service.get_remaining()
        if not timers:
            return "Нет активных таймеров."
        parts = []
        for tid, remaining, label in timers:
            parts.append(
                f"Таймер {tid}: осталось {TimerService._fmt(remaining)}"
            )
        return " ".join(parts)
