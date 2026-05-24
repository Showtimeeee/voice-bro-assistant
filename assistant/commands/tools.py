import random


class ToolCommands:
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

    def tell_joke(self, command):
        jokes = [
            "Почему программист не пошел на вечеринку? Потому что он не смог найти подходящий URL!",
            "Почему компьютер пошел к врачу? У него был вирус!",
            "Как программист назвал свою кошку? Ctrl+Alt+Meow!"
        ]
        return random.choice(jokes)

    def translate(self, command):
        try:
            text_to_translate = command.replace("переведи", "").strip()
            return f"Перевод: {text_to_translate}"
        except Exception:
            return "Ошибка при переводе"

    def play_music(self, command):
        return "Функция воспроизведения музыки 1"
