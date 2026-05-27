from assistant.translator import OfflineTranslator


class TestParseCommand:
    def setup_method(self):
        self.t = OfflineTranslator()

    def test_default_to_russian(self):
        text, target = self.t.parse_command("переведи hello world")
        assert text == "hello world"
        assert target == "ru"

    def test_to_english(self):
        text, target = self.t.parse_command("переведи на английский привет")
        assert text == "привет"
        assert target == "en"

    def test_to_french(self):
        text, target = self.t.parse_command("переведи на французский merci")
        assert text == "merci"
        assert target == "fr"

    def test_no_text(self):
        text, target = self.t.parse_command("переведи")
        assert text == ""
        assert target == "ru"

    def test_перевод_variant(self):
        text, target = self.t.parse_command("перевод dog")
        assert text == "dog"
        assert target == "ru"
