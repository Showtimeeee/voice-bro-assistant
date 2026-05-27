import pytest
from assistant.commands.tools import ToolCommands


@pytest.fixture
def tools():
    return ToolCommands()


# --- _safe_eval ---

@pytest.mark.parametrize("expr, expected", [
    ("2+2", 4),
    ("10 - 3", 7),
    ("4 * 5", 20),
    ("15 / 3", 5),
    ("(2+3)*4", 20),
    ("10.5 + 0.5", 11.0),
    ("3 * 2 + 4", 10),
    ("100 / 4", 25),
    ("0.5 * 10", 5.0),
    ("-5 + 10", 5.0),
])
def test_safe_eval_valid(tools, expr, expected):
    assert tools._safe_eval(expr) == expected


@pytest.mark.parametrize("expr", [
    "", "()", "+", "*", "/",
    "a + b",
    "__import__('os')",
    "os.system('rm')",
    "1/0",
    "import os",
])
def test_safe_eval_invalid(tools, expr):
    with pytest.raises(Exception):
        tools._safe_eval(expr)


# --- tell_joke ---

def test_tell_joke_returns_string(tools):
    result = tools.tell_joke("шутка")
    assert isinstance(result, str)
    assert len(result) > 10


# --- calculate ---

def test_calculate_valid(tools):
    result = tools.calculate("посчитай 2+3")
    assert result == "Результат: 5"


def test_calculate_invalid(tools):
    result = tools.calculate("посчитай abc")
    assert result == "Некорректное математическое выражение"


def test_calculate_without_prefix(tools):
    class Fake:
        def _safe_eval(self, x):
            return 42
    result = tools.calculate("2+2")
    assert "Результат" in result
