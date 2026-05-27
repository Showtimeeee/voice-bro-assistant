import os
from assistant.notes import NotesManager, ReminderManager
from assistant import config


class TestNotesManager:
    def setup_method(self):
        self.path = config.FILE_PATHS['notes']
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


class TestReminderManager:
    def setup_method(self):
        self.path = config.FILE_PATHS['reminders']
        if os.path.exists(self.path):
            os.remove(self.path)
        self.mgr = ReminderManager()

    def test_empty_reminders(self):
        assert self.mgr.show_reminders() == "Напоминаний нет"

    def test_add_reminder(self):
        result = self.mgr.add_reminder("позвонить")
        assert result == "Напоминание добавлено"

    def test_show_reminders(self):
        self.mgr.add_reminder("напоминание 1")
        result = self.mgr.show_reminders()
        assert "напоминание 1" in result

    def test_delete_reminder(self):
        self.mgr.add_reminder("удалить")
        self.mgr.delete_reminder(1)
        assert self.mgr.show_reminders() == "Напоминаний нет"

    def test_persistence(self):
        self.mgr.add_reminder("сохранённое")
        mgr2 = ReminderManager()
        result = mgr2.show_reminders()
        assert "сохранённое" in result
