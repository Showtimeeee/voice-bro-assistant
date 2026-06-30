import os
from assistant.notes import NotesManager
from assistant.reminder import ReminderService
from assistant.config import FILE_PATHS


class TestNotesManager:
    def setup_method(self):
        self.path = FILE_PATHS['notes']
        if os.path.exists(self.path):
            os.remove(self.path)
        self.mgr = NotesManager()

    def test_empty_notes(self):
        assert self.mgr.show_notes() == "Заметок нет"

    def test_add_note(self):
        result = self.mgr.add_note("купить хлеб")
        assert result == "Заметка добавлена"

    def test_show_notes(self):
        self.mgr.add_note("заметка 1")
        self.mgr.add_note("заметка 2")
        result = self.mgr.show_notes()
        assert "заметка 1" in result
        assert "заметка 2" in result

    def test_delete_note(self):
        self.mgr.add_note("удалить меня")
        result = self.mgr.delete_note(1)
        assert "удалена" in result
        assert self.mgr.show_notes() == "Заметок нет"

    def test_delete_note_invalid_index(self):
        self.mgr.add_note("заметка")
        result = self.mgr.delete_note(99)
        assert "Неверный номер" in result

    def test_persistence(self):
        self.mgr.add_note("сохранённая заметка")
        mgr2 = NotesManager()
        result = mgr2.show_notes()
        assert "сохранённая заметка" in result

    def test_add_empty_text(self):
        result = self.mgr.add_note("")
        assert "Не указан" in result

    def test_count_zero(self):
        assert self.mgr.count_notes() == "У вас нет заметок"

    def test_count_one(self):
        self.mgr.add_note("одна заметка")
        assert self.mgr.count_notes() == "У вас 1 заметка"

    def test_count_many(self):
        self.mgr.add_note("заметка 1")
        self.mgr.add_note("заметка 2")
        self.mgr.add_note("заметка 3")
        assert self.mgr.count_notes() == "У вас 3 заметок"


class TestReminderService:
    def setup_method(self):
        self.path = FILE_PATHS['reminders']
        if os.path.exists(self.path):
            os.remove(self.path)
        self.svc = ReminderService()

    def test_empty(self):
        assert self.svc.show_all() == "Напоминаний нет"

    def test_add_simple(self):
        self.svc.add("позвонить")
        result = self.svc.show_all()
        assert "позвонить" in result

    def test_delete(self):
        self.svc.add("удалить")
        result = self.svc.delete(1)
        assert "удалено" in result
        assert self.svc.show_all() == "Напоминаний нет"

    def test_delete_invalid_index(self):
        self.svc.add("тест")
        result = self.svc.delete(99)
        assert "Неверный номер" in result

    def test_parse_with_time(self):
        dt, text = self.svc.parse("напомни через 10 минут выключить чайник")
        assert text is not None
        assert dt is not None

    def test_parse_without_time(self):
        dt, text = self.svc.parse("напомни позвонить")
        assert text == "позвонить"
        assert dt is None
