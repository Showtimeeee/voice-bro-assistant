from assistant.commands.general import GeneralCommands


class TestGeneralCommands:
    def setup_method(self):
        self.cmd = GeneralCommands()

    def test_handle_greeting_returns_string(self):
        result = self.cmd.handle_greeting("привет")
        assert isinstance(result, str)
        assert len(result) > 3

    def test_handle_greeting_variety(self):
        results = {self.cmd.handle_greeting("привет") for _ in range(50)}
        assert len(results) > 1

    def test_handle_farewell_returns_string(self):
        result = self.cmd.handle_farewell("пока")
        assert isinstance(result, str)

    def test_handle_how_are_you_returns_string(self):
        result = self.cmd.handle_how_are_you("как дела")
        assert isinstance(result, str)

    def test_show_help_contains_commands(self):
        result = self.cmd.show_help("помощь")
        lower = result.lower()
        assert "погод" in lower
        assert "новост" in lower
        assert "времен" in lower
        assert "поиск" in lower
